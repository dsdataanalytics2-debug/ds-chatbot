#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💊 উন্নত মেডিসিন চ্যাটবট রান স্ক্রিপ্ট
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("=" * 60)
    print("💊 উন্নত মেডিসিন চ্যাটবট")
    print("=" * 60)
    print()
    
    # Check if medicine_data.xlsx exists
    if not Path("medicine_data.xlsx").exists():
        print("❌ medicine_data.xlsx ফাইল পাওয়া যায়নি!")
        print("💡 অনুগ্রহ করে আপনার Excel ফাইলটি প্রজেক্ট ফোল্ডারে রাখুন")
        input("Enter চাপুন বন্ধ করতে...")
        return
    
    # Check if virtual environment exists
    venv_path = Path("venv")
    if not venv_path.exists():
        print("🔧 ভার্চুয়াল এনভায়রনমেন্ট তৈরি হচ্ছে...")
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            print("✅ ভার্চুয়াল এনভায়রনমেন্ট তৈরি হয়েছে")
        except subprocess.CalledProcessError:
            print("❌ ভার্চুয়াল এনভায়রনমেন্ট তৈরি করতে পারেনি")
            input("Enter চাপুন বন্ধ করতে...")
            return
    
    # Get streamlit path
    if os.name == 'nt':  # Windows
        streamlit_path = "venv\\Scripts\\streamlit"
    else:  # Unix/Linux/Mac
        streamlit_path = "venv/bin/streamlit"
    
    # Check if streamlit is installed
    if not Path(streamlit_path).exists():
        print("📦 প্রয়োজনীয় প্যাকেজ ইনস্টল হচ্ছে...")
        try:
            pip_path = streamlit_path.replace("streamlit", "pip")
            subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
            print("✅ প্যাকেজ ইনস্টল হয়েছে")
        except subprocess.CalledProcessError:
            print("❌ প্যাকেজ ইনস্টল করতে পারেনি")
            input("Enter চাপুন বন্ধ করতে...")
            return
    
    # Run the chatbot
    print("🚀 চ্যাটবট চালু হচ্ছে...")
    print("🌐 ব্রাউজারে http://localhost:8501 এ যান")
    print("🛑 বন্ধ করতে Ctrl+C চাপুন")
    print("-" * 60)
    
    try:
        subprocess.run([streamlit_path, "run", "medicine_chatbot_advanced.py"])
    except KeyboardInterrupt:
        print("\n👋 চ্যাটবট বন্ধ করা হয়েছে")
    except subprocess.CalledProcessError as e:
        print(f"❌ চ্যাটবট চালু করতে সমস্যা: {e}")
        input("Enter চাপুন বন্ধ করতে...")

if __name__ == "__main__":
    main()
