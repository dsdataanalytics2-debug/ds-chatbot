@echo off
chcp 65001 >nul
title DIGITAL SEBE CHATBOT

echo.
echo ============================================================
echo                    🏥 DIGITAL SEBE CHATBOT
echo ============================================================
echo.

echo 📦 প্রয়োজনীয় প্যাকেজ ইনস্টল করা হচ্ছে...
pip install -r requirements_digital_sebe.txt

if %errorlevel% neq 0 (
    echo ❌ প্যাকেজ ইনস্টল করতে সমস্যা হয়েছে
    pause
    exit /b 1
)

echo ✅ সব প্যাকেজ সফলভাবে ইনস্টল হয়েছে!
echo.
echo 🚀 চ্যাটবট শুরু করা হচ্ছে...
echo 🌐 ব্রাউজারে http://localhost:8501 এ যান
echo.
echo চ্যাটবট বন্ধ করতে Ctrl+C চাপুন
echo.

streamlit run digital_sebe_chatbot.py --server.port 8501

pause
