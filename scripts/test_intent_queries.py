import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from backend.rag.pipeline import get_rag_pipeline

pipeline = get_rag_pipeline()

test_cases = [
    ("কম্পিউটার ভাইরাস কী?", "শুধু সংজ্ঞা"),
    ("কম্পিউটার ভাইরাস কী এবং কীভাবে ছড়ায়?", "সংজ্ঞা + কীভাবে ছড়ায়"),
    ("কম্পিউটার ভাইরাস কীভাবে ছড়ায়?", "শুধু ছড়ানোর পদ্ধতি"),
    ("ভাইরাস থেকে কীভাবে নিরাপদ থাকব?", "শুধু প্রতিরোধ/নিরাপত্তার উপায়"),
    ("ভাইরাসের উদাহরণ দাও।", "শুধু উদাহরণ"),
    ("শক্তিশালী পাসওয়ার্ড তৈরি করার নিয়মগুলো কী?", "শুধু নিয়মাবলি"),
    ("কম্পিউটার ঘন ঘন রিস্টার্ট হলে কী করব?", "শুধু ট্রাবলশুটিং সমাধান"),
    ("ই-লার্নিং বলতে কী বোঝায়?", "শুধু ই-লার্নিংয়ের সংজ্ঞা"),
    ("চার্লস ব্যাবেজ কেন বিখ্যাত?", "শুধু অবদান ও পরিচয়"),
    ("কম্পিউটারে ভাইরাস আক্রমণের লক্ষণগুলো কী?", "শুধু লক্ষণসমূহ")
]

print("=========================================================================")
print("          TESTING TEXTBOOK-BASED INTENT & SCOPE ANSWERS                  ")
print("=========================================================================\n")

for q, expected in test_cases:
    res = pipeline.process_query(q)
    print(f"QUESTION: {q}")
    print(f"EXPECTED: {expected}")
    print(f"DETECTED INTENT: {res['intent']} ({res['intent_label']})")
    print("ANSWER:")
    print(res["answer"])
    print("SOURCE CITATION:", [(s["topic"], f"পৃষ্ঠা: {s['page']}") for s in res["sources"][:1]])
    print("=" * 73 + "\n")
