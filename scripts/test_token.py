import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.rag.pipeline import RAGPipeline

rag = RAGPipeline()
q = "বঙ্গবন্ধু স্যাটেলাইট-১ কত সালে উৎক্ষেপণ করা হয় এবং বাংলাদেশ কততম দেশ?"
res = rag.process_query(q)
print("Intent:", res.get("intent"))
print("Answer:\n", res.get("answer"))
