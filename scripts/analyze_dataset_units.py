import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("data/nctb_raw/ict_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Total chunks: {len(chunks)}")
for idx, c in enumerate(chunks, 1):
    ch = c.get("chapter")
    topic = c.get("topic")
    page = c.get("page")
    content = c.get("content", "")
    print(f"[{idx:02d}] Ch {ch} | P.{page} | {topic}")
    lines = [line.strip() for line in content.split("\n") if line.strip()]
    first_two = " | ".join(lines[:2])
    print(f"     Preview: {first_two[:140]}...")
