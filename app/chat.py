import streamlit as st
import sys
import os
from datetime import datetime, timedelta, date

sys.path.insert(0, os.path.dirname(__file__))
import query
import db

st.set_page_config(
    page_title="Tableau Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
db.init_db()

# ── Design System ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    -webkit-font-smoothing: antialiased !important;
    height: 100% !important;
}

.stApp { height: 100vh !important; overflow: hidden !important; }

[data-testid="stAppViewContainer"] {
    display: flex !important;
    flex-direction: row !important;
    height: 100vh !important;
    overflow: hidden !important;
}

[data-testid="stMain"] {
    flex: 1 !important;
    display: flex !important;
    flex-direction: column !important;
    height: 100vh !important;
    overflow: hidden !important;
}

[data-testid="stMain"] .main {
    flex: 1 !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    height: 0 !important;
    padding-bottom: 1rem !important;
}

[data-testid="stSidebar"] {
    height: 100vh !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
}

[data-testid="stHeader"] { background: transparent !important; border: none !important; }
footer, #MainMenu { display: none !important; }

[data-testid="stToolbar"] > * { visibility: hidden !important; }
[data-testid="stToolbar"] { background: transparent !important; }
[data-testid="collapsedControl"] {
    visibility: visible !important;
    display: flex !important;
    position: fixed !important;
    top: 0.75rem !important;
    left: 0.75rem !important;
    z-index: 99999 !important;
}

.block-container {
    max-width: 760px !important;
    padding: 2rem 1.75rem 8rem !important;
    margin: 0 auto !important;
}

