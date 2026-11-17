"""Stream source files, retain the first valid registration per student."""
from pathlib import Path
from .report import write_outputs
from .validator import InvalidRegistration, parse_registration


def process_registration_files(source_files, output_folder):
    records_by_register = {}
    seen_register_numbers = set()
    errors = []

    for source_path in source_files:
        source_path = Path(source_path)
        try:
            with open(source_path, "r", encoding="utf-8") as source:
                for line_number, raw_line in enumerate(source, start=1):
                    if not raw_line.strip():
                        continue
                    try:
                        record = parse_registration(raw_line)
                    except InvalidRegistration as error:
                        errors.append((source_path.name, line_number, str(error)))
                        continue

                    register_number = record["register_number"]
                    if register_number in seen_register_numbers:
                        errors.append((
                            source_path.name,
                            line_number,
                            f"duplicate registration {register_number}; first valid record kept",
                        ))
                        continue

                    seen_register_numbers.add(register_number)
                    records_by_register[register_number] = record

        except FileNotFoundError as error:
            errors.append((source_path.name, "", f"FileNotFoundError: {error}"))
        except PermissionError as error:
            errors.append((source_path.name, "", f"PermissionError: {error}"))
        except UnicodeDecodeError as error:
            errors.append((source_path.name, "", f"UnicodeDecodeError: {error}"))
        except OSError as error:
            errors.append((source_path.name, "", f"OSError: {error}"))

    records = list(records_by_register.values())
    write_outputs(records, errors, output_folder)
    return records, errors

