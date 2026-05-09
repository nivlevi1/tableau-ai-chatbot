import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
import query
import db

st.set_page_config(page_title="Tableau Assistant", page_icon="📊", layout="wide")
db.init_db()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _render_source(src: dict):
    label = src["title"] or src["source_file"]
    badge = f"`{src['source_type'].upper()}`" if src["source_type"] else ""
    if src["url"]:
        st.markdown(f"{badge} [{label}]({src['url']})")
    else:
        section = f" — {src['section']}" if src["section"] else ""
        st.markdown(f"{badge} **{label}**{section}")


def _render_messages(messages: list[dict]):
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg.get("sources"):
                with st.expander(f"Sources ({len(msg['sources'])})"):
                    for src in msg["sources"]:
                        _render_source(src)


# ── Session state defaults ────────────────────────────────────────────────────

if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []


def _load_session(session_id: int):
    st.session_state.session_id = session_id
    st.session_state.messages   = db.get_messages(session_id)


def _new_session():
    st.session_state.session_id = None
    st.session_state.messages   = []


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("💬 Conversations")
    if st.button("＋ New Chat", use_container_width=True):
        _new_session()
        st.rerun()

    st.divider()

    sessions = db.get_sessions()
    if not sessions:
        st.caption("No past conversations yet.")

    for s in sessions:
        col1, col2 = st.columns([5, 1])
        is_active  = s["id"] == st.session_state.session_id
        date       = s["created_at"][:10]
        with col1:
            if st.button(
                f"{'▶ ' if is_active else ''}{s['title']}",
                key=f"sess_{s['id']}",
                use_container_width=True,
                help=date,
            ):
                _load_session(s["id"])
                st.rerun()
        with col2:
            if st.button("🗑", key=f"del_{s['id']}", help="Delete"):
                db.delete_session(s["id"])
                if st.session_state.session_id == s["id"]:
                    _new_session()
                st.rerun()


# ── Main chat area ────────────────────────────────────────────────────────────

st.title("📊 Tableau Assistant")
if not st.session_state.session_id:
    st.caption("Ask anything about Tableau — answers sourced from official docs, books, blogs, and community Q&A.")

_render_messages(st.session_state.messages)


# ── Input ─────────────────────────────────────────────────────────────────────

if prompt := st.chat_input("Ask a Tableau question..."):
    # Create a new session on first message
    if st.session_state.session_id is None:
        sid = db.create_session(prompt)
        st.session_state.session_id = sid
    else:
        sid = st.session_state.session_id

    # Slice history BEFORE appending current message
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[-6:]
    ]

    db.save_message(sid, "user", prompt, [])
    st.session_state.messages.append({"role": "user", "content": prompt, "sources": []})

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer, sources = query.ask(prompt, history)
        st.write(answer)
        if sources:
            with st.expander(f"Sources ({len(sources)})"):
                for src in sources:
                    _render_source(src)

    db.save_message(sid, "assistant", answer, sources)
    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})

    # Auto-title session from first question
    if len(st.session_state.messages) == 2:
        db.rename_session(sid, prompt)

    st.rerun()
