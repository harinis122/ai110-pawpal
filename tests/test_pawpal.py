from datetime import datetime
from pawpal_system import Task, Pet


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
