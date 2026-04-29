# Way of working

# Projektplan & Way of Working - Brottsbalken AI

Detta dokument beskriver hur gruppen samarbetar och fördelar ansvar under projektet i kursen AI Engineering och LLMOps. Syftet är att lösa ett verkligt problem med agil metodik.

## 1. Projektöversikt
Vi ska skapa en RAG-applikation (Retrieval-Augmented Generation) baserad på **Brottsbalken**. Applikationen ska låta användare ställa frågor om lagtexten och få svar med referenser.

## 2. Rollfördelning (4 personer)
* Vi kommer att mobcodea tilsammans.

## 3. Arbetstider och Möten
* **Kärntid:** Vi arbetar alla föreläsningsfria dagar mellan kl. **10:00 - till vi känner oss klara**. Under denna tid ska alla vara tillgängliga för samarbete och frågor.
* **Daily Standup:** Tre dagar i veckan hålls ett kort möte (max 10 min) där vi går igenom vad vi gjort, vad vi ska göra och om någon är blockerad.

## 4. Agilt arbetsflöde (Kanban)
* Vi använder GitHub Projects med en **Kanban-tavla**.
* Alla arbetsuppgifter ska definieras som **Issues** innan arbete påbörjas.
* När en uppgift påbörjas flyttas den till "In Progress" och tilldelas den ansvarige personen.

## 5. Versionshantering och Kodkvalitet
* **Branching:** Vi arbetar i funktions-branches. Ingen kod pushas direkt till `main`.
* **Pull Requests (PR):** All kod ska granskas av minst en annan teammedlem via en PR innan merge.
* **Commits:** Varje gruppmedlem ansvarar för att kontinuerligt committa sin kod för att visa individuell aktivitet.
* **DRY-principen:** Vi strävar efter välstrukturerad kod som undviker upprepningar.

## 6. Policy för AI-användning
* LLM:er får användas för kodgenerering av mindre delar, men inte hela moduler.
* **Viktigt:** All AI-genererad kod ska markeras med en kommentar: `// LLM Generated` eller motsvarande.
* Vi ska kunna förklara all kod vi inkluderar i projektet.

## 7. Inlämning och Presentation
* Projektet dokumenteras i en README med skärmdumpar.
* Alla deltar i den slutliga presentationen (10-15 min).
* Varje medlem skriver en individuell reflektion (0.5 - 1 sida).