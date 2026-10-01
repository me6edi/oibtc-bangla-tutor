"""
Intent and Scope Detection Module for OIBTC
Analyzes student queries in Bengali to determine pedagogical intent and scope.
Runs 100% offline with zero token latency.
"""

import re
from enum import Enum
from typing import List, Dict, Any, Optional


class IntentType(str, Enum):
    DEFINITION = "DEFINITION"                  # সংজ্ঞা / মূলভাব
    MECHANISM = "MECHANISM"                    # ছড়ানোর পদ্ধতি / কীভাবে কাজ করে
    MULTI_INTENT = "MULTI_INTENT"              # যৌথ বিষয় (যেমন: সংজ্ঞা + কীভাবে ছড়ায়)
    PREVENTION = "PREVENTION"                  # নিরাপত্তা / প্রতিরোধের উপায়
    EXAMPLES = "EXAMPLES"                      # উদাহরণ / নামসমূহ
    SYMPTOMS = "SYMPTOMS"                      # আক্রান্ত হওয়ার লক্ষণ
    RULES = "RULES"                            # নিয়মাবলি / স্তম্ভসমূহ
    TROUBLESHOOTING = "TROUBLESHOOTING"        # ট্রাবলশুটিং / সমস্যা ও সমাধান
    HISTORY_PERSON = "HISTORY_PERSON"          # ব্যক্তিত্ব ও ইতিহাস
    GENERAL = "GENERAL"                        # সাধারণ পাঠ্যবই সংক্রান্ত প্রশ্ন
    OUT_OF_CURRICULUM = "OUT_OF_CURRICULUM"    # সিলেবাসের বাইরের প্রশ্ন


class GranularityType(str, Enum):
    YEAR = "YEAR"                  # কত সালে / কবে / কোন সালে
    PERSON = "PERSON"              # কে / কার / কাদের / আবিষ্কারক কে
    COUNT = "COUNT"                # কয়টি / কতটি / কতগুলো
    ONE_LINE = "ONE_LINE"          # এক লাইনে / এক বাক্যে
    SHORT = "SHORT"                # সংক্ষেপে / ছোট করে
    DETAILED = "DETAILED"          # বিস্তারিত / বিশদভাবে
    WHY = "WHY"                    # কেন / কী কারণে
    HOW = "HOW"                    # কীভাবে / কিভাবে / পদ্ধতি
    WHAT = "WHAT"                  # কী / কি / কাকে বলে
    LIST = "LIST"                  # কী কী / প্রকারভেদ / নামসমূহ
    EXAMPLES = "EXAMPLES"          # উদাহরণ
    OVERVIEW = "OVERVIEW"          # সম্পর্কে বলো
    GENERAL = "GENERAL"            # সাধারণ


class IntentResult:
    def __init__(
        self,
        primary_intent: IntentType,
        intent_label_bn: str,
        sub_intents: Optional[List[IntentType]] = None,
        scope_description: str = "",
        target_topic: Optional[str] = None,
        granularity: GranularityType = GranularityType.GENERAL
    ):
        self.primary_intent = primary_intent
        self.intent_label_bn = intent_label_bn
        self.sub_intents = sub_intents or [primary_intent]
        self.scope_description = scope_description
        self.target_topic = target_topic
        self.granularity = granularity

    def to_dict(self) -> Dict[str, Any]:
        return {
            "primary_intent": self.primary_intent.value,
            "intent_label_bn": self.intent_label_bn,
            "sub_intents": [i.value for i in self.sub_intents],
            "scope_description": self.scope_description,
            "target_topic": self.target_topic,
            "granularity": self.granularity.value
        }


