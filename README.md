
# CSA08 Assignment 4 — Robust Data Processing

## Student details

- Name: Prajeesh B
- Register number: 1924260076
- Repository: CSA08-1924260076-Assignment4
- GitHub link: https://github.com/bprajeesh1117-rgb/-CSA08-1924260076-Assignment4
- Python version used: Python 3.15.2

## Run commands

Run these from the repository root in the VS Code terminal. On Windows, use py -3 instead of python if needed.

| Task | Command | Main result |
|---|---|---|
| 1 | python Task01/main.py | Task01/output/mess_report.txt and rejected_lines.csv |
| 2 | python Task02/main.py | Three monthly attendance CSV reports in Task02/output/ |
| 3 | python Task03/complete_code.py | Required tuple and bad-line list |
| 3 missing file | python Task03/missing_file_demo.py | Shows AttendanceFileError with FileNotFoundError cause |
| 3 misuse experiment | python Task03/misuse_experiment.py | Shows the hidden counter typo by printing 0 |
| 4 legacy evidence | python Task04/legacy_demo.py | Shows overwritten/concatenated log and missing error log |
| 4 repaired program | python Task04/main.py | Appends returns and writes Task04/output/errors.log |
| 5(a) one script | python Task05/single_script/main.py | Percentage and 3-day absence reports |
| 5(b) one module | python Task05/one_module/main.py | Same reports |
| 5(c) three modules | python Task05/three_modules/main.py | Same reports |
| 5(d) package | python Task05/package/main.py | Same reports |
| 6 | python Task06/run_demo.py | Master list, event files, summary and error log |

Task 2 reports are regenerated on each run. Task 4's log is append-only; remove generated files in Task04/output before a fresh demonstration. Task 6 includes one intentionally missing department file.

## Repository contents

- Task01–Task06 contain source files and sample inputs.
- Task05 contains all four requested code organization styles.
- Task06/fest_registration is the reusable package.
- evidence/README.md lists the screenshots to capture after running the programs.
- REPORT.md contains written answers, pseudocode, traces and complexity comparisons.
- COMMIT_PLAN.md gives a 27-step commit sequence for progressive GitHub history.

## Progressive Git history

Create the repository named CSA08-[RegisterNumber]-Assignment4, then commit each task as completed. Example:

~~~text
git init
git add README.md requirements.txt REPORT.md Task01
git commit -m "Complete Task 1 file processing"
git add Task02
git commit -m "Complete Task 2 attendance design"
git add Task03
git commit -m "Complete Task 3 exception handling"
git add Task04
git commit -m "Complete Task 4 file forensics"
git add Task05
git commit -m "Complete Task 5 module organizations"
git add Task06
git commit -m "Complete Task 6 fest registration package"
git remote add origin <your-repository-url>
git branch -M main
git push -u origin main
~~~

Add the requested screenshots and output samples to the task folders before the final push. Confirm the repository link works and share it with the course faculty as required.

=======
# -CSA08-1924260076-Assignment4
>>>>>>> 66072a3f990d950137799c9b8287d10f2b124311
