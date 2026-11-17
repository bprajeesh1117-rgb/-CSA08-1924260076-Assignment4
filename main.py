"""Append each day's returned books and save file errors in an error log."""
from pathlib import Path


def _append_error(error_log, message):
    with open(error_log, "a", encoding="utf-8") as errors:
        errors.write(message.rstrip() + "\n")


def process(day_file, log_file, error_log):
    day_file = Path(day_file)
    try:
        with open(day_file, "r", encoding="utf-8") as source:
            with open(log_file, "a", encoding="utf-8") as log:
                for line in source:
                    if line.strip():
                        log.write(line.rstrip("\r\n") + "\n")
        return True
    except FileNotFoundError as error:
        message = f"FileNotFoundError: {day_file}: {error}"
    except PermissionError as error:
        message = f"PermissionError: {day_file}: {error}"
    except UnicodeDecodeError as error:
        message = f"UnicodeDecodeError: {day_file}: {error}"
    except OSError as error:
        message = f"OSError: {day_file}: {error}"

    try:
        _append_error(error_log, message)
    except OSError as log_error:
        print(f"Could not save error log: {log_error}")
    return False


def main():
    base = Path(__file__).parent
    output = base / "output"
    output.mkdir(exist_ok=True)
    log_file = output / "returns.log"
    error_log = output / "errors.log"
    for day_name in ("day1.txt", "day2-missing.txt", "day3.txt"):
        ok = process(base / "input" / day_name, log_file, error_log)
        print(f"{day_name}: {'processed' if ok else 'failed; logged'}")
    if log_file.exists():
        print("--- returns.log ---")
        print(log_file.read_text(encoding="utf-8"), end="")
    if error_log.exists():
        print("--- errors.log ---")
        print(error_log.read_text(encoding="utf-8"), end="")


if __name__ == "__main__":
    main()

