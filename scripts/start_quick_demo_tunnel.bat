@echo off
title OIBTC - Online Demo Tunnel (Cloudflare)
color 0a

echo =========================================================================
echo      OIBTC: Online Demo Quick Tunnel (Cloudflare Zero-Trust)
echo =========================================================================
echo.
echo Connecting local OIBTC (http://localhost:3000) to Cloudflare Global Edge...
echo.
echo [!] NOTE: Close this window or press Ctrl+C anytime to IMMEDIATELY destroy
echo           the public tunnel and make the chatbot completely offline again.
echo =========================================================================
echo.

if exist "cloudflared.exe" (
    .\cloudflared.exe tunnel --url http://localhost:3000
) else (
    echo [ERROR] cloudflared.exe not found!
    pause
)
