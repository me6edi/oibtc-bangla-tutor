import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("data/nctb_raw/ict_class9_10_ch1_ch2.json", "r", encoding="utf-8") as f:
    topics = json.load(f)

print(f"Total topics: {len(topics)}")
for i, t in enumerate(topics, 1):
    print(f"{i:2d}. Ch {t['chapter']}, Page {t['page']:2d}: {t['topic']}")
