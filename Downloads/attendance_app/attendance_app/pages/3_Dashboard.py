"""
pages/3_Dashboard.py
----------------------
Real-time attendance and work-progress overview. Admins see a
company-wide snapshot for today; employees see their own status.
"""

from datetime import date

import streamlit as st

import config
from database.db_setup import get_session
from database.models import Employee, Attendance, Task
from utils.auth import require_login, is_admin, current_employee_id
from utils.calculations import compute_live_elapsed_hours, task_progress_summary
from utils.ui import (
    inject_global_css, render_sidebar_brand, hero, section_title,
    kpi_card, status_badge, muted_text,
)

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
inject_global_css()
require_login()
render_sidebar_brand(config.APP_NAME, config.APP_ICON)
hero("Dashboard", "Real-time attendance and work-progress overview.", icon="📊")

session = get_session()
today = date.today()

if is_admin():
    employees = session.query(Employee).filter_by(is_active=True).order_by(Employee.full_name).all()
    today_records = {
        r.employee_id: r
        for r in session.query(Attendance).filter_by(date=today).all()
    }
    tasks = session.query(Task).all()

    present = sum(1 for r in today_records.values() if r.status in ("Present", "Late", "Half-Day"))
    late = sum(1 for r in today_records.values() if r.status == "Late")
    absent = len(employees) - len(today_records)
    total_hours = sum(
        (compute_live_elapsed_hours(r.check_in, r.check_out) if r.check_in else 0.0)
        for r in today_records.values()
    )
    avg_hours = round(total_hours / len(today_records), 2) if today_records else 0.0
    progress = task_progress_summary(tasks)

    section_title("Today's Snapshot", "📅")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        kpi_card("👥", "Total Employees", len(employees))
    with c2:
        kpi_card("✅", "Present Today", present, color="#1E8E5A")
    with c3:
        kpi_card("⏰", "Late Today", late, color="#C77700")
    with c4:
        kpi_card("🚫", "Absent Today", max(absent, 0), color="#C0392B")
    with c5:
        kpi_card("⏱️", "Avg Hours Today", f"{avg_hours:.2f}")
    with c6:
        kpi_card("📋", "Task Completion", f"{progress['completion_pct']}%")

    section_title("Employee Status — Today", "🧑‍💼")
    if not employees:
        st.info("No active employees yet.")
    else:
        for emp in employees:
            rec = today_records.get(emp.id)
            with st.container(border=True):
                c1, c2, c3, c4, c5 = st.columns([2.3, 1.1, 1.1, 1.1, 1.3])
                with c1:
                    st.markdown(f"**{emp.full_name}**")
                    st.markdown(muted_text(emp.department or "—"), unsafe_allow_html=True)
                with c2:
                    st.markdown(status_badge(rec.status) if rec else status_badge("Absent"), unsafe_allow_html=True)
                with c3:
                    st.markdown(muted_text(f"In: {rec.check_in.strftime('%H:%M') if rec and rec.check_in else '—'}"), unsafe_allow_html=True)
                with c4:
                    st.markdown(muted_text(f"Out: {rec.check_out.strftime('%H:%M') if rec and rec.check_out else '—'}"), unsafe_allow_html=True)
                with c5:
                    if rec and rec.check_in and not rec.check_out:
                        live = compute_live_elapsed_hours(rec.check_in, rec.check_out)
                        st.markdown(muted_text(f"{live:.2f} hrs (live)"), unsafe_allow_html=True)
                    else:
                        hrs = rec.hours_worked if rec else 0.0
                        st.markdown(muted_text(f"{hrs:.2f} hrs"), unsafe_allow_html=True)

    section_title("Work Progress Overview", "📋")
    p1, p2, p3, p4, p5 = st.columns(5)
    p1.metric("Total Tasks", progress["total"])
    p2.metric("Completed", progress["completed"])
    p3.metric("In Progress", progress["in_progress"])
    p4.metric("Not Started", progress["not_started"])
    p5.metric("Overdue", progress["overdue"])

else:
    employee = session.query(Employee).get(current_employee_id())
    if not employee:
        st.error("No employee profile linked to this account.")
        st.stop()

    record = session.query(Attendance).filter_by(employee_id=employee.id, date=today).first()
    my_tasks = session.query(Task).filter_by(employee_id=employee.id).all()
    progress = task_progress_summary(my_tasks)

    if record and record.check_in and not record.check_out:
        live_hours = compute_live_elapsed_hours(record.check_in, record.check_out)
        hours_display = f"{live_hours:.2f} (live)"
    else:
        hours_display = f"{record.hours_worked:.2f}" if record else "0.00"

    section_title(f"Welcome back, {employee.full_name}", "👋")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("📌", "Today's Status", record.status if record else "Absent")
    with c2:
        kpi_card("⏱️", "Hours Today", hours_display)
    with c3:
        kpi_card("📋", "My Task Completion", f"{progress['completion_pct']}%")
    with c4:
        kpi_card("⚠️", "Overdue Tasks", progress["overdue"], color="#C0392B" if progress["overdue"] else "#1E8E5A")

    if record:
        st.markdown(status_badge(record.status), unsafe_allow_html=True)

    section_title("My Tasks Summary", "📋")
    t1, t2, t3, t4 = st.columns(4)
    t1.metric("Total", progress["total"])
    t2.metric("Completed", progress["completed"])
    t3.metric("In Progress", progress["in_progress"])
    t4.metric("Not Started", progress["not_started"])
