import json
import sys
import re

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("data/nctb_raw/ict_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"=================================================================")
print(f"COMPREHENSIVE DATASET PEDAGOGICAL UNIT EXTRACTION (CHUNKS: {len(chunks)})")
print(f"=================================================================\n")

ch1_chunks = [c for c in chunks if c.get("chapter") == 1]
ch2_chunks = [c for c in chunks if c.get("chapter") == 2]

print(f"Chapter 1 Chunks: {len(ch1_chunks)}")
print(f"Chapter 2 Chunks: {len(ch2_chunks)}")
print()

for idx, c in enumerate(chunks, 1):
    ch = c.get("chapter")
    page = c.get("page")
    topic = c.get("topic")
    content = c.get("content", "")
    
    # Extract numbers/years
    years = re.findall(r'\b(1[89]\d\d|20\d\d)\b', content)
    bn_years = re.findall(r'[০-৯]{4}', content)
    
    # Extract lists / numbered items
    numbered = re.findall(r'(?:^|\n)\s*([১-৯১-৯]|\d+)\.\s*([^\n]+)', content)
    bulleted = re.findall(r'(?:^|\n)\s*[•\-*]\s*([^\n]+)', content)
    
    # Extract English terms / technical terms
    eng_terms = re.findall(r'([A-Za-z0-9\-\.\s]{3,35})\b', content)
    eng_terms = list(set([t.strip() for t in eng_terms if len(t.strip()) > 2 and not t.strip().isdigit()]))[:6]
    
    print(f"[{idx:02d}] CH {ch} | P.{page:02d} | TOPIC: {topic}")
    print(f"     Content Length: {len(content)} chars")
    if years or bn_years:
        print(f"     Key Years/Dates: {list(set(years + bn_years))}")
    if eng_terms:
        print(f"     Key Tech Terms: {eng_terms[:5]}")
    if numbered:
        print(f"     Numbered Points ({len(numbered)}): {[item[1][:40] + '...' for item in numbered[:3]]}")
    if bulleted:
        print(f"     Bulleted Points ({len(bulleted)}): {[item[:40] + '...' for item in bulleted[:3]]}")
    print("-" * 65)
