"""Main program for organisation (d)."""
from pathlib import Path
from attendance import read_records, attendance_percentages, absent_three_days, write_reports


def main():
    base = Path(__file__).parent.parent
    records = read_records(base / "input" / "attendance.csv")
    percentages = attendance_percentages(records)
    three_day = absent_three_days(records)
    write_reports(percentages, three_day, Path(__file__).parent / "output")
    print(f"Students: {len(percentages)}; absent for 3 consecutive days: {three_day}")


if __name__ == "__main__":
    main()

