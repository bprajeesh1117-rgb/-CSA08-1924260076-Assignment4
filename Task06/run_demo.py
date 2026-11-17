"""Run the fest package against four sample files and one missing department file."""
from pathlib import Path
from fest_registration import process_registration_files


def main():
    base = Path(__file__).parent
    input_folder = base / "input"
    source_names = [
        "department_cse.txt",
        "department_eee.txt",
        "department_mech.txt",
        "department_civil.txt",
        "department_it.txt",  # intentionally absent for the missing-file demonstration
    ]
    files = [input_folder / name for name in source_names]
    records, errors = process_registration_files(files, base / "output")
    print(f"Accepted registrations: {len(records)}")
    print(f"Logged issues: {len(errors)}")
    print(f"Reports: {base / 'output'}")


if __name__ == "__main__":
    main()

