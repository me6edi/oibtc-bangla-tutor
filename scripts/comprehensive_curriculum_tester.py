"""
Comprehensive NCTB Curriculum Testing Engine for OIBTC (Chapters 1 & 2)
Tests coverage, intent scoping, paraphrase resilience, accuracy, and hallucination resistance.
"""

import os
import sys
import json
import time
from typing import List, Dict, Any

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.rag.pipeline import get_rag_pipeline

# Exhaustive test question dataset covering all 39 curriculum topics + user paraphrasing + traps
TEST_SUITE: List[Dict[str, Any]] = [
    # =========================================================================
    # CHAPTER 1: তথ্য ও যোগাযোগ প্রযুক্তি এবং আমাদের বাংলাদেশ (Pages 1–14)
    # =========================================================================
    # Topic 1: একুশ শতক এবং জ্ঞানভিত্তিক অর্থনীতি
    {
        "id": "C1_01_A",
        "chapter": 1,
        "topic": "জ্ঞানভিত্তিক অর্থনীতি ও দক্ষতা",
        "type": "direct",
        "query": "একুশ শতকের অর্থনীতির মূল ভিত্তি কী?",
        "expected_keywords": ["জ্ঞান", "জ্ঞানভিত্তিক", "অর্থনীতি"],
        "min_score": 0.15
    },
    {
        "id": "C1_01_B",
        "chapter": 1,
        "topic": "জ্ঞানভিত্তিক অর্থনীতি ও দক্ষতা",
        "type": "paraphrased_natural",
        "query": "বর্তমান যুগে টিকে থাকতে হলে একজন মানুষের কোন কোন দক্ষতা থাকা দরকার?",
        "expected_keywords": ["দক্ষতা", "আইসিটি", "তথ্য"],
        "min_score": 0.15
    },

    # Topic 2: একুশ শতকে কৃত্রিম বুদ্ধিমত্তা (AI)
    {
        "id": "C1_02_A",
        "chapter": 1,
        "topic": "কৃত্রিম বুদ্ধিমত্তা (AI)",
        "type": "definition",
        "query": "কৃত্রিম বুদ্ধিমত্তা বা AI বলতে কী বোঝায়?",
        "expected_keywords": ["কৃত্রিম বুদ্ধিমত্তা", "চিন্তাশক্তি", "যন্ত্র"],
        "min_score": 0.15
    },
    {
        "id": "C1_02_B",
        "chapter": 1,
        "topic": "কৃত্রিম বুদ্ধিমত্তা (AI)",
        "type": "natural",
        "query": "কম্পিউটার কি মানুষের মতো ভাবতে পারে? একে কি বলে?",
        "expected_keywords": ["কৃত্রিম বুদ্ধিমত্তা", "AI"],
        "min_score": 0.12
    },

    # Topic 3: চার্লস ব্যাবেজ ও অ্যানালিটিক্যাল ইঞ্জিন
    {
        "id": "C1_03_A",
        "chapter": 1,
        "topic": "চার্লস ব্যাবেজ",
        "type": "direct",
        "query": "আধুনিক কম্পিউটারের জনক কে এবং তিনি কোন কোন যন্ত্র তৈরি করেন?",
        "expected_keywords": ["চার্লস ব্যাবেজ", "ডিফারেন্স ইঞ্জিন", "অ্যানালিটিক্যাল ইঞ্জিন"],
        "min_score": 0.20
    },
    {
        "id": "C1_03_B",
        "chapter": 1,
        "topic": "চার্লস ব্যাবেজ",
        "type": "short",
        "query": "চার্লস ব্যাবেজ কত সালে ডিফারেন্স ইঞ্জিন তৈরি করেন?",
        "expected_keywords": ["১৮২২"],
        "min_score": 0.18
    },

    # Topic 4: অ্যাডা লাভলেস ও তুরিন বিশ্ববিদ্যালয় ১৮৪০
    {
        "id": "C1_04_A",
        "chapter": 1,
        "topic": "অ্যাডা লাভলেস ও তুরিন",
        "type": "multi_clause",
        "query": "চার্লস ব্যাবেজ কত সালে তুরিন বিশ্ববিদ্যালয়ে বক্তৃতা দিয়েছিলেন এবং তাঁর এই কাজের সাথে কোন নারী যুক্ত ছিলেন?",
        "expected_keywords": ["১৮৪০", "তুরিন", "অ্যাডা লাভলেস"],
        "min_score": 0.25
    },
    {
        "id": "C1_04_B",
        "chapter": 1,
        "topic": "অ্যাডা লাভলেস ও তুরিন",
        "type": "natural",
        "query": "ইতিহাসের প্রথম প্রোগ্রামার কে এবং তিনি কার কাজের ওপর নোট লিখেছিলেন?",
        "expected_keywords": ["অ্যাডা লাভলেস", "চার্লস ব্যাবেজ"],
        "min_score": 0.20
    },

    # Topic 5: ম্যাক্সওয়েল, জগদীশচন্দ্র ও মার্কনি
    {
        "id": "C1_05_A",
        "chapter": 1,
        "topic": "বেতার তরঙ্গ ও যোগাযোগ",
        "type": "direct",
        "query": "স্যার জগদীশ চন্দ্র বসু অতিক্ষুদ্র তরঙ্গ ব্যবহার করে কত সালে সংকেত পাঠান?",
        "expected_keywords": ["জগদীশ চন্দ্র বসু", "১৮৯৫"],
        "min_score": 0.20
    },
    {
        "id": "C1_05_B",
        "chapter": 1,
        "topic": "বেতার তরঙ্গ ও যোগাযোগ",
        "type": "why_who",
        "query": "গুলিয়েলমো মার্কনি কেন বিখ্যাত?",
        "expected_keywords": ["মার্কনি", "বেতার", "রেডিও"],
        "min_score": 0.20
    },

    # Topic 6: আইবিএম মেইনফ্রেম ও রেমন্ড টমলিনসন
    {
        "id": "C1_06_A",
        "chapter": 1,
        "topic": "ই-মেইল আবিষ্কার",
        "type": "direct",
        "query": "ই-মেইল পদ্ধতির জনক কে এবং তিনি কবে প্রথম ইমেইল পাঠান?",
        "expected_keywords": ["টমলিনসন", "১৯৭১"],
        "min_score": 0.20
    },
    {
        "id": "C1_06_B",
        "chapter": 1,
        "topic": "ই-মেইল আবিষ্কার",
        "type": "short",
        "query": "ইমেইলে '@' চিহ্ন প্রথম কে ব্যবহার করেন?",
        "expected_keywords": ["টমলিনসন"],
        "min_score": 0.20
    },

    # Topic 7: স্টিভ জবস ও কোয়ান্টাম কম্পিউটার
    {
        "id": "C1_07_A",
        "chapter": 1,
        "topic": "স্টিভ জবস ও অ্যাপল",
        "type": "direct",
        "query": "স্টিভ জবস ও তাঁর বন্ধুরা কত সালে অ্যাপল কম্পিউটার প্রতিষ্ঠা করেন?",
        "expected_keywords": ["স্টিভ জবস", "১৯৭৬", "অ্যাপল"],
        "min_score": 0.20
    },
    {
        "id": "C1_07_B",
        "chapter": 1,
        "topic": "কোয়ান্টাম কম্পিউটার",
        "type": "definition",
        "query": "কোয়ান্টাম কম্পিউটার কী এবং এর সুবিধা কী?",
        "expected_keywords": ["কোয়ান্টাম", "সুপারপজিশন", "দ্রুত"],
        "min_score": 0.20
    },

    # Topic 8: বিল গেটস ও টিম বার্নার্স-লি
    {
        "id": "C1_08_A",
        "chapter": 1,
        "topic": "বিল গেটস ও মাইক্রোসফট",
        "type": "direct",
        "query": "বিল গেটস কোন প্রতিষ্ঠান গড়ে তোলেন এবং এর তৈরি অপারেটিং সিস্টেমের নাম কী?",
        "expected_keywords": ["মাইক্রোসফট", "উইন্ডোজ"],
        "min_score": 0.20
    },
    {
        "id": "C1_08_B",
        "chapter": 1,
        "topic": "টিম বার্নার্স-লি ও WWW",
        "type": "direct",
        "query": "ওয়ার্ল্ড ওয়াইড ওয়েব (WWW) কে কত সালে আবিষ্কার করেন?",
        "expected_keywords": ["টিম বার্নার্স-লি", "১৯৮৯", "WWW"],
        "min_score": 0.20
    },

    # Topic 9: মার্ক জাকারবার্গ ও ফেসবুক
    {
        "id": "C1_09_A",
        "chapter": 1,
        "topic": "মার্ক জাকারবার্গ",
        "type": "direct",
        "query": "ফেসবুকের প্রতিষ্ঠাতা কে এবং এটি কত সালে প্রতিষ্ঠিত হয়?",
        "expected_keywords": ["মার্ক জাকারবার্গ", "২০০৪", "ফেসবুক"],
        "min_score": 0.20
    },

    # Topic 10: ই-লার্নিং ও বাংলাদেশ
    {
        "id": "C1_10_A",
        "chapter": 1,
        "topic": "ই-লার্নিং",
        "type": "definition",
        "query": "ই-লার্নিং বলতে কী বোঝায়?",
        "expected_keywords": ["ই-লার্নিং", "দূরদূরান্ত", "শিক্ষা"],
        "min_score": 0.20
    },
    {
        "id": "C1_10_B",
        "chapter": 1,
        "topic": "ই-লার্নিং",
        "type": "relation",
        "query": "ই-লার্নিং কি সনাতন ক্লাসরুম শিক্ষার বিকল্প?",
        "expected_keywords": ["বিকল্প নয়", "পরিপূরক"],
        "min_score": 0.15
    },

    # Topic 11: ই-গভর্ন্যান্স ও বাংলাদেশ
    {
        "id": "C1_11_A",
        "chapter": 1,
        "topic": "ই-গভর্ন্যান্স",
        "type": "definition",
        "query": "ই-গভর্ন্যান্স কী এবং এর মূল উদ্দেশ্য কী?",
        "expected_keywords": ["ই-গভর্ন্যান্স", "স্বচ্ছ", "জবাবদিহিতা"],
        "min_score": 0.20
    },

    # Topic 12: ই-সার্ভিস ও নাগরিক সেবা
    {
        "id": "C1_12_A",
        "chapter": 1,
        "topic": "ই-সার্ভিস",
        "type": "definition",
        "query": "ই-সার্ভিস বলতে কী বোঝায়?",
        "expected_keywords": ["ই-সার্ভিস", "সেবা", "নাগরিক"],
        "min_score": 0.20
    },
    {
        "id": "C1_12_B",
        "chapter": 1,
        "topic": "ই-পুর্জি ও ই-পর্চা",
        "type": "examples",
        "query": "ই-পুর্জি ও ই-পর্চা সেবা কী কাজে লাগে?",
        "expected_keywords": ["আখ", "জমি", "অনুলিপি"],
        "min_score": 0.20
    },

    # Topic 13: ই-কমার্স ও বাংলাদেশ
    {
        "id": "C1_13_A",
        "chapter": 1,
        "topic": "ই-কমার্স",
        "type": "definition",
        "query": "ই-কমার্স বলতে কী বোঝায়?",
        "expected_keywords": ["ই-কমার্স", "পণ্য", "কেনাবেচা"],
        "min_score": 0.20
    },

    # Topic 14: কর্মক্ষেত্রে আইসিটি ও ফ্রিল্যান্সিং
    {
        "id": "C1_14_A",
        "chapter": 1,
        "topic": "ফ্রিল্যান্সিং",
        "type": "direct",
        "query": "ঘরে বসে ইন্টারনেটে মুক্ত পেশাজীবী হিসেবে কাজ করাকে কী বলে?",
        "expected_keywords": ["ফ্রিল্যান্সিং", "মুক্তপেশা"],
        "min_score": 0.15
    },

    # Topic 15: সামাজিক যোগাযোগ মাধ্যম
    {
        "id": "C1_15_A",
        "chapter": 1,
        "topic": "সামাজিক যোগাযোগ",
        "type": "examples",
        "query": "পাঠ্যবইয়ে উল্লেখিত কয়েকটি সামাজিক যোগাযোগ মাধ্যমের নাম বলো।",
        "expected_keywords": ["ফেসবুক", "টুইটার", "ইনস্টাগ্রাম"],
        "min_score": 0.18
    },

    # Topic 16: বিনোদন ও লিপফ্রগ প্রযুক্তি
    {
        "id": "C1_16_A",
        "chapter": 1,
        "topic": "লিপফ্রগ প্রযুক্তি",
        "type": "concept",
        "query": "লিপফ্রগ প্রযুক্তি বলতে কী বোঝানো হয়েছে?",
        "expected_keywords": ["লিপফ্রগ", "ধাপ", "প্রযুক্তি"],
        "min_score": 0.15
    },

    # Topic 17: ডিজিটাল বাংলাদেশ ও বঙ্গবন্ধু স্যাটেলাইট-১
    {
        "id": "C1_17_A",
        "chapter": 1,
        "topic": "ডিজিটাল বাংলাদেশ স্তম্ভ",
        "type": "rules",
        "query": "ডিজিটাল বাংলাদেশ রূপকল্পের ৪টি প্রধান স্তম্ভ কী কী?",
        "expected_keywords": ["মানবসম্পদ", "সংযোগ", "ই-গভর্ন্যান্স", "আইসিটি শিল্প"],
        "min_score": 0.20
    },
    {
        "id": "C1_17_B",
        "chapter": 1,
        "topic": "বঙ্গবন্ধু স্যাটেলাইট-১",
        "type": "direct",
        "query": "বঙ্গবন্ধু স্যাটেলাইট-১ কত তারিখে মহাকাশে উৎক্ষেপণ করা হয় এবং বাংলাদেশ কততম দেশ?",
        "expected_keywords": ["২০১৮", "১২ মে", "৫৭তম"],
        "min_score": 0.20
    },

    # =========================================================================
    # CHAPTER 2: কম্পিউটার ও ব্যবহারকারীর নিরাপত্তা (Pages 15–41)
    # =========================================================================
    # Topic 18: সফটওয়্যার রক্ষণাবেক্ষণ
    {
        "id": "C2_18_A",
        "chapter": 2,
        "topic": "কম্পিউটার রক্ষণাবেক্ষণ",
        "type": "why",
        "query": "কম্পিউটার সচল রাখতে সফটওয়্যার রক্ষণাবেক্ষণ কেন জরুরি?",
        "expected_keywords": ["রক্ষণাবেক্ষণ", "সফটওয়্যার", "ধীরগতি"],
        "min_score": 0.18
    },

    # Topic 19: রেজিস্ট্রি ক্লিনিং ও Run Commands
    {
        "id": "C2_19_A",
        "chapter": 2,
        "topic": "টেম্পোরারি ফাইল অপসারণ",
        "type": "direct",
        "query": "কম্পিউটার থেকে সাময়িক ফাইল মুছতে রান কমান্ডে কী লিখতে হয়?",
        "expected_keywords": ["temp", "prefetch"],
        "min_score": 0.20
    },

    # Topic 20: ডিস্ক ক্লিনআপ ও ডিস্ক ডিফ্র্যাগমেন্টার
    {
        "id": "C2_20_A",
        "chapter": 2,
        "topic": "ডিস্ক ক্লিনআপ",
        "type": "difference",
        "query": "ডিস্ক ক্লিনআপ এবং ডিস্ক ডিফ্র্যাগমেন্টার ব্যবহারের উদ্দেশ্য কী?",
        "expected_keywords": ["ডিস্ক ক্লিনআপ", "ডিফ্র্যাগমেন্টার", "জায়গা"],
        "min_score": 0.20
    },

    # Topic 21: সফটওয়্যার ইনস্টলেশন
    {
        "id": "C2_21_A",
        "chapter": 2,
        "topic": "সফটওয়্যার ইনস্টলেশন",
        "type": "definition_process",
        "query": "সফটওয়্যার ইনস্টলেশন কী এবং সেটআপ ফাইল সাধারণত কী নামে থাকে?",
        "expected_keywords": ["ইনস্টলেশন", "setup", "প্রোগ্রাম"],
        "min_score": 0.20
    },

    # Topic 22: সফটওয়্যার আনইনস্টল বনাম ডিলিট
    {
        "id": "C2_22_A",
        "chapter": 2,
        "topic": "সফটওয়্যার আনইনস্টলেশন",
        "type": "difference",
        "query": "সফটওয়্যার ডিলিট এবং আনইনস্টল করার মধ্যে পার্থক্য কী?",
        "expected_keywords": ["কন্ট্রোল প্যানেল", "মুছে", "আনইনস্টল"],
        "min_score": 0.20
    },

    # Topic 23: শক্তিশালী পাসওয়ার্ড তৈরির ৫টি নিয়ম
    {
        "id": "C2_23_A",
        "chapter": 2,
        "topic": "পাসওয়ার্ড তৈরির নিয়ম",
        "type": "rules",
        "query": "একটি শক্তিশালী পাসওয়ার্ড তৈরি করার ৫টি নিয়ম কী কী?",
        "expected_keywords": ["বড় হাতের", "ছোট হাতের", "সংখ্যা", "চিহ্ন", "৮ থেকে ১৬"],
        "min_score": 0.25
    },
    {
        "id": "C2_23_B",
        "chapter": 2,
        "topic": "পাসওয়ার্ড তৈরির নিয়ম",
        "type": "natural",
        "query": "পাসওয়ার্ডে নিজের নাম বা মোবাইল নাম্বার দিলে কি নিরাপদ থাকে?",
        "expected_keywords": ["ব্যক্তিগত তথ্য", "নিরাপদ নয়", "সহজে"],
        "min_score": 0.15
    },

    # Topic 24: টু-ফ্যাক্টর অথেনটিকেশন (2FA)
    {
        "id": "C2_24_A",
        "chapter": 2,
        "topic": "2FA ও বায়োমেট্রিক",
        "type": "definition",
        "query": "টু-ফ্যাক্টর অথেনটিকেশন বা 2FA বলতে কী বোঝায়?",
        "expected_keywords": ["টু-ফ্যাক্টর", "পাসওয়ার্ড", "যাচাইকরণ"],
        "min_score": 0.20
    },

    # Topic 25: কম্পিউটার ভাইরাসের সংজ্ঞা ও ইতিহাস
    {
        "id": "C2_25_A",
        "chapter": 2,
        "topic": "ভাইরাস সংজ্ঞা ও নামকরণ",
        "type": "definition",
        "query": "কম্পিউটার ভাইরাস কী এবং VIRUS এর পূর্ণরূপ কী?",
        "expected_keywords": ["Vital Information Resources Under Siege", "ক্ষতিকর প্রোগ্রাম"],
        "min_score": 0.25
    },
    {
        "id": "C2_25_B",
        "chapter": 2,
        "topic": "ভাইরাস সংজ্ঞা ও নামকরণ",
        "type": "history",
        "query": "কম্পিউটার ভাইরাসের নামকরণ কে এবং কত সালে করেন?",
        "expected_keywords": ["ফ্রেড কোহেন", "১৯৮৩"],
        "min_score": 0.20
    },

    # Topic 26: উল্লেখযোগ্য ভাইরাসের তালিকা
    {
        "id": "C2_26_A",
        "chapter": 2,
        "topic": "ভাইরাস তালিকা",
        "type": "examples",
        "query": "বইয়ে উল্লেখিত কয়েকটি বিপজ্জনক ভাইরাসের নাম বলো।",
        "expected_keywords": ["সিআইএইচ", "ব্রেন", "জেরুজালেম"],
        "min_score": 0.20
    },

    # Topic 27: ভাইরাস সংক্রমণের লক্ষণ
    {
        "id": "C2_27_A",
        "chapter": 2,
        "topic": "ভাইরাস লক্ষণ",
        "type": "symptoms",
        "query": "কম্পিউটার ভাইরাসে আক্রান্ত হলে কী কী লক্ষণ প্রকাশ পায়?",
        "expected_keywords": ["ধীরগতি", "ফাইল", "মেমোরি", "রিস্টার্ট"],
        "min_score": 0.20
    },

    # Topic 28: ভাইরাস প্রতিরোধ ও অ্যান্টিভাইরাস
    {
        "id": "C2_28_A",
        "chapter": 2,
        "topic": "অ্যান্টিভাইরাস ও প্রতিরোধ",
        "type": "prevention",
        "query": "কম্পিউটারকে ভাইরাস মুক্ত রাখতে কী কী সতর্কতা অবলম্বন করতে হবে?",
        "expected_keywords": ["অ্যান্টিভাইরাস", "আপডেট", "পেনড্রাইভ", "স্ক্যান"],
        "min_score": 0.20
    },
    {
        "id": "C2_28_B",
        "chapter": 2,
        "topic": "অ্যান্টিভাইরাস তালিকা",
        "type": "examples",
        "query": "কয়েকটি অ্যান্টিভাইরাস সফটওয়্যারের নাম লেখো।",
        "expected_keywords": ["Avast", "Avira", "Kaspersky", "Norton"],
        "min_score": 0.20
    },

    # Topic 29: সাইবার অপরাধ ও অনলাইন নিরাপত্তা
    {
        "id": "C2_29_A",
        "chapter": 2,
        "topic": "সাইবার অপরাধ",
        "type": "direct",
        "query": "সাইবার ক্রাইম বা সাইবার অপরাধ বলতে কী বোঝায়?",
        "expected_keywords": ["ইন্টারনেট", "অপরাধ", "নিরাপত্তা"],
        "min_score": 0.18
    },

    # Topic 30: ফেইক নিউজ ও গুজব প্রতিরোধ
    {
        "id": "C2_30_A",
        "chapter": 2,
        "topic": "ফেইক নিউজ",
        "type": "definition",
        "query": "ফেইক নিউজ কাকে বলে এবং এটি কীভাবে ছড়ায়?",
        "expected_keywords": ["ফেইক নিউজ", "অসত্য", "অপতথ্য"],
        "min_score": 0.20
    },

    # Topic 31: ডিজিটাল আসক্তি ও নার্সিসিজম
    {
        "id": "C2_31_A",
        "chapter": 2,
        "topic": "ডিজিটাল আসক্তি ও নার্সিসিজম",
        "type": "definition",
        "query": "সামাজিক যোগাযোগ মাধ্যমে নার্সিসিজম বলতে কী বোঝায়?",
        "expected_keywords": ["নার্সিসিজম", "নিজেকে", "উপস্থাপন"],
        "min_score": 0.20
    },

    # Topic 32: ডিজিটাল আসক্তি থেকে মুক্তির উপায়
    {
        "id": "C2_32_A",
        "chapter": 2,
        "topic": "আসক্তি মুক্তি",
        "type": "prevention",
        "query": "ডিজিটাল ডিভাইসের অতিরিক্ত আসক্তি থেকে বাঁচার উপায় কী?",
        "expected_keywords": ["আসক্তি", "সময়", "মাঠের খেলা"],
        "min_score": 0.18
    },

    # Topic 33: কপিরাইট আইন ও সফটওয়্যার পাইরেসি
    {
        "id": "C2_33_A",
        "chapter": 2,
        "topic": "কপিরাইট ও পাইরেসি",
        "type": "definition",
        "query": "সফটওয়্যার পাইরেসি কী এবং বাংলাদেশে কপিরাইট আইন কত সালের?",
        "expected_keywords": ["অনুমতি ব্যতীত", "পাইরেসি", "২০০০"],
        "min_score": 0.20
    },

    # Topic 34: তথ্য অধিকার আইন ২০০৯
    {
        "id": "C2_34_A",
        "chapter": 2,
        "topic": "তথ্য অধিকার আইন",
        "type": "direct",
        "query": "বাংলাদেশে তথ্য অধিকার আইন কত সালে প্রণীত হয় এবং এর লক্ষ্য কী?",
        "expected_keywords": ["তথ্য অধিকার", "২০০৯", "নাগরিক"],
        "min_score": 0.20
    },

    # Topic 35: ট্রাবলশুটিং সাধারণ ধারণা
    {
        "id": "C2_35_A",
        "chapter": 2,
        "topic": "ট্রাবলশুটিং ধারণা",
        "type": "definition",
        "query": "কম্পিউটারে ট্রাবলশুটিং বলতে কী বোঝায়?",
        "expected_keywords": ["ট্রাবলশুটিং", "ত্রুটি", "সমাধান"],
        "min_score": 0.20
    },

    # Topic 36: ট্রাবলশুটিং ১-৪ (পাওয়ার, ডিসপ্লে, অতিরিক্ত তাপ, সিএমওএস)
    {
        "id": "C2_36_A",
        "chapter": 2,
        "topic": "ট্রাবলশুটিং - ডিসপ্লে না আসলে",
        "type": "troubleshooting",
        "query": "কম্পিউটার চালু হওয়ার পর যদি মনিটরে কোনো ডিসপ্লে না আসে তবে কী করতে হবে?",
        "expected_keywords": ["র‍্যাম", "RAM", "ইরেজার", "স্লট"],
        "min_score": 0.20
    },
    {
        "id": "C2_36_B",
        "chapter": 2,
        "topic": "ট্রাবলশুটিং - সিএমওএস ব্যাটারি",
        "type": "troubleshooting",
        "query": "কম্পিউটারের ঘড়ির তারিখ ও সময় প্রতিবার বন্ধ করলে উল্টাপাল্টা হয়ে যায় কেন?",
        "expected_keywords": ["সিএমওএস", "CMOS", "ব্যাটারি"],
        "min_score": 0.20
    },

    # Topic 37: ট্রাবলশুটিং ৫-৮ (ধীরগতি, শক, রিস্টার্ট, বুট সমস্যা)
    {
        "id": "C2_37_A",
        "chapter": 2,
        "topic": "ট্রাবলশুটিং - মেটালিক বডি শক",
        "type": "troubleshooting",
        "query": "সিপিইউ এর মেটালিক বডিতে হাত দিলে হালকা কারেন্ট শক করে কেন?",
        "expected_keywords": ["আর্থিং", "গ্রাউন্ডিং", "শক"],
        "min_score": 0.20
    },
    {
        "id": "C2_37_B",
        "chapter": 2,
        "topic": "ট্রাবলশুটিং - ঘন ঘন রিস্টার্ট",
        "type": "troubleshooting",
        "query": "কম্পিউটার নিজে নিজেই বারবার রিস্টার্ট নিচ্ছে, কী সমাধান?",
        "expected_keywords": ["কুলিং ফ্যান", "থার্মাল পেস্ট", "রিস্টার্ট"],
        "min_score": 0.20
    },

    # Topic 38: ট্রাবলশুটিং ৯-১২ (বুট এরর, স্ক্রিন কাঁপুনী, কিবোর্ড, মাউস)
    {
        "id": "C2_38_A",
        "chapter": 2,
        "topic": "ট্রাবলশুটিং - কিবোর্ড কাজ না করা",
        "type": "troubleshooting",
        "query": "কম্পিউটারে কিবোর্ড কাজ করছে না, কী করতে হবে?",
        "expected_keywords": ["কিবোর্ড", "ইউএসবি", "পোর্ট"],
        "min_score": 0.20
    },
    {
        "id": "C2_38_B",
        "chapter": 2,
        "topic": "ট্রাবলশুটিং - মাউস পয়েন্টার",
        "type": "troubleshooting",
        "query": "মাউস পয়েন্টার নড়াচড়া করছে না, সমাধান কী?",
        "expected_keywords": ["মাউস", "ইউএসবি", "সেন্সর"],
        "min_score": 0.20
    },

    # Topic 39: ট্রাবলশুটিং ১৩-১৬ (ইন্টারনেট, অডিও, ইউএসবি, প্রিন্টার)
    {
        "id": "C2_39_A",
        "chapter": 2,
        "topic": "ট্রাবলশুটিং - সাউন্ড না আসা",
        "type": "troubleshooting",
        "query": "কম্পিউটারে গান বাজালে কোনো শব্দ বা অডিও শোনা যায় না কেন?",
        "expected_keywords": ["সাউন্ড", "অডিও", "স্পিকার", "ড্রাইভার"],
        "min_score": 0.20
    },
    {
        "id": "C2_39_B",
        "chapter": 2,
        "topic": "ট্রাবলশুটিং - প্রিন্টার সমস্যা",
        "type": "troubleshooting",
        "query": "প্রিন্টার দিয়ে প্রিন্ট বের হচ্ছে না, কী পরীক্ষা করতে হবে?",
        "expected_keywords": ["প্রিন্টার", "কেবল", "কার্টিজ", "কাগজ"],
        "min_score": 0.20
    },

    # =========================================================================
    # TRAP & OUT-OF-CURRICULUM QUESTIONS (Negative Verification)
    # =========================================================================
    {
        "id": "TRAP_01",
        "chapter": 0,
        "topic": "আউট অব সিলেবাস - ভূগোল",
        "type": "out_of_curriculum",
        "query": "বাংলাদেশের প্রধান প্রধান নদী কোনগুলো?",
        "expected_keywords": ["আওতাভুক্ত নয়"],
        "min_score": 0.0
    },
    {
        "id": "TRAP_02",
        "chapter": 0,
        "topic": "আউট অব সিলেবাস - ইতিহাস",
        "type": "out_of_curriculum",
        "query": "১৯৭১ সালের মুক্তিযুদ্ধের প্রধান সেনাপতি কে ছিলেন?",
        "expected_keywords": ["আওতাভুক্ত নয়"],
        "min_score": 0.0
    },
    {
        "id": "TRAP_03",
        "chapter": 0,
        "topic": "আউট অব সিলেবাস - খেলাধুলা",
        "type": "out_of_curriculum",
        "query": "ফিফা বিশ্বকাপ ফুটবল ২০২৬ কোথায় অনুষ্ঠিত হবে?",
        "expected_keywords": ["আওতাভুক্ত নয়"],
        "min_score": 0.0
    }
]


