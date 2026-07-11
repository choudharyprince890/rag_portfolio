"""
src/notifications/telegram_notifier.py

Sends a Telegram message via the Bot HTTP API whenever a visitor books a
meeting through the "Connect with Me" tab.

Configuration lives in .streamlit/secrets.toml (kept out of git):

    TELEGRAM_BOT_TOKEN = "123456789:AA...your-token..."
    TELEGRAM_CHAT_ID   = "123456789"

TELEGRAM_CHAT_ID is *your* personal chat id (i.e. where the bot should send
notifications), not the bot's own id. See the README section on how to find
it — in short: message your bot once, then hit
https://api.telegram.org/bot<TOKEN>/getUpdates and read the "chat":{"id": ...}
field back out.
"""

from __future__ import annotations

import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env into os.environ, if present

TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"


class TelegramConfigError(Exception):
    """Raised when the bot token or chat id is missing/misconfigured."""


def _get_config() -> tuple[str, str]:
    # Prefer .env / real environment variables; fall back to Streamlit secrets
    # (guarded, since st.secrets can error if no secrets.toml exists at all).
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")

    if not token or not chat_id:
        try:
            token = token or st.secrets.get("TELEGRAM_BOT_TOKEN", "")
            chat_id = chat_id or st.secrets.get("TELEGRAM_CHAT_ID", "")
        except Exception:
            pass

    if not token or not chat_id:
        raise TelegramConfigError(
            "Telegram is not configured. Add TELEGRAM_BOT_TOKEN and "
            "TELEGRAM_CHAT_ID to your .env file (or .streamlit/secrets.toml)."
        )
    return token, chat_id


def send_telegram_message(text: str) -> None:
    """
    Send a plain-text message to the configured chat id.

    Raises:
        TelegramConfigError: if secrets are missing.
        requests.RequestException: on network failure.
        RuntimeError: if Telegram returns a non-ok response.
    """
    token, chat_id = _get_config()

    response = requests.post(
        TELEGRAM_API_URL.format(token=token),
        data={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
        },
        timeout=10,
    )

    payload = response.json()
    if not payload.get("ok"):
        raise RuntimeError(f"Telegram API error: {payload}")


def format_meeting_message(
    name: str,
    email: str,
    date_str: str,
    time_str: str,
    duration: str,
    notes: str,
) -> str:
    lines = [
        "📅 *New Meeting Request*",
        f"*Name:* {name}",
        f"*Email:* {email}",
        f"*Date:* {date_str}",
        f"*Time:* {time_str}",
        f"*Duration:* {duration}",
    ]
    if notes:
        lines.append(f"*Notes:* {notes}")
    return "\n".join(lines)