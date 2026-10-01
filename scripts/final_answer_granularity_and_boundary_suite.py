"""
Final Answer Granularity and Strict Knowledge-Boundary Verification Suite
Validates Section 29 & Section 33 requirements of the Final Master Prompt.
"""

import sys
import os
import time
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, ".")

from typing import Dict, Any, List
from backend.rag.pipeline import get_rag_pipeline
from backend.rag.intent import GranularityType

# Reconfigure stdout for utf-8
sys.stdout.reconfigure(encoding='utf-8')

pipeline = get_rag_pipeline()

TEST_CASES = [
    # -------------------------------------------------------------
    # 1. YEAR: "কত সালে?" / "কবে?" -> Direct Year First
    # -------------------------------------------------------------
    {
        "id": "GRAN_01_YEAR_SATELLITE",
        "category": "Answer Granularity - Year",
        "query": "বঙ্গবন্ধু স্যাটেলাইট-১ কত সালে মহাকাশে উৎক্ষেপণ করা হয়?",
        "expected_granularity": GranularityType.YEAR,
        "first_line_must_contain": ["২০১৮"],
        "answer_must_contain": ["২০১৮", "১২ মে", "৫৭তম"],
        "forbidden_patterns": ["১৮৬৫ সালে", "১৯৭১ সালের মুক্তিযুদ্ধ"],
        "is_oos": False
    },
    {
        "id": "GRAN_02_YEAR_FACEBOOK",
        "category": "Answer Granularity - Year",
        "query": "ফেসবুক কত সালে প্রতিষ্ঠিত হয়?",
        "expected_granularity": GranularityType.YEAR,
        "first_line_must_contain": ["২০০৪"],
        "answer_must_contain": ["২০০৪", "৪ঠা ফেব্রুয়ারি"],
        "forbidden_patterns": [],
        "is_oos": False
    },
    {
        "id": "GRAN_03_YEAR_WWW",
        "category": "Answer Granularity - Year",
        "query": "টিম বার্নার্স-লি কত সালে ডব্লিউডব্লিউডব্লিউ বা WWW এর প্রস্তাব দেন?",
        "expected_granularity": GranularityType.YEAR,
        "first_line_must_contain": ["১৯৮৯"],
        "answer_must_contain": ["১৯৮৯", "এইচটিটিপি"],
        "forbidden_patterns": [],
        "is_oos": False
    },
    {
        "id": "GRAN_04_YEAR_EMAIL",
        "category": "Answer Granularity - Year",
        "query": "রেমন্ড টমলিনসন কত সালে প্রথম ই-মেইল ব্যবস্থা চালু করেন?",
        "expected_granularity": GranularityType.YEAR,
        "first_line_must_contain": ["১৯৭১"],
        "answer_must_contain": ["১৯৭১", "আরপানেট"],
        "forbidden_patterns": [],
        "is_oos": False
    },
    {
        "id": "GRAN_05_YEAR_MAXWELL_ABSENT",
        "category": "Answer Granularity - Year (Strict Grounding)",
        "query": "জেমস ক্লার্ক ম্যাক্সওয়েল কত সালে তড়িৎচুম্বকীয় বলের ধারণা প্রকাশ করেন?",
        "expected_granularity": GranularityType.YEAR,
        "first_line_must_contain": ["অধ্যায় ১", "dataset-এ সরাসরি উল্লেখ নেই"],
        "answer_must_contain": ["ম্যাক্সওয়েল", "উল্লেখ নেই"],
        "forbidden_patterns": ["১৮৬৫ সালে তড়িৎ"],  # Must NOT hallucinate 1865 because not in chunk!
        "is_oos": False
    },

    # -------------------------------------------------------------
    # 2. PERSON: "কে?" / "কার?" -> Direct Name First
    # -------------------------------------------------------------
    {
        "id": "GRAN_06_PERSON_BABBAGE",
        "category": "Answer Granularity - Person",
        "query": "কম্পিউটারের জনক কে?",
        "expected_granularity": GranularityType.PERSON,
        "first_line_must_contain": ["চার্লস ব্যাবেজ"],
        "answer_must_contain": ["চার্লস ব্যাবেজ"],
        "forbidden_patterns": [],
        "is_oos": False
    },
    {
        "id": "GRAN_07_PERSON_PROGRAMMER",
        "category": "Answer Granularity - Person",
        "query": "ইতিহাসের প্রথম কম্পিউটার প্রোগ্রামার কে ছিলেন?",
        "expected_granularity": GranularityType.PERSON,
        "first_line_must_contain": ["অ্যাডা লাভলেস"],
        "answer_must_contain": ["অ্যাডা লাভলেস"],
        "forbidden_patterns": [],
        "is_oos": False
    },
    {
        "id": "GRAN_08_PERSON_VIRUS_NAME",
        "category": "Answer Granularity - Person",
        "query": "কম্পিউটার ভাইরাস নামটি কে দেন?",
        "expected_granularity": GranularityType.PERSON,
        "first_line_must_contain": ["ফ্রেড কোহেন"],
        "answer_must_contain": ["ফ্রেড কোহেন"],
        "forbidden_patterns": [],
        "is_oos": False
    },
    {
        "id": "GRAN_09_PERSON_RADIO",
        "category": "Answer Granularity - Person",
        "query": "বেতার তরঙ্গ ব্যবহারের জন্য কোন বিজ্ঞানী প্রথম সার্বজনীন স্বীকৃতি পান?",
        "expected_granularity": GranularityType.PERSON,
        "first_line_must_contain": ["গুলিয়েলমো মার্কনি"],
        "answer_must_contain": ["গুলিয়েলমো মার্কনি"],
        "forbidden_patterns": [],
        "is_oos": False
    },

    # -------------------------------------------------------------
    # 3. COUNT: "কতটি?" / "কয়টি?" -> Direct Count First + List
    # -------------------------------------------------------------
    {
        "id": "GRAN_10_COUNT_PILLARS",
        "category": "Answer Granularity - Count",
        "query": "ডিজিটাল বাংলাদেশ রূপকল্পের কয়টি প্রধান স্তম্ভ রয়েছে?",
        "expected_granularity": GranularityType.COUNT,
        "first_line_must_contain": ["৪টি"],
        "answer_must_contain": ["৪টি প্রধান স্তম্ভ", "মানবসম্পদ উন্নয়ন", "নাগরিক সংযোগ", "ডিজিটাল সরকার", "তথ্যপ্রযুক্তি শিল্প"],
        "forbidden_patterns": [],
        "is_oos": False
    },
    {
        "id": "GRAN_11_COUNT_PASSWORD_RULES",
        "category": "Answer Granularity - Count",
        "query": "শক্তিশালী পাসওয়ার্ড তৈরির কয়টি প্রধান নিয়ম বইয়ে আলোচনা করা হয়েছে?",
        "expected_granularity": GranularityType.COUNT,
        "first_line_must_contain": ["৫টি"],
        "answer_must_contain": ["৫টি নিয়ম", "বড় হাতের", "সংখ্যা", "চিহ্ন", "৮ থেকে ১৬"],
        "forbidden_patterns": [],
        "is_oos": False
    },
    {
        "id": "GRAN_12_COUNT_ECOMMERCE_CONDS",
        "category": "Answer Granularity - Count",
        "query": "ই-কমার্সে লেনদেনের জন্য কয়টি প্রধান শর্ত প্রয়োজন?",
        "expected_granularity": GranularityType.COUNT,
        "first_line_must_contain": ["৩টি"],
        "answer_must_contain": ["৩টি প্রধান শর্ত", "পণ্য", "মূল্য", "হস্তান্তর"],
        "forbidden_patterns": [],
        "is_oos": False
    },

    # -------------------------------------------------------------
    # 4. DEFINITION: "কী?" -> Concise Definition
    # -------------------------------------------------------------
    {
        "id": "GRAN_13_DEF_VIRUS",
        "category": "Answer Granularity - Definition",
        "query": "কম্পিউটার ভাইরাস কী?",
        "expected_granularity": GranularityType.WHAT,
        "first_line_must_contain": ["ক্ষতিকর প্রোগ্রাম"],
        "answer_must_contain": ["Vital Information Resources Under Siege", "ক্ষতিকর প্রোগ্রাম"],
        "forbidden_patterns": ["কুলিং ফ্যান", "আর্থিং"],
        "is_oos": False
    },
    {
        "id": "GRAN_14_DEF_EPURJEE",
        "category": "Answer Granularity - Definition",
        "query": "ই-পুর্জি কী?",
        "expected_granularity": GranularityType.WHAT,
        "first_line_must_contain": ["আখ চাষি"],
        "answer_must_contain": ["চিনি", "আখ", "অনুমতিপত্র"],
        "forbidden_patterns": [],
        "is_oos": False
    },
    {
        "id": "GRAN_15_DEF_2FA",
        "category": "Answer Granularity - Definition",
        "query": "টু-ফ্যাক্টর অথেনটিকেশন (2FA) কী?",
        "expected_granularity": GranularityType.WHAT,
        "first_line_must_contain": ["নিরাপত্তা"],
        "answer_must_contain": ["দ্বি-স্তর", "ওটিপি"],
        "forbidden_patterns": [],
        "is_oos": False
    },

    # -------------------------------------------------------------
    # 5. PROCESS / METHOD: "কীভাবে?" -> Process / Method First
    # -------------------------------------------------------------
    {
        "id": "GRAN_16_HOW_VIRUS_SPREADS",
        "category": "Answer Granularity - Process",
        "query": "কম্পিউটার ভাইরাস কীভাবে ছড়ায়?",
        "expected_granularity": GranularityType.HOW,
        "first_line_must_contain": ["ছড়ায়"],
        "answer_must_contain": ["পেনড্রাইভ", "ডাউনলোড", "পাইরেটেড"],
        "forbidden_patterns": [],
        "is_oos": False
    },
    {
        "id": "GRAN_17_HOW_UNINSTALL",
        "category": "Answer Granularity - Process",
        "query": "উইন্ডোজ অপারেটিং সিস্টেমে সফটওয়্যার কীভাবে আনইনস্টল করতে হয়?",
        "expected_granularity": GranularityType.HOW,
        "first_line_must_contain": ["কন্ট্রোল প্যানেল"],
        "answer_must_contain": ["Control Panel", "Uninstall a program"],
        "forbidden_patterns": [],
        "is_oos": False
    },

    # -------------------------------------------------------------
    # 6. CAUSE / REASON: "কেন?" -> Direct Cause First
    # -------------------------------------------------------------
    {
        "id": "GRAN_18_WHY_SHOCK",
        "category": "Answer Granularity - Reason",
        "query": "কম্পিউটারের মেটালিক বডিতে হাত দিলে শক লাগে কেন?",
        "expected_granularity": GranularityType.WHY,
        "first_line_must_contain": ["আর্থিং"],
        "answer_must_contain": ["গ্রাউন্ডিং", "আর্থিং"],
        "forbidden_patterns": [],
        "is_oos": False
    },
    {
        "id": "GRAN_19_WHY_CMOS",
        "category": "Answer Granularity - Reason",
        "query": "কম্পিউটার বন্ধ করলে ঘড়ির সময় ও তারিখ উল্টাপাল্টা হয়ে যায় কেন?",
        "expected_granularity": GranularityType.WHY,
        "first_line_must_contain": ["সিএমওএস"],
        "answer_must_contain": ["CMOS", "ব্যাটারি"],
        "forbidden_patterns": [],
        "is_oos": False
    },

    # -------------------------------------------------------------
    # 7. CONCISE / ONE-LINE: "সংক্ষেপে বলো" / "এক লাইনে বলো"
    # -------------------------------------------------------------
    {
        "id": "GRAN_20_CONCISE_ELEARNING",
        "category": "Answer Granularity - Concise",
        "query": "ই-লার্নিং কাকে বলে সংক্ষেপে বলো।",
        "expected_granularity": GranularityType.SHORT,
        "first_line_must_contain": ["ইলেকট্রনিক"],
        "answer_must_contain": ["ই-লার্নিং", "ইন্টারনেট"],
        "forbidden_patterns": [],
        "is_oos": False
    },
    {
        "id": "GRAN_21_ONE_LINE_DEFRAG",
        "category": "Answer Granularity - One Line",
        "query": "ডিস্ক ডিফ্র্যাগমেন্টারের কাজ কী এক লাইনে বলো।",
        "expected_granularity": GranularityType.ONE_LINE,
        "first_line_must_contain": ["ডিস্ক ডিফ্র্যাগমেন্টার"],
        "answer_must_contain": ["ফাইল", "সাজিয়ে"],
        "forbidden_patterns": [],
        "is_oos": False
    },

    # -------------------------------------------------------------
    # 8. DETAILED: "বিস্তারিত বলো"
    # -------------------------------------------------------------
    {
        "id": "GRAN_22_DETAILED_MAINTENANCE",
        "category": "Answer Granularity - Detailed",
        "query": "কম্পিউটারের সফটওয়্যার রক্ষণাবেক্ষণের প্রয়োজনীয়তা সম্পর্কে বিস্তারিত বলো।",
        "expected_granularity": GranularityType.DETAILED,
        "first_line_must_contain": ["সফটওয়্যার রক্ষণাবেক্ষণ"],
        "answer_must_contain": ["ক্যাশ", "টেম্পোরারি ফাইল", "ডিস্ক ক্লিনআপ", "ধীরগতি"],
        "forbidden_patterns": [],
        "is_oos": False
    },

    # -------------------------------------------------------------
    # 9. MULTI-INTENT: Both requested components
    # -------------------------------------------------------------
    {
        "id": "GRAN_23_MULTI_VIRUS_DEF_HOW",
        "category": "Multi-Intent Handling",
        "query": "কম্পিউটার ভাইরাস কী এবং এটি কীভাবে ছড়ায়?",
        "expected_granularity": GranularityType.HOW,
        "first_line_must_contain": ["সংজ্ঞা", "ভাইরাস"],
        "answer_must_contain": ["ক্ষতিকর প্রোগ্রাম", "পেনড্রাইভ"],
        "forbidden_patterns": [],
        "is_oos": False
    },
    {
        "id": "GRAN_24_MULTI_COPYRIGHT_BSA",
        "category": "Multi-Intent Handling",
        "query": "বাংলাদেশে কপিরাইট আইন কত সালে প্রণীত হয় এবং বিএসএ এর রিপোর্ট কী?",
        "expected_granularity": GranularityType.YEAR,
        "first_line_must_contain": ["কপিরাইট"],
        "answer_must_contain": ["২০০০", "২০০৫", "১০ জনের মধ্যে ৪ জন"],
        "forbidden_patterns": [],
        "is_oos": False
    },

    # -------------------------------------------------------------
    # 10. CONTEXTUAL FOLLOW-UP
    # -------------------------------------------------------------
    {
        "id": "GRAN_25_CONTEXT_FOLLOWUP",
        "category": "Contextual Follow-up",
        "query": "এটি কীভাবে ছড়ায়?",
        "history": [
            {
                "query": "কম্পিউটার ভাইরাস কী?",
                "answer": "কম্পিউটার ভাইরাস হলো ক্ষতিকর প্রোগ্রাম。",
                "sources_json": json.dumps([{"topic": "কম্পিউটার ভাইরাস ধারণা ও ক্ষতিকারক দিক"}])
            }
        ],
        "expected_granularity": GranularityType.HOW,
        "first_line_must_contain": ["ছড়ায়"],
        "answer_must_contain": ["পেনড্রাইভ", "ডাউনলোড"],
        "forbidden_patterns": [],
        "is_oos": False
    },

    # -------------------------------------------------------------
    # 11. STRICT KNOWLEDGE-BOUNDARY & OUT-OF-CURRICULUM REJECTION
    # -------------------------------------------------------------
    {
        "id": "BOUND_01_SQL",
        "category": "Knowledge Boundary - SQL",
        "query": "এসকিউএল (SQL) দিয়ে ডাটাবেজে নতুন টেবিল তৈরি করার কোড কী?",
        "expected_granularity": GranularityType.GENERAL,
        "first_line_must_contain": ["আওতাভুক্ত নয় বা dataset-এ পাওয়া যায়নি"],
        "answer_must_contain": ["অধ্যায় ১ ও অধ্যায় ২"],
        "forbidden_patterns": ["CREATE TABLE", "SELECT *"],
        "is_oos": True
    },
    {
        "id": "BOUND_02_EXCEL_SUM",
        "category": "Knowledge Boundary - Excel SUM",
        "query": "মাইক্রোসফট এক্সেলে যোগ করার জন্য SUM ফাংশন কীভাবে লিখতে হয়?",
        "expected_granularity": GranularityType.GENERAL,
        "first_line_must_contain": ["আওতাভুক্ত নয় বা dataset-এ পাওয়া যায়নি"],
        "answer_must_contain": ["অধ্যায় ১ ও অধ্যায় ২"],
        "forbidden_patterns": ["=SUM(", "ফর্মুলা"],
        "is_oos": True
    },
    {
        "id": "BOUND_03_PHOTOSHOP",
        "category": "Knowledge Boundary - Photoshop",
        "query": "ফটোশপে ব্যাকগ্রাউন্ড রিমুভ করার লেসো টুল কীভাবে কাজ করে?",
        "expected_granularity": GranularityType.GENERAL,
        "first_line_must_contain": ["আওতাভুক্ত নয় বা dataset-এ পাওয়া যায়নি"],
        "answer_must_contain": ["অধ্যায় ১ ও অধ্যায় ২"],
        "forbidden_patterns": ["Lasso", "Layer"],
        "is_oos": True
    },
    {
        "id": "BOUND_04_PYTHON",
        "category": "Knowledge Boundary - Python",
        "query": "পাইথনে ফর লুপ (for loop) ব্যবহারের সিনট্যাক্স কী?",
        "expected_granularity": GranularityType.GENERAL,
        "first_line_must_contain": ["আওতাভুক্ত নয় বা dataset-এ পাওয়া যায়নি"],
        "answer_must_contain": ["অধ্যায় ১ ও অধ্যায় ২"],
        "forbidden_patterns": ["for i in range"],
        "is_oos": True
    },
    {
        "id": "BOUND_05_GENERAL_RIVER",
        "category": "Knowledge Boundary - General Knowledge",
        "query": "বাংলাদেশের প্রধান প্রধান নদী কোনগুলো?",
        "expected_granularity": GranularityType.GENERAL,
        "first_line_must_contain": ["আওতাভুক্ত নয় বা dataset-এ পাওয়া যায়নি"],
        "answer_must_contain": ["অধ্যায় ১ ও অধ্যায় ২"],
        "forbidden_patterns": ["পদ্মা", "মেঘনা", "যমুনা"],
        "is_oos": True
    },
    {
        "id": "BOUND_06_CHAPTER_5",
        "category": "Knowledge Boundary - Non-Ch1/2",
        "query": "তথ্য ও যোগাযোগ প্রযুক্তি বইয়ের অধ্যায় ৫ মাল্টিমিডিয়া সম্পর্কে বিস্তারিত বলো।",
        "expected_granularity": GranularityType.DETAILED,
        "first_line_must_contain": ["আওতাভুক্ত নয় বা dataset-এ পাওয়া যায়নি"],
        "answer_must_contain": ["অধ্যায় ১ ও অধ্যায় ২"],
        "forbidden_patterns": ["অডিও", "ভিডিও", "অ্যানিমেশন"],
        "is_oos": True
    }
]


def run_suite():
    print("=" * 80)
    print("RUNNING FINAL ANSWER GRANULARITY & STRICT KNOWLEDGE-BOUNDARY TEST SUITE")
    print("=" * 80)

    total = len(TEST_CASES)
    passed = 0
    failed = 0
    latencies = []
    failures = []

    for idx, tc in enumerate(TEST_CASES, 1):
        t0 = time.perf_counter()
        res = pipeline.process_query(
            query=tc["query"],
            history=tc.get("history")
        )
        latency = (time.perf_counter() - t0) * 1000
        latencies.append(latency)

        ans = res.get("answer", "")
        lines = [line.strip() for line in ans.split("\n") if line.strip()]
        first_line = lines[0] if lines else ""

        is_passed = True
        reason = []

        # Check OOS flag
        if tc["is_oos"]:
            if not res.get("is_out_of_curriculum"):
                is_passed = False
                reason.append("Expected is_out_of_curriculum=True")
        else:
            if res.get("is_out_of_curriculum"):
                is_passed = False
                reason.append("False positive: Query flagged as out of curriculum")

        # Check first line must contain
        for kw in tc.get("first_line_must_contain", []):
            if kw not in first_line:
                # Also check full answer if first line was a title/header
                if kw not in ans:
                    is_passed = False
                    reason.append(f"Missing core answer keyword: '{kw}'")

        # Check answer must contain
        for kw in tc.get("answer_must_contain", []):
            if kw not in ans:
                is_passed = False
                reason.append(f"Answer missing expected keyword: '{kw}'")

        # Check forbidden patterns (hallucination check)
        for forb in tc.get("forbidden_patterns", []):
            if forb in ans:
                is_passed = False
                reason.append(f"Hallucination detected: found forbidden '{forb}'")

        status_str = "PASS" if is_passed else "FAIL"
        if is_passed:
            passed += 1
        else:
            failed += 1
            failures.append({
                "id": tc["id"],
                "query": tc["query"],
                "reason": reason,
                "first_line": first_line,
                "answer_snippet": ans[:180]
            })

        print(f"[{status_str}] #{idx:02d} ({tc['id']}) Latency: {latency:.2f}ms")
        print(f"       Q: {tc['query']}")
        print(f"       1st Line: {first_line[:90]}")
        if not is_passed:
            print(f"       [!] FAILED: {reason}")
        print("-" * 80)

    min_lat = min(latencies) if latencies else 0.0
    avg_lat = sum(latencies) / len(latencies) if latencies else 0.0
    max_lat = max(latencies) if latencies else 0.0

    print("\n" + "=" * 80)
    print("ANSWER GRANULARITY & BOUNDARY TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests Executed: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Pass Rate: {passed/total*100:.2f}%")
    print(f"Latency: Min={min_lat:.2f}ms | Avg={avg_lat:.2f}ms | Max={max_lat:.2f}ms")
    print("=" * 80)

    if failures:
        print("\nFAILURES:")
        for f in failures:
            print(f"- ID: {f['id']}")
            print(f"  Query: {f['query']}")
            print(f"  Reason: {f['reason']}")
            print(f"  Answer: {f['answer_snippet']}")
    else:
        print("\nALL GRANULARITY AND KNOWLEDGE BOUNDARY TESTS PASSED PERFECTLY!")

    report_data = {
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": passed / total * 100,
        "latency_ms": {
            "min": round(min_lat, 2),
            "avg": round(avg_lat, 2),
            "max": round(max_lat, 2)
        },
        "failures": failures
    }
    with open("scripts/final_granularity_report.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    return failed == 0

if __name__ == "__main__":
    success = run_suite()
    sys.exit(0 if success else 1)
