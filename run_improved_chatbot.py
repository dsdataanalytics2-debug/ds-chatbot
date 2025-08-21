#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💊 উন্নত মেডিসিন চ্যাটবট রান স্ক্রিপ্ট
Improved এবং Organized ভার্সন চালানোর জন্য
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """প্রিন্ট ব্যানার"""
    print("=" * 70)
    print("💊 উন্নত এবং সংগঠিত মেডিসিন চ্যাটবট")
    print("🎨 Modern UI Design with Better User Experience")
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
        
        # Create sample data if user wants
        create_sample = input("📝 স্যাম্পল Excel ফাইল তৈরি করতে চান? (y/n): ").lower().strip()
        if create_sample in ['y', 'yes', 'হ্যাঁ']:
            return create_sample_excel()
        return False

def create_sample_excel():
    """স্যাম্পল Excel ফাইল তৈরি করুন"""
    print("\n📝 স্যাম্পল Excel ফাইল তৈরি করা হচ্ছে...")
    
    try:
        import pandas as pd
        
        # Sample medicine data with Bengali content
        sample_data = {
            'Medicine Name': [
                'Paracetamol', 'Ibuprofen', 'Omeprazole', 'Cetirizine', 'Metformin',
                'Aspirin', 'Amoxicillin', 'Losartan', 'Atorvastatin', 'Ranitidine'
            ],
            'Generic Name': [
                'Acetaminophen', 'Ibuprofen', 'Omeprazole', 'Cetirizine', 'Metformin',
                'Acetylsalicylic acid', 'Amoxicillin', 'Losartan', 'Atorvastatin', 'Ranitidine'
            ],
            'Uses (ব্যবহার)': [
                'জ্বর, ব্যথা নিরাময়', 'ব্যথা, প্রদাহ কমানো', 'পেটের আলসার চিকিৎসা', 
                'অ্যালার্জি প্রতিরোধ', 'ডায়াবেটিস নিয়ন্ত্রণ', 'হার্ট অ্যাটাক প্রতিরোধ',
                'ব্যাকটেরিয়া সংক্রমণ', 'উচ্চ রক্তচাপ', 'কোলেস্টেরল কমানো', 'পেটের অ্যাসিড কমানো'
            ],
            'Side Effects (পার্শ্বপ্রতিক্রিয়া)': [
                'বমি, মাথাব্যথা', 'পেটে ব্যথা, গ্যাস', 'মাথাব্যথা, চক্কর', 'ঘুম, মুখ শুকানো',
                'বমি, ডায়রিয়া', 'পেট জ্বালা, রক্তপাত', 'ডায়রিয়া, অ্যালার্জি', 'চক্কর, কাশি',
                'পেশী ব্যথা, লিভার সমস্যা', 'মাথাব্যথা, কোষ্ঠকাঠিন্য'
            ],
            'Dosage (ডোজ)': [
                '500-1000mg প্রতি ৬ ঘণ্টায়', '200-400mg প্রতি ৮ ঘণ্টায়', '20mg দিনে একবার',
                '10mg দিনে একবার', '500mg দিনে দুইবার', '75-100mg দিনে একবার',
                '250-500mg প্রতি ৮ ঘণ্টায়', '50mg দিনে একবার', '10-80mg দিনে একবার',
                '150mg দিনে দুইবার'
            ],
            'Price (৳)': [5, 8, 15, 12, 20, 3, 25, 18, 35, 10],
            'Company': [
                'Square', 'Beximco', 'Incepta', 'ACI', 'Renata', 'Opsonin', 'Drug International',
                'Healthcare', 'Popular', 'Eskayef'
            ]
        }
        
        df = pd.DataFrame(sample_data)
        df.to_excel('medicine_data.xlsx', index=False)
        print("✅ স্যাম্পল Excel ফাইল তৈরি হয়েছে")
        print("📊 ১০টি ওষুধের তথ্য যোগ করা হয়েছে")
        return True
    except Exception as e:
        print(f"❌ স্যাম্পল ফাইল তৈরি করতে সমস্যা: {e}")
        return False

def run_improved_chatbot():
    """উন্নত চ্যাটবট চালু করুন"""
    print("\n🚀 উন্নত মেডিসিন চ্যাটবট চালু হচ্ছে...")
    print("🌐 ব্রাউজারে http://localhost:8501 এ যান")
    print("🎨 নতুন UI এবং উন্নত ফিচার উপভোগ করুন!")
    print("🛑 বন্ধ করতে Ctrl+C চাপুন")
    print("-" * 70)
    
    try:
        # Use appropriate python command for the platform
        if platform.system() == "Windows":
            subprocess.run(["python", "-m", "streamlit", "run", "improved_medicine_chatbot.py"])
        else:
            subprocess.run(["python3", "-m", "streamlit", "run", "improved_medicine_chatbot.py"])
    except KeyboardInterrupt:
        print("\n👋 চ্যাটবট বন্ধ করা হয়েছে")
    except subprocess.CalledProcessError as e:
        print(f"❌ চ্যাটবট চালু করতে সমস্যা: {e}")
        print("💡 সমাধান: pip install streamlit")
    except FileNotFoundError:
        print("❌ Python বা Streamlit পাওয়া যায়নি")
        print("💡 Python এবং Streamlit ইনস্টল করুন")

def show_features():
    """নতুন ফিচারের তালিকা দেখান"""
    print("\n🎯 নতুন ফিচারসমূহ:")
    print("=" * 50)
    print("🎨 Modern এবং Responsive UI Design")
    print("🧭 Improved Navigation System")
    print("📱 Mobile-Friendly Interface")
    print("🔍 Enhanced Search Functionality")
    print("📊 Better Data Visualization")
    print("📁 Organized File Upload System")
    print("💫 Smooth Animations এবং Transitions")
    print("🎭 Professional Color Scheme")
    print("📖 Built-in Help এবং FAQ")
    print("⚡ Quick Access Features")
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
    print("\n🎉 সবকিছু প্রস্তুত! উন্নত চ্যাটবট চালু করা হচ্ছে...")
    print("💡 টিপস: সাইডবার থেকে বিভিন্ন পেজ এক্সপ্লোর করুন")
    
    # Run the improved chatbot
    run_improved_chatbot()

if __name__ == "__main__":
    main()
