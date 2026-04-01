from pawpal_system import Task, Owner, DailyPlan, PRIORITY_RANK


class Scheduler:
    def generate_plan(self, owner: Owner, tasks: list[Task] | None = None) -> DailyPlan:
        """
        Generate a daily plan for the owner.

        Sorts tasks by priority (high → low) then duration (shorter first as tiebreak).
        Greedily schedules tasks that fit within the owner's available_minutes budget.
        Records reasoning for every include/skip decision.

        If tasks is provided, use that list directly.
        Otherwise, aggregate tasks from all of the owner's pets via get_all_tasks().
        """
        plan = DailyPlan()
        remaining = owner.available_minutes

        all_tasks = tasks if tasks is not None else owner.get_all_tasks()

        sorted_tasks = sorted(
            all_tasks,
            key=lambda t: (-PRIORITY_RANK[t.priority], t.duration_minutes)
        )

        for task in sorted_tasks:
            if task.duration_minutes <= remaining:
                plan.scheduled.append(task)
                remaining -= task.duration_minutes
                plan.total_minutes += task.duration_minutes
                plan.reasoning.append(
                    f"Added '{task.title}' ({task.duration_minutes} min, {task.priority} priority)"
                    f" — {remaining} min remaining."
                )
            else:
                plan.skipped.append(task)
                plan.reasoning.append(
                    f"Skipped '{task.title}' ({task.duration_minutes} min, {task.priority} priority)"
                    f" — only {remaining} min left."
                )

        return plan

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """
        Sort a list of Task objects by their start_time attribute in ascending order.

        Uses a lambda with sorted() to compare start times as "HH:MM" strings.
        Tasks with no start_time ("") are sorted to the end.
        """
        return sorted(
            tasks,
            key=lambda t: t.start_time if t.start_time else "99:99"
        )

    def filter_tasks(
        self,
        tasks: list[Task],
        completed: bool | None = None,
        pet_name: str | None = None,
        owner: Owner | None = None,
    ) -> list[Task]:
        """
        Filter tasks by completion status and/or pet name.

        Args:
            tasks: Flat list of Task objects to filter.
            completed: If True, return only completed tasks. If False, return only
                       incomplete tasks. If None, no completion filter is applied.
            pet_name: If provided, return only tasks belonging to this pet.
                      Requires owner to look up pet→task associations.
            owner: Required when filtering by pet_name.

        Returns a new list of Task objects matching all specified criteria.
        """
        result = list(tasks)

        if completed is not None:
            result = [t for t in result if t.completed == completed]

        if pet_name is not None and owner is not None:
            pet_tasks = set()
            for pet in owner.pets:
                if pet.name.lower() == pet_name.lower():
                    pet_tasks.update(id(t) for t in pet.tasks)
            result = [t for t in result if id(t) in pet_tasks]

        return result

    def detect_conflicts(self, tasks: list[Task]) -> list[str]:
        """
        Detect scheduling conflicts where two or more tasks share the same start_time.

        Uses a lightweight exact-match strategy: two tasks conflict if they have the
        same non-empty start_time. Returns a list of warning strings rather than
        raising an exception, so the program continues running.
        """
        warnings = []
        timed_tasks = [t for t in tasks if t.start_time]

        seen: dict[str, Task] = {}
        for task in timed_tasks:
            if task.start_time in seen:
                other = seen[task.start_time]
                warnings.append(
                    f"⚠ Conflict at {task.start_time}: "
                    f"'{task.title}' and '{other.title}' are scheduled at the same time."
                )
            else:
                seen[task.start_time] = task

        return warnings
