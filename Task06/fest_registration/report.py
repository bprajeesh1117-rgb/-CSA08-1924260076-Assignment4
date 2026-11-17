"""Write the master list, event participant files, summary and error log."""
import csv
import re
from pathlib import Path


def _event_slug(event):
    slug = re.sub(r"[^A-Za-z0-9_-]+", "_", event).strip("_").lower()
    return slug or "event"


def write_outputs(records, errors, output_folder):
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    with open(output_folder / "master_registrations.csv", "w", newline="", encoding="utf-8") as target:
        writer = csv.writer(target)
        writer.writerow(["register_number", "name", "department", "email", "events"])
        for record in records:
            writer.writerow([
                record["register_number"],
                record["name"],
                record["department"],
                record["email"],
                ";".join(record["events"]),
            ])

    participants = {}
    for record in records:
        for event in record["events"]:
            participants.setdefault(event, []).append(record)

    event_files = {}
    for index, event in enumerate(sorted(participants), start=1):
        file_name = f"participants_{index:02d}_{_event_slug(event)}.csv"
        event_files[event] = file_name
        with open(output_folder / file_name, "w", newline="", encoding="utf-8") as target:
            writer = csv.writer(target)
            writer.writerow(["register_number", "name", "department", "email"])
            for record in participants[event]:
                writer.writerow([
                    record["register_number"],
                    record["name"],
                    record["department"],
                    record["email"],
                ])

    with open(output_folder / "summary.txt", "w", encoding="utf-8") as target:
        target.write(f"Unique accepted registrations: {len(records)}\n")
        target.write(f"Distinct events: {len(participants)}\n")
        target.write(f"Rejected rows, duplicates and file errors: {len(errors)}\n")
        target.write("Participants by event:\n")
        for event in sorted(participants):
            target.write(f"- {event}: {len(participants[event])} ({event_files[event]})\n")

    with open(output_folder / "error_log.csv", "w", newline="", encoding="utf-8") as target:
        writer = csv.writer(target)
        writer.writerow(["source_file", "line_number", "issue"])
        writer.writerows(errors)

