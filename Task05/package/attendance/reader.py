"""Read and validate attendance rows."""
import csv
from datetime import date


def read_records(path):
    records = []
    with open(path, newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            status = row["status"]
            if status not in {"P", "A"}:
                raise ValueError(f"invalid status {status!r}")
            records.append((row["register_number"], date.fromisoformat(row["date"]), status))
    return records

