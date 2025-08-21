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
    print("PDF, Word, API সমর্থন সহ")
    print("=" * 60)
    print()
    
    # Check if medicine_data.xlsx exists
    if not Path("medicine_data.xlsx").exists():
        print("❌ medicine_data.xlsx ফাইল পাওয়া যায়নি!")
        print("💡 অনুগ্রহ করে আপনার Excel ফাইলটি প্রজেক্ট ফোল্ডারে রাখুন")
        input("Enter চাপুন বন্ধ করতে...")
        return
    
    # Install advanced requirements
    print("📦 উন্নত ফিচারের জন্য প্রয়োজনীয় প্যাকেজ ইনস্টল হচ্ছে...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_advanced.txt"], check=True)
        print("✅ সব প্যাকেজ ইনস্টল হয়েছে")
    except subprocess.CalledProcessError:
        print("❌ প্যাকেজ ইনস্টল করতে পারেনি")
        input("Enter চাপুন বন্ধ করতে...")
        return
    
    # Run the advanced chatbot
    print("🚀 উন্নত চ্যাটবট চালু হচ্ছে...")
    print("🌐 ব্রাউজারে http://localhost:8501 এ যান")
    print("🛑 বন্ধ করতে Ctrl+C চাপুন")
    print("-" * 60)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "advanced_medicine_chatbot.py"])
    except KeyboardInterrupt:
        print("\n👋 চ্যাটবট বন্ধ করা হয়েছে")
    except subprocess.CalledProcessError as e:
        print(f"❌ চ্যাটবট চালু করতে সমস্যা: {e}")
        input("Enter চাপুন বন্ধ করতে...")

if __name__ == "__main__":
    main()
