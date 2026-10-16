from dataclasses import dataclass


PRIORITIES = {"low": 1, "medium": 2, "high": 3}


@dataclass
class Task:
    id: int
    title: str
    priority: int = 2
    done: bool = False
