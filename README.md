# 🤖 Interactive RAG Resume Agent

A production-grade **Retrieval-Augmented Generation (RAG)** system that acts as my "digital twin." This agent parses my engineering resume and answers technical questions about my experience, projects, and skills in real-time, powered by Llama 3.1 and Groq's high-speed inference.

## 🚀 Architecture Overview
The system is built as a modular pipeline to ensure high accuracy and low latency:

1. **Ingestion:** Extracts text from PDF, cleans data, and splits it into semantic chunks.
2. **Storage:** Uses **ChromaDB** for persistent vector storage.
3. **Retrieval:** Employs **MMR (Maximal Marginal Relevance)** to ensure the retrieved context is both relevant and diverse.
4. **Generation:** Streams responses via **Groq (Llama-3.1-8b-instant)** for instantaneous user interaction.



## 🛠️ Tech Stack
* **Language:** Python 3.11+
* **LLM Inference:** Groq API (Llama 3.1)
* **Framework:** LangChain, Streamlit
* **Database:** ChromaDB
* **Embeddings:** HuggingFace (`bge-small-en-v1.5`)

## ⚙️ Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/choudharyprince890/rag_portfolio.git](https://github.com/choudharyprince890/rag_portfolio.git)
   cd rag_portfolio