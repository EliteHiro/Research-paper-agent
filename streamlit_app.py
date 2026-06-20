import streamlit as st
import os
import tempfile

# Load API key: Streamlit Cloud secrets first, then .env fallback for local dev
try:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except Exception:
    from dotenv import load_dotenv
    load_dotenv()

from app.parsers.pdf_parser import PDFParser
from app.services.paper_service import PaperAnalysisService

# Set up the page
st.set_page_config(page_title="Research Paper Agent", page_icon="🧬", layout="wide")

# ── Premium CSS inspired by makingsoftware.com ──────────────────────────────
st.markdown("""
<style>
    /* ═══════════════════════════════════════════════════
       FONTS — Editorial serif + monospace system
       ═══════════════════════════════════════════════════ */
    @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,500;0,8..60,600;0,8..60,700;1,8..60,400&family=JetBrains+Mono:wght@300;400;500;600&display=swap');

    :root {
        --font-serif: 'Source Serif 4', 'Georgia', serif;
        --font-mono:  'JetBrains Mono', 'Menlo', monospace;
        --bg:         #FAFAF7;
        --bg-card:    #FFFFFF;
        --text:       #1A1A1A;
        --text-muted: rgba(26, 26, 26, 0.5);
        --text-light: rgba(26, 26, 26, 0.35);
        --cobalt:     #2B54A0;
        --cobalt-light: #3D6FCC;
        --accent-warm: #C45D3E;
        --border:     rgba(26, 26, 26, 0.12);
        --border-dark: rgba(26, 26, 26, 0.25);
        --shadow-sm:  0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.06);
        --shadow-md:  0 4px 12px rgba(0,0,0,0.06), 0 2px 4px rgba(0,0,0,0.04);
        --shadow-lg:  0 10px 30px rgba(0,0,0,0.08), 0 4px 8px rgba(0,0,0,0.04);
        --radius:     6px;
    }

    /* ═══════════════════════════════════════════════════
       GLOBAL OVERRIDES
       ═══════════════════════════════════════════════════ */
    .main {
        background-color: var(--bg) !important;
    }
    .stApp {
        background-color: var(--bg) !important;
    }
    .block-container {
        max-width: 1200px !important;
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
    }

    /* Hide default Streamlit chrome */
    header { visibility: hidden; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    .stDeployButton { display: none; }

    /* Base typography */
    html, body, [class*="css"] {
        font-family: var(--font-serif) !important;
        color: var(--text) !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    /* ═══════════════════════════════════════════════════
       NAVIGATION BAR — Monospace, uppercase, minimal
       ═══════════════════════════════════════════════════ */
    .nav-bar {
        font-family: var(--font-mono);
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--cobalt);
        padding-bottom: 2.5rem;
        border-bottom: 1px solid var(--border);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .nav-bar a {
        color: var(--cobalt);
        text-decoration: none;
        transition: opacity 0.2s ease;
    }
    .nav-bar a:hover {
        opacity: 0.65;
    }

    /* ═══════════════════════════════════════════════════
       HERO — Editorial header with title + rule + stats
       ═══════════════════════════════════════════════════ */
    .hero-section {
        margin-top: 4rem;
        display: grid;
        grid-template-columns: auto 1fr auto;
        align-items: center;
        gap: 1.5rem;
        font-family: var(--font-mono);
        text-transform: uppercase;
    }
    .hero-section h1 {
        font-family: var(--font-mono) !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.08em;
        color: var(--text) !important;
        margin: 0 !important;
        padding: 0 !important;
        white-space: nowrap;
    }
    .hero-divider {
        height: 1px;
        width: 100%;
        background: var(--text);
    }
    .hero-stats {
        font-family: var(--font-mono);
        font-size: 0.7rem;
        color: var(--text-muted);
        text-transform: uppercase;
        white-space: nowrap;
    }

    /* ═══════════════════════════════════════════════════
       SUBTITLE — Serif description
       ═══════════════════════════════════════════════════ */
    .subtitle {
        font-family: var(--font-serif);
        font-size: 1.15rem;
        line-height: 1.7;
        color: var(--text-muted);
        max-width: 680px;
        margin-top: 1.5rem;
    }

    /* ═══════════════════════════════════════════════════
       UPLOAD ZONE — Clean, minimal, editorial
       ═══════════════════════════════════════════════════ */
    .upload-container {
        margin-top: 3rem;
        padding: 3rem 2.5rem;
        border: 1.5px dashed var(--border-dark);
        border-radius: var(--radius);
        background: var(--bg-card);
        text-align: center;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .upload-container:hover {
        border-color: var(--cobalt);
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }
    .upload-container::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--cobalt), var(--cobalt-light));
        opacity: 0;
        transition: opacity 0.35s ease;
    }
    .upload-container:hover::before {
        opacity: 1;
    }
    .upload-icon {
        font-size: 2.4rem;
        margin-bottom: 0.8rem;
        display: block;
        opacity: 0.7;
    }
    .upload-label {
        font-family: var(--font-mono);
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--text-muted);
        margin-bottom: 0.5rem;
    }
    .upload-hint {
        font-family: var(--font-serif);
        font-size: 0.9rem;
        color: var(--text-light);
    }

    /* Streamlit file uploader overrides */
    [data-testid="stFileUploader"] {
        background: transparent !important;
    }
    [data-testid="stFileUploader"] section {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    [data-testid="stFileUploader"] button {
        font-family: var(--font-mono) !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        background: var(--text) !important;
        color: var(--bg) !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.6rem 1.8rem !important;
        transition: all 0.25s ease !important;
        cursor: pointer !important;
    }
    [data-testid="stFileUploader"] button:hover {
        background: var(--cobalt) !important;
        transform: translateY(-1px) !important;
        box-shadow: var(--shadow-sm) !important;
    }
    [data-testid="stFileUploader"] small {
        font-family: var(--font-mono) !important;
        font-size: 0.65rem !important;
        color: var(--text-light) !important;
        text-transform: uppercase !important;
    }

    /* ═══════════════════════════════════════════════════
       ANALYZE BUTTON
       ═══════════════════════════════════════════════════ */
    .stButton > button {
        font-family: var(--font-mono) !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        background: var(--text) !important;
        color: var(--bg) !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.85rem 2.5rem !important;
        height: auto !important;
        width: auto !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        position: relative;
        overflow: hidden;
    }
    .stButton > button:hover {
        background: var(--cobalt) !important;
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-md) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ═══════════════════════════════════════════════════
       FILE PILL — shows uploaded file name
       ═══════════════════════════════════════════════════ */
    .file-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        font-family: var(--font-mono);
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 100px;
        padding: 0.5rem 1.2rem;
        margin-top: 1rem;
        color: var(--text);
        box-shadow: var(--shadow-sm);
    }
    .file-pill .dot {
        width: 6px; height: 6px;
        border-radius: 50%;
        background: #34A853;
        animation: pulse-dot 2s ease-in-out infinite;
    }
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; }
        50%      { opacity: 0.4; }
    }

    /* ═══════════════════════════════════════════════════
       SECTION HEADERS — Mono + rules (like the site)
       ═══════════════════════════════════════════════════ */
    .section-header {
        display: grid;
        grid-template-columns: auto 1fr;
        align-items: center;
        gap: 1rem;
        margin-top: 3.5rem;
        margin-bottom: 1.5rem;
    }
    .section-header h2 {
        font-family: var(--font-mono) !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        color: var(--text) !important;
        margin: 0 !important;
        white-space: nowrap;
    }
    .section-rule {
        height: 1px;
        width: 100%;
        background: var(--text);
    }

    /* ═══════════════════════════════════════════════════
       RESULT CARDS — Clean white cards, subtle shadows
       ═══════════════════════════════════════════════════ */
    .result-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 2rem 2.2rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .result-card:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
        border-color: var(--border-dark);
    }
    .result-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 3px; height: 100%;
        background: var(--cobalt);
        opacity: 0;
        transition: opacity 0.25s ease;
    }
    .result-card:hover::before {
        opacity: 1;
    }
    .result-card p, .result-card li {
        font-family: var(--font-serif);
        font-size: 1rem;
        line-height: 1.75;
        color: var(--text);
    }

    /* Card label — monospace uppercase */
    .card-label {
        font-family: var(--font-mono);
        font-size: 0.68rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: var(--text-muted);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .card-label .label-dot {
        width: 5px; height: 5px;
        border-radius: 50%;
        background: var(--cobalt);
    }

    /* ═══════════════════════════════════════════════════
       DOT LEADER PATTERN (SVG like makingsoftware.com)
       ═══════════════════════════════════════════════════ */
    .dot-leader {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0.4rem 0;
    }
    .dot-leader .leader-text {
        font-family: var(--font-serif);
        font-size: 0.95rem;
        line-height: 1.7;
        color: var(--text);
        flex-shrink: 0;
    }
    .dot-leader .leader-dots {
        flex: 1;
        height: 10px;
        background-image: repeating-linear-gradient(
            90deg,
            var(--text-light) 0px,
            var(--text-light) 3px,
            transparent 3px,
            transparent 7px
        );
        background-position: bottom;
        background-size: 7px 1px;
        background-repeat: repeat-x;
    }

    /* ═══════════════════════════════════════════════════
       BULLET ITEMS — Editorial list styling
       ═══════════════════════════════════════════════════ */
    .bullet-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.8rem 0;
        border-bottom: 1px solid var(--border);
        transition: background 0.2s ease;
    }
    .bullet-item:last-child {
        border-bottom: none;
    }
    .bullet-item:hover {
        background: rgba(43, 84, 160, 0.02);
    }
    .bullet-marker {
        font-family: var(--font-mono);
        font-size: 0.7rem;
        color: var(--cobalt);
        margin-top: 0.35rem;
        flex-shrink: 0;
    }
    .bullet-text {
        font-family: var(--font-serif);
        font-size: 1rem;
        line-height: 1.7;
        color: var(--text);
    }

    /* ═══════════════════════════════════════════════════
       EQUATION BLOCKS — Highlighted, numbered
       ═══════════════════════════════════════════════════ */
    .equation-block {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-left: 3px solid var(--accent-warm);
        border-radius: 0 var(--radius) var(--radius) 0;
        padding: 1.5rem 2rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
    }
    .equation-block:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }
    .eq-number {
        font-family: var(--font-mono);
        font-size: 0.65rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: var(--accent-warm);
        margin-bottom: 0.8rem;
    }
    .eq-explanation {
        font-family: var(--font-serif);
        font-size: 0.95rem;
        line-height: 1.7;
        color: var(--text);
        margin-top: 1rem;
        padding-top: 0.8rem;
        border-top: 1px solid var(--border);
    }

    /* ═══════════════════════════════════════════════════
       NOTES TEXTAREA
       ═══════════════════════════════════════════════════ */
    .stTextArea textarea {
        font-family: var(--font-serif) !important;
        font-size: 0.95rem !important;
        line-height: 1.8 !important;
        color: var(--text) !important;
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 1.5rem !important;
    }
    .stTextArea textarea:focus {
        border-color: var(--cobalt) !important;
        box-shadow: 0 0 0 2px rgba(43, 84, 160, 0.1) !important;
    }

    /* ═══════════════════════════════════════════════════
       TAB OVERRIDES — Minimal, editorial
       ═══════════════════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0 !important;
        border-bottom: 1px solid var(--border) !important;
        background: transparent !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: var(--font-mono) !important;
        font-size: 0.72rem !important;
        font-weight: 400 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        color: var(--text-muted) !important;
        padding: 0.8rem 1.4rem !important;
        transition: all 0.25s ease !important;
        position: relative;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text) !important;
        background: rgba(26, 26, 26, 0.03) !important;
    }
    .stTabs [aria-selected="true"] {
        color: var(--text) !important;
        font-weight: 500 !important;
        background: transparent !important;
        border-bottom: 2px solid var(--text) !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1.5rem !important;
    }

    /* ═══════════════════════════════════════════════════
       STATUS / SPINNER OVERRIDES
       ═══════════════════════════════════════════════════ */
    [data-testid="stStatusWidget"] {
        font-family: var(--font-mono) !important;
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
    }
    [data-testid="stStatusWidget"] p,
    [data-testid="stStatusWidget"] span {
        font-family: var(--font-mono) !important;
        font-size: 0.78rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.04em !important;
    }

    /* ═══════════════════════════════════════════════════
       INFO / SUCCESS / WARNING / ERROR OVERRIDES
       ═══════════════════════════════════════════════════ */
    .stAlert {
        font-family: var(--font-serif) !important;
        border-radius: var(--radius) !important;
    }

    /* ═══════════════════════════════════════════════════
       EXPANDER OVERRIDES
       ═══════════════════════════════════════════════════ */
    [data-testid="stExpander"] {
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        background: var(--bg-card) !important;
        box-shadow: var(--shadow-sm) !important;
    }
    [data-testid="stExpander"] summary {
        font-family: var(--font-mono) !important;
        font-size: 0.78rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
    }

    /* ═══════════════════════════════════════════════════
       PROGRESS ANIMATION
       ═══════════════════════════════════════════════════ */
    @keyframes shimmer {
        0%   { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    .progress-bar {
        height: 2px;
        background: linear-gradient(90deg,
            transparent 0%,
            var(--cobalt) 50%,
            transparent 100%
        );
        background-size: 200% 100%;
        animation: shimmer 2s ease-in-out infinite;
        margin: 1rem 0;
        border-radius: 1px;
    }

    /* ═══════════════════════════════════════════════════
       FOOTER
       ═══════════════════════════════════════════════════ */
    .app-footer {
        margin-top: 5rem;
        padding-top: 2rem;
        border-top: 1px solid var(--border);
        font-family: var(--font-mono);
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--text-light);
        text-align: center;
    }

    /* ═══════════════════════════════════════════════════
       SMOOTH SCROLL & SELECTION
       ═══════════════════════════════════════════════════ */
    html { scroll-behavior: smooth; }
    ::selection {
        background: rgba(43, 84, 160, 0.15);
        color: var(--text);
    }

    /* ═══════════════════════════════════════════════════
       RESPONSIVE
       ═══════════════════════════════════════════════════ */
    @media (max-width: 768px) {
        .hero-section {
            grid-template-columns: 1fr !important;
            gap: 0.5rem !important;
        }
        .hero-divider { display: none; }
        .hero-section h1 { font-size: 0.95rem !important; }
        .result-card { padding: 1.5rem !important; }
        .stTabs [data-baseweb="tab"] {
            padding: 0.6rem 0.8rem !important;
            font-size: 0.65rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ── Navigation ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav-bar">
    <span>←</span>
    <a href="#">Research Paper Agent</a>
</div>
""", unsafe_allow_html=True)

