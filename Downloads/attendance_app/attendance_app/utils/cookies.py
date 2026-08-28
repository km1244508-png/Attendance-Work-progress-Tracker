"""
utils/cookies.py
-----------------
Persistent, encrypted browser-cookie storage for the login session.
st.session_state alone only survives within a single browser tab's
WebSocket connection — opening a new tab, refreshing, or reopening the
app all create a fresh session and force a re-login. Storing the same
auth info in an encrypted cookie lets every page (and every tab) pick
the session back up automatically.

IMPORTANT: set COOKIE_PASSWORD as a real secret/env var in production
(Streamlit Cloud -> Settings -> Secrets). The fallback below is only
for local development.
"""

import os
import time

import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

cookies = EncryptedCookieManager(
    prefix="attendance_app/",
    password=os.environ.get("COOKIE_PASSWORD", "dev-only-change-this-secret"),
)


def block_until_ready():
    """The cookie component talks to the browser over an async round-trip,
    so it isn't ready on the very first script run of a given page.

    FIX: previously pages called `if not cookies.ready(): st.stop()`,
    which just froze the page on a blank screen — Streamlit doesn't
    automatically re-run just because a component became ready, so the
    page could stay blank until the user manually interacted with it
    (e.g. clicked a sidebar link again). This version shows a spinner
    and actively triggers the rerun itself, so the page always
    resolves within a fraction of a second instead of hanging blank.
    """
    if cookies.ready():
        return
    with st.spinner("Loading your session..."):
        time.sleep(0.15)
    st.rerun()
