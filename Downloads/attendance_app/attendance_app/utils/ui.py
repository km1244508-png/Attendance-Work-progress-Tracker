"""
utils/ui.py
-----------
Shared design system: global CSS, KPI cards, hero banners, section
titles, sidebar branding, and status badges. Keep all color/style
constants here so branding can be changed from one place.
"""

import streamlit as st

NAVY = "#1F3864"
NAVY_DARK = "#152747"
BLUE = "#2E74B5"
LIGHT_BG = "#F5F7FA"
TEXT_MUTED = "#66707F"
TEXT_DARK = "#1A1F2B"
BORDER = "#E7EBF1"

# A small curated accent palette used to give repeating card grids
# (Quick Navigation, KPI rows, etc.) visual variety without breaking
# the overall navy/blue brand identity.
ACCENT_PALETTE = ["#2E74B5", "#5B5FC7", "#0E9F6E", "#D97706", "#DB2777", "#0EA5A5"]

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
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, .stApp, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        }}

        .stApp {{ background-color: {LIGHT_BG}; }}
        #MainMenu, footer, header[data-testid="stHeader"] {{ visibility: hidden; }}

        .block-container {{
            padding-top: 2.2rem !important;
            padding-bottom: 3rem !important;
            max-width: 1200px;
        }}

        /* ---------------------------------------------------------------
           Equal-height card rows: whenever cards are laid out with
           st.columns(), stretch every column to the tallest one in that
           row so cards with shorter text don't end up visually shorter.
        --------------------------------------------------------------- */
        div[data-testid="stHorizontalBlock"] {{
            align-items: stretch !important;
            gap: 4px;
        }}
        div[data-testid="column"] {{
            display: flex !important;
        }}
        div[data-testid="column"] > div {{
            width: 100%;
            display: flex;
        }}
        div[data-testid="column"] div[data-testid="stVerticalBlock"] {{
            width: 100%;
            height: 100%;
        }}
        div[data-testid="column"] div[data-testid="stVerticalBlockBorderWrapper"] {{
            height: 100%;
        }}

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

        /* FIX: color-scheme was inherited as "dark" from Streamlit's base
           theme, which makes the BROWSER itself paint native form widgets
           (date/time pickers, their clock/calendar icons, spin arrows)
           with dark chrome — no CSS background/color override can beat
           that, only color-scheme can. This was the real reason the date
           and time boxes stayed black no matter what background-color we
           set. Forcing light here fixes the native chrome everywhere. */
        html, body, .stApp {{
            color-scheme: light !important;
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
           Entry check-in/check-out fields). Same broad fix, plus the
           color-scheme fix above for the native picker chrome. */
        div[data-testid="stTimeInput"],
        div[data-testid="stTimeInput"] > div,
        div[data-testid="stTimeInput"] div,
        div[data-testid="stTimeInput"] [data-baseweb],
        div[data-testid="stTimeInput"] input {{
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
           etc. were unreadable black squares. The first attempt at this
           only targeted the wrapping <div data-testid="stButton">, but
           this Streamlit version puts the testid on the <button> itself
           (data-testid="stBaseButton-secondary/primary"), so that rule
           never matched. Covering both patterns here, plus the plain
           kind="..." attribute, so this works regardless of version. */
        div[data-testid="stButton"] button,
        div[data-testid="stDownloadButton"] button,
        div[data-testid="stFormSubmitButton"] button,
        button[kind="secondary"],
        button[data-testid="stBaseButton-secondary"],
        button[data-testid="stBaseButton-secondaryFormSubmit"] {{
            background-color: #FFFFFF !important;
            color: {NAVY} !important;
            border: 1.5px solid {NAVY} !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }}
        div[data-testid="stButton"] button *,
        div[data-testid="stDownloadButton"] button *,
        div[data-testid="stFormSubmitButton"] button *,
        button[kind="secondary"] *,
        button[data-testid="stBaseButton-secondary"] *,
        button[data-testid="stBaseButton-secondaryFormSubmit"] * {{
            color: inherit !important;
        }}
        div[data-testid="stButton"] button:hover,
        div[data-testid="stDownloadButton"] button:hover,
        div[data-testid="stFormSubmitButton"] button:hover,
        button[kind="secondary"]:hover,
        button[data-testid="stBaseButton-secondary"]:hover,
        button[data-testid="stBaseButton-secondaryFormSubmit"]:hover {{
            background-color: {LIGHT_BG} !important;
            border-color: {BLUE} !important;
        }}
        div[data-testid="stButton"] button[kind="primary"],
        div[data-testid="stDownloadButton"] button[kind="primary"],
        div[data-testid="stFormSubmitButton"] button[kind="primary"],
        button[kind="primary"],
        button[data-testid="stBaseButton-primary"],
        button[data-testid="stBaseButton-primaryFormSubmit"] {{
            background-color: {BLUE} !important;
            border: 1.5px solid {BLUE} !important;
            color: #FFFFFF !important;
        }}
        div[data-testid="stButton"] button[kind="primary"] *,
        div[data-testid="stDownloadButton"] button[kind="primary"] *,
        div[data-testid="stFormSubmitButton"] button[kind="primary"] *,
        button[kind="primary"] *,
        button[data-testid="stBaseButton-primary"] *,
        button[data-testid="stBaseButton-primaryFormSubmit"] * {{
            color: #FFFFFF !important;
        }}
        button:disabled, button:disabled * {{
            background-color: #EDEFF3 !important;
            color: #A6AEBB !important;
            border-color: #D8DEE8 !important;
        }}

        /* Placeholder text (e.g. "Press Enter to submit form") */
        input::placeholder, textarea::placeholder {{
            color: {TEXT_MUTED} !important;
            opacity: 1 !important;
        }}

        /* Generic "card" look for bordered containers, e.g.
           st.container(border=True) on the login screen. */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > div[data-testid="stVerticalBlock"]) {{
            border-radius: 14px !important;
        }}
        [data-testid="stForm"] {{
            border: none !important;
            padding: 0 !important;
            background: transparent !important;
        }}
        .login-card,
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: white;
            border-radius: 14px !important;
            box-shadow: 0 4px 24px rgba(31,56,100,0.08);
            border: 1px solid {BORDER} !important;
        }}

        .hero-banner {{
            background: linear-gradient(135deg, {NAVY} 0%, {BLUE} 100%);
            color: white;
            padding: 30px 34px;
            border-radius: 16px;
            margin-bottom: 26px;
            box-shadow: 0 8px 28px rgba(31,56,100,0.18);
            position: relative;
            overflow: hidden;
        }}
        .hero-banner::after {{
            content: "";
            position: absolute;
            top: -60%; right: -8%;
            width: 260px; height: 260px;
            border-radius: 50%;
            background: rgba(255,255,255,0.06);
        }}
        .hero-banner h1 {{
            color: white !important;
            font-size: 1.65rem;
            margin: 0 0 6px 0;
            font-weight: 800;
            position: relative;
        }}
        .hero-banner p {{
            color: white !important;
            margin: 0;
            opacity: 0.9;
            font-size: 0.98rem;
            position: relative;
        }}

        /* ---------------------------------------------------------------
           Cards (Quick Navigation tiles, KPI stat cards). Flex column so
           the description can grow to fill leftover space, which keeps
           every card in a row the same footprint regardless of how much
           text it holds — combined with the equal-height row rules above.
        --------------------------------------------------------------- */
        .kpi-card {{
            background: white;
            border-radius: 14px;
            padding: 20px 18px;
            border: 1px solid {BORDER};
            border-top: 3px solid var(--kpi-color, {BLUE});
            box-shadow: 0 2px 10px rgba(31,56,100,0.05);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            display: flex;
            flex-direction: column;
            width: 100%;
            box-sizing: border-box;
        }}
        .kpi-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 24px rgba(31,56,100,0.12);
        }}
        .kpi-icon {{
            width: 42px;
            height: 42px;
            border-radius: 11px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            background: color-mix(in srgb, var(--kpi-color, {BLUE}) 14%, white);
            margin-bottom: 12px;
            flex-shrink: 0;
        }}
        .kpi-title {{
            font-weight: 700;
            color: {TEXT_DARK};
            font-size: 1.02rem;
            margin-bottom: 4px;
        }}
        .kpi-value {{
            font-weight: 700;
            color: {TEXT_DARK};
            font-size: 1.4rem;
        }}
        .kpi-desc {{
            color: {TEXT_MUTED};
            font-size: 0.85rem;
            line-height: 1.45;
            flex-grow: 1;
        }}

        .section-title {{
            font-weight: 800;
            color: {NAVY} !important;
            font-size: 1.15rem;
            margin: 22px 0 12px 0;
            padding-bottom: 8px;
            border-bottom: 1px solid {BORDER};
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

        /* -----------------------------------------------------------
           Sidebar: brand header + built-in multipage navigation +
           user/logout footer, restyled to look like one cohesive
           product nav rather than default Streamlit chrome.
        ----------------------------------------------------------- */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {NAVY} 0%, {NAVY_DARK} 100%);
            border-right: none;
        }}
        section[data-testid="stSidebar"] * {{
            color: #EAF0FA !important;
        }}
        section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {{
            padding-top: 4px;
        }}

        [data-testid="stSidebarNav"] {{
            padding: 6px 12px 10px 12px !important;
        }}
        [data-testid="stSidebarNav"] ul {{
            padding: 0 !important;
        }}
        [data-testid="stSidebarNav"] li {{
            margin-bottom: 3px;
        }}
        [data-testid="stSidebarNav"] a {{
            border-radius: 9px !important;
            padding: 10px 14px !important;
            font-weight: 500 !important;
            font-size: 0.92rem !important;
            transition: background 0.15s ease;
        }}
        [data-testid="stSidebarNav"] a:hover {{
            background: rgba(255,255,255,0.08) !important;
        }}
        [data-testid="stSidebarNav"] a[aria-current="page"] {{
            background: rgba(255,255,255,0.14) !important;
            font-weight: 700 !important;
            box-shadow: inset 3px 0 0 #6FA8DC;
        }}

        .sidebar-brand {{
            text-align: center;
            padding: 14px 10px 16px 10px;
            border-bottom: 1px solid rgba(255,255,255,0.12);
            margin-bottom: 8px;
        }}
        .sidebar-brand .brand-icon {{ font-size: 1.9rem; }}
        .sidebar-brand .brand-name {{
            font-weight: 800;
            font-size: 0.98rem;
            line-height: 1.3;
            margin-top: 2px;
        }}

        .sidebar-user {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px 6px;
            margin-top: 10px;
            border-top: 1px solid rgba(255,255,255,0.12);
        }}
        .sidebar-user .avatar {{
            width: 34px;
            height: 34px;
            border-radius: 50%;
            background: rgba(255,255,255,0.14);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.85rem;
            flex-shrink: 0;
        }}
        .sidebar-user .who {{ line-height: 1.3; overflow: hidden; }}
        .sidebar-user .who .name {{
            font-weight: 700;
            font-size: 0.85rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .sidebar-user .who .role {{
            font-size: 0.72rem;
            opacity: 0.75;
        }}
        section[data-testid="stSidebar"] div[data-testid="stButton"] button {{
            background: rgba(255,255,255,0.06) !important;
            border: 1px solid rgba(255,255,255,0.18) !important;
            color: #EAF0FA !important;
            font-size: 0.82rem !important;
            padding: 4px 0 !important;
        }}
        section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {{
            background: rgba(255,255,255,0.14) !important;
            border-color: rgba(255,255,255,0.32) !important;
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
            <div class="sidebar-brand">
                <div class="brand-icon">{app_icon}</div>
                <div class="brand-name">{app_name}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        _render_sidebar_user_footer()


def _render_sidebar_user_footer():
    """Signed-in-as strip + working logout button, shown at the bottom of
    every page's sidebar. Kept optional/defensive: if nothing is logged
    in yet (e.g. rendered from the login screen) it simply does nothing."""
    username = st.session_state.get("auth_username")
    role = st.session_state.get("auth_role")
    if not username:
        return

    initials = "".join(part[0] for part in username.split()[:2]).upper() or "U"
    st.markdown(
        f"""
        <div class="sidebar-user">
            <div class="avatar">{initials}</div>
            <div class="who">
                <div class="name">{username}</div>
                <div class="role">{role or ""}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Log out", key="sidebar_logout_btn", use_container_width=True):
        from utils.auth import logout
        logout()
        st.rerun()


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
            <div class="kpi-value">{value}</div>
            <div class="kpi-desc">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
