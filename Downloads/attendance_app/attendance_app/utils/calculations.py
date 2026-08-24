"""
utils/calculations.py
----------------------
Pure calculation logic for attendance status, hours worked, lateness,
and overtime. All thresholds are pulled from config.py — never
hardcoded here — so business-rule changes stay in one place.
"""

from datetime import datetime, date, time as dtime
from typing import Optional

import config


def _parse_hhmm(value: str) -> dtime:
    h, m = value.split(":")
    return dtime(int(h), int(m))


def get_shift_bounds(employee) -> tuple[dtime, dtime]:
    """Return (shift_start, shift_end) for an employee, falling back to config defaults."""
    start = _parse_hhmm(employee.shift_start) if getattr(employee, "shift_start", None) else _parse_hhmm(config.DEFAULT_SHIFT_START)
    end = _parse_hhmm(employee.shift_end) if getattr(employee, "shift_end", None) else _parse_hhmm(config.DEFAULT_SHIFT_END)
    return start, end


def is_working_day(d: date) -> bool:
    """Monday=0 ... Sunday=6, per config.WORKING_DAYS."""
    return d.weekday() in config.WORKING_DAYS


def compute_hours_worked(check_in: Optional[datetime], check_out: Optional[datetime]) -> float:
    if not check_in or not check_out:
        return 0.0
    delta = check_out - check_in
    hours = delta.total_seconds() / 3600.0
    return round(max(hours, 0.0), 2)


def compute_lateness(check_in: Optional[datetime], employee) -> bool:
    """True if check-in is later than shift start + grace period."""
    if not check_in:
        return False
    shift_start, _ = get_shift_bounds(employee)
    scheduled = datetime.combine(check_in.date(), shift_start)
    grace_cutoff = scheduled.timestamp() + config.GRACE_PERIOD_MINUTES * 60
    return check_in.timestamp() > grace_cutoff


def compute_overtime(hours_worked: float) -> float:
    if hours_worked > config.OVERTIME_THRESHOLD_HOURS:
        return round(hours_worked - config.OVERTIME_THRESHOLD_HOURS, 2)
    return 0.0


def compute_status(hours_worked: float, is_late: bool, has_checkin: bool) -> str:
    """
    Present / Late / Half-Day / Absent, in priority order:
    no check-in -> Absent; below half-day threshold -> Half-Day;
    late (but full hours) -> Late; otherwise -> Present.
    """
    if not has_checkin or hours_worked <= 0:
        return "Absent"
    if hours_worked < config.HALF_DAY_THRESHOLD_HOURS:
        return "Half-Day"
    if is_late:
        return "Late"
    return "Present"


def evaluate_attendance(check_in: Optional[datetime], check_out: Optional[datetime], employee) -> dict:
    """Run the full pipeline and return all derived attendance fields."""
    hours_worked = compute_hours_worked(check_in, check_out)
    is_late = compute_lateness(check_in, employee)
    overtime = compute_overtime(hours_worked)
    status = compute_status(hours_worked, is_late, has_checkin=check_in is not None)
    return {
        "hours_worked": hours_worked,
        "is_late": is_late,
        "overtime_hours": overtime,
        "status": status,
    }


def task_progress_summary(tasks) -> dict:
    """Given a list of Task ORM objects, return counts + completion %."""
    total = len(tasks)
    if total == 0:
        return {"total": 0, "completed": 0, "in_progress": 0,
                "not_started": 0, "on_hold": 0, "completion_pct": 0.0,
                "overdue": 0}

    completed = sum(1 for t in tasks if t.status == config.TASK_STATUS_COMPLETED)
    in_progress = sum(1 for t in tasks if t.status == config.TASK_STATUS_IN_PROGRESS)
    not_started = sum(1 for t in tasks if t.status == config.TASK_STATUS_NOT_STARTED)
    on_hold = sum(1 for t in tasks if t.status == config.TASK_STATUS_ON_HOLD)

    today = date.today()
    overdue = sum(
        1 for t in tasks
        if t.due_date and t.due_date < today and t.status != config.TASK_STATUS_COMPLETED
    )

    return {
        "total": total,
        "completed": completed,
        "in_progress": in_progress,
        "not_started": not_started,
        "on_hold": on_hold,
        "completion_pct": round((completed / total) * 100, 1),
        "overdue": overdue,
    }
