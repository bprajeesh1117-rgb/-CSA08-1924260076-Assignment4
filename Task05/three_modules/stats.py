"""Compute attendance percentages and three-day absence streaks."""
from collections import defaultdict
from datetime import timedelta


def attendance_percentages(records):
    counts = defaultdict(lambda: [0, 0])
    for student, _, status in records:
        counts[student][0] += status == "P"
        counts[student][1] += 1
    return {student: 100 * present / total for student, (present, total) in counts.items()}


def absent_three_days(records):
    by_student = defaultdict(list)
    for student, day, status in records:
        by_student[student].append((day, status))
    result = []
    for student, days in by_student.items():
        streak, previous = 0, None
        for day, status in sorted(days):
            if previous is None or day != previous + timedelta(days=1):
                streak = 0
            streak = streak + 1 if status == "A" else 0
            if streak >= 3:
                result.append(student)
                break
            previous = day
    return sorted(result)

