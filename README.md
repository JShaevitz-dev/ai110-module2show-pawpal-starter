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

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

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
============================= test session starts =============================
platform win32 -- Python 3.10.11, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Coldfur\Documents\Code\pawpal-repo
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.13.0, hydra-core-1.3.2, cov-7.1.0
collected 28 items

tests\test_pawpal.py ............................                        [100%]

============================= 28 passed in 0.08s ==============================

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

============================= 28 passed in 0.05s ==============================
```

Sample test output:

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

============================= 28 passed in 0.05s ==============================
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Run Streamlit program
2. Fill in details for pet and owner
3. Add events to the schedule
4. Generate schedule
5. Interact with schedule

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
