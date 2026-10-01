"""
Banglish & Typo Normalization Engine for OIBTC
Author: Senior AI & NLP Engineer
Converts Romanized Bangla (Banglish), English ICT terms, and typos into standard Bengali curriculum representations.
Runs 100% offline with zero external dependencies and < 1ms latency.
"""

import re
import sys
from typing import Dict, Any, List, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def canonicalize_bengali(text: str) -> str:
    """Normalize Bengali unicode representations (nukta decomposition vs precomposed)."""
    if not text:
        return ""
    text = text.replace('\u09af\u09bc', '\u09df')  # য + ় -> য়
    text = text.replace('\u09a1\u09bc', '\u09dc')  # ড + ় -> ড়
    text = text.replace('\u09a2\u09bc', '\u09dd')  # ঢ + ় -> ঢ়
    text = text.replace('\u0985\u09be', '\u0986')  # অ + া -> আ
    return text.lower().strip()
ICT_LEXICON: List[Tuple[str, str]] = [
    # Multi-word phrases first (order matters)
    (r"\bstrong password\b", "শক্তিশালী পাসওয়ার্ড"),
    (r"\bcomputer virus\b", "কম্পিউটার ভাইরাস"),
    (r"\bdisk cleanup\b", "ডিস্ক ক্লিনআপ"),
    (r"\bdisk defragmenter\b", "ডিস্ক ডিফ্র্যাগমেন্টার"),
    (r"\bsoftware uninstall\b", "সফটওয়্যার আনইনস্টলেশন"),
    (r"\bsoftware install\b", "সফটওয়্যার ইনস্টলেশন"),
    (r"\bfake news\b", "ফেইক নিউজ"),
    (r"\bcyber crime\b", "সাইবার অপরাধ"),
    (r"\bdigital addiction\b", "ডিজিটাল আসক্তি"),
    (r"\bsocial media\b", "সামাজিক যোগাযোগ"),
    (r"\bcharles babbage\b", "চার্লস ব্যাবেজ"),
    (r"\bada lovelace\b", "অ্যাডা লাভলেস"),
    (r"\bbill gates\b", "বিল গেটস"),
    (r"\btim berners-lee\b", "টিম বার্নার্স-লি"),
    (r"\bmark zuckerberg\b", "মার্ক জাকারবার্গ"),
    (r"\bsteve jobs\b", "স্টিভ জবস"),
    (r"\bjagdish chandra bose\b", "জগদীশচন্দ্র বসু"),
    (r"\bmetallic body\b", "মেটালিক বডি"),
    (r"\btwo factor authentication\b", "টু-ফ্যাক্টর অথেনটিকেশন"),
    (r"\b2fa\b", "টু-ফ্যাক্টর অথেনটিকেশন"),
    (r"\bcmos battery\b", "সিএমওএস ব্যাটারি"),
    (r"\bcmos\b", "সিএমওএস"),
    (r"\bchapter\s*1\b", "অধ্যায় ১"),
    (r"\bchapter\s*2\b", "অধ্যায় ২"),
    (r"\bchapter\b", "অধ্যায়"),
    (r"\brange\b", "রেঞ্জ"),
    (r"\brun commands?\b", "রান কমান্ড"),

    # Single ICT domain terms
    (r"\bkompiutare\b", "কম্পিউটারে"),
    (r"\bkompiutarer\b", "কম্পিউটারের"),
    (r"\bkompiutar\b", "কম্পিউটার"),
    (r"\bcomputer\b", "কম্পিউটার"),
    (r"\bcomputers\b", "কম্পিউটার"),
    (r"\bpassword\b", "পাসওয়ার্ড"),
    (r"\bpassward\b", "পাসওয়ার্ড"),
    (r"\bpasswrord\b", "পাসওয়ার্ড"),
    (r"\bviruser\b", "ভাইরাসের"),
    (r"\bvirus\b", "ভাইরাস"),
    (r"\bmalware\b", "ম্যালওয়্যার"),
    (r"\bantivirus\b", "অ্যান্টিভাইরাস"),
    (r"\buninstall\b", "আনইনস্টল"),
    (r"\binstall\b", "ইনস্টল"),
    (r"\binstallation\b", "ইনস্টলেশন"),
    (r"\buninstallation\b", "আনইনস্টলেশন"),
    (r"\bcleanup\b", "ক্লিনআপ"),
    (r"\bdifragmantar\b", "ডিফ্র্যাগমেন্টার"),
    (r"\bdefragmantar\b", "ডিফ্র্যাগমেন্টার"),
    (r"\bdefragmenter\b", "ডিফ্র্যাগমেন্টার"),
    (r"\btroubleshooting\b", "ট্রাবলশুটিং"),
    (r"\bearthing\b", "আর্থিং"),
    (r"\bgrounding\b", "আর্থিং"),
    (r"\breboot\b", "রিস্টার্ট"),
    (r"\brestart\b", "রিস্টার্ট"),
    (r"\bhanging?\b", "হ্যাং"),
    (r"\bbattery\b", "ব্যাটারি"),
    (r"\bfreelancing\b", "ফ্রিল্যান্সিং"),
    (r"\bmuktopesha\b", "মুক্তপেশা"),
    (r"\bsatellite\b", "স্যাটেলাইট"),
    (r"\bbangabandhu satellite\b", "বঙ্গবন্ধু স্যাটেলাইট"),
    (r"\bfacebook\b", "ফেসবুক"),
    (r"\btwitter\b", "টুইটার"),
    (r"\binstagram\b", "ইনস্টাগ্রাম"),
    (r"\blinkedin\b", "লিঙ্কডইন"),
    (r"\bai\b", "কৃত্রিম বুদ্ধিমত্তা"),
    (r"\be-learning\b", "ই-লার্নিং"),
    (r"\belearning\b", "ই-লার্নিং"),
    (r"\be-governance\b", "ই-গভর্ন্যান্স"),
    (r"\begovernance\b", "ই-গভর্ন্যান্স"),
    (r"\be-services?\b", "ই-সার্ভিস"),
    (r"\beservices?\b", "ই-সার্ভিস"),
    (r"\be-purjee\b", "ই-পুর্জি"),
    (r"\bepurjee\b", "ই-পুর্জি"),
    (r"\be-purji\b", "ই-পুর্জি"),
    (r"\bepurji\b", "ই-পুর্জি"),
    (r"\bemts\b", "ইএমটিএস"),
    (r"\be-porcha\b", "ই-পর্চা"),
    (r"\beporcha\b", "ই-পর্চা"),
    (r"\be-commerce\b", "ই-কমার্স"),
    (r"\becommerce\b", "ই-কমার্স"),
    (r"\bcopyright\b", "কপিরাইট"),
    (r"\bpiracy\b", "পাইরেসি"),
    (r"\baddiction\b", "আসক্তি"),
    (r"\bnarcissism\b", "নার্সিসিজম"),
    (r"\bdisplay\b", "ডিসপ্লে"),
    (r"\bmonitor\b", "মনিটর"),
    (r"\bram\b", "র‍্যাম"),
    (r"\bkeyboard\b", "কিবোর্ড"),
    (r"\bmouse\b", "মাউস"),
    (r"\bprinter\b", "প্রিন্টার"),
    (r"\blan\b", "ল্যান"),
    (r"\busb\b", "ইউএসবি"),
    (r"\bsata\b", "সাটা"),
    (r"\bbios\b", "বায়োস"),
    (r"\bpower\b", "পাওয়ার"),
    (r"\bcable\b", "ক্যাবল"),
    (r"\blan cable\b", "ল্যান ক্যাবল"),
    (r"\bheating\b", "অতিরিক্ত তাপ"),
    (r"\bcooling fan\b", "কুলিং ফ্যান"),
    (r"\bfan\b", "ফ্যান"),
    (r"\btemp\b", "temp"),
    (r"\bprefetch\b", "prefetch"),
    (r"\bqubit\b", "কিউবিট"),
    (r"\bquantum\b", "কোয়ান্টাম"),
]

