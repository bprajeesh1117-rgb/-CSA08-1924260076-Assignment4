# Assignment 4 — Written Report

**Student:** [Your full name]  
**Register number:** [Your register number]  
**Course:** Python Programming (CSA08)  
**Repository link:** [Paste your GitHub link after publishing]

The pseudocode uses structured, language-independent steps with uppercase control words such as BEGIN, END, INPUT, OUTPUT, IF, FOR and WHILE. Replace the student fields and add your own notes after running the programs.

---

## Task 1 — File-processing design review

### 1.1 Deficiencies and office impact

| Deficiency | What could go wrong |
|---|---|
| The path is hard-coded to one user's Desktop. | The program fails on another office computer or when the file is moved. |
| The file is opened without a with statement or explicit close. | A handle may remain open after an error, delaying release of the file and system resources. |
| read() loads the entire file into memory. | A much larger monthly file consumes memory proportional to the full file size. |
| A bare except: pass catches every error. | Permission, decoding, indexing, and programming errors are silently treated like bad records; staff cannot investigate missing bills. |
| int() rejects decimal amounts such as 1250.50. | Valid paise amounts are discarded instead of included in the total. |
| Repeated report string concatenation copies an increasingly large string. | Building a large report can take quadratic copying work and uses extra memory. |
| split("\n") produces an empty final item when the file ends with a newline. | The last empty item has too few fields; the broad handler hides it without distinguishing it from a damaged student row. |
| The code assumes there are at least three comma-separated fields. | A short or malformed line can raise IndexError; extra fields are also accepted without review. |
| Rejected lines are not recorded. | The office cannot identify students whose bills were omitted, correct the source file, or audit the total. |
| No encoding is specified. | Different platform defaults can decode names differently or fail unpredictably. |

### 1.2 Repaired design

Run python Task01/main.py. The program takes the input filename as a function argument, opens files with context managers, processes one line at a time, parses money with Decimal, writes accepted rows directly to the report file, and saves rejected rows with line numbers and reasons.

This design treats an empty line as a non-record and records malformed non-empty lines. It reports file-level errors separately. The sample contains a decimal bill, a valid integer amount, a bad amount and a row with a missing field.

### 1.3 Design defence (under 100 words)

The program reads one record at a time, so it does not need to keep all 50,000 input lines in memory. A with statement closes both files even if parsing or writing fails. Decimal arithmetic preserves paise, and specific handlers distinguish bad records from file and encoding failures. Rejected lines are saved with their line numbers and reasons, so the office can audit and correct them. Valid report rows are written as they are processed, while only the required rejected-row list and running total remain in memory.

### Alternative concept and complexity

Let B be the input bytes, n the number of lines, L the longest line, and r the number of rejected lines.

- read() or readlines() reads all input before processing: time is O(B); input memory is O(B), plus O(n) line objects for readlines().
- Iterating over the file is also O(B) time, but input-buffer memory is O(L), approximately one current line plus the file buffer.
- This solution retains rejected rows to satisfy the audit requirement, so its additional memory is O(r × rejected-row-size). Accepted report rows go directly to disk and are not retained in memory.

For 50,000 lines, streaming avoids holding the complete source file and all its line strings at once.

---

## Task 2 — From requirement to file-processing design

### 2.1 Data model

**Input:** one UTF-8 text file per day, named by date, with one record per line:

~~~text
register_number,YYYY-MM-DD,P
register_number,YYYY-MM-DD,A
~~~

For example, 192311001,2026-10-08,P. A valid record has exactly three fields, a non-empty register number, an ISO date, and status P or A.

**In-memory data:**

- counts[register_number] = [present_count, valid_record_count].
- damaged is a list of (file_name, line_number, raw_line, reason) tuples.

**Output files:**

1. attendance_percentage.csv: register number, present count, valid-record count, and percentage.
2. below_75_percent.csv: register number and percentage for students below 75%.
3. damaged_lines.csv: source file, line number, original row, and reason.

The percentage denominator is the student's valid attendance records found in the month's supplied files. This makes the assumption explicit if a daily file is missing.

### 2.2 File operations

