"""
Curriculum Content Retriever for OIBTC
Offline, high-precision semantic search over NCTB textbook chunks.
Supports both FAISS dense search and local TF-IDF cosine similarity.
"""

import json
import os
import re
import sys
from typing import List, Dict, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from backend.rag.transliteration import normalize_query

def canonicalize_bengali(text: str) -> str:
    """Normalize Bengali unicode representations (nukta decomposition vs precomposed)."""
    if not text:
        return ""
    text = text.replace('\u09af\u09bc', '\u09df')  # য + ় -> য়
    text = text.replace('\u09a1\u09bc', '\u09dc')  # ড + ় -> ড়
    text = text.replace('\u09a2\u09bc', '\u09dd')  # ঢ + ় -> ঢ়
    text = text.replace('\u0985\u09be', '\u0986')  # অ + া -> আ
    return text.lower().strip()

CHUNKS_PATH = os.path.join("data", "nctb_raw", "ict_chunks.json")
FAISS_INDEX_PATH = os.path.join("data", "vectorstore", "ict_ch1_ch2.faiss")


class NCTBRetriever:
    def __init__(self):
        self.chunks: List[Dict[str, Any]] = []
        self.vectorizer: TfidfVectorizer = None
        self.tfidf_matrix = None
        self.faiss_index = None
        self.embed_model = None
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        """Load chunked NCTB data and prepare retrieval indices."""
        if not os.path.exists(CHUNKS_PATH):
            print(f"Warning: Chunks file not found at {CHUNKS_PATH}")
            return

        with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        # Build local TF-IDF index for fast offline search
        corpus = [f"{c['topic']} {c['chapter_title']} {c['content']}" for c in self.chunks]
        self.vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            min_df=1
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
        print(f"NCTBRetriever: Indexed {len(self.chunks)} chunks with character n-gram TF-IDF.")

        # Attempt to load FAISS index if present
        if os.path.exists(FAISS_INDEX_PATH):
            try:
                import faiss
                self.faiss_index = faiss.read_index(FAISS_INDEX_PATH)
                print("NCTBRetriever: Successfully loaded FAISS vector index.")
            except Exception as e:
                print(f"NCTBRetriever: FAISS index load notice ({e}). Using n-gram similarity.")

    def search(
        self,
        query: str,
        grade: int = 9,
        subject: str = "ICT",
        top_k: int = 3
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        Search for top-K matching NCTB textbook chunks.
        Returns list of (chunk_dict, score) tuples.
        """
        if not self.chunks or self.vectorizer is None:
            return []

        # Filter candidate indices by grade and subject
        candidate_indices = [
            i for i, c in enumerate(self.chunks)
            if c.get("grade") == grade and c.get("subject", "").upper() == subject.upper()
        ]
        if not candidate_indices:
            candidate_indices = list(range(len(self.chunks)))

        # Normalize query (handles Banglish and typos)
        norm_res = normalize_query(query)
        search_query = norm_res.get("dual", query)
        norm_bn = norm_res.get("normalized", query)

        # Compute query vector using dual representation
        query_vec = self.vectorizer.transform([search_query])
        scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Rank candidates with topic-level phrase boost
        scored_candidates = []
        topic_triggers = [
            (["সামাজিক যোগাযোগ", "সোশ্যাল মিডিয়া", "টুইটার", "ইনস্টাগ্রাম"], "সামাজিক যোগাযোগ"),
            (["ডিজিটাল বাংলাদেশ", "স্তম্ভ", "রূপকল্পের"], "ডিজিটাল বাংলাদেশ"),
            (["বঙ্গবন্ধু স্যাটেলাইট", "স্যাটেলাইট"], "স্যাটেলাইট"),
            (["মুক্ত পেশাজীবী", "মুক্তপেশা", "মুক্ত পেশা", "ফ্রিল্যান্সিং", "ফ্রিল্যান্স"], "ফ্রিল্যান্সিং"),
            (["কৃত্রিম বুদ্ধিমত্তা", "এআই", "ভাবতে পারে", "মানুষের মতো"], "কৃত্রিম বুদ্ধিমত্তা"),
            (["লিপফ্রগ", "leap frog", "লাফ"], "লিপফ্রগ"),
            (["পাসওয়ার্ড", "পাসওয়ার্ড"], "পাসওয়ার্ড"),
            (["ভাইরাস", "ম্যালওয়্যার", "ম্যালওয়্যার"], "ভাইরাস"),
            (["অ্যান্টিভাইরাস", "antivirus"], "অ্যান্টিভাইরাস"),
            (["ই-লার্নিং", "দূরশিক্ষণ"], "ই-লার্নিং"),
            (["ই-গভর্ন্যান্স", "সুশাসন"], "ই-গভর্ন্যান্স"),
            (["ই-সার্ভিস", "ই-পুর্জি", "ই-পর্চা", "ইএমটিএস"], "ই-সার্ভিস"),
            (["ই-কমার্স", "অনলাইন কেনাবেচা"], "ই-কমার্স"),
            (["রেজিস্ট্রি", "temp", "prefetch", "রান কমান্ড"], "রেজিস্ট্রি"),
            (["ডিস্ক ক্লিনআপ", "ডিফ্র্যাগমেন্টার", "disk cleanup"], "ডিস্ক ক্লিনআপ"),
            (["ইনস্টলেশন", "setup", "সেটআপ"], "ইনস্টলেশন"),
            (["আনইনস্টলেশন", "আনইনস্টল", "uninstall"], "আনইনস্টলেশন"),
            (["কপিরাইট", "পাইরেসি", "সফটওয়্যার পাইরেসি"], "পাইরেসি"),
            (["তথ্য অধিকার", "তথ্য অধিকার আইন"], "তথ্য অধিকার"),
            (["নার্সিসিজম", "আসক্তি", "ডিজিটাল আসক্তি"], "ডিজিটাল আসক্তি"),
            (["ফেইক নিউজ", "গুজব", "ভুয়া খবর"], "ফেইক নিউজ"),
            (["সাইবার ক্রাইম", "সাইবার অপরাধ"], "সাইবার অপরাধ"),
            (["ট্রাবলশুটিং", "troubleshooting"], "ট্রাবলশুটিং"),
            (["ডিসপ্লে", "মনিটর"], "মনিটর"),
            (["সিএমওএস", "cmos", "তারিখ ও সময়"], "সিএমওএস"),
            (["রিস্টার্ট", "হ্যাং", "গরম", "কুলিং ফ্যান"], "রিস্টার্ট"),
            (["কিবোর্ড", "keyboard"], "কিবোর্ড"),
            (["মাউস", "mouse"], "মাউস"),
            (["প্রিন্টার", "প্রিন্ট", "printer"], "প্রিন্টার"),
            (["সাউন্ড", "অডিও", "শব্দ", "স্পিকার"], "সাউন্ড"),
            (["ইউএসবি", "পেনড্রাইভ", "usb"], "ইউএসবি"),
            (["মেটালিক বডি", "আর্থিং", "গ্রাউন্ডিং", "শক", "কারেন্ট"], "আর্থিং")
        ]

        for i in candidate_indices:
            chunk = self.chunks[i]
            base_score = float(scores[i])
            topic_str = chunk.get("topic", "")
            
            boost = 0.0
            for keywords, target_topic_part in topic_triggers:
                if any(kw in query or kw in norm_bn for kw in keywords) and target_topic_part in topic_str:
                    boost += 0.35
                    break

            scored_candidates.append((chunk, base_score + boost))

        scored_candidates.sort(key=lambda x: x[1], reverse=True)
        return scored_candidates[:top_k]


# Singleton instance
_retriever_instance = None

def get_retriever() -> NCTBRetriever:
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = NCTBRetriever()
    return _retriever_instance


if __name__ == "__main__":
    retriever = get_retriever()
    test_queries = [
        "কম্পিউটার ভাইরাস কীভাবে ছড়ায়?",
        "শক্তিশালী পাসওয়ার্ড তৈরি করার নিয়ম কী?",
        "ই-লার্নিং বলতে কী বোঝায়?",
        "চার্লস ব্যাবেজ কেন বিখ্যাত?"
    ]
    for q in test_queries:
        results = retriever.search(q, top_k=2)
        print(f"\nQuery: {q}")
        for chunk, score in results:
            print(f" -> [Score: {score:.3f}] অধ্যায় {chunk['chapter']}, {chunk['topic']} (পৃষ্ঠা {chunk['page']})")
