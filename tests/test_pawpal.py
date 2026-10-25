from datetime import date, timedelta

import pytest

from pawpal_system import Owner, Pet, Scheduler, Task, format_time

TODAY = date(2026, 10, 25)


def make_owner(minutes=120, **kwargs):
    owner = Owner("Jordan", available_minutes=minutes, **kwargs)
    owner.add_pet(Pet("Mochi", "dog"))
    return owner


def add(owner, title, duration, priority="medium", pet="Mochi", **kwargs):
    task = Task(title, duration, priority, due_date=kwargs.pop("due_date", TODAY), **kwargs)
    owner.get_pet(pet).add_task(task)
    return task


# --- Task validation ---------------------------------------------------------

def test_blank_title_rejected():
    with pytest.raises(ValueError):
        Task("   ", 10)


@pytest.mark.parametrize("kwargs", [{"duration_minutes": 0}, {"priority": "urgent"},
                                    {"frequency": "hourly"}, {"preferred_time": "25:99"}])
def test_invalid_task_fields_rejected(kwargs):
    base = {"title": "Walk", "duration_minutes": 10}
    with pytest.raises(ValueError):
        Task(**{**base, **kwargs})


def test_add_task_tags_pet_name():
    owner = make_owner()
    task = add(owner, "Walk", 20)
    assert task.pet_name == "Mochi"


def test_adding_task_increases_pet_task_count():
    pet = Pet("Mochi")
    assert len(pet.tasks) == 0
    pet.add_task(Task("Walk", 20))
    pet.add_task(Task("Feed", 10))
    assert len(pet.tasks) == 2


def test_duplicate_pet_name_rejected():
    owner = make_owner()
    with pytest.raises(ValueError):
        owner.add_pet(Pet("Mochi"))


# --- Sorting & filtering -----------------------------------------------------

def test_sort_by_priority_then_duration():
    tasks = [Task("a", 30, "low"), Task("b", 30, "high"), Task("c", 10, "high"), Task("d", 5, "medium")]
    assert [t.title for t in Scheduler.sort_by_priority(tasks)] == ["c", "b", "d", "a"]


def test_sort_by_time_puts_untimed_last():
    tasks = [Task("x", 5), Task("late", 5, preferred_time="18:00"), Task("early", 5, preferred_time="07:30")]
    assert [t.title for t in Scheduler.sort_by_time(tasks)] == ["early", "late", "x"]


def test_filter_by_pet_and_status():
    owner = make_owner()
    owner.add_pet(Pet("Luna", "cat"))
    walk = add(owner, "Walk", 20)
    add(owner, "Litter", 10, pet="Luna")
    walk.completed = True
    s = Scheduler(owner)
    assert [t.title for t in s.filter_tasks(pet_name="Luna")] == ["Litter"]
    assert [t.title for t in s.filter_tasks(completed=True)] == ["Walk"]


# --- Plan building -----------------------------------------------------------

def test_plan_respects_time_budget_and_priority():
    owner = make_owner(minutes=45)
    add(owner, "Walk", 30, "high")
    add(owner, "Play", 20, "low")
    add(owner, "Feed", 10, "high")
    plan = Scheduler(owner).build_plan(TODAY)
    assert {s.task.title for s in plan.scheduled} == {"Walk", "Feed"}
    assert [t.title for t, _ in plan.skipped] == ["Play"]
    assert plan.total_minutes <= 45


def test_smaller_task_still_fits_after_large_one_skipped():
    owner = make_owner(minutes=30)
    add(owner, "Long", 40, "high")
    add(owner, "Short", 10, "low")
    plan = Scheduler(owner).build_plan(TODAY)
    assert [s.task.title for s in plan.scheduled] == ["Short"]


def test_flexible_tasks_start_at_day_start_without_overlap():
    owner = make_owner(day_start="07:00")
    add(owner, "Walk", 30, "high")
    add(owner, "Feed", 10, "medium")
    plan = Scheduler(owner).build_plan(TODAY)
    assert [(format_time(s.start), s.task.title) for s in plan.scheduled] == [("07:00", "Walk"), ("07:30", "Feed")]


def test_fixed_time_honored_and_flexible_fills_around_it():
    owner = make_owner(day_start="08:00")
    add(owner, "Meds", 10, "high", preferred_time="08:00")
    add(owner, "Walk", 30, "medium")
    plan = Scheduler(owner).build_plan(TODAY)
    starts = {s.task.title: format_time(s.start) for s in plan.scheduled}
    assert starts == {"Meds": "08:00", "Walk": "08:10"}


def test_conflicting_fixed_times_warn_and_lower_priority_moves():
    owner = make_owner()
    owner.add_pet(Pet("Luna", "cat"))
    add(owner, "Walk", 30, "high", preferred_time="09:00")
    add(owner, "Brush", 15, "low", pet="Luna", preferred_time="09:15")
    plan = Scheduler(owner).build_plan(TODAY)
    assert len(plan.warnings) == 1 and "overlaps" in plan.warnings[0]
    starts = {s.task.title: format_time(s.start) for s in plan.scheduled}
    assert starts["Walk"] == "09:00"
    assert starts["Brush"] != "09:15"
    # nothing in the final plan overlaps
    ordered = sorted(plan.scheduled, key=lambda s: s.start)
    assert all(a.end <= b.start for a, b in zip(ordered, ordered[1:]))


def test_back_to_back_fixed_tasks_are_not_conflicts():
    a, b = Task("A", 30, preferred_time="09:00"), Task("B", 10, preferred_time="09:30")
    assert Scheduler.detect_conflicts([a, b]) == []


def test_tasks_at_exact_same_time_are_flagged():
    walk = Task("Walk", 30, preferred_time="08:00", pet_name="Mochi")
    meds = Task("Meds", 5, preferred_time="08:00", pet_name="Luna")
    conflicts = Scheduler.detect_conflicts([walk, meds])
    assert len(conflicts) == 1
    assert "Walk" in conflicts[0] and "Meds" in conflicts[0]


def test_every_scheduled_task_has_reason():
    owner = make_owner()
    add(owner, "Walk", 30, "high")
    plan = Scheduler(owner).build_plan(TODAY)
    assert "high priority" in plan.scheduled[0].reason


def test_empty_owner_gives_empty_plan():
    plan = Scheduler(make_owner()).build_plan(TODAY)
    assert plan.scheduled == [] and plan.skipped == []
    assert "nothing scheduled" in plan.to_text()


def test_tasks_outside_day_window_are_skipped():
    owner = make_owner(minutes=600, day_start="08:00", day_end="09:00")
    add(owner, "A", 45)
    add(owner, "B", 30)
    plan = Scheduler(owner).build_plan(TODAY)
    assert [s.task.title for s in plan.scheduled] == ["B"] or [s.task.title for s in plan.scheduled] == ["A"]
    assert len(plan.skipped) == 1


def test_future_and_completed_tasks_excluded():
    owner = make_owner()
    add(owner, "Tomorrow", 10, due_date=TODAY + timedelta(days=1))
    done = add(owner, "Done", 10)
    done.completed = True
    assert Scheduler(owner).build_plan(TODAY).scheduled == []


def test_overdue_task_carries_over():
    owner = make_owner()
    add(owner, "Vet call", 10, due_date=TODAY - timedelta(days=2))
    plan = Scheduler(owner).build_plan(TODAY)
    assert "overdue" in plan.scheduled[0].reason


# --- Recurrence --------------------------------------------------------------

@pytest.mark.parametrize("freq,delta", [("daily", 1), ("weekly", 7)])
def test_completing_recurring_task_creates_next(freq, delta):
    owner = make_owner()
    task = add(owner, "Feed", 10, frequency=freq)
    nxt = Scheduler(owner).complete_task(task)
    assert task.completed
    assert nxt.due_date == TODAY + timedelta(days=delta) and not nxt.completed
    assert nxt in owner.get_pet("Mochi").tasks
    assert [s.task for s in Scheduler(owner).build_plan(nxt.due_date).scheduled] == [nxt]


def test_completing_one_off_task_creates_nothing():
    owner = make_owner()
    task = add(owner, "Bath", 20)
    assert Scheduler(owner).complete_task(task) is None
    assert len(owner.get_pet("Mochi").tasks) == 1
