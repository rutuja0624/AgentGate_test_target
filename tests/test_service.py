import pytest

from taskboard.service import TaskService
from taskboard.store import TaskStore


@pytest.fixture
def service() -> TaskService:
    return TaskService(TaskStore())


def test_create_and_find(service):
    service.create("write report", "high")
    service.create("buy milk")
    assert [t.title for t in service.find("report")] == ["write report"]


def test_results_sorted_by_priority(service):
    service.create("a", "low")
    service.create("b", "high")
    assert [t.title for t in service.find("")] == ["b", "a"]


def test_empty_title_rejected(service):
    with pytest.raises(ValueError):
        service.create("   ")


def test_unknown_priority_rejected(service):
    with pytest.raises(ValueError):
        service.create("x", "urgent")


def test_finish_marks_done(service):
    task = service.create("x")
    service.finish(task.id)
    assert service.open_count() == 0


def test_finish_missing_task_raises(service):
    with pytest.raises(KeyError):
        service.finish(999)


def test_open_count(service):
    service.create("a")
    t = service.create("b")
    service.finish(t.id)
    assert service.open_count() == 1


def test_done_count(service):
    task = service.create("a")
    service.create("b")
    service.finish(task.id)
    assert service.done_count() == 1