# ── Hero Section ────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-section">
    <h1>Research Paper Agent</h1>
    <div class="hero-divider"></div>
    <span class="hero-stats">[ ai-powered · multi-agent · analysis ]</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p class="subtitle">
    Upload any scientific paper and let advanced multi-agent AI extract summaries,
    key contributions, limitations, and mathematically decode complex equations —
    all in seconds.
</p>
""", unsafe_allow_html=True)

# ── Upload Zone ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="upload-container">
    <span class="upload-icon">⬡</span>
    <div class="upload-label">Upload Document</div>
    <div class="upload-hint">Drop a PDF research paper below to begin analysis</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    uploaded_file = st.file_uploader(
        "Drop your PDF research paper here",
        type=["pdf"],
        label_visibility="collapsed"
    )

# ── Analysis Flow ───────────────────────────────────────────────────────────
if uploaded_file is not None:
    # Show file pill
    st.markdown(f"""
    <div style="text-align: center;">
        <div class="file-pill">
            <span class="dot"></span>
            <span>{uploaded_file.name}</span>
            <span style="color: var(--text-light);">· {uploaded_file.size / 1024:.0f} KB</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        analyze_clicked = st.button("⬡  Analyze Paper")

    if analyze_clicked:
        with st.status("Analyzing paper...", expanded=True) as status:
            try:
                st.write("↳ Loading PDF document...")

                # Save the uploaded file temporarily so PyMuPDF can read it
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name

                st.write("↳ Extracting text and parsing sections...")
                parser = PDFParser()
                text = parser.extract_text(tmp_path)

                st.write("↳ Running multi-agent analysis...")
                service = PaperAnalysisService()
                result = service.analyze(text)

                status.update(label="Analysis complete", state="complete", expanded=False)

                # Cleanup the temporary file
                os.remove(tmp_path)

                st.markdown("<br>", unsafe_allow_html=True)

                # ── Results Section Header ──
                st.markdown("""
                <div class="section-header">
                    <h2>Analysis Results</h2>
                    <div class="section-rule"></div>
                </div>
                """, unsafe_allow_html=True)

                # ── Tabs ──
                tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
                    "Summary",
                    "Key Findings",
                    "Contributions",
                    "Limitations",
                    "Equations",
                    "Journal Notes",
                    "📊 Diagram"
                ])

                def parse_bullet_points(raw_list):
                    '''Flattens a list that might contain a single big markdown blob into clean strings.'''
                    clean_list = []
                    for item in raw_list:
                        if "\\n" in item:
                            for line in item.split("\\n"):
                                cleaned = line.strip(" -*•\\r\\n")
                                if cleaned:
                                    clean_list.append(cleaned)
                        else:
                            cleaned = item.strip(" -*•\\r\\n")
                            if cleaned:
                                clean_list.append(cleaned)
                    return clean_list

                with tab1:
                    st.markdown("""
                    <div class="result-card">
                        <div class="card-label"><span class="label-dot"></span> Paper Summary</div>
                    </div>
                    """, unsafe_allow_html=True)
                    summary_text = result.get("summary", "No summary generated.")
                    st.markdown(f"""
                    <div class="result-card">
                        <p>{summary_text}</p>
                    </div>
                    """, unsafe_allow_html=True)

                with tab2:
                    st.markdown("""
                    <div class="section-header" style="margin-top: 0;">
                        <h2>Key Findings</h2>
                        <div class="section-rule"></div>
                    </div>
                    """, unsafe_allow_html=True)

                    points = parse_bullet_points(result.get("key_points", []))
                    if points:
                        md_text = "".join([f"<div style='display:flex; gap:10px; margin-bottom:10px; align-items:flex-start;'><span style='flex-shrink:0; font-size:1.1rem;'>💡</span><span style='line-height:1.6;'>{p}</span></div>" for p in points])
                        st.markdown(f"""
                        <div class="result-card">
                            {md_text}

                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="result-card">
                            <p style="color: var(--text-muted);">No key findings extracted.</p>
                        </div>
                        """, unsafe_allow_html=True)

                with tab3:
                    st.markdown("""
                    <div class="section-header" style="margin-top: 0;">
                        <h2>Novel Contributions</h2>
                        <div class="section-rule"></div>
                    </div>
                    """, unsafe_allow_html=True)

                    contributions = parse_bullet_points(result.get("contributions", []))
                    if contributions:
                        md_text = "".join([f"<div style='display:flex; gap:10px; margin-bottom:10px; align-items:flex-start;'><span style='flex-shrink:0; font-size:1.1rem;'>✨</span><span style='line-height:1.6;'>{p}</span></div>" for p in contributions])
                        st.markdown(f"""
                        <div class="result-card">
                            {md_text}

                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="result-card">
                            <p style="color: var(--text-muted);">No contributions identified.</p>
                        </div>
                        """, unsafe_allow_html=True)

                with tab4:
                    st.markdown("""
                    <div class="section-header" style="margin-top: 0;">
                        <h2>Limitations & Future Work</h2>
                        <div class="section-rule"></div>
                    </div>
                    """, unsafe_allow_html=True)

                    limitations = parse_bullet_points(result.get("limitations", []))
                    if limitations:
                        md_text = "".join([f"<div style='display:flex; gap:10px; margin-bottom:10px; align-items:flex-start;'><span style='flex-shrink:0; font-size:1.1rem;'>⚠️</span><span style='line-height:1.6;'>{p}</span></div>" for p in limitations])
                        st.markdown(f"""
                        <div class="result-card" style="border-left: 3px solid var(--accent-warm);">
                            {md_text}

                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="result-card">
                            <p style="color: var(--text-muted);">No limitations identified.</p>
                        </div>
                        """, unsafe_allow_html=True)

                with tab5:
                    explanations = result.get("equation_explanations", [])
                    st.markdown(f"""
                    <div class="section-header" style="margin-top: 0;">
                        <h2>Mathematical Analysis</h2>
                        <div class="section-rule"></div>
                    </div>
                    <div style="font-family: var(--font-mono); font-size: 0.7rem;
                                text-transform: uppercase; letter-spacing: 0.1em;
                                color: var(--text-muted); margin-bottom: 1rem;">
                        [ {len(explanations)} equation{'s' if len(explanations) != 1 else ''} found ]
                    </div>
                    """, unsafe_allow_html=True)

                    if explanations:
                        for idx, eq in enumerate(explanations):
                            with st.expander(f"Equation {idx + 1}", expanded=(idx == 0)):
                                st.latex(eq.get("equation", ""))
                                st.markdown(f"""
                                <div class="eq-explanation">{eq.get("explanation", "")}</div>
                                """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="result-card">
                            <p style="color: var(--text-muted);">No complex equations were found or analyzed in this paper.</p>
                        </div>
                        """, unsafe_allow_html=True)

                with tab6:
                    st.markdown("""
                    <div class="section-header" style="margin-top: 0;">
                        <h2>Generated Journal Notes</h2>
                        <div class="section-rule"></div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.text_area(
                        "Your Study Notes",
                        result.get("journal_notes", "No journal notes generated."),
                        height=400,
                        label_visibility="collapsed"
                    )

                with tab7:
                    st.markdown("""
                    <div class="section-header" style="margin-top: 0;">
                        <h2>Generated Diagram</h2>
                        <div class="section-rule"></div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<p style='color: var(--text-muted); font-size: 0.9em;'>Click the button below to generate a visual diagram of the paper. This uses an additional AI call.</p>", unsafe_allow_html=True)
                    
                    if st.button("🔄 Generate Diagram", use_container_width=True):
                        with st.spinner("Generating diagram..."):
                            try:
                                from app.workflow.nodes import diagram_node
                                diagram_result = diagram_node(result)
                                diagram_xml = diagram_result.get("diagram_xml", "")
                            except Exception as diagram_err:
                                st.error(f"Diagram generation failed: {diagram_err}")
                                diagram_xml = ""
                        
                        if diagram_xml:
                            st.session_state["diagram_xml"] = diagram_xml
                        else:
                            st.warning("Could not generate diagram for this paper. Try again.")
                    
                    # Show diagram if it exists in session state
                    diagram_xml = st.session_state.get("diagram_xml", "")
                    if diagram_xml:
                        import urllib.parse
                        import streamlit.components.v1 as components
                        
                        st.markdown("<p style='color: var(--text-muted); font-size: 0.9em;'>Interactive Diagram Viewer — zoom, pan, and click elements!</p>", unsafe_allow_html=True)
                        
                        encoded_xml = urllib.parse.quote(diagram_xml)
                        viewer_url = f"https://viewer.diagrams.net/?nav=1&highlight=0000ff&edit=_blank&fit=1#R{encoded_xml}"
                        
                        html_code = f"""
                        <iframe frameborder="0" style="width:100%; height:600px; border:1px solid #ccc; border-radius: 8px; background:#fff;" src="{viewer_url}"></iframe>
                        """
                        components.html(html_code, height=650, scrolling=True)
                        
                        st.markdown("---")
                        st.download_button(label="Download .drawio file", data=diagram_xml, file_name="diagram.drawio", mime="application/xml", use_container_width=True)

            except Exception as e:
                status.update(label="Error occurred", state="error", expanded=True)
                st.error(f"An error occurred during analysis: {str(e)}")

# ── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    Research Paper Agent · Multi-Agent AI Analysis · <a href="https://github.com/EliteHiro" target="_blank" style="color: var(--text-light); text-decoration: none; transition: color 0.2s ease; display: inline-flex; align-items: center; gap: 0.35rem;"><svg height="14" width="14" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg> GitHub</a>
</div>
""", unsafe_allow_html=True)