# Banglish Conversational Grammar & Question Words
BANGLISH_GRAMMAR: List[Tuple[str, str]] = [
    (r"\bkivabe\b", "কীভাবে"),
    (r"\bkibhabe\b", "কীভাবে"),
    (r"\bkemne\b", "কীভাবে"),
    (r"\bhow\b", "কীভাবে"),
    (r"\bki\b", "কী"),
    (r"\bkee\b", "কী"),
    (r"\bwhat\b", "কী"),
    (r"\bkeno\b", "কেন"),
    (r"\bkno\b", "কেন"),
    (r"\bwhy\b", "কেন"),
    (r"\bkoto\b", "কত"),
    (r"\bprokar\b", "প্রকার"),
    (r"\brokom\b", "রকম"),
    (r"\btypes?\b", "প্রকার"),
    (r"\brules?\b", "নিয়ম"),
    (r"\bniyom\b", "নিয়ম"),
    (r"\bniyomaboli\b", "নিয়মাবলি"),
    (r"\bbolte\b", "বলতে"),
    (r"\bbujhai\b", "বোঝায়"),
    (r"\bbujhay\b", "বোঝায়"),
    (r"\bbujhi\b", "বোঝায়"),
    (r"\bchoray\b", "ছড়ায়"),
    (r"\bchhoray\b", "ছড়ায়"),
    (r"\bchorai\b", "ছড়ায়"),
    (r"\bspreads?\b", "ছড়ায়"),
    (r"\bkaj\b", "কাজ"),
    (r"\bkaaj\b", "কাজ"),
    (r"\bwork\b", "কাজ"),
    (r"\bhoy\b", "হয়"),
    (r"\bhoi\b", "হয়"),
    (r"\blakkhan\b", "লক্ষণ"),
    (r"\blokkhon\b", "লক্ষণ"),
    (r"\bsymptoms?\b", "লক্ষণ"),
    (r"\bupay\b", "উপায়"),
    (r"\bupai\b", "উপায়"),
    (r"\bways?\b", "উপায়"),
    (r"\bprotirodh\b", "প্রতিরোধ"),
    (r"\bbachar\b", "বাঁচার"),
    (r"\bprotection\b", "প্রতিরোধ"),
    (r"\bprevention\b", "প্রতিরোধ"),
    (r"\bparthokko\b", "পার্থক্য"),
    (r"\bdifference\b", "পার্থক্য"),
    (r"\bdiff\b", "পার্থক্য"),
    (r"\bdhap\b", "ধাপ"),
    (r"\bsteps?\b", "ধাপ"),
    (r"\bsomadhan\b", "সমাধান"),
    (r"\bsolution\b", "সমাধান"),
    (r"\bshuru\b", "শুরু"),
    (r"\bstart\b", "শুরু"),
    (r"\bkore\b", "করে"),
    (r"\bkorbo\b", "করব"),
    (r"\bkorum\b", "করব"),
    (r"\bbananor\b", "বানানোর"),
    (r"\btoirir\b", "তৈরির"),
    (r"\btoiri\b", "তৈরি"),
    (r"\bshoktishali\b", "শক্তিশালী"),
    (r"\bdhukle\b", "ঢুকলে"),
    (r"\bnosto\b", "নষ্ট"),
    (r"\bgulo\b", "গুলো"),
    (r"\bebong\b", "এবং"),
    (r"\band\b", "এবং"),
    (r"\bar\b", "আর"),
    (r"\bsomossa\b", "সমস্যা"),
    (r"\bproblem\b", "সমস্যা"),
    (r"\bbistarito\b", "বিস্তারিত"),
    (r"\bdetails?\b", "বিস্তারিত"),
    (r"\bsongkhepe\b", "সংক্ষেপে"),
    (r"\bshort\b", "সংক্ষেপে"),
    (r"\bshob\b", "সব"),
    (r"\bshobgulo\b", "সবগুলো"),
    (r"\bkhoti\b", "ক্ষতি"),
    (r"\bharm\b", "ক্ষতি"),
    (r"\bmukti\b", "মুক্তি"),
    (r"\blage\b", "লাগে"),
    (r"\blakbe\b", "লাগবে"),
    (r"\budahoron\b", "উদাহরণ"),
    (r"\bexample\b", "উদাহরণ"),
    (r"\bnam\b", "নাম"),
    (r"\bnames?\b", "নাম"),
    (r"\ber\b", "এর"),
    (r"\beta\b", "এটা"),
    (r"\beti\b", "এটি"),
    (r"\betar\b", "এটার"),
    (r"\bprothom\b", "প্রথম"),
    (r"\bprothomti\b", "প্রথমটি"),
    (r"\bditiyo\b", "দ্বিতীয়"),
    (r"\bditiyoti\b", "দ্বিতীয়টি"),
    (r"\bfirst\b", "প্রথমটি"),
    (r"\bsecond\b", "দ্বিতীয়টি"),
]