/* ── Sidebar ──────────────────────────────────── */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child,
[data-testid="stSidebar"] section,
[data-testid="stSidebar"] .block-container {
    background: #0D1117 !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 1.25rem 0.875rem 2rem !important;
}
[data-testid="stSidebar"] hr {
    border: none !important;
    border-top: 1px solid #21262D !important;
    margin: 0.75rem 0 !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] small { color: #8B949E !important; }

[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    color: #C9D1D9 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.8125rem !important;
    text-align: left !important;
    padding: 0.4rem 0.625rem !important;
    transition: all .15s ease !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #161B22 !important;
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] .st-key-new_chat_btn button {
    background: linear-gradient(135deg, #1D4ED8, #2563EB, #3B82F6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    letter-spacing: 0.015em !important;
    padding: 0.625rem 1rem !important;
    text-align: center !important;
    box-shadow: 0 2px 12px rgba(37,99,235,.4) !important;
    transition: all .2s cubic-bezier(.4,0,.2,1) !important;
}
[data-testid="stSidebar"] .st-key-new_chat_btn button:hover {
    background: linear-gradient(135deg, #1E3A8A, #1D4ED8, #2563EB) !important;
    color: #fff !important;
    box-shadow: 0 4px 20px rgba(37,99,235,.55) !important;
    transform: translateY(-1px) !important;
}

[data-testid="stSidebar"] [class*="st-key-del_"] button {
    color: #484F58 !important;
    font-size: .8rem !important;
    padding: .4rem .375rem !important;
    text-align: center !important;
}
[data-testid="stSidebar"] [class*="st-key-del_"] button:hover {
    background: rgba(248,81,73,.12) !important;
    color: #F85149 !important;
}

/* ── Chat messages ────────────────────────────── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: .2rem 0 !important;
    gap: .75rem !important;
    align-items: flex-start !important;
}

[data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(135deg, #1a1f2e, #252d3d) !important;
    border: 1.5px solid rgba(255,255,255,.08) !important;
    border-radius: 10px !important;
    width: 34px !important; min-width: 34px !important; height: 34px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,.2) !important;
}
[data-testid="chatAvatarIcon-assistant"] svg,
[data-testid="chatAvatarIcon-assistant"] p { color: #3B82F6 !important; fill: #3B82F6 !important; }

[data-testid="chatAvatarIcon-user"] {
    background: linear-gradient(135deg, #2563EB, #7C3AED) !important;
    border: none !important;
    border-radius: 10px !important;
    width: 34px !important; min-width: 34px !important; height: 34px !important;
    box-shadow: 0 2px 10px rgba(37,99,235,.4) !important;
}
[data-testid="chatAvatarIcon-user"] svg,
[data-testid="chatAvatarIcon-user"] p { color: #fff !important; fill: #fff !important; }

[data-testid="stChatMessageContent"] {
    border-radius: 4px 16px 16px 16px !important;
    padding: .875rem 1.0625rem !important;
    font-size: .9375rem !important;
    line-height: 1.7 !important;
    font-family: 'Inter', sans-serif !important;
    max-width: 84% !important;
    box-shadow: 0 1px 6px rgba(0,0,0,.07) !important;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stChatMessageContent"] {
    background: var(--secondary-background-color) !important;
    border: 1px solid rgba(0,0,0,.07) !important;
    color: var(--text-color) !important;
    border-radius: 4px 16px 16px 16px !important;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    flex-direction: row-reverse !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageContent"] {
    background: linear-gradient(135deg, #1D4ED8, #2563EB 60%, #3B82F6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 16px 4px 16px 16px !important;
    box-shadow: 0 2px 14px rgba(37,99,235,.35) !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageContent"] * {
    color: #fff !important;
}

[data-testid="stChatMessageContent"] pre {
    background: #0D1117 !important;
    border: 1px solid rgba(255,255,255,.08) !important;
    border-radius: 10px !important;
    padding: .875rem 1rem !important;
    margin: .625rem 0 !important;
    overflow-x: auto !important;
}
[data-testid="stChatMessageContent"] pre code {
    font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace !important;
    font-size: .8125rem !important;
    background: transparent !important;
    color: #E2E8F0 !important;
    padding: 0 !important;
}
[data-testid="stChatMessageContent"] p code,
[data-testid="stChatMessageContent"] li code {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: .875em !important;
    background: rgba(99,102,241,.1) !important;
    color: #6366F1 !important;
    padding: .1rem .35rem !important;
    border-radius: 4px !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) p code {
    background: rgba(255,255,255,.2) !important;
    color: #fff !important;
}

/* ── Input area ───────────────────────────────── */
[data-testid="stBottom"] {
    background: linear-gradient(to top, var(--background-color) 65%, transparent) !important;
    padding-bottom: 1.25rem !important;
    padding-top: 1.5rem !important;
}
[data-testid="stChatInput"] {
    border-radius: 14px !important;
    border: 1.5px solid rgba(0,0,0,.1) !important;
    background: var(--background-color) !important;
    box-shadow: 0 4px 28px rgba(0,0,0,.09), 0 1px 4px rgba(0,0,0,.05) !important;
    overflow: hidden !important;
    transition: border-color .2s, box-shadow .2s !important;
    max-width: 760px !important;
    margin: 0 auto !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #2563EB !important;
    box-shadow: 0 4px 28px rgba(37,99,235,.12), 0 0 0 3px rgba(37,99,235,.08) !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'Inter', sans-serif !important;
    font-size: .9375rem !important;
    line-height: 1.5 !important;
    padding: .875rem 1rem !important;
    background: transparent !important;
    border: none !important;
    color: var(--text-color) !important;
    resize: none !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #94A3B8 !important; }
[data-testid="stChatInput"] button {
    background: #2563EB !important;
    border-radius: 10px !important;
    border: none !important;
    color: #fff !important;
    width: 36px !important; height: 36px !important;
    padding: .375rem !important;
    margin: .375rem !important;
    transition: all .2s cubic-bezier(.4,0,.2,1) !important;
    flex-shrink: 0 !important;
}
[data-testid="stChatInput"] button:hover {
    background: #1D4ED8 !important;
    transform: scale(1.06) !important;
    box-shadow: 0 2px 10px rgba(37,99,235,.45) !important;
}

/* ── Sources expander ─────────────────────────── */
[data-testid="stExpander"] {
    border: 1px solid rgba(0,0,0,.07) !important;
    border-radius: 12px !important;
    background: var(--secondary-background-color) !important;
    overflow: hidden !important;
    margin-top: .625rem !important;
    box-shadow: none !important;
}
[data-testid="stExpander"] > details > summary {
    font-family: 'Inter', sans-serif !important;
    font-size: .8125rem !important;
    font-weight: 500 !important;
    color: #64748B !important;
    padding: .625rem .875rem !important;
    transition: color .15s !important;
}
[data-testid="stExpander"] > details > summary:hover { color: #2563EB !important; }
[data-testid="stExpander"] > details[open] > summary {
    border-bottom: 1px solid rgba(0,0,0,.06) !important;
}
[data-testid="stExpander"] .stExpanderDetails { padding: .5rem !important; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,0,0,.12); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0,0,0,.22); }

/* ── Quick-action chips ───────────────────────── */
.chip-btn .stButton > button {
    background: var(--secondary-background-color) !important;
    border: 1.5px solid rgba(0,0,0,.08) !important;
    border-radius: 12px !important;
    color: var(--text-color) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .875rem !important;
    padding: .75rem 1rem !important;
    text-align: left !important;
    white-space: normal !important;
    height: auto !important;
    line-height: 1.45 !important;
    transition: all .2s cubic-bezier(.4,0,.2,1) !important;
    box-shadow: 0 1px 4px rgba(0,0,0,.06) !important;
}
.chip-btn .stButton > button:hover {
    border-color: #2563EB !important;
    background: rgba(37,99,235,.04) !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,.1), 0 1px 4px rgba(0,0,0,.06) !important;
    transform: translateY(-1px) !important;
    color: #2563EB !important;
}

/* ── Sidebar group labels ─────────────────────── */
.sidebar-label {
    display: block;
    font-family: 'Inter', sans-serif;
    font-size: .6875rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: #8B949E;
    padding: .875rem .5rem .3rem;
}

/* ── Step / loading text ──────────────────────── */
.step-text {
    display: flex;
    align-items: center;
    gap: .5rem;
    padding: .5rem 0;
    font-family: 'Inter', sans-serif;
    font-size: .8125rem;
    color: #64748B;
}
.t-dots { display: inline-flex; gap: 4px; align-items: center; }
.t-dots span {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #2563EB;
    animation: tBounce 1.2s ease-in-out infinite;
    display: inline-block;
}
.t-dots span:nth-child(2) { animation-delay: .2s; }
.t-dots span:nth-child(3) { animation-delay: .4s; }
@keyframes tBounce {
    0%,60%,100% { transform: translateY(0); opacity: .4; }
    30%          { transform: translateY(-5px); opacity: 1; }
}

/* ── Source cards ─────────────────────────────── */
.src-card {
    display: flex; align-items: flex-start; gap: 10px;
    padding: 10px 12px;
    border: 1px solid rgba(0,0,0,.07);
    border-radius: 10px; margin: 4px 0;
    background: var(--background-color);
    transition: all .15s ease;
}
.src-card:hover {
    border-color: rgba(37,99,235,.3);
    box-shadow: 0 2px 8px rgba(37,99,235,.08);
}
.src-icon { font-size: 18px; line-height: 1.6; flex-shrink: 0; margin-top: 1px; }
.src-body { flex: 1; min-width: 0; }
.src-type {
    font-family: 'Inter', sans-serif;
    font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: .07em;
    color: #94A3B8; margin-bottom: 2px;
}
.src-title {
    font-family: 'Inter', sans-serif;
    font-size: 13px; font-weight: 500;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.src-title a { color: #2563EB; text-decoration: none; transition: color .15s; }
.src-title a:hover { color: #1D4ED8; text-decoration: underline; }
.src-title-plain {
    font-family: 'Inter', sans-serif;
    font-size: 13px; font-weight: 500;
    color: var(--text-color);
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.src-section {
    font-family: 'Inter', sans-serif;
    font-size: 11px; color: #94A3B8; margin-top: 1px;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
SOURCE_ICONS = {
    "stackoverflow": "🟠",
    "reddit":        "🔴",
    "book":          "📚",
    "blog":          "✍️",
    "help":          "📘",
    "idea":          "💡",
}

EXAMPLE_QUESTIONS = [
    "How do I create a calculated field?",
    "What is a Level of Detail (LOD) expression?",
    "How do I connect Tableau to a live database?",
    "What's the difference between a dimension and a measure?",
]


# ── Helpers ────────────────────────────────────────────────────────────────────
def _esc(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _render_source(src: dict):
    icon    = SOURCE_ICONS.get(src["source_type"], "📄")
    label   = _esc(src["title"] or src["source_file"] or "Source")
    stype   = _esc((src["source_type"] or "").upper())
    section = _esc(src.get("section") or "")
    sec_html = f'<div class="src-section">{section}</div>' if section else ""
    if src["url"]:
        url = _esc(src["url"])
        title_html = f'<div class="src-title"><a href="{url}" target="_blank" rel="noopener">{label}</a></div>'
    else:
        title_html = f'<div class="src-title-plain">{label}</div>'
    st.markdown(
        f'<div class="src-card">'
        f'  <span class="src-icon">{icon}</span>'
        f'  <div class="src-body"><div class="src-type">{stype}</div>{title_html}{sec_html}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _render_messages(messages: list[dict]):
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                n = len(msg["sources"])
                with st.expander(f"🔗  {n} source{'s' if n != 1 else ''}"):
                    for src in msg["sources"]:
                        _render_source(src)


def _group_sessions(sessions: list[dict]) -> dict:
    today     = date.today()
    yesterday = today - timedelta(days=1)
    week_ago  = today - timedelta(days=7)
    groups: dict[str, list] = {"Today": [], "Yesterday": [], "Last 7 Days": [], "Older": []}
    for s in sessions:
        try:
            d = datetime.fromisoformat(s["created_at"]).date()
        except Exception:
            d = today
        if d == today:
            groups["Today"].append(s)
        elif d == yesterday:
            groups["Yesterday"].append(s)
        elif d >= week_ago:
            groups["Last 7 Days"].append(s)
        else:
            groups["Older"].append(s)
    return groups


# ── Session state ──────────────────────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = None
    st.session_state.messages   = []


def _load_session(session_id: int):
    st.session_state.session_id = session_id
    st.session_state.messages   = db.get_messages(session_id)


def _new_session():
    st.session_state.session_id = None
    st.session_state.messages   = []


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;
                padding:.125rem .25rem .875rem;margin-bottom:.125rem;">
        <div style="width:34px;height:34px;border-radius:9px;flex-shrink:0;
                    background:linear-gradient(135deg,#1D4ED8,#3B82F6);
                    display:flex;align-items:center;justify-content:center;
                    font-size:17px;box-shadow:0 2px 10px rgba(37,99,235,.45);">📊</div>
        <div>
            <div style="font-family:'Inter',sans-serif;font-size:.9375rem;
                        font-weight:600;color:#E2E8F0;letter-spacing:-.01em;
                        line-height:1.2;">Tableau Assistant</div>
            <div style="font-family:'Inter',sans-serif;font-size:.6875rem;
                        color:#484F58;margin-top:1px;">AI-powered help</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("＋  New Chat", use_container_width=True, key="new_chat_btn"):
        _new_session()
        st.rerun()

    st.markdown('<div style="border-top:1px solid #21262D;margin:.875rem 0;"></div>',
                unsafe_allow_html=True)

    sessions = db.get_sessions()
    print(f"[sidebar] db.get_sessions() returned {len(sessions)} session(s)", flush=True)

    if not sessions:
        st.markdown("""
        <div style="text-align:center;padding:1.5rem .5rem;font-family:'Inter',sans-serif;">
            <div style="font-size:1.5rem;margin-bottom:.5rem;opacity:.35;">💬</div>
            <div style="font-size:.8125rem;color:#8B949E;line-height:1.6;">
                No conversations yet.<br>Start a new chat above.
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        groups = _group_sessions(sessions)
        for group_name, group_sessions in groups.items():
            if not group_sessions:
                continue
            st.markdown(f'<span class="sidebar-label">{group_name}</span>',
                        unsafe_allow_html=True)
            for s in group_sessions:
                col1, col2    = st.columns([5, 1])
                is_active     = s["id"] == st.session_state.session_id
                display_title = ("▸ " if is_active else "") + s["title"][:38]
                with col1:
                    if st.button(display_title, key=f"sess_{s['id']}",
                                 use_container_width=True, help=s["created_at"][:10]):
                        _load_session(s["id"])
                        st.rerun()
                with col2:
                    if st.button("✕", key=f"del_{s['id']}", help="Delete conversation"):
                        db.delete_session(s["id"])
                        if st.session_state.session_id == s["id"]:
                            _new_session()
                        st.rerun()


# ── Resolve prompt FIRST so we know whether to show welcome ────────────────────
prompt = st.chat_input("Ask me anything about Tableau…")

if not prompt and "pending_question" in st.session_state:
    prompt = st.session_state.pop("pending_question")


# ── Main area ──────────────────────────────────────────────────────────────────
# Welcome only when there are no messages AND no incoming prompt this run.
if not st.session_state.messages and not prompt:
    st.markdown("""
    <div style="text-align:center;padding:3.5rem 0 2rem;user-select:none;">
        <div style="display:inline-flex;align-items:center;justify-content:center;
                    width:68px;height:68px;border-radius:18px;
                    background:linear-gradient(135deg,#1D4ED8 0%,#2563EB 50%,#60A5FA 100%);
                    font-size:1.875rem;margin-bottom:1.25rem;
                    box-shadow:0 8px 32px rgba(37,99,235,.38),0 2px 8px rgba(37,99,235,.2);">
            📊
        </div>
        <h1 style="font-family:'Inter',sans-serif;font-size:1.75rem;font-weight:700;
                   color:var(--text-color);margin:0 0 .5rem;
                   letter-spacing:-.03em;line-height:1.2;">
            Tableau Assistant
        </h1>
        <p style="font-family:'Inter',sans-serif;font-size:.9375rem;color:#94A3B8;
                  max-width:400px;margin:0 auto;line-height:1.65;">
            Ask anything about Tableau — answered from official docs,
            books, blogs, and community Q&amp;A.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="small")
    for i, q in enumerate(EXAMPLE_QUESTIONS):
        with (col1 if i % 2 == 0 else col2):
            st.markdown('<div class="chip-btn">', unsafe_allow_html=True)
            if st.button(q, use_container_width=True, key=f"ex_{i}"):
                st.session_state["pending_question"] = q
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.messages:
    _render_messages(st.session_state.messages)


# ── Process prompt ─────────────────────────────────────────────────────────────
if prompt:
    if st.session_state.session_id is None:
        sid = db.create_session(prompt)
        print(f"[create_session] created sid={sid} for prompt={prompt!r}", flush=True)
        st.session_state.session_id = sid
    else:
        sid = st.session_state.session_id

    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[-6:]
    ]

    db.save_message(sid, "user", prompt, [])
    st.session_state.messages.append({"role": "user", "content": prompt, "sources": []})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if query.is_conversational(prompt):
            with st.spinner(""):
                answer = query.quick_reply(prompt, history)
            st.markdown(answer)
            sources = []

        else:
            _DOTS = '<div class="t-dots"><span></span><span></span><span></span></div>'
            _step = st.empty()
            _step.markdown(
                f'<div class="step-text">{_DOTS} Generating search queries…</div>',
                unsafe_allow_html=True,
            )

            def _on_step(s: str):
                _step.markdown(
                    f'<div class="step-text">{_DOTS} {_esc(s)}</div>',
                    unsafe_allow_html=True,
                )

            messages, sources, direct_answer = query.retrieve(prompt, history, on_step=_on_step)
            _step.empty()

            if direct_answer is not None:
                answer = direct_answer
                st.markdown(answer)
            else:
                def _token_gen():
                    for chunk in query.stream_response(messages):
                        delta = chunk.choices[0].delta.content
                        if delta:
                            yield delta

                answer = st.write_stream(_token_gen())

                if answer.startswith(query.OFFTOPIC_PREFIX):
                    answer  = answer[len(query.OFFTOPIC_PREFIX):].strip()
                    sources = []
                else:
                    query.store_result(prompt, answer, sources)

            if sources:
                n = len(sources)
                with st.expander(f"🔗  {n} source{'s' if n != 1 else ''}"):
                    for src in sources:
                        _render_source(src)

    db.save_message(sid, "assistant", answer, sources)
    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})

    already_titled = any(m.get("sources") for m in st.session_state.messages[:-1])
    if sources and not already_titled:
        title = query.generate_title(prompt, answer)
        print(f"Generated title: {title!r}", flush=True)
        db.rename_session(sid, title)

    st.rerun()