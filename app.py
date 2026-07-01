import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env right away
load_dotenv()

# Import your functional pipeline components
from src.ingestion.pdf_loader import extract_text_from_pdf
from src.ingestion.preprocessor import clean_resume_text
from src.ingestion.text_splitter import split_text_into_chunks
from src.database.vector_store import save_chunks_to_db
from src.pipeline import answer_query_stream

# Configure the Streamlit page layout
st.set_page_config(page_title="Prince Choudhary | AI Resume Agent", page_icon="🤖", layout="centered")

# --- 1. Background Ingestion (From data/raw/) ---
@st.cache_resource(show_spinner="Indexing resume from data/raw/...")
def initialize_vector_store():
    """
    Checks for the raw resume PDF, extracts text, chunks it, 
    and saves it into the local database automatically on app launch.
    """
    raw_pdf_dir = "data/raw"
    
    # Look for any PDF in the data/raw folder
    if not os.path.exists(raw_pdf_dir):
        return {"status": "error", "message": "The directory 'data/raw' does not exist."}
        
    pdfs = [f for f in os.listdir(raw_pdf_dir) if f.endswith(".pdf")]
    if not pdfs:
        return {"status": "error", "message": "No PDF found in 'data/raw/'. Please drop your resume there."}
        
    target_pdf = os.path.join(raw_pdf_dir, pdfs[0])
    
    try:
        # Read binary bytes from local storage
        with open(target_pdf, "rb") as f:
            file_bytes = f.read()
            
        raw_text = extract_text_from_pdf(file_bytes)
        cleaned_text = clean_resume_text(raw_text)
        chunks = split_text_into_chunks(cleaned_text, chunk_size=400, chunk_overlap=40)
        
        if not chunks:
            return {"status": "error", "message": "Could not split text into chunks."}
            
        # Save chunks to your database
        save_chunks_to_db(chunks)
        return {"status": "success", "file_name": pdfs[0], "total_chunks": len(chunks)}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Auto-run ingestion silently on startup (cached so it runs only once)
db_status = initialize_vector_store()

# --- 2. Sidebar Interface ---
with st.sidebar:
    st.title("🤖 Resume Agent")
    st.caption("Powered by LangChain & Grok-4.3")
    st.markdown("---")
    
    if db_status["status"] == "success":
        st.success(f"🟢 Database Ready\n\nIndexed: `{db_status['file_name']}` ({db_status['total_chunks']} chunks)")
        
        # Recruiter download utility
        resume_path = os.path.join("data/raw", db_status["file_name"])
        with open(resume_path, "rb") as pdf_file:
            st.download_button(
                label="📄 Download Raw Resume PDF",
                data=pdf_file.read(),
                file_name=db_status["file_name"],
                mime="application/pdf"
            )
    else:
        st.error(f"🔴 DB Initialization Failed: {db_status['message']}")

    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# --- 3. Chat Session State Architecture ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
        "role": "assistant",
        "content": "🤖 Welcome! I'm Prince's AI assistant, trained on his projects, experience, and technical expertise. Ask me about Computer Vision, Machine Learning, Robotics, Python, or anything from his portfolio."
        }
    ]

    

# Display historical messages in current loop
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. Streamed Generation Loop ---
if prompt := st.chat_input("Ask a question about my experience..."):
    
    if db_status["status"] != "success":
        st.error("Cannot query the agent. Please make sure a resume PDF is in 'data/raw/'.")
    else:
        # User message display
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Assistant real-time streaming display
        with st.chat_message("assistant"):
            # Pass user query straight into our generator pipeline
            token_generator = answer_query_stream(prompt)
            full_response = st.write_stream(token_generator)
            
        # Commit response to memory history
        st.session_state.messages.append({"role": "assistant", "content": full_response})