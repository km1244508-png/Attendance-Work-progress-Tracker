"""
utils/ui.py
-----------
Shared design system: global CSS, KPI cards, hero banners, section
titles, sidebar branding, and status badges. Keep all color/style
constants here so branding can be changed from one place.
"""

import streamlit as st

NAVY = "#1F3864"
BLUE = "#2E74B5"
LIGHT_BG = "#F5F7FA"
TEXT_MUTED = "#66707F"
TEXT_DARK = "#1A1F2B"

STATUS_COLORS = {
    "Present": "#1E8E5A",
    "Late": "#C77700",
    "Half-Day": "#B8860B",
    "Absent": "#C0392B",
    "Not Started": "#8A93A3",
    "In Progress": "#2E74B5",
    "Completed": "#1E8E5A",
    "On Hold": "#C77700",
}


def inject_global_css():
    st.markdown(
        f"""
        <style>
        .stApp {{ background-color: {LIGHT_BG}; }}
        #MainMenu, footer {{ visibility: hidden; }}

        /* Main area text color fix */
        .stApp, .stMarkdown, p, span, label {{
            color: {TEXT_DARK} !important;
        }}

        /* Tab buttons and titles visible fix */
        button[data-baseweb="tab"] {{
            color: {TEXT_MUTED} !important;
        }}
        button[data-baseweb="tab"] p {{
            color: {TEXT_MUTED} !important;
            font-size: 15px !important;
            font-weight: 600 !important;
        }}
        button[data-baseweb="tab"][aria-selected="true"] p {{
            color: {NAVY} !important;
            font-weight: 800 !important;
        }}

        /* Download buttons (Excel / PDF) full styling */
        .stDownloadButton button {{
            background-color: {NAVY} !important;
            color: #FFFFFF !important;
            border: 1px solid {NAVY} !important;
            border-radius: 8px !important;
            padding: 8px 24px !important;
            font-weight: 700 !important;
            transition: all 0.2s ease !important;
        }}
        .stDownloadButton button:hover {{
            background-color: {BLUE} !important;
            border-color: {BLUE} !important;
            color: #FFFFFF !important;
        }}
        .stDownloadButton button p, .stDownloadButton button span {{
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }}

        .login-card {{
            background: white;
            padding: 28px 32px;
            border-radius: 14px;
            box-shadow: 0 4px 24px rgba(31,56,100,0.08);
            border: 1px solid #E7EBF1;
        }}

        .hero-banner {{
            background: linear-gradient(135deg, {NAVY} 0%, {BLUE} 100%);
            color: white;
            padding: 28px 32px;
            border-radius: 14px;
            margin-bottom: 22px;
        }}
        .hero-banner h1 {{
            color: white !important;
            font-size: 1.6rem;
            margin: 0 0 6px 0;
            font-weight: 800;
        }}
        .hero-banner p {{
            color: white !important;
            margin: 0;
            opacity: 0.92;
            font-size: 0.98rem;
        }}

        .kpi-card {{
            background: white;
            border-radius: 12px;
            padding: 18px 16px;
            border: 1px solid #E7EBF1;
            border-top: 3px solid var(--kpi-color, {BLUE});
            box-shadow: 0 2px 10px rgba(31,56,100,0.05);
            transition: transform 0.15s ease;
        }}
        .kpi-card:hover {{ transform: translateY(-2px); }}
        .kpi-icon {{ font-size: 1.6rem; margin-bottom: 6px; }}

        .section-title {{
            font-weight: 800;
            color: {NAVY} !important;
            font-size: 1.15rem;
            margin: 18px 0 10px 0;
        }}

        .status-badge {{
            display: inline-block;
            padding: 3px 12px;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 700;
            color: white !important;
        }}

        section[data-testid="stSidebar"] {{
            background-color: {NAVY};
        }}
        section[data-testid="stSidebar"] * {{ 
            color: #EAF0FA !important; 
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle_html: str, icon: str = "🕒"):
    st.markdown(
        f"""
        <div class="hero-banner">
            <h1>{icon} {title}</h1>
            <p>{subtitle_html}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(text: str, icon: str = ""):
    st.markdown(
        f'<div class="section-title">{icon} {text}</div>',
        unsafe_allow_html=True,
    )


def render_sidebar_brand(app_name: str, app_icon: str):
    with st.sidebar:
        st.markdown(
            f"""
            <div style="text-align:center;padding:10px 0 18px 0;">
                <div style="font-size:2rem;">{app_icon}</div>
                <div style="font-weight:800;font-size:1.0rem;line-height:1.3;">{app_name}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def status_badge(status: str) -> str:
    color = STATUS_COLORS.get(status, "#8A93A3")
    return f'<span class="status-badge" style="background:{color};">{status}</span>'


def kpi_card(icon: str, label: str, value, color: str = BLUE):
    st.markdown(
        f"""
        <div class="kpi-card" style="--kpi-color:{color};">
            <div class="kpi-icon">{icon}</div>
            <div style="font-weight:700;color:{TEXT_DARK};font-size:1.4rem;">{value}</div>
            <div style="color:{TEXT_MUTED};font-size:0.85rem;">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )