import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.rag.pipeline import RAGPipeline

p = RAGPipeline()

print("--- TEST 1: Microsoft Excel SUM (Must be safely rejected) ---")
r1 = p.process_query("Microsoft Excel-এর SUM কীভাবে ব্যবহার করব?")
print("Q:", r1["query"])
print("Ans:", r1["answer"])
print("Is OOS:", r1["is_out_of_curriculum"])

print("\n--- TEST 2: Banglish Strong Password ---")
r2 = p.process_query("strong password bananor rules ki ki?")
print("Q:", r2["query"])
print("Resolved:", r2.get("resolved_query"))
print("Ans:", r2["answer"][:120] + "...")
print("Sources:", [s["topic"] for s in r2["sources"]])
print("Is OOS:", r2["is_out_of_curriculum"])

print("\n--- TEST 3: Banglish Virus Multi-Intent ---")
r3 = p.process_query("computer virus ki ebong kivabe chhoray?")
print("Q:", r3["query"])
print("Resolved:", r3.get("resolved_query"))
print("Ans:", r3["answer"][:120] + "...")
print("Sources:", [s["topic"] for s in r3["sources"]])
print("Is OOS:", r3["is_out_of_curriculum"])

print("\n--- TEST 4: Contextual Follow-up Turn 1 -> Turn 2 ---")
hist = [
    {
        "sender": "student",
        "query_text": "কম্পিউটার ভাইরাস কী?",
        "sources_json": '[{"topic": "কম্পিউটার ভাইরাস ও ম্যালওয়্যার - নামকরণ ও ভাইরাসের ইতিহাস"}]'
    }
]
r4 = p.process_query("এটি কীভাবে ছড়ায়?", history=hist)
print("Q:", r4["query"])
print("Resolved:", r4.get("resolved_query"))
print("Ans:", r4["answer"][:120] + "...")
print("Sources:", [s["topic"] for s in r4["sources"]])
print("Is OOS:", r4["is_out_of_curriculum"])
