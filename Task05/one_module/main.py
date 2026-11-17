"""Main program for organisation (b)."""
from pathlib import Path
import attendance


def main():
    base = Path(__file__).parent.parent
    records = attendance.read_records(base / "input" / "attendance.csv")
    percentages = attendance.attendance_percentages(records)
    three_day = attendance.absent_three_days(records)
    attendance.write_reports(percentages, three_day, Path(__file__).parent / "output")
    print(f"Students: {len(percentages)}; absent for 3 consecutive days: {three_day}")


if __name__ == "__main__":
    main()

