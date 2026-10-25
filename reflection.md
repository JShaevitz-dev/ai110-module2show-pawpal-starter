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
  No, I intentionally stuck as close to the original design as possible.
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
