"""Completed TODO program, with file-level errors chained to their cause."""
import os
import tempfile


class InvalidRecord(Exception):
    """Raised when one attendance line is not in the expected format."""


class AttendanceFileError(Exception):
    """Raised when the attendance file cannot be processed."""


def parse_line(line):
    """'192311001,2026-10-08,P' -> ('192311001', '2026-10-08', 'P')"""
    parts = [part.strip() for part in line.strip().split(",")]
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    if parts[2] not in {"P", "A"}:
        raise InvalidRecord(f"invalid status {parts[2]!r}")
    return tuple(parts)


def summarise(path):
    present, absent, errors = 0, 0, []
    stream = None

    try:
        stream = open(path, "r", encoding="utf-8")
        with stream:
            for line_number, line in enumerate(stream, start=1):
                try:
                    _, _, status = parse_line(line)
                except InvalidRecord as error:
                    errors.append((line_number, str(error)))
                    continue
                else:
                    if status == "P":
                        present += 1
                    else:
                        absent += 1
    except FileNotFoundError as error:
        raise AttendanceFileError(f"attendance file not found: {path}") from error
    except PermissionError as error:
        raise AttendanceFileError(f"permission denied: {path}") from error
    except UnicodeDecodeError as error:
        raise AttendanceFileError(f"attendance file is not UTF-8: {path}") from error
    except OSError as error:
        raise AttendanceFileError(f"cannot read attendance file: {path}") from error
    else:
        return present, absent, errors
    finally:
        # The with block closes the stream; this also covers an exception while
        # entering the block and is harmless if it has already been closed.
        if stream is not None and not stream.closed:
            stream.close()


data = (
    "192311001,2026-10-08,P\n192311002,2026-10-08,A\n"
    "192311003,2026-10-08\n192311004,2026-10-08,L\n"
)

if __name__ == "__main__":
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", suffix=".csv", delete=False, encoding="utf-8"
        ) as temporary_file:
            temporary_file.write(data)
            temporary_path = temporary_file.name
        print(summarise(temporary_path))
    finally:
        if temporary_path and os.path.exists(temporary_path):
            os.remove(temporary_path)

