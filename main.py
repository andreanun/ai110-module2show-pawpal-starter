from pawpal_system import Task, Pet, Owner
from scheduler import Scheduler

scheduler = Scheduler()

# --- Setup: tasks added OUT OF ORDER by start_time ---
mochi_tasks = [
    Task(title="Enrichment puzzle", duration_minutes=20, priority="medium",
         frequency="daily", start_time="15:00"),
    Task(title="Morning walk",      duration_minutes=30, priority="high",
         frequency="daily", start_time="07:00"),
    Task(title="Feeding",           duration_minutes=10, priority="high",
         frequency="daily", start_time="08:00"),
]

garfield_tasks = [
    Task(title="Vet checkup",  duration_minutes=60, priority="low",
         frequency="as needed", start_time="10:00"),
    Task(title="Brush coat",   duration_minutes=15, priority="medium",
         frequency="weekly",   start_time="09:00"),
    # Intentional conflict: same start_time as Mochi's Feeding
    Task(title="Feeding",      duration_minutes=10, priority="high",
         frequency="daily",    start_time="08:00"),
]

mochi   = Pet(name="Mochi",    species="dog", tasks=mochi_tasks)
garfield = Pet(name="Garfield", species="cat", tasks=garfield_tasks)
owner   = Owner(name="Jordan", available_minutes=120, pets=[mochi, garfield])

all_tasks = owner.get_all_tasks()

# --- 1. Sort by time ---
print("=" * 45)
print("  TASKS SORTED BY START TIME")
print("=" * 45)
sorted_tasks = scheduler.sort_by_time(all_tasks)
for t in sorted_tasks:
    time_label = t.start_time if t.start_time else "no time"
    print(f"  {time_label}  {t.title} ({t.duration_minutes} min, {t.priority})")

# --- 2. Conflict detection ---
print("\n" + "=" * 45)
print("  CONFLICT DETECTION")
print("=" * 45)
conflicts = scheduler.detect_conflicts(all_tasks)
if conflicts:
    for warning in conflicts:
        print(f"  {warning}")
else:
    print("  No conflicts detected.")

# --- 3. Filter: incomplete tasks only ---
print("\n" + "=" * 45)
print("  INCOMPLETE TASKS")
print("=" * 45)
incomplete = scheduler.filter_tasks(all_tasks, completed=False)
for t in incomplete:
    print(f"  ○ {t.title}")

# --- 4. Filter: tasks for Mochi only ---
print("\n" + "=" * 45)
print("  MOCHI'S TASKS ONLY")
print("=" * 45)
mochi_only = scheduler.filter_tasks(all_tasks, pet_name="Mochi", owner=owner)
for t in mochi_only:
    print(f"  • {t.title}")

# --- 5. Recurring task auto-creation ---
print("\n" + "=" * 45)
print("  RECURRING TASK DEMO")
print("=" * 45)
walk = mochi_tasks[1]  # Morning walk (daily)
print(f"  Completing '{walk.title}' due {walk.due_date} ...")
next_task = walk.mark_complete()
print(f"  Task completed: {walk.completed}")
if next_task:
    print(f"  Next occurrence auto-created: '{next_task.title}' due {next_task.due_date}")

# --- 6. Daily plan ---
print("\n" + "=" * 45)
print("  TODAY'S SCHEDULE FOR JORDAN")
print("=" * 45)
plan = scheduler.generate_plan(owner)
print(f"\n  Time budget : {owner.available_minutes} min")
print(f"  Pets        : {', '.join(p.name for p in owner.pets)}\n")

print("  Scheduled:")
for t in plan.scheduled:
    print(f"    ✓ {t.title} ({t.duration_minutes} min, {t.priority})")

print(f"\n  Total: {plan.total_minutes} / {owner.available_minutes} min")

if plan.skipped:
    print("\n  Skipped:")
    for t in plan.skipped:
        print(f"    ✗ {t.title} ({t.duration_minutes} min, {t.priority})")

print("\n  Reasoning:")
for r in plan.reasoning:
    print(f"    • {r}")

print("=" * 45)
