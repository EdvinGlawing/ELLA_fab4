# How to Run the Project

This document explains how to run the project.

---

## 1. First-time setup

From the project root, run:

```bash
uv sync
```

This creates or updates the virtual environment and installs dependencies from the workspace.

Create a `.env` file in the project root:

```env
COHERE_API_KEY=your_cohere_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
VOICE_ID=
```

Depending on the LLM provider, additional API keys may be needed later.


After that is done, from src/brottsbalken/scripts, run:

```bash
uv run vectorize.py
```
This is needed for everything to run smoothly.

---

## 2. How to Run backend

From src, run:
```bash
uv run uvicorn brottsbalken.backend.api:app --reload
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

## 3. How to Run frontend

From src/brottsbalken/frontend, run:
```bash
uv run streamlit run app.py
```

---

## 4. How to Run monitoring/mlflow

From src/brottsbalken/monitoring, run:
```bash
uv run mlflow ui
```

---

## How to run the scripts and what they do

The scripts are located here:

```text
src/brottsbalken/scripts/
```

They are used to prepare the data and vector database.

### Parse Brottsbalken markdown
From src/brottsbalken/scripts, run:
```bash
uv run parse.py
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
From src/brottsbalken/scripts, run:
```bash
uv run vectorize.py
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

The script uses `mode="overwrite"`, so it is safe to run multiple times. It recreates the table instead of adding duplicate rows.

---



