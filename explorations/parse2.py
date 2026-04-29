import re
import json

text = open("brottsbalken.txt", encoding="utf-8").read()

chunks = []

for block in re.split(r'\n(?=\d+ kap\.)', text):
    match = re.match(r'(\d+ kap\.) (.+?)\n(.+)', block, re.DOTALL)
    if match:
        chunks.append({
            "kapitel": match.group(1),
            "titel": match.group(2).strip(),
            "text": match.group(3).strip()
        })

json.dump(chunks, open("brottsbalken_chunks.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"Antal kapitel: {len(chunks)}")