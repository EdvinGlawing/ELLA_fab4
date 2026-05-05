"""
agents.py

This file contains the LLM/RAG logic.

The flow is:
1. Receive a user question.
2. Retrieve relevant Brottsbalken paragraphs from LanceDB.
3. Format those paragraphs into context.
4. Send the question + context to the LLM.
5. Return the answer together with the sources.

This is where the "generation" part of RAG happens.
"""
from dotenv import load_dotenv
from pydantic_ai import Agent

from brottsbalken.backend.constants import MODEL_MEDIUM
from brottsbalken.backend.data_models import RagResponse, Source, LLMAnswer
from brottsbalken.backend.retriever import retrieve_sources

load_dotenv()

# The LLM agent
law_agent = Agent(
    model=MODEL_MEDIUM,
    output_type=LLMAnswer,
    system_prompt="""
Du är en juridisk informationsassistent som svarar på frågor om Brottsbalken.

Regler:
- Svara endast baserat på den hämtade lagtexten.
- Om svaret inte finns i materialet, säg att du inte hittar stöd i Brottsbalken.
- Ge inte personlig juridisk rådgivning.
- Svara tydligt och kortfattat.
- Hänvisa alltid till kapitel och paragraf.
- Skriv på svenska.
- Sätt is_relevant till false om frågan inte handlar om Brottsbalken.
""",
)


def format_context(sources: list[dict]) -> str:
    """
    Convert retrieved source dictionaries into a text block for the LLM.

    The LLM receives this as "Relevant lagtext" and should base its answer on it.
    """
    return "\n---\n".join(
        f"""Källa: Brottsbalken, {source["chapter_number"]} {source["paragraph"]}, {source["title"]}
Text:
{source["text"]}"""
        for source in sources
    )


async def bot_answer(question: str) -> RagResponse:
    # Retrieve relevant paragraphs from LanceDB
    sources_raw = retrieve_sources(question, k=3)
    # Format retrieved paragraphs as context for the LLM
    context = format_context(sources_raw)

    # Create the user prompt for the LLM
    prompt = f"""
Fråga:
{question}

Relevant lagtext:
{context}

Svara på frågan baserat på lagtexten ovan.
"""

    # Ask the LLM to answer based on the retrieved context
    result = await law_agent.run(prompt)

    # Convert raw source dictionaries into Pydantic Source objects
    sources = [
        Source(
            chapter_number=source["chapter_number"],
            title=source["title"],
            paragraph=source["paragraph"],
            text=source["text"],
        )
        for source in sources_raw
    ]

    # Return answer and sources to the API
    return RagResponse(
        answer=result.output.answer,
        sources=sources if result.output.is_relevant else None,
    )