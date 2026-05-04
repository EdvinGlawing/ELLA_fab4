from dotenv import load_dotenv
from pydantic_ai import Agent

from brottsbalken.backend.constants import MODEL_MEDIUM
from brottsbalken.backend.data_models import RagResponse, Source
from brottsbalken.backend.retriever import retrieve_sources

load_dotenv()


law_agent = Agent(
    model=MODEL_MEDIUM,
    output_type=str,
    system_prompt="""
Du är en juridisk informationsassistent som svarar på frågor om Brottsbalken.

Regler:
- Svara endast baserat på den hämtade lagtexten.
- Om svaret inte finns i materialet, säg att du inte hittar stöd i Brottsbalken.
- Ge inte personlig juridisk rådgivning.
- Svara tydligt och kortfattat.
- Hänvisa alltid till kapitel och paragraf.
- Skriv på svenska.
""",
)


def format_context(sources: list[dict]) -> str:
    return "\n---\n".join(
        f"""Källa: Brottsbalken, {source["chapter_number"]} {source["paragraph"]}, {source["title"]}
Text:
{source["text"]}"""
        for source in sources
    )


async def bot_answer(question: str) -> RagResponse:
    sources_raw = retrieve_sources(question, k=3)
    context = format_context(sources_raw)

    prompt = f"""
Fråga:
{question}

Relevant lagtext:
{context}

Svara på frågan baserat på lagtexten ovan.
"""

    result = await law_agent.run(prompt)

    sources = [
        Source(
            chapter_number=source["chapter_number"],
            title=source["title"],
            paragraph=source["paragraph"],
            text=source["text"],
        )
        for source in sources_raw
    ]

    return RagResponse(
        answer=result.output,
        sources=sources,
    )