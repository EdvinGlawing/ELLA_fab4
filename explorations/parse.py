"""
Brottsbalken Parser – Markdown → JSON
======================================
Konverterar brottsbalken.md (hämtad från riksdagen.se) till strukturerad JSON
lämplig för chattbotar, RAG-system eller annan juridisk applikation.

Användning:
    python parse_brottsbalken.py
    python parse_brottsbalken.py --input brottsbalken.md --output brottsbalken.json

Output-struktur:
    {
      "titel": "Brottsbalk (1962:700)",
      "metadata": { "sfs_nr", "departement", "utfardad", "andrad" },
      "avdelningar": ["FÖRSTA AVDELNINGEN", ...],
      "kapitel": [
        {
          "chapter_number": 3,
          "title": "3 kap. Om brott mot liv och hälsa",
          "subheadings": [...],
          "paragraphs": [
            {
              "paragraph": "1 §",
              "text": "Den som berövar annan livet...",
              "law_references": ["_Lag (2019:805)_."],
              "repealed": false
            }
          ]
        }
      ],
      "total_kapitel": 38,
      "total_paragrafer": 556
    }
"""

import re
import json
import argparse
from pathlib import Path


# ── 1. Läs fil ────────────────────────────────────────────────────────────────

def read_file(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


# ── 2. Rensa bort navigation, sidhuvud och sidfot ────────────────────────────

def strip_boilerplate(raw: str) -> str:
    """
    Behåller bara lagtexten – allt från '# Brottsbalk (1962:700)'
    till den avslutande 'Svensk författningssamling'-footern.
    """
    start_marker = "# Brottsbalk (1962:700)"
    end_marker   = "## Svensk författningssamling"

    start = raw.find(start_marker)
    if start == -1:
        raise ValueError("Hittade inte startmarkören '# Brottsbalk (1962:700)' i filen.")

    # Använd den SISTA förekomsten av end_marker (footern, inte den i toppen)
    end = raw.rfind(end_marker)
    if end == -1 or end <= start:
        end = len(raw)

    return raw[start:end].strip()


# ── 3. Rensa kod-block-formaterade tabeller (kap 2) ──────────────────────────

def clean_code_blocks(text: str) -> str:
    """
    Kapitel 2 har en behörighetstabell formaterad som ASCII-kodblock.
    Kollapsar ``` ... ``` till ren text.
    """
    text = re.sub(r'```\n(.*?)\n```', lambda m: m.group(1), text, flags=re.DOTALL)
    # Normalisera blankrader
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text


# ── 4. Extrahera metadata ─────────────────────────────────────────────────────

def extract_metadata(content: str) -> dict:
    patterns = {
        "sfs_nr":      r'\*\*SFS nr\*\*:\s*\n(.+)',
        "departement": r'\*\*Departement/myndighet\*\*:\s*\n(.+)',
        "utfardad":    r'\*\*Utfärdad\*\*:\s*\n(.+)',
        "andrad":      r'\*\*Ändrad\*\*:\s*\n(.+)',
    }
    meta = {}
    for key, pattern in patterns.items():
        m = re.search(pattern, content)
        meta[key] = m.group(1).strip() if m else None
    return meta


# ── 5. Hitta avdelningar ──────────────────────────────────────────────────────

def extract_avdelningar(content: str) -> list[str]:
    return re.findall(
        r'^## ((?:FÖRSTA|ANDRA|TREDJE) AVDELNINGEN)',
        content, re.MULTILINE
    )


# ── 6. Rensa paragraftext ─────────────────────────────────────────────────────

def clean_paragraph_text(text: str) -> str:
    # Fixa numrerade listor: "1\. " → "1. "
    text = re.sub(r'(\d+)\\\. ', r'\1. ', text)
    # Ta bort escaped understreck
    text = re.sub(r'\\_', '_', text)
    # Normalisera blankrader
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


# ── 7. Parsa kapitel och paragrafer ──────────────────────────────────────────

def parse_chapters(content: str) -> list[dict]:
    """
    Delar upp innehållet i kapitel (### N kap. ...) och extraherar
    varje paragraf (**N §** text) inom respektive kapitel.
    """
    chapter_re  = re.compile(r'^### (.+)', re.MULTILINE)
    chapter_matches = list(chapter_re.finditer(content))

    chapters = []

    for i, ch_match in enumerate(chapter_matches):
        ch_title = ch_match.group(1).strip()
        ch_start = ch_match.start()
        ch_end   = chapter_matches[i + 1].start() if i + 1 < len(chapter_matches) else len(content)
        ch_text  = content[ch_start:ch_end]

        # Kapitelnummer
        num_match = re.match(r'(\d+)\s+kap\.', ch_title)
        ch_num = int(num_match.group(1)) if num_match else None

        # Underrubriker (####)
        subheadings = re.findall(r'^#### (.+)', ch_text, re.MULTILINE)

        # Paragrafer: **N §**  eller  **N a §**  osv.
        para_re = re.compile(
            r'^\*\*(\d+\s*[a-z]?\s*§)\*\*\s+(.*?)(?=^\*\*\d+|\Z)',
            re.MULTILINE | re.DOTALL
        )

        paragraphs = []
        for p in para_re.finditer(ch_text):
            para_num  = p.group(1).strip()
            para_raw  = p.group(2).strip()

            # Plocka ut lagnummer-hänvisningar
            law_refs  = re.findall(r'_Lag \([^)]+\)_\.?', para_raw)

            # Ta bort lagnummer-hänvisningarna från brödtexten
            para_text = re.sub(r'\s*_Lag \([^)]+\)_\.?', '', para_raw)
            para_text = clean_paragraph_text(para_text)

            # Markera upphävda paragrafer
            repealed = bool(re.search(
                r'upphävts|upphört att gälla|Har upphört',
                para_text, re.IGNORECASE
            ))

            if not para_text:
                continue

            paragraphs.append({
                "paragraph":      para_num,
                "text":           para_text,
                "law_references": law_refs,
                "repealed":       repealed,
            })

        # Hoppa över pseudo-kapitel (t.ex. innehållsförteckning, övergångsbestämmelser)
        if ch_num is None:
            continue

        chapters.append({
            "chapter_number": ch_num,
            "title":          ch_title,
            "subheadings":    subheadings,
            "paragraphs":     paragraphs,
        })

    return chapters


# ── 8. Bygg slutlig JSON ──────────────────────────────────────────────────────

def build_json(content: str) -> dict:
    meta        = extract_metadata(content)
    avdelningar = extract_avdelningar(content)
    chapters    = parse_chapters(content)

    total_paragrafer = sum(len(c["paragraphs"]) for c in chapters)

    return {
        "titel":            "Brottsbalk (1962:700)",
        "metadata":         meta,
        "avdelningar":      avdelningar,
        "kapitel":          chapters,
        "total_kapitel":    len(chapters),
        "total_paragrafer": total_paragrafer,
    }


# ── 9. Skriv JSON ─────────────────────────────────────────────────────────────

def write_json(data: dict, output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── 10. Rapportera resultat ───────────────────────────────────────────────────

def print_summary(data: dict) -> None:
    print(f"\n✅ Klar!")
    print(f"   Titel:       {data['titel']}")
    print(f"   SFS:         {data['metadata']['sfs_nr']}")
    print(f"   Ändrad:      {data['metadata']['andrad']}")
    print(f"   Kapitel:     {data['total_kapitel']}")
    print(f"   Paragrafer:  {data['total_paragrafer']}")
    print()
    print("   Kapitel:")
    for kap in data["kapitel"]:
        print(f"     {kap['title']} — {len(kap['paragraphs'])} §§")


# ── Ingångspunkt ──────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Konverterar brottsbalken.md till strukturerad JSON."
    )
    parser.add_argument(
        "--input",  "-i",
        default="brottsbalken.md",
        help="Sökväg till markdown-filen (default: brottsbalken.md)",
    )
    parser.add_argument(
        "--output", "-o",
        default="brottsbalken.json",
        help="Sökväg för output-JSON (default: brottsbalken.json)",
    )
    args = parser.parse_args()

    if not Path(args.input).exists():
        raise SystemExit(f"❌ Filen '{args.input}' hittades inte.")

    print(f"📖 Läser {args.input}...")
    raw     = read_file(args.input)

    print("🔧 Rensar bort navigation och sidfot...")
    content = strip_boilerplate(raw)
    content = clean_code_blocks(content)

    print("🔍 Parsar kapitel och paragrafer...")
    data = build_json(content)

    print(f"💾 Skriver {args.output}...")
    write_json(data, args.output)

    print_summary(data)


if __name__ == "__main__":
    main()