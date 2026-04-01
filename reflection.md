# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The system was designed around three core user actions:

1. **Set up owner & pet info** — The user enters their name, their pet's name and species, and how many minutes they have available that day. This establishes the scheduling constraint (time budget) and personalizes the experience. Represented by the `Owner` and `Pet` classes.

2. **Add care tasks** — The user defines what needs to be done by specifying a task title, duration in minutes, and priority level (low / medium / high). Each task is represented by the `Task` class, which holds exactly these three attributes.

3. **Generate a daily schedule** — The user triggers the scheduler, which selects and orders tasks based on priority and available time. The `Scheduler` class produces a `DailyPlan` that shows which tasks were scheduled, which were skipped, and the reasoning behind every decision.

The UML diagram includes five classes: `Task`, `Pet`, `Owner`, `DailyPlan`, and `Scheduler`. `Scheduler` depends on `Owner` and `Task` as inputs and produces a `DailyPlan`. `DailyPlan` holds references to scheduled and skipped `Task` objects. `Owner` is associated with one `Pet`.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

After reviewing the skeleton (`pawpal_system.py`) against the full requirements, several gaps were identified and the design was updated:

1. **`Task` was missing `frequency` and `completed`** — The initial design only tracked title, duration, and priority. To properly represent a care activity, `frequency: str` (e.g. "daily", "weekly") and `completed: bool` were added.

2. **`Pet` had no task list** — The initial `Pet` only stored name and species. A `tasks: list[Task]` field was added so each pet owns its own care tasks, matching the requirement that Pet "stores pet details and a list of tasks."

3. **`Owner` managed a single implicit pet, not multiple** — The initial design had no `pets` field. This was changed to `pets: list[Pet]` to support multiple pets. A `get_all_tasks()` method was also added to aggregate tasks across all pets, making `Owner` the entry point for the scheduler.

4. **`Scheduler` was updated to use `owner.get_all_tasks()`** — The `generate_plan()` method now accepts an optional `tasks` argument for backwards compatibility, but defaults to pulling tasks from `owner.get_all_tasks()`, making the scheduler truly pet-aware.

These changes were made because the original design did not fully reflect the intended responsibilities of each class.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers two main constraints: **time budget** (how many minutes the owner has available that day) and **task priority** (high, medium, or low). Tasks are ranked by priority first, then by duration as a tiebreaker — so if two tasks have the same priority, the shorter one gets scheduled first to maximize the number of tasks that fit.

I decided that time and priority mattered most because they map directly to the scenario: a busy pet owner can't do everything, so the system has to make a judgment call about what's most important. Preferences like species-specific rules or preferred time windows were noted as future improvements but left out of the first version to keep the logic focused and testable.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The conflict detection strategy checks for **exact start_time matches** rather than overlapping durations. For example, a 30-minute task starting at 08:00 and a 10-minute task starting at 08:15 would not be flagged as a conflict, even though they overlap.

This is a deliberate tradeoff: exact-match detection is simple, fast, and doesn't crash the program — it returns a warning string and lets the user decide what to do. A full overlap check would require tracking task end times and comparing intervals, which adds complexity without much practical benefit for a daily care planner where tasks are rarely scheduled with minute-level precision. For this scenario, the simpler approach is reasonable.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used Claude throughout the entire project — from drafting the initial UML and class stubs, to implementing the scheduling algorithm, to writing and running tests, to wiring everything into the Streamlit UI. The most effective Claude features were:

- **Plan mode** — Before writing any code, I asked Claude to explore the codebase and present an implementation plan for my approval. This let me catch design issues (like `Pet` not having a task list) before they became bugs.
- **Step-by-step execution** — I deliberately asked Claude to implement one layer at a time: models first, then scheduler, then tests, then UI. This kept each piece clean and verifiable before moving on.
- **Inline review** — I shared my skeleton (`pawpal_system.py`) and asked Claude to flag missing relationships and bottlenecks. It caught that `Owner` wasn't linked to `Pet` and that `DailyPlan` didn't store the original time budget — both real design gaps.
- **Targeted prompts** — The most useful prompts were specific: "how do I use a lambda to sort by HH:MM strings" or "implement conflict detection that returns warnings instead of crashing." Broad prompts like "make it better" were less useful.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When Claude first implemented `generate_plan()`, it accepted a flat `tasks` list directly without any connection to `owner.get_all_tasks()`. That meant the `Owner`/`Pet` relationship existed in the data model but was completely bypassed by the scheduler — the UI was just passing raw dictionaries from session state instead of real `Task` objects tied to a `Pet`.

I pushed back on this and asked Claude to update `generate_plan()` so it could pull tasks from the owner's pets by default, while still accepting a direct task list for backwards compatibility. I verified the fix by running `main.py` in the terminal with two pets and confirming that tasks from both pets appeared in the plan — not just a manually passed list. That test proved the multi-pet architecture was actually wired end-to-end, not just on paper.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I wrote 10 tests covering: all tasks fitting within budget, low-priority tasks being skipped first, priority ordering, a single task exceeding the full budget, an empty task list, marking a task complete, adding a task to a pet, sorting by start time, daily recurrence creating the next day's task, and conflict detection flagging duplicate start times.

These tests mattered because the scheduler makes real decisions — it drops tasks and explains why. Without tests, I had no way to know if a change to the sorting logic accidentally broke priority ordering, or if the recurrence feature was creating tasks with the wrong date. Tests made refactoring safe and gave me confidence that each feature worked independently before I connected them in the UI.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

**4 / 5** — I'm confident in the core scheduling, sorting, recurrence, and conflict detection. The one gap is overlap-based conflict detection: right now two tasks at 08:00 and 08:15 won't be flagged even if the first one runs 30 minutes. With more time I'd add duration-aware overlap checking and test edge cases like tasks that span midnight, tasks with identical titles but different pets, and weekly recurrence across month boundaries.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The part I'm most satisfied with is how the system design actually held together end-to-end. When I ran `main.py` and saw tasks from two different pets being sorted, scheduled, and explained in plain language — all flowing through classes I designed — it felt like the architecture actually worked, not just in theory but in practice. The fact that the tests passed without any patches or workarounds was also a good sign that the logic was clean from the start.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I'd give `DailyPlan` a reference back to the `Owner` so it's self-contained and doesn't require the UI to pass `available_minutes` separately. I'd also add duration-aware conflict detection and species-specific task defaults (e.g. dogs need daily walks, cats need enrichment but not walks). And I'd update the Streamlit UI to support multiple pets directly — right now the UI assumes one pet even though the backend supports many.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The most important thing I learned is that AI is a fast executor but a poor architect — and the difference matters. Claude could implement any method I described almost instantly, but it had no sense of whether the overall design was coherent. When I let it fill in blanks without a clear spec, it made reasonable-looking choices that quietly broke the architecture (like bypassing `get_all_tasks()` and passing raw dicts instead). The moment I stepped in as the lead architect — reviewing plans before approving them, catching that `Owner` wasn't linked to `Pet`, pushing back on the flat task list — the system became genuinely well-structured. AI amplified my speed, but only my judgment kept the design clean.
