"""
src/chat/render.py

Renders the "Chat" tab:
    - A welcome card + suggested-question chips when there's no history yet
    - Styled chat bubbles with avatars once a conversation is underway
    - The chat input box and response generation

Keeps app.py thin — all chat-specific UI logic lives here.
"""

from __future__ import annotations

import streamlit as st

from src.pipeline import ask
from src.dashboard.render import load_profile

USER_AVATAR = "🧑"


def _inject_css() -> None:
    st.markdown(
        """
        <style>
        .chat-welcome {
            padding: 2rem 2rem 1.6rem 2rem;
            border-radius: 16px;
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            color: #f9fafb;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .chat-welcome .avatar {
            font-size: 2.8rem;
            margin-bottom: 0.4rem;
        }
        .chat-welcome h2 {
            margin: 0.2rem 0 0.3rem 0;
            color: #f9fafb;
        }
        .chat-welcome p {
            color: #d1d5db;
            font-size: 0.98rem;
            margin: 0;
        }
        .suggestion-label {
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.03em;
            opacity: 0.6;
            margin: 0.4rem 0 0.6rem 0;
        }
        div[data-testid="stChatMessage"] {
            border-radius: 14px;
            padding: 0.3rem 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _get_assistant_avatar(profile: dict) -> str:
    return profile.get("avatar", "🤖")


def _render_welcome(profile: dict) -> str | None:
    """Renders the empty-state welcome card + suggestion chips.

    Returns a prompt string if the user clicked a suggestion, else None.
    """
    name = profile.get("name", "me")
    avatar = _get_assistant_avatar(profile)

    st.markdown(
        f"""
        <div class="chat-welcome">
            <div class="avatar">{avatar}</div>
            <h2>Ask me anything about {name}</h2>
            <p>I can talk through experience, skills, projects, and how this app itself was built.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    questions = profile.get("suggested_questions", [])
    if not questions:
        return None

    st.markdown('<div class="suggestion-label">Try asking</div>', unsafe_allow_html=True)

    clicked_prompt = None
    cols = st.columns(min(len(questions), 4) or 1)
    for i, question in enumerate(questions):
        col = cols[i % len(cols)]
        with col:
            if st.button(question, key=f"suggested_{i}", use_container_width=True):
                clicked_prompt = question

    return clicked_prompt


def _handle_prompt(prompt: str, assistant_avatar: str) -> None:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=assistant_avatar):
        with st.spinner("Thinking..."):
            try:
                response = ask(prompt)
            except Exception as e:
                response = f"❌ Error: {e}"
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})


def render_chat() -> None:
    _inject_css()

    try:
        profile = load_profile()
    except FileNotFoundError:
        profile = {}

    assistant_avatar = _get_assistant_avatar(profile)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Empty state: welcome card + suggestions instead of a blank page
    if not st.session_state.messages:
        clicked_prompt = _render_welcome(profile)
        if clicked_prompt:
            _handle_prompt(clicked_prompt, assistant_avatar)
            st.rerun()
    else:
        for message in st.session_state.messages:
            avatar = USER_AVATAR if message["role"] == "user" else assistant_avatar
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything..."):
        _handle_prompt(prompt, assistant_avatar)
        st.rerun()