from typing import List, Optional, Dict
from datetime import datetime

from .models import Task, TaskCreate, TaskUpdate, TaskStatus


class TaskDatabase:
    """In-memory database for tasks"""

    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1
        # Add some sample data
        self._init_sample_data()

    def _init_sample_data(self):
        """Initialize with some sample tasks"""
        sample_tasks = [
            TaskCreate(
                title="Set up CI/CD pipeline",
                description="Configure GitHub Actions for automated testing and deployment",
                status=TaskStatus.IN_PROGRESS,
            ),
            TaskCreate(
                title="Write API documentation",
                description="Create comprehensive API documentation with examples",
                status=TaskStatus.PENDING,
            ),
            TaskCreate(
                title="Add authentication",
                description="Implement JWT token-based authentication",
                status=TaskStatus.PENDING,
            ),
        ]

        for task_create in sample_tasks:
            self.create_task(task_create)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        return list(self._tasks.values())

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID"""
        return self._tasks.get(task_id)

    def create_task(self, task_create: TaskCreate) -> Task:
        """Create a new task"""
        now = datetime.utcnow()
        task = Task(
            id=self._next_id,
            title=task_create.title,
            description=task_create.description,
            status=task_create.status,
            created_at=now,
            updated_at=now,
        )

        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def update_task(self, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
        """Update an existing task"""
        if task_id not in self._tasks:
            return None

        task = self._tasks[task_id]
        update_data = task_update.model_dump(exclude_unset=True)

        if update_data:
            for field, value in update_data.items():
                setattr(task, field, value)
            task.updated_at = datetime.utcnow()

        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def get_tasks_by_status(self, status: str) -> List[Task]:
        """Get tasks filtered by status"""
        return [task for task in self._tasks.values() if task.status == status]

    def get_task_count(self) -> int:
        """Get total number of tasks"""
        return len(self._tasks)

    def clear_all_tasks(self) -> None:
        """Clear all tasks (useful for testing)"""
        self._tasks.clear()
        self._next_id = 1
