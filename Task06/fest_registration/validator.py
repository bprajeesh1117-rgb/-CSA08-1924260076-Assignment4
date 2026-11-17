"""Validation for a registration record."""
import csv


class InvalidRegistration(Exception):
    """A registration row has invalid structure or field values."""


def is_valid_email(email):
    """Apply practical email checks using string methods (not full RFC validation)."""
    candidate = email.strip()
    if candidate != email or candidate.count("@") != 1 or " " in candidate:
        return False
    local_part, separator, domain = candidate.partition("@")
    if not separator or not local_part or not domain:
        return False
    if "." not in domain or domain.startswith(".") or domain.endswith("."):
        return False
    return True


def parse_registration(raw_line):
    """Parse register,name,department,email,event1;event2 into a dictionary."""
    try:
        fields = next(csv.reader([raw_line], skipinitialspace=True))
    except (csv.Error, StopIteration) as error:
        raise InvalidRegistration(f"cannot parse CSV row: {error}") from error
    if len(fields) != 5:
        raise InvalidRegistration(f"expected 5 fields, found {len(fields)}")

    register_number, name, department, email, event_text = [
        field.strip() for field in fields
    ]
    if not register_number or not name or not department:
        raise InvalidRegistration("register number, name and department are required")
    if not is_valid_email(email):
        raise InvalidRegistration(f"invalid email {email!r}")

    events = [event.strip() for event in event_text.split(";") if event.strip()]
    if not events:
        raise InvalidRegistration("at least one event is required")

    return {
        "register_number": register_number,
        "name": name,
        "department": department,
        "email": email,
        "events": events,
    }

