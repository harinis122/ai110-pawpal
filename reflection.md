# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
Three core actions: enter pet and task information, see detailed daily schedule based on inputted constraints, see reasoning behind the plan/schedule.

Initial UML design:
Owner class with attributes (name, pets), methods (add_pet, remove_pet, get_pets)
Pet class with attributes (breed, name, tasks), methods (add_task, remove_task, get_tasks)
Task class with attributes (description, duration, due_time, priority, completion_status, frequency), methods (mark_as_completed)
Scheduler class with attributes (tasks, owner), methods (get_schedule, check_if_all_tasks_can_be_completed, optimize_tasks_by_priority)

owner --has--> pet(s)
pet --has--> task(s)
scheduler --manages--> task(s)
scheduler --uses--> task(s)

**b. Design changes**
Yes, my design changed during implementation. Based on AI feedback, I adjusted my skeleton of Scheduler by adding a method to account for recurring tasks. I also added comments to emphasize that Scheduler tasks need to be changed every time pet tasks get added/deleted.

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**
My scheduler first considers owner preferences (how much time in the day they have to care for their pets), then priority, then due time for a task. I decided to proceed with this order because there is no point in scheduling tasks if the owner has no time for it, and because it is better to prioritize higher priority tasks over low priority tasks due earlier.

**b. Tradeoffs**
One tradeoff my scheduler makes is removing some tasks if the given tasks' combined time exceeds the owner's available amount of hours per day. My program removes only low-priority tasks with latest due times as much as possible. This is to ensure that owners can optimize the time they have available as much as possible.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
