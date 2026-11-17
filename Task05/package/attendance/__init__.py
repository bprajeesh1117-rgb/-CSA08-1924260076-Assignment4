"""Attendance processing package."""
from .reader import read_records
from .stats import attendance_percentages, absent_three_days
from .report import write_reports

__all__ = ["read_records", "attendance_percentages", "absent_three_days", "write_reports"]

