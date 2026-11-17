"""Forensics demonstration of the original overwrite/concatenation defects."""
from pathlib import Path
import tempfile


def save_returns(books, log_name):
    log = open(log_name, "w")
    for book in books:
        log.write(book)
    log.close()


def process(day_file, log_name):
    try:
        books = open(day_file).read().split("\n")
        save_returns(books, log_name)
    except FileNotFoundError:
        print("missing")


def demonstrate():
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        day1 = root / "day1.txt"
        day3 = root / "day3.txt"
        log = root / "returns.log"
        error_log = root / "errors.log"
        day1.write_text("Book A\nBook B\n", encoding="utf-8")
        day3.write_text("Book C\nBook D\n", encoding="utf-8")

        process(day1, log)
        process(root / "day2-missing.txt", log)
        process(day3, log)

        print("Final log:", repr(log.read_text(encoding="utf-8")))
        print("Persistent error log created:", error_log.exists())


if __name__ == "__main__":
    demonstrate()

