#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 উন্নত AI মেডিসিন চ্যাটবট রান স্ক্রিপ্ট
ChatGPT/Cursor AI স্টাইলে বিস্তারিত উত্তর প্রদান করে
"""

import os
import sys
import subprocess
import platform
import time
from pathlib import Path

def print_banner():
    """প্রিন্ট সুন্দর ব্যানার"""
    print("=" * 80)
    print("🤖 উন্নত AI মেডিসিন চ্যাটবট")
    print("ChatGPT/Cursor AI স্টাইলে বিস্তারিত উত্তর প্রদান করে")
    print("=" * 80)
    print()

def print_features():
    """প্রিন্ট বৈশিষ্ট্যসমূহ"""
    print("✨ **মূল বৈশিষ্ট্যসমূহ:**")
    print("🔍 স্মার্ট অনুসন্ধান - মেডিসিনের নাম, জেনেরিক নাম, ব্যবহারের কারণ অনুসন্ধান")
    print("📋 বিস্তারিত তথ্য - সম্পূর্ণ মেডিসিন তথ্য সুন্দরভাবে প্রদর্শন")
    print("💡 সহায়ক পরামর্শ - স্বাস্থ্য সম্পর্কিত সাধারণ পরামর্শ")
    print("🎨 সুন্দর UI - আধুনিক এবং ব্যবহারকারী-বান্ধব ইন্টারফেস")
    print("📊 পরিসংখ্যান - চ্যাট ইতিহাস এবং ব্যবহার পরিসংখ্যান")
    print("🔄 চ্যাট ইতিহাস - পূর্ববর্তী কথোপকথন স্মরণ রাখা")
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
    
    # Check if requirements file exists
    requirements_file = "requirements.txt"
    if not Path(requirements_file).exists():
        print(f"❌ {requirements_file} ফাইল পাওয়া যায়নি!")
        print("💡 অনুগ্রহ করে requirements.txt ফাইলটি প্রজেক্ট ফোল্ডারে রাখুন")
        return False
    
    try:
        # Use appropriate pip command for the platform
        if platform.system() == "Windows":
            cmd = ["py", "-m", "pip", "install", "-r", requirements_file]
        else:
            cmd = [sys.executable, "-m", "pip", "install", "-r", requirements_file]
        
        print("🔄 প্যাকেজ ইনস্টল হচ্ছে... (এটি কিছু সময় নিতে পারে)")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ সব প্রয়োজনীয় প্যাকেজ ইনস্টল হয়েছে")
            return True
        else:
            print(f"❌ প্যাকেজ ইনস্টল করতে সমস্যা:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ প্যাকেজ ইনস্টল করতে সমস্যা: {e}")
        return False

def check_excel_file():
    """Excel ফাইল চেক করুন"""
    print("\n📊 Excel ফাইল চেক করা হচ্ছে...")
    
    excel_file = Path("medicine_data.xlsx")
    if excel_file.exists():
        print(f"✅ {excel_file} পাওয়া গেছে")
        
        # Check file size
        file_size = excel_file.stat().st_size
        if file_size > 0:
            print(f"📏 ফাইল সাইজ: {file_size / 1024:.1f} KB")
            return True
        else:
            print("❌ ফাইলটি খালি!")
            return False
    else:
        print(f"❌ {excel_file} পাওয়া যায়নি!")
        print("💡 অনুগ্রহ করে আপনার Excel ফাইলটি প্রজেক্ট ফোল্ডারে রাখুন")
        return False

def check_chatbot_file():
    """চ্যাটবট ফাইল চেক করুন"""
    print("\n🤖 চ্যাটবট ফাইল চেক করা হচ্ছে...")
    
    chatbot_file = Path("advanced_ai_chatbot.py")
    if chatbot_file.exists():
        print(f"✅ {chatbot_file} পাওয়া গেছে")
        return True
    else:
        print(f"❌ {chatbot_file} পাওয়া যায়নি!")
        return False

def run_chatbot():
    """চ্যাটবট চালু করুন"""
    print("\n🚀 উন্নত AI চ্যাটবট চালু হচ্ছে...")
    print("🌐 ব্রাউজারে http://localhost:8501 এ যান")
    print("🛑 বন্ধ করতে Ctrl+C চাপুন")
    print("📱 মোবাইল থেকে http://[আপনার-IP]:8501 এ যেতে পারেন")
    print("-" * 80)
    
    try:
        # Use appropriate streamlit command for the platform
        if platform.system() == "Windows":
            cmd = ["py", "-m", "streamlit", "run", "advanced_ai_chatbot.py", "--server.port", "8501"]
        else:
            cmd = [sys.executable, "-m", "streamlit", "run", "advanced_ai_chatbot.py", "--server.port", "8501"]
        
        print("🔄 চ্যাটবট লোড হচ্ছে...")
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 চ্যাটবট বন্ধ করা হয়েছে")
    except subprocess.CalledProcessError as e:
        print(f"❌ চ্যাটবট চালু করতে সমস্যা: {e}")
    except FileNotFoundError:
        print("❌ Streamlit পাওয়া যায়নি! অনুগ্রহ করে ইনস্টল করুন: pip install streamlit")

def show_usage_tips():
    """ব্যবহারের টিপস দেখান"""
    print("\n💡 **ব্যবহারের টিপস:**")
    print("🔸 মেডিসিনের নাম লিখুন (যেমন: Paracetamol, Aspirin)")
    print("🔸 জেনেরিক নাম দিয়ে অনুসন্ধান করুন")
    print("🔸 ব্যবহারের কারণ লিখুন (যেমন: জ্বর, ব্যথা)")
    print("🔸 সাধারণ স্বাস্থ্য পরামর্শ চাইতে পারেন")
    print("🔸 উদাহরণ প্রশ্ন বোতাম ব্যবহার করুন")
    print()

def main():
    """মেইন ফাংশন"""
    print_banner()
    print_features()
    
    # Check Python
    if not check_python():
        input("\nEnter চাপুন বন্ধ করতে...")
        return
    
    # Check chatbot file
    if not check_chatbot_file():
        print("❌ চ্যাটবট ফাইল ছাড়া চালানো যাবে না")
        input("\nEnter চাপুন বন্ধ করতে...")
        return
    
    # Install requirements
    if not install_requirements():
        print("❌ প্রয়োজনীয় প্যাকেজ ইনস্টল না হলে চ্যাটবট চালানো যাবে না")
        input("\nEnter চাপুন বন্ধ করতে...")
        return
    
    # Check Excel file
    if not check_excel_file():
        print("❌ Excel ফাইল ছাড়া চ্যাটবট চালানো যাবে না")
        input("\nEnter চাপুন বন্ধ করতে...")
        return
    
    # Show usage tips
    show_usage_tips()
    
    # Run chatbot
    run_chatbot()

if __name__ == "__main__":
    main()