- Use pathlib.Path.glob("*.txt") to list daily files.
- Open source files in r mode with encoding="utf-8" and iterate over the file. Iteration streams one line at a time. read() and readline() are not used: read() would load the whole file, and an explicit readline() loop is unnecessary when iteration already gives one line at a time.
- Open each generated report in w mode with UTF-8; use csv.writer and newline="" for CSV output.
- Use write through csv.writer rather than assembling a full report string.
- No append mode is needed for monthly reports because each run regenerates the complete result.
- Empty lines are skipped. A malformed non-empty row is logged and processing continues.

### 2.3 Monthly-processing pseudocode

~~~text
ALGORITHM PROCESS_MONTH
INPUT: input_folder, output_folder, target_month

BEGIN
    counts ← empty dictionary
    damaged ← empty list
    daily_files ← SORT all *.txt paths in input_folder

    FOR EACH file IN daily_files
        TRY
            OPEN file FOR reading as UTF-8
            line_number ← 0

            FOR EACH line IN file
                line_number ← line_number + 1
                IF line is blank THEN
                    CONTINUE
                END IF

                TRY
                    fields ← split line by comma and trim spaces
                    IF field count is not 3 THEN
                        RAISE InvalidRecord
                    END IF
                    register_number, date, status ← fields
                    IF date is invalid OR status is not P or A THEN
                        RAISE InvalidRecord
                    END IF
                CATCH InvalidRecord AS reason
                    APPEND (file name, line_number, line, reason) to damaged
                    CONTINUE
                END TRY

                IF date belongs to target_month THEN
                    IF register_number is not in counts THEN
                        counts[register_number] ← [0, 0]
                    END IF
                    IF status = P THEN
                        counts[register_number].present ← present + 1
                    END IF
                    counts[register_number].valid_records ← valid_records + 1
                END IF
            END FOR
        CATCH FileNotFoundError, PermissionError, UnicodeDecodeError, OSError AS reason
            APPEND (file name, 0, empty text, reason) to damaged
        END TRY
    END FOR

    OPEN attendance_percentage.csv FOR writing
    WRITE header
    FOR EACH register_number IN SORTED counts
        percentage ← 100 × present / valid_records
        WRITE register_number, present, valid_records, percentage
    END FOR
    CLOSE report

    OPEN below_75_percent.csv FOR writing
    WRITE each student whose percentage is less than 75
    CLOSE report

    OPEN damaged_lines.csv FOR writing
    WRITE header and every item in damaged
    CLOSE report
END
~~~

### 2.4 Trace

For the sample file 2026-10-08.txt:

| Line | Input | Processing result |
|---:|---|---|
| 1 | 192311001,2026-10-08,P | Valid. Counts become 192311001 → [1, 1]. |
| 2 | 192311002,2026-10-08,A | Valid. Counts become 192311002 → [0, 1]. |
| 3 | broken-line | Rejected: expected 3 fields, found 1. Add (2026-10-08.txt, 3, broken-line, reason) to damaged. |

After the two valid rows, the percentage rows are 100.00% for 192311001 and 0.00% for 192311002. The latter is included in the below-75% report. Line 3 appears in the damaged-lines report.

### Alternative concept and complexity

With one pass through all files, the processor is O(f × l) in time, where f is the file count and l is the average number of lines per file. Re-reading every file separately for each of s students costs O(s × f × l). The one-pass design uses O(s + d) memory for student counters and damaged entries, where d is the damaged-row count. Re-reading can use O(1) working memory per student if it writes results as it goes, but performs far more file I/O.

---

## Task 3 — Error handling

### 3.1 Principal failures

| Failure | Typical exception | Handling |
|---|---|---|
| Input folder or file is absent | FileNotFoundError | Report the path; skip the unavailable file or stop the current file operation. |
| No read permission | PermissionError | Report the affected path; do not silently skip it. |
| File bytes do not decode as UTF-8 | UnicodeDecodeError | Record a file-level decoding failure. |
| A row has too few or too many fields | InvalidRecord (application exception); unchecked indexing could raise IndexError | Raise and catch InvalidRecord at the row boundary; log the row. |
| Status is not P or A | InvalidRecord | Log the invalid status and continue with the next row. |
| Date or numeric conversion is invalid | ValueError | Convert it to an InvalidRecord with context, or log it at the row boundary. |
| Empty file | No exception | Return zero present, zero absent, and an empty error list. |
| Empty line | InvalidRecord if parsed | Skip blank lines or record them according to the stated rule. |
| Disk or other operating-system file failure | OSError | Preserve the cause and report the file operation that failed. |
| Unexpected bug such as a misspelled variable | Often NameError or UnboundLocalError | Allow it to surface during development; do not suppress it with a bare handler. |

