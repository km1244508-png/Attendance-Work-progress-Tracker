"""
app.py
------
Login screen and landing page — entry point of the app.
"""

import streamlit as st

import config
from database.db_setup import init_db, default_admin_notice, default_admin_still_active
from utils.auth import login, logout, is_logged_in, is_admin
from utils.ui import inject_global_css, hero, section_title, render_sidebar_brand

st.set_page_config(
    page_title=config.APP_NAME,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_global_css()

# Create tables + seed default admin on first run (safe to call every time).
init_db()


def render_login():
    st.markdown("<div style='height:4vh'></div>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.15, 1])
    with col:
        st.markdown(
            f"""
            <div style="text-align:center;margin-bottom:18px;">
                <div style="font-size:2.6rem;">{config.APP_ICON}</div>
                <div style="font-size:1.5rem;font-weight:800;color:#1F3864;margin-top:4px;">
                    {config.APP_NAME}
                </div>
                <div style="color:#66707F;font-size:0.95rem;margin-top:4px;">
                    Sign in to your workspace
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="e.g. admin")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Log In →", type="primary", use_container_width=True)

        if submitted:
            if login(username, password):
                st.success("Login successful.")
                st.rerun()
            else:
                st.error("Invalid username or password.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        if default_admin_still_active():
            st.info(default_admin_notice())


def render_landing():
    render_sidebar_brand(config.APP_NAME, config.APP_ICON)

    role = st.session_state.get("auth_role")
    username = st.session_state.get("auth_username")

    hero(
        f"Welcome back, {username} 👋",
        f"You're signed in as <b>{role}</b>. Use the sidebar to navigate the workspace.",
        icon=config.APP_ICON,
    )

    if is_admin():
        cards = [
            ("🕒", "Mark Attendance", "Record daily check-in / check-out for employees."),
            ("👥", "Employee Management", "Add, edit, or deactivate employees and login accounts."),
            ("📊", "Dashboard", "Real-time attendance and work-progress overview."),
            ("📑", "Reports", "Daily, weekly, monthly, individual & comparative reports."),
            ("📋", "Work Progress", "Assign and track tasks per employee."),
        ]
    else:
        cards = [
            ("📊", "Dashboard", "Your personal attendance overview."),
            ("📑", "Reports", "Your own attendance history, exportable anytime."),
            ("📋", "Work Progress", "View and update your assigned tasks."),
        ]

    section_title("Quick Navigation", "🧭")
    cols = st.columns(len(cards))
    for c, (icon, label, desc) in zip(cols, cards):
        with c:
            st.markdown(
                f"""
                <div class="kpi-card" style="--kpi-color:#2E74B5; min-height:150px;">
                    <div class="kpi-icon">{icon}</div>
                    <div style="font-weight:700;color:#1A1F2B;font-size:1.02rem;margin-bottom:4px;">{label}</div>
                    <div style="color:#66707F;font-size:0.85rem;line-height:1.4;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


if not is_logged_in():
    render_login()
else:
    render_landing()
