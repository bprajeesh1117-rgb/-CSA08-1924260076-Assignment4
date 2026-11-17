"""Write attendance output files."""
import csv
from pathlib import Path


def write_reports(percentages, three_day_students, folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    with open(folder / "percentages.csv", "w", newline="", encoding="utf-8") as target:
        writer = csv.writer(target)
        writer.writerow(["register_number", "percentage"])
        writer.writerows((student, f"{value:.2f}") for student, value in sorted(percentages.items()))
    with open(folder / "three_day_absentees.txt", "w", encoding="utf-8") as target:
        target.write("\n".join(three_day_students) + ("\n" if three_day_students else ""))

