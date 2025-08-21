#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💊 সরল মেডিসিন চ্যাটবট
"""

import os
import sys
import json
import re
from pathlib import Path

class SimpleMedicineChatbot:
    def __init__(self):
        self.medicines = []
        self.load_data()
    
    def load_data(self):
        """Excel ফাইল থেকে ডেটা লোড করুন"""
        try:
            # Try to import pandas
            import pandas as pd
            excel_file = Path("medicine_data.xlsx")
            if excel_file.exists():
                df = pd.read_excel(excel_file)
                self.medicines = df.to_dict('records')
                print(f"✅ {len(self.medicines)} টি মেডিসিন লোড হয়েছে")
            else:
                print("❌ medicine_data.xlsx ফাইল পাওয়া যায়নি!")
                self.create_sample_data()
        except ImportError:
            print("⚠️ pandas ইনস্টল নেই, স্যাম্পল ডেটা ব্যবহার করা হচ্ছে")
            self.create_sample_data()
    
    def create_sample_data(self):
        """স্যাম্পল ডেটা তৈরি করুন"""
        self.medicines = [
            {
                'Medicine Name': 'Paracetamol',
                'Generic Name': 'Acetaminophen',
                'Uses': 'জ্বর, ব্যথা',
                'Side Effects': 'মাথাব্যথা, বমি',
                'Dosage': '500-1000mg',
                'Price (৳)': 5
            },
            {
                'Medicine Name': 'Ibuprofen',
                'Generic Name': 'Ibuprofen',
                'Uses': 'ব্যথা, প্রদাহ',
                'Side Effects': 'পেটে ব্যথা',
                'Dosage': '200-400mg',
                'Price (৳)': 8
            },
            {
                'Medicine Name': 'Omeprazole',
                'Generic Name': 'Omeprazole',
                'Uses': 'পেটের আলসার',
                'Side Effects': 'মাথাব্যথা',
                'Dosage': '20mg',
                'Price (৳)': 15
            }
        ]
        print("✅ স্যাম্পল ডেটা লোড হয়েছে")
    
    def search_medicines(self, query):
        """মেডিসিন অনুসন্ধান করুন"""
        if not query.strip():
            return []
        
        query = query.lower()
        results = []
        
        for medicine in self.medicines:
            score = 0
            for key, value in medicine.items():
                if isinstance(value, str):
                    if query in str(value).lower():
                        score += 1
                elif isinstance(value, (int, float)):
                    if query in str(value):
                        score += 1
            
            if score > 0:
                results.append((medicine, score))
        
        # Sort by score (highest first)
        results.sort(key=lambda x: x[1], reverse=True)
        return [medicine for medicine, score in results]
    
    def get_medicine_details(self, medicine):
        """মেডিসিনের বিস্তারিত তথ্য দিন"""
        details = []
        for key, value in medicine.items():
            details.append(f"**{key}:** {value}")
        return "\n".join(details)
    
    def run(self):
        """চ্যাটবট চালান"""
        print("=" * 60)
        print("💊 সরল মেডিসিন চ্যাটবট")
        print("=" * 60)
        print("🔍 মেডিসিনের নাম, ব্যবহার, পার্শ্বপ্রতিক্রিয়া ইত্যাদি লিখে অনুসন্ধান করুন")
        print("🛑 বন্ধ করতে 'quit' বা 'exit' লিখুন")
        print("-" * 60)
        
        while True:
            try:
                query = input("\n💬 আপনি কি খুঁজছেন? ").strip()
                
                if query.lower() in ['quit', 'exit', 'বন্ধ', 'q']:
                    print("👋 ধন্যবাদ! আবার আসবেন!")
                    break
                
                if not query:
                    print("⚠️ অনুগ্রহ করে কিছু লিখুন")
                    continue
                
                results = self.search_medicines(query)
                
                if results:
                    print(f"\n✅ {len(results)} টি ফলাফল পাওয়া গেছে:")
                    print("-" * 40)
                    
                    for i, medicine in enumerate(results[:5], 1):  # Show max 5 results
                        print(f"\n{i}. **{medicine.get('Medicine Name', 'N/A')}**")
                        print(f"   Generic: {medicine.get('Generic Name', 'N/A')}")
                        print(f"   Uses: {medicine.get('Uses', 'N/A')}")
                        print(f"   Dosage: {medicine.get('Dosage', 'N/A')}")
                        print(f"   Price: ৳{medicine.get('Price (৳)', 'N/A')}")
                        
                        # Ask if user wants more details
                        choice = input(f"\n{i} নম্বর মেডিসিনের বিস্তারিত দেখতে চান? (y/n): ").lower().strip()
                        if choice in ['y', 'yes', 'হ্যাঁ']:
                            print("\n📋 বিস্তারিত তথ্য:")
                            print("-" * 30)
                            print(self.get_medicine_details(medicine))
                            print("-" * 30)
                else:
                    print("❌ কোনো মেডিসিন পাওয়া যায়নি")
                    print("💡 অন্য কীওয়ার্ড দিয়ে চেষ্টা করুন")
                    
            except KeyboardInterrupt:
                print("\n👋 ধন্যবাদ! আবার আসবেন!")
                break
            except Exception as e:
                print(f"❌ ত্রুটি: {e}")

def main():
    """মেইন ফাংশন"""
    chatbot = SimpleMedicineChatbot()
    chatbot.run()

if __name__ == "__main__":
    main()
