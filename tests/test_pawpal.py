import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner
from scheduler import Scheduler


def make_task(title, duration, priority):
    return Task(title=title, duration_minutes=duration, priority=priority)


def test_all_tasks_fit():
    """All tasks scheduled when total duration fits within budget."""
    owner = Owner(name="Jordan", available_minutes=120)
    tasks = [
        make_task("Walk", 20, "high"),
        make_task("Feeding", 10, "high"),
        make_task("Playtime", 30, "medium"),
    ]
    plan = Scheduler().generate_plan(owner, tasks)
    assert len(plan.scheduled) == 3
    assert len(plan.skipped) == 0
    assert plan.total_minutes == 60


def test_low_priority_skipped_first():
    """When budget is tight, low-priority tasks are skipped before high-priority ones."""
    owner = Owner(name="Jordan", available_minutes=30)
    tasks = [
        make_task("Walk", 20, "high"),
        make_task("Grooming", 20, "low"),
    ]
    plan = Scheduler().generate_plan(owner, tasks)
    scheduled_titles = [t.title for t in plan.scheduled]
    skipped_titles = [t.title for t in plan.skipped]
    assert "Walk" in scheduled_titles
    assert "Grooming" in skipped_titles


def test_priority_ordering():
    """High-priority tasks are scheduled before medium, regardless of insertion order."""
    owner = Owner(name="Jordan", available_minutes=120)
    tasks = [
        make_task("Enrichment", 30, "medium"),
        make_task("Meds", 5, "high"),
    ]
    plan = Scheduler().generate_plan(owner, tasks)
    assert plan.scheduled[0].title == "Meds"
    assert plan.scheduled[1].title == "Enrichment"


def test_single_task_larger_than_budget():
    """A task larger than the total budget is skipped with a reason."""
    owner = Owner(name="Jordan", available_minutes=10)
    tasks = [make_task("Long grooming", 60, "high")]
    plan = Scheduler().generate_plan(owner, tasks)
    assert len(plan.scheduled) == 0
    assert len(plan.skipped) == 1
    assert any("Skipped" in r for r in plan.reasoning)


def test_empty_task_list():
    """Empty task list returns an empty plan without errors."""
    owner = Owner(name="Jordan", available_minutes=120)
    plan = Scheduler().generate_plan(owner, [])
    assert plan.scheduled == []
    assert plan.skipped == []
    assert plan.total_minutes == 0


def test_mark_complete_changes_status():
    """Calling mark_complete() sets completed to True."""
    task = Task(title="Morning walk", duration_minutes=30, priority="high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    """Adding a task to a Pet increases its task count."""
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.tasks) == 0
    pet.tasks.append(Task(title="Feeding", duration_minutes=10, priority="high"))
    assert len(pet.tasks) == 1


def test_sort_by_time_returns_chronological_order():
    """Tasks with start_time are sorted in ascending HH:MM order; no-time tasks go last."""
    tasks = [
        Task(title="Afternoon play", duration_minutes=20, priority="medium", start_time="15:00"),
        Task(title="Morning walk",   duration_minutes=30, priority="high",   start_time="07:00"),
        Task(title="Feeding",        duration_minutes=10, priority="high",   start_time="08:00"),
        Task(title="No time task",   duration_minutes=5,  priority="low",    start_time=""),
    ]
    sorted_tasks = Scheduler().sort_by_time(tasks)
    times = [t.start_time if t.start_time else "99:99" for t in sorted_tasks]
    assert times == sorted(times)
    assert sorted_tasks[-1].title == "No time task"


def test_daily_recurrence_creates_next_day_task():
    """Marking a daily task complete returns a new task due the following day."""
    today = date.today()
    task = Task(title="Morning walk", duration_minutes=30, priority="high",
                frequency="daily", due_date=today)
    next_task = task.mark_complete()
    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.completed is False


def test_conflict_detection_flags_duplicate_times():
    """Scheduler warns when two tasks share the same start_time."""
    tasks = [
        Task(title="Feeding",    duration_minutes=10, priority="high", start_time="08:00"),
        Task(title="Medication", duration_minutes=5,  priority="high", start_time="08:00"),
        Task(title="Walk",       duration_minutes=30, priority="high", start_time="07:00"),
    ]
    warnings = Scheduler().detect_conflicts(tasks)
    assert len(warnings) == 1
    assert "08:00" in warnings[0]
    assert "Feeding" in warnings[0] or "Medication" in warnings[0]
