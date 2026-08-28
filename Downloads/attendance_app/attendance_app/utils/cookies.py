"""
utils/cookies.py
-----------------
Persistent browser-cookie storage for the login session, using
extra-streamlit-components' CookieManager.

NOTE: this project previously used streamlit-cookies-manager, but that
package internally calls the long-removed `st.cache` API and crashes
with an AttributeError on current Streamlit versions. This library
is actively maintained and works with modern Streamlit.

All auth fields are packed into ONE JSON cookie ("attendance_auth")
instead of five separate cookies — setting multiple cookies within a
single script run is unreliable with this component (reruns can
race), so a single combined cookie avoids that entirely.
"""

import json
import time

import streamlit as st
import extra_streamlit_components as stx

COOKIE_NAME = "attendance_auth"


def get_manager() -> stx.CookieManager:
    """One CookieManager per browser session — reused via
    session_state so the underlying component isn't re-embedded on
    every rerun."""
    if "_cookie_manager" not in st.session_state:
        st.session_state["_cookie_manager"] = stx.CookieManager(key="attendance_app_cookie_manager")
    return st.session_state["_cookie_manager"]


def cookies_ready() -> bool:
    """The component talks to the browser asynchronously, so on the
    very first script run of a session it hasn't returned data yet."""
    return get_manager().get_all(key="attendance_app_cookies_ready_check") is not None


def block_until_ready():
    """Show a brief spinner and force a rerun until the cookie
    component has responded, instead of leaving the page blank."""
    if cookies_ready():
        return
    with st.spinner("Loading your session..."):
        time.sleep(0.2)
    st.rerun()


def read_auth_cookie():
    raw = get_manager().get(cookie=COOKIE_NAME)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except (ValueError, TypeError):
        return None


def write_auth_cookie(data: dict):
    get_manager().set(COOKIE_NAME, json.dumps(data), key="set_attendance_auth")


def clear_auth_cookie():
    manager = get_manager()
    if manager.get(cookie=COOKIE_NAME):
        manager.delete(COOKIE_NAME, key="delete_attendance_auth")