### 3.2 Custom exception

InvalidRecord is raised by parse_line when the row has a field count other than three or status outside P/A. It is caught inside the per-line loop in summarise, where the line number and message are appended to errors. This boundary lets the file continue after a damaged record.

AttendanceFileError represents a file-level problem. summarise raises it with the original FileNotFoundError, PermissionError, UnicodeDecodeError, or OSError chained as its cause.

### 3.3 Complete try statement and TODO completion

Run python Task03/complete_code.py. The completed program implements both TODOs:

- parse_line trims fields, checks exactly three fields, checks status, and returns a tuple.
- summarise uses with, catches InvalidRecord per line, counts P and A in the else branch, handles specific file exceptions, returns results in the successful else branch, and closes the stream in finally if the context has not already closed it.
- raise AttendanceFileError(...) from error preserves the original cause for diagnosis.

Expected output:

~~~text
(1, 1, [(3, 'expected 3 fields, found 2'), (4, "invalid status 'L'")])
~~~

Run python Task03/missing_file_demo.py to try a missing path. The caller catches AttendanceFileError, and the caught exception's __cause__ is the original FileNotFoundError.

### 3.4 Misuse experiment

Run python Task03/misuse_experiment.py. It prints 0. The intentional misspelling presnt += 1 raises UnboundLocalError while processing a present row. except Exception: pass catches and discards it, so the counter remains zero and the program gives a plausible but wrong answer without an error message.

### Alternative concept and complexity

An EAFP approach tries to parse each line and catches InvalidRecord. A LBYL approach first checks field count, required values, status and date, then uses the values. Both are O(k) time per line of length k, and both can be O(1) working space per line, aside from stored errors.

When invalid rows are rare, exceptions happen rarely, so EAFP keeps the normal path direct. When invalid rows are common, repeated exception construction and stack unwinding add cost; explicit checks are usually cheaper and make expected validation failures clear. Both approaches should still record the bad row rather than silently discard it.

---

## Task 4 — File and exception forensics

### 4.1 Defects

- open(log_name, "w") truncates the old log each day, so only the latest processed day remains.
- Each book string is written with no newline. The final entry of one row runs directly into the next.
- If write() raises before close(), the close call is skipped. The output handle may remain open and buffered data may not be flushed.
- The source open also lacks with; an exception during reading has no explicit cleanup guarantee.
- The only error handler prints missing. It does not save the error to a log and does not handle permission, decode or write failures.

### 4.2 Forensics evidence

Run python Task04/legacy_demo.py. The test supplies day 1 and day 3 files and intentionally requests a missing day 2 file. Expected demonstration:

~~~text
missing
Final log: 'Book CBook D'
Persistent error log created: False
~~~

The day 3 overwrite has removed day 1, and the two day 3 book names are joined. The day 2 failure is visible only on the console; no persistent error log exists.

### 4.3 Repair

Run python Task04/main.py. The repaired process uses append mode, writes one newline-terminated book per line, wraps both input and output handles in with, and appends file errors to errors.log. It processes later day files after a missing file.

### 4.4 Prevention rules

1. Use with open(...) for every file so handles close on both success and failure.
2. Choose file mode deliberately: w replaces a file, while a preserves earlier log entries; include explicit record separators such as newline.

### Alternative concept and complexity

A correct manual version opens a file, performs work in try, and closes it in finally:

~~~text
file_handle ← OPEN log in append mode
TRY
    WRITE each book and newline
FINALLY
    CLOSE file_handle
END TRY
~~~

