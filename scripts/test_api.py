import sys
import httpx

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

res = httpx.get("http://127.0.0.1:8000/api/v1/curriculum/subjects")
print("Curriculum Subjects Status:", res.status_code)
data = res.json()
print("Grades available:", [g["grade_label_bn"] for g in data["curriculum"]])

chat_res = httpx.post(
    "http://127.0.0.1:8000/api/v1/chat/query",
    json={"query": "কম্পিউটার ভাইরাস কী?", "grade": 9, "subject": "ICT"}
)
print("Chat Query Status:", chat_res.status_code)
chat_data = chat_res.json()
print("Session ID:", chat_data["session_id"])
print("Answer Preview:\n", chat_data["answer"][:180])
print("Sources:\n", chat_data["sources"])

# Test history
hist_res = httpx.get(f"http://127.0.0.1:8000/api/v1/chat/history/{chat_data['session_id']}")
print("History Status:", hist_res.status_code, "Turns count:", hist_res.json()["count"])
