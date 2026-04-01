from pawpal_system import Task, Owner, DailyPlan, PRIORITY_RANK


class Scheduler:
    def generate_plan(self, owner: Owner, tasks: list[Task] | None = None) -> DailyPlan:
        """
        Generate a daily plan for the owner.
        If tasks is provided, use that list directly.
        Otherwise, aggregate tasks from all of the owner's pets.
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
