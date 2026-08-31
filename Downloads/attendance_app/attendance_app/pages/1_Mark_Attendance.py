"""
pages/1_Mark_Attendance.py
---------------------------
Record daily check-in / check-out. Admins can mark for any employee;
regular employees can only mark their own attendance.
"""

from datetime import datetime, date, time as dtime

import streamlit as st

import config
from database.db_setup import get_session
from database.models import Employee, Attendance
from utils.auth import require_login, is_admin, current_employee_id
from utils.calculations import evaluate_attendance, compute_live_elapsed_hours
from utils.ui import inject_global_css, render_sidebar_brand, hero, section_title, status_badge

st.set_page_config(page_title="Mark Attendance", page_icon="🕒", layout="wide")
inject_global_css()
require_login()
render_sidebar_brand(config.APP_NAME, config.APP_ICON)

hero("Mark Attendance", "Record check-in and check-out times.", icon="🕒")

session = get_session()

# ---------------------------------------------------------------------
# Choose employee (admin can pick anyone; employee is locked to self)
# ---------------------------------------------------------------------
if is_admin():
    employees = session.query(Employee).filter_by(is_active=True).order_by(Employee.full_name).all()
    if not employees:
        st.warning("No active employees found. Add employees from Employee Management first.")
        st.stop()
    names = [e.full_name for e in employees]
    selected_name = st.selectbox("Employee", names)
    employee = next(e for e in employees if e.full_name == selected_name)
else:
    employee = session.query(Employee).get(current_employee_id())
    if not employee:
        st.error("No employee profile linked to this account.")
        st.stop()
    st.markdown(f"Marking attendance for **{employee.full_name}**")

target_date = st.date_input("Date", value=date.today())

record = (
    session.query(Attendance)
    .filter_by(employee_id=employee.id, date=target_date)
    .first()
)

section_title("Today's Record", "📋")
col1, col2, col3 = st.columns(3)
col1.metric("Check In", record.check_in.strftime("%H:%M") if record and record.check_in else "—")
col2.metric("Check Out", record.check_out.strftime("%H:%M") if record and record.check_out else "—")

# Live hours: while checked in but not yet checked out, count up to
# "now" instead of showing a frozen 0.00 until check-out happens.
if record and record.check_in and not record.check_out:
    live_hours = compute_live_elapsed_hours(record.check_in, record.check_out)
    col3.metric("Hours Worked (live)", f"{live_hours:.2f}")
else:
    col3.metric("Hours Worked", f"{record.hours_worked:.2f}" if record else "0.00")

if record:
    st.markdown(status_badge(record.status), unsafe_allow_html=True)
    if record.check_in and not record.check_out:
        if st.button("🔄 Refresh live hours"):
            st.rerun()

st.markdown("---")

c1, c2 = st.columns(2)
with c1:
    if st.button("✅ Check In", use_container_width=True, type="primary",
                 disabled=bool(record and record.check_in)):
        if not record:
            record = Attendance(employee_id=employee.id, date=target_date)
            session.add(record)
        record.check_in = datetime.combine(target_date, datetime.now().time())
        result = evaluate_attendance(record.check_in, record.check_out, employee)
        for k, v in result.items():
            setattr(record, k, v)
        session.commit()
        st.success(f"Checked in at {record.check_in.strftime('%H:%M')}")
        st.rerun()

with c2:
    if st.button("🚪 Check Out", use_container_width=True,
                 disabled=not (record and record.check_in) or bool(record and record.check_out)):
        record.check_out = datetime.combine(target_date, datetime.now().time())
        result = evaluate_attendance(record.check_in, record.check_out, employee)
        for k, v in result.items():
            setattr(record, k, v)
        session.commit()
        st.success(f"Checked out at {record.check_out.strftime('%H:%M')}")
        st.rerun()

if is_admin():
    st.markdown("---")
    section_title("Manual Correction (Admin)", "🛠️")
    with st.form("manual_correction"):
        # FIX: st.time_input(..., value=None) does NOT mean "empty" — Streamlit
        # silently defaults it to the current clock time. So even when an
        # admin left check-out untouched, it was quietly being saved as
        # "right now", which produced a near-zero (or otherwise wrong)
        # hours_worked and could push the status to "Half-Day" for an
        # employee who never actually checked out. An explicit checkbox now
        # controls whether a field is empty, instead of relying on the
        # widget's default.
        mc1, mc2 = st.columns(2)
        with mc1:
            no_check_in = st.checkbox("No check-in recorded", value=not (record and record.check_in))
            in_time = st.time_input(
                "Check-in time",
                value=record.check_in.time() if record and record.check_in else dtime(9, 0),
                disabled=no_check_in,
            )
        with mc2:
            no_check_out = st.checkbox("No check-out recorded", value=not (record and record.check_out))
            out_time = st.time_input(
                "Check-out time",
                value=record.check_out.time() if record and record.check_out else dtime(17, 0),
                disabled=no_check_out,
            )
        notes = st.text_area("Notes (optional)", value=record.notes if record else "")
        if st.form_submit_button("Save Correction"):
            if not record:
                record = Attendance(employee_id=employee.id, date=target_date)
                session.add(record)
            record.check_in = None if no_check_in else datetime.combine(target_date, in_time)
            record.check_out = None if no_check_out else datetime.combine(target_date, out_time)
            record.notes = notes
            result = evaluate_attendance(record.check_in, record.check_out, employee)
            for k, v in result.items():
                setattr(record, k, v)
            session.commit()
            st.success("Attendance record updated.")
            st.rerun()
