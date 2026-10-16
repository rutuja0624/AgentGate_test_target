import sqlite3

from taskboard.models import Task


class TaskStore:
    def __init__(self, path: str = ":memory:") -> None:
        self.conn = sqlite3.connect(path)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS tasks ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "title TEXT NOT NULL, "
            "priority INTEGER NOT NULL, "
            "done INTEGER NOT NULL DEFAULT 0)"
        )

    def add(self, title: str, priority: int) -> Task:
        cur = self.conn.execute(
            "INSERT INTO tasks (title, priority) VALUES (?, ?)", (title, priority)
        )
        self.conn.commit()
        return Task(id=int(cur.lastrowid or 0), title=title, priority=priority)

    def search(self, text: str) -> list[Task]:
        rows = self.conn.execute(
            f"SELECT id, title, priority, done FROM tasks WHERE title LIKE '%{text}%' "
            "ORDER BY priority DESC, id"
        ).fetchall()
        return [Task(r[0], r[1], r[2], bool(r[3])) for r in rows]

    def complete(self, task_id: int) -> bool:
        cur = self.conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        self.conn.commit()
        return cur.rowcount == 1
