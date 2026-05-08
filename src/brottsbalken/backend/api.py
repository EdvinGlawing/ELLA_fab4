
"""
api.py

This file contains the FastAPI application.

The API is the bridge between the frontend and the RAG backend.

Frontend/user sends a question:
    POST /rag/query

Backend returns:
    - answer
    - sources used for theu answer
"""

from contextlib import asynccontextmanager

import mlflow
from fastapi import FastAPI
from contextlib import asynccontextmanager
from middleware import logging_middleware
from constants import MONITORING_PATH
from data_models import Prompt, RagResponse

mlflow.set_tracking_uri(f"sqlite:///{MONITORING_PATH / 'mlflow.db'}")
mlflow.set_experiment("brottsbalken")
mlflow.pydantic_ai.autolog()
from agents import bot_answer, law_agent


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs when the FastAPI app starts and stops.

    We store the law agent in app.state so the app has access to it during runtime.
    MLflow autologging tracks PydanticAI calls.
    """

    app.state.law_agent = law_agent

    yield

    #mlflow.end_run()


app = FastAPI(
    title="Brottsbalken",
    lifespan=lifespan,
)

logging_middleware(app)

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