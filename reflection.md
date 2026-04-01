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

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
