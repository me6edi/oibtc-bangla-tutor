"""
NCTB Textbook Ingestion & Vector Indexing Script
Offline Intelligent Bangla Tutoring Chatbot (OIBTC)
"""

import json
import os
import pickle
import re
from typing import List, Dict, Any

RAW_DATA_PATH = os.path.join("data", "nctb_raw", "ict_class9_10_ch1_ch2.json")
CHUNKS_OUTPUT_PATH = os.path.join("data", "nctb_raw", "ict_chunks.json")
VECTORSTORE_DIR = os.path.join("data", "vectorstore")
FAISS_INDEX_PATH = os.path.join(VECTORSTORE_DIR, "ict_ch1_ch2.faiss")
METADATA_PATH = os.path.join(VECTORSTORE_DIR, "ict_metadata.pkl")


def clean_bengali_text(text: str) -> str:
    """Normalize Bengali text by removing superfluous whitespace and non-standard symbols."""
    text = re.sub(r"\r\n|\r", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def chunk_topic(item: Dict[str, Any], max_words: int = 120, overlap: int = 25) -> List[Dict[str, Any]]:
    """Divide a topic content into overlapping chunks preserving sentence boundaries."""
    content = clean_bengali_text(item["content"])
    sentences = re.split(r"(?<=[।!?\n])\s*", content)
    chunks = []
    current_sentences = []
    current_len = 0

    for sentence in sentences:
        s = sentence.strip()
        if not s:
            continue
        words = s.split()
        if current_len + len(words) > max_words and current_sentences:
            chunk_text = " ".join(current_sentences)
            chunks.append(chunk_text)
            # Retain overlap sentences
            overlap_sentences = []
            overlap_len = 0
            for prev_s in reversed(current_sentences):
                prev_words = prev_s.split()
                if overlap_len + len(prev_words) <= overlap:
                    overlap_sentences.insert(0, prev_s)
                    overlap_len += len(prev_words)
                else:
                    break
            current_sentences = overlap_sentences
            current_len = sum(len(s.split()) for s in current_sentences)

        current_sentences.append(s)
        current_len += len(words)

    if current_sentences:
        chunks.append(" ".join(current_sentences))

    # If splitting resulted in no chunks, use full content
    if not chunks:
        chunks = [content]

    result = []
    for i, c_text in enumerate(chunks):
        chunk_obj = {
            "chunk_id": f"ict-g{item['grade']}-c{item['chapter']}-p{item['page']}-{i+1}",
            "grade": item["grade"],
            "subject": item["subject"],
            "subject_name_bn": item.get("subject_name_bn", "তথ্য ও যোগাযোগ প্রযুক্তি"),
            "chapter": item["chapter"],
            "chapter_title": item["chapter_title"],
            "topic": item["topic"],
            "page": item["page"],
            "content": c_text
        }
        result.append(chunk_obj)
    return result


def prepare_chunks() -> List[Dict[str, Any]]:
    """Load raw textbook sections and generate chunks with metadata."""
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"Raw data file not found at: {RAW_DATA_PATH}")

    with open(RAW_DATA_PATH, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    all_chunks = []
    for item in raw_data:
        chunks = chunk_topic(item)
        all_chunks.extend(chunks)

    os.makedirs(os.path.dirname(CHUNKS_OUTPUT_PATH), exist_ok=True)
    with open(CHUNKS_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"Successfully created {len(all_chunks)} chunks from {len(raw_data)} NCTB topics.")
    return all_chunks


def build_vector_index(chunks: List[Dict[str, Any]]):
    """Index chunks using FAISS + SentenceTransformers, with fallback to TF-IDF if unavailable."""
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    texts = [f"{c['topic']} - {c['content']}" for c in chunks]

    # Try building with SentenceTransformers + FAISS
    built_with_faiss = False
    try:
        from sentence_transformers import SentenceTransformer
        import faiss
        import numpy as np

        print("Loading local embedding model (paraphrase-multilingual-MiniLM-L12-v2)...")
        embed_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        embeddings = embed_model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)

        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(embeddings.astype(np.float32))

        faiss.write_index(index, FAISS_INDEX_PATH)
        built_with_faiss = True
        print(f"FAISS dense vector index saved to {FAISS_INDEX_PATH} (dim={dim}, count={index.ntotal})")
    except Exception as e:
        print(f"Notice: FAISS or sentence-transformers dense embedding deferral ({e}).")

    # Always generate the universal fallback metadata & lightweight index
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)

    payload = {
        "chunks": chunks,
        "texts": texts,
        "tfidf_vectorizer": vectorizer,
        "tfidf_matrix": tfidf_matrix,
        "has_faiss": built_with_faiss
    }

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(payload, f)
    print(f"Universal retrieval metadata stored successfully at {METADATA_PATH}")


if __name__ == "__main__":
    print("--- Starting NCTB Ingestion & Indexing Pipeline ---")
    chunks = prepare_chunks()
    build_vector_index(chunks)
    print("--- Ingestion Complete! ---")
