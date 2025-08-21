#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💊 মেডিসিন চ্যাটবট - অটোমেটিক সেটআপ এবং রান স্ক্রিপ্ট
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def print_banner():
    """প্রিন্ট ব্যানার"""
    print("=" * 60)
    print("💊 মেডিসিন চ্যাটবট - অটোমেটিক সেটআপ")
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

def create_virtual_environment():
    """ভার্চুয়াল এনভায়রনমেন্ট তৈরি করুন"""
    print("\n🔧 ভার্চুয়াল এনভায়রনমেন্ট তৈরি করা হচ্ছে...")
    
    venv_path = Path("venv")
    if venv_path.exists():
    
        print("✅ ভার্চুয়াল এনভায়রনমেন্ট ইতিমধ্যে বিদ্যমান")
        return True
    
    try:
        # Use 'py' command for Windows
        if platform.system() == "Windows":
            subprocess.run(["py", "-m", "venv", "venv"], check=True)
        else:
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ ভার্চুয়াল এনভায়রনমেন্ট সফলভাবে তৈরি হয়েছে")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ভার্চুয়াল এনভায়রনমেন্ট তৈরি করতে সমস্যা: {e}")
        return False

def get_activate_script():
    """অপারেটিং সিস্টেম অনুযায়ী অ্যাক্টিভেট স্ক্রিপ্ট পাথ দিন"""
    if platform.system() == "Windows":
        return "venv\\Scripts\\activate"
    else:
        return "venv/bin/activate"

def install_requirements():
    """প্রয়োজনীয় প্যাকেজ ইনস্টল করুন"""
    print("\n📦 প্রয়োজনীয় প্যাকেজ ইনস্টল করা হচ্ছে...")
    
    try:
        # Use 'py -m pip' for Windows
        if platform.system() == "Windows":
            # Upgrade pip first
            subprocess.run(["py", "-m", "pip", "install", "--upgrade", "pip"], check=True)
            print("✅ pip আপগ্রেড হয়েছে")
            
            # Install requirements
            subprocess.run(["py", "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            print("✅ সব প্রয়োজনীয় প্যাকেজ ইনস্টল হয়েছে")
        else:
            # Get pip path for other systems
            pip_path = "venv/bin/pip"
            subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
            print("✅ pip আপগ্রেড হয়েছে")
            subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
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
            streamlit_path = "venv/bin/streamlit"
            subprocess.run([streamlit_path, "run", "medicine_chatbot.py"])
    except KeyboardInterrupt:
        print("\n👋 চ্যাটবট বন্ধ করা হয়েছে")
    except subprocess.CalledProcessError as e:
        print(f"❌ চ্যাটবট চালু করতে সমস্যা: {e}")

def create_sample_excel():
    """স্যাম্পল Excel ফাইল তৈরি করুন"""
    print("\n📝 স্যাম্পল Excel ফাইল তৈরি করা হচ্ছে...")
    
    try:
        import pandas as pd
        
        # Sample medicine data
        sample_data = {
            'Medicine Name': ['Paracetamol', 'Ibuprofen', 'Omeprazole', 'Cetirizine', 'Metformin'],
            'Generic Name': ['Acetaminophen', 'Ibuprofen', 'Omeprazole', 'Cetirizine', 'Metformin'],
            'Uses': ['জ্বর, ব্যথা', 'ব্যথা, প্রদাহ', 'পেটের আলসার', 'অ্যালার্জি', 'ডায়াবেটিস'],
            'Side Effects': ['মাথাব্যথা, বমি', 'পেটে ব্যথা', 'মাথাব্যথা', 'ঘুম', 'বমি'],
            'Dosage': ['500-1000mg', '200-400mg', '20mg', '10mg', '500mg'],
            'Price (৳)': [5, 8, 15, 12, 20]
        }
        
        df = pd.DataFrame(sample_data)
        df.to_excel('medicine_data.xlsx', index=False)
        print("✅ স্যাম্পল Excel ফাইল তৈরি হয়েছে")
        return True
    except Exception as e:
        print(f"❌ স্যাম্পল ফাইল তৈরি করতে সমস্যা: {e}")
        return False

def main():
    """মেইন ফাংশন"""
    print_banner()
    
    # Check Python
    if not check_python():
        input("\nEnter চাপুন বন্ধ করতে...")
        return
    
    # Create virtual environment
    if not create_virtual_environment():
        input("\nEnter চাপুন বন্ধ করতে...")
        return
    
    # Install requirements
    if not install_requirements():
        input("\nEnter চাপুন বন্ধ করতে...")
        return
    
    # Check Excel file
    if not check_excel_file():
        print("\n💡 স্যাম্পল Excel ফাইল তৈরি করতে চান? (y/n): ", end="")
        choice = input().lower().strip()
        if choice in ['y', 'yes', 'হ্যাঁ']:
            if create_sample_excel():
                print("✅ স্যাম্পল ডেটা দিয়ে চ্যাটবট চালু করা যাবে")
            else:
                print("❌ স্যাম্পল ফাইল তৈরি করতে পারেনি")
                input("\nEnter চাপুন বন্ধ করতে...")
                return
        else:
            print("❌ Excel ফাইল ছাড়া চ্যাটবট চালানো যাবে না")
            input("\nEnter চাপুন বন্ধ করতে...")
            return
    
    # Run chatbot
    run_chatbot()

if __name__ == "__main__":
    main()
