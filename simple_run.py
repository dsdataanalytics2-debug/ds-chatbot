#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💊 মেডিসিন চ্যাটবট - সরল রান স্ক্রিপ্ট
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """প্রিন্ট ব্যানার"""
    print("=" * 60)
    print("💊 মেডিসিন চ্যাটবট - সরল রান")
    print("=" * 60)
    print()

def check_python():
    """Python ভার্সন চেক করুন"""
    print("🐍 Python ভার্সন চেক করা হচ্ছে...")
    try:
        version = sys.version_info
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} পাওয়া গেছে")
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            print("❌ Python 3.7+ প্রয়োজন!")
            return False
        return True
    except Exception as e:
        print(f"❌ Python চেক করতে সমস্যা: {e}")
        return False

def install_requirements():
    """প্রয়োজনীয় প্যাকেজ ইনস্টল করুন"""
    print("\n📦 প্রয়োজনীয় প্যাকেজ ইনস্টল করা হচ্ছে...")
    
    try:
        # Use 'py -m pip' for Windows
        if platform.system() == "Windows":
            # Install requirements directly
            subprocess.run(["py", "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            print("✅ সব প্রয়োজনীয় প্যাকেজ ইনস্টল হয়েছে")
        else:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            print("✅ সব প্রয়োজনীয় প্যাকেজ ইনস্টল হয়েছে")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ প্যাকেজ ইনস্টল করতে সমস্যা: {e}")
        return False

def check_excel_file():
    """Excel ফাইল চেক করুন"""
    print("\n📊 Excel ফাইল চেক করা হচ্ছে...")
    
    excel_file = Path("medicine_data.xlsx")
    if excel_file.exists():
        print(f"✅ {excel_file} পাওয়া গেছে")
        return True
    else:
        print(f"❌ {excel_file} পাওয়া যায়নি!")
        print("💡 অনুগ্রহ করে আপনার Excel ফাইলটি প্রজেক্ট ফোল্ডারে রাখুন")
        return False

def run_chatbot():
    """চ্যাটবট চালু করুন"""
    print("\n🚀 চ্যাটবট চালু হচ্ছে...")
    print("🌐 ব্রাউজারে http://localhost:8501 এ যান")
    print("🛑 বন্ধ করতে Ctrl+C চাপুন")
    print("-" * 60)
    
    try:
        # Use 'py -m streamlit' for Windows
        if platform.system() == "Windows":
            subprocess.run(["py", "-m", "streamlit", "run", "medicine_chatbot.py"])
        else:
            subprocess.run([sys.executable, "-m", "streamlit", "run", "medicine_chatbot.py"])
    except KeyboardInterrupt:
        print("\n👋 চ্যাটবট বন্ধ করা হয়েছে")
    except subprocess.CalledProcessError as e:
        print(f"❌ চ্যাটবট চালু করতে সমস্যা: {e}")

def main():
    """মেইন ফাংশন"""
    print_banner()
    
    # Check Python
    if not check_python():
        input("\nEnter চাপুন বন্ধ করতে...")
        return
    
    # Install requirements
    if not install_requirements():
        input("\nEnter চাপুন বন্ধ করতে...")
        return
    
    # Check Excel file
    if not check_excel_file():
        print("❌ Excel ফাইল ছাড়া চ্যাটবট চালানো যাবে না")
        input("\nEnter চাপুন বন্ধ করতে...")
        return
    
    # Run chatbot
    run_chatbot()

if __name__ == "__main__":
    main()
