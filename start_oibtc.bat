@echo off
title OIBTC - Offline Intelligent Bangla Tutoring Chatbot
color 0b

echo =========================================================================
echo      OIBTC: Offline Intelligent Bangla Tutoring Chatbot (WUB CSE)
echo =========================================================================
echo.
echo [1/3] Checking Offline Database and Vector Stores...
python scripts/build_faiss.py

echo.
echo [2/3] Starting FastAPI Backend on 0.0.0.0:8000 (Classroom Hotspot Ready)...
start "OIBTC Backend Server" cmd /k "python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000"

timeout /t 2 /nobreak >nul

echo.
echo [3/3] Starting React Frontend on 0.0.0.0:3000...
start "OIBTC Frontend Client" cmd /k "npm --prefix frontend run dev"

timeout /t 3 /nobreak >nul

echo.
echo =========================================================================
echo [SUCCESS] OIBTC is now running 100%% offline!
echo Local Browser URL: http://localhost:3000
echo Classroom Hotspot URL: http://192.168.0.134:3000
echo =========================================================================
echo Opening browser...
start http://localhost:3000
