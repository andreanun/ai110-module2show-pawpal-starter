from models import Task, Owner, DailyPlan, PRIORITY_RANK


class Scheduler:
    def generate_plan(self, owner: Owner, tasks: list[Task]) -> DailyPlan:
        plan = DailyPlan()
        remaining = owner.available_minutes

        sorted_tasks = sorted(
            tasks,
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
