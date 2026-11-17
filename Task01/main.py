"""Stream hostel mess records and preserve rejected rows for review."""
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path


def process_mess_file(file_name, output_folder):
    """Write valid report rows as they are read; return total and rejected rows."""
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    rejected_rows = []
    total = Decimal("0.00")
    report_path = output_folder / "mess_report.txt"

    with open(file_name, "r", encoding="utf-8") as source:
        with open(report_path, "w", encoding="utf-8") as report:
            report.write("STUDENT\tAMOUNT\n")
            for line_number, raw_line in enumerate(source, start=1):
                line = raw_line.rstrip("\r\n")
                if not line.strip():
                    # Ignore a blank final line; it is not a student record.
                    continue

                try:
                    fields = [field.strip() for field in line.split(",")]
                    if len(fields) != 3:
                        raise ValueError(f"expected 3 fields, found {len(fields)}")
                    register_number, name, amount_text = fields
                    if not register_number or not name:
                        raise ValueError("register number and name are required")
                    amount = Decimal(amount_text)
                    if not amount.is_finite():
                        raise ValueError("amount must be a finite number")
                except (InvalidOperation, ValueError) as error:
                    rejected_rows.append((line_number, line, str(error)))
                    continue

                total += amount
                report.write(f"{name}\t{amount:.2f}\n")

    rejected_path = output_folder / "rejected_lines.csv"
    with open(rejected_path, "w", newline="", encoding="utf-8") as target:
        writer = csv.writer(target)
        writer.writerow(["line_number", "raw_line", "reason"])
        writer.writerows(rejected_rows)

    return total, rejected_rows


def main():
    base = Path(__file__).parent
    input_file = base / "input" / "mess_oct.txt"
    output_folder = base / "output"
    try:
        total, rejected = process_mess_file(input_file, output_folder)
    except FileNotFoundError as error:
        print(f"Input file not found: {error.filename}")
        return
    except PermissionError as error:
        print(f"Permission denied: {error.filename}")
        return
    except UnicodeDecodeError as error:
        print(f"Input is not valid UTF-8: {error}")
        return
    except OSError as error:
        print(f"File error: {error}")
        return

    print(f"Total: {total:.2f}")
    print(f"Valid report: {output_folder / 'mess_report.txt'}")
    print("Rejected rows:")
    for line_number, line, reason in rejected:
        print(f"line {line_number}: {line!r} ({reason})")


if __name__ == "__main__":
    main()

