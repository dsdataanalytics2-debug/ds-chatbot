#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💊 Professional মেডিসিন চ্যাটবট রান স্ক্রিপ্ট
Professional এবং Organized ভার্সন চালানোর জন্য
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """প্রিন্ট ব্যানার"""
    print("=" * 70)
    print("💊 PROFESSIONAL মেডিসিন চ্যাটবট")
    print("🎨 Completely Reorganized UI with Better UX")
    print("=" * 70)
    print()

def check_requirements():
    """প্রয়োজনীয় প্যাকেজ চেক করুন"""
    print("📦 প্রয়োজনীয় প্যাকেজ চেক করা হচ্ছে...")
    
    required_packages = [
        'streamlit',
        'pandas',
        'scikit-learn',
        'nltk',
        'openpyxl'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} পাওয়া গেছে")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} পাওয়া যায়নি")
    
    if missing_packages:
        print(f"\n❌ অনুপস্থিত প্যাকেজ: {', '.join(missing_packages)}")
        print("💡 ইনস্টল করতে চালান: pip install " + " ".join(missing_packages))
        return False
    
    print("✅ সব প্রয়োজনীয় প্যাকেজ পাওয়া গেছে")
    return True

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

def run_professional_chatbot():
    """Professional চ্যাটবট চালু করুন"""
    print("\n🚀 Professional মেডিসিন চ্যাটবট চালু হচ্ছে...")
    print("🌐 ব্রাউজারে http://localhost:8501 এ যান")
    print("🎨 নতুন Professional UI এবং উন্নত ফিচার উপভোগ করুন!")
    print("🛑 বন্ধ করতে Ctrl+C চাপুন")
    print("-" * 70)
    
    try:
        # Use appropriate python command for the platform
        if platform.system() == "Windows":
            subprocess.run(["python", "-m", "streamlit", "run", "professional_medicine_chatbot.py"])
        else:
            subprocess.run(["python3", "-m", "streamlit", "run", "professional_medicine_chatbot.py"])
    except KeyboardInterrupt:
        print("\n👋 চ্যাটবট বন্ধ করা হয়েছে")
    except subprocess.CalledProcessError as e:
        print(f"❌ চ্যাটবট চালু করতে সমস্যা: {e}")
        print("💡 সমাধান: pip install streamlit")
    except FileNotFoundError:
        print("❌ Python বা Streamlit পাওয়া যায়নি")
        print("💡 Python এবং Streamlit ইনস্টল করুন")

def show_features():
    """নতুন Professional ফিচারের তালিকা দেখান"""
    print("\n🎯 Professional UI ফিচারসমূহ:")
    print("=" * 50)
    print("🎨 Completely Reorganized Layout")
    print("📱 Professional Spacing and Organization")
    print("🔍 Better Search Interface Organization")
    print("📁 Improved File Upload Layout")
    print("📊 Enhanced Data View Interface")
    print("💫 Professional Color Scheme")
    print("🎭 Modern Design Elements")
    print("⚡ Better User Experience")
    print("📖 Professional Help System")
    print("=" * 50)

def main():
    """মেইন ফাংশন"""
    print_banner()
    show_features()
    
    # Check requirements
    if not check_requirements():
        input("\nEnter চাপুন বন্ধ করতে...")
        return
    
    # Check Excel file
    if not check_excel_file():
        input("\nEnter চাপুন বন্ধ করতে...")
        return
    
    # Show final message before starting
    print("\n🎉 সবকিছু প্রস্তুত! Professional চ্যাটবট চালু করা হচ্ছে...")
    print("💡 টিপস: সাইডবার থেকে বিভিন্ন পেজ এক্সপ্লোর করুন")
    
    # Run the professional chatbot
    run_professional_chatbot()

if __name__ == "__main__":
    main()
