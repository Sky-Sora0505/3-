"""最小限のシェル（REPL）実装。"""

import os
import shlex
import subprocess
import sys
from pathlib import Path

PROMPT = "myshell> "

HELP_TEXT = """\
組み込みコマンド:
  cd [DIR]   ディレクトリを移動する（引数なしは HOME へ）
  pwd        現在のディレクトリを表示する
  help       このヘルプを表示する
  exit       シェルを終了する
  quit       シェルを終了する
"""


def builtin_cd(args: list[str]) -> int:
    target = Path(args[1]) if len(args) >= 2 else Path.home()
    try:
        os.chdir(target)
        return 0
    except FileNotFoundError:
        print(f"myshell: cd: {target}: No such file or directory", file=sys.stderr)
        return 1
    except NotADirectoryError:
        print(f"myshell: cd: {target}: Not a directory", file=sys.stderr)
        return 1
    except PermissionError:
        print(f"myshell: cd: {target}: Permission denied", file=sys.stderr)
        return 1


def builtin_pwd(_args: list[str]) -> int:
    print(os.getcwd())
    return 0


def builtin_help(_args: list[str]) -> int:
    print(HELP_TEXT, end="")
    return 0


BUILTINS = {
    "cd":   builtin_cd,
    "pwd":  builtin_pwd,
    "help": builtin_help,
}


def _parse_args(segment: str) -> list[str] | None:
    """セグメントをパースして引数リストを返す。失敗時は None。"""
    try:
        args = shlex.split(segment)
    except ValueError as e:
        print(f"myshell: parse error: {e}", file=sys.stderr)
        return None
    return args or None


def run_command(line: str) -> int:
    """パイプを含むコマンド行を実行して終了コードを返す。"""
    segments = line.split("|")

    # パイプなし
    if len(segments) == 1:
        args = _parse_args(line)
        if args is None:
            return 0
        if args[0] in BUILTINS:
            return BUILTINS[args[0]](args)
        try:
            return subprocess.run(args).returncode
        except FileNotFoundError:
            print(f"myshell: {args[0]}: command not found", file=sys.stderr)
            return 127
        except PermissionError:
            print(f"myshell: {args[0]}: permission denied", file=sys.stderr)
            return 126

    # パイプあり: 各セグメントを順に繋ぐ
    procs: list[subprocess.Popen] = []
    try:
        for i, segment in enumerate(segments):
            args = _parse_args(segment)
            if not args:
                print("myshell: empty command in pipeline", file=sys.stderr)
                return 1

            stdin = procs[-1].stdout if procs else None
            # 最後のコマンド以外は stdout をパイプで受け渡す
            stdout = subprocess.PIPE if i < len(segments) - 1 else None

            try:
                proc = subprocess.Popen(args, stdin=stdin, stdout=stdout)
            except FileNotFoundError:
                print(f"myshell: {args[0]}: command not found", file=sys.stderr)
                for p in procs:
                    p.kill()
                return 127
            except PermissionError:
                print(f"myshell: {args[0]}: permission denied", file=sys.stderr)
                for p in procs:
                    p.kill()
                return 126

            # 前段の stdout を閉じて所有権を次プロセスへ渡す
            if stdin is not None:
                stdin.close()

            procs.append(proc)

        # 全プロセスの終了を待ち、最後の終了コードを返す
        for proc in procs:
            proc.wait()
        return procs[-1].returncode

    except KeyboardInterrupt:
        for p in procs:
            p.kill()
        print()
        return 130


def repl() -> None:
    """REPLループ。Ctrl+D または exit/quit で終了。"""
    while True:
        try:
            line = input(PROMPT).strip()
        except EOFError:
            # Ctrl+D
            print()
            break
        except KeyboardInterrupt:
            # Ctrl+C で入力をキャンセルし、次のプロンプトへ
            print()
            continue

        if not line:
            continue

        if line in {"exit", "quit"}:
            break

        run_command(line)


def main() -> None:
    repl()


if __name__ == "__main__":
    main()
