"""One imported module containing the reader, statistics and report functions."""
import csv
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path


def read_records(path):
    with open(path, newline="", encoding="utf-8") as source:
        return [
            (row["register_number"], date.fromisoformat(row["date"]), row["status"])
            for row in csv.DictReader(source)
        ]


def attendance_percentages(records):
    counts = defaultdict(lambda: [0, 0])
    for student, _, status in records:
        if status not in {"P", "A"}:
            raise ValueError(f"invalid status {status!r}")
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


def write_reports(percentages, three_day_students, folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    with open(folder / "percentages.csv", "w", newline="", encoding="utf-8") as target:
        writer = csv.writer(target)
        writer.writerow(["register_number", "percentage"])
        writer.writerows((student, f"{value:.2f}") for student, value in sorted(percentages.items()))
    with open(folder / "three_day_absentees.txt", "w", encoding="utf-8") as target:
        target.write("\n".join(three_day_students) + ("\n" if three_day_students else ""))

