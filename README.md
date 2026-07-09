# AI Portfolio Assistant - Project Context

## Project Overview

This project is a production-style Retrieval-Augmented Generation (RAG) application built to answer questions about Prince Choudhary's professional experience, projects, skills, education, and achievements.

The goal is not just to build a chatbot but to demonstrate production RAG architecture and best practices suitable for a Machine Learning / AI Engineer portfolio.

The application uses offline document ingestion, semantic retrieval, Groq LLM inference, conversation memory, query rewriting, and multiple guardrails.

---

# Technology Stack

### Language

* Python 3.11

### Framework

* Streamlit

### LLM

* Groq
* Model:
  llama-3.3-70b-versatile

### Embeddings

* HuggingFace Embeddings
* Loaded once during application startup

### Vector Database

* ChromaDB (Persistent)

### Retrieval

* Similarity Search

### Libraries

* LangChain
* LangChain Community
* LangChain Chroma
* LangChain Groq
* HuggingFace Embeddings

---

# High-Level Architecture

Offline Ingestion

Resume PDF
↓
About Me Markdown
↓
Preprocessing
↓
Text Splitting
↓
Embeddings
↓
Persist Chroma Database

Online Inference

User
↓
Streamlit
↓
Pipeline
↓
Prompt Injection Guard
↓
Conversation Memory
↓
Query Rewriter
↓
Retriever
↓
ChromaDB
↓
Retrieved Context
↓
Prompt Builder
↓
Groq LLM
↓
Hallucination Guard
↓
Response

---

# Project Structure

rag_portfolio/

app.py

scripts/
ingest.py

config/
prompts.py

data/

```
raw/
    resume.pdf
    about_me.md

processed/
    chroma_db/
```

src/

```
embeddings/
    embedding_model.py

ingestion/
    pdf_loader.py
    markdown_loader.py
    preprocessor.py
    text_splitter.py

database/
    vector_store.py

retrieval/
    retriever.py
    query_rewriter.py
    reranker.py

memory/
    conversation_memory.py

llm/
    llm_client.py

guardrails/
    prompt_injection.py
    hallucination.py

knowledge_graph/
    graph.py

pipeline.py
```

---

# Responsibilities of Each Module

## embeddings/

Loads the embedding model exactly once.

Exports:

embeddings_model

No other module initializes embeddings.

---

## ingestion/

Responsible only for document ingestion.

### pdf_loader.py

Loads resume.pdf.

Returns LangChain Documents.

### markdown_loader.py

Loads about_me.md.

Returns LangChain Documents.

### preprocessor.py

Performs lightweight text cleaning.

Responsibilities:

* Remove extra spaces
* Normalize blank lines
* Normalize whitespace

Nothing more.

### text_splitter.py

Uses RecursiveCharacterTextSplitter.

Returns chunked LangChain Documents.

---

## database/

### vector_store.py

Responsible only for ChromaDB.

Functions:

* Create vector database
* Persist embeddings
* Load existing database

It never loads PDFs or markdown files.

It only accepts Document chunks.

---

## scripts/

### ingest.py

Offline ingestion script.

Run only when source documents change.

Flow:

PDF
↓

Markdown
↓

Merge

↓

Preprocess

↓

Split

↓

Embeddings

↓

Persist Chroma

Command:

python scripts/ingest.py

The Streamlit application never performs ingestion.

---

## retrieval/

### retriever.py

Loads Chroma.

Performs similarity search.

Returns top-k Documents.

Nothing else.

### query_rewriter.py

Uses the LLM to rewrite follow-up questions into standalone questions before retrieval.

Example:

User:

Tell me about your RAG project.

User:

What guardrails did you implement?

Rewritten query:

What guardrails did Prince Choudhary implement in his RAG project?

This improves retrieval quality.

---

## llm/

### llm_client.py

Initializes Groq exactly once.

Exports:

generate_response(prompt)

No retrieval logic exists here.

---

## memory/

### conversation_memory.py

Stores recent conversation.

Responsibilities:

* Store user messages
* Store assistant messages
* Return conversation history

Memory is independent of retrieval.

---

## guardrails/

### prompt_injection.py

Runs before retrieval.

Detects prompt injection attacks.

Returns:

True → Safe

False → Unsafe

---

### hallucination.py

Runs after answer generation.

Checks whether the answer is supported by the retrieved context.

Returns:

True → Supported

False → Unsupported

---

## knowledge_graph/

(Currently planned)

Purpose:

Expand retrieval queries using relationships between projects, skills, technologies, and concepts.

Example:

RAG

↓

Conversation Memory

↓

Query Rewriting

↓

Prompt Injection

↓

Hallucination Detection

↓

Knowledge Graph Expansion

This improves retrieval quality.

---

## pipeline.py

Acts as the orchestrator.

It does NOT implement retrieval or LLM logic.

Pipeline Flow

User Question

↓

Prompt Injection Guard

↓

Conversation Memory

↓

Query Rewriter

↓

Retriever

↓

Retrieved Context

↓

Prompt Builder

↓

Groq

↓

Hallucination Guard

↓

Return Answer

---

# Design Principles

The project follows the Single Responsibility Principle.

Every module has exactly one responsibility.

Examples:

retriever.py

Only retrieves.

llm_client.py

Only communicates with Groq.

vector_store.py

Only manages ChromaDB.

pipeline.py

Only orchestrates components.

This architecture makes every module independently replaceable.

---

# Current Features

Implemented

✓ Offline ingestion

✓ Persistent ChromaDB

✓ HuggingFace Embeddings

✓ Similarity Search

✓ Groq Integration

✓ Streamlit Chat UI

✓ Conversation Memory

✓ Query Rewriting

✓ Prompt Injection Guard

✓ Hallucination Detection

---

# Planned Features

Knowledge Graph

Hybrid Retrieval

Cross Encoder Reranking

Metadata Filtering

Streaming Responses

Source Citation Display

Evaluation Metrics

Conversation Summarization

---

# Coding Guidelines

* Keep every module focused on a single responsibility.
* Never mix retrieval logic with LLM logic.
* Never create embeddings inside Streamlit.
* Never rebuild ChromaDB during application startup.
* All ingestion must happen through scripts/ingest.py.
* Prefer reusable utility functions over duplicated code.
* Use LangChain Document objects throughout the pipeline.
* Maintain clean, production-style folder organization.
* Future features should integrate into the existing architecture rather than introducing tightly coupled code.

Whenever extending this project, preserve the current modular architecture and avoid breaking the separation of concerns.
