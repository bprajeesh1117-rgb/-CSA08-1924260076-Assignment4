"""Main program for organisation (c)."""
from pathlib import Path
import reader
import stats
import report


def main():
    base = Path(__file__).parent.parent
    records = reader.read_records(base / "input" / "attendance.csv")
    percentages = stats.attendance_percentages(records)
    three_day = stats.absent_three_days(records)
    report.write_reports(percentages, three_day, Path(__file__).parent / "output")
    print(f"Students: {len(percentages)}; absent for 3 consecutive days: {three_day}")


if __name__ == "__main__":
    main()

