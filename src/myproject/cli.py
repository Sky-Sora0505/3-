"""TODO CLI エントリーポイント。"""

import argparse
from pathlib import Path
from myproject.todo import add_task, list_tasks, complete_task, delete_task

DEFAULT_FILE = Path("todos.json")


def cmd_add(args: argparse.Namespace) -> None:
    task = add_task(args.title, filepath=args.file)
    print(f"[追加] [{task['id']}] {task['title']}")


def cmd_list(args: argparse.Namespace) -> None:
    tasks = list_tasks(filepath=args.file)
    if not tasks:
        print("タスクはありません。")
        return
    for task in tasks:
        status = "✓" if task["done"] else " "
        print(f"[{status}] [{task['id']}] {task['title']}  ({task['created_at']})")


def cmd_complete(args: argparse.Namespace) -> None:
    try:
        task = complete_task(args.id, filepath=args.file)
        print(f"[完了] [{task['id']}] {task['title']}")
    except ValueError as e:
        print(f"エラー: {e}")


def cmd_delete(args: argparse.Namespace) -> None:
    try:
        task = delete_task(args.id, filepath=args.file)
        print(f"[削除] [{task['id']}] {task['title']}")
    except ValueError as e:
        print(f"エラー: {e}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="todo",
        description="シンプルなTODO管理ツール",
    )
    parser.add_argument(
        "--file", type=Path, default=DEFAULT_FILE, metavar="FILE",
        help="JSONファイルのパス (デフォルト: todos.json)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # add
    p_add = sub.add_parser("add", help="タスクを追加する")
    p_add.add_argument("title", help="タスクのタイトル")
    p_add.set_defaults(func=cmd_add)

    # list
    p_list = sub.add_parser("list", help="タスク一覧を表示する")
    p_list.set_defaults(func=cmd_list)

    # complete
    p_complete = sub.add_parser("complete", help="タスクを完了にする")
    p_complete.add_argument("id", help="タスクID")
    p_complete.set_defaults(func=cmd_complete)

    # delete
    p_delete = sub.add_parser("delete", help="タスクを削除する")
    p_delete.add_argument("id", help="タスクID")
    p_delete.set_defaults(func=cmd_delete)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
