"""
Build FAISS Vector Index for NCTB ICT Ch 1 & 2
Ensures 100% offline generation of data/vectorstore/ict_ch1_ch2.faiss
"""

import json
import os
import sys
import numpy as np
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CHUNKS_PATH = os.path.join("data", "nctb_raw", "ict_chunks.json")
VECTORSTORE_DIR = os.path.join("data", "vectorstore")
FAISS_PATH = os.path.join(VECTORSTORE_DIR, "ict_ch1_ch2.faiss")


def build_faiss_index():
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    if not os.path.exists(CHUNKS_PATH):
        raise FileNotFoundError(f"Chunks file missing: {CHUNKS_PATH}")

    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    corpus = [f"{c['topic']} {c['chapter_title']} {c['content']}" for c in chunks]
    print(f"Building FAISS vector index for {len(chunks)} NCTB chunks...")

    dim = 512
    # Dense vectorization using n-gram TF-IDF projection
    vectorizer = TfidfVectorizer(max_features=dim, analyzer="char_wb", ngram_range=(3, 5))
    X = vectorizer.fit_transform(corpus).toarray().astype(np.float32)

    # Pad if dimension < 512
    if X.shape[1] < dim:
        padding = np.zeros((X.shape[0], dim - X.shape[1]), dtype=np.float32)
        X = np.hstack([X, padding])

    # L2 normalize for cosine similarity via inner product
    faiss.normalize_L2(X)

    # Create Inner Product Flat Index
    index = faiss.IndexFlatIP(dim)
    index.add(X)

    faiss.write_index(index, FAISS_PATH)
    print(f"Success: FAISS index saved to {FAISS_PATH} (dim={dim}, total_vectors={index.ntotal})")


if __name__ == "__main__":
    build_faiss_index()
