    """Monthly attendance processor. Input rows: register,date,P-or-A."""
import csv
from datetime import datetime
from pathlib import Path


class InvalidRecord(Exception):
    """A single attendance row is malformed."""


def parse_attendance_line(raw_line):
    fields = [field.strip() for field in raw_line.strip().split(",")]
    if len(fields) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(fields)}")
    register_number, date_text, status = fields
    if not register_number:
        raise InvalidRecord("register number is empty")
    try:
        record_date = datetime.strptime(date_text, "%Y-%m-%d").date()
    except ValueError as error:
        raise InvalidRecord(f"invalid date {date_text!r}") from error
    if status not in {"P", "A"}:
        raise InvalidRecord(f"invalid status {status!r}")
    return register_number, record_date, status


def process_month(input_folder, output_folder, month):
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    counts = {}  # register number -> [present count, valid record count]
    damaged = []

    if not input_folder.is_dir():
        raise FileNotFoundError(f"input folder not found: {input_folder}")
    try:
        daily_files = sorted(input_folder.glob("*.txt"))
    except OSError as error:
        raise OSError(f"cannot list input folder {input_folder}: {error}") from error

    for daily_file in daily_files:
        try:
            with open(daily_file, "r", encoding="utf-8") as source:
                for line_number, raw_line in enumerate(source, start=1):
                    if not raw_line.strip():
                        continue
                    try:
                        register_number, record_date, status = parse_attendance_line(raw_line)
                        if record_date.strftime("%Y-%m") != month:
                            continue
                    except InvalidRecord as error:
                        damaged.append((daily_file.name, line_number, raw_line.rstrip("\r\n"), str(error)))
                        continue
                    student_counts = counts.setdefault(register_number, [0, 0])
                    student_counts[0] += status == "P"
                    student_counts[1] += 1
        except FileNotFoundError as error:
            damaged.append((daily_file.name, 0, "", f"file disappeared: {error}"))
        except PermissionError as error:
            damaged.append((daily_file.name, 0, "", f"permission denied: {error}"))
        except UnicodeDecodeError as error:
            damaged.append((daily_file.name, 0, "", f"invalid UTF-8: {error}"))
        except OSError as error:
            damaged.append((daily_file.name, 0, "", f"file error: {error}"))

    with open(output_folder / "attendance_percentage.csv", "w", newline="", encoding="utf-8") as report:
        writer = csv.writer(report)
        writer.writerow(["register_number", "present", "valid_records", "percentage"])
        for register_number, (present, valid_records) in sorted(counts.items()):
            percentage = 100.0 * present / valid_records if valid_records else 0.0
            writer.writerow([register_number, present, valid_records, f"{percentage:.2f}"])

    with open(output_folder / "below_75_percent.csv", "w", newline="", encoding="utf-8") as report:
        writer = csv.writer(report)
        writer.writerow(["register_number", "percentage"])
        for register_number, (present, valid_records) in sorted(counts.items()):
            percentage = 100.0 * present / valid_records if valid_records else 0.0
            if percentage < 75:
                writer.writerow([register_number, f"{percentage:.2f}"])

    with open(output_folder / "damaged_lines.csv", "w", newline="", encoding="utf-8") as report:
        writer = csv.writer(report)
        writer.writerow(["file_name", "line_number", "raw_line", "reason"])
        writer.writerows(damaged)

    return counts, damaged


def main():
    base = Path(__file__).parent
    try:
        counts, damaged = process_month(base / "input", base / "output", "2026-10")
    except FileNotFoundError as error:
        print(f"Input folder not found: {error}")
        return
    except PermissionError as error:
        print(f"Permission denied: {error}")
        return
    except OSError as error:
        print(f"Could not process attendance files: {error}")
        return
    print(f"Processed {len(counts)} students; damaged records: {len(damaged)}")
    print(f"Reports written to {base / 'output'}")


if __name__ == "__main__":
    main()

