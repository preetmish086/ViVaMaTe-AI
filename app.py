import streamlit as st
from rag.pdf_loader import extract_text_from_pdf
from rag.text_splitter import split_text
from rag.vector_store import create_vector_store
from rag.retriever import retrieve_chunks
from rag.embeddings import load_embeddings
from llm.response_generator import generate_response
from utils.memory import add_turn, clear_history
from utils.session_manager import initialize_session
from modules.presentation_generator import(
    show_presentation_generator
)
from modules.mock_viva import show_mock_viva
#from archive.presentation_practice import show_practice_mode
from modules.final_report import show_final_report
import json
import os

# ── Config ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ViVaMaTe AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

initialize_session()

PERSONAS = {
    "professor":        ("📚 Professor",        "Academic, rigorous, structured"),
    "student":          ("🌱 Student",           "Simple, curious, relatable"),
    "skeptic":          ("🔍 Skeptic",           "Critical, probing, questioning"),
    "industry_expert":  ("💼 Industry Expert",   "Practical, deployment-focused"),
    "interviewer":      ("🎯 Interviewer",       "Probing, interview-style"),
}

# ── Global Styling ────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ---------- Base ---------- */
    html, body, [class*="css"], .stApp, .stMarkdown, .stChatMessage {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    .stApp {
        background:
            radial-gradient(1200px 700px at 8% -10%, rgba(139,92,246,0.35), transparent 60%),
            radial-gradient(1000px 600px at 100% 10%, rgba(16,185,129,0.22), transparent 60%),
            radial-gradient(900px 500px at 50% 110%, rgba(236,72,153,0.18), transparent 60%),
            linear-gradient(135deg, #0a0b14 0%, #141832 45%, #0d0f1c 100%);
        background-attachment: fixed;
        color: #e6e8ef;
    }
    [data-testid="stHeader"] { background: transparent !important; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}    .block-container {padding-top: 2rem; padding-bottom: 6rem; max-width: 1200px;}

    /* ---------- Typography ---------- */
    h1, h2, h3, h4 { color: #f4f5fb !important; letter-spacing: -0.02em; }
    h1 { font-weight: 800 !important; }
    p, span, label, div { color: #c7cad6; }
    code, pre, kbd { font-family: 'JetBrains Mono', monospace !important; }

    /* ---------- Hero ---------- */
    .hero {
        background: linear-gradient(135deg, rgba(99,102,241,0.12), rgba(16,185,129,0.06));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 28px 32px;
        margin-bottom: 24px;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
    }
    .hero h1 {
        font-size: 2.1rem !important;
        margin: 0 0 6px 0 !important;
        background: linear-gradient(90deg, #ffffff 0%, #a5b4fc 50%, #6ee7b7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero p { color: #9aa0b4; margin: 0; font-size: 0.98rem; }
    .badge {
        display: inline-flex; align-items: center; gap: 6px;
        padding: 4px 10px; border-radius: 999px;
        background: rgba(99,102,241,0.15);
        border: 1px solid rgba(99,102,241,0.35);
        color: #c7d2fe; font-size: 0.72rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.08em;
        margin-bottom: 10px;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #11142a 0%,
        #0b0d18 60%,
        #0a0b14 100%
    ) !important;

    border-right: 1px solid rgba(139,92,246,0.18);
    box-shadow: 4px 0 30px rgba(0,0,0,0.4);
}
    [data-testid="stSidebar"] > div { background: transparent !important; }
    [data-testid="stSidebarCollapsedControl"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        border-radius: 10px !important;
        color: #fff !important;
        box-shadow: 0 6px 18px rgba(99,102,241,0.45);
        visibility: visible !important; opacity: 1 !important;
    }
    [data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }
    .sidebar-brand {
        display: flex; align-items: center; gap: 10px;
        padding: 6px 0 14px 0; border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 16px;
    }
    .sidebar-brand .logo {
        width: 36px; height: 36px; border-radius: 10px;
        background: linear-gradient(135deg, #6366f1, #10b981);
        display: flex; align-items: center; justify-content: center;
        font-size: 18px; box-shadow: 0 6px 20px rgba(99,102,241,0.35);
    }
    .sidebar-brand .name { font-weight: 700; color: #f4f5fb; font-size: 1rem; }
    .sidebar-brand .sub { color: #7b8095; font-size: 0.72rem; letter-spacing: 0.05em; text-transform: uppercase; }

    .section-label {
        font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em;
        color: #7b8095; text-transform: uppercase;
        margin: 14px 0 8px 0;
    }

    /* ---------- Buttons ---------- */
    .stButton > button {
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        background: rgba(255,255,255,0.03) !important;
        color: #d8dbe7 !important;
        font-weight: 500 !important;
        padding: 0.55rem 0.9rem !important;
        transition: all 0.18s ease !important;
        text-align: left !important;
    }
    .stButton > button:hover {
        background: rgba(99,102,241,0.12) !important;
        border-color: rgba(99,102,241,0.4) !important;
        transform: translateY(-1px);
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        color: #ffffff !important;
        box-shadow: 0 8px 24px rgba(99,102,241,0.35) !important;
    }

    /* ---------- File uploader ---------- */
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.025);
        border: 1.5px dashed rgba(255,255,255,0.15);
        border-radius: 14px;
        padding: 8px;
        transition: all 0.2s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(99,102,241,0.5);
        background: rgba(99,102,241,0.05);
    }
    [data-testid="stFileUploader"] section { background: transparent !important; border: none !important; }
    [data-testid="stFileUploader"] small { color: #7b8095 !important; }

    /* ---------- Cards / containers ---------- */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255,255,255,0.025) !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 14px !important;
        backdrop-filter: blur(10px);
    }

    /* ---------- Chat ---------- */
    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 14px 18px !important;
        margin-bottom: 10px;
    }
    [data-testid="stChatInput"] {
        background: rgba(15,17,28,0.85) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 14px !important;
        backdrop-filter: blur(12px);
    }
    [data-testid="stChatInput"] textarea { color: #f4f5fb !important; }

    /* ---------- Tabs ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(255,255,255,0.03);
        padding: 5px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.06);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent; border-radius: 8px;
        color: #9aa0b4; font-weight: 500;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(99,102,241,0.25), rgba(79,70,229,0.25)) !important;
        color: #ffffff !important;
    }

    /* ---------- Source cards ---------- */
    .src-card {
        background: linear-gradient(135deg, rgba(99,102,241,0.06), rgba(16,185,129,0.04));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 12px;
        transition: all 0.2s ease;
    }
    .src-card:hover { border-color: rgba(99,102,241,0.4); transform: translateY(-1px); }
    .src-head {
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 10px;
    }
    .src-title { font-weight: 700; color: #f4f5fb; font-size: 0.95rem; }
    .src-meta {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #9aa0b4;
        background: rgba(255,255,255,0.05);
        padding: 3px 8px; border-radius: 6px;
    }
    .src-body {
        color: #c7cad6; font-size: 0.88rem; line-height: 1.6;
        border-left: 2px solid rgba(99,102,241,0.5);
        padding-left: 12px; margin-top: 6px;
    }

    /* ---------- Alerts ---------- */
    [data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(10px);
    }

    /* ---------- Empty state ---------- */
    .empty {
        text-align: center; padding: 60px 20px;
        background: rgba(255,255,255,0.02);
        border: 1px dashed rgba(255,255,255,0.1);
        border-radius: 18px;
    }
    .empty .icon { font-size: 3rem; margin-bottom: 12px; }
    .empty h3 { margin: 0 0 6px 0 !important; }
    .empty p { color: #7b8095; }

    /* ---------- Metric pills ---------- */
    .pill-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }
    .pill {
        display: inline-flex; align-items: center; gap: 6px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 6px 12px; border-radius: 999px;
        font-size: 0.78rem; color: #c7cad6;
    }
    .pill .dot { width: 6px; height: 6px; border-radius: 50%; background: #10b981; box-shadow: 0 0 8px #10b981; }
    [data-testid="stChatInput"] {
    position: sticky;
    bottom: 1rem;
    z-index: 100;
}      
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for key, default in [
    ("chat_history", []),
    ("chunks", []),
    ("faiss_index", None),
    ("paper_name", None),
    ("persona", "professor"),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand">
            <div class="logo">🔬</div>
            <div>
                <div class="name">ViVaMaTe AI</div>
                <div class="sub">Paper Intelligence</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">📄 Document</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload Research Paper (PDF)", type=["pdf"], label_visibility="collapsed")

    st.markdown('<div class="section-label">🎭 AI Persona</div>', unsafe_allow_html=True)
    for key, (label, desc) in PERSONAS.items():
        if st.button(f"{label}", use_container_width=True,
                     type="primary" if st.session_state.persona == key else "secondary",
                     key=f"persona_{key}"):
            st.session_state.persona = key
            st.rerun()

    active_label, active_desc = PERSONAS[st.session_state.persona]
    st.caption(f"✨ {active_desc}")

    st.markdown('<div class="section-label">⚙️ Session</div>', unsafe_allow_html=True)
    if st.button("🗑️  Clear Chat", use_container_width=True):
        st.session_state.chat_history = clear_history()
        st.rerun()

    if st.session_state.paper_name:
        with st.container(border=True):
            st.markdown(f"**📄 Loaded Paper**")
            st.caption(st.session_state.paper_name)
            st.markdown(
                f'<div class="pill-row">'
                f'<span class="pill"><span class="dot"></span>Indexed</span>'
                f'<span class="pill">🧩 {len(st.session_state.chunks)} chunks</span>'
                f'</div>',
                unsafe_allow_html=True
            )

# ── PDF Processing ─────────────────────────────────────────────────────────────
if uploaded and uploaded.name != st.session_state.paper_name:
    # st.write(st.session_state.paper_context)
    with st.spinner("Reading, chunking, and indexing paper..."):
        try:
            text = extract_text_from_pdf(uploaded)
            chunks = split_text(text)
            index = create_vector_store(chunks, load_embeddings(), uploaded.name)
            st.session_state.paper_context = {
            "paper_name": uploaded.name,
            "full_text": text,
            "chunks": chunks,
            "faiss_index": index
}
            st.session_state.chunks = chunks
            st.session_state.faiss_index = index
            st.session_state.paper_name = uploaded.name
            st.session_state.chat_history = clear_history()

            st.success(f"✅ Indexed {len(chunks)} chunks.")

        except ValueError as e:
            st.error(str(e))
            st.stop()

# ── Main UI ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <span class="badge">● Live · {active_label}</span>
    <h1>ViVaMaTe AI 🔬</h1>
    <p>Chat with your research papers through five expert personas — grounded in retrieval, powered by your sources.</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.faiss_index:
    st.markdown("""
        <div class="empty">
            <div class="icon">📄</div>
            <h3>Upload a research paper to begin</h3>
            <p>Drop a PDF into the sidebar to extract, embed, and start your research conversation.</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Tabs: Chat & Sources ──────────────────────────────────────────────────────
chat_tab, presentation_tab, viva_tab, practice_tab, report_tab = st.tabs([
    "💬 Research Chat",
    # "📚 Knowledge Base",
    "📊 Presentation Generator",
    "🎓 Mock Viva",
    "🎤 Practice Mode",
    "📈 Final Report"
])

with chat_tab:

    # Chat input

    question = st.chat_input(
        "Ask anything about the paper..."
    )
    
    # Render previous chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Auto-scroll
    st.markdown("""
        <script>
        function scrollToBottom() {
            const main = window.parent.document.querySelector('.main');

            if (main) {
                main.scrollTo({
                    top: main.scrollHeight,
                    behavior: 'smooth'
                });
            }
        }

        setTimeout(scrollToBottom, 200);
        </script>
    """, unsafe_allow_html=True)

    if question :

        # User message
        with st.chat_message("user"):
            st.markdown(question)

        # Retrieve chunks
        chunks = retrieve_chunks(
            st.session_state.faiss_index,
            question
        )

        # Assistant response
        with st.chat_message("assistant"):

            with st.spinner(
                f"Thinking as {PERSONAS[st.session_state.persona][0]}..."
            ):

                answer = generate_response(
                    question=question,
                    chunks=chunks,
                    persona_key=st.session_state.persona,
                    chat_history=st.session_state.chat_history
                )

            st.markdown(answer)

            # Retrieved sources
            with st.expander(
                f"📚 Evidence Used For This Answer ({len(chunks)} chunks)"
            ):
                for i, c in enumerate(chunks):
                    source = c.metadata.get(
                        "source",
                        "Unknown PDF"
                    )

                    chunk_id = c.metadata.get(
                        "chunk_id",
                        "?"
                    )

                    with st.container(border=True):

                        st.markdown(
                            f"**📄 Source {i+1}**"
                        )

                        st.caption(
                            f"{source} • Chunk {chunk_id}"
                        )

                        st.write(
                            c.page_content[:400] + "..."
                        )


        # Save history
        st.session_state.chat_history = add_turn(
            st.session_state.chat_history,
            "user",
            question
        )

        st.session_state.chat_history = add_turn(
            st.session_state.chat_history,
            "assistant",
            answer
        )


# with sources_tab:
#     st.markdown("### 📚 Indexed Knowledge Base")
#     st.caption(f"All {len(st.session_state.chunks)} chunks from **{st.session_state.paper_name}**")

#     if not st.session_state.chunks:
#         st.info("No chunks indexed yet.")
#     else:
#         preview_count = min(30, len(st.session_state.chunks))
#         st.caption(f"Showing first {preview_count} chunks")
#         for i, c in enumerate(st.session_state.chunks[:preview_count]):
#             try:
#                 content = c.page_content if hasattr(c, "page_content") else str(c)
#                 source = c.metadata.get("source", st.session_state.paper_name) if hasattr(c, "metadata") else st.session_state.paper_name
#                 chunk_id = c.metadata.get("chunk_id", i) if hasattr(c, "metadata") else i
#             except Exception:
#                 content = str(c); source = st.session_state.paper_name; chunk_id = i
#             preview = content.replace("\n", " ").strip()[:320]
#             st.markdown(f"""
#                 <div class="src-card">
#                     <div class="src-head">
#                         <div class="src-title">🧩 Chunk {i+1}</div>
#                         <div class="src-meta">{source} · id {chunk_id}</div>
#                     </div>
#                     <div class="src-body">{preview}…</div>
#                 </div>
#             """, unsafe_allow_html=True)
    
with presentation_tab:
        show_presentation_generator()
        with st.expander("📄 Paper Information"):
            st.write(
                st.session_state.paper_context["paper_name"]
            )

            st.write(
                f"Chunks Indexed: {len(st.session_state.paper_context['chunks'])}"
            )
        

with viva_tab:
        show_mock_viva()

with practice_tab:

    st.markdown("## 🎤 VivaMate Practice Mode")

    st.link_button(
        "🚀 Open Practice Mode",
        "http://127.0.0.1:5000"
    )

    if st.button("Refresh"):
        st.rerun()

    st.markdown("---")

    if os.path.exists("results.json"):

        try:

            with open("results.json","r") as f:

                practice_data = json.load(f)

            st.subheader("📊 Last Practice Session")

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric(
                    "Confidence",
                    f"{practice_data.get('confidence_score',0)}%"
                )

            with c2:
                st.metric(
                    "Engagement",
                    f"{practice_data.get('engagement_score',0)}%"
                )

            with c3:
                st.metric(
                    "Eye Contact",
                    f"{practice_data.get('eye_contact_rate',0)}%"
                )

            with c4:
                st.metric(
                    "Face Detection",
                    f"{practice_data.get('face_detection_rate',0)}%"
                )

            left,right = st.columns(2)

            with left:

                st.subheader("💪 Strengths")

                strengths = practice_data.get(
                    "strengths",
                    []
                )

                if strengths:

                    for item in strengths:
                        st.success(item)

                else:
                    st.info(
                        "No strengths available yet."
                    )

            with right:

                st.subheader("📌 Improvements")

                improvements = practice_data.get(
                    "improvements",
                    []
                )

                if improvements:

                    for item in improvements:
                        st.warning(item)

                else:
                    st.success(
                        "No improvements required yet."
                    )

            transcript = practice_data.get(
                "transcript",
                ""
            ).strip()

            if len(transcript.split()) >= 15:

                st.subheader("📝 Practice Transcript")

                st.text_area(
                    "",
                    transcript,
                    height=200
                )   

            fillers = practice_data.get(
                "filler_words",
                {}
            )

            used_fillers = {
                k:v
                for k,v in fillers.items()
                if v > 0
            }

            st.subheader("🗣 Filler Words")

            if used_fillers:

                for word,count in used_fillers.items():

                    st.write(
                        f"**{word}** : {count}"
                    )

            else:

                st.success(
                    "No filler words detected."
                )

        except Exception as e:

            st.error(
                f"Unable to load practice data: {e}"
            )

with report_tab:

    show_final_report()