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
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
============================= test session starts =============================
platform win32 -- Python 3.10.11, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Coldfur\Documents\Code\pawpal-repo
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.13.0, hydra-core-1.3.2, cov-7.1.0
collected 26 items

tests\test_pawpal.py ..........................                          [100%]

============================= 26 passed in 0.04s ==============================

# Run with coverage:
============================= test session starts =============================
platform win32 -- Python 3.10.11, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Coldfur\Documents\Code\pawpal-repo
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.13.0, hydra-core-1.3.2, cov-7.1.0
collected 26 items

tests\test_pawpal.py ..........................                          [100%]

=============================== tests coverage ================================
______________ coverage: platform win32, python 3.10.11-final-0 _______________

Name                   Stmts   Miss  Cover
------------------------------------------
pawpal_system.py         197      9    95%
tests\test_pawpal.py     139      0   100%
------------------------------------------
TOTAL                    336      9    97%
============================= 26 passed in 0.13s ==============================
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
collecting ... collected 26 items

tests/test_pawpal.py::test_blank_title_rejected PASSED                   [  3%]
tests/test_pawpal.py::test_invalid_task_fields_rejected[kwargs0] PASSED  [  7%]
tests/test_pawpal.py::test_invalid_task_fields_rejected[kwargs1] PASSED  [ 11%]
tests/test_pawpal.py::test_invalid_task_fields_rejected[kwargs2] PASSED  [ 15%]
tests/test_pawpal.py::test_invalid_task_fields_rejected[kwargs3] PASSED  [ 19%]
tests/test_pawpal.py::test_add_task_tags_pet_name PASSED                 [ 23%]
tests/test_pawpal.py::test_adding_task_increases_pet_task_count PASSED   [ 26%]
tests/test_pawpal.py::test_duplicate_pet_name_rejected PASSED            [ 30%]
tests/test_pawpal.py::test_sort_by_priority_then_duration PASSED         [ 34%]
tests/test_pawpal.py::test_sort_by_time_puts_untimed_last PASSED         [ 38%]
tests/test_pawpal.py::test_filter_by_pet_and_status PASSED               [ 42%]
tests/test_pawpal.py::test_plan_respects_time_budget_and_priority PASSED [ 46%]
tests/test_pawpal.py::test_smaller_task_still_fits_after_large_one_skipped PASSED [ 50%]
tests/test_pawpal.py::test_flexible_tasks_start_at_day_start_without_overlap PASSED [ 53%]
tests/test_pawpal.py::test_fixed_time_honored_and_flexible_fills_around_it PASSED [ 57%]
tests/test_pawpal.py::test_conflicting_fixed_times_warn_and_lower_priority_moves PASSED [ 61%]
tests/test_pawpal.py::test_back_to_back_fixed_tasks_are_not_conflicts PASSED [ 65%]
tests/test_pawpal.py::test_tasks_at_exact_same_time_are_flagged PASSED   [ 69%]
tests/test_pawpal.py::test_every_scheduled_task_has_reason PASSED        [ 73%]
tests/test_pawpal.py::test_empty_owner_gives_empty_plan PASSED           [ 76%]
tests/test_pawpal.py::test_tasks_outside_day_window_are_skipped PASSED   [ 80%]
tests/test_pawpal.py::test_future_and_completed_tasks_excluded PASSED    [ 84%]
tests/test_pawpal.py::test_overdue_task_carries_over PASSED              [ 88%]
tests/test_pawpal.py::test_completing_recurring_task_creates_next[daily-1] PASSED [ 92%]
tests/test_pawpal.py::test_completing_recurring_task_creates_next[weekly-7] PASSED [ 96%]
tests/test_pawpal.py::test_completing_one_off_task_creates_nothing PASSED [100%]

============================= 26 passed in 0.04s ==============================
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
