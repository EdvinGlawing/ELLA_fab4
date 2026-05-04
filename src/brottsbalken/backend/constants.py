from pathlib import Path

BASE_PATH = Path(__file__).parents[1]

DATA_PATH = BASE_PATH / "data"
CLEAN_DATA_PATH = DATA_PATH / "clean_data" / "brottsbalken_clean.json"

VECTOR_DB_PATH = BASE_PATH / "knowledge_base" / "lancedb"
TABLE_NAME = "brottsbalken"

EMBEDDING_MODEL = "embed-multilingual-light-v3.0"

MODEL_SMALL="openrouter:openai/gpt-oss-20b:free"
MODEL_MEDIUM="google-gla:gemini-3-flash-preview"
MODEL_LARGE="openrouter:nvidia/nemotron-3-super-120b-a12b:free"
