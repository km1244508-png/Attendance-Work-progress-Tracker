"""
utils/ui.py
-----------
Shared design system: global CSS, KPI cards, hero banners, section
titles, sidebar branding, and status badges. Keep all color/style
constants here so branding can be changed from one place.

Visual language: deep-slate "premium SaaS" dark theme (Deel / Linear /
Stripe style) — slate-900 canvas, slate-800 surfaces, ultra-subtle
borders, soft ambient shadows, Inter type, and a small semantic accent
set (indigo = primary/brand, emerald = active/positive, amber = pending,
rose = negative).
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Palette — deep slate dark theme
# ---------------------------------------------------------------------------
BG = "#0B1220"           # app canvas (near slate-950)
SURFACE = "#141B2D"      # cards, containers (slate-900/800 blend)
SURFACE_2 = "#1B2436"    # slightly raised surface (hover, sidebar footer)
BORDER = "rgba(255,255,255,0.08)"
BORDER_STRONG = "rgba(255,255,255,0.14)"

TEXT_PRIMARY = "#F1F5F9"   # slate-100
TEXT_MUTED = "#94A3B8"     # slate-400
TEXT_FAINT = "#64748B"     # slate-500

PRIMARY = "#6366F1"        # indigo-500 — brand / primary actions
PRIMARY_HOVER = "#7C7FF2"
EMERALD = "#10B981"        # active / positive
AMBER = "#F59E0B"          # pending / warning
ROSE = "#F43F5E"           # negative / absent

# Kept for backward-compat imports elsewhere in the codebase.
NAVY = SURFACE
NAVY_DARK = BG
BLUE = PRIMARY
LIGHT_BG = BG
TEXT_DARK = TEXT_PRIMARY

# A small curated accent palette used to give repeating card grids
# (Quick Navigation, KPI rows, etc.) visual variety without breaking
# the overall dark/indigo brand identity. Chosen to stay legible on a
# dark surface.
ACCENT_PALETTE = ["#6366F1", "#10B981", "#38BDF8", "#F59E0B", "#F472B6", "#2DD4BF"]

STATUS_COLORS = {
    "Present": EMERALD,
    "Late": AMBER,
    "Half-Day": "#FB923C",
    "Absent": ROSE,
    "Not Started": TEXT_FAINT,
    "In Progress": "#38BDF8",
    "Completed": EMERALD,
    "On Hold": AMBER,
}


def inject_global_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, .stApp, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        }}

        html, body, .stApp {{
            color-scheme: dark !important;
        }}

        .stApp {{ background-color: {BG}; }}
        #MainMenu, footer, header[data-testid="stHeader"] {{ visibility: hidden; }}

        .block-container {{
            padding-top: 2.2rem !important;
            padding-bottom: 3rem !important;
            max-width: 1220px;
        }}

        /* Slim, unobtrusive dark scrollbars — small polish detail that
           matches the rest of the premium-dark aesthetic. */
        ::-webkit-scrollbar {{ width: 10px; height: 10px; }}
        ::-webkit-scrollbar-track {{ background: transparent; }}
        ::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 8px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: #475569; }}

        /* ---------------------------------------------------------------
           Equal-height card rows: whenever cards are laid out with
           st.columns(), stretch every column to the tallest one in that
           row so cards with shorter text don't end up visually shorter.
           This is what keeps every "tracking box" the same size.
        --------------------------------------------------------------- */
        div[data-testid="stHorizontalBlock"] {{
            align-items: stretch !important;
            gap: 16px;
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

        /* Base text colors */
        .stApp, .stMarkdown, p, span, label, li {{
            color: {TEXT_PRIMARY} !important;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {TEXT_PRIMARY} !important;
            letter-spacing: -0.01em;
        }}

        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] p,
        .stCaption, .stCaption p {{
            color: {TEXT_MUTED} !important;
            opacity: 1 !important;
        }}

        /* Tabs */
        button[data-baseweb="tab"] {{
            color: {TEXT_MUTED} !important;
        }}
        button[data-baseweb="tab"] p {{
            color: {TEXT_MUTED} !important;
            font-size: 14.5px !important;
            font-weight: 600 !important;
        }}
        button[data-baseweb="tab"][aria-selected="true"] p {{
            color: {TEXT_PRIMARY} !important;
            font-weight: 700 !important;
        }}
        div[data-baseweb="tab-highlight"] {{
            background-color: {PRIMARY} !important;
        }}
        div[data-baseweb="tab-border"] {{
            background-color: {BORDER} !important;
        }}

        /* -----------------------------------------------------------
           Form inputs — dark surface, subtle border, indigo focus ring.
        ----------------------------------------------------------- */
        input, textarea,
        [data-baseweb="input"], [data-baseweb="textarea"],
        [data-baseweb="select"], [data-baseweb="base-input"],
        div[data-testid="stTimeInput"] input,
        div[data-testid="stDateInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea {{
            background-color: {SURFACE_2} !important;
            color: {TEXT_PRIMARY} !important;
            border: 1px solid {BORDER_STRONG} !important;
            border-radius: 10px !important;
        }}
        [data-baseweb="input"] > div,
        [data-baseweb="textarea"] > div,
        [data-baseweb="select"] > div {{
            background-color: {SURFACE_2} !important;
        }}
        input:focus, textarea:focus, [data-baseweb="select"]:focus-within {{
            border-color: {PRIMARY} !important;
            box-shadow: 0 0 0 3px rgba(99,102,241,0.25) !important;
        }}

        div[data-testid="stDateInput"] > div,
        div[data-testid="stDateInput"] div,
        div[data-testid="stDateInput"] [data-baseweb="datepicker"],
        div[data-testid="stDateInput"] [role="spinbutton"] {{
            background-color: {SURFACE_2} !important;
            color: {TEXT_PRIMARY} !important;
        }}
        div[data-testid="stDateInput"] > div {{
            border: 1px solid {BORDER_STRONG} !important;
            border-radius: 10px !important;
        }}

        div[data-testid="stTimeInput"],
        div[data-testid="stTimeInput"] > div,
        div[data-testid="stTimeInput"] div,
        div[data-testid="stTimeInput"] [data-baseweb],
        div[data-testid="stTimeInput"] input {{
            background-color: {SURFACE_2} !important;
            color: {TEXT_PRIMARY} !important;
        }}
        div[data-testid="stTimeInput"] > div {{
            border: 1px solid {BORDER_STRONG} !important;
            border-radius: 10px !important;
        }}

        /* Dropdown/select popover menus */
        ul[data-baseweb="menu"], div[data-baseweb="popover"] {{
            background-color: {SURFACE_2} !important;
        }}
        li[data-baseweb="menu-item"] {{
            color: {TEXT_PRIMARY} !important;
        }}
        li[data-baseweb="menu-item"]:hover {{
            background-color: rgba(99,102,241,0.15) !important;
        }}

        /* -----------------------------------------------------------
           Buttons
        ----------------------------------------------------------- */
        div[data-testid="stButton"] button,
        div[data-testid="stDownloadButton"] button,
        div[data-testid="stFormSubmitButton"] button,
        button[kind="secondary"],
        button[data-testid="stBaseButton-secondary"],
        button[data-testid="stBaseButton-secondaryFormSubmit"] {{
            background-color: {SURFACE_2} !important;
            color: {TEXT_PRIMARY} !important;
            border: 1px solid {BORDER_STRONG} !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            transition: background 0.15s ease, border-color 0.15s ease;
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
            background-color: #232E45 !important;
            border-color: {PRIMARY} !important;
        }}
        div[data-testid="stButton"] button[kind="primary"],
        div[data-testid="stDownloadButton"] button[kind="primary"],
        div[data-testid="stFormSubmitButton"] button[kind="primary"],
        button[kind="primary"],
        button[data-testid="stBaseButton-primary"],
        button[data-testid="stBaseButton-primaryFormSubmit"] {{
            background-color: {PRIMARY} !important;
            border: 1px solid {PRIMARY} !important;
            color: #FFFFFF !important;
            box-shadow: 0 4px 14px rgba(99,102,241,0.35);
        }}
        div[data-testid="stButton"] button[kind="primary"]:hover,
        div[data-testid="stDownloadButton"] button[kind="primary"]:hover,
        div[data-testid="stFormSubmitButton"] button[kind="primary"]:hover,
        button[kind="primary"]:hover,
        button[data-testid="stBaseButton-primary"]:hover,
        button[data-testid="stBaseButton-primaryFormSubmit"]:hover {{
            background-color: {PRIMARY_HOVER} !important;
            border-color: {PRIMARY_HOVER} !important;
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
            background-color: {SURFACE} !important;
            color: {TEXT_FAINT} !important;
            border-color: {BORDER} !important;
            box-shadow: none !important;
        }}

        input::placeholder, textarea::placeholder {{
            color: {TEXT_FAINT} !important;
            opacity: 1 !important;
        }}

        /* -----------------------------------------------------------
           Bordered containers (login card, etc.)
        ----------------------------------------------------------- */
        [data-testid="stForm"] {{
            border: none !important;
            padding: 0 !important;
            background: transparent !important;
        }}
        .login-card,
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: {SURFACE};
            border-radius: 16px !important;
            box-shadow: 0 20px 50px rgba(0,0,0,0.35);
            border: 1px solid {BORDER} !important;
        }}

        /* -----------------------------------------------------------
           Hero banner
        ----------------------------------------------------------- */
        .hero-banner {{
            background: linear-gradient(135deg, #1E2A47 0%, #312E81 100%);
            color: {TEXT_PRIMARY};
            padding: 30px 34px;
            border-radius: 18px;
            margin-bottom: 26px;
            box-shadow: 0 20px 45px rgba(0,0,0,0.35);
            border: 1px solid {BORDER};
            position: relative;
            overflow: hidden;
        }}
        .hero-banner::after {{
            content: "";
            position: absolute;
            top: -60%; right: -8%;
            width: 280px; height: 280px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(99,102,241,0.35) 0%, rgba(99,102,241,0) 70%);
        }}
        .hero-banner h1 {{
            color: {TEXT_PRIMARY} !important;
            font-size: 1.65rem;
            margin: 0 0 6px 0;
            font-weight: 800;
            position: relative;
        }}
        .hero-banner p {{
            color: {TEXT_MUTED} !important;
            margin: 0;
            font-size: 0.98rem;
            position: relative;
        }}
        .hero-banner p b {{ color: {TEXT_PRIMARY} !important; }}

        /* ---------------------------------------------------------------
           Cards (Quick Navigation tiles, KPI stat cards) — uniform grid:
           same border-radius, padding and height across every card, flex
           column so descriptions grow to fill leftover space evenly.
        --------------------------------------------------------------- */
                .kpi-card {{
            background: {SURFACE};
            border-radius: 14px;
            padding: 20px 20px;
            border: 1px solid {BORDER};
            box-shadow: 0 8px 24px rgba(0,0,0,0.22);
            transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
            display: flex;
            flex-direction: column;
            width: 100%;
            height: 100%;
            min-height: 168px;
            box-sizing: border-box;
        }}
        div[data-testid="stHorizontalBlock"] {{
            align-items: stretch;
        }}
        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {{
            display: flex;
        }}
        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] > div {{
            width: 100%;
        }}
        .kpi-card:hover {{
            transform: translateY(-3px);
            border-color: color-mix(in srgb, var(--kpi-color, {PRIMARY}) 45%, {BORDER});
            box-shadow: 0 14px 34px rgba(0,0,0,0.32);
        }}
        .kpi-icon {{
            width: 42px;
            height: 42px;
            border-radius: 11px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            background: color-mix(in srgb, var(--kpi-color, {PRIMARY}) 18%, {SURFACE});
            margin-bottom: 14px;
            flex-shrink: 0;
        }}
        .kpi-title {{
            font-weight: 700;
            color: {TEXT_PRIMARY};
            font-size: 1.02rem;
            margin-bottom: 4px;
        }}
        .kpi-value {{
            font-weight: 700;
            color: {TEXT_PRIMARY};
            font-size: 1.5rem;
            letter-spacing: -0.02em;
        }}
        .kpi-desc {{
            color: {TEXT_MUTED};
            font-size: 0.85rem;
            line-height: 1.5;
            flex-grow: 1;
        }}

        .section-title {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 700;
            color: {TEXT_PRIMARY} !important;
            font-size: 1.05rem;
            margin: 24px 0 14px 0;
            padding-bottom: 10px;
            border-bottom: 1px solid {BORDER};
        }}

        /* Low-opacity status "mini badge" with a small dot indicator,
           instead of a bulky solid-color pill. */
        .status-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 11px 4px 8px;
            border-radius: 999px;
            font-size: 0.74rem;
            font-weight: 600;
            background: color-mix(in srgb, var(--status-color, {TEXT_FAINT}) 16%, transparent);
            border: 1px solid color-mix(in srgb, var(--status-color, {TEXT_FAINT}) 38%, transparent);
            color: var(--status-color, {TEXT_MUTED}) !important;
        }}
        .status-dot {{
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--status-color, {TEXT_FAINT});
            flex-shrink: 0;
        }}

        .muted-text {{
            color: {TEXT_MUTED} !important;
            font-size: 0.85rem;
            line-height: 1.4;
        }}

        /* -----------------------------------------------------------
           Sidebar: brand header + built-in multipage navigation +
           user/logout footer, restyled as one cohesive product nav.
        ----------------------------------------------------------- */
        section[data-testid="stSidebar"] {{
            background: {BG};
            border-right: 1px solid {BORDER};
        }}
        section[data-testid="stSidebar"] * {{
            color: {TEXT_PRIMARY} !important;
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
            margin-bottom: 2px;
        }}
        [data-testid="stSidebarNav"] a {{
            border-radius: 8px !important;
            padding: 10px 14px !important;
            font-weight: 500 !important;
            font-size: 0.92rem !important;
            color: {TEXT_MUTED} !important;
            border-left: 2px solid transparent;
            transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
        }}
        [data-testid="stSidebarNav"] a:hover {{
            background: rgba(255,255,255,0.05) !important;
            color: {TEXT_PRIMARY} !important;
        }}
        [data-testid="stSidebarNav"] a[aria-current="page"] {{
            background: rgba(99,102,241,0.14) !important;
            color: {TEXT_PRIMARY} !important;
            font-weight: 700 !important;
            border-left: 2px solid {PRIMARY};
        }}

        .sidebar-brand {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 14px 12px 16px 12px;
            border-bottom: 1px solid {BORDER};
            margin-bottom: 8px;
        }}
        .sidebar-brand .brand-icon {{
            font-size: 1.5rem;
            width: 38px;
            height: 38px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(99,102,241,0.16);
            flex-shrink: 0;
        }}
        .sidebar-brand .brand-name {{
            font-weight: 800;
            font-size: 0.92rem;
            line-height: 1.3;
            color: {TEXT_PRIMARY};
        }}

        .sidebar-user {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px 6px;
            margin-top: 10px;
            border-top: 1px solid {BORDER};
        }}
        .sidebar-user .avatar {{
            width: 34px;
            height: 34px;
            border-radius: 50%;
            background: linear-gradient(135deg, {PRIMARY} 0%, #38BDF8 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.82rem;
            color: #FFFFFF !important;
            flex-shrink: 0;
        }}
        .sidebar-user .who {{ line-height: 1.3; overflow: hidden; }}
        .sidebar-user .who .name {{
            font-weight: 700;
            font-size: 0.85rem;
            color: {TEXT_PRIMARY};
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .sidebar-user .who .role {{
            font-size: 0.72rem;
            color: {TEXT_MUTED};
        }}
        section[data-testid="stSidebar"] div[data-testid="stButton"] button {{
            background: transparent !important;
            border: 1px solid {BORDER_STRONG} !important;
            color: {TEXT_MUTED} !important;
            font-size: 0.82rem !important;
            padding: 4px 0 !important;
        }}
        section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {{
            background: rgba(244,63,94,0.1) !important;
            border-color: {ROSE} !important;
            color: {TEXT_PRIMARY} !important;
        }}

        /* Streamlit's default dataframe/table also gets a dark pass so it
           doesn't sit as a bright white block inside the dark canvas. */
        [data-testid="stDataFrame"] {{
            border: 1px solid {BORDER} !important;
            border-radius: 10px !important;
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
    color = STATUS_COLORS.get(status, TEXT_FAINT)
    return (
        f'<span class="status-badge" style="--status-color:{color};">'
        f'<span class="status-dot"></span>{status}</span>'
    )


def muted_text(text: str) -> str:
    """HTML-safe muted caption line — use instead of st.caption() wherever
    text has previously appeared to not show up (e.g. inside custom
    st.markdown blocks that also carry unsafe_allow_html=True)."""
    return f'<div class="muted-text">{text}</div>'


def kpi_card(icon: str, label: str, value, color: str = PRIMARY):
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