# Bengali Typo Normalization (Common student mistakes)
TYPO_MAPPING: List[Tuple[str, str]] = [
    (r"কমপিউটার", "কম্পিউটার"),
    (r"শক্তিসালী", "শক্তিশালী"),
    (r"পাসওয়ার্ডের", "পাসওয়ার্ডের"),
    (r"পাসয়ার্ড", "পাসওয়ার্ড"),
    (r"পাসওর্য়াড", "পাসওয়ার্ড"),
    (r"পাসওার্ড", "পাসওয়ার্ড"),
    (r"নিয়োম", "নিয়ম"),
    (r"নিয়মাবলি", "নিয়মাবলি"),
    (r"লক্ষন", "লক্ষণ"),
    (r"লকখন", "লক্ষণ"),
    (r"ডিষ্ক", "ডিস্ক"),
    (r"ডিফ্রাগমেন্টার", "ডিফ্র্যাগমেন্টার"),
    (r"ডিফ্রেগমেন্টার", "ডিফ্র্যাগমেন্টার"),
    (r"বেটারি", "ব্যাটারি"),
    (r"সিএমস", "সিএমওএস"),
    (r"ম্যালও্যার", "ম্যালওয়্যার"),
    (r"ম্যালওয়ার", "ম্যালওয়্যার"),
    (r"ইলার্নিং", "ই-লার্নিং"),
    (r"ইগভর্ন্যান্স", "ই-গভর্ন্যান্স"),
    (r"ইসার্ভিস", "ই-সার্ভিস"),
    (r"ইপুর্জি", "ই-পুর্জি"),
    (r"ইপর্চা", "ই-পর্চা"),
    (r"ইকমার্স", "ই-কমার্স"),
    (r"ট্রাবলশুটিংয়ের", "ট্রাবলশুটিং"),
    (r"ট্রাবলসুটিং", "ট্রাবলশুটিং"),
    (r"আর্থিংয়ের", "আর্থিং"),
    (r"ক্যাবল", "কেবল"),
    (r"কাঁপুনী", "কাঁপুনী"),
]


def normalize_query(query: str) -> Dict[str, Any]:
    """
    Analyzes student query, detects Banglish / typos, and produces
    normalized Bengali representation as well as dual-script search vectors.
    """
    raw = query.strip()
    if not raw:
        return {"raw": "", "normalized": "", "dual": "", "is_banglish": False}

    has_latin = bool(re.search(r"[a-zA-Z]", raw))
    text = raw.lower()

    # Step 1: Fix Bengali typos first if query contains Bengali characters
    for pattern, repl in TYPO_MAPPING:
        text = re.sub(pattern, repl, text)

    # Step 2: If Latin characters are present, run ICT Lexicon replacement
    if has_latin:
        for pattern, repl in ICT_LEXICON:
            text = re.sub(pattern, repl, text)

        for pattern, repl in BANGLISH_GRAMMAR:
            text = re.sub(pattern, repl, text)

    # Clean up multi-spaces
    normalized = re.sub(r"\s+", " ", text).strip()

    # Build dual query for retrieval (original + normalized Bengali terms)
    if has_latin:
        dual_query = f"{raw} {normalized}".strip()
    else:
        dual_query = normalized

    return {
        "raw": raw,
        "normalized": normalized,
        "dual": dual_query,
        "is_banglish": has_latin
    }


if __name__ == "__main__":
    sample_queries = [
        "strong password bananor rules ki ki?",
        "computer virus ki ebong kivabe chhoray?",
        "e-learning bolte ki bujhai?",
        "software uninstall kivabe kore?",
        "disk defragmenter er kaj ki?",
        "earthing keno lage?",
        "কমপিউটার ভাইরাসের লক্ষন গুলা কি কি?",
        "শক্তিসালী পাসয়ার্ড বানানোর ৫টি নিয়োম",
        "ডিষ্ক ডিফ্রেগমেন্টার এর কাজ কি?"
    ]
    print("Testing Banglish & Typo Normalizer:")
    for q in sample_queries:
        res = normalize_query(q)
        print(f"\nRaw       : {res['raw']}")
        print(f"Normalized: {res['normalized']}")
        print(f"Dual Query: {res['dual']}")