For input plus output, use a separate try/finally cleanup for each handle, or nest the blocks so each opened handle has its own guaranteed close. A correctly written manual cleanup and a with statement have the same O(B) time for B characters and O(L) streaming memory for longest line L. The context-manager version makes cleanup automatic. In the repaired sequential design, at most one input and one output handle are open at a time (two during the copy); either with or correct finally closes them. Without guaranteed cleanup, a write failure can leave the output handle open; the original source handle also has no explicit close.

---

## Task 5 — Four organizations

### 5.1 Structures

~~~text
(a) single_script/
    main.py                 reader + statistics + report writer

(b) one_module/
    main.py                 orchestration and __main__ guard
    attendance.py           reader + statistics + report writer

(c) three_modules/
    main.py                 orchestration and __main__ guard
    reader.py
    stats.py
    report.py

(d) package/
    main.py                 orchestration and __main__ guard
    attendance/
        __init__.py
        reader.py
        stats.py
        report.py
~~~

The code in each directory reads the shared sample input, writes percentage and three-consecutive-day absence reports, and uses an if __name__ == "__main__" guard in the executable main script.

### 5.2 Change effort for the new report

Starting from a percentage-only implementation, the second report needs a statistic that scans each student's dates in order and detects an absence streak of three consecutive calendar days.

| Organization | Files to change | Reason |
|---|---:|---|
| One script | 1 | Add the statistic and output in main.py. |
| One module plus main | 2 | Add the statistic/report function in attendance.py, then call it in main.py. |
| Three modules | 3 | Add the statistic in stats.py, the file output in report.py, and the calls in main.py. |
| Package with public re-exports | 4 | Change stats.py, report.py, attendance/__init__.py exports, and main.py. If callers import attendance.stats directly instead of using package re-exports, the initializer need not change. |

The submitted versions contain both reports, so these counts describe the change from the original one-report requirement.

### 5.3 Comparison

| Organization | Readability | Reuse and testing | Naming conflicts |
|---|---|---|---|
| One script | Easiest for a tiny program; harder to scan as it grows. | Functions can be tested, but importing also loads the single file. | Many helpers share one module namespace. |
| One module | Separates entry point from utility code. | Utility module can be imported and tested; reuse is straightforward. | Fewer main-script names, though all utility functions live together. |
| Three modules | Each file has one responsibility. | Reader, statistics and report code can be tested independently. | Module names such as reader can conflict with unrelated top-level modules. |
| Package | Clear namespace and scalable structure for related modules. | Importable submodules; package API can be controlled in __init__.py. | Package-qualified names reduce collisions; relative imports keep internal modules together. |

- import attendance.stats imports the stats submodule; if it defines percentage, callers use attendance.stats.percentage(...).
- from attendance import stats binds the submodule name stats; callers use stats.percentage(...).
- from attendance.stats import percentage binds the function directly; calls are shorter, but the function name can collide with another imported name.

### Alternative concept and complexity

A package adds a small one-time import and module initialization cost. Python loads each module once per process and caches it in sys.modules; later imports use the cached module. The package's memory use is proportional to its loaded code and module objects, O(m) for package size m, and is typically small beside the records being processed.

Finding a function in one script means searching a larger file. A package places it in a named responsibility module, making focused edits and tests easier as the project grows. The algorithmic time and data memory do not change merely because the same functions are split across modules.

---

## Task 6 — College fest registration design challenge

### Stage 1: Inputs, outputs and testable rules

**Inputs:** five UTF-8 department files; each non-empty line contains register number, name, department, e-mail, and one or more event names separated by semicolons.

**Outputs:**

- A clean master CSV containing one accepted row per register number.
- One CSV participant list per event.
- A summary with unique registration and event counts.
- An error CSV containing source filename, line number (when available), and issue.

**Rules to verify:**

1. A structurally valid row has exactly five fields and non-empty register number, name and department.
2. E-mail validation checks one @, non-empty local and domain parts, no spaces, and a domain containing a dot that does not start or end with a dot. This is a practical check, not complete standards validation.
3. At least one non-empty event is required.
4. The first valid row for a register number is kept; later valid duplicates are logged and ignored.
5. Invalid rows and unreadable or missing department files are logged; the processor continues to later files.
6. Every accepted student appears once in the master file and once in each chosen event's participant file.
7. Sample demonstration accepts five unique registrations and logs four issues: one duplicate, one invalid e-mail, one damaged line, and one missing department file.

