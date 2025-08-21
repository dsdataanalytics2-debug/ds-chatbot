#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ChatGPT স্টাইল মেডিসিন চ্যাটবট চালানোর স্ক্রিপ্ট
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import streamlit
        import pandas
        import numpy
        print("✅ সব প্রয়োজনীয় প্যাকেজ ইনস্টল আছে")
        return True
    except ImportError as e:
        print(f"❌ প্যাকেজ ইনস্টল নেই: {e}")
        return False

def install_requirements():
    """Install required packages"""
    print("📦 প্রয়োজনীয় প্যাকেজ ইনস্টল করা হচ্ছে...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_chatgpt_style.txt"])
        print("✅ প্যাকেজ ইনস্টল সম্পন্ন")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ প্যাকেজ ইনস্টল করতে সমস্যা: {e}")
        return False

def run_chatbot():
    """Run the ChatGPT-style chatbot"""
    print("🤖 ChatGPT স্টাইল মেডিসিন চ্যাটবট চালু হচ্ছে...")
    print("🌐 ব্রাউজারে http://localhost:8501 এ যান")
    print("🛑 বন্ধ করতে Ctrl+C চাপুন")
    print("-" * 60)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "chatgpt_style_medicine_chatbot.py"])
    except KeyboardInterrupt:
        print("\n👋 চ্যাটবট বন্ধ করা হয়েছে")
    except Exception as e:
        print(f"❌ চ্যাটবট চালু করতে সমস্যা: {e}")

def main():
    """Main function"""
    print("=" * 60)
    print("🤖 ChatGPT স্টাইল মেডিসিন চ্যাটবট")
    print("=" * 60)
    print()
    
    # Check if chatbot file exists
    if not Path("chatgpt_style_medicine_chatbot.py").exists():
        print("❌ chatgpt_style_medicine_chatbot.py ফাইল পাওয়া যায়নি!")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("\n💡 প্রয়োজনীয় প্যাকেজ ইনস্টল করতে চান? (y/n): ", end="")
        choice = input().lower().strip()
        if choice in ['y', 'yes', 'হ্যাঁ']:
            if not install_requirements():
                return
        else:
            print("❌ প্যাকেজ ছাড়া চ্যাটবট চালানো যাবে না")
            return
    
    # Run chatbot
    run_chatbot()

if __name__ == "__main__":
    main()