# Known curriculum entities for topic resolution
KNOWN_TOPICS = {
    "ভাইরাস": "কম্পিউটার ভাইরাস ও ম্যালওয়্যার - নামকরণ ও ভাইরাসের ইতিহাস",
    "ম্যালওয়্যার": "কম্পিউটার ভাইরাস ও ম্যালওয়্যার - নামকরণ ও ভাইরাসের ইতিহাস",
    "পাসওয়ার্ড": "কম্পিউটার নিরাপত্তা ও শক্তিশালী পাসওয়ার্ড তৈরির ৫টি নিয়ম",
    "পাসওয়ার্ড": "কম্পিউটার নিরাপত্তা ও শক্তিশালী পাসওয়ার্ড তৈরির ৫টি নিয়ম",
    "অ্যান্টিভাইরাস": "কম্পিউটার ভাইরাস প্রতিরোধ ও অ্যান্টিভাইরাস সফটওয়্যার",
    "ই-লার্নিং": "ই-লার্নিং ও বাংলাদেশ",
    "ই-গভর্ন্যান্স": "ই-গভর্ন্যান্স ও বাংলাদেশ",
    "ই-সার্ভিস": "ই-সার্ভিস ও নাগরিক সেবা - ই-পুর্জি, ইএমটিএস ও ই-পর্চা",
    "ই-পুর্জি": "ই-সার্ভিস ও নাগরিক সেবা - ই-পুর্জি, ইএমটিএস ও ই-পর্চা",
    "ই-পর্চা": "ই-সার্ভিস ও নাগরিক সেবা - ই-পুর্জি, ইএমটিএস ও ই-পর্চা",
    "ইএমটিএস": "ই-সার্ভিস ও নাগরিক সেবা - ই-পুর্জি, ইএমটিএস ও ই-পর্চা",
    "ই-কমার্স": "ই-কমার্স ও বাংলাদেশ",
    "ডিজিটাল বাংলাদেশ": "আইসিটি সূচক, ডিজিটাল বাংলাদেশ ও বঙ্গবন্ধু স্যাটেলাইট-১",
    "স্তম্ভ": "আইসিটি সূচক, ডিজিটাল বাংলাদেশ ও বঙ্গবন্ধু স্যাটেলাইট-১",
    "স্যাটেলাইট": "আইসিটি সূচক, ডিজিটাল বাংলাদেশ ও বঙ্গবন্ধু স্যাটেলাইট-১",
    "বঙ্গবন্ধু স্যাটেলাইট": "আইসিটি সূচক, ডিজিটাল বাংলাদেশ ও বঙ্গবন্ধু স্যাটেলাইট-১",
    "সামাজিক যোগাযোগ": "সামাজিক যোগাযোগ মাধ্যম - ফেসবুক, টুইটার, ইনস্টাগ্রাম ও লিঙ্কডইন",
    "সোশ্যাল মিডিয়া": "সামাজিক যোগাযোগ মাধ্যম - ফেসবুক, টুইটার, ইনস্টাগ্রাম ও লিঙ্কডইন",
    "টুইটার": "সামাজিক যোগাযোগ মাধ্যম - ফেসবুক, টুইটার, ইনস্টাগ্রাম ও লিঙ্কডইন",
    "ইনস্টাগ্রাম": "সামাজিক যোগাযোগ মাধ্যম - ফেসবুক, টুইটার, ইনস্টাগ্রাম ও লিঙ্কডইন",
    "লিঙ্কডইন": "সামাজিক যোগাযোগ মাধ্যম - ফেসবুক, টুইটার, ইনস্টাগ্রাম ও লিঙ্কডইন",
    "লিপফ্রগ": "বিনোদন ও আইসিটি - ডিজিটাল মিডিয়া, গেমিং ও লিপফ্রগ প্রযুক্তি",
    "ফ্রিল্যান্সিং": "কর্মক্ষেত্রে আইসিটি ও ফ্রিল্যান্সিং",
    "মুক্তপেশা": "কর্মক্ষেত্রে আইসিটি ও ফ্রিল্যান্সিং",
    "মুক্ত পেশা": "কর্মক্ষেত্রে আইসিটি ও ফ্রিল্যান্সিং",
    "মুক্ত পেশাজীবী": "কর্মক্ষেত্রে আইসিটি ও ফ্রিল্যান্সিং",
    "ঘরে বসে": "কর্মক্ষেত্রে আইসিটি ও ফ্রিল্যান্সিং",
    "কৃত্রিম বুদ্ধিমত্তা": "একুশ শতকে কৃত্রিম বুদ্ধিমত্তা (AI) ও আধুনিক মানবসম্পদ",
    "এআই": "একুশ শতকে কৃত্রিম বুদ্ধিমত্তা (AI) ও আধুনিক মানবসম্পদ",
    "ভাবতে পারে": "একুশ শতকে কৃত্রিম বুদ্ধিমত্তা (AI) ও আধুনিক মানবসম্পদ",
    "মানুষের মতো": "একুশ শতকে কৃত্রিম বুদ্ধিমত্তা (AI) ও আধুনিক মানবসম্পদ",
    "জ্ঞানভিত্তিক": "একুশ শতক এবং তথ্য ও যোগাযোগ প্রযুক্তি - জ্ঞানভিত্তিক অর্থনীতি ও দক্ষতা",
    "অর্থনীতি": "একুশ শতক এবং তথ্য ও যোগাযোগ প্রযুক্তি - জ্ঞানভিত্তিক অর্থনীতি ও দক্ষতা",
    "টিকে থাকতে": "একুশ শতকে কৃত্রিম বুদ্ধিমত্তা (AI) ও আধুনিক মানবসম্পদ",
    "রক্ষণাবেক্ষণ": "কম্পিউটার রক্ষণাবেক্ষণে সফটওয়্যারের গুরুত্ব",
    "রেজিস্ট্রি": "রেজিস্ট্রি ক্লিনিং ও অপ্রয়োজনীয় ফাইল অপসারণ (Run Commands)",
    "ইনস্টলেশন": "সফটওয়্যার ইনস্টলেশন পদ্ধতি (Software Installation)",
    "আনইনস্টলেশন": "সফটওয়্যার আনইনস্টলেশন ও ডিলিট করার পার্থক্য (Software Uninstallation)",
    "পাইরেসি": "কপিরাইট আইন ও সফটওয়্যার পাইরেসি",
    "কপিরাইট": "কপিরাইট আইন ও সফটওয়্যার পাইরেসি",
    "তথ্য অধিকার": "তথ্য অধিকার আইন ২০০৯ ও সাইবার নৈতিকতা",
    "ফেইক নিউজ": "ফেইক নিউজ ও গুজব প্রতিরোধ",
    "গুজব": "ফেইক নিউজ ও গুজব প্রতিরোধ",
    "আসক্তি": "ডিজিটাল আসক্তি ও নার্সিসিজম",
    "নার্সিসিজম": "ডিজিটাল আসক্তি ও নার্সিসিজম",
    "সাইবার অপরাধ": "সাইবার অপরাধ ও অনলাইন নিরাপত্তা",
    "সাইবার ক্রাইম": "সাইবার অপরাধ ও অনলাইন নিরাপত্তা",
    "ট্রাবলশুটিং": "কম্পিউটার ট্রাবলশুটিং ধারণা (Troubleshooting Overview)",
    "চার্লস ব্যাবেজ": "আইসিটি বিকাশে উল্লেখযোগ্য ব্যক্তিত্ব - চার্লস ব্যাবেজ ও অ্যানালিটিক্যাল ইঞ্জিন",
    "অ্যাডা লাভলেস": "আইসিটি বিকাশে উল্লেখযোগ্য ব্যক্তিত্ব - অ্যাডা লাভলেস ও তুরিন বিশ্ববিদ্যালয় ১৮৪০",
    "তুরিন": "আইসিটি বিকাশে উল্লেখযোগ্য ব্যক্তিত্ব - অ্যাডা লাভলেস ও তুরিন বিশ্ববিদ্যালয় ১৮৪০",
    "বক্তৃতা": "আইসিটি বিকাশে উল্লেখযোগ্য ব্যক্তিত্ব - অ্যাডা লাভলেস ও তুরিন বিশ্ববিদ্যালয় ১৮৪০",
    "বক্তব্য": "আইসিটি বিকাশে উল্লেখযোগ্য ব্যক্তিত্ব - অ্যাডা লাভলেস ও তুরিন বিশ্ববিদ্যালয় ১৮৪০",
    "কোয়ান্টাম": "আইসিটি বিকাশে উল্লেখযোগ্য ব্যক্তিত্ব - স্টিভ জবস ও কোয়ান্টাম কম্পিউটার বিপ্লব",
    "ডিস্ক ক্লিনআপ": "ডিস্ক ক্লিনআপ ও ডিস্ক ডিফ্র্যাগমেন্টার",
    "ডিফ্র্যাগমেন্টার": "ডিস্ক ক্লিনআপ ও ডিস্ক ডিফ্র্যাগমেন্টার",
    "স্টিভ জবস": "আইসিটি বিকাশে উল্লেখযোগ্য ব্যক্তিত্ব - স্টিভ জবস ও কোয়ান্টাম কম্পিউটার বিপ্লব",
    "জাকারবার্গ": "আইসিটি বিকাশে উল্লেখযোগ্য ব্যক্তিত্ব - মার্ক জাকারবার্গ ও ফেসবুক",
    "ফেসবুক": "আইসিটি বিকাশে উল্লেখযোগ্য ব্যক্তিত্ব - মার্ক জাকারবার্গ ও ফেসবুক",
    "জগদীশচন্দ্র": "আইসিটি বিকাশে উল্লেখযোগ্য ব্যক্তিত্ব - ম্যাক্সওয়েল, জগদীশচন্দ্র বসু ও মার্কনি",
    "মার্কনি": "আইসিটি বিকাশে উল্লেখযোগ্য ব্যক্তিত্ব - ম্যাক্সওয়েল, জগদীশচন্দ্র বসু ও মার্কনি",
    "বিল গেটস": "আইসিটি বিকাশে উল্লেখযোগ্য ব্যক্তিত্ব - বিল গেটস ও টিম বার্নার্স-লি",
    "টিম বার্নার্স-লি": "আইসিটি বিকাশে উল্লেখযোগ্য ব্যক্তিত্ব - বিল গেটস ও টিম বার্নার্স-লি",
    "টমলিনসন": "আইসিটি বিকাশে উল্লেখযোগ্য ব্যক্তিত্ব - আইবিএম মেইনফ্রেম ও রেমন্ড টমলিনসনের ই-মেইল",
    "ই-মেইল": "আইসিটি বিকাশে উল্লেখযোগ্য ব্যক্তিত্ব - আইবিএম মেইনফ্রেম ও রেমন্ড টমলিনসনের ই-মেইল",
    "শক": "ট্রাবলশুটিং সমস্যা ৫ থেকে ৮ - ধীরগতি, মেটালিক বডি শক, হ্যাং/রিস্টার্ট ও উইন্ডোজ বুট সমস্যা",
    "মেটালিক বডি": "ট্রাবলশুটিং সমস্যা ৫ থেকে ৮ - ধীরগতি, মেটালিক বডি শক, হ্যাং/রিস্টার্ট ও উইন্ডোজ বুট সমস্যা",
    "আর্থিং": "ট্রাবলশুটিং সমস্যা ৫ থেকে ৮ - ধীরগতি, মেটালিক বডি শক, হ্যাং/রিস্টার্ট ও উইন্ডোজ বুট সমস্যা",
    "সিএমওএস": "ট্রাবলশুটিং সমস্যা ১ থেকে ৪ - পাওয়ার, মনিটর ডিসপ্লে, অতিরিক্ত তাপ ও সিএমওএস ব্যাটারি",
    "cmos": "ট্রাবলশুটিং সমস্যা ১ থেকে ৪ - পাওয়ার, মনিটর ডিসপ্লে, অতিরিক্ত তাপ ও সিএমওএস ব্যাটারি",
    "কিবোর্ড": "ট্রাবলশুটিং সমস্যা ৯ থেকে ১২ - বুট এরর, স্ক্রিন কাঁপুনী, কিবোর্ড ও মাউস ত্রুটি",
    "মাউস": "ট্রাবলশুটিং সমস্যা ৯ থেকে ১২ - বুট এরর, স্ক্রিন কাঁপুনী, কিবোর্ড ও মাউস ত্রুটি",
    "সাউন্ড": "ট্রাবলশুটিং সমস্যা ১৩ থেকে ১৬ - ইন্টারনেট সংযোগ, অডিও, ইউএসবি ড্রাইভ ও প্রিন্টার সমস্যা",
    "অডিও": "ট্রাবলশুটিং সমস্যা ১৩ থেকে ১৬ - ইন্টারনেট সংযোগ, অডিও, ইউএসবি ড্রাইভ ও প্রিন্টার সমস্যা",
    "প্রিন্টার": "ট্রাবলশুটিং সমস্যা ১৩ থেকে ১৬ - ইন্টারনেট সংযোগ, অডিও, ইউএসবি ড্রাইভ ও প্রিন্টার সমস্যা",
    "প্রিন্ট": "ট্রাবলশুটিং সমস্যা ১৩ থেকে ১৬ - ইন্টারনেট সংযোগ, অডিও, ইউএসবি ড্রাইভ ও প্রিন্টার সমস্যা"
}


def classify_intent(query: str) -> IntentResult:
    """
    Classify student query into intent, scope, and intelligent answer granularity according to NCTB textbook semantics.
    """
    q = query.strip()
    q_lower = q.lower()

    # 0. Out of Curriculum Check (Non-ICT and Chapters 3, 4, 5, 6 of NCTB ICT)
    oos_patterns = [
        # Non-ICT general domains
        r'(নদী|নদীগুলো|রাজধানী|যুদ্ধ|১৯৭১.*?মুক্তিযুদ্ধ|মুক্তিযুদ্ধ|বীরশ্রেষ্ঠ|ভূগোল|রান্না|বিরিয়ানি|ফুটবল|ক্রিকেট|বিশ্বকাপ|আবহাওয়া|বৃষ্টি|পাহাড়|পর্বত|রাজনীতি)',
        r'(অংক|বীজগণিত|জ্যামিতি|পীথাগোরাস|পীথাগোরাসের|উপপাদ্য|রসায়ন|পদার্থবিজ্ঞান|জীববিজ্ঞান)',
        # Out-of-scope ICT syllabus: Chapter 4 (Spreadsheets / Word Processing)
        r'\b(excel|spreadsheet|sum\s+function|average\s+function|cell|row|column)\b',
        r'(এক্সেল|এক্সেলে|স্প্রেডশিট|স্প্রেডশীট|সাম\s*ফাংশন|গড়ের\s*সূত্র|ওয়ার্ড প্রসেসর|এমএস ওয়ার্ড|মাইক্রোসফট ওয়ার্ড)',
        # Out-of-scope ICT syllabus: Chapter 5 (Graphics & Multimedia)
        r'\b(photoshop|illustrator|powerpoint|slide)\b',
        r'(ফটোশপ|ফটোশপে|ইলাস্ট্রেটর|পাওয়ারপয়েন্ট|পাওয়ারপয়েন্ট|স্লাইড|ছবি এডিট)',
        # Out-of-scope ICT syllabus: Other Chapters (Chapters 3, 4, 5, 6)
        r'(অধ্যায়\s*[৩-৬|3-6]|অধ্যায়\s*[৩-৬|3-6]|chapter\s*[3-6])',
        # Out-of-scope ICT syllabus: Chapter 6 (Database) & General Programming
        r'\b(database|sql|ms access|python|java|javascript|c\+\+|html|css|php)\b',
        r'(ডাটাবেজ|এসকিউএল|এক্সেস|কুয়েরি|পাইথন|পাইথনে|জাভা|এইচটিএমএল|ওয়েবপেজ ডিজাইন)'
    ]
    for pat in oos_patterns:
        if re.search(pat, q_lower):
            return IntentResult(
                primary_intent=IntentType.OUT_OF_CURRICULUM,
                intent_label_bn="সিলেবাস বহির্ভূত",
                sub_intents=[IntentType.OUT_OF_CURRICULUM],
                scope_description="সিলেবাসের বাইরের প্রশ্ন",
                target_topic=None,
                granularity=GranularityType.GENERAL
            )

    # Detect entity / topic
    detected_topic = None
    for kw, topic_name in KNOWN_TOPICS.items():
        if kw in q or kw in q_lower:
            detected_topic = topic_name
            break

    # Determine Intelligent Answer Granularity from user question phrasing
    granularity = GranularityType.GENERAL
    if re.search(r'(?:^|\s)(কবে)(?:$|\s|[?।!])|কত\s*সালে|কোন\s*সালে|কত\s*খ্রিস্টাব্দে|সাল\s*কত|কোন\s*তারিখে', q):
        granularity = GranularityType.YEAR
    elif re.search(r'(?:^|\s)(কে|কার|কারা|কাদের)(?:$|\s|[?।!])|(?:আবিষ্কারক|উদ্ভাবক|প্রতিষ্ঠাতা|জনক)\s*কে|কে\s*(?:ছিলেন|আবিষ্কার|তৈরি|প্রতিষ্ঠা|শুরু|করেছেন|করেন|দেন|দিয়েছেন|দিয়েছিলেন)|কোন\s*নারী', q) and not re.search(r'(কীভাবে|কেন|কিভাবে)', q):
        granularity = GranularityType.PERSON
    elif re.search(r'(?:^|\s)(কয়টি|কয়টি|কতটি|কতগুলো|কয়টা|কয়টা)(?:$|\s|[?।!])', q):
        granularity = GranularityType.COUNT
    elif re.search(r'এক\s*লাইনে|এক\s*বাক্যে', q):
        granularity = GranularityType.ONE_LINE
    elif re.search(r'সংক্ষেপে|ছোট\s*করে', q):
        granularity = GranularityType.SHORT
    elif re.search(r'বিস্তারিত|বিশদভাবে|ব্যাখ্যা\s*কর|ব্যাখ্যা\s*করো', q):
        granularity = GranularityType.DETAILED
    elif re.search(r'কী\s*কী|কি\s*কি|প্রকারভেদ|তালিকা|নামগুলো|নাম\s*বলো|নাম\s*কী\s*কী|নাম\s*কি\s*কি', q):
        granularity = GranularityType.LIST
    elif re.search(r'উদাহরণ|উদাহরণ\s*দাও', q):
        granularity = GranularityType.EXAMPLES
    elif re.search(r'(?:^|\s)(কেন|কী\s*জন্য|কি\s*জন্য)(?:$|\s|[?।!])|কী\s*কারণে|কি\s*কারণে', q):
        granularity = GranularityType.WHY
    elif re.search(r'কীভাবে|কিভাবে|কী\s*উপায়ে|কি\s*উপায়ে|পদ্ধতি|প্রক্রিয়া', q):
        granularity = GranularityType.HOW
    elif re.search(r'সম্পর্কে\s*বলো|সম্পর্কে\s*বল|সম্পর্কে\s*জানাও', q):
        granularity = GranularityType.OVERVIEW
    elif re.search(r'(?:^|\s)(কী|কি)(?:$|\s|[?।!])|কাকে\s*বলে|বলতে\s*কী|বলতে\s*কি', q):
        granularity = GranularityType.WHAT

    # 1. Multi-Intent Detection (e.g. "কী এবং কীভাবে ছড়ায়", "সংজ্ঞা ও ছড়ানোর উপায়")
    # Note: "কী" or "কি" must NOT simply be part of "কীভাবে"
    q_without_kivabe = re.sub(r'কীভাবে|কিভাবে', '', q)
    has_def_cue = bool(re.search(r'(?:\b|\s|^)(কী|কি)(?:\b|\s|[?।!]|$)|(কাকে বলে|বলতে কী|বলতে কি|সংজ্ঞা)', q_without_kivabe))
    has_mech_cue = bool(re.search(r'(কীভাবে ছড়ায়|কিভাবে ছড়ায়|ছড়ানোর (উপায়|পদ্ধতি|মাধ্যম)|কীভাবে সংক্রামিত|কীভাবে কাজ করে)', q))
    has_conjunction = bool(re.search(r'(এবং|ও|আর|সাথে|পাশাপাশি)', q))

    if has_def_cue and has_mech_cue and has_conjunction:
        return IntentResult(
            primary_intent=IntentType.MULTI_INTENT,
            intent_label_bn="সংজ্ঞা ও ছড়ানোর পদ্ধতি",
            sub_intents=[IntentType.DEFINITION, IntentType.MECHANISM],
            scope_description="বই অনুসারে সংজ্ঞা + কীভাবে ছড়ায়—দুই অংশই আলাদাভাবে দেবে।",
            target_topic=detected_topic,
            granularity=granularity
        )

    # 2. Examples Intent (e.g. "ভাইরাসের উদাহরণ দাও", "কয়েকটি ভাইরাসের নাম লেখ")
    if re.search(r'(উদাহরণ|উদাহরণ দাও|উদাহরণগুলো|নাম দাও|নাম কী কী|কয়েকটি.*?নাম|নামগুলো|তালিকা)', q):
        return IntentResult(
            primary_intent=IntentType.EXAMPLES,
            intent_label_bn="পাঠ্যবইয়ের উদাহরণ",
            sub_intents=[IntentType.EXAMPLES],
            scope_description="শুধু বইয়ে থাকা প্রাসঙ্গিক উদাহরণগুলো দেবে।",
            target_topic=detected_topic,
            granularity=granularity
        )

    # 3. Prevention & Safety Intent (e.g. "ভাইরাস থেকে কীভাবে নিরাপদ থাকব?", "প্রতিরোধের উপায় কী?")
    if re.search(r'(নিরাপদ থাকব|নিরাপদে থাকব|নিরাপদ রাখা|নিরাপদ রাখার উপায়|সুরক্ষিত রাখার উপায়|কীভাবে নিরাপদ|প্রতিরোধ|সুরক্ষা|বাঁচার উপায়|সতর্কতা|নিরাপদ থাকার উপায়|নিরাপত্তা নিশ্চিত|মুক্তির উপায়|মুক্ত থাকার উপায়|মুক্ত হওয়ার উপায়)', q):
        return IntentResult(
            primary_intent=IntentType.PREVENTION,
            intent_label_bn="নিরাপত্তা ও প্রতিরোধের উপায়",
            sub_intents=[IntentType.PREVENTION],
            scope_description="শুধু বই অনুসারে প্রতিরোধ/নিরাপত্তার উপায় দেবে।",
            target_topic=detected_topic,
            granularity=granularity
        )

    # 4. Mechanism / Transmission / Process (e.g. "কম্পিউটার ভাইরাস কীভাবে ছড়ায়?", "কীভাবে ইনস্টল/আনইনস্টল করব?")
    if re.search(r'(কীভাবে.*?ছড়ায়|কিভাবে.*?ছড়ায়|ছড়ায়|ছড়ানোর|সংক্রমণ|কীভাবে কাজ করে|কীভাবে আনইনস্টল|কীভাবে ইনস্টল|কীভাবে পরিষ্কার)', q):
        return IntentResult(
            primary_intent=IntentType.MECHANISM,
            intent_label_bn="ছড়ানোর পদ্ধতি ও প্রক্রিয়া",
            sub_intents=[IntentType.MECHANISM],
            scope_description="শুধু বই অনুসারে ছড়ানোর পদ্ধতি বা কার্যপদ্ধতি দেবে।",
            target_topic=detected_topic,
            granularity=granularity
        )

    # 5. Symptoms Intent (e.g. "লক্ষণগুলো কী কী?", "আক্রান্ত হলে কী হয়?", "কীভাবে বুঝব?")
    if re.search(r'(লক্ষণ|উপসর্গ|আক্রান্ত হলে|সংক্রমিত হলে|ঢুকলে|প্রবেশ করলে|কীভাবে বুঝব)', q):
        return IntentResult(
            primary_intent=IntentType.SYMPTOMS,
            intent_label_bn="আক্রমণের লক্ষণ",
            sub_intents=[IntentType.SYMPTOMS],
            scope_description="শুধু বই অনুসারে ভাইরাস আক্রান্ত হওয়ার লক্ষণগুলো দেবে।",
            target_topic=detected_topic,
            granularity=granularity
        )

    # 6. Rules / Pillars Intent (e.g. "পাসওয়ার্ড তৈরির নিয়মগুলো কী?", "৪টি স্তম্ভ কী?")
    if re.search(r'(নিয়ম|নিয়ম|নিয়মাবলি|নিয়মাবলি|নিয়মগুলো|নিয়মগুলো|স্তম্ভ|৪টি স্তম্ভ|চারটি স্তম্ভ|৫টি|পাঁচটি|বৈশিষ্ট্য)', q):
        return IntentResult(
            primary_intent=IntentType.RULES,
            intent_label_bn="নিয়ম ও নির্দেশিকা",
            sub_intents=[IntentType.RULES],
            scope_description="শুধু বই অনুসারে নিয়মাবলি বা স্তম্ভসমূহ পয়েন্ট আকারে দেবে।",
            target_topic=detected_topic,
            granularity=granularity
        )

    # 7. Troubleshooting Intent (e.g. "কম্পিউটার ঘন ঘন রিস্টার্ট হলে কী করব?", "ডিসপ্লে না আসলে?", "শক লাগে কেন?")
    if re.search(r'(হলে কী করব|হলে কি করব|সমাধান কী|ত্রুটি|রিস্টার্ট|ডিসপ্লে|চালু না হলে|ট্রাবলশুটিং|শক লাগে|শক লাগলে|মেটালিক বডি|আর্থিং|কাজ না করলে|কাজ করছে না|ভুল দেখালে|বের হচ্ছে না|কী পরীক্ষা করতে হবে|কি পরীক্ষা করতে হবে|করণীয় কী|করণীয় কী|করণীয় কি|করণীয় কি)', q):
        return IntentResult(
            primary_intent=IntentType.TROUBLESHOOTING,
            intent_label_bn="ট্রাবলশুটিং ও সমাধান",
            sub_intents=[IntentType.TROUBLESHOOTING],
            scope_description="শুধু বই অনুসারে নির্দিষ্ট সমস্যার সমাধান প্রক্রিয়া দেবে।",
            target_topic=detected_topic,
            granularity=granularity
        )

    # 8. History / Person Intent (e.g. "চার্লস ব্যাবেজ কেন বিখ্যাত?", "অ্যাডা লাভলেস কে ছিলেন?")
    is_ai_or_system_query = bool(re.search(r'(কৃত্রিম বুদ্ধিমত্তা|\bai\b|ভাইরাস|পাসওয়ার্ড|পাসওয়ার্ড|ই-লার্নিং|স্যাটেলাইট)', q, re.I))
    if not is_ai_or_system_query and (re.search(r'(কেন বিখ্যাত|কে ছিলেন|অবদান কী|আবিষ্কারক|আবিষ্কার করেন|কে আবিষ্কার|কে তৈরি|কে শুরু|কে প্রতিষ্ঠা|ইতিহাস|ভূমিকা কী|বক্তৃতা|বক্তব্য|তুরিন|কত সালে)', q) or any(p in q for p in ["চার্লস ব্যাবেজ", "অ্যাডা লাভলেস", "জগদীশচন্দ্র", "মার্কনি", "বিল গেটস", "টিম বার্নার্স-লি", "ফ্রেড কোহেন", "স্টিভ জবস", "জাকারবার্গ", "টমলিনসন"])):
        if not re.search(r'(কীভাবে ছড়ায়|প্রতিরোধ|উদাহরণ)', q):
            return IntentResult(
                primary_intent=IntentType.HISTORY_PERSON,
                intent_label_bn="ঐতিহাসিক ব্যক্তিত্ব ও অবদান",
                sub_intents=[IntentType.HISTORY_PERSON],
                scope_description="বই অনুসারে সংশ্লিষ্ট ব্যক্তির অবদান ও পরিচয় দেবে।",
                target_topic=detected_topic,
                granularity=granularity
            )

    # 9. Definition Intent (e.g. "কম্পিউটার ভাইরাস কী?", "ই-লার্নিং কাকে বলে?", "ই-সার্ভিস বলতে কী বোঝায়?")
    if re.search(r'(কী\?|কি\?|কী$|কি$|কী |কি |কাকে বলে|বলতে কী বোঝায়|বলতে কি বোঝায়|স্বরূপ|পরিচয়)', q):
        return IntentResult(
            primary_intent=IntentType.DEFINITION,
            intent_label_bn="পাঠ্যবইয়ের সংজ্ঞা",
            sub_intents=[IntentType.DEFINITION],
            scope_description="শুধু বই অনুসারে সংজ্ঞা দেবে।",
            target_topic=detected_topic,
            granularity=granularity
        )

    # Default: General curriculum question
    return IntentResult(
        primary_intent=IntentType.GENERAL,
        intent_label_bn="পাঠ্যবইভিত্তিক উত্তর",
        sub_intents=[IntentType.GENERAL],
        scope_description="বইয়ের সংশ্লিষ্ট অংশ থেকে সংক্ষিপ্ত ও প্রাসঙ্গিক উত্তর দেবে।",
        target_topic=detected_topic,
        granularity=granularity
    )
