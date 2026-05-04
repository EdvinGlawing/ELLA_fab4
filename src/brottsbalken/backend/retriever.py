import lancedb
from dotenv import load_dotenv

from brottsbalken.backend.constants import TABLE_NAME, VECTOR_DB_PATH

load_dotenv()

def retrieve_sources(query: str, k: int = 5) -> list[dict]:
    db = lancedb.connect(VECTOR_DB_PATH)
    table = db.open_table(TABLE_NAME)

    results = (
        table.search(query)
        .limit(k)
        .to_list()
    )

    sources = []

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