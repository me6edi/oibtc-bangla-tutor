import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


with open("data/nctb_raw/ict_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Total chunks in ict_chunks.json: {len(chunks)}")
for c in chunks:
    print(f"ID: {c.get('id')} | Ch: {c.get('chapter')} | Page: {c.get('page')} | Topic: {c.get('topic')}")
