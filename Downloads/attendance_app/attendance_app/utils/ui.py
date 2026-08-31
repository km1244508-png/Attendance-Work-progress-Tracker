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

        /* FIX: st.caption() text was being forced to dark/near-invisible
           by the rule above in some contexts. Give captions their own
           reliable muted style with higher specificity so they always
           render, e.g. task descriptions in Work Progress. */
        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] p,
        .stCaption, .stCaption p {{
            color: {TEXT_MUTED} !important;
            opacity: 1 !important;
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

        /* FIX: text/time/number/date inputs, text areas, and selects were
           rendering with Streamlit's default dark theme (dark box, barely
           visible text) even though the rest of the app uses a light
           theme. Force a light, readable style on every input widget. */
        input, textarea,
        [data-baseweb="input"], [data-baseweb="textarea"],
        [data-baseweb="select"], [data-baseweb="base-input"],
        div[data-testid="stTimeInput"] input,
        div[data-testid="stDateInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea {{
            background-color: #FFFFFF !important;
            color: {TEXT_DARK} !important;
            border: 1px solid #C9D2E0 !important;
            border-radius: 8px !important;
        }}
        /* The wrapping container BaseWeb draws around inputs also needs
           its background lightened, or the white input floats inside a
           dark box with mismatched padding. */
        [data-baseweb="input"] > div,
        [data-baseweb="textarea"] > div,
        [data-baseweb="select"] > div {{
            background-color: #FFFFFF !important;
        }}

        /* FIX: st.date_input doesn't render as a plain <input> — it's a
           BaseWeb "datepicker" made of separate year/month/day spin
           fields inside nested divs, none of which matched the rules
           above. That left the date box solid black with barely-visible
           text (as seen on Mark Attendance). Force every layer of it
           light, not just the outermost wrapper. */
        div[data-testid="stDateInput"] > div,
        div[data-testid="stDateInput"] div,
        div[data-testid="stDateInput"] [data-baseweb="datepicker"],
        div[data-testid="stDateInput"] [role="spinbutton"] {{
            background-color: #FFFFFF !important;
            color: {TEXT_DARK} !important;
        }}
        div[data-testid="stDateInput"] > div {{
            border: 1px solid #C9D2E0 !important;
            border-radius: 8px !important;
        }}

        /* FIX: st.time_input has the exact same BaseWeb structure problem
           as st.date_input above — it's not a plain <input>, so it was
           still rendering as a solid black box (seen on the Manual Time
           Entry check-in/check-out fields). Same broad fix. */
        div[data-testid="stTimeInput"] > div,
        div[data-testid="stTimeInput"] div,
        div[data-testid="stTimeInput"] [data-baseweb] {{
            background-color: #FFFFFF !important;
            color: {TEXT_DARK} !important;
        }}
        div[data-testid="stTimeInput"] > div {{
            border: 1px solid #C9D2E0 !important;
            border-radius: 8px !important;
        }}

        /* FIX: st.button / st.download_button / st.form_submit_button were
           rendering with Streamlit's dark default (black background, low-
           contrast text) — "Deactivate", "Download Excel", "Download PDF"
           etc. were unreadable black squares. Force a light, bordered
           style for ordinary buttons, and a solid accent-color fill (with
           guaranteed white text) for primary buttons. */
        div[data-testid="stButton"] button,
        div[data-testid="stDownloadButton"] button,
        div[data-testid="stFormSubmitButton"] button {{
            background-color: #FFFFFF !important;
            color: {NAVY} !important;
            border: 1.5px solid {NAVY} !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }}
        div[data-testid="stButton"] button *,
        div[data-testid="stDownloadButton"] button *,
        div[data-testid="stFormSubmitButton"] button * {{
            color: inherit !important;
        }}
        div[data-testid="stButton"] button:hover,
        div[data-testid="stDownloadButton"] button:hover,
        div[data-testid="stFormSubmitButton"] button:hover {{
            background-color: {LIGHT_BG} !important;
            border-color: {BLUE} !important;
        }}
        div[data-testid="stButton"] button[kind="primary"],
        div[data-testid="stDownloadButton"] button[kind="primary"],
        div[data-testid="stFormSubmitButton"] button[kind="primary"] {{
            background-color: {BLUE} !important;
            border-color: {BLUE} !important;
            color: #FFFFFF !important;
        }}
        div[data-testid="stButton"] button[kind="primary"] *,
        div[data-testid="stDownloadButton"] button[kind="primary"] *,
        div[data-testid="stFormSubmitButton"] button[kind="primary"] * {{
            color: #FFFFFF !important;
        }}
        div[data-testid="stButton"] button:disabled,
        div[data-testid="stDownloadButton"] button:disabled,
        div[data-testid="stFormSubmitButton"] button:disabled {{
            background-color: #EDEFF3 !important;
            color: #A6AEBB !important;
            border-color: #D8DEE8 !important;
        }}

        /* Placeholder text (e.g. "Press Enter to submit form") */
        input::placeholder, textarea::placeholder {{
            color: {TEXT_MUTED} !important;
            opacity: 1 !important;
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

        /* Reusable muted-text helper for anything rendered via
           st.markdown(..., unsafe_allow_html=True) instead of
           st.caption() — used by task descriptions, notes, etc. */
        .muted-text {{
            color: {TEXT_MUTED} !important;
            font-size: 0.85rem;
            line-height: 1.4;
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


def muted_text(text: str) -> str:
    """HTML-safe muted caption line — use instead of st.caption() wherever
    text has previously appeared to not show up (e.g. inside custom
    st.markdown blocks that also carry unsafe_allow_html=True)."""
    return f'<div class="muted-text">{text}</div>'


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
