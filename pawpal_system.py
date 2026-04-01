from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Literal

Priority = Literal["low", "medium", "high"]
PRIORITY_RANK = {"high": 3, "medium": 2, "low": 1}


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: Priority
    frequency: str = "daily"      # "daily", "weekly", "as needed"
    completed: bool = False
    start_time: str = ""          # "HH:MM" format, empty means no fixed time
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> "Task | None":
        """
        Mark this task as complete.

        For recurring tasks (daily or weekly), automatically creates and returns
        a new Task instance scheduled for the next occurrence using timedelta.
        Returns None for non-recurring tasks.
        """
        self.completed = True
        if self.frequency == "daily":
            return Task(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                frequency=self.frequency,
                start_time=self.start_time,
                due_date=self.due_date + timedelta(days=1),
            )
        if self.frequency == "weekly":
            return Task(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                frequency=self.frequency,
                start_time=self.start_time,
                due_date=self.due_date + timedelta(weeks=1),
            )
        return None


@dataclass
class Pet:
    name: str
    species: str  # dog, cat, other
    tasks: list[Task] = field(default_factory=list)


@dataclass
class Owner:
    name: str
    available_minutes: int = 120  # daily time budget in minutes
    pets: list[Pet] = field(default_factory=list)

    def get_all_tasks(self) -> list[Task]:
        """Aggregate all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


@dataclass
class DailyPlan:
    scheduled: list[Task] = field(default_factory=list)
    skipped: list[Task] = field(default_factory=list)
    reasoning: list[str] = field(default_factory=list)
    total_minutes: int = 0
