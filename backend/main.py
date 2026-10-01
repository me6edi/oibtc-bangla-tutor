"""
FastAPI Backend Application for OIBTC
Provides offline REST API for student tutoring, curriculum discovery, and session history.
"""

import os
import socket
import sys
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.database.sqlite import init_db, create_session, add_message, get_history
from backend.rag.pipeline import get_rag_pipeline

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Initialize database
init_db()

app = FastAPI(
    title="OIBTC Backend API",
    description="Offline Intelligent Bangla Tutoring Chatbot for Secondary Education in Bangladesh",
    version="1.0.0"
)

# Enable CORS for local network and Classroom Hotspot Mode
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_local_ip() -> str:
    """Retrieve local LAN/Hotspot IP address for Classroom Mode."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


# Request / Response Schemas
class SessionCreateRequest(BaseModel):
    grade: int = 9
    subject: str = "ICT"
    subject_bn: str = "তথ্য ও যোগাযোগ প্রযুক্তি"


class ChatQueryRequest(BaseModel):
    session_id: Optional[str] = None
    query: str
    grade: int = 9
    subject: str = "ICT"


class ChatQueryResponse(BaseModel):
    session_id: str
    query: str
    answer: str
    sources: List[dict]
    suggested_followups: List[str]
    is_out_of_curriculum: bool
    intent: Optional[str] = "GENERAL"
    intent_label: Optional[str] = "সাধারণ প্রশ্ন"


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "mode": "offline",
        "system": "OIBTC",
        "local_ip": get_local_ip()
    }


@app.get("/api/v1/status")
def system_status():
    rag = get_rag_pipeline()
    return {
        "offline_ready": True,
        "faiss_loaded": rag.retriever.faiss_index is not None,
        "ollama_connected": rag.llm.is_ollama_available,
        "total_curriculum_chunks": len(rag.retriever.chunks),
        "local_ip": get_local_ip(),
        "classroom_mode_url": f"http://{get_local_ip()}:3000"
    }


@app.get("/api/v1/curriculum/subjects")
def get_curriculum_subjects():
    return {
        "curriculum": [
            {
                "grade": 9,
                "grade_label_bn": "৯ম শ্রেণি",
                "subjects": [
                    {
                        "code": "ICT",
                        "name_bn": "তথ্য ও যোগাযোগ প্রযুক্তি",
                        "status": "active_pilot",
                        "chapters": [
                            {
                                "chapter": 1,
                                "title": "তথ্য ও যোগাযোগ প্রযুক্তি এবং আমাদের বাংলাদেশ",
                                "topics": [
                                    "একুশ শতক এবং আইসিটি",
                                    "আইসিটি বিকাশে উল্লেখযোগ্য ব্যক্তিত্ব",
                                    "ই-লার্নিং ও বাংলাদেশ",
                                    "ই-গভর্ন্যান্স ও ই-সার্ভিস",
                                    "ডিজিটাল বাংলাদেশ"
                                ]
                            },
                            {
                                "chapter": 2,
                                "title": "কম্পিউটার ও কম্পিউটার ব্যবহারকারীর নিরাপত্তা",
                                "topics": [
                                    "কম্পিউটারের সঠিক রক্ষণাবেক্ষণ",
                                    "সফটওয়্যার ইনস্টলেশন ও আনইনস্টলেশন",
                                    "পাসওয়ার্ড ও নিরাপত্তা",
                                    "কম্পিউটার ভাইরাস ও অ্যান্টিভাইরাস",
                                    "সাধারণ ট্রাবলশুটিং"
                                ]
                            }
                        ]
                    },
                    {
                        "code": "SCIENCE",
                        "name_bn": "সাধারণ বিজ্ঞান",
                        "status": "upcoming",
                        "chapters": []
                    },
                    {
                        "code": "MATH",
                        "name_bn": "সাধারণ গণিত",
                        "status": "upcoming",
                        "chapters": []
                    }
                ]
            }
        ]
    }


@app.post("/api/v1/chat/session")
def start_session(req: SessionCreateRequest):
    session_id = create_session(grade=req.grade, subject=req.subject, subject_bn=req.subject_bn)
    return {"session_id": session_id}


@app.post("/api/v1/chat/query", response_model=ChatQueryResponse)
def handle_chat_query(req: ChatQueryRequest):
    session_id = req.session_id
    if not session_id:
        session_id = create_session(grade=req.grade, subject=req.subject)

    # Retrieve recent conversation history for contextual follow-up
    history = get_history(session_id) if session_id else []
    rag = get_rag_pipeline()
    result = rag.process_query(query=req.query, grade=req.grade, subject=req.subject, history=history)

    # Save to SQLite local history
    add_message(
        session_id=session_id,
        sender="student",
        query_text=req.query,
        response_text=result["answer"],
        sources=result["sources"]
    )

    return ChatQueryResponse(
        session_id=session_id,
        query=req.query,
        answer=result["answer"],
        sources=result["sources"],
        suggested_followups=result["suggested_followups"],
        is_out_of_curriculum=result["is_out_of_curriculum"],
        intent=result.get("intent", "GENERAL"),
        intent_label=result.get("intent_label", "সাধারণ প্রশ্ন")
    )


@app.get("/api/v1/chat/history/{session_id}")
def get_chat_history(session_id: str):
    history = get_history(session_id)
    return {
        "session_id": session_id,
        "count": len(history),
        "messages": history
    }


# Mount static frontend build for unified production deployment
FRONTEND_DIST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")
if os.path.exists(FRONTEND_DIST):
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    print(f"Starting OIBTC backend server on 0.0.0.0:8000 (Classroom IP: {get_local_ip()})...")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=False)
