"""
Verification Script for NCTB 2026 Curriculum Dataset and Scoped Answering
Tests Chapter 1 and Chapter 2 queries including multi-clause Turin query,
definitions, troubleshooting cases, and intent scoping.
"""

import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

from backend.rag.pipeline import RAGPipeline
from backend.rag.intent import classify_intent

TEST_CASES = [
    {
        "name": "Babbage Turin 1840 & Ada Lovelace Multi-Clause",
        "query": "চার্লস ব্যাবেজ কত সালে তুরিন বিশ্ববিদ্যালয়ে বক্তৃতা দিয়েছিলেন এবং তাঁর এই কাজের সাথে কোন নারী যুক্ত ছিলেন?",
        "expected_keywords": ["১৮৪০", "তুরিন", "অ্যাডা লাভলেস"],
        "forbidden_keywords": ["১৭৯১-১৮৭১"]  # should not just dump generic Babbage birth-death bio
    },
    {
        "name": "Computer Virus Definition Only",
        "query": "কম্পিউটার ভাইরাস কী?",
        "expected_keywords": ["Vital Information Resources Under Siege", "ক্ষতিকর প্রোগ্রাম"],
        "forbidden_keywords": ["কীভাবে ছড়ায়:", "প্রতিরোধের উপায়:"]
    },
    {
        "name": "Computer Virus Definition + Mechanism (Multi-Intent)",
        "query": "কম্পিউটার ভাইরাস কী এবং কীভাবে ছড়ায়?",
        "expected_keywords": ["সংজ্ঞা", "ছড়ায়", "পেনড্রাইভ"],
        "forbidden_keywords": []
    },
    {
        "name": "Strong Password Rules",
        "query": "শক্তিশালী পাসওয়ার্ড তৈরির নিয়ম কী?",
        "expected_keywords": ["পাসওয়ার্ড", "নিয়মাবলি", "বড় হাতের অক্ষর", "বিশেষ চিহ্ন"],
        "forbidden_keywords": []
    },
    {
        "name": "Troubleshooting - Metallic Body Shock",
        "query": "কম্পিউটারের মেটালিক বডিতে হাত দিলে শক লাগে কেন?",
        "expected_keywords": ["আর্থিং", "গ্রাউন্ডিং", "শক"],
        "forbidden_keywords": []
    },
    {
        "name": "Troubleshooting - Frequent Restart",
        "query": "কম্পিউটার ঘন ঘন রিস্টার্ট হলে কী করব?",
        "expected_keywords": ["কুলিং ফ্যান", "থার্মাল পেস্ট", "রিস্টার্ট"],
        "forbidden_keywords": []
    },
    {
        "name": "Troubleshooting - CMOS Battery Date/Time",
        "query": "কম্পিউটারের তারিখ ও সময় বারবার ভুল দেখালে কী করতে হবে?",
        "expected_keywords": ["সিএমওএস", "CMOS", "ব্যাটারি"],
        "forbidden_keywords": []
    },
    {
        "name": "2026 Topic - Quantum Computer Definition",
        "query": "কোয়ান্টাম কম্পিউটার কী?",
        "expected_keywords": ["কোয়ান্টাম", "সুপারপজিশন", "কম্পিউটার"],
        "forbidden_keywords": []
    },
    {
        "name": "2026 Topic - Fake News Definition",
        "query": "ফেইক নিউজ কাকে বলে?",
        "expected_keywords": ["ফেইক নিউজ", "অসত্য", "অপতথ্য"],
        "forbidden_keywords": []
    },
    {
        "name": "Chapter 1 Historical Person - Steve Jobs",
        "query": "স্টিভ জবস কে ছিলেন?",
        "expected_keywords": ["স্টিভ জবস", "অ্যাপল", "১৯৭৬"],
        "forbidden_keywords": []
    },
    {
        "name": "2026 Topic - Bangabandhu Satellite-1",
        "query": "বঙ্গবন্ধু স্যাটেলাইট-১ সম্পর্কে বলো",
        "expected_keywords": ["বঙ্গবন্ধু স্যাটেলাইট", "২০১৮", "৫৭তম"],
        "forbidden_keywords": []
    },
    {
        "name": "Out of Curriculum Query",
        "query": "বাংলাদেশের প্রধান নদীগুলোর নাম কী?",
        "expected_keywords": ["আওতাভুক্ত নয়"],
        "forbidden_keywords": []
    }
]


def run_tests():
    print("Initializing RAGPipeline...")
    pipeline = RAGPipeline()
    passed = 0
    total = len(TEST_CASES)

    print(f"\nRunning {total} Verification Test Cases for 2026 Curriculum:\n" + "=" * 70)

    for idx, tc in enumerate(TEST_CASES, 1):
        q = tc["query"]
        res = pipeline.process_query(q)
        ans = res["answer"]
        intent_label = res["intent_label"]

        success = True
        missing = []
        for kw in tc["expected_keywords"]:
            if kw.lower() not in ans.lower():
                success = False
                missing.append(kw)

        found_forbidden = []
        for kw in tc["forbidden_keywords"]:
            if kw.lower() in ans.lower():
                success = False
                found_forbidden.append(kw)

        if success:
            passed += 1
            print(f"[PASS] #{idx} {tc['name']}")
            print(f"       Query: {q}")
            print(f"       Intent: {intent_label}")
            print(f"       Answer Sample: {ans[:90]}...\n")
        else:
            print(f"[FAIL] #{idx} {tc['name']}")
            print(f"       Query: {q}")
            print(f"       Intent: {intent_label}")
            if missing:
                print(f"       Missing expected keywords: {missing}")
            if found_forbidden:
                print(f"       Contains forbidden keywords: {found_forbidden}")
            print(f"       Actual Answer: {ans}\n")

    print("=" * 70)
    print(f"Result: {passed}/{total} test cases passed ({passed/total*100:.1f}%)")
    if passed == total:
        print("ALL TESTS PASSED! 2026 NCTB Curriculum dataset and answering verified.")
        return 0
    else:
        print("SOME TESTS FAILED.")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
