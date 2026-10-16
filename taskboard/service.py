from taskboard.models import PRIORITIES, Task
from taskboard.store import TaskStore


class TaskService:
    def __init__(self, store: TaskStore) -> None:
        self.store = store

    def create(self, title: str, priority: str = "medium") -> Task:
        title = title.strip()
        if not title:
            raise ValueError("title must not be empty")
        if priority not in PRIORITIES:
            raise ValueError(f"unknown priority: {priority}")
        return self.store.add(title, PRIORITIES[priority])

    def find(self, text: str) -> list[Task]:
        return self.store.search(text.strip())

    def finish(self, task_id: int) -> None:
        if not self.store.complete(task_id):
            raise KeyError(task_id)

    def open_count(self) -> int:
        return sum(1 for t in self.store.search("") if t.done)
