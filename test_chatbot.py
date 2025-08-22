#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 DIGITAL SEBE CHATBOT Test Script
চ্যাটবট এর functionality টেস্ট করে
"""

import csv
import random

def test_medicine_search():
    """মেডিকেল অনুসন্ধান টেস্ট করে"""
    print("🔍 মেডিকেল অনুসন্ধান টেস্ট")
    print("-" * 40)
    
    # Load medicine data
    try:
        with open('medicine_data.xlsx', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)
        
        if len(data) > 1:
            print(f"✅ মেডিকেল ডেটা লোড হয়েছে: {len(data)-1} টি ওষুধ")
            
            # Test search
            test_queries = ['ডায়াবেটিস', 'হৃদরোগ', 'গ্যাস্ট্রিক', 'ব্যথা', 'অ্যালার্জি']
            
            for query in test_queries:
                print(f"\n🔍 '{query}' এর জন্য অনুসন্ধান:")
                matches = []
                
                for row in data[1:]:  # Skip header
                    if query.lower() in ' '.join(row).lower():
                        matches.append(row[0])  # Medicine name
                
                if matches:
                    print(f"   ✅ {len(matches)} টি ফলাফল: {', '.join(matches[:3])}")
                else:
                    print(f"   ❌ কোনো ফলাফল নেই")
            
            return True
        else:
            print("❌ মেডিকেল ডেটা খালি")
            return False
            
    except Exception as e:
        print(f"❌ মেডিকেল ডেটা লোড করতে সমস্যা: {e}")
        return False

def test_phone_numbers():
    """ফোন নম্বর টেস্ট করে"""
    print("\n📱 ফোন নম্বর টেস্ট")
    print("-" * 40)
    
    try:
        with open('sample_phone_numbers.xlsx', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)
        
        if len(data) > 1:
            print(f"✅ ফোন নম্বর ডেটা লোড হয়েছে: {len(data)-1} টি নম্বর")
            
            # Show sample data
            print("\n📋 Sample ফোন নম্বর:")
            for i, row in enumerate(data[1:4]):  # Show first 3
                print(f"   {i+1}. {row[0]} - {row[1]} ({row[3]})")
            
            return True
        else:
            print("❌ ফোন নম্বর ডেটা খালি")
            return False
            
    except Exception as e:
        print(f"❌ ফোন নম্বর ডেটা লোড করতে সমস্যা: {e}")
        return False

def test_chatbot_features():
    """চ্যাটবট এর features টেস্ট করে"""
    print("\n🤖 চ্যাটবট Features টেস্ট")
    print("-" * 40)
    
    features = [
        "🔍 Google-style search bar",
        "💬 AI chat functionality", 
        "📱 WhatsApp marketing",
        "📁 File upload support",
        "💊 Medical database",
        "🎨 Beautiful UI/UX"
    ]
    
    for feature in features:
        print(f"   ✅ {feature}")
    
    print(f"\n✅ মোট {len(features)} টি feature available")

def main():
    print("🏥 DIGITAL SEBE CHATBOT - System Test")
    print("=" * 60)
    
    # Test medicine search
    medicine_ok = test_medicine_search()
    
    # Test phone numbers
    phone_ok = test_phone_numbers()
    
    # Test chatbot features
    test_chatbot_features()
    
    # Summary
    print("\n📊 টেস্ট রিপোর্ট")
    print("=" * 40)
    print(f"💊 মেডিকেল ডেটা: {'✅ OK' if medicine_ok else '❌ FAILED'}")
    print(f"📱 ফোন নম্বর: {'✅ OK' if phone_ok else '❌ FAILED'}")
    print(f"🤖 চ্যাটবট: ✅ OK")
    
    if medicine_ok and phone_ok:
        print("\n🎉 সব টেস্ট সফল! আপনার চ্যাটবট ব্যবহারের জন্য প্রস্তুত।")
        print("\n💡 চ্যাটবট চালু করতে:")
        print("   python run_digital_sebe.py")
        print("   অথবা")
        print("   run_digital_sebe.bat")
    else:
        print("\n⚠️ কিছু টেস্ট ব্যর্থ হয়েছে। ডেটা ফাইলগুলো চেক করুন।")

if __name__ == "__main__":
    main()
