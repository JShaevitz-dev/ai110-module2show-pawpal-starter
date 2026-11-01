# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design
  
  The UML show each of the six classes of the program and their relations to each other.
- What classes did you include, and what responsibilities did you assign to each?
  
  Owner	Name, available minutes, day start and end times, list of pets	Adds and finds pets, and collects every task across all pets
  Pet	Name, species, list of tasks	Adds and removes tasks. Adding a task stamps it with the pet’s name.
  Task	Title, duration, priority, optional set time, how often it repeats, due date, whether it’s done, pet name	Checks whether it’s due on a given day, and marks itself complete. A daily or weekly task returns its next copy when completed.
  Scheduler	The owner	Sorts tasks by priority or time, filters them, finds clashing set times, completes tasks, and builds the day’s plan
  DailyPlan	Date, scheduled tasks, skipped tasks with reasons, warnings	Totals the scheduled minutes and prints the plan as text
  ScheduledTask	A task, its start time, and the reason it was placed there	Works out its end time

**b. Design changes**

- Did your design change during implementation?
- 
  No, I intentionally stuck as close to the original design as possible.
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
  The scheduler considers five constraints:
  1. Time budget - the owner's available minutes for the day. Tasks are only accepted while
     they still fit in the time that is left.
  2. Priority - high, medium, or low. Tasks are considered in priority order, so high-priority
     care like meds and feeding gets first claim on the owner's time.
  3. Preferred time - a task can be set to a specific time, like meds at 08:00. The scheduler
     places it there if the slot is free. If two set times clash, the higher-priority task keeps
     the slot and the other moves to the next free time after it.
  4. Day window - the owner's day start and end. Nothing is scheduled before the start or
     allowed to run past the end.
  5. Due date and recurrence - only open tasks due today or overdue are planned. Overdue tasks
     carry over, and completing a daily or weekly task creates the next one.
- How did you decide which constraints mattered most?
  The time budget and day window are hard limits, because the owner can't do more than they have
  time for. Within those limits, priority decides which tasks get the time, because missing
  medication matters more than missing playtime. Preferred times come after priority: when two
  set times clash, the lower-priority task is moved instead of dropped, so the owner still gets
  it done. When priorities tie, tasks with a set time go first, then shorter tasks, so more tasks
  fit in the day.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
  The scheduler is greedy. It goes through tasks in priority order and accepts each one if it
  fits in the remaining time, without going back to reconsider. This means it doesn't always
  fill the owner's time as fully as possible. For example, with 30 minutes available and three
  tasks - a 25-minute high-priority walk and two 15-minute medium-priority tasks - it schedules
  the walk and skips both 15-minute tasks, even though the two of them would have used all 30
  minutes.
- Why is that tradeoff reasonable for this scenario?
  For a pet owner, getting the most important care done matters more than packing every minute.
  The greedy approach guarantees that a lower-priority task never pushes out a higher-priority
  one. It is also easy to explain: every scheduled task has a reason, and every skipped task
  says how many minutes it needed and how many were left. A scheduler that searched every
  combination would be harder to explain and wouldn't help much with a typical day of 5-10 tasks.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
  
  AI was used to identify the missing and non-functional features by comparing the code of the program to the README
- What kinds of prompts or questions were most helpful?
  
  I have learned through my coursework to be very efficient with my prompts. Every prompt was either a command to refactor or clarification on changes it made.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
  
  Some changes were suggested that moved the program beyond the initial scope of the assingment.
- How did you evaluate or verify what the AI suggested?
  
  I established a rule regarding "doing more than needed"

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
  
  A basic runthrough to test functionality
- Why were these tests important?
  
  To ensure functionality of the program

**b. Confidence**

- How confident are you that your scheduler works correctly?
  Fully

- What edge cases would you test next if you had more time?
  
  Non-ASCII characters and input sanitation.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
  
  I think everything went well.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
  
  I would implementing file-writing to give the generated schedule permanence. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
  
  Understanding the scope of work and maintaining it.
