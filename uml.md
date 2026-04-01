# PawPal+ UML Class Diagram

```mermaid
classDiagram
    class Task {
        +str title
        +int duration_minutes
        +Priority priority
    }

    class Pet {
        +str name
        +str species
    }

    class Owner {
        +str name
        +int available_minutes
    }

    class DailyPlan {
        +list~Task~ scheduled
        +list~Task~ skipped
        +list~str~ reasoning
        +int total_minutes
    }

    class Scheduler {
        +generate_plan(owner: Owner, tasks: list~Task~) DailyPlan
    }

    Scheduler --> Owner : uses
    Scheduler --> Task : uses
    Scheduler --> DailyPlan : produces
    DailyPlan "1" --> "*" Task : scheduled / skipped
    Owner "1" -- "1" Pet : owns
```

## Relationships

- `Scheduler` takes an `Owner` and a list of `Task` objects → produces a `DailyPlan`
- `DailyPlan` holds references to `Task` objects (scheduled and skipped)
- `Owner` is associated with a `Pet` (one owner, one pet in current scope)
```
