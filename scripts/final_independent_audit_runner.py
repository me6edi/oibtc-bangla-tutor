"""
Final Independent Audit Test Runner for OIBTC
Author: Senior AI Engineer & RAG Evaluation Specialist
Executes exhaustive verification across:
1. Dataset Integrity & Information-Unit Coverage
2. Previous 67-Test Benchmark
3. Answer Granularity Suite (Year, Person, Count, Def, Process, Detailed, Short, Multi-Intent, Context)
4. Adversarial Scope & Zero-Hallucination Suite (Keyword traps, false premises, out-of-curriculum)
5. Banglish & Typo Robustness Suite
6. Contextual Multi-Turn Conversation Suite
7. API & SQLite Integration Suite
8. Performance / Latency Measurements
"""

import os
import sys
import time
import json
import re
from typing import Dict, Any, List

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.rag.pipeline import RAGPipeline
from backend.rag.intent import GranularityType
from backend.rag.transliteration import canonicalize_bengali

def run_audit():
    print("=" * 80)
    print("      OIBTC FINAL INDEPENDENT AUDIT & SYSTEM INTEGRITY EVALUATION")
    print("=" * 80)
    
    t0 = time.time()
    pipeline = RAGPipeline()
    load_time = time.time() - t0
    print(f"RAGPipeline initialized in {load_time:.2f}s.\n")
    
    results = {
        "dataset": {},
        "coverage": {"total": 0, "passed": 0, "failed": 0, "cases": []},
        "benchmark_67": {"total": 0, "passed": 0, "failed": 0, "cases": []},
        "granularity": {"total": 0, "passed": 0, "failed": 0, "cases": []},
        "scope_hallucination": {"total": 0, "passed": 0, "failed": 0, "cases": []},
        "banglish_typo": {"total": 0, "passed": 0, "failed": 0, "cases": []},
        "context": {"total": 0, "passed": 0, "failed": 0, "cases": []},
        "api": {"total": 0, "passed": 0, "failed": 0, "cases": []},
        "latencies": []
    }

    # -------------------------------------------------------------
    # 1. DATASET INTEGRITY AUDIT
    # -------------------------------------------------------------
    print("--- 1. DATASET INTEGRITY AUDIT ---")
    chunks_path = os.path.join("data", "nctb_raw", "ict_chunks.json")
    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
        
    ch1 = [c for c in chunks if c.get("chapter") == 1]
    ch2 = [c for c in chunks if c.get("chapter") == 2]
    ids = [c["chunk_id"] for c in chunks]
    unique_ids = set(ids)
    
    results["dataset"] = {
        "total_chunks": len(chunks),
        "chapter_1_chunks": len(ch1),
        "chapter_2_chunks": len(ch2),
        "unique_ids": len(unique_ids),
        "duplicates": len(ids) - len(unique_ids),
        "empty_chunks": len([c for c in chunks if not c.get("content", "").strip()]),
        "small_chunks": len([c for c in chunks if len(c.get("content", "").strip()) < 50])
    }
    print(f"Total Chunks: {len(chunks)} (Ch 1: {len(ch1)}, Ch 2: {len(ch2)})")
    print(f"Unique IDs: {len(unique_ids)} / {len(ids)}")
    print(f"Empty: {results['dataset']['empty_chunks']}, Small (<50 chars): {results['dataset']['small_chunks']}")
    assert len(unique_ids) == len(chunks), "Duplicate chunk IDs found!"
    assert len(ch1) == 19, f"Expected 19 chunks in Chapter 1, got {len(ch1)}"
    assert len(ch2) == 24, f"Expected 24 chunks in Chapter 2, got {len(ch2)}"
    print("[PASS] Dataset integrity verified.\n")

    # Helper function to evaluate single query
    def eval_query(q, history=None):
        t_start = time.time()
        res = pipeline.process_query(q, history=history)
        lat = time.time() - t_start
        results["latencies"].append(lat)
        return res, lat

    # -------------------------------------------------------------
    # 2. INFORMATION-UNIT COVERAGE AUDIT (Across all 43 chunks)
    # -------------------------------------------------------------
    print("--- 2. INFORMATION-UNIT COVERAGE AUDIT ---")
    coverage_queries = [
        # Chapter 1
        ("জ্ঞানভিত্তিক অর্থনীতি কী?", ["জ্ঞান", "অর্থনীতি"], False, 1),
        ("একুশ শতকে আইসিটি ব্যবহারের জন্য কী ধরনের দক্ষতা প্রয়োজন?", ["দক্ষতা", "আইসিটি"], False, 1),
        ("কৃত্রিম বুদ্ধিমত্তা বা AI কাকে বলে?", ["মানুষের মতো", "চিন্তা", "সিদ্ধান্ত"], False, 1),
        ("ডিফারেন্স ইঞ্জিন কে তৈরি করেন?", ["চার্লস ব্যাবেজ", "১৮২২"], False, 1),
        ("অ্যানালিটিক্যাল ইঞ্জিনের নকশা কে তৈরি করেন?", ["চার্লস ব্যাবেজ", "১৮৩৩"], False, 1),
        ("অ্যাডা লাভলেস কেন বিখ্যাত?", ["অ্যালগরিদম", "প্রোগ্রামার"], False, 1),
        ("জেমস ক্লার্ক ম্যাক্সওয়েল কোন ধারণা প্রকাশ করেন?", ["তড়িৎ", "চৌম্বকীয়"], False, 1),
        ("জগদীশচন্দ্র বসু ১৮৯৫ সালে কী আবিষ্কার করেন?", ["অতিক্ষুদ্র তরঙ্গ", "মাইক্রোওয়েভ", "সংকেত"], False, 1),
        ("গুলিয়েলমো মার্কনি কেন বিখ্যাত?", ["বেতার", "রেডিও"], False, 1),
        ("রেমন্ড টমলিনসন ১৯৭১ সালে কী আবিষ্কার করেন?", ["ই-মেইল", "@"], False, 1),
        ("স্টিভ জবস ১৯৭৬ সালে কোন কোম্পানি প্রতিষ্ঠা করেন?", ["অ্যাপল", "কম্পিউটার"], False, 1),
        ("উইলিয়াম হেনরি বিল গেটস কোন অপারেটিং সিস্টেম তৈরি করেন?", ["মাইক্রোসফট", "ডস", "উইন্ডোজ"], False, 1),
        ("টিম বার্নার্স-লি ১৯৮৯ সালে কী প্রস্তাব করেন?", ["WWW", "HTTP"], False, 1),
        ("মার্ক জাকারবার্গ কত সালে ফেসবুক প্রতিষ্ঠা করেন?", ["২০০৪", "ফেসবুক"], False, 1),
        ("ই-লার্নিং বলতে কী বোঝায়?", ["ইলেকট্রনিক", "দূরশিক্ষণ", "পরিপূরক"], False, 1),
        ("ই-গভর্ন্যান্স কী এবং এর সুবিধা কী?", ["স্বচ্ছ", "ই-গভর্ন্যান্স"], False, 1),
        ("আখ চাষিদের জন্য ই-পুর্জি কীভাবে সাহায্য করে?", ["চিনিকল", "এসএমএস", "অনুমতিপত্র"], False, 1),
        ("ইএমটিএস (EMTS) ডাক সেবার মাধ্যমে কত সময়ে টাকা পাঠানো যায়?", ["১ মিনিট", "ডাক বিভাগ"], False, 1),
        ("ই-পর্চা কী?", ["খতিয়ান", "জমিজমা", "অনলাইন"], False, 1),
        ("ই-কমার্স বাণিজ্যের ৩টি প্রধান শর্ত কী কী?", ["পণ্য", "মূল্য পরিশোধ"], False, 1),
        ("ফ্রিল্যান্সিং বা মুক্তপেশা বলতে কী বোঝায়?", ["স্বাধীন", "ইন্টারনেট"], False, 1),
        ("টুইটারে কত অক্ষরের মধ্যে বার্তা প্রকাশ করতে হয়?", ["২৮০", "টুইট"], False, 1),
        ("লিপফ্রগ প্রযুক্তি কী?", ["মধ্যবর্তী", "সর্বাধুনিক প্রযুক্তি"], False, 1),
        ("ডিজিটাল বাংলাদেশ রূপকল্পের ৪টি স্তম্ভ কী কী?", ["মানবসম্পদ উন্নয়ন", "নাগরিক সংযোগ", "ডিজিটাল সরকার", "তথ্যপ্রযুক্তি শিল্প"], False, 1),
        ("বঙ্গবন্ধু স্যাটেলাইট-১ কত তারিখে উৎক্ষেপণ করা হয়?", ["২০১৮", "১২ মে"], False, 1),
        ("বঙ্গবন্ধু স্যাটেলাইট-১ কত ডিগ্রি দ্রাঘিমাংশে অবস্থান করছে?", ["১১৯.১°", "পূর্ব"], False, 1),
        ("স্যাটেলাইট ক্ষমতাধর দেশ হিসেবে বাংলাদেশ কততম?", ["৫৭তম"], False, 1),

        # Chapter 2
        ("কম্পিউটার ধীরগতির হলে সফটওয়্যার রক্ষণাবেক্ষণ কেন জরুরি?", ["ধীরগতি", "টেম্পোরারি ফাইল", "ক্যাশ"], False, 2),
        ("ক্যাশ ও অস্থায়ী ফাইল ডিলিট করার রান কমান্ডগুলো কী কী?", ["temp", "%temp%", "prefetch"], False, 2),
        ("ডিস্ক ক্লিনআপের কাজ কী?", ["অপ্রয়োজনীয় ফাইল", "জায়গা"], False, 2),
        ("ডিস্ক ডিফ্র্যাগমেন্টার কীভাবে হার্ডডিস্কের গতি বাড়ায়?", ["বিচ্ছিন্ন ফাইল", "সুবিন্যস্ত"], False, 2),
        ("সফটওয়্যার ইনস্টলেশন করার সেটআপ ফাইলের নাম সাধারণত কী থাকে?", ["setup"], False, 2),
        ("সফটওয়্যার শুধু ডিলিট না করে আনইনস্টল করতে হয় কেন?", ["Uninstall"], False, 2),
        ("শক্তিশালী পাসওয়ার্ড তৈরির ৫টি নিয়ম কী কী?", ["বড় হাতের অক্ষর", "ছোট হাতের অক্ষর", "সংখ্যা", "বিশেষ চিহ্ন", "৮ থেকে ১৬"], False, 2),
        ("টু-ফ্যাক্টর অথেনটিকেশন (2FA) কী?", ["দ্বি-স্তর", "পাসওয়ার্ড"], False, 2),
        ("কম্পিউটার ভাইরাস শব্দের পূর্ণরূপ কী?", ["Vital Information Resources Under Siege"], False, 2),
        ("ফ্রেড কোহেন কত সালে ভাইরাসের নামকরণ করেন?", ["১৯৮৩", "ফ্রেড কোহেন"], False, 2),
        ("জন ভন নিউম্যান ১৯৪৯ সালে কোন ধারণা দেন?", ["স্ব-প্রতিলিপিকরণ"], False, 2),
        ("পাঠ্যবইয়ে উল্লেখিত কয়েকটি ভাইরাসের নাম বল।", ["সিআইএইচ", "ব্রেন", "জেরুজালেম", "ভিয়েনা"], False, 2),
        ("কম্পিউটার ভাইরাসে আক্রান্ত হওয়ার ৩টি লক্ষণ কী কী?", ["ধীর গতি", "মেমোরি", "রিস্টার্ট"], False, 2),
        ("কম্পিউটার ভাইরাস এক কম্পিউটার থেকে অন্য কম্পিউটারে কীভাবে ছড়ায়?", ["পেনড্রাইভ", "মেমোরি কার্ড", "ইন্টারনেট"], False, 2),
        ("ভাইরাস প্রতিরোধে কয়েকটি অ্যান্টিভাইরাস সফটওয়্যারের নাম লেখ।", ["Avast", "Avira", "Kaspersky", "Defender"], False, 2),
        ("ফেইক নিউজ বা গুজব ছড়ানো প্রতিরোধে কী করা উচিত?", ["Fact-checking", "শেয়ার"], False, 2),
        ("ডিজিটাল আসক্তি বলতে কী বোঝায়?", ["দৈনন্দিন", "বিঘ্ন"], False, 2),
        ("নার্সিসিজম কী?", ["লাইক", "আত্মপ্রেম"], False, 2),
        ("ডিজিটাল আসক্তি থেকে মুক্তির উপায় কী?", ["খেলাধুলা", "বই পড়া"], False, 2),
        ("বাংলাদেশে কপিরাইট আইন কত সালে প্রণীত ও সংশোধিত হয়?", ["২০০০", "২০০৫"], False, 2),
        ("সফটওয়্যার পাইরেসি কী?", ["অনুমতি", "অনুলিপি", "পাইরেসি"], False, 2),
        ("বিএসএ (BSA) এর রিপোর্ট অনুযায়ী কতজন ব্যবহারকারী পাইরেটেড সফটওয়্যার ব্যবহার করে?", ["১০ জনের ৪ জন"], False, 2),
        ("তথ্য অধিকার আইন কত সালে পাস হয় এবং এর লক্ষ্য কী?", ["২০০৯", "নাগরিকের তথ্য জানার অধিকার"], False, 2),
        ("কম্পিউটার ট্রাবলশুটিং বলতে কী বোঝায়?", ["উৎস", "সমাধান"], False, 2),
        ("কম্পিউটার চালু হলেও মনিটরে ডিসপ্লে না আসলে কী করতে হবে?", ["র‍্যাম", "RAM", "ডিসপ্লে"], False, 2),
        ("কম্পিউটারের ঘড়ির সময় ও তারিখ বারবার ভুল দেখালে কী করতে হবে?", ["সিএমওএস", "CMOS", "ব্যাটারি"], False, 2),
        ("সিপিইউ এর মেটালিক বডিতে হাত দিলে শক লাগে কেন?", ["আর্থিং", "গ্রাউন্ডিং", "শক"], False, 2),
        ("কম্পিউটার স্বয়ংক্রিয়ভাবে বারবার রিস্টার্ট হলে কী করতে হবে?", ["কুলিং ফ্যান", "থার্মাল পেস্ট", "রিস্টার্ট"], False, 2),
        ("কম্পিউটারে কিবোর্ড বা মাউস কাজ না করলে প্রাথমিক সমাধান কী?", ["পোর্ট", "ইউএসবি"], False, 2),
        ("প্রিন্টারে প্রিন্ট না আসলে কী পরীক্ষা করতে হবে?", ["কাগজ", "সংযোগ"], False, 2),
    ]

    for q, kw_list, expect_oos, exp_ch in coverage_queries:
        res, lat = eval_query(q)
        ans = res["answer"]
        passed = True
        ans_canon = canonicalize_bengali(ans)
        if expect_oos:
            if not res["is_out_of_curriculum"]:
                passed = False
        else:
            if res["is_out_of_curriculum"]:
                passed = False
            for kw in kw_list:
                if canonicalize_bengali(kw) not in ans_canon:
                    passed = False
                    break
        results["coverage"]["total"] += 1
        if passed:
            results["coverage"]["passed"] += 1
        else:
            results["coverage"]["failed"] += 1
            results["coverage"]["cases"].append({"query": q, "expected": kw_list, "got": ans[:150]})

    cov_pct = (results["coverage"]["passed"] / results["coverage"]["total"]) * 100
    print(f"Coverage Tested: {results['coverage']['total']} units | Passed: {results['coverage']['passed']} | Accuracy: {cov_pct:.1f}%\n")

    # -------------------------------------------------------------
    # 3. ANSWER GRANULARITY & EXAM-FIRST RESPONSE AUDIT
    # -------------------------------------------------------------
    print("--- 3. ANSWER GRANULARITY AUDIT ---")
    granularity_tests = [
        # (Query, Granularity Label, Must start with / Direct match, Description)
        ("বঙ্গবন্ধু স্যাটেলাইট-১ কত সালে উৎক্ষেপণ করা হয়?", "YEAR", r"^\*\*উত্তর:\s*২০১৮", "Year first"),
        ("চার্লস ব্যাবেজ কত সালে তুরিন বিশ্ববিদ্যালয়ে বক্তব্য দেন?", "YEAR", r"^\*\*উত্তর:\s*১৮৪০", "Year first"),
        ("বাংলাদেশে কপিরাইট আইন কত সালে প্রণীত হয়?", "YEAR", r"^\*\*উত্তর:\s*২০০০", "Year first"),
        ("তথ্য অধিকার আইন কত সালে পাস হয়?", "YEAR", r"^\*\*উত্তর:\s*২০০৯", "Year first"),
        ("ফেসবুক কত সালে প্রতিষ্ঠিত হয়?", "YEAR", r"^\*\*উত্তর:\s*২০০৪", "Year first"),
        ("কম্পিউটার ভাইরাসের নামকরণ কত সালে করা হয়?", "YEAR", r"^\*\*উত্তর:\s*১৯৮৩", "Year first"),
        ("কম্পিউটারের জনক কে?", "PERSON", r"^\*\*উত্তর:\s*চার্লস ব্যাবেজ", "Person first"),
        ("ইতিহাসের প্রথম কম্পিউটার প্রোগ্রামার কে?", "PERSON", r"^\*\*উত্তর:\s*অ্যাডা লাভলেস", "Person first"),
        ("কম্পিউটার ভাইরাসের নামকরণ কে করেন?", "PERSON", r"^\*\*উত্তর:\s*ফ্রেড কোহেন", "Person first"),
        ("ফেসবুকের প্রতিষ্ঠাতা কে?", "PERSON", r"^\*\*উত্তর:\s*মার্ক জাকারবার্গ", "Person first"),
        ("ডব্লিউডব্লিউডব্লিউ (WWW) এর জনক বা প্রস্তাবক কে?", "PERSON", r"^\*\*উত্তর:\s*স্যার টিম বার্নার্স-লি", "Person first"),
        ("ই-মেইল এবং @ চিহ্নের প্রবর্তক কে?", "PERSON", r"^\*\*উত্তর:\s*রেমন্ড স্যামুয়েল টমলিনসন", "Person first"),
        ("ডিজিটাল বাংলাদেশ রূপকল্পের কয়টি স্তম্ভ?", "COUNT", r"^\*\*উত্তর:\s*৪টি", "Count first"),
        ("শক্তিশালী পাসওয়ার্ড তৈরির কয়টি নিয়ম?", "COUNT", r"^\*\*উত্তর:\s*প্রধান ৫টি", "Count first"),
        ("ই-কমার্স বাণিজ্যের কয়টি প্রধান শর্ত?", "COUNT", r"^\*\*উত্তর:\s*৩টি", "Count first"),
        ("মেটালিক বডিতে হাত দিলে শক লাগে কেন?", "WHY", r"^\*\*উত্তর:\s*কম্পিউটার পাওয়ার লাইনে সঠিক আর্থিং", "Cause first"),
        ("তারিখ ও সময় বারবার ভুল দেখায় কেন?", "WHY", r"^\*\*উত্তর:\s*মাদারবোর্ডের সিএমওএস", "Cause first"),
        ("এক লাইনে বলো কম্পিউটার ভাইরাস কী?", "ONE_LINE", r"^\*\*উত্তর:\*\*\s*কম্পিউটার ভাইরাস হলো", "Single line definition"),
        ("ই-পুর্জি সম্পর্কে সংক্ষেপে বলো।", "SHORT", r"^\*\*উত্তর:\*\*\s*চিনি কলগুলোতে", "Concise short overview"),
        ("কম্পিউটার ভাইরাসের উদাহরণ দাও।", "LIST", r"উল্লেখযোগ্য কম্পিউটার ভাইরাসের নাম", "List of examples"),
        ("কম্পিউটার ভাইরাস কী?", "DEFINITION", r"পাঠ্যবই অনুযায়ী, কম্পিউটার ভাইরাস \(VIRUS", "Direct definition"),
        ("কম্পিউটার ভাইরাস কীভাবে ছড়ায়?", "PROCESS", r"পাঠ্যবই অনুযায়ী, কম্পিউটার ভাইরাস যেভাবে", "Direct spreading process"),
        ("কম্পিউটার ভাইরাস কী এবং কীভাবে ছড়ায়?", "MULTI_INTENT", r"^\*\*১\. কম্পিউটার ভাইরাসের সংজ্ঞা:\*\*", "Multi-intent structured"),
    ]

    for q, g_label, pattern, desc in granularity_tests:
        res, lat = eval_query(q)
        ans = res["answer"].strip()
        matched = bool(re.search(pattern, ans))
        results["granularity"]["total"] += 1
        if matched:
            results["granularity"]["passed"] += 1
        else:
            results["granularity"]["failed"] += 1
            results["granularity"]["cases"].append({"query": q, "type": g_label, "pattern": pattern, "got": ans[:150]})

    gran_pct = (results["granularity"]["passed"] / results["granularity"]["total"]) * 100
    print(f"Granularity Tested: {results['granularity']['total']} | Passed: {results['granularity']['passed']} | Accuracy: {gran_pct:.1f}%\n")

    # -------------------------------------------------------------
    # 4. ADVERSARIAL SCOPE & ZERO-HALLUCINATION AUDIT
    # -------------------------------------------------------------
    print("--- 4. ADVERSARIAL SCOPE & ZERO-HALLUCINATION AUDIT ---")
    adversarial_queries = [
        # Keyword traps (curriculum keywords but unsupported topics)
        "Microsoft Excel-এর SUM কীভাবে ব্যবহার করব?",
        "Microsoft Word-এ টেবিল কীভাবে আঁকব?",
        "কম্পিউটারে পাইথন দিয়ে লুপ প্রোগ্রামিং কীভাবে করব?",
        "কম্পিউটারে ফটোশপে ব্যাকগ্রাউন্ড কীভাবে রিমুভ করব?",
        "এইচটিএমএল (HTML) দিয়ে কীভাবে ওয়েবপেজ বানাব?",
        "এসকিউএল (SQL) দিয়ে ডাটাবেজে টেবিল কীভাবে তৈরি করব?",
        
        # General knowledge / Out-of-curriculum subjects
        "বাংলাদেশের দীর্ঘতম নদীর নাম কী এবং এটি কোথা দিয়ে প্রবাহিত?",
        "১৯৭১ সালের মুক্তিযুদ্ধ এবং সাতজন বীরশ্রেষ্ঠের নাম বল।",
        "পীথাগোরাসের উপপাদ্যটি প্রমাণ কর।",
        "২০২৩ সালের ক্রিকেট বিশ্বকাপ চ্যাম্পিয়ন কোন দেশ?",
        "সুস্বাদু বিরিয়ানি রান্নার সহজ রেসিপি দাও।",
        "বর্তমান পৃথিবীর জনসংখ্যা কত?",
        "আইনস্টাইনের আপেক্ষিকতা তত্ত্ব বুঝিয়ে বল।",
        
        # Absent attributes of known entities (Hallucination traps)
        "কম্পিউটার ভাইরাসের আবিষ্কারক ফ্রেড কোহেন কোন হাই স্কুলে পড়েছেন?",
        "বঙ্গবন্ধু স্যাটেলাইট-১ তৈরিতে মোট কতজন বাঙালি প্রকৌশলী ছিলেন?",
        "চার্লস ব্যাবেজের প্রিয় খাবার কী ছিল?",
        "স্টিভ জবসের প্রথম গাড়ির মডেল কী ছিল?",
        
        # False premises
        "Chapter 2 অনুযায়ী কম্পিউটার ভাইরাস ৫ প্রকার—সেগুলো কী কী?",
        "বঙ্গবন্ধু স্যাটেলাইট-১ কি চাঁদে পাঠানো হয়েছে?",
        "বিল গেটস কি ফেসবুক তৈরি করেছেন?",
        "Chapter 1 অনুযায়ী ফটোশপের প্রধান ৩টি সুবিধা কী?",
    ]

    for q in adversarial_queries:
        res, lat = eval_query(q)
        ans = res["answer"]
        results["scope_hallucination"]["total"] += 1
        
        # Safe response check
        is_safe = False
        if res["is_out_of_curriculum"] or "dataset-এ পাওয়া যায়নি" in ans or "আওতাভুক্ত নয়" in ans:
            is_safe = True
        # Also check false premise refutations
        if "৫ প্রকার" in q and "এমন কোনো তথ্য বা তালিকা নেই" in ans:
            is_safe = True
        elif "চাঁদে" in q and "চাঁদে পাঠানো হয়নি" in ans:
            is_safe = True
        elif "বিল গেটস" in q and "ফেসবুক তৈরি করেননি" in ans:
            is_safe = True

        if is_safe:
            results["scope_hallucination"]["passed"] += 1
        else:
            results["scope_hallucination"]["failed"] += 1
            results["scope_hallucination"]["cases"].append({"query": q, "got": ans[:150]})

    adv_pct = (results["scope_hallucination"]["passed"] / results["scope_hallucination"]["total"]) * 100
    print(f"Scope & Hallucination Tested: {results['scope_hallucination']['total']} | Passed: {results['scope_hallucination']['passed']} | Accuracy: {adv_pct:.1f}%\n")

    # -------------------------------------------------------------
    # 5. BANGLISH & TYPO ROBUSTNESS AUDIT
    # -------------------------------------------------------------
    print("--- 5. BANGLISH & TYPO ROBUSTNESS AUDIT ---")
    banglish_queries = [
        ("strong password bananor rules ki ki?", ["বড় হাতের অক্ষর", "বিশেষ চিহ্ন"]),
        ("password ki?", ["পাসওয়ার্ড"]),
        ("password kivabe strong korbo?", ["বড় হাতের", "সংখ্যা"]),
        ("computer virus ki?", ["ক্ষতিকর প্রোগ্রাম", "VIRUS"]),
        ("virus kivabe choray?", ["পেনড্রাইভ", "ইন্টারনেট"]),
        ("software uninstall kivabe korbo?", ["Control Panel", "Uninstall"]),
        ("e-learning bolte ki bujhai?", ["দূরশিক্ষণ", "শিক্ষা"]),
        ("disk defragmenter er kaj ki?", ["ফাইল", "পাশাপাশি"]),
        ("earthing keno lage?", ["শক", "আর্থিং"]),
        ("e-purjee ki?", ["আখ", "অনুমতিপত্র"]),
        ("kompiutar viruser lokkhon gulo ki?", ["ধীর গতি", "মেমোরি"]),
        ("kompiutare virus dhukle ki hoy?", ["ধীর", "মেমোরি"]),
        ("shoktishali password toirir 5 ti niyom", ["৫টি", "অক্ষর"]),
        ("difragmantar kivabe kaj kore?", ["ফাইল", "হার্ডডিস্ক"]),
        ("cmos battery nosto hole ki hoy?", ["তারিখ", "সময়"]),
    ]

    for q, kw_list in banglish_queries:
        res, lat = eval_query(q)
        ans_canon = canonicalize_bengali(res["answer"])
        passed = not res["is_out_of_curriculum"] and all(canonicalize_bengali(kw) in ans_canon for kw in kw_list)
        results["banglish_typo"]["total"] += 1
        if passed:
            results["banglish_typo"]["passed"] += 1
        else:
            results["banglish_typo"]["failed"] += 1
            results["banglish_typo"]["cases"].append({"query": q, "expected": kw_list, "got": ans[:150]})

    bang_pct = (results["banglish_typo"]["passed"] / results["banglish_typo"]["total"]) * 100
    print(f"Banglish & Typo Tested: {results['banglish_typo']['total']} | Passed: {results['banglish_typo']['passed']} | Accuracy: {bang_pct:.1f}%\n")

    # -------------------------------------------------------------
    # 6. CONTEXTUAL MULTI-TURN CONVERSATION AUDIT
    # -------------------------------------------------------------
    print("--- 6. CONTEXTUAL MULTI-TURN AUDIT ---")
    # Dialogue 1: Computer Virus
    history = []
    # Turn 1
    r1, _ = eval_query("কম্পিউটার ভাইরাস কী?")
    history.append({"query_text": "কম্পিউটার ভাইরাস কী?", "answer_text": r1["answer"], "sources_json": json.dumps(r1["sources"])})
    # Turn 2: Follow-up with pronoun
    r2, _ = eval_query("এটি কীভাবে ছড়ায়?", history=history)
    passed_2 = "পেনড্রাইভ" in r2["answer"] or "ছড়ায়" in r2["answer"]
    results["context"]["total"] += 1
    if passed_2:
        results["context"]["passed"] += 1
    else:
        results["context"]["failed"] += 1
        results["context"]["cases"].append({"turn": 2, "query": "এটি কীভাবে ছড়ায়?", "got": r2["answer"][:120]})
    history.append({"query_text": "এটি কীভাবে ছড়ায়?", "answer_text": r2["answer"], "sources_json": json.dumps(r2["sources"])})

    # Turn 3: Follow-up prevention
    r3, _ = eval_query("এর হাত থেকে বাঁচার উপায় কী?", history=history)
    passed_3 = "অ্যান্টিভাইরাস" in r3["answer"] or "স্ক্যান" in r3["answer"]
    results["context"]["total"] += 1
    if passed_3:
        results["context"]["passed"] += 1
    else:
        results["context"]["failed"] += 1
        results["context"]["cases"].append({"turn": 3, "query": "এর হাত থেকে বাঁচার উপায় কী?", "got": r3["answer"][:120]})

    # Turn 4: Context Switch to Password
    r4, _ = eval_query("পাসওয়ার্ড কী?")
    history.append({"query_text": "পাসওয়ার্ড কী?", "answer_text": r4["answer"], "sources_json": json.dumps(r4["sources"])})
    # Turn 5: Follow-up on new topic
    r5, _ = eval_query("এটি শক্তিশালী করার ৫টি নিয়ম কী?", history=history)
    passed_5 = "বড় হাতের অক্ষর" in r5["answer"] or "সংখ্যা" in r5["answer"]
    results["context"]["total"] += 1
    if passed_5:
        results["context"]["passed"] += 1
    else:
        results["context"]["failed"] += 1
        results["context"]["cases"].append({"turn": 5, "query": "এটি শক্তিশালী করার ৫টি নিয়ম কী?", "got": r5["answer"][:120]})

    ctx_pct = (results["context"]["passed"] / results["context"]["total"]) * 100
    print(f"Contextual Tested: {results['context']['total']} | Passed: {results['context']['passed']} | Accuracy: {ctx_pct:.1f}%\n")

    # -------------------------------------------------------------
    # 7. PREVIOUS 67-TEST BENCHMARK RE-EXECUTION
    # -------------------------------------------------------------
    print("--- 7. RERUNNING PREVIOUS 67-TEST BENCHMARK ---")
    import scripts.large_scale_rag_stress_test as stress_module
    test_results, cat_stats, failure_counts = stress_module.run_full_regression()
    b_passed = sum(1 for t in test_results if t.get("Pass/Fail") == "PASS")
    b_total = len(test_results)
    results["benchmark_67"] = {
        "total": b_total,
        "passed": b_passed,
        "failed": b_total - b_passed,
        "accuracy": round((b_passed / b_total) * 100, 2) if b_total > 0 else 0.0
    }
    print(f"Benchmark 67 Tested: {results['benchmark_67']['total']} | Passed: {results['benchmark_67']['passed']} | Accuracy: {results['benchmark_67']['accuracy']:.2f}%\n")

    # -------------------------------------------------------------
    # 8. API INTEGRATION AUDIT
    # -------------------------------------------------------------
    print("--- 8. API INTEGRATION AUDIT ---")
    from fastapi.testclient import TestClient
    from backend.main import app
    client = TestClient(app)

    # Test 1: Curriculum subjects
    api_r1 = client.get("/api/v1/curriculum/subjects")
    p1 = api_r1.status_code == 200 and "curriculum" in api_r1.json()
    results["api"]["total"] += 1
    if p1: results["api"]["passed"] += 1
    else: results["api"]["failed"] += 1

    # Test 2: Chat query
    api_r2 = client.post("/api/v1/chat/query", json={"query": "কম্পিউটার ভাইরাস কী?", "grade": 9, "subject": "ICT"})
    p2 = api_r2.status_code == 200 and "answer" in api_r2.json() and "session_id" in api_r2.json()
    results["api"]["total"] += 1
    if p2: results["api"]["passed"] += 1
    else: results["api"]["failed"] += 1

    # Test 3: Session history
    sid = api_r2.json().get("session_id", "")
    api_r3 = client.get(f"/api/v1/chat/history/{sid}")
    p3 = api_r3.status_code == 200 and api_r3.json().get("count", 0) >= 1
    results["api"]["total"] += 1
    if p3: results["api"]["passed"] += 1
    else: results["api"]["failed"] += 1

    # Test 4: Out-of-scope through API
    api_r4 = client.post("/api/v1/chat/query", json={"query": "বাংলাদেশের দীর্ঘতম নদী কোনটি?", "grade": 9, "subject": "ICT"})
    p4 = api_r4.status_code == 200 and "dataset-এ পাওয়া যায়নি" in api_r4.json()["answer"]
    results["api"]["total"] += 1
    if p4: results["api"]["passed"] += 1
    else: results["api"]["failed"] += 1

    api_pct = (results["api"]["passed"] / results["api"]["total"]) * 100
    print(f"API Endpoints Tested: {results['api']['total']} | Passed: {results['api']['passed']} | Accuracy: {api_pct:.1f}%\n")

    # -------------------------------------------------------------
    # 9. PERFORMANCE & LATENCY MEASUREMENTS
    # -------------------------------------------------------------
    lats = results["latencies"]
    min_lat = min(lats) if lats else 0
    max_lat = max(lats) if lats else 0
    avg_lat = sum(lats) / len(lats) if lats else 0
    print(f"Latency: Min: {min_lat*1000:.1f}ms | Avg: {avg_lat*1000:.1f}ms | Max: {max_lat*1000:.1f}ms")

    # -------------------------------------------------------------
    # TOTAL SCORE CALCULATION
    # -------------------------------------------------------------
    total_audited = (
        results["coverage"]["total"] +
        results["granularity"]["total"] +
        results["scope_hallucination"]["total"] +
        results["banglish_typo"]["total"] +
        results["context"]["total"] +
        results["benchmark_67"]["total"] +
        results["api"]["total"]
    )
    total_passed = (
        results["coverage"]["passed"] +
        results["granularity"]["passed"] +
        results["scope_hallucination"]["passed"] +
        results["banglish_typo"]["passed"] +
        results["context"]["passed"] +
        results["benchmark_67"]["passed"] +
        results["api"]["passed"]
    )
    total_failed = total_audited - total_passed
    overall_pct = (total_passed / total_audited) * 100

    print("=" * 80)
    print(f"AUDIT COMPLETE: Total Executed Tests: {total_audited} | Passed: {total_passed} | Failed: {total_failed} ({overall_pct:.2f}%)")
    print("=" * 80)

    # Save complete JSON audit result
    audit_output_path = os.path.join("scripts", "final_independent_audit_report.json")
    with open(audit_output_path, "w", encoding="utf-8") as f:
        json.dump({
            "summary": {
                "total_executed": total_audited,
                "total_passed": total_passed,
                "total_failed": total_failed,
                "overall_accuracy_pct": overall_pct,
                "latency_ms": {"min": min_lat*1000, "avg": avg_lat*1000, "max": max_lat*1000}
            },
            "category_metrics": {
                "dataset_coverage": results["coverage"],
                "answer_granularity": results["granularity"],
                "scope_hallucination": results["scope_hallucination"],
                "banglish_typo": results["banglish_typo"],
                "contextual_multiturn": results["context"],
                "benchmark_67": results["benchmark_67"],
                "api_integration": results["api"]
            }
        }, f, indent=2, ensure_ascii=False)
    print(f"Detailed audit saved to: {audit_output_path}")

    return {
        "total_audited": total_audited,
        "total_passed": total_passed,
        "total_failed": total_failed,
        "overall_pct": overall_pct,
        "results": results
    }

if __name__ == "__main__":
    run_audit()
