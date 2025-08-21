@echo off
echo 💊 মেডিসিন চ্যাটবট চালু হচ্ছে...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python ইনস্টল নেই! প্রথমে Python ইনস্টল করুন।
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 🔧 ভার্চুয়াল এনভায়রনমেন্ট তৈরি হচ্ছে...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 ভার্চুয়াল এনভায়রনমেন্ট অ্যাক্টিভেট হচ্ছে...
call venv\Scripts\activate

REM Install requirements
echo 📦 প্রয়োজনীয় প্যাকেজ ইনস্টল হচ্ছে...
pip install -r requirements.txt

REM Run the chatbot
echo 🚀 চ্যাটবট চালু হচ্ছে...
echo 🌐 ব্রাউজারে http://localhost:8501 এ যান
echo.
streamlit run medicine_chatbot.py

pause
