import re
import json

with open("brottsbalken.txt", "r", encoding="utf-8") as f:
    text = f.read()

def parse_brottsbalken(text):
    result = []
    current_avdelning = None
    current_kapitel = None
    current_paragraf = None

    lines = text.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Avdelning: "FÖRSTA AVDELNINGEN", "ANDRA AVDELNINGEN" etc.
        if re.match(r'^[A-ZÅÄÖ]+ AVDELNINGEN$', line):
            current_avdelning = {
                "avdelning": line,
                "rubrik": "",
                "kapitel": []
            }
            result.append(current_avdelning)
            current_kapitel = None
            current_paragraf = None

        # Rubrik under avdelning (raden direkt efter avdelningsrubriken)
        elif current_avdelning and current_avdelning["rubrik"] == "" and line and not re.match(r'^\d+ kap\.', line):
            current_avdelning["rubrik"] = line

        # Kapitel: "1 kap. Om brott och brottspåföljder"
        elif re.match(r'^\d+ kap\.', line):
            titel = line
            current_kapitel = {
                "kapitel": re.match(r'^(\d+ kap\.)', line).group(1),
                "titel": titel,
                "paragrafer": []
            }
            if current_avdelning:
                current_avdelning["kapitel"].append(current_kapitel)
            current_paragraf = None

        # Paragraf: "1 §", "2 §" etc.
        elif re.match(r'^\d+ §', line):
            paragraf_nr = re.match(r'^(\d+ §)', line).group(1)
            paragraf_text = line
            current_paragraf = {
                "paragraf": paragraf_nr,
                "text": paragraf_text
            }
            if current_kapitel:
                current_kapitel["paragrafer"].append(current_paragraf)

        # Fortsättning av paragraftext (indragen eller tom rad = nytt stycke)
        elif current_paragraf is not None and line:
            current_paragraf["text"] += " " + line

        i += 1

    return result

parsed = parse_brottsbalken(text)

with open("brottsbalken.json", "w", encoding="utf-8") as f:
    json.dump(parsed, f, ensure_ascii=False, indent=2)

print("Klar! Antal avdelningar:", len(parsed))
for avd in parsed:
    print(f"  {avd['avdelning']}: {len(avd['kapitel'])} kapitel")