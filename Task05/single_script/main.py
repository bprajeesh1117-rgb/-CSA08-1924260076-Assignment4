"""Organisation (a): all reader, statistics and report functions in one script."""
import csv
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path


def read_records(path):
    records = []
    with open(path, newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            records.append((row["register_number"], date.fromisoformat(row["date"]), row["status"]))
    return records


def attendance_percentages(records):
    counts = defaultdict(lambda: [0, 0])
    for register_number, _, status in records:
        if status not in {"P", "A"}:
            raise ValueError(f"invalid status {status!r}")
        counts[register_number][0] += status == "P"
        counts[register_number][1] += 1
    return {student: 100 * present / total for student, (present, total) in counts.items()}


def absent_three_days(records):
    by_student = defaultdict(list)
    for register_number, day, status in records:
        by_student[register_number].append((day, status))
    result = []
    for student, days in by_student.items():
        streak = 0
        previous_day = None
        for day, status in sorted(days):
            if previous_day is None or day != previous_day + timedelta(days=1):
                streak = 0
            streak = streak + 1 if status == "A" else 0
            if streak >= 3:
                result.append(student)
                break
            previous_day = day
    return sorted(result)


def write_reports(percentages, three_day_students, folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    with open(folder / "percentages.csv", "w", newline="", encoding="utf-8") as target:
        writer = csv.writer(target)
        writer.writerow(["register_number", "percentage"])
        for student, percentage in sorted(percentages.items()):
            writer.writerow([student, f"{percentage:.2f}"])
    with open(folder / "three_day_absentees.txt", "w", encoding="utf-8") as target:
        target.write("\n".join(three_day_students))
        if three_day_students:
            target.write("\n")


def main():
    base = Path(__file__).parent.parent
    records = read_records(base / "input" / "attendance.csv")
    percentages = attendance_percentages(records)
    three_day = absent_three_days(records)
    write_reports(percentages, three_day, Path(__file__).parent / "output")
    print(f"Students: {len(percentages)}; absent for 3 consecutive days: {three_day}")


if __name__ == "__main__":
    main()

