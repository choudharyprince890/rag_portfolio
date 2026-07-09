"""
llm_client.py

Initializes the Groq LLM and provides a simple interface
for generating responses.

Responsibilities:
- Initialize Groq once
- Send prompts to the LLM
- Return the generated response

This module does NOT know about:
- Retrieval
- ChromaDB
- Prompt templates
- Conversation Memory
- Guardrails
"""

import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

# ---------------------------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------------------------

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables.")


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

MODEL_NAME = "llama-3.3-70b-versatile"
TEMPERATURE = 0.2
MAX_TOKENS = 1024


# ---------------------------------------------------------------------
# Initialize LLM (Only Once)
# ---------------------------------------------------------------------

print(f"Loading Groq model: {MODEL_NAME}...")

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=MODEL_NAME,
    temperature=TEMPERATURE,
    max_tokens=MAX_TOKENS,
)

print("Groq model loaded successfully.")


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def generate_response(prompt: str) -> str:
    """
    Generate a response from the Groq LLM.

    Args:
        prompt: The complete prompt to send to the model.

    Returns:
        Generated response as a string.
    """

    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    return response.content.strip()