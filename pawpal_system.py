"""Core logic for PawPal+: owners, pets, care tasks, and the daily scheduler."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date, datetime, timedelta
from typing import Optional

PRIORITY_RANK = {"high": 3, "medium": 2, "low": 1}
FREQUENCIES = ("once", "daily", "weekly")


def parse_time(value: str) -> int:
    """Convert "HH:MM" to minutes after midnight."""
    try:
        parsed = datetime.strptime(value.strip(), "%H:%M")
    except (ValueError, AttributeError) as exc:
        raise ValueError(f"Invalid time {value!r}; expected HH:MM") from exc
    return parsed.hour * 60 + parsed.minute


def format_time(minutes: int) -> str:
    """Convert minutes after midnight to "HH:MM"."""
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


@dataclass
class Task:
    """A single pet care activity."""

    title: str
    duration_minutes: int
    priority: str = "medium"
    preferred_time: Optional[str] = None  # "HH:MM" if the task should happen at a set time
    frequency: str = "once"
    due_date: date = field(default_factory=date.today)
    completed: bool = False
    pet_name: str = ""

    def __post_init__(self) -> None:
        self.title = self.title.strip()
        if not self.title:
            raise ValueError("Task title cannot be blank")
        if self.duration_minutes <= 0:
            raise ValueError("Duration must be a positive number of minutes")
        if self.priority not in PRIORITY_RANK:
            raise ValueError(f"Priority must be one of {list(PRIORITY_RANK)}")
        if self.frequency not in FREQUENCIES:
            raise ValueError(f"Frequency must be one of {list(FREQUENCIES)}")
        if self.preferred_time is not None:
            self.preferred_time = self.preferred_time.strip() or None
        if self.preferred_time is not None:
            parse_time(self.preferred_time)  # validate format

    @property
    def priority_rank(self) -> int:
        return PRIORITY_RANK[self.priority]

    def is_due(self, on: date) -> bool:
        """A task is due if it is not done and its due date has arrived (overdue tasks carry over)."""
        return not self.completed and self.due_date <= on

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task done; for recurring tasks, return the next occurrence."""
        self.completed = True
        if self.frequency == "daily":
            return replace(self, completed=False, due_date=self.due_date + timedelta(days=1))
        if self.frequency == "weekly":
            return replace(self, completed=False, due_date=self.due_date + timedelta(weeks=1))
        return None


@dataclass
class Pet:
    """A pet and the care tasks it needs."""

    name: str
    species: str = "dog"
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        self.tasks.remove(task)


@dataclass
class Owner:
    """The pet owner, their pets, and their daily constraints."""

    name: str
    available_minutes: int = 120
    day_start: str = "08:00"
    day_end: str = "21:00"
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        if self.get_pet(pet.name) is not None:
            raise ValueError(f"A pet named {pet.name!r} already exists")
        self.pets.append(pet)

    def get_pet(self, name: str) -> Optional[Pet]:
        return next((p for p in self.pets if p.name == name), None)

    def all_tasks(self) -> list[Task]:
        return [t for pet in self.pets for t in pet.tasks]


@dataclass
class ScheduledTask:
    task: Task
    start: int  # minutes after midnight
    reason: str

    @property
    def end(self) -> int:
        return self.start + self.task.duration_minutes


@dataclass
class DailyPlan:
    """The result of scheduling one day."""

    day: date
    scheduled: list[ScheduledTask] = field(default_factory=list)
    skipped: list[tuple[Task, str]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def total_minutes(self) -> int:
        return sum(s.task.duration_minutes for s in self.scheduled)

    def to_text(self) -> str:
        lines = [f"Daily plan for {self.day.isoformat()}:"]
        for s in self.scheduled:
            t = s.task
            lines.append(
                f"  {format_time(s.start)}-{format_time(s.end)} - {t.title} ({t.pet_name}, "
                f"{t.duration_minutes} min) [priority: {t.priority}]"
            )
            lines.append(f"      why: {s.reason}")
        if not self.scheduled:
            lines.append("  (nothing scheduled)")
        for t, why in self.skipped:
            lines.append(f"  SKIPPED {t.title} ({t.pet_name}): {why}")
        for w in self.warnings:
            lines.append(f"  WARNING: {w}")
        return "\n".join(lines)


class Scheduler:
    """Builds a daily plan for an owner's pets within their time budget."""

    def __init__(self, owner: Owner):
        self.owner = owner

    # --- sorting and filtering -------------------------------------------------

    @staticmethod
    def sort_by_priority(tasks: list[Task]) -> list[Task]:
        """Highest priority first; ties go to tasks with a set time, then earlier time, then shorter."""
        return sorted(
            tasks,
            key=lambda t: (
                -t.priority_rank,
                t.preferred_time is None,
                parse_time(t.preferred_time) if t.preferred_time else 0,
                t.duration_minutes,
            ),
        )

    @staticmethod
    def sort_by_time(tasks: list[Task]) -> list[Task]:
        """Tasks with a preferred time in chronological order; untimed tasks last."""
        return sorted(tasks, key=lambda t: parse_time(t.preferred_time) if t.preferred_time else 24 * 60)

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
        due_on: Optional[date] = None,
    ) -> list[Task]:
        tasks = self.owner.all_tasks()
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name == pet_name]
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        if due_on is not None:
            tasks = [t for t in tasks if t.is_due(due_on)]
        return tasks

    # --- conflicts -------------------------------------------------------------

    @staticmethod
    def detect_conflicts(tasks: list[Task]) -> list[str]:
        """Report pairs of fixed-time tasks whose time slots overlap."""
        timed = Scheduler.sort_by_time([t for t in tasks if t.preferred_time])
        conflicts = []
        for i, a in enumerate(timed):
            a_start = parse_time(a.preferred_time)
            for b in timed[i + 1:]:
                b_start = parse_time(b.preferred_time)
                if b_start >= a_start + a.duration_minutes:
                    break
                conflicts.append(
                    f"'{a.title}' ({a.pet_name}, {a.preferred_time}) overlaps "
                    f"'{b.title}' ({b.pet_name}, {b.preferred_time})"
                )
        return conflicts

    # --- recurrence ------------------------------------------------------------

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task done and add its next occurrence to the same pet if it recurs."""
        next_task = task.mark_complete()
        if next_task is not None:
            pet = self.owner.get_pet(task.pet_name)
            if pet is not None:
                pet.add_task(next_task)
        return next_task

    # --- planning --------------------------------------------------------------

    def build_plan(self, day: Optional[date] = None) -> DailyPlan:
        """Choose tasks by priority within the time budget, then place them on the clock.

        1. Due tasks are sorted by priority (see sort_by_priority).
        2. Tasks are accepted greedily while they fit the owner's available minutes.
        3. Accepted fixed-time tasks are placed at their preferred time; if that slot is taken
           or outside the day window, they fall back to the next free slot.
        4. Flexible tasks fill the earliest free gaps starting at the owner's day start.
        """
        day = day or date.today()
        plan = DailyPlan(day=day)
        day_start = parse_time(self.owner.day_start)
        day_end = parse_time(self.owner.day_end)
        if day_end <= day_start:
            raise ValueError("Day end must be after day start")

        due = self.sort_by_priority(self.filter_tasks(due_on=day))
        plan.warnings.extend(self.detect_conflicts(due))

        budget = self.owner.available_minutes
        accepted: list[Task] = []
        for task in due:
            if task.duration_minutes <= budget:
                accepted.append(task)
                budget -= task.duration_minutes
            else:
                plan.skipped.append(
                    (task, f"needs {task.duration_minutes} min but only {budget} min of your time is left")
                )

        busy: list[tuple[int, int]] = []

        def is_free(start: int, end: int) -> bool:
            return start >= day_start and end <= day_end and all(end <= b0 or start >= b1 for b0, b1 in busy)

        def first_free_slot(length: int) -> Optional[int]:
            candidates = sorted({day_start} | {b1 for _, b1 in busy})
            for start in candidates:
                if is_free(start, start + length):
                    return start
            return None

        def place(task: Task, start: int, reason: str) -> None:
            busy.append((start, start + task.duration_minutes))
            plan.scheduled.append(ScheduledTask(task, start, reason))

        def base_reason(task: Task) -> str:
            why = f"{task.priority} priority"
            if task.due_date < day:
                why += f", overdue since {task.due_date.isoformat()}"
            if task.frequency != "once":
                why += f", recurs {task.frequency}"
            return why

        fixed = [t for t in accepted if t.preferred_time]
        flexible = [t for t in accepted if not t.preferred_time]

        for task in fixed:  # already in priority order, so higher priority wins a contested slot
            wanted = parse_time(task.preferred_time)
            if is_free(wanted, wanted + task.duration_minutes):
                place(task, wanted, f"{base_reason(task)}; at your preferred time {task.preferred_time}")
                continue
            slot = first_free_slot(task.duration_minutes)
            if slot is None:
                plan.skipped.append((task, "no free slot left in your day window"))
                continue
            place(
                task,
                slot,
                f"{base_reason(task)}; moved from {task.preferred_time} because that slot was taken "
                f"or outside your day",
            )

        for task in flexible:
            slot = first_free_slot(task.duration_minutes)
            if slot is None:
                plan.skipped.append((task, "no free slot left in your day window"))
                continue
            place(task, slot, f"{base_reason(task)}; placed in the earliest free slot")

        plan.scheduled.sort(key=lambda s: s.start)
        return plan
