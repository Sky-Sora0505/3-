import pytest
from pathlib import Path
from myproject.todo import add_task, list_tasks, complete_task, delete_task


@pytest.fixture
def todo_file(tmp_path: Path) -> Path:
    """テストごとに独立した一時JSONファイルを返す。"""
    return tmp_path / "todos.json"


class TestAddTask:
    def test_returns_task_dict(self, todo_file):
        task = add_task("買い物", filepath=todo_file)
        assert task["title"] == "買い物"
        assert task["done"] is False
        assert "id" in task
        assert "created_at" in task

    def test_saved_to_file(self, todo_file):
        add_task("読書", filepath=todo_file)
        tasks = list_tasks(filepath=todo_file)
        assert len(tasks) == 1
        assert tasks[0]["title"] == "読書"

    def test_multiple_tasks(self, todo_file):
        add_task("タスク1", filepath=todo_file)
        add_task("タスク2", filepath=todo_file)
        assert len(list_tasks(filepath=todo_file)) == 2


class TestListTasks:
    def test_empty_when_no_file(self, todo_file):
        assert list_tasks(filepath=todo_file) == []

    def test_returns_all_tasks(self, todo_file):
        add_task("A", filepath=todo_file)
        add_task("B", filepath=todo_file)
        tasks = list_tasks(filepath=todo_file)
        titles = [t["title"] for t in tasks]
        assert "A" in titles
        assert "B" in titles


class TestCompleteTask:
    def test_marks_done(self, todo_file):
        task = add_task("運動", filepath=todo_file)
        completed = complete_task(task["id"], filepath=todo_file)
        assert completed["done"] is True

    def test_persisted(self, todo_file):
        task = add_task("運動", filepath=todo_file)
        complete_task(task["id"], filepath=todo_file)
        tasks = list_tasks(filepath=todo_file)
        assert tasks[0]["done"] is True

    def test_not_found_raises(self, todo_file):
        with pytest.raises(ValueError, match="Task not found"):
            complete_task("nonexistent", filepath=todo_file)


class TestDeleteTask:
    def test_removes_task(self, todo_file):
        task = add_task("削除対象", filepath=todo_file)
        delete_task(task["id"], filepath=todo_file)
        assert list_tasks(filepath=todo_file) == []

    def test_returns_deleted_task(self, todo_file):
        task = add_task("削除対象", filepath=todo_file)
        deleted = delete_task(task["id"], filepath=todo_file)
        assert deleted["title"] == "削除対象"

    def test_only_deletes_target(self, todo_file):
        t1 = add_task("残す", filepath=todo_file)
        t2 = add_task("消す", filepath=todo_file)
        delete_task(t2["id"], filepath=todo_file)
        tasks = list_tasks(filepath=todo_file)
        assert len(tasks) == 1
        assert tasks[0]["id"] == t1["id"]

    def test_not_found_raises(self, todo_file):
        with pytest.raises(ValueError, match="Task not found"):
            delete_task("nonexistent", filepath=todo_file)
