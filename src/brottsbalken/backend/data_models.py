from pydantic import BaseModel, Field


class Prompt(BaseModel):
    prompt: str = Field(description="User question about Brottsbalken")


class Source(BaseModel):
    chapter_number: str
    title: str
    paragraph: str
    text: str


class RagResponse(BaseModel):
    answer: str = Field(description="Answer based on retrieved Brottsbalken context")
    sources: list[Source] = Field(
        default_factory=list,
        description="Retrieved legal sources from Brottsbalken",
    )