"""
src/dashboard/render.py

Renders the "Dashboard" tab of the AI Portfolio Assistant:
    - Professional profile header
    - Skills
    - Experience timeline
    - Featured projects
    - Resume download
    - Contact information

All content is data-driven from data/profile.json so you can update your
info without touching this file.
"""

from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

PROFILE_PATH = Path("data/profile.json")


# ---------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------

@st.cache_data(show_spinner=False)
def load_profile() -> dict:
    if not PROFILE_PATH.exists():
        raise FileNotFoundError(
            f"Profile config not found at {PROFILE_PATH}. "
            "Create it (see data/profile.json in the project)."
        )
    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------
# Styles (scoped to dashboard elements via CSS classes)
# ---------------------------------------------------------------------

def _inject_dashboard_css() -> None:
    st.markdown(
        """
        <style>
        .profile-card {
            padding: 1.75rem 2rem;
            border-radius: 16px;
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            color: #f9fafb;
            margin-bottom: 1.5rem;
        }
        .profile-card h1 {
            margin-bottom: 0.1rem;
            color: #f9fafb;
        }
        .profile-title {
            font-size: 1.1rem;
            color: #93c5fd;
            font-weight: 500;
            margin-bottom: 0.6rem;
        }
        .profile-bio {
            color: #d1d5db;
            font-size: 0.98rem;
            line-height: 1.5;
        }
        .section-header {
            font-size: 1.3rem;
            font-weight: 700;
            margin-top: 1.8rem;
            margin-bottom: 0.8rem;
            border-bottom: 2px solid rgba(147, 197, 253, 0.4);
            padding-bottom: 0.3rem;
        }
        .skill-badge {
            display: inline-block;
            background: rgba(147, 197, 253, 0.15);
            color: #2563eb;
            border: 1px solid rgba(37, 99, 235, 0.3);
            padding: 0.25rem 0.7rem;
            margin: 0.2rem 0.3rem 0.2rem 0;
            border-radius: 999px;
            font-size: 0.85rem;
            font-weight: 500;
        }
        .skill-category {
            font-weight: 600;
            font-size: 0.95rem;
            margin-top: 0.6rem;
            margin-bottom: 0.3rem;
            color: inherit;
        }
        .timeline-item {
            border-left: 3px solid #2563eb;
            padding-left: 1rem;
            margin-bottom: 1.3rem;
            position: relative;
        }
        .timeline-item::before {
            content: "";
            position: absolute;
            left: -8px;
            top: 4px;
            width: 13px;
            height: 13px;
            border-radius: 50%;
            background: #2563eb;
        }
        .timeline-role {
            font-weight: 700;
            font-size: 1.05rem;
        }
        .timeline-meta {
            font-size: 0.85rem;
            opacity: 0.7;
            margin-bottom: 0.4rem;
        }
        .project-card {
            border: 1px solid rgba(128,128,128,0.25);
            border-radius: 12px;
            padding: 1rem 1.2rem;
            margin-bottom: 1rem;
            height: 100%;
        }
        .project-card h4 {
            margin-bottom: 0.3rem;
        }
        .contact-link {
            display: inline-block;
            margin-right: 1rem;
            margin-bottom: 0.4rem;
            text-decoration: none;
            font-weight: 500;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------
# Section renderers
# ---------------------------------------------------------------------

def _render_header(profile: dict) -> None:
    st.markdown(
        f"""
        <div class="profile-card">
            <div style="font-size:2.6rem;">{profile.get('avatar', '🧑‍💻')}</div>
            <h1>{profile.get('name', '')}</h1>
            <div class="profile-title">{profile.get('title', '')} · {profile.get('location', '')}</div>
            <div class="profile-bio">{profile.get('tagline', '')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write(profile.get("bio", ""))


def _render_skills(profile: dict) -> None:
    st.markdown('<div class="section-header">🛠️ Skills</div>', unsafe_allow_html=True)
    skills = profile.get("skills", [])
    if not skills:
        st.caption("No skills listed yet.")
        return

    cols = st.columns(len(skills)) if len(skills) <= 4 else st.columns(4)
    for i, group in enumerate(skills):
        col = cols[i % len(cols)]
        with col:
            st.markdown(
                f'<div class="skill-category">{group.get("category", "")}</div>',
                unsafe_allow_html=True,
            )
            badges = "".join(
                f'<span class="skill-badge">{item}</span>' for item in group.get("items", [])
            )
            st.markdown(badges, unsafe_allow_html=True)


def _render_experience(profile: dict) -> None:
    st.markdown('<div class="section-header">💼 Experience</div>', unsafe_allow_html=True)
    experience = profile.get("experience", [])
    if not experience:
        st.caption("No experience listed yet.")
        return

    for job in experience:
        highlights_html = "".join(f"<li>{h}</li>" for h in job.get("highlights", []))
        st.markdown(
            f"""
            <div class="timeline-item">
                <div class="timeline-role">{job.get('role', '')} · {job.get('company', '')}</div>
                <div class="timeline-meta">{job.get('duration', '')}</div>
                <div>{job.get('description', '')}</div>
                <ul>{highlights_html}</ul>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_projects(profile: dict) -> None:
    st.markdown('<div class="section-header">🚀 Featured Projects</div>', unsafe_allow_html=True)
    projects = [p for p in profile.get("projects", []) if p.get("featured")]
    if not projects:
        projects = profile.get("projects", [])
    if not projects:
        st.caption("No projects listed yet.")
        return

    cols = st.columns(min(len(projects), 3)) if projects else []
    for i, project in enumerate(projects):
        col = cols[i % len(cols)]
        with col:
            tech_badges = "".join(
                f'<span class="skill-badge">{t}</span>' for t in project.get("tech", [])
            )
            link = project.get("link") or ""
            link_html = f'<a href="{link}" target="_blank">🔗 View project</a>' if link else ""
            st.markdown(
                f"""
                <div class="project-card">
                    <h4>{project.get('name', '')}</h4>
                    <p style="font-size:0.9rem;">{project.get('description', '')}</p>
                    <div>{tech_badges}</div>
                    <div style="margin-top:0.5rem;">{link_html}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_resume(profile: dict) -> None:
    st.markdown('<div class="section-header">📄 Resume</div>', unsafe_allow_html=True)
    resume_path = Path(profile.get("resume_path", ""))
    if resume_path.exists():
        with open(resume_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Resume (PDF)",
                data=f,
                file_name=resume_path.name,
                mime="application/pdf",
                use_container_width=False,
            )
    else:
        st.caption(f"Resume file not found at `{resume_path}`. Update `resume_path` in profile.json.")


def _render_contact(profile: dict) -> None:
    st.markdown('<div class="section-header">📬 Contact</div>', unsafe_allow_html=True)
    contact = profile.get("contact", {})
    links = []
    if contact.get("email"):
        links.append(f'<a class="contact-link" href="mailto:{contact["email"]}">✉️ Email</a>')
    if contact.get("phone"):
        links.append(f'<span class="contact-link">📞 {contact["phone"]}</span>')
    if contact.get("linkedin"):
        links.append(f'<a class="contact-link" href="{contact["linkedin"]}" target="_blank">💼 LinkedIn</a>')
    if contact.get("github"):
        links.append(f'<a class="contact-link" href="{contact["github"]}" target="_blank">🐙 GitHub</a>')
    if contact.get("leetcode"):
        links.append(f'<a class="contact-link" href="{contact["leetcode"]}" target="_blank">🧩 LeetCode</a>')
    if contact.get("website"):
        links.append(f'<a class="contact-link" href="{contact["website"]}" target="_blank">🌐 Website</a>')
    if contact.get("twitter"):
        links.append(f'<a class="contact-link" href="{contact["twitter"]}" target="_blank">🐦 Twitter/X</a>')

    st.markdown("".join(links) if links else "No contact info provided.", unsafe_allow_html=True)


# ---------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------

def render_dashboard() -> None:
    """Render the full dashboard tab. Call this from app.py."""
    try:
        profile = load_profile()
    except FileNotFoundError as e:
        st.error(str(e))
        return

    _inject_dashboard_css()
    _render_header(profile)

    col1, col2 = st.columns([2, 1])
    with col1:
        _render_experience(profile)
    with col2:
        _render_skills(profile)
        _render_resume(profile)
        _render_contact(profile)

    _render_projects(profile)