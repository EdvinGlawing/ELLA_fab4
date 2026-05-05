"""
constants.py

This file contains shared backend settings.

We keep paths and model names here so we do not hardcode them in many files.
If we need to change the vector database path, table name, embedding model, or LLM model,
we only need to update it here.

Used by:
- vectorize.py
- retriever.py
- agents.py
"""
from pathlib import Path

# BASE_PATH points to src/brottsbalken/
BASE_PATH = Path(__file__).parents[1]

# Path to the data folder
DATA_PATH = BASE_PATH / "data"
# Path to the cleaned Brottsbalken JSON file used for vectorization
CLEAN_DATA_PATH = DATA_PATH / "clean_data" / "brottsbalken_clean.json"

# Path to the LanceDB vector database
VECTOR_DB_PATH = BASE_PATH / "knowledge_base" / "lancedb"
# Name of the LanceDB table
TABLE_NAME = "brottsbalken"

EMBEDDING_MODEL = "embed-multilingual-light-v3.0"

MODEL_SMALL="openrouter:openai/gpt-oss-20b:free"
MODEL_MEDIUM="google-gla:gemini-3-flash-preview"
MODEL_LARGE="openrouter:nvidia/nemotron-3-super-120b-a12b:free"
