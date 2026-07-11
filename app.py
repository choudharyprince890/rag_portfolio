

# """
# Streamlit application for the AI Portfolio Assistant.

# Responsibilities:
# - Dashboard (profile, skills, experience, projects, resume, contact)
# - Chat interface
# - User input
# - Display conversation

# This file does NOT:
# - Create embeddings
# - Build the vector database
# - Perform ingestion

# Run:
#     streamlit run app.py
# """

# import streamlit as st

# from src.pipeline import ask
# from src.memory import conversation_memory
# from src.dashboard.render import render_dashboard, load_profile

# # ---------------------------------------------------------------------
# # Page Configuration
# # ---------------------------------------------------------------------

# st.set_page_config(
#     page_title="AI Portfolio Assistant",
#     page_icon="🤖",
#     layout="wide",
# )

# # ---------------------------------------------------------------------
# # Global styling
# # ---------------------------------------------------------------------

# st.markdown(
#     """
#     <style>
#     .block-container {
#         padding-top: 2rem;
#         padding-bottom: 2rem;
#     }
#     div[data-testid="stChatMessage"] {
#         border-radius: 12px;
#     }

#     /* Bigger nav buttons (Dashboard / Chat) */
#     .st-key-nav_dashboard button, .st-key-nav_chat button {
#         height: 3.2rem;
#         border-radius: 10px;
#     }
#     .st-key-nav_dashboard button p, .st-key-nav_chat button p {
#         font-size: 1.35rem !important;
#         font-weight: 600;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # ---------------------------------------------------------------------
# # Active view (session state) — drives both the nav bar and the sidebar
# # ---------------------------------------------------------------------

# if "active_view" not in st.session_state:
#     st.session_state.active_view = "dashboard"

# # ---------------------------------------------------------------------
# # Header
# # ---------------------------------------------------------------------

# try:
#     _profile_name = load_profile().get("name", "my portfolio")
# except FileNotFoundError:
#     _profile_name = "my portfolio"

# st.title("🤖 AI Portfolio Assistant")
# st.caption(f"Explore {_profile_name}'s experience, projects, and skills — or ask the assistant directly.")

# # ---------------------------------------------------------------------
# # Nav bar: Dashboard / Chat
# # ---------------------------------------------------------------------

# nav_col1, nav_col2, _spacer = st.columns([1, 1, 4])

# with nav_col1:
#     with st.container(key="nav_dashboard"):
#         dashboard_type = "primary" if st.session_state.active_view == "dashboard" else "secondary"
#         if st.button("📊 Dashboard", use_container_width=True, type=dashboard_type):
#             st.session_state.active_view = "dashboard"
#             st.rerun()

# with nav_col2:
#     with st.container(key="nav_chat"):
#         chat_type = "primary" if st.session_state.active_view == "chat" else "secondary"
#         if st.button("💬 Chat", use_container_width=True, type=chat_type):
#             st.session_state.active_view = "chat"
#             st.rerun()

# st.divider()

# # ---------------------------------------------------------------------
# # Sidebar — only shown while on the Chat view
# # ---------------------------------------------------------------------

# if st.session_state.active_view == "chat":
#     with st.sidebar:
#         st.header("⚙️ Settings")

#         if st.button("🗑️ Clear Chat", use_container_width=True):
#             st.session_state.messages = []
#             conversation_memory.clear()
#             st.rerun()

#         st.divider()
#         st.caption("Built with a custom RAG pipeline: retrieval + reranking + guardrails.")

# # ---------------------------------------------------------------------
# # Views
# # ---------------------------------------------------------------------

# if st.session_state.active_view == "dashboard":
#     render_dashboard()

# else:  # chat view
#     # -----------------------------------------------------------------
#     # Session State
#     # -----------------------------------------------------------------
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # -----------------------------------------------------------------
#     # Display Chat History
#     # -----------------------------------------------------------------
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     # -----------------------------------------------------------------
#     # Chat Input
#     # -----------------------------------------------------------------
#     if prompt := st.chat_input("Ask me anything..."):

#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(prompt)

#         with st.chat_message("assistant"):
#             with st.spinner("Thinking..."):
#                 try:
#                     response = ask(prompt)
#                 except Exception as e:
#                     response = f"❌ Error: {e}"

#             st.markdown(response)

#         st.session_state.messages.append({"role": "assistant", "content": response})




"""
Streamlit application for the AI Portfolio Assistant.

Responsibilities:
- Dashboard (profile, skills, experience, projects, resume, contact)
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

from src.memory import conversation_memory
from src.dashboard.render import render_dashboard, load_profile
from src.scheduler.render import render_connect
from src.chat.render import render_chat

# ---------------------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------------------

st.set_page_config(
    page_title="AI Portfolio Assistant",
    page_icon="🤖",
    layout="wide",
)

# ---------------------------------------------------------------------
# Global styling
# ---------------------------------------------------------------------

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stChatMessage"] {
        border-radius: 12px;
    }

    /* Bigger nav buttons (Dashboard / Chat / Connect) */
    .st-key-nav_dashboard button, .st-key-nav_chat button, .st-key-nav_connect button {
        height: 3.2rem;
        border-radius: 10px;
    }
    .st-key-nav_dashboard button p, .st-key-nav_chat button p, .st-key-nav_connect button p {
        font-size: 1.35rem !important;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------
# Active view (session state) — drives both the nav bar and the sidebar
# ---------------------------------------------------------------------

if "active_view" not in st.session_state:
    st.session_state.active_view = "dashboard"

# ---------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------

try:
    _profile_name = load_profile().get("name", "my portfolio")
except FileNotFoundError:
    _profile_name = "my portfolio"

st.title("🤖 AI Portfolio Assistant")
st.caption(f"Explore {_profile_name}'s experience, projects, and skills — or ask the assistant directly.")

# ---------------------------------------------------------------------
# Nav bar: Dashboard / Chat / Connect
# ---------------------------------------------------------------------

nav_col1, nav_col2, nav_col3, _spacer = st.columns([1, 1, 1, 3])

with nav_col1:
    with st.container(key="nav_dashboard"):
        dashboard_type = "primary" if st.session_state.active_view == "dashboard" else "secondary"
        if st.button("📊 Dashboard", use_container_width=True, type=dashboard_type):
            st.session_state.active_view = "dashboard"
            st.rerun()

with nav_col2:
    with st.container(key="nav_chat"):
        chat_type = "primary" if st.session_state.active_view == "chat" else "secondary"
        if st.button("💬 Chat", use_container_width=True, type=chat_type):
            st.session_state.active_view = "chat"
            st.rerun()

with nav_col3:
    with st.container(key="nav_connect"):
        connect_type = "primary" if st.session_state.active_view == "connect" else "secondary"
        if st.button("📅 Connect", use_container_width=True, type=connect_type):
            st.session_state.active_view = "connect"
            st.rerun()

st.divider()

# ---------------------------------------------------------------------
# Sidebar — only shown while on the Chat view
# ---------------------------------------------------------------------

if st.session_state.active_view == "chat":
    with st.sidebar:
        st.header("⚙️ Settings")

        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            conversation_memory.clear()
            st.rerun()

        st.divider()
        st.caption("Built with a custom RAG pipeline: retrieval + reranking + guardrails.")

# ---------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------

if st.session_state.active_view == "dashboard":
    render_dashboard()

elif st.session_state.active_view == "connect":
    render_connect()

else:  # chat view
    render_chat()