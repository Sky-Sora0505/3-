"""TODO リストのデータ管理ロジック。"""

import json
import uuid
from pathlib import Path
from datetime import datetime


DEFAULT_FILE = Path("todos.json")


def _load(filepath: Path) -> list[dict]:
    if not filepath.exists():
        return []
    return json.loads(filepath.read_text(encoding="utf-8"))


def _save(tasks: list[dict], filepath: Path) -> None:
    filepath.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")


def add_task(title: str, filepath: Path = DEFAULT_FILE) -> dict:
    """タスクを追加して返す。"""
    tasks = _load(filepath)
    task = {
        "id": str(uuid.uuid4())[:8],
        "title": title,
        "done": False,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    tasks.append(task)
    _save(tasks, filepath)
    return task


def list_tasks(filepath: Path = DEFAULT_FILE) -> list[dict]:
    """全タスクを返す。"""
    return _load(filepath)


def complete_task(task_id: str, filepath: Path = DEFAULT_FILE) -> dict:
    """タスクを完了にして返す。見つからなければ ValueError を送出。"""
    tasks = _load(filepath)
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            _save(tasks, filepath)
            return task
    raise ValueError(f"Task not found: {task_id}")


def delete_task(task_id: str, filepath: Path = DEFAULT_FILE) -> dict:
    """タスクを削除して返す。見つからなければ ValueError を送出。"""
    tasks = _load(filepath)
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            _save(tasks, filepath)
            return task
    raise ValueError(f"Task not found: {task_id}")
