import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models import Task, Owner
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
