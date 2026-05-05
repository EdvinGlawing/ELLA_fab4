
"""
api.py

This file contains the FastAPI application.

The API is the bridge between the frontend and the RAG backend.

Frontend/user sends a question:
    POST /rag/query

Backend returns:
    - answer
    - sources used for the answer
"""

from fastapi import FastAPI

from brottsbalken.backend.agents import bot_answer
from brottsbalken.backend.data_models import Prompt, RagResponse

# Create the FastAPI app
app = FastAPI()


@app.get("/health")
async def health_check():
    """
    Simple health check endpoint.

    Used to check if the backend is running.
    """
    return {"status": "ok"}


@app.post("/rag/query")
async def query_brottsbalken(query: Prompt) -> RagResponse:
    """
    Main RAG endpoint.

    Request example:
    {
        "prompt": "Vad säger Brottsbalken om mord?"
    }

    Response:
    {
        "answer": "...",
        "sources": [...]
    }
    """
    # Send the user's prompt to the RAG agent
    result = await bot_answer(query.prompt)
    # Return answer + sources
    return result