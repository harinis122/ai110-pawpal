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
I used GitHub copilot during this project to generate base code, writing tests, and a bit for debugging when test cases were failing. The most helpful prompts were ones that directed the AI to generate code, as I felt that once I had AI-generated code, I could work to optimize it.


**b. Judgment and verification**
I did not accept AI suggestions to include additional, unnecessary methods in classes such as including a "get_tasks_by_pet_name" method in Scheduler. I evaluated what the AI suggested by thinking about whether a method was needed or not before accepting it. Even if the method seemed correctly implemented, I thought twice before accepting any AI generated code to see if it is really needed.


---

## 4. Testing and Verification

**a. What you tested**
I tested task completion toggling and that adding a task raises a pet’s task count, schedule output ordering by due time and priority, time-capacity behavior, multi-pet scheduling, pet-specific task filtering, and duplicate-time warning text in formatted UI output. These tests were important to ensure that the program works well not only under basic condiitons but also under edge cases.


**b. Confidence**
I think that I am pretty confident that my tests are comprehensive, but if I had more time I would add comprehensive test cases to ensure that the program does not break with large amounts of tasks.

---

## 5. Reflection

**a. What went well**
I am most satisfied that I was able to use AI to efficiently create this program, and direct the AI rather than relying on it. I successfully evaluated whether or not to use AI generated code.

**b. What you would improve**
I would probably split the Scheduler class into Schedule and Scheduler classes because I feel that Scheduler currently has too many responsibilities which would be better off delegated to a helper class.

**c. Key takeaway**
I learned that having a sense of system design before starting coding is important, especially when coding with AI, to ensure that you have a sense of what direction you're headed in. This will ensure that you know exactly what you're looking for when deciding whether to accept AI generated code. Without knowing the systen design, you might accept AI generated code which does not have the correct system design, leading to a long-term weak system.

