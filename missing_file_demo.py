"""Show a missing file being translated and handled by summarise."""
from complete_code import AttendanceFileError, summarise


if __name__ == "__main__":
    try:
        print(summarise("attendance-file-that-does-not-exist.csv"))
    except AttendanceFileError as error:
        print(error)
        print(f"Original cause: {type(error.__cause__).__name__}")

