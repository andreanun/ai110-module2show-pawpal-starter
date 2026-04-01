# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Smarter Scheduling

Beyond the basic greedy planner, the scheduler includes three additional capabilities:

- **Sort by time** — `Scheduler.sort_by_time(tasks)` sorts any task list by `start_time` (HH:MM) using a lambda key, placing tasks with no fixed time at the end.
- **Filter tasks** — `Scheduler.filter_tasks(tasks, completed=, pet_name=, owner=)` returns tasks matching a completion status and/or a specific pet's task list.
- **Conflict detection** — `Scheduler.detect_conflicts(tasks)` checks for exact `start_time` collisions and returns human-readable warning strings instead of crashing.
- **Recurring task auto-creation** — Calling `task.mark_complete()` on a `daily` or `weekly` task returns a new `Task` instance scheduled for the next occurrence, calculated with Python's `timedelta`.

## Testing PawPal+

### Run the tests

```bash
python3 -m pytest tests/test_pawpal.py -v
```

### What the tests cover

| Test | What it verifies |
|---|---|
| `test_all_tasks_fit` | All tasks are scheduled when the total duration fits within the time budget |
| `test_low_priority_skipped_first` | Low-priority tasks are dropped before high-priority ones when time runs out |
| `test_priority_ordering` | High-priority tasks appear before medium-priority tasks in the schedule |
| `test_single_task_larger_than_budget` | A task that exceeds the full budget is skipped with a recorded reason |
| `test_empty_task_list` | An empty task list returns a valid empty plan without errors |
| `test_mark_complete_changes_status` | Calling `mark_complete()` sets `completed` to `True` |
| `test_adding_task_increases_pet_task_count` | Appending a task to a `Pet` correctly increases its task count |
| `test_sort_by_time_returns_chronological_order` | Tasks are sorted in ascending HH:MM order; tasks with no time go last |
| `test_daily_recurrence_creates_next_day_task` | Completing a daily task auto-creates a new task due the following day |
| `test_conflict_detection_flags_duplicate_times` | The scheduler warns when two tasks share the same `start_time` |

### Confidence level

**4 / 5 stars**

The core scheduling, sorting, conflict detection, and recurrence logic are all tested and passing. One star is held back because conflict detection only checks for exact `start_time` matches — overlapping durations (e.g. a 30-min task at 08:00 and a 10-min task at 08:15) are not yet caught. That edge case would require additional tests and a duration-aware conflict algorithm.

---

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