### Stage 2: Processing flow

~~~text
Five department paths
        |
        v
Open each file (specific file errors -> error log; continue)
        |
        v
Read one line -> parse field count -> validate required fields/e-mail/events
        | valid                         | invalid
        v                               v
Check register-number set             Add source, line and reason to error list
        | unseen        | duplicate
        v               v
Add to seen set       Log duplicate; keep first valid row
        |
        v
Write master CSV + event participant CSVs + summary + error log
~~~

### Stage 3: Critical decisions

- **Duplicate key:** the register number, stored in a set for average O(1) membership checks. First valid registration wins; invalid rows do not reserve a number.
- **E-mail check:** trim whitespace, require exactly one @, split with partition("@"), require non-empty local and domain pieces, reject spaces, require a dot in the domain, and reject a domain beginning or ending with a dot.
- **Row errors:** parse_registration raises InvalidRegistration; the processor catches it inside the line loop and records the filename and line number.
- **File errors:** catch FileNotFoundError, PermissionError, UnicodeDecodeError, and OSError around each file; record the file-level issue and continue with the next department.
- **Output:** use csv.writer and UTF-8. Event filenames include a sequence number and sanitized event name.

### Stage 4: Package and pseudocode

~~~text
Task06/
    run_demo.py
    fest_registration/
        __init__.py
        validator.py       is_valid_email, parse_registration, InvalidRegistration
        processor.py       process_registration_files
        report.py          write_outputs
    input/
        department_cse.txt
        department_eee.txt
        department_mech.txt
        department_civil.txt
        department_it.txt  intentionally missing in sample
    output/
~~~

~~~text
ALGORITHM PROCESS_REGISTRATION_FILES
INPUT: ordered source_files, output_folder
OUTPUT: master file, event participant files, summary, error log

BEGIN
    seen_register_numbers ← empty set
    accepted_records ← empty dictionary
    errors ← empty list

    FOR EACH source_file IN source_files
        TRY
            OPEN source_file FOR UTF-8 reading
            line_number ← 0

            FOR EACH line IN source_file
                line_number ← line_number + 1
                IF line is blank THEN
                    CONTINUE
                END IF

                TRY
                    record ← PARSE line
                    VALIDATE field count, required fields, e-mail and events
                CATCH InvalidRegistration AS reason
                    APPEND (source_file, line_number, reason) to errors
                    CONTINUE
                END TRY

                IF record.register_number IN seen_register_numbers THEN
                    APPEND duplicate issue to errors
                ELSE
                    ADD record.register_number to seen_register_numbers
                    accepted_records[record.register_number] ← record
                END IF
            END FOR
        CATCH FileNotFoundError, PermissionError, UnicodeDecodeError, OSError AS reason
            APPEND (source_file, no line number, reason) to errors
        END TRY
    END FOR

    GROUP accepted_records by event
    WRITE master CSV
    FOR EACH event group
        WRITE one participant CSV
    END FOR
    WRITE summary and error log
END
~~~

### Stage 5: Demonstration

Run python Task06/run_demo.py. The input set deliberately includes:

- Clean registrations in the CSE, EEE, Mechanical and Civil files.
- Register 192311001 repeated in the EEE file; the CSE record is retained.
- An invalid e-mail kiranexample.edu.
- A damaged Civil row with only four fields.
- A missing department_it.txt.

Expected sample result: 5 accepted unique registrations; 4 issues logged; 4 event participant files for Dance, Drama, Music and Robotics. Inspect Task06/output after execution and capture the terminal plus generated summary/error log in your evidence.

### Alternative concept and complexity

With a list of all previous register numbers, checking each new registration against the list costs O(i) at record i; across n records the worst-case time is O(n²). The set approach costs O(1) on average per membership check and O(n) average total time. Both store up to O(n) register numbers; the accepted records and event participant groups also require O(n + e) memory for n records and e event memberships. The set gives faster duplicate checks without increasing the asymptotic space order.

