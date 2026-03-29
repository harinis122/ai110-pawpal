from datetime import datetime
from pawpal_system import Task, Pet, Owner, Scheduler

def format_schedule(schedule: list, all_tasks_can_be_completed: bool, owner: Owner) -> str:
    """Format the schedule in a clear, readable way for terminal output."""
    if not schedule:
        return "📅 No tasks scheduled for today!"

    output = []
    output.append("🐾 PAWPAL DAILY SCHEDULE")
    output.append("=" * 50)

    # Display tasks in scheduler order (by due time and priority)
    for i, task in enumerate(schedule, 1):
        # Find which pet this task belongs to for display
        pet_name = "Unknown Pet"
        for pet in owner.pets:
            if task in pet.tasks:
                pet_name = pet.name
                break

        # Priority indicator
        priority_icon = {1: "🔴", 2: "🟡", 3: "🟢"}.get(task.priority, "⚪")
        priority_text = {1: "HIGH", 2: "MEDIUM", 3: "LOW"}.get(task.priority, "UNKNOWN")

        # Format time nicely
        time_str = task.due_time.strftime("%I:%M %p")

        # Status indicator
        status_icon = "✅" if task.is_completed else "⏳"

        output.append(f"{i}. {status_icon} {task.description} ({pet_name})")
        output.append(f"   ⏰ {time_str} | {priority_icon} {priority_text} | ⏱️ {task.duration}min")

    # Add summary
    total_tasks = len(schedule)
    completed_tasks = sum(1 for task in schedule if task.is_completed)
    total_duration = sum(task.duration for task in schedule)

    output.append("\n" + "=" * 50)
    output.append("📊 SCHEDULE SUMMARY")
    output.append(f"   Total Tasks: {total_tasks}")
    output.append(f"   Completed: {completed_tasks}")
    output.append(f"   Pending: {total_tasks - completed_tasks}")
    output.append(f"   Total Time: {total_duration} minutes ({total_duration//60}h {total_duration%60}m)")

    # Check for tasks with the same due time
    due_times = [task.due_time for task in schedule]
    if len(due_times) != len(set(due_times)):
        output.append("\nNote: Multiple tasks have the same due time and have been optimized by priority level.")

    # Print warning if schedule exceeds available hours
    if not all_tasks_can_be_completed:
        output.append("\nNote: All tasks cannot be completed within available hours. Schedule has been optimized by priority and due time to fit available hours:")

    return "\n".join(output)

def create_schedule():
    # Create some tasks
    task1 = Task(description="Feed Buddy", duration=30,due_time=datetime(2023, 10, 1, 9), priority=1)
    task2 = Task(description="Feed Whiskers", duration=15, due_time=datetime(2023, 10, 1, 10), priority=1)
    task3 = Task(description="Play with Whiskers", duration=30, due_time=datetime(2023, 10, 1, 10), priority=2)
    task4 = Task(description="Groom Whiskers", duration=45, due_time=datetime(2023, 10, 1, 11), priority=3)
    task5 = Task(description="Walk Buddy", duration=45, due_time=datetime(2023, 10, 1, 12), priority=2)
    task6 = Task(description="Groom Buddy", duration=20, due_time=datetime(2023, 10, 1, 13), priority=3)
    task7 = Task(description="Vet Appointment for Buddy", duration=90, due_time=datetime(2023, 10, 1, 14), priority=1)


    # Create a pet and add tasks to it
    buddy = Pet(breed="Golden Retriever", name="Buddy", tasks=[task6, task7, task1, task5])
    whiskers = Pet(breed="Siamese Cat", name="Whiskers", tasks=[task3, task2, task4])

    # Create an owner and add pets to it
    alice = Owner(name="Alice", pets=[buddy, whiskers], available_hours=4)

    # Create a scheduler and get the schedule
    scheduler = Scheduler(all_tasks=alice.get_all_tasks(), owner=alice)
    schedule = scheduler.get_schedule()

    # Print the formatted schedule
    formatted_schedule = format_schedule(schedule, scheduler.all_tasks_can_be_completed(), alice)
    print(formatted_schedule)



if __name__ == "__main__":
    create_schedule()