"""Demonstrates how except Exception: pass hides a misspelled counter."""
def count_present_with_typo(lines):
    present = 0
    for line in lines:
        try:
            status = line.strip().split(",")[2]
            if status == "P":
                presnt += 1  # Intentional typo: should be present.
        except Exception:
            pass
    return present


if __name__ == "__main__":
    rows = ["192311001,2026-10-08,P"]
    print(count_present_with_typo(rows))

