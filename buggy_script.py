"""
学生の成績を管理するスクリプト。
3つのバグが隠されています。見つけられるか挑戦してみてください。
"""


def get_highest_score(scores: list[int]) -> int:
    """リストの中から最高得点を返す。"""
    highest = 0
    for i in range(len(scores) + 1):  # Bug 1
        if scores[i] > highest:
            highest = scores[i]
    return highest


def calculate_average(scores: list) -> float:
    """得点リストの平均を計算する。"""
    total = 0
    for score in scores:
        total = total + score  # Bug 2
    return total / 2  # Bug 3


def grade(average: float) -> str:
    """平均点に応じてグレードを返す。"""
    if average >= 90:
        return "A"
    elif average >= 75:
        return "B"
    elif average >= 60:
        return "C"
    else:
        return "D"


if __name__ == "__main__":
    students = {
        "Alice": [85, 92, 78, 95],
        "Bob": [60, 70, 65, 80],
        "Carol": [90, 88, 95, 100],
    }

    for name, scores in students.items():
        avg = calculate_average(scores)
        best = get_highest_score(scores)
        print(f"{name}: 平均={avg:.1f}, 最高点={best}, グレード={grade(avg)}")
