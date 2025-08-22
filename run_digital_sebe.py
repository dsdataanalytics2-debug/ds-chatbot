#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏥 DIGITAL SEBE CHATBOT Runner
এই ফাইলটি চালিয়ে আপনার চ্যাটবট শুরু করুন
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 প্রয়োজনীয় প্যাকেজ ইনস্টল করা হচ্ছে...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_digital_sebe.txt"])
        print("✅ সব প্যাকেজ সফলভাবে ইনস্টল হয়েছে!")
    except subprocess.CalledProcessError:
        print("❌ প্যাকেজ ইনস্টল করতে সমস্যা হয়েছে")
        return False
    return True

def run_chatbot():
    """Run the chatbot"""
    print("🚀 DIGITAL SEBE CHATBOT শুরু করা হচ্ছে...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "digital_sebe_chatbot.py", "--server.port", "8501"])
    except KeyboardInterrupt:
        print("\n👋 চ্যাটবট বন্ধ করা হয়েছে")
    except Exception as e:
        print(f"❌ চ্যাটবট চালাতে সমস্যা: {e}")

def main():
    print("=" * 60)
    print("🏥 DIGITAL SEBE CHATBOT")
    print("=" * 60)
    
    # Check if requirements file exists
    if not os.path.exists("requirements_digital_sebe.txt"):
        print("❌ requirements_digital_sebe.txt ফাইল পাওয়া যায়নি")
        return
    
    # Check if chatbot file exists
    if not os.path.exists("digital_sebe_chatbot.py"):
        print("❌ digital_sebe_chatbot.py ফাইল পাওয়া যায়নি")
        return
    
    # Install requirements
    if install_requirements():
        # Run chatbot
        run_chatbot()
    else:
        print("❌ চ্যাটবট চালানো যায়নি")

if __name__ == "__main__":
    main()
