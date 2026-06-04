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

# Custom CSS for a premium, dynamic look
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #0E1117;
    }
    /* Hide Streamlit header and footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Hero Section */
    .hero {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .hero h1 {
        font-size: 3.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .hero p {
        font-size: 1.2rem;
        color: #A0AEC0;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3rem;
        background: linear-gradient(90deg, #4ECDC4, #556270);
        color: white;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(78, 205, 196, 0.4);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1E1E1E;
        border-radius: 8px 8px 0px 0px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2D2D2D;
        border-bottom: 2px solid #4ECDC4;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <h1>Research Paper Agent</h1>
    <p>Upload any scientific paper and let advanced AI extract summaries, contributions, limitations, and mathematically decode complex equations.</p>
</div>
""", unsafe_allow_html=True)

# Main UI
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    uploaded_file = st.file_uploader("Drop your PDF research paper here", type=["pdf"])

if uploaded_file is not None:
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn2:
        analyze_clicked = st.button("🚀 Analyze Paper Now")

    if analyze_clicked:
        with st.status("🧠 AI is analyzing the paper...", expanded=True) as status:
            try:
                st.write("📥 Loading PDF document...")
                # Save the uploaded file temporarily so PyMuPDF can read it
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name

                st.write("🔍 Extracting text and parsing sections...")
                parser = PDFParser()
                text = parser.extract_text(tmp_path)
                
                st.write("⚡ Running multi-agent analysis (Summary, Math, Contributions)...")
                service = PaperAnalysisService()
                result = service.analyze(text)

                status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
                
                # Cleanup the temporary file
                os.remove(tmp_path)

                st.markdown("<br>", unsafe_allow_html=True)
                
                # Display Results in beautiful Tabs
                tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                    "📑 Summary", 
                    "🔑 Key Points", 
                    "💡 Contributions", 
                    "⚠️ Limitations", 
                    "🧮 Equations", 
                    "📝 Notes"
                ])
                
                with tab1:
                    st.markdown("### 📑 Paper Summary")
                    st.info(result.get("summary", "No summary generated."))
                    
                with tab2:
                    st.markdown("### 🔑 Key Findings")
                    for point in result.get("key_points", []):
                        st.markdown(f"**—** {point}")
                        
                with tab3:
                    st.markdown("### 💡 Novel Contributions")
                    for cont in result.get("contributions", []):
                        st.success(f"{cont}")
                        
                with tab4:
                    st.markdown("### ⚠️ Limitations & Future Work")
                    for lim in result.get("limitations", []):
                        st.warning(f"{lim}")
                        
                with tab5:
                    explanations = result.get("equation_explanations", [])
                    st.markdown(f"### 🧮 Mathematical Analysis ({len(explanations)} equations found)")
                    
                    if explanations:
                        for idx, eq in enumerate(explanations):
                            with st.expander(f"Equation {idx + 1}", expanded=(idx==0)):
                                st.latex(eq.get("equation", ""))
                                st.markdown("---")
                                st.write(eq.get("explanation", ""))
                    else:
                        st.info("No complex equations were found or analyzed in this paper.")
                        
                with tab6:
                    st.markdown("### 📝 Generated Journal Notes")
                    st.text_area("Your Study Notes", result.get("journal_notes", "No journal notes generated."), height=400)

            except Exception as e:
                status.update(label="❌ Error occurred", state="error", expanded=True)
                st.error(f"An error occurred during analysis: {str(e)}")
