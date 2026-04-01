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

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