def run_comprehensive_test():
    print("=" * 80)
    print("      OIBTC FULL CURRICULUM TESTING HARNESS (CHAPTER 1 & CHAPTER 2)      ")
    print("=" * 80)
    print(f"Total Test Cases: {len(TEST_SUITE)}")
    ch1_cases = [c for c in TEST_SUITE if c["chapter"] == 1]
    ch2_cases = [c for c in TEST_SUITE if c["chapter"] == 2]
    trap_cases = [c for c in TEST_SUITE if c["chapter"] == 0]
    print(f"Chapter 1 Cases: {len(ch1_cases)} | Chapter 2 Cases: {len(ch2_cases)} | Trap Cases: {len(trap_cases)}\n")

    pipeline = get_rag_pipeline()

    results_log = []
    ch1_pass = 0
    ch2_pass = 0
    trap_pass = 0
    issues = []

    for idx, tc in enumerate(TEST_SUITE, 1):
        qid = tc["id"]
        q = tc["query"]
        expected_chapter = tc["chapter"]
        expected_keywords = tc["expected_keywords"]

        t0 = time.time()
        res = pipeline.process_query(q)
        duration = time.time() - t0

        ans = res.get("answer", "")
        intent = res.get("intent", "")
        sources = res.get("sources", [])
        top_chapter = sources[0].get("chapter") if sources else None
        top_topic = sources[0].get("topic") if sources else "None"

        # Check Chapter Isolation: If it's a curriculum question, did it match the expected chapter?
        chapter_match = True
        if expected_chapter in [1, 2]:
            chapter_match = (top_chapter == expected_chapter)

        # Check Keyword & Factual Alignment with Unicode Normalization
        import unicodedata

        def normalize_bengali(text: str) -> str:
            if not text:
                return ""
            text = unicodedata.normalize('NFKC', text)
            text = text.replace('\u09af\u09bc', '\u09df')
            text = text.replace('\u09a1\u09bc', '\u09dc')
            text = text.replace('\u09a2\u09bc', '\u09dd')
            return text.lower()

        def check_keyword_present(kw: str, ans_text: str) -> bool:
            norm_kw = normalize_bengali(kw)
            norm_ans = normalize_bengali(ans_text)
            if norm_kw in norm_ans:
                return True
            synonyms = {
                "১২ মে": ["১২ই মে", "12 may", "১২ মে"],
                "কেবল": ["ক্যাবল", "cable"],
                "ক্যাবল": ["কেবল", "cable"],
                "কন্ট্রোল প্যানেল": ["control panel", "কন্ট্রোল প্যানেল"],
                "আইসিটি": ["তথ্য ও যোগাযোগ প্রযুক্তি", "আইসিটি", "ict"],
                "setup": ["সেটআপ", "setup.exe", "setup"],
                "নিরাপদ নয়": ["নিরাপদ নয়", "ঝুঁকিপূর্ণ", "পরিহার", "নিরাপদ নয়", "এড়িয়ে"],
                "ব্যক্তিগত তথ্য": ["নিজের নাম", "মোবাইল নম্বর", "ব্যক্তিগত তথ্য"],
                "জায়গা": ["জায়গা", "জায়গা", "space", "স্পেস"]
            }
            for k, syn_list in synonyms.items():
                if normalize_bengali(k) == norm_kw:
                    if any(normalize_bengali(s) in norm_ans for s in syn_list):
                        return True
            return False

        missing_kw = [kw for kw in expected_keywords if not check_keyword_present(kw, ans)]
        passed = (len(missing_kw) == 0) and (chapter_match or expected_chapter == 0)

        status_str = "PASS" if passed else "FAIL"

        if expected_chapter == 1:
            if passed: ch1_pass += 1
        elif expected_chapter == 2:
            if passed: ch2_pass += 1
        else:
            if passed: trap_pass += 1

        if not passed:
            issue_detail = {
                "id": qid,
                "query": q,
                "expected_chapter": expected_chapter,
                "retrieved_chapter": top_chapter,
                "retrieved_topic": top_topic,
                "missing_keywords": missing_kw,
                "intent": intent,
                "answer": ans
            }
            issues.append(issue_detail)

        print(f"[{status_str}] #{idx:02d} ({qid}) Q: {q}")
        print(f"       Intent: {res.get('intent_label')} | Top Source: {top_topic} (Ch {top_chapter})")
        if not passed:
            if not chapter_match:
                print(f"       [!] CHAPTER MISMATCH: Expected Ch {expected_chapter}, got Ch {top_chapter}")
            if missing_kw:
                print(f"       [!] MISSING KEYWORDS: {missing_kw}")
            print(f"       Answer: {ans[:150]}...")
        print("-" * 80)

        results_log.append({
            "id": qid,
            "query": q,
            "passed": passed,
            "chapter": expected_chapter,
            "top_topic": top_topic,
            "duration": duration
        })

    # Summary Report
    total_curriculum = len(ch1_cases) + len(ch2_cases)
    total_passed = ch1_pass + ch2_pass + trap_pass
    total_cases = len(TEST_SUITE)

    print("\n" + "=" * 80)
    print("                           FINAL TEST REPORT                            ")
    print("=" * 80)
    print(f"Chapter 1 Coverage & Accuracy: {ch1_pass}/{len(ch1_cases)} ({ch1_pass/len(ch1_cases)*100:.1f}%)")
    print(f"Chapter 2 Coverage & Accuracy: {ch2_pass}/{len(ch2_cases)} ({ch2_pass/len(ch2_cases)*100:.1f}%)")
    print(f"Trap & Out-of-Curriculum Resistance: {trap_pass}/{len(trap_cases)} ({trap_pass/len(trap_cases)*100:.1f}%)")
    print(f"Overall Test Score: {total_passed}/{total_cases} ({total_passed/total_cases*100:.1f}%)")
    print(f"Total Issues Detected: {len(issues)}")
    print("=" * 80)

    # Save detailed JSON report
    report_path = os.path.join("scripts", "comprehensive_test_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": time.time(),
            "total_tested": total_cases,
            "total_passed": total_passed,
            "chapter_1": {"tested": len(ch1_cases), "passed": ch1_pass},
            "chapter_2": {"tested": len(ch2_cases), "passed": ch2_pass},
            "traps": {"tested": len(trap_cases), "passed": trap_pass},
            "issues": issues
        }, f, ensure_ascii=False, indent=2)
    print(f"Full diagnostic report saved to: {report_path}")

    return issues


if __name__ == "__main__":
    issues = run_comprehensive_test()
    if issues:
        sys.exit(1)
    else:
        sys.exit(0)
