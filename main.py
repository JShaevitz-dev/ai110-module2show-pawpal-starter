"""Terminal demo for PawPal+: builds a sample owner, pets, and tasks, then prints the plan."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def print_tasks(heading: str, tasks: list[Task]) -> None:
    print(heading)
    for t in tasks:
        when = t.preferred_time or "flexible"
        status = "done" if t.completed else "open"
        print(f"  {when:>8}  {t.title:<14} {t.pet_name:<7} {t.duration_minutes:>3} min  "
              f"[{t.priority}] ({status})")
    print()


def main() -> None:
    today = date.today()
    owner = Owner("Jordan", available_minutes=90, day_start="07:00", day_end="21:00")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    # Added out of order on purpose; Meds and Morning walk share 08:00 to show a conflict.
    mochi.add_task(Task("Evening walk", 30, "medium", preferred_time="18:00", frequency="daily", due_date=today))
    luna.add_task(Task("Brushing", 15, "low", frequency="weekly", due_date=today))
    mochi.add_task(Task("Morning walk", 30, "high", preferred_time="08:00", frequency="daily", due_date=today))
    luna.add_task(Task("Meds", 5, "high", preferred_time="08:00", due_date=today))
    mochi.add_task(Task("Feeding", 10, "high", frequency="daily", due_date=today))
    luna.add_task(Task("Play session", 20, "medium", due_date=today))

    scheduler = Scheduler(owner)

    print("=== Today's Schedule ===")
    print(f"Owner: {owner.name} | {owner.available_minutes} min available | "
          f"day {owner.day_start}-{owner.day_end}")
    print(scheduler.build_plan(today).to_text())
    print()

    print_tasks("=== All tasks sorted by time ===", Scheduler.sort_by_time(owner.all_tasks()))
    print_tasks("=== All tasks sorted by priority ===", Scheduler.sort_by_priority(owner.all_tasks()))
    print_tasks("=== Filter: Luna's tasks ===", scheduler.filter_tasks(pet_name="Luna"))

    print("=== Conflict check ===")
    conflicts = Scheduler.detect_conflicts(owner.all_tasks())
    for c in conflicts:
        print(f"  WARNING: {c}")
    if not conflicts:
        print("  No conflicts.")
    print()

    print("=== Recurring task ===")
    feeding = next(t for t in mochi.tasks if t.title == "Feeding")
    next_feeding = scheduler.complete_task(feeding)
    print(f"  Marked '{feeding.title}' complete; next one due {next_feeding.due_date.isoformat()}")
    print()
    print_tasks("=== Filter: completed tasks ===", scheduler.filter_tasks(completed=True))


if __name__ == "__main__":
    main()
