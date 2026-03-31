from dataclasses import dataclass, field
from typing import Literal

Priority = Literal["low", "medium", "high"]
PRIORITY_RANK = {"high": 3, "medium": 2, "low": 1}


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: Priority


@dataclass
class Pet:
    name: str
    species: str  # dog, cat, other


@dataclass
class Owner:
    name: str
    available_minutes: int = 120  # daily time budget in minutes


@dataclass
class DailyPlan:
    scheduled: list[Task] = field(default_factory=list)
    skipped: list[Task] = field(default_factory=list)
    reasoning: list[str] = field(default_factory=list)
    total_minutes: int = 0
