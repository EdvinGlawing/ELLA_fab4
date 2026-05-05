# ELLA_fab4
LLMops school project

# ELLA_fab4 - Brottsbalken Chatbot
Detta är ett AI Engineering / LLMOps-projekt där vi bygger en chatbot för **Brottsbalken (1962:700)**.
Målet är att göra juridisk information mer tillgänglig genom en RAG-baserad lösning med källnära svar.

## Projektidé
Vi bygger en chatbot där användaren kan ställa frågor om Brottsbalken och få:
- ett begripligt svar
- hänvisning till relevanta kapitel/paragrafer
- möjlighet att följa upp med nya frågor i samma kontext
Projektet är en del av kursen i AI Engineering och LLMOps och utvecklas med agilt arbetssätt i grupp.

## Status just nu
Projektet är under aktiv utveckling. Följande delar är klara hittills:
- [x] Datainsamling och rådata i markdown/json
- [x] Parser för att strukturera lagtext
- [x] Clean dataset på paragrafnivå
- [x] Embeddings + indexering i LanceDB
- [x] Projektstruktur i `src/`
- [x] Way of Working-dokument
Pågående / kvar:
- [ ] FastAPI-backend för frågeendpoint
- [ ] Chat/agentlogik ovanpå retrieval
- [ ] Frontend
- [ ] Dockerisering
- [ ] README med screenshots + demoflöde
- [ ] (Bonus) MLflow för prompt-versionering och utvärdering
- [ ] (Bonus) Deployment till Azure

## Arkitektur (nuvarande + planerad)
1. **Rådata**: Brottsbalken i markdown/json
2. **Parsing**: extraherar metadata, kapitel, paragrafer
3. **Datastädning**: normaliserad paragrafdata
4. **Embedding**: vektorrepresentation av text
5. **Vector DB**: lagring och semantisk sökning i LanceDB
6. **(Planerad) API + LLM**: FastAPI endpoint för chatbot-svar
7. **(Planerad) Frontend**: användargränssnitt för chat

## Repo-struktur
```text
.
├── README.md
├── pyproject.toml
├── way_of_working.md
├── data/
└── src/
    └── brottsbalken/
        ├── backend/
        │   ├── api.py
        │   └── agent.py
        ├── data/
        │   ├── raw_data/
        │   └── clean_data/
        ├── scripts/
        │   ├── parse.py
        │   └── vectorize.py
        ├── knowledge_base/
        │   └── lancedb/
        ├── explorations/
        └── utils/
            └── constants.py
Dataöversikt
Nuvarande dataset innehåller:

38 kapitel
556 paragrafer
Tech stack
Python 3.12+
FastAPI (backend, planerad integration)
LanceDB
Pandas
Pydantic / Pydantic-AI
Streamlit (möjlig frontend/prototyp)
MLflow (bonusspår)
Kom igång lokalt (work in progress)
uv sync
python src/brottsbalken/scripts/parse.py
python src/brottsbalken/scripts/vectorize.py
Körinstruktioner uppdateras när backend/frontend är integrerade.

Arbetssätt (kurskrav)
Vi följer kursens gemensamma krav:

branches + pull requests
kanban + issues
gemensamt repo per grupp
way of working-dokument
presentation med demo
Se way_of_working.md för detaljer.

Demo (lägg till senare)

 Screenshot: startsida

 Screenshot: fråga + svar

 Screenshot: källa/referenser

 Kort GIF/video av chatflöde
Begränsningar / disclaimer
Denna chatbot är ett utbildningsprojekt och ersätter inte juridisk rådgivning. Modellen kan göra fel; svar bör verifieras mot original lagtext.

Team
(Lägg till namn, roller och ansvar)

Individuell reflektion
(Länkar eller sektioner för varje gruppmedlems reflektion)