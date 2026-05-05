"""
retriever.py

This file handles retrieval from LanceDB.

The retriever takes a user question, searches the LanceDB vector database,
and returns the most relevant Brottsbalken paragraphs.

Important:
- LanceDB stores vectors for the Brottsbalken paragraphs.
- When we search with a user question, LanceDB also embeds the question.
- That is why COHERE_API_KEY is needed here too, not only in vectorize.py.

Used by:
- agents.py
"""
import lancedb
from dotenv import load_dotenv

from brottsbalken.backend.constants import TABLE_NAME, VECTOR_DB_PATH

load_dotenv()

def retrieve_sources(query: str, k: int = 5) -> list[dict]:
    # Connect to the local LanceDB database
    db = lancedb.connect(VECTOR_DB_PATH)
    # Open the Brottsbalken table
    table = db.open_table(TABLE_NAME)

    # Semantic search
    # LanceDB embeds the query and compares it to the stored paragraph vectors
    results = (
        table.search(query)
        .limit(k)
        .to_list()
    )

    sources = []

    # Keep only the fields we want to send to the LLM and frontend
    for result in results:
        sources.append(
            {
                "chapter_number": result.get("chapter_number", ""),
                "title": result.get("title", ""),
                "paragraph": result.get("paragraph", ""),
                "text": result.get("text", ""),
            }
        )

    return sources