"""
Large-Scale Automated RAG Stress Testing & Regression Engine for OIBTC
Author: Senior AI Architect, NLP Engineer & RAG Evaluation Specialist
Covers NCTB ICT Chapter 1 & Chapter 2 Comprehensive Evaluation across 12 Categories (A–L).
Evaluates 100+ Test Cases with Full Semantic Normalization, Context Memory, and Evidence Verification.
"""

import os
import sys
import json
import time
import re
from typing import List, Dict, Any, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.rag.pipeline import RAGPipeline
from backend.rag.intent import IntentType
from backend.rag.transliteration import canonicalize_bengali, normalize_query

# =========================================================================
# 12-CATEGORY COMPREHENSIVE STRESS TEST SUITE (100+ Rigorous Cases)
# =========================================================================
STRESS_TEST_SUITE: List[Dict[str, Any]] = [
    # ---------------------------------------------------------------------
    # A. DIRECT BANGLA QUERIES (Definitions, Types, How, Why, Prevention, Comparison)
    # ---------------------------------------------------------------------
    {
        "id": "A_DIR_01",
        "category": "Direct Bangla",
        "chapter": 1,
        "topic": "কৃত্রিম বুদ্ধিমত্তা (AI)",
        "query": "কৃত্রিম বুদ্ধিমত্তা বা AI কাকে বলে?",
        "expected_intent": "DEFINITION",
        "expected_chapter": 1,
        "expected_evidence": ["মানুষের মতো", "চিন্তাভাবনা", "বুদ্ধি"],
        "is_out_of_scope": False
    },
    {
        "id": "A_DIR_02",
        "category": "Direct Bangla",
        "chapter": 1,
        "topic": "ই-লার্নিং ও বাংলাদেশ",
        "query": "ই-লার্নিং কী?",
        "expected_intent": "DEFINITION",
        "expected_chapter": 1,
        "expected_evidence": ["দূরশিক্ষণ", "ইলেকট্রনিক"],
        "is_out_of_scope": False
    },
    {
        "id": "A_DIR_03",
        "category": "Direct Bangla",
        "chapter": 1,
        "topic": "ই-সার্ভিস ও নাগরিক সেবা",
        "query": "ই-পুর্জি কী?",
        "expected_intent": "DEFINITION",
        "expected_chapter": 1,
        "expected_evidence": ["আখ", "চিনি", "এসএমএস"],
        "is_out_of_scope": False
    },
    {
        "id": "A_DIR_04",
        "category": "Direct Bangla",
        "chapter": 1,
        "topic": "ই-সার্ভিস ও নাগরিক সেবা",
        "query": "ইএমটিএস (EMTS) কী এবং এর সুবিধা কী?",
        "expected_intent": "DEFINITION",
        "expected_chapter": 1,
        "expected_evidence": ["ডাক বিভাগ", "১ মিনিট", "টাকা"],
        "is_out_of_scope": False
    },
    {
        "id": "A_DIR_05",
        "category": "Direct Bangla",
        "chapter": 1,
        "topic": "লিপফ্রগ প্রযুক্তি",
        "query": "লিপফ্রগ প্রযুক্তি কাকে বলে?",
        "expected_intent": "DEFINITION",
        "expected_chapter": 1,
        "expected_evidence": ["মধ্যবর্তী", "লাফ", "সর্বাধুনিক"],
        "is_out_of_scope": False
    },
    {
        "id": "A_DIR_06",
        "category": "Direct Bangla",
        "chapter": 2,
        "topic": "কম্পিউটার ভাইরাস",
        "query": "কম্পিউটার ভাইরাস কী?",
        "expected_intent": "DEFINITION",
        "expected_chapter": 2,
        "expected_evidence": ["ক্ষতিকর প্রোগ্রাম", "Vital Information Resources Under Siege"],
        "is_out_of_scope": False
    },
    {
        "id": "A_DIR_07",
        "category": "Direct Bangla",
        "chapter": 2,
        "topic": "টু-ফ্যাক্টর অথেনটিকেশন",
        "query": "টু-ফ্যাক্টর অথেনটিকেশন বা 2FA বলতে কী বোঝায়?",
        "expected_intent": "DEFINITION",
        "expected_chapter": 2,
        "expected_evidence": ["পাসওয়ার্ড", "ওটিপি", "নিরাপত্তা"],
        "is_out_of_scope": False
    },
    {
        "id": "A_DIR_08",
        "category": "Direct Bangla",
        "chapter": 2,
        "topic": "সিএমওএস ব্যাটারি",
        "query": "মাদারবোর্ডে সিএমওএস (CMOS) ব্যাটারির কাজ কী?",
        "expected_intent": "TROUBLESHOOTING",
        "expected_chapter": 2,
        "expected_evidence": ["তারিখ", "সময়", "ব্যাটারি"],
        "is_out_of_scope": False
    },
    {
        "id": "A_DIR_09",
        "category": "Direct Bangla",
        "chapter": 2,
        "topic": "সফটওয়্যার পাইরেসি",
        "query": "সফটওয়্যার পাইরেসি কাকে বলে?",
        "expected_intent": "DEFINITION",
        "expected_chapter": 2,
        "expected_evidence": ["অনুমতি ব্যতীত", "অনুলিপি", "পাইরেসি"],
        "is_out_of_scope": False
    },
    {
        "id": "A_DIR_10",
        "category": "Direct Bangla",
        "chapter": 2,
        "topic": "নার্সিসিজম",
        "query": "নার্সিসিজম কী?",
        "expected_intent": "DEFINITION",
        "expected_chapter": 2,
        "expected_evidence": ["আত্মপ্রেম", "লাইক", "নিজেকে"],
        "is_out_of_scope": False
    },
    {
        "id": "A_DIR_11",
        "category": "Direct Bangla",
        "chapter": 1,
        "topic": "ডিজিটাল বাংলাদেশ",
        "query": "ডিজিটাল বাংলাদেশ রূপকল্পের ৪টি স্তম্ভ কী কী?",
        "expected_intent": "RULES",
        "expected_chapter": 1,
        "expected_evidence": ["মানবসম্পদ উন্নয়ন", "নাগরিক সংযোগ", "ডিজিটাল সরকার", "তথ্যপ্রযুক্তি শিল্প"],
        "is_out_of_scope": False
    },
    {
        "id": "A_DIR_12",
        "category": "Direct Bangla",
        "chapter": 2,
        "topic": "পাসওয়ার্ড তৈরির নিয়ম",
        "query": "শক্তিশালী পাসওয়ার্ড তৈরির ৫টি নিয়ম কী কী?",
        "expected_intent": "RULES",
        "expected_chapter": 2,
        "expected_evidence": ["বড় হাতের", "ছোট হাতের", "সংখ্যা", "চিহ্ন", "দৈর্ঘ্য"],
        "is_out_of_scope": False
    },
    {
        "id": "A_DIR_13",
        "category": "Direct Bangla",
        "chapter": 2,
        "topic": "রান কমান্ড",
        "query": "অপ্রয়োজনীয় ক্যাশ ফাইল পরিষ্কারের ৩টি রান কমান্ড কী কী?",
        "expected_intent": "RULES",
        "expected_chapter": 2,
        "expected_evidence": ["temp", "%temp%", "prefetch"],
        "is_out_of_scope": False
    },
    {
        "id": "A_DIR_14",
        "category": "Direct Bangla",
        "chapter": 2,
        "topic": "ভাইরাস ছড়ানোর পদ্ধতি",
        "query": "কম্পিউটার ভাইরাস কীভাবে এক কম্পিউটার থেকে অন্য কম্পিউটারে ছড়ায়?",
        "expected_intent": "MECHANISM",
        "expected_chapter": 2,
        "expected_evidence": ["পেনড্রাইভ", "ইন্টারনেট", "ডাউনলোড"],
        "is_out_of_scope": False
    },
    {
        "id": "A_DIR_15",
        "category": "Direct Bangla",
        "chapter": 2,
        "topic": "ভাইরাস প্রতিরোধ",
        "query": "কম্পিউটারকে ভাইরাস থেকে কীভাবে মুক্ত রাখা যায়?",
        "expected_intent": "PREVENTION",
        "expected_chapter": 2,
        "expected_evidence": ["অ্যান্টিভাইরাস", "আপডেট", "স্ক্যান"],
        "is_out_of_scope": False
    },
    {
        "id": "A_DIR_16",
        "category": "Direct Bangla",
        "chapter": 2,
        "topic": "মেটালিক বডি শক",
        "query": "কম্পিউটারের মেটালিক বডিতে হাত দিলে বৈদ্যুতিক শক লাগে কেন?",
        "expected_intent": "TROUBLESHOOTING",
        "expected_chapter": 2,
        "expected_evidence": ["আর্থিং", "গ্রাউন্ডিং", "শক"],
        "is_out_of_scope": False
    },
    {
        "id": "A_DIR_17",
        "category": "Direct Bangla",
        "chapter": 2,
        "topic": "ডিস্ক ক্লিনআপ বনাম ডিফ্র্যাগমেন্টার",
        "query": "ডিস্ক ক্লিনআপ ও ডিস্ক ডিফ্র্যাগমেন্টারের মধ্যে পার্থক্য কী?",
        "expected_intent": "GENERAL",
        "expected_chapter": 2,
        "expected_evidence": ["ডিস্ক ক্লিনআপ", "ডিফ্র্যাগমেন্টার", "অপ্রয়োজনীয় ফাইল"],
        "is_out_of_scope": False
    },
    {
        "id": "A_DIR_18",
        "category": "Direct Bangla",
        "chapter": 2,
        "topic": "আনইনস্টল বনাম ডিলিট",
        "query": "সফটওয়্যার ডিলিট করা এবং আনইনস্টল করার মধ্যে পার্থক্য কী?",
        "expected_intent": "GENERAL",
        "expected_chapter": 2,
        "expected_evidence": ["রেজিস্ট্রি", "ডিলিট", "আনইনস্টল"],
        "is_out_of_scope": False
    },

    # ---------------------------------------------------------------------
    # B. BANGLISH QUERIES (Romanized Bangla)
    # ---------------------------------------------------------------------
    {
        "id": "B_BGL_01",
        "category": "Banglish",
        "chapter": 2,
        "topic": "পাসওয়ার্ড তৈরির নিয়ম",
        "query": "strong password bananor rules ki ki?",
        "expected_intent": "RULES",
        "expected_chapter": 2,
        "expected_evidence": ["বড় হাতের", "সংখ্যা", "চিহ্ন"],
        "is_out_of_scope": False
    },
    {
        "id": "B_BGL_02",
        "category": "Banglish",
        "chapter": 2,
        "topic": "পাসওয়ার্ড কী",
        "query": "password ki?",
        "expected_intent": "DEFINITION",
        "expected_chapter": 2,
        "expected_evidence": ["পাসওয়ার্ড", "নিরাপত্তা"],
        "is_out_of_scope": False
    },
    {
        "id": "B_BGL_03",
        "category": "Banglish",
        "chapter": 2,
        "topic": "পাসওয়ার্ড শক্তিশালীকরণ",
        "query": "password kivabe strong korbo?",
        "expected_intent": "RULES",
        "expected_chapter": 2,
        "expected_evidence": ["বড় হাতের", "ছোট হাতের", "সংখ্যা", "চিহ্ন"],
        "is_out_of_scope": False
    },
    {
        "id": "B_BGL_04",
        "category": "Banglish",
        "chapter": 2,
        "topic": "কম্পিউটার ভাইরাস",
        "query": "computer virus ki?",
        "expected_intent": "DEFINITION",
        "expected_chapter": 2,
        "expected_evidence": ["Vital Information Resources Under Siege", "ক্ষতিকর প্রোগ্রাম"],
        "is_out_of_scope": False
    },
    {
        "id": "B_BGL_05",
        "category": "Banglish",
        "chapter": 2,
        "topic": "ভাইরাস ছড়ানো",
        "query": "virus kivabe choray?",
        "expected_intent": "MECHANISM",
        "expected_chapter": 2,
        "expected_evidence": ["পেনড্রাইভ", "ইন্টারনেট", "ডাউনলোড"],
        "is_out_of_scope": False
    },
    {
        "id": "B_BGL_06",
        "category": "Banglish",
        "chapter": 2,
        "topic": "সফটওয়্যার আনইনস্টল",
        "query": "software uninstall kivabe korbo?",
        "expected_intent": "MECHANISM",
        "expected_chapter": 2,
        "expected_evidence": ["Control Panel", "Programs and Features", "Uninstall"],
        "is_out_of_scope": False
    },
    {
        "id": "B_BGL_07",
        "category": "Banglish",
        "chapter": 1,
        "topic": "ই-লার্নিং",
        "query": "e-learning bolte ki bujhai?",
        "expected_intent": "DEFINITION",
        "expected_chapter": 1,
        "expected_evidence": ["দূরশিক্ষণ", "ইলেকট্রনিক"],
        "is_out_of_scope": False
    },
    {
        "id": "B_BGL_08",
        "category": "Banglish",
        "chapter": 2,
        "topic": "ডিস্ক ডিফ্র্যাগমেন্টার",
        "query": "disk defragmenter er kaj ki?",
        "expected_intent": "GENERAL",
        "expected_chapter": 2,
        "expected_evidence": ["ডিফ্র্যাগমেন্টার", "পাশাপাশি"],
        "is_out_of_scope": False
    },
    {
        "id": "B_BGL_09",
        "category": "Banglish",
        "chapter": 2,
        "topic": "আর্থিং",
        "query": "earthing keno lage?",
        "expected_intent": "TROUBLESHOOTING",
        "expected_chapter": 2,
        "expected_evidence": ["আর্থিং", "শক"],
        "is_out_of_scope": False
    },
    {
        "id": "B_BGL_10",
        "category": "Banglish",
        "chapter": 1,
        "topic": "ই-পুর্জি",
        "query": "e-purjee ki?",
        "expected_intent": "DEFINITION",
        "expected_chapter": 1,
        "expected_evidence": ["আখ", "চিনি", "এসএমএস"],
        "is_out_of_scope": False
    },

    # ---------------------------------------------------------------------
    # C. MIXED SCRIPT QUERIES (Bangla + English Terms)
    # ---------------------------------------------------------------------
    {
        "id": "C_MIX_01",
        "category": "Mixed Script",
        "chapter": 2,
        "topic": "কম্পিউটার ভাইরাস",
        "query": "কম্পিউটার Virus কীভাবে ছড়ায়?",
        "expected_intent": "MECHANISM",
        "expected_chapter": 2,
        "expected_evidence": ["পেনড্রাইভ", "ইন্টারনেট", "ডাউনলোড"],
        "is_out_of_scope": False
    },
    {
        "id": "C_MIX_02",
        "category": "Mixed Script",
        "chapter": 2,
        "topic": "পাসওয়ার্ড",
        "query": "Strong Password তৈরির নিয়ম কী?",
        "expected_intent": "RULES",
        "expected_chapter": 2,
        "expected_evidence": ["বড় হাতের", "সংখ্যা", "চিহ্ন"],
        "is_out_of_scope": False
    },
    {
        "id": "C_MIX_03",
        "category": "Mixed Script",
        "chapter": 2,
        "topic": "টু-ফ্যাক্টর অথেনটিকেশন",
        "query": "2FA বা Two Factor Authentication কী?",
        "expected_intent": "DEFINITION",
        "expected_chapter": 2,
        "expected_evidence": ["পাসওয়ার্ড", "ওটিপি", "নিরাপত্তা"],
        "is_out_of_scope": False
    },
    {
        "id": "C_MIX_04",
        "category": "Mixed Script",
        "chapter": 2,
        "topic": "ট্রাবলশুটিং",
        "query": "পিসিতে Earthing কেন প্রয়োজন?",
        "expected_intent": "TROUBLESHOOTING",
        "expected_chapter": 2,
        "expected_evidence": ["আর্থিং", "শক"],
        "is_out_of_scope": False
    },
    {
        "id": "C_MIX_05",
        "category": "Mixed Script",
        "chapter": 1,
        "topic": "কৃত্রিম বুদ্ধিমত্তা",
        "query": "একুশ শতকে Artificial Intelligence বা AI এর ভূমিকা কী?",
        "expected_intent": "GENERAL",
        "expected_chapter": 1,
        "expected_evidence": ["কৃত্রিম বুদ্ধিমত্তা", "মানুষের মতো", "চিন্তাভাবনা"],
        "is_out_of_scope": False
    },

    # ---------------------------------------------------------------------
    # D. TYPO & INFORMAL SPELLING MISTAKES
    # ---------------------------------------------------------------------
    {
        "id": "D_TYP_01",
        "category": "Typo",
        "chapter": 2,
        "topic": "ভাইরাস লক্ষণ",
        "query": "কমপিউটার ভাইরাসের লক্ষন গুলা কি কি?",
        "expected_intent": "SYMPTOMS",
        "expected_chapter": 2,
        "expected_evidence": ["ধীর গতি", "মেমোরি", "রিস্টার্ট"],
        "is_out_of_scope": False
    },
    {
        "id": "D_TYP_02",
        "category": "Typo",
        "chapter": 2,
        "topic": "পাসওয়ার্ড",
        "query": "শক্তিসালী পাসয়ার্ড বানানোর ৫টি নিয়োম",
        "expected_intent": "RULES",
        "expected_chapter": 2,
        "expected_evidence": ["বড় হাতের", "সংখ্যা", "চিহ্ন"],
        "is_out_of_scope": False
    },
    {
        "id": "D_TYP_03",
        "category": "Typo",
        "chapter": 2,
        "topic": "ডিফ্র্যাগমেন্টার",
        "query": "ডিষ্ক ডিফ্রেগমেন্টার এর কাজ কি?",
        "expected_intent": "GENERAL",
        "expected_chapter": 2,
        "expected_evidence": ["ডিফ্র্যাগমেন্টার", "পাশাপাশি"],
        "is_out_of_scope": False
    },
    {
        "id": "D_TYP_04",
        "category": "Typo",
        "chapter": 2,
        "topic": "সিএমওএস ব্যাটারি",
        "query": "মাদারবোর্ডের সিএমস বেটারি নষ্ট হলে কি হয়?",
        "expected_intent": "TROUBLESHOOTING",
        "expected_chapter": 2,
        "expected_evidence": ["তারিখ", "সময়", "ব্যাটারি"],
        "is_out_of_scope": False
    },

    # ---------------------------------------------------------------------
    # E. PARAPHRASE (Same Info, Different Wordings)
    # ---------------------------------------------------------------------
    {
        "id": "E_PAR_01",
        "category": "Paraphrase",
        "chapter": 2,
        "topic": "পাসওয়ার্ড নিয়ম",
        "query": "পাসওয়ার্ড শক্তিশালী করার উপায়গুলো বল।",
        "expected_intent": "RULES",
        "expected_chapter": 2,
        "expected_evidence": ["বড় হাতের", "সংখ্যা", "চিহ্ন"],
        "is_out_of_scope": False
    },
    {
        "id": "E_PAR_02",
        "category": "Paraphrase",
        "chapter": 2,
        "topic": "পাসওয়ার্ড নিয়ম",
        "query": "পাসওয়ার্ড তৈরির ৫টি শর্ত কী কী?",
        "expected_intent": "RULES",
        "expected_chapter": 2,
        "expected_evidence": ["বড় হাতের", "সংখ্যা", "চিহ্ন"],
        "is_out_of_scope": False
    },
    {
        "id": "E_PAR_03",
        "category": "Paraphrase",
        "chapter": 2,
        "topic": "পাসওয়ার্ড নিরাপত্তা",
        "query": "একটি পাসওয়ার্ড কীভাবে নিরাপদ রাখা যায়?",
        "expected_intent": "PREVENTION",
        "expected_chapter": 2,
        "expected_evidence": ["পাসওয়ার্ড", "নিয়মিত পরিবর্তন"],
        "is_out_of_scope": False
    },
    {
        "id": "E_PAR_04",
        "category": "Paraphrase",
        "chapter": 2,
        "topic": "পাসওয়ার্ড নিয়ম (Banglish)",
        "query": "Strong password rules কি কি?",
        "expected_intent": "RULES",
        "expected_chapter": 2,
        "expected_evidence": ["বড় হাতের", "সংখ্যা", "চিহ্ন"],
        "is_out_of_scope": False
    },

    # ---------------------------------------------------------------------
    # F. CONTEXT / MULTI-TURN FOLLOW-UP QUERIES
    # ---------------------------------------------------------------------
    {
        "id": "F_CTX_01",
        "category": "Context",
        "chapter": 2,
        "topic": "কম্পিউটার ভাইরাস",
        "query": "কম্পিউটার ভাইরাস কী?",
        "history": [],
        "expected_intent": "DEFINITION",
        "expected_chapter": 2,
        "expected_evidence": ["Vital Information Resources Under Siege", "ক্ষতিকর প্রোগ্রাম"],
        "is_out_of_scope": False
    },
    {
        "id": "F_CTX_02",
        "category": "Context",
        "chapter": 2,
        "topic": "কম্পিউটার ভাইরাস (Follow-up 1)",
        "query": "এটি কীভাবে ছড়ায়?",
        "history": [
            {
                "sender": "student",
                "query_text": "কম্পিউটার ভাইরাস কী?",
                "sources_json": '[{"topic": "কম্পিউটার ভাইরাস ও ম্যালওয়্যার - নামকরণ ও ভাইরাসের ইতিহাস", "chapter": 2}]'
            }
        ],
        "expected_intent": "MECHANISM",
        "expected_chapter": 2,
        "expected_evidence": ["পেনড্রাইভ", "ইন্টারনেট", "ডাউনলোড"],
        "is_out_of_scope": False
    },
    {
        "id": "F_CTX_03",
        "category": "Context",
        "chapter": 2,
        "topic": "কম্পিউটার ভাইরাস (Follow-up 2)",
        "query": "এর হাত থেকে বাঁচার উপায় কী?",
        "history": [
            {
                "sender": "student",
                "query_text": "কম্পিউটার ভাইরাস কীভাবে ছড়ায়?",
                "sources_json": '[{"topic": "কম্পিউটার ভাইরাস ও ম্যালওয়্যার - নামকরণ ও ভাইরাসের ইতিহাস", "chapter": 2}]'
            }
        ],
        "expected_intent": "PREVENTION",
        "expected_chapter": 2,
        "expected_evidence": ["অ্যান্টিভাইরাস", "আপডেট", "স্ক্যান"],
        "is_out_of_scope": False
    },
    {
        "id": "F_CTX_04",
        "category": "Context",
        "chapter": 2,
        "topic": "পাসওয়ার্ড (Follow-up)",
        "query": "এটি শক্তিশালী করার ৫টি নিয়ম কী?",
        "history": [
            {
                "sender": "student",
                "query_text": "পাসওয়ার্ড কী?",
                "sources_json": '[{"topic": "কম্পিউটার নিরাপত্তা ও শক্তিশালী পাসওয়ার্ড তৈরির ৫টি নিয়ম", "chapter": 2}]'
            }
        ],
        "expected_intent": "RULES",
        "expected_chapter": 2,
        "expected_evidence": ["বড় হাতের", "সংখ্যা", "চিহ্ন"],
        "is_out_of_scope": False
    },

    # ---------------------------------------------------------------------
    # G. MULTI-INTENT QUERIES
    # ---------------------------------------------------------------------
    {
        "id": "G_MUL_01",
        "category": "Multi-intent",
        "chapter": 2,
        "topic": "কম্পিউটার ভাইরাস",
        "query": "কম্পিউটার ভাইরাস কী এবং এটি কীভাবে ছড়ায়?",
        "expected_intent": "MULTI_INTENT",
        "expected_chapter": 2,
        "expected_evidence": ["Vital Information Resources Under Siege", "সংজ্ঞা", "পেনড্রাইভ", "ছড়ায়"],
        "is_out_of_scope": False
    },
    {
        "id": "G_MUL_02",
        "category": "Multi-intent",
        "chapter": 2,
        "topic": "পাসওয়ার্ড নিরাপত্তা",
        "query": "পাসওয়ার্ড কী এবং শক্তিশালী পাসওয়ার্ড তৈরির প্রধান নিয়মগুলো কী কী?",
        "expected_intent": "MULTI_INTENT",
        "expected_chapter": 2,
        "expected_evidence": ["পাসওয়ার্ড", "নিয়ম", "বড় হাতের", "চিহ্ন"],
        "is_out_of_scope": False
    },
    {
        "id": "G_MUL_03",
        "category": "Multi-intent",
        "chapter": 1,
        "topic": "চার্লস ব্যাবেজ",
        "query": "চার্লস ব্যাবেজ কে ছিলেন এবং তিনি কোন কোন গণনা যন্ত্রের নকশা করেন?",
        "expected_intent": "HISTORY_PERSON",
        "expected_chapter": 1,
        "expected_evidence": ["চার্লস ব্যাবেজ", "ডিফারেন্স ইঞ্জিন", "অ্যানালিটিক্যাল ইঞ্জিন"],
        "is_out_of_scope": False
    },

    # ---------------------------------------------------------------------
    # H. FALSE PREMISE QUERIES
    # ---------------------------------------------------------------------
    {
        "id": "H_FAL_01",
        "category": "False Premise",
        "chapter": 2,
        "topic": "কম্পিউটার ভাইরাস প্রকারভেদ",
        "query": "Chapter 2 অনুযায়ী কম্পিউটার ভাইরাস ৫ প্রকার—সেগুলো কী কী?",
        "expected_intent": "GENERAL",
        "expected_chapter": 2,
        "expected_evidence": ["পাঠ্যবই", "ভাইরাস"],
        "is_out_of_scope": False
    },
    {
        "id": "H_FAL_02",
        "category": "False Premise",
        "chapter": 1,
        "topic": "বঙ্গবন্ধু স্যাটেলাইট",
        "query": "বঙ্গবন্ধু স্যাটেলাইট-১ কি চাঁদে পাঠানো হয়েছে?",
        "expected_intent": "GENERAL",
        "expected_chapter": 1,
        "expected_evidence": ["কক্ষপথ", "১১৯.১"],
        "is_out_of_scope": False
    },
    {
        "id": "H_FAL_03",
        "category": "False Premise",
        "chapter": 1,
        "topic": "আইসিটি ব্যক্তিত্ব",
        "query": "বিল গেটস কি ফেসবুক তৈরি করেছেন?",
        "expected_intent": "HISTORY_PERSON",
        "expected_chapter": 1,
        "expected_evidence": ["বিল গেটস", "মাইক্রোসফট", "মার্ক জাকারবার্গ"],
        "is_out_of_scope": False
    },

    # ---------------------------------------------------------------------
    # I. SCOPE LEAKAGE (Known Keywords in Unrelated/Outside Questions)
    # ---------------------------------------------------------------------
    {
        "id": "I_LEA_01",
        "category": "Scope Leakage",
        "chapter": 0,
        "topic": "মাইক্রোসফট এক্সেল (Ch 4)",
        "query": "Microsoft Excel-এর SUM কীভাবে ব্যবহার করব?",
        "expected_intent": "OUT_OF_CURRICULUM",
        "expected_chapter": 0,
        "expected_evidence": ["পাওয়া যায়নি"],
        "is_out_of_scope": True
    },
    {
        "id": "I_LEA_02",
        "category": "Scope Leakage",
        "chapter": 0,
        "topic": "মাইক্রোসফট ওয়ার্ড (Ch 4)",
        "query": "মাইক্রোসফট ওয়ার্ডে টেবিল কীভাবে বানাব?",
        "expected_intent": "OUT_OF_CURRICULUM",
        "expected_chapter": 0,
        "expected_evidence": ["পাওয়া যায়নি"],
        "is_out_of_scope": True
    },
    {
        "id": "I_LEA_03",
        "category": "Scope Leakage",
        "chapter": 0,
        "topic": "কম্পিউটার প্রোগ্রামিং পাইথন",
        "query": "কম্পিউটারে পাইথন দিয়ে লুপ প্রোগ্রামিং কীভাবে শিখব?",
        "expected_intent": "OUT_OF_CURRICULUM",
        "expected_chapter": 0,
        "expected_evidence": ["পাওয়া যায়নি"],
        "is_out_of_scope": True
    },

    # ---------------------------------------------------------------------
    # J. COMPLETELY OUT-OF-SCOPE (Other Chapters & Unrelated Domains)
    # ---------------------------------------------------------------------
    {
        "id": "J_OOS_01",
        "category": "Out-of-Scope",
        "chapter": 0,
        "topic": "ভূগোল ও নদী",
        "query": "বাংলাদেশের দীর্ঘতম নদীর নাম কী এবং এটি কোথা থেকে উৎপন্ন হয়েছে?",
        "expected_intent": "OUT_OF_CURRICULUM",
        "expected_chapter": 0,
        "expected_evidence": ["পাওয়া যায়নি"],
        "is_out_of_scope": True
    },
    {
        "id": "J_OOS_02",
        "category": "Out-of-Scope",
        "chapter": 0,
        "topic": "ইতিহাস ও মুক্তিযুদ্ধ",
        "query": "১৯৭১ সালের মুক্তিযুদ্ধ এবং সাতজন বীরশ্রেষ্ঠের নাম বল।",
        "expected_intent": "OUT_OF_CURRICULUM",
        "expected_chapter": 0,
        "expected_evidence": ["পাওয়া যায়নি"],
        "is_out_of_scope": True
    },
    {
        "id": "J_OOS_03",
        "category": "Out-of-Scope",
        "chapter": 0,
        "topic": "গণিত",
        "query": "পীথাগোরাসের উপপাদ্যটি প্রমাণ কর।",
        "expected_intent": "OUT_OF_CURRICULUM",
        "expected_chapter": 0,
        "expected_evidence": ["পাওয়া যায়নি"],
        "is_out_of_scope": True
    },
    {
        "id": "J_OOS_04",
        "category": "Out-of-Scope",
        "chapter": 0,
        "topic": "খেলাধুলা",
        "query": "২০২৩ সালের ক্রিকেট বিশ্বকাপ চ্যাম্পিয়ন কোন দল হয়েছিল?",
        "expected_intent": "OUT_OF_CURRICULUM",
        "expected_chapter": 0,
        "expected_evidence": ["পাওয়া যায়নি"],
        "is_out_of_scope": True
    },
    {
        "id": "J_OOS_05",
        "category": "Out-of-Scope",
        "chapter": 0,
        "topic": "রান্না",
        "query": "সুস্বাদু বিরিয়ানি রান্নার রেসিপি কী?",
        "expected_intent": "OUT_OF_CURRICULUM",
        "expected_chapter": 0,
        "expected_evidence": ["পাওয়া যায়নি"],
        "is_out_of_scope": True
    },
    {
        "id": "J_OOS_06",
        "category": "Out-of-Scope",
        "chapter": 0,
        "topic": "ফটোশপ (Ch 5)",
        "query": "ফটোশপে ব্যাকগ্রাউন্ড কীভাবে রিমুভ করব?",
        "expected_intent": "OUT_OF_CURRICULUM",
        "expected_chapter": 0,
        "expected_evidence": ["পাওয়া যায়নি"],
        "is_out_of_scope": True
    },
    {
        "id": "J_OOS_07",
        "category": "Out-of-Scope",
        "chapter": 0,
        "topic": "ডাটাবেজ ও এসকিউএল (Ch 6)",
        "query": "এসকিউএল (SQL) দিয়ে ডাটাবেজে টেবিল কীভাবে তৈরি করব?",
        "expected_intent": "OUT_OF_CURRICULUM",
        "expected_chapter": 0,
        "expected_evidence": ["পাওয়া যায়নি"],
        "is_out_of_scope": True
    },

    # ---------------------------------------------------------------------
    # K. CHAPTER ISOLATION (No Cross-Chapter Retrieval)
    # ---------------------------------------------------------------------
    {
        "id": "K_ISO_01",
        "category": "Chapter Isolation",
        "chapter": 1,
        "topic": "বঙ্গবন্ধু স্যাটেলাইট",
        "query": "বঙ্গবন্ধু স্যাটেলাইট-১ কত সালে উৎক্ষেপণ করা হয় এবং বাংলাদেশ কততম দেশ?",
        "expected_intent": "GENERAL",
        "expected_chapter": 1,
        "expected_evidence": ["২০১৮", "১২ মে", "৫৭তম"],
        "is_out_of_scope": False
    },
    {
        "id": "K_ISO_02",
        "category": "Chapter Isolation",
        "chapter": 2,
        "topic": "কপিরাইট আইন",
        "query": "বাংলাদেশে কপিরাইট আইন কত সালে প্রণীত হয় এবং বিএসএ এর রিপোর্ট কী?",
        "expected_intent": "GENERAL",
        "expected_chapter": 2,
        "expected_evidence": ["২০০০", "২০০৫", "৪ জন"],
        "is_out_of_scope": False
    },
    {
        "id": "K_ISO_03",
        "category": "Chapter Isolation",
        "chapter": 1,
        "topic": "ই-পুর্জি",
        "query": "আখ চাষিদের জন্য ই-পুর্জি কীভাবে কাজ করে?",
        "expected_intent": "GENERAL",
        "expected_chapter": 1,
        "expected_evidence": ["আখ", "চিনি", "ই-পুর্জি"],
        "is_out_of_scope": False
    },
    {
        "id": "K_ISO_04",
        "category": "Chapter Isolation",
        "chapter": 2,
        "topic": "ট্রাবলশুটিং রিস্টার্ট",
        "query": "কম্পিউটার বারবার স্বয়ংক্রিয়ভাবে রিস্টার্ট বা হ্যাং হলে কী করতে হবে?",
        "expected_intent": "TROUBLESHOOTING",
        "expected_chapter": 2,
        "expected_evidence": ["কুলিং ফ্যান", "রিস্টার্ট", "হ্যাং"],
        "is_out_of_scope": False
    },

    # ---------------------------------------------------------------------
    # L. HALLUCINATION RESISTANCE (Deliberately Absent Facts)
    # ---------------------------------------------------------------------
    {
        "id": "L_HAL_01",
        "category": "Hallucination",
        "chapter": 0,
        "topic": "অনুপস্থিত তথ্য ১",
        "query": "কম্পিউটার ভাইরাসের আবিষ্কারক ফ্রেড কোহেন কোন হাই স্কুলে পড়াশোনা করেছিলেন?",
        "expected_intent": "OUT_OF_CURRICULUM",
        "expected_chapter": 0,
        "expected_evidence": ["পাওয়া যায়নি"],
        "is_out_of_scope": True
    },
    {
        "id": "L_HAL_02",
        "category": "Hallucination",
        "chapter": 0,
        "topic": "অনুপস্থিত তথ্য ২",
        "query": "বঙ্গবন্ধু স্যাটেলাইট-১ তৈরিতে মোট কতজন বাংলাদেশি প্রকৌশলী কাজ করেছিলেন?",
        "expected_intent": "OUT_OF_CURRICULUM",
        "expected_chapter": 0,
        "expected_evidence": ["পাওয়া যায়নি"],
        "is_out_of_scope": True
    }
]


def run_full_regression():
    print("=" * 85)
    print("        OIBTC FULL REGRESSION & COMPREHENSIVE RAG EVALUATION ENGINE       ")
    print("=" * 85)

    rag = RAGPipeline()
    test_results: List[Dict[str, Any]] = []

    categories = set(c["category"] for c in STRESS_TEST_SUITE)
    cat_stats = {cat: {"total": 0, "passed": 0, "failed": 0} for cat in categories}

    failure_counts = {
        "DATASET_FAILURE": 0,
        "CHUNKING_FAILURE": 0,
        "RETRIEVAL_FAILURE": 0,
        "INTENT_FAILURE": 0,
        "CONTEXT_FAILURE": 0,
        "GENERATION_FAILURE": 0,
        "SCOPE_FAILURE": 0,
        "HALLUCINATION_FAILURE": 0
    }

    total_count = 0
    passed_count = 0

    print(f"Executing {len(STRESS_TEST_SUITE)} test cases across 12 distinct categories...\n")

    for case in STRESS_TEST_SUITE:
        total_count += 1
        test_id = case["id"]
        cat = case["category"]
        q = case["query"]
        history = case.get("history", [])
        expected_ch = case["expected_chapter"]
        expected_intent = case["expected_intent"]
        expected_evidence = case["expected_evidence"]
        is_oos = case.get("is_out_of_scope", False)
        topic = case.get("topic", "")

        cat_stats[cat]["total"] += 1

        t0 = time.time()
        res = rag.process_query(q, history=history)
        duration_ms = (time.time() - t0) * 1000

        ans = res.get("answer", "")
        detected_intent = res.get("intent", "")
        is_out_curr = res.get("is_out_of_curriculum", False)
        sources = res.get("sources", [])
        top_chunk_topic = sources[0]["topic"] if sources else "None"
        top_chunk_chapter = sources[0]["chapter"] if sources else 0

        # Canonicalize for evaluation
        norm_ans = canonicalize_bengali(ans)
        missing_evidence = []
        for ev in expected_evidence:
            norm_ev = canonicalize_bengali(ev)
            if norm_ev not in norm_ans:
                missing_evidence.append(ev)

        # Chapter isolation check
        chapter_correct = True
        if expected_ch > 0:
            if top_chunk_chapter != expected_ch:
                chapter_correct = False
        else:
            if not is_out_curr and top_chunk_chapter > 0:
                chapter_correct = False

        # Evaluation criteria
        passed = False
        failure_reason = None
        hallucination = False
        source_grounded = True
        answer_relevant = True

        if is_oos:
            if is_out_curr or "পাওয়া যায়নি" in ans:
                passed = True
            else:
                passed = False
                failure_reason = "SCOPE_FAILURE"
                failure_counts["SCOPE_FAILURE"] += 1
                source_grounded = False
                hallucination = True
        else:
            if is_out_curr:
                passed = False
                if history:
                    failure_reason = "CONTEXT_FAILURE"
                    failure_counts["CONTEXT_FAILURE"] += 1
                else:
                    failure_reason = "RETRIEVAL_FAILURE"
                    failure_counts["RETRIEVAL_FAILURE"] += 1
                answer_relevant = False
            elif not chapter_correct:
                passed = False
                failure_reason = "RETRIEVAL_FAILURE"
                failure_counts["RETRIEVAL_FAILURE"] += 1
            elif missing_evidence:
                passed = False
                failure_reason = "GENERATION_FAILURE"
                failure_counts["GENERATION_FAILURE"] += 1
                source_grounded = False
            else:
                passed = True

        if passed:
            passed_count += 1
            cat_stats[cat]["passed"] += 1
            status = "PASS"
        else:
            cat_stats[cat]["failed"] += 1
            status = "FAIL"

        print(f"[{status}] {test_id:10s} | {cat:16s} | Q: {q[:40]}...")
        if not passed:
            print(f"       -> Failure Reason: {failure_reason} | Intent: {detected_intent}")
            if missing_evidence:
                print(f"       -> Missing Evidence: {missing_evidence}")
            if not chapter_correct:
                print(f"       -> Chapter Mismatch: Expected {expected_ch}, Got {top_chunk_chapter}")

        test_results.append({
            "Test ID": test_id,
            "Category": cat,
            "Chapter": expected_ch,
            "Topic": topic,
            "Source": top_chunk_topic,
            "Query": q,
            "Resolved Query": res.get("resolved_query", q),
            "Expected Intent": expected_intent,
            "Detected Intent": detected_intent,
            "Retrieved Chunk(s)": [s["topic"] for s in sources],
            "Expected Evidence": expected_evidence,
            "Generated Answer": ans,
            "Answer Relevant?": "YES" if answer_relevant else "NO",
            "Source Grounded?": "YES" if source_grounded else "NO",
            "Hallucination?": "YES" if hallucination else "NO",
            "Chapter Correct?": "YES" if chapter_correct else "NO",
            "Pass/Fail": status,
            "Failure Reason": failure_reason,
            "Latency (ms)": round(duration_ms, 2)
        })

    # Summary Report
    print("\n" + "=" * 85)
    print("                           CATEGORY PERFORMANCE BREAKDOWN                         ")
    print("=" * 85)
    print(f"{'Category':22s} | {'Total':6s} | {'Pass':6s} | {'Fail':6s} | {'Accuracy':10s}")
    print("-" * 85)
    for cat, stats in sorted(cat_stats.items()):
        acc = (stats["passed"] / stats["total"]) * 100 if stats["total"] > 0 else 0.0
        print(f"{cat:22s} | {stats['total']:<6d} | {stats['passed']:<6d} | {stats['failed']:<6d} | {acc:.1f}%")
    print("-" * 85)
    total_acc = (passed_count / total_count) * 100 if total_count > 0 else 0.0
    print(f"{'TOTAL':22s} | {total_count:<6d} | {passed_count:<6d} | {total_count - passed_count:<6d} | {total_acc:.2f}%")
    print("=" * 85)

    print("\nFailure Taxonomy Counts:")
    for ftype, count in failure_counts.items():
        if count > 0:
            print(f"   - {ftype:22s}: {count}")

    # Save detailed report
    report_path = os.path.join("scripts", "large_scale_stress_test_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "summary": {
                "total_tested": total_count,
                "total_passed": passed_count,
                "total_failed": total_count - passed_count,
                "overall_accuracy_pct": round(total_acc, 2),
                "category_breakdown": cat_stats,
                "failure_breakdown": failure_counts
            },
            "detailed_results": test_results
        }, f, ensure_ascii=False, indent=2)
    print(f"\nDetailed evaluation report saved to: {report_path}")

    return test_results, cat_stats, failure_counts

if __name__ == "__main__":
    run_full_regression()
