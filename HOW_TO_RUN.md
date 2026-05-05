# How to Run the Project

This document explains how to run the project, how the uv workspace works, how to recreate LanceDB, and how to add packages.

---

## 1. Project structure

The project uses a `src/` structure and uv workspaces.

```text
ELLA_FAB4/
├── pyproject.toml
├── uv.lock
├── README.md
├── HOW_TO_RUN.md
├── .env
├── explorations/
└── src/
    └── brottsbalken/
        ├── backend/
        │   ├── pyproject.toml
        │   ├── api.py
        │   ├── agents.py
        │   ├── constants.py
        │   ├── data_models.py
        │   └── retriever.py
        ├── frontend/
        │   ├── pyproject.toml
        │   └── app.py
        ├── scripts/
        │   ├── parse.py
        │   └── vectorize.py
        ├── data/
        └── knowledge_base/
```

Main folders:

```text
backend/        FastAPI backend and RAG logic
frontend/       Streamlit frontend
scripts/        Data setup scripts
data/           Brottsbalken source and cleaned data
knowledge_base/ LanceDB vector database
explorations/   Notebooks and experiments
```

---

## 2. First-time setup

From the project root, run:

```bash
uv sync
```

This creates or updates the virtual environment and installs dependencies from the workspace.

Create a `.env` file in the project root:

```env
COHERE_API_KEY=your_cohere_api_key_here
```

Depending on the LLM provider, additional API keys may be needed later.

---

## 3. How the workspace works

The root `pyproject.toml` controls the workspace.

It lists the workspace members:

```toml
[tool.uv.workspace]
members = [
    "src/brottsbalken/backend",
    "src/brottsbalken/frontend",
]
```

This means backend and frontend are separate uv projects inside the same repository.

The project has one shared lockfile:

```text
uv.lock
```

---

## 4. What each `pyproject.toml` does

### Root `pyproject.toml`

The root `pyproject.toml` is the workspace controller.

It usually contains workspace-level dependencies such as:

```toml
dependencies = [
    "ipykernel",
    "mlflow",
]
```

It also has:

```toml
[tool.uv]
package = false
```

This means the root project is not an installable Python package. It only manages the workspace.

### Backend `pyproject.toml`

Located here:

```text
src/brottsbalken/backend/pyproject.toml
```

This contains backend dependencies, for example:

```text
fastapi
uvicorn
lancedb
pandas
cohere
pydantic-ai
python-dotenv
```

Use the backend package when running the API or scripts that need RAG dependencies.

### Frontend `pyproject.toml`

Located here:

```text
src/brottsbalken/frontend/pyproject.toml
```

This contains frontend dependencies, for example:

```text
streamlit
httpx
python-dotenv
```

The frontend should not need LanceDB, Cohere, or embedding dependencies. It should call the backend API.

---

## 5. Why we use `PYTHONPATH=src`

Our Python package is inside:

```text
src/brottsbalken/
```

So we run commands with:

```bash
PYTHONPATH=src
```

This tells Python where to find the `brottsbalken` package.

Example import:

```python
from brottsbalken.backend.retriever import retrieve_sources
```

---

## 6. How to run the backend

From the project root:

```bash
PYTHONPATH=src uv run --package brottsbalken-backend uvicorn brottsbalken.backend.api:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

Test the endpoint:

```text
POST /rag/query
```

Example request:

```json
{
  "prompt": "Vad säger Brottsbalken om mord?"
}
```

---

## 7. How to run the scripts

The scripts are located here:

```text
src/brottsbalken/scripts/
```

They are used to prepare the data and vector database.

### Parse Brottsbalken markdown

```bash
PYTHONPATH=src uv run --package brottsbalken-backend python -m brottsbalken.scripts.parse
```

This reads:

```text
src/brottsbalken/data/raw_data/brottsbalken.md
```

and creates or updates:

```text
src/brottsbalken/data/raw_data/brottsbalken.json
```

### Create LanceDB vector database

```bash
PYTHONPATH=src uv run --package brottsbalken-backend python -m brottsbalken.scripts.vectorize
```

This reads:

```text
src/brottsbalken/data/clean_data/brottsbalken_clean.json
```

and creates:

```text
src/brottsbalken/knowledge_base/lancedb/brottsbalken.lance/
```

Expected output:

```text
556 paragrafer indexerade i tabellen 'brottsbalken'.
```

---

## 8. How to recreate LanceDB from scratch

Delete the generated LanceDB table:

```bash
rm -rf src/brottsbalken/knowledge_base/lancedb/brottsbalken.lance
```

Then recreate it:

```bash
PYTHONPATH=src uv run --package brottsbalken-backend python -m brottsbalken.scripts.vectorize
```

The script uses `mode="overwrite"`, so it is safe to run multiple times. It recreates the table instead of adding duplicate rows.

---

## 9. How to add packages later

Always run these commands from the project root.

### Add a backend package

```bash
uv add --package brottsbalken-backend package-name
```

Example:

```bash
uv add --package brottsbalken-backend openai
```

This updates:

```text
src/brottsbalken/backend/pyproject.toml
uv.lock
```

### Add a frontend package

```bash
uv add --package brottsbalken-frontend package-name
```

Example:

```bash
uv add --package brottsbalken-frontend plotly
```

This updates:

```text
src/brottsbalken/frontend/pyproject.toml
uv.lock
```

### Add a root/notebook package

```bash
uv add package-name
```

Example:

```bash
uv add matplotlib
```

Use this for notebook or root-level tooling only.

---

## 10. Current backend flow

The backend RAG flow is:

```text
User question
→ FastAPI endpoint /rag/query
→ bot_answer()
→ retrieve_sources()
→ LanceDB search
→ retrieved Brottsbalken paragraphs
→ LLM answer
→ response with answer + sources
```

Important backend files:

```text
api.py          FastAPI endpoints
agents.py      LLM prompt and response generation
retriever.py   LanceDB semantic search
data_models.py Request and response models
constants.py   Paths, table name, and model settings
```

---

