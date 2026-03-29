from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class Task:
    description: str
    duration: int
    due_time: datetime
    priority: str
    completion_status: bool
    frequency: str

    def mark_as_completed(self):
        self.completion_status = True


@dataclass
class Pet:
    breed: str
    name: str
    tasks: List[Task]

    def add_task(self, task: Task):
        self.tasks.append(task)

    def remove_task(self, task: Task):
        self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        return self.tasks


@dataclass
class Owner:
    name: str
    pets: List[Pet]

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def remove_pet(self, pet: Pet):
        self.pets.remove(pet)

    def get_pets(self) -> List[Pet]:
        return self.pets


@dataclass
class Scheduler:
    tasks: List[Task]
    owner: Owner

    def get_schedule(self):
        # TODO: Implement schedule generation logic
        pass

    def check_if_all_tasks_can_be_completed(self) -> bool:
        # TODO: Implement check logic
        pass

    def optimize_tasks_by_priority(self):
        # TODO: Implement optimization logic
        pass
