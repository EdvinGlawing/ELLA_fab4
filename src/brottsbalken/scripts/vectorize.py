import json
from pathlib import Path

import lancedb
import pandas as pd
from dotenv import load_dotenv
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector

from brottsbalken.backend.constants import (
    CLEAN_DATA_PATH,
    VECTOR_DB_PATH,
    TABLE_NAME,
    EMBEDDING_MODEL,
)

load_dotenv()

embedding_model = get_registry().get("cohere").create(name=EMBEDDING_MODEL)


class ParagraphModel(LanceModel):
    embed_text: str = embedding_model.SourceField()
    vector: Vector(embedding_model.ndims()) = embedding_model.VectorField()

    chapter_number: str
    title: str
    law_references: list[str]
    paragraph: str
    text: str


def load_data(path: Path) -> pd.DataFrame:
    with open(path, encoding="utf-8") as file:
        data = json.load(file)

    return pd.DataFrame(data)


def build_embed_text(row: pd.Series) -> str:
    parts = [
        f"{row['chapter_number']} {row['title']}",
        row["paragraph"],
        row["text"],
        f"{row['law_references']}",
    ]

    return " | ".join(str(part) for part in parts if part)


def vectorize() -> None:
    df = load_data(CLEAN_DATA_PATH)
    df["embed_text"] = df.apply(build_embed_text, axis=1)

    db = lancedb.connect(VECTOR_DB_PATH)

    table = db.create_table(
        TABLE_NAME,
        schema=ParagraphModel,
        mode="overwrite",
    )

    table.add(
        df[
            [
                "embed_text",
                "chapter_number",
                "title",
                "law_references",
                "paragraph",
                "text",
            ]
        ].to_dict("records")
    )

    print(f"{table.count_rows()} paragrafer indexerade i tabellen '{TABLE_NAME}'.")


if __name__ == "__main__":
    vectorize()