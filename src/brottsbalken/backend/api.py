from fastapi import FastAPI

from brottsbalken.backend.agents import bot_answer
from brottsbalken.backend.data_models import Prompt, RagResponse

app = FastAPI()


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/rag/query")
async def query_brottsbalken(query: Prompt) -> RagResponse:
    result = await bot_answer(query.prompt)
    return result