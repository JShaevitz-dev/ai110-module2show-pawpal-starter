# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Features

- **Owner settings** - how many minutes you have today, plus when your day starts and ends.
- **Multiple pets** - each pet has its own task list; blank and duplicate pet names are rejected.
- **Task management** - add, edit, mark complete, and delete tasks. Each task has a duration,
  priority (low/medium/high), optional set time, repeat setting (once/daily/weekly), and due date.
  Blank titles and duplicate open tasks are rejected.
- **Priority scheduling within a time budget** - tasks are chosen highest priority first until your
  available minutes run out; a task that doesn't fit is skipped, but shorter ones after it can still fit.
- **Set times and flexible tasks** - tasks with a set time go at that time; flexible tasks fill the
  earliest free gaps in your day.
- **Conflict handling** - overlapping set times produce a warning. The higher-priority task keeps the
  slot and the other moves to the next free time after it.
- **Explanations** - every scheduled task says why it was placed where it is, and every skipped task
  says why it was left out.
- **Sorting and filtering** - view tasks sorted by time or priority, filtered by pet or by status.
- **Recurring tasks** - completing a daily or weekly task creates the next one automatically;
  overdue tasks carry over to today.
- **CLI demo** - `main.py` runs the same logic in the terminal.

## 🖥️ Sample Output

Output of `python main.py` (the dates depend on the day you run it):

```
=== Today's Schedule ===
Owner: Jordan | 90 min available | day 07:00-21:00
Daily plan for 2026-11-01:
  07:00-07:10 - Feeding (Mochi, 10 min) [priority: high]
      why: high priority, recurs daily; placed in the earliest free slot
  07:10-07:25 - Brushing (Luna, 15 min) [priority: low]
      why: low priority, recurs weekly; placed in the earliest free slot
  08:00-08:05 - Meds (Luna, 5 min) [priority: high]
      why: high priority; at your preferred time 08:00
  08:05-08:35 - Morning walk (Mochi, 30 min) [priority: high]
      why: high priority, recurs daily; moved from 08:00 to 08:05 because 'Meds' already had that time
  18:00-18:30 - Evening walk (Mochi, 30 min) [priority: medium]
      why: medium priority, recurs daily; at your preferred time 18:00
  SKIPPED Play session (Luna): needs 20 min but only 15 min of your time is left
  WARNING: 'Meds' (Luna, 08:00) overlaps 'Morning walk' (Mochi, 08:00)

=== All tasks sorted by time ===
     08:00  Morning walk   Mochi    30 min  [high] (open)
     08:00  Meds           Luna      5 min  [high] (open)
     18:00  Evening walk   Mochi    30 min  [medium] (open)
  flexible  Feeding        Mochi    10 min  [high] (open)
  flexible  Brushing       Luna     15 min  [low] (open)
  flexible  Play session   Luna     20 min  [medium] (open)

=== All tasks sorted by priority ===
     08:00  Meds           Luna      5 min  [high] (open)
     08:00  Morning walk   Mochi    30 min  [high] (open)
  flexible  Feeding        Mochi    10 min  [high] (open)
     18:00  Evening walk   Mochi    30 min  [medium] (open)
  flexible  Play session   Luna     20 min  [medium] (open)
  flexible  Brushing       Luna     15 min  [low] (open)

=== Filter: Luna's tasks ===
  flexible  Brushing       Luna     15 min  [low] (open)
     08:00  Meds           Luna      5 min  [high] (open)
  flexible  Play session   Luna     20 min  [medium] (open)

=== Conflict check ===
  WARNING: 'Morning walk' (Mochi, 08:00) overlaps 'Meds' (Luna, 08:00)

=== Recurring task ===
  Marked 'Feeding' complete; next one due 2026-11-02

=== Filter: completed tasks ===
  flexible  Feeding        Mochi    10 min  [high] (done)
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
python -m pytest --cov
```

The suite (`tests/test_pawpal.py`, 28 tests) covers:

- **Validation** - blank titles, invalid durations, priorities, repeat settings, and times are rejected;
  duplicate pet names are rejected; adding tasks increases a pet's task count.
- **Sorting and filtering** - chronological order by time (flexible tasks last), priority order with
  tie-breaks, and filtering by pet and by completion status.
- **Scheduling** - the time budget is respected, higher priority wins, flexible tasks start at the
  day start without overlapping, set times are honored, tasks outside the day window are skipped,
  and every scheduled task has a reason.
- **Conflicts** - overlapping and exactly matching set times are flagged; back-to-back tasks are not;
  a bumped task moves later (or earlier only if nothing later fits).
- **Recurrence and due dates** - completing a daily or weekly task creates the next one 1 or 7 days
  later, one-off tasks don't repeat, future and completed tasks are left out, and overdue tasks carry over.

**Confidence level: 4/5 (\*\*\*\*)** - all 28 tests pass and cover 96% of `pawpal_system.py`. The
Streamlit UI was checked by hand and with Streamlit's test harness rather than by the automated suite.

Test run (`python -m pytest`):

```
============================= test session starts =============================
platform win32 -- Python 3.10.11, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Coldfur\Documents\Code\pawpal-repo
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.13.0, hydra-core-1.3.2, cov-7.1.0
collected 28 items

tests\test_pawpal.py ............................                        [100%]

============================= 28 passed in 0.04s ==============================
```

Coverage run (`python -m pytest --cov`):

```
============================= test session starts =============================
platform win32 -- Python 3.10.11, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Coldfur\Documents\Code\pawpal-repo
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.13.0, hydra-core-1.3.2, cov-7.1.0
collected 28 items

tests\test_pawpal.py ............................                        [100%]

=============================== tests coverage ================================
______________ coverage: platform win32, python 3.10.11-final-0 _______________

Name                   Stmts   Miss  Cover
------------------------------------------
pawpal_system.py         202      9    96%
tests\test_pawpal.py     155      0   100%
------------------------------------------
TOTAL                    357      9    97%
============================= 28 passed in 0.14s ==============================
```

Sample test output (`python -m pytest -v`):

```
============================= test session starts =============================
platform win32 -- Python 3.10.11, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\Coldfur\AppData\Local\Programs\Python\Python310\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Coldfur\Documents\Code\pawpal-repo
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.13.0, hydra-core-1.3.2, cov-7.1.0
collecting ... collected 28 items

tests/test_pawpal.py::test_blank_title_rejected PASSED                   [  3%]
tests/test_pawpal.py::test_invalid_task_fields_rejected[kwargs0] PASSED  [  7%]
tests/test_pawpal.py::test_invalid_task_fields_rejected[kwargs1] PASSED  [ 10%]
tests/test_pawpal.py::test_invalid_task_fields_rejected[kwargs2] PASSED  [ 14%]
tests/test_pawpal.py::test_invalid_task_fields_rejected[kwargs3] PASSED  [ 17%]
tests/test_pawpal.py::test_add_task_tags_pet_name PASSED                 [ 21%]
tests/test_pawpal.py::test_adding_task_increases_pet_task_count PASSED   [ 25%]
tests/test_pawpal.py::test_duplicate_pet_name_rejected PASSED            [ 28%]
tests/test_pawpal.py::test_sort_by_priority_then_duration PASSED         [ 32%]
tests/test_pawpal.py::test_sort_by_time_puts_untimed_last PASSED         [ 35%]
tests/test_pawpal.py::test_filter_by_pet_and_status PASSED               [ 39%]
tests/test_pawpal.py::test_plan_respects_time_budget_and_priority PASSED [ 42%]
tests/test_pawpal.py::test_smaller_task_still_fits_after_large_one_skipped PASSED [ 46%]
tests/test_pawpal.py::test_flexible_tasks_start_at_day_start_without_overlap PASSED [ 50%]
tests/test_pawpal.py::test_fixed_time_honored_and_flexible_fills_around_it PASSED [ 53%]
tests/test_pawpal.py::test_conflicting_fixed_times_warn_and_lower_priority_moves PASSED [ 57%]
tests/test_pawpal.py::test_bumped_fixed_task_moves_later_not_earlier PASSED [ 60%]
tests/test_pawpal.py::test_bumped_fixed_task_goes_earlier_only_if_nothing_later_fits PASSED [ 64%]
tests/test_pawpal.py::test_back_to_back_fixed_tasks_are_not_conflicts PASSED [ 67%]
tests/test_pawpal.py::test_tasks_at_exact_same_time_are_flagged PASSED   [ 71%]
tests/test_pawpal.py::test_every_scheduled_task_has_reason PASSED        [ 75%]
tests/test_pawpal.py::test_empty_owner_gives_empty_plan PASSED           [ 78%]
tests/test_pawpal.py::test_tasks_outside_day_window_are_skipped PASSED   [ 82%]
tests/test_pawpal.py::test_future_and_completed_tasks_excluded PASSED    [ 85%]
tests/test_pawpal.py::test_overdue_task_carries_over PASSED              [ 89%]
tests/test_pawpal.py::test_completing_recurring_task_creates_next[daily-1] PASSED [ 92%]
tests/test_pawpal.py::test_completing_recurring_task_creates_next[weekly-7] PASSED [ 96%]
tests/test_pawpal.py::test_completing_one_off_task_creates_nothing PASSED [100%]

============================= 28 passed in 0.04s ==============================
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `Scheduler.sort_by_priority()` | By "HH:MM" time with flexible tasks last; or by priority, then set time, then shorter duration |
| Filtering | `Scheduler.filter_tasks()`, `Task.is_due()` | By pet, completion status, or due date; the plan only uses open tasks due today or overdue |
| Time budget | `Scheduler.build_plan()` | Greedy: tasks are accepted in priority order while they fit the owner's available minutes |
| Conflict handling | `Scheduler.detect_conflicts()`, `Scheduler.build_plan()` | Overlapping set times produce a warning; the higher-priority task keeps the slot and the other moves to the next free time after it |
| Recurring tasks | `Task.mark_complete()`, `Scheduler.complete_task()` | Completing a daily task adds the next one 1 day later, weekly 7 days later (`timedelta`) |
| Plan explanation | `DailyPlan.to_text()`, `ScheduledTask.reason` | Each scheduled task has a reason; skipped tasks and warnings are listed |

## 📸 Demo Walkthrough

**Main features:** enter owner settings, add pets, add and manage care tasks, filter the task list,
and generate a daily plan that explains itself.

Example workflow:

1. Install the requirements (`pip install -r requirements.txt`) and start the app with `streamlit run app.py`.
2. **Owner:** set the time available today (for example 90 minutes) and the day start and end (07:00-21:00).
3. **Pets:** add Mochi (dog) and Luna (cat).
4. **Tasks:** add tasks for each pet, for example Morning walk (Mochi, 30 min, high, daily, at 08:00),
   Meds (Luna, 5 min, high, at 08:00), Feeding (Mochi, 10 min, high, daily), and Play session
   (Luna, 20 min, medium). The task table is sorted by priority and can be filtered by pet and status.
5. **Edit, complete, or delete:** open "Edit, complete, or delete a task", pick a task, and change it.
   Marking a daily task complete creates the next day's copy.
6. **Build schedule:** pick a date and click "Generate schedule". The app shows a conflict warning for
   the two 08:00 tasks, a summary of minutes used, a table of times, pets, tasks, priorities, and
   reasons, a list of tasks left out and why, and a "How this plan was built" section.

Key scheduler behaviors shown in the CLI demo below (`main.py` adds two more tasks, Evening walk
and Brushing, so the 90-minute budget runs out):

- **Sorting** - tasks are chosen in priority order; the task list can be shown by time or priority.
- **Conflict warnings** - Meds and Morning walk both want 08:00. Meds keeps it (same priority,
  shorter), and Morning walk moves to 08:05.
- **Time budget** - Play session is skipped because only 15 of the 90 minutes are left.
- **Recurrence** - completing Feeding (daily) creates the next one due tomorrow.

CLI demo (`python main.py`, plan section):

```
=== Today's Schedule ===
Owner: Jordan | 90 min available | day 07:00-21:00
Daily plan for 2026-11-01:
  07:00-07:10 - Feeding (Mochi, 10 min) [priority: high]
      why: high priority, recurs daily; placed in the earliest free slot
  07:10-07:25 - Brushing (Luna, 15 min) [priority: low]
      why: low priority, recurs weekly; placed in the earliest free slot
  08:00-08:05 - Meds (Luna, 5 min) [priority: high]
      why: high priority; at your preferred time 08:00
  08:05-08:35 - Morning walk (Mochi, 30 min) [priority: high]
      why: high priority, recurs daily; moved from 08:00 to 08:05 because 'Meds' already had that time
  18:00-18:30 - Evening walk (Mochi, 30 min) [priority: medium]
      why: medium priority, recurs daily; at your preferred time 18:00
  SKIPPED Play session (Luna): needs 20 min but only 15 min of your time is left
  WARNING: 'Meds' (Luna, 08:00) overlaps 'Morning walk' (Mochi, 08:00)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
