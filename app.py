

"""
Streamlit application for the AI Portfolio Assistant.

Responsibilities:
- Chat interface
- User input
- Display conversation

This file does NOT:
- Create embeddings
- Build the vector database
- Perform ingestion

Run:
    streamlit run app.py
"""

import streamlit as st

from src.pipeline import ask
from src.memory import conversation_memory

# ---------------------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------------------

st.set_page_config(
    page_title="AI Portfolio Assistant",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI Portfolio Assistant")

with st.sidebar:

    st.header("⚙️ Settings")

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.divider()
        # Clear Streamlit chat history
        st.session_state.messages = []

        # Clear Conversation Memory
        conversation_memory.clear()

        # Refresh the app
        st.rerun()




st.caption("Ask me anything about Prince Choudhary's experience, projects, skills, and career.")


# ---------------------------------------------------------------------
# Session State
# ---------------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------------------------
# Display Chat History
# ---------------------------------------------------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------------------------------------------------------------
# Chat Input
# ---------------------------------------------------------------------

if prompt := st.chat_input("Ask me anything..."):

    # Store and display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):
            try:
                response = ask(prompt)
            except Exception as e:
                response = f"❌ Error: {e}"

        st.markdown(response)

    # Store assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )


