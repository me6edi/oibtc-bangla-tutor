import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("data/nctb_raw/ict_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

with open("scripts/full_dataset_dump.txt", "w", encoding="utf-8") as out:
    for i, c in enumerate(chunks, 1):
        out.write(f"=== CHUNK {i:02d} | Chapter {c.get('chapter')} | Page {c.get('page')} ===\n")
        out.write(f"Topic: {c.get('topic')}\n")
        out.write(f"Content:\n{c.get('content')}\n\n")

print(f"Dumped {len(chunks)} chunks to scripts/full_dataset_dump.txt")
