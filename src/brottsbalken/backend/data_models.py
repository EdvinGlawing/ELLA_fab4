"""
data_models.py

This file contains the Pydantic models used by the FastAPI backend.

Pydantic models define the structure of data that comes into and goes out of the API.

Prompt:
- The request body sent from the frontend/user to the backend.

Source:
- One retrieved paragraph from Brottsbalken.
- Used to show which chapter and paragraph the answer is based on.

RagResponse:
- The response returned from the backend.
- Contains the generated answer and the retrieved legal sources.
"""
from pydantic import BaseModel, Field


class Prompt(BaseModel):
    # The user's question, for example:
    # "Vad säger Brottsbalken om mord?"
    prompt: str = Field(description="User question about Brottsbalken")


class Source(BaseModel):
    # Metadata and text for one retrieved Brottsbalken paragraph
    chapter_number: str
    title: str
    paragraph: str
    text: str

class LLMAnswer(BaseModel):
    answer: str  # Svaret från LLM:en
    is_relevant: bool  # LLM:en kryssar i om frågan handlade om Brottsbalken eller inte

class RagResponse(BaseModel):
    # The LLM-generated answer
    answer: str = Field(description="Answer based on retrieved Brottsbalken context")
    # The legal sources used as context for the answer
    sources: list[Source] | None = Field(
        default_factory=list,
        description="Retrieved legal sources from Brottsbalken",
    )