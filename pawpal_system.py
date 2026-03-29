from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class Task:
    description: str
    duration: int # Duration in minutes
    due_time: datetime
    priority: int # 1 = High, 2 = Medium, 3 = Low
    is_completed: bool = False

    def mark_as_completed(self):
        """Mark this task as completed."""
        self.is_completed = True


@dataclass
class Pet:
    breed: str
    name: str
    tasks: List[Task]

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Remove a task from this pet's task list."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks

@dataclass
class Owner:
    name: str
    pets: List[Pet]
    available_hours: int

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks from all pets owned by this owner."""
        all_tasks = []
        for pet in self.pets:
            all_tasks += pet.get_tasks()
        return all_tasks

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's list of pets."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet):
        """Remove a pet from the owner's list of pets."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pets(self) -> List[Pet]:
        """Return all pets the owner has."""
        return self.pets


@dataclass
class Scheduler:
    all_tasks: List[Task]
    owner: Owner

    def get_schedule(self) -> List[Task]:
        """Retrieve and organize all tasks by due time (earliest first)."""
        # Get all pending tasks
        pending_tasks = self.get_pending_tasks()
        
        if self.all_tasks_can_be_completed():
            # If all tasks can be completed, sort by due time
            return sorted(pending_tasks, key=lambda task: task.due_time)
        else:
            # If not all tasks can be completed, get optimized tasks by priority
            optimized_tasks = self.get_optimized_tasks_by_priority()
            return sorted(optimized_tasks, key=lambda task: task.due_time)


    def all_tasks_can_be_completed(self) -> bool:
        """
        Check if all pending tasks can be completed within available hours.
        Returns True if total duration fits, False otherwise.
        """
        pending_tasks = self.get_pending_tasks()
        total_task_duration = sum(task.duration for task in pending_tasks)
        # Convert total duration (in minutes) to hours
        total_hours = total_task_duration / 60
        return total_hours <= self.owner.available_hours

    def get_optimized_tasks_by_priority(self) -> List[Task]:
        """
        Sort all tasks by priority (1 = highest priority) and select only tasks that can be completed within available hours.
        Returns tasks organized from highest to lowest priority, limited by available time.
        """
        pending_tasks = self.get_pending_tasks()
        # Sort by priority (ascending, so 1 comes first), then by due_time for tiebreaking
        sorted_tasks = sorted(pending_tasks, key=lambda task: (task.priority, task.due_time))
        
        # Select tasks that fit within available hours, starting with highest priority
        selected_tasks = []
        total_time_used = 0
        available_minutes = self.owner.available_hours * 60
        
        for task in sorted_tasks:
            if total_time_used + task.duration <= available_minutes:
                selected_tasks.append(task)
                total_time_used += task.duration
        
        return selected_tasks
    
    def get_pending_tasks(self) -> List[Task]:
        """Return all pending (not completed) tasks."""
        return [task for task in self.all_tasks if not task.is_completed]

    def get_high_priority_tasks(self) -> List[Task]:
        """Return all high priority (priority=1) tasks."""
        return [task for task in self.all_tasks if task.priority == 1]
    
    def get_medium_priority_tasks(self) -> List[Task]:
        """Return all medium priority (priority=2) tasks."""
        return [task for task in self.all_tasks if task.priority == 2]
    
    def get_low_priority_tasks(self) -> List[Task]:
        """Return all low priority (priority=3) tasks."""
        return [task for task in self.all_tasks if task.priority == 3]

    def update_all_tasks(self) -> None:
        """Sync all_tasks list with current owner's tasks."""
        self.all_tasks = self.owner.get_all_tasks()

