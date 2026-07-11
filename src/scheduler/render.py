"""
src/scheduler/render.py

Renders the "Connect with Me" tab:
    - A form to pick a date/time for a meeting (plus name, email, notes)
    - On submit: notifies you on Telegram and saves a local record

Meeting records are appended to data/meetings.json so you have a durable
log even if a Telegram send fails.
"""

from __future__ import annotations

import json
from datetime import date, datetime, time, timedelta
from pathlib import Path

import streamlit as st

from src.notifications.telegram_notifier import (
    TelegramConfigError,
    format_meeting_message,
    send_telegram_message,
)

MEETINGS_PATH = Path("data/meetings.json")

DURATION_OPTIONS = ["15 min", "30 min", "45 min", "60 min"]


# ---------------------------------------------------------------------
# Local persistence
# ---------------------------------------------------------------------

def _load_meetings() -> list[dict]:
    if not MEETINGS_PATH.exists():
        return []
    try:
        with open(MEETINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def _save_meeting(record: dict) -> None:
    MEETINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    meetings = _load_meetings()
    meetings.append(record)
    with open(MEETINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(meetings, f, indent=2)


# ---------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------

def _inject_css() -> None:
    st.markdown(
        """
        <style>
        .connect-intro {
            padding: 1.5rem 1.8rem;
            border-radius: 16px;
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            color: #f9fafb;
            margin-bottom: 1.5rem;
        }
        .connect-intro h2 {
            margin-top: 0;
            color: #f9fafb;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------

def render_connect() -> None:
    _inject_css()

    st.markdown(
        """
        <div class="connect-intro">
            <h2>📅 Connect with Me</h2>
            <div>Pick a date and time that works for you, and I'll get notified right away.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("schedule_meeting_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name *")
            meeting_date = st.date_input(
                "Preferred Date *",
                min_value=date.today(),
                value=date.today() + timedelta(days=1),
            )
            duration = st.selectbox("Duration", DURATION_OPTIONS, index=1)
        with col2:
            email = st.text_input("Your Email *")
            meeting_time = st.time_input("Preferred Time *", value=time(10, 0))

        notes = st.text_area(
            "What would you like to discuss? (optional)",
            placeholder="e.g. Job opportunity, collaboration, project feedback...",
        )

        submitted = st.form_submit_button("📨 Request Meeting", use_container_width=True)

    if not submitted:
        return

    # Validation
    if not name.strip() or not email.strip():
        st.error("Please fill in your name and email.")
        return
    if "@" not in email or "." not in email:
        st.error("Please enter a valid email address.")
        return

    date_str = meeting_date.strftime("%A, %B %d, %Y")
    time_str = meeting_time.strftime("%I:%M %p")

    record = {
        "name": name.strip(),
        "email": email.strip(),
        "date": meeting_date.isoformat(),
        "time": meeting_time.strftime("%H:%M"),
        "duration": duration,
        "notes": notes.strip(),
        "requested_at": datetime.now().isoformat(timespec="seconds"),
    }
    _save_meeting(record)

    try:
        message = format_meeting_message(
            name=record["name"],
            email=record["email"],
            date_str=date_str,
            time_str=time_str,
            duration=duration,
            notes=record["notes"],
        )
        send_telegram_message(message)
        st.success(
            f"✅ Meeting request sent! I'll reach out to **{email}** to confirm "
            f"**{date_str} at {time_str}**."
        )
    except TelegramConfigError:
        st.warning(
            "Your request was saved, but Telegram notifications aren't configured yet "
            "(missing bot token / chat id in secrets)."
        )
    except Exception as e:
        st.warning(
            f"Your request was saved, but I couldn't send the Telegram notification "
            f"right now ({e}). I'll still follow up via email."
        )