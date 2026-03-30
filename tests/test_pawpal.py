from datetime import datetime
from pawpal_system import Task, Pet, Owner, Scheduler
from main import format_schedule


def test_task_completion_changes_status():
    # create a task that starts incomplete
    task = Task(description="Feed test pet", duration=10, due_time=datetime.now(), priority=1, is_completed=False)

    assert task.is_completed is False

    # mark complete action
    task.mark_as_completed()

    assert task.is_completed is True


def test_pet_task_addition_increases_task_count():
    pet = Pet(breed="TestBreed", name="TestPet", tasks=[])

    initial_count = pet.get_task_count() if hasattr(pet, 'get_task_count') else len(pet.tasks)
    assert initial_count == 0

    new_task = Task(description="Walk test pet", duration=20, due_time=datetime.now(), priority=2)
    pet.add_task(new_task)

    final_count = pet.get_task_count() if hasattr(pet, 'get_task_count') else len(pet.tasks)
    assert final_count == 1


def test_scheduler_empty_task_list():
    """Test scheduling with no tasks."""
    owner = Owner(name="Test Owner", pets=[], available_hours=4)
    scheduler = Scheduler(all_tasks=[], owner=owner)
    
    schedule = scheduler.get_schedule()
    assert schedule == []
    assert scheduler.all_tasks_can_be_completed() == True


def test_scheduler_single_task():
    """Test scheduling with a single task."""
    task = Task(description="Feed pet", duration=30, due_time=datetime(2023, 10, 1, 9, 0), priority=1)
    pet = Pet(breed="Dog", name="Buddy", tasks=[task])
    owner = Owner(name="Test Owner", pets=[pet], available_hours=4)
    scheduler = Scheduler(all_tasks=[task], owner=owner)
    
    schedule = scheduler.get_schedule()
    assert len(schedule) == 1
    assert schedule[0] == task
    assert scheduler.all_tasks_can_be_completed() == True


def test_scheduler_tasks_chronological_order():
    """Test that tasks are returned in chronological order when all fit."""
    task1 = Task(description="Morning feed", duration=30, due_time=datetime(2023, 10, 1, 8, 0), priority=1)
    task2 = Task(description="Afternoon walk", duration=45, due_time=datetime(2023, 10, 1, 14, 0), priority=2)
    task3 = Task(description="Evening feed", duration=30, due_time=datetime(2023, 10, 1, 18, 0), priority=1)
    
    pet = Pet(breed="Dog", name="Buddy", tasks=[task1, task2, task3])
    owner = Owner(name="Test Owner", pets=[pet], available_hours=8)
    scheduler = Scheduler(all_tasks=[task1, task2, task3], owner=owner)
    
    schedule = scheduler.get_schedule()
    assert len(schedule) == 3
    assert schedule[0] == task1  # 8:00
    assert schedule[1] == task2  # 14:00
    assert schedule[2] == task3  # 18:00
    assert scheduler.all_tasks_can_be_completed() == True


def test_scheduler_same_due_time_sorted_by_priority():
    """Test that tasks with same due time are sorted by priority."""
    task1 = Task(description="High priority task", duration=30, due_time=datetime(2023, 10, 1, 10, 0), priority=1)
    task2 = Task(description="Medium priority task", duration=30, due_time=datetime(2023, 10, 1, 10, 0), priority=2)
    task3 = Task(description="Low priority task", duration=30, due_time=datetime(2023, 10, 1, 10, 0), priority=3)
    
    pet = Pet(breed="Dog", name="Buddy", tasks=[task1, task2, task3])
    owner = Owner(name="Test Owner", pets=[pet], available_hours=4)
    scheduler = Scheduler(all_tasks=[task1, task2, task3], owner=owner)
    
    schedule = scheduler.get_schedule()
    assert len(schedule) == 3
    assert schedule[0] == task1  # Priority 1 first
    assert schedule[1] == task2  # Priority 2 second
    assert schedule[2] == task3  # Priority 3 last


def test_scheduler_exceeds_available_time_prioritizes():
    """Test that when tasks exceed available time, only high priority tasks are scheduled."""
    task1 = Task(description="High priority", duration=60, due_time=datetime(2023, 10, 1, 9, 0), priority=1)
    task2 = Task(description="High priority 2", duration=60, due_time=datetime(2023, 10, 1, 10, 0), priority=1)
    task3 = Task(description="Medium priority", duration=60, due_time=datetime(2023, 10, 1, 11, 0), priority=2)
    
    pet = Pet(breed="Dog", name="Buddy", tasks=[task1, task2, task3])
    owner = Owner(name="Test Owner", pets=[pet], available_hours=1)  # Only 60 minutes available
    scheduler = Scheduler(all_tasks=[task1, task2, task3], owner=owner)
    
    schedule = scheduler.get_schedule()
    assert len(schedule) == 1  # Only one task fits
    assert schedule[0] == task1  # First high priority task
    assert scheduler.all_tasks_can_be_completed() == False


def test_scheduler_completed_tasks_excluded():
    """Test that completed tasks are not included in the schedule."""
    task1 = Task(description="Completed task", duration=30, due_time=datetime(2023, 10, 1, 9, 0), priority=1, is_completed=True)
    task2 = Task(description="Pending task", duration=30, due_time=datetime(2023, 10, 1, 10, 0), priority=2, is_completed=False)
    
    pet = Pet(breed="Dog", name="Buddy", tasks=[task1, task2])
    owner = Owner(name="Test Owner", pets=[pet], available_hours=4)
    scheduler = Scheduler(all_tasks=[task1, task2], owner=owner)
    
    schedule = scheduler.get_schedule()
    assert len(schedule) == 1
    assert schedule[0] == task2
    assert task1 not in schedule


def test_scheduler_multiple_pets():
    """Test scheduling with tasks from multiple pets."""
    task1 = Task(description="Feed dog", duration=30, due_time=datetime(2023, 10, 1, 8, 0), priority=1)
    task2 = Task(description="Feed cat", duration=15, due_time=datetime(2023, 10, 1, 9, 0), priority=1)
    
    dog = Pet(breed="Dog", name="Buddy", tasks=[task1])
    cat = Pet(breed="Cat", name="Whiskers", tasks=[task2])
    owner = Owner(name="Test Owner", pets=[dog, cat], available_hours=4)
    scheduler = Scheduler(all_tasks=[task1, task2], owner=owner)
    
    schedule = scheduler.get_schedule()
    assert len(schedule) == 2
    assert schedule[0] == task1  # Earlier time
    assert schedule[1] == task2


def test_scheduler_zero_available_hours():
    """Test scheduling with zero available hours."""
    task1 = Task(description="Any task", duration=30, due_time=datetime(2023, 10, 1, 9, 0), priority=1)
    
    pet = Pet(breed="Dog", name="Buddy", tasks=[task1])
    owner = Owner(name="Test Owner", pets=[pet], available_hours=0)
    scheduler = Scheduler(all_tasks=[task1], owner=owner)
    
    schedule = scheduler.get_schedule()
    assert len(schedule) == 0  # No tasks can be scheduled
    assert scheduler.all_tasks_can_be_completed() == False


def test_scheduler_identical_timestamps():
    """Test handling of tasks with identical timestamps (edge case)."""
    dt = datetime(2023, 10, 1, 10, 0, 0)
    task1 = Task(description="Task 1", duration=30, due_time=dt, priority=2)
    task2 = Task(description="Task 2", duration=30, due_time=dt, priority=1)  # Higher priority
    
    pet = Pet(breed="Dog", name="Buddy", tasks=[task1, task2])
    owner = Owner(name="Test Owner", pets=[pet], available_hours=4)
    scheduler = Scheduler(all_tasks=[task1, task2], owner=owner)
    
    schedule = scheduler.get_schedule()
    assert len(schedule) == 2
    assert schedule[0] == task2  # Higher priority first despite same time
    assert schedule[1] == task1


def test_scheduler_tasks_across_multiple_days():
    """Test scheduling tasks across different days."""
    task1 = Task(description="Day 1 morning", duration=30, due_time=datetime(2023, 10, 1, 8, 0), priority=1)
    task2 = Task(description="Day 2 morning", duration=30, due_time=datetime(2023, 10, 2, 8, 0), priority=1)
    task3 = Task(description="Day 1 evening", duration=30, due_time=datetime(2023, 10, 1, 18, 0), priority=2)
    
    pet = Pet(breed="Dog", name="Buddy", tasks=[task1, task2, task3])
    owner = Owner(name="Test Owner", pets=[pet], available_hours=8)
    scheduler = Scheduler(all_tasks=[task1, task2, task3], owner=owner)
    
    schedule = scheduler.get_schedule()
    assert len(schedule) == 3
    assert schedule[0] == task1  # Day 1, 8:00
    assert schedule[1] == task3  # Day 1, 18:00
    assert schedule[2] == task2  # Day 2, 8:00


def test_scheduler_get_tasks_by_pet_name():
    """Test filtering tasks by pet name."""
    task1 = Task(description="Feed dog", duration=30, due_time=datetime(2023, 10, 1, 8, 0), priority=1)
    task2 = Task(description="Feed cat", duration=15, due_time=datetime(2023, 10, 1, 9, 0), priority=1)
    
    dog = Pet(breed="Dog", name="Buddy", tasks=[task1])
    cat = Pet(breed="Cat", name="Whiskers", tasks=[task2])
    owner = Owner(name="Test Owner", pets=[dog, cat], available_hours=4)
    scheduler = Scheduler(all_tasks=[task1, task2], owner=owner)
    
    dog_tasks = scheduler.get_scheduled_tasks_by_pet_name("Buddy")
    cat_tasks = scheduler.get_scheduled_tasks_by_pet_name("Whiskers")
    unknown_tasks = scheduler.get_scheduled_tasks_by_pet_name("Unknown")
    
    assert len(dog_tasks) == 1
    assert dog_tasks[0] == task1
    assert len(cat_tasks) == 1
    assert cat_tasks[0] == task2
    assert len(unknown_tasks) == 0


def test_scheduler_get_scheduled_tasks_by_pet_name():
    """Test filtering scheduled tasks by pet name (considers time constraints)."""
    task1 = Task(description="High priority dog task", duration=60, due_time=datetime(2023, 10, 1, 8, 0), priority=1)
    task2 = Task(description="Low priority dog task", duration=60, due_time=datetime(2023, 10, 1, 9, 0), priority=3)
    task3 = Task(description="Cat task", duration=30, due_time=datetime(2023, 10, 1, 10, 0), priority=1)
    
    dog = Pet(breed="Dog", name="Buddy", tasks=[task1, task2])
    cat = Pet(breed="Cat", name="Whiskers", tasks=[task3])
    owner = Owner(name="Test Owner", pets=[dog, cat], available_hours=1)  # Only 60 minutes available
    scheduler = Scheduler(all_tasks=[task1, task2, task3], owner=owner)
    
    dog_scheduled = scheduler.get_scheduled_tasks_by_pet_name("Buddy")
    cat_scheduled = scheduler.get_scheduled_tasks_by_pet_name("Whiskers")
    
    assert len(dog_scheduled) == 1  # Only high priority task fits
    assert dog_scheduled[0] == task1
    assert len(cat_scheduled) == 0  # Cat task doesn't fit due to time constraints


def test_format_schedule_flags_duplicate_times():
    """Test that format_schedule shows warning when tasks have duplicate due times."""
    dt = datetime(2023, 10, 1, 10, 0)
    task1 = Task(description="Task 1", duration=30, due_time=dt, priority=1)
    task2 = Task(description="Task 2", duration=30, due_time=dt, priority=2)  # Same time
    task3 = Task(description="Task 3", duration=30, due_time=datetime(2023, 10, 1, 11, 0), priority=1)
    
    pet = Pet(breed="Dog", name="Buddy", tasks=[task1, task2, task3])
    owner = Owner(name="Test Owner", pets=[pet], available_hours=4)
    
    formatted = format_schedule([task1, task2, task3], True, owner)
    assert "\nNote: Multiple tasks have the same due time and have been optimized by priority level." in formatted


def test_format_schedule_no_warning_unique_times():
    """Test that format_schedule does not show duplicate time warning when all times are unique."""
    task1 = Task(description="Task 1", duration=30, due_time=datetime(2023, 10, 1, 9, 0), priority=1)
    task2 = Task(description="Task 2", duration=30, due_time=datetime(2023, 10, 1, 10, 0), priority=2)
    task3 = Task(description="Task 3", duration=30, due_time=datetime(2023, 10, 1, 11, 0), priority=1)
    
    pet = Pet(breed="Dog", name="Buddy", tasks=[task1, task2, task3])
    owner = Owner(name="Test Owner", pets=[pet], available_hours=4)
    
    formatted = format_schedule([task1, task2, task3], True, owner)
    assert "\nNote: Multiple tasks have the same due time and have been optimized by priority level." not in formatted
