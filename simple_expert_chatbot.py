#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Expert Mode Chatbot Demo
"""

import pandas as pd

def format_expert_response(query: str, excel_results, all_source_results):
    """এক্সপার্ট ডেভেলপার Dibedex এর জন্য নির্দিষ্ট ফরম্যাটে উত্তর"""
    try:
        parts = []
        
        if not excel_results and not all_source_results:
            parts.append("❌ **দুঃখিত, আপনার প্রশ্নের সাথে মিলে এমন তথ্য পাওয়া যায়নি।**\n")
            return "".join(parts)

        # মূল ওষুধের তথ্য - নির্দিষ্ট ফরম্যাটে
        if excel_results:
            top = excel_results[0]
            
            # Name - সঠিক কলাম নাম ব্যবহার
            name = top.get('Name', 'N/A')
            parts.append(f"**Name:**{name}\n")
            
            # Regular Price - সঠিক কলাম নাম ব্যবহার
            price = top.get('Regular Price', 'N/A')
            parts.append(f"**Regular Price:**{price}\n")
            
            # Company Name - সঠিক কলাম নাম ব্যবহার
            company = top.get('Company Name', 'N/A')
            parts.append(f"**Company Name:**{company}\n")
            
            # Medicine Group - সঠিক কলাম নাম ব্যবহার
            group = top.get('Medicine Group', 'N/A')
            parts.append(f"**Medicine Group:**{group}\n")
            
            # কার্যকারিতা - সঠিক কলাম নাম ব্যবহার এবং পরিষ্কার করা
            uses = top.get('ওষুধের কার্যকারিতা', 'N/A')
            # "কার্যকারিতা :" অংশ সরানো
            if isinstance(uses, str) and 'কার্যকারিতা :' in uses:
                uses = uses.replace('কার্যকারিতা :', '').strip()
            parts.append(f"**ওষুধের কার্যকারিতা:**{uses}\n")
            
            # খাওয়ার নিয়ম (প্রাপ্তবয়স্ক) - সঠিক কলাম নাম ব্যবহার
            adult_dosage = top.get('খাওয়ার নিয়ম( প্রাপ্তবয়স্ক ক্ষেত্রে)', 'nan')
            parts.append(f"**খাওয়ার নিয়ম (প্রাপ্তবয়স্ক ক্ষেত্রে):**{adult_dosage}\n")
            
            # খাওয়ার নিয়ম (কিশোর) - সঠিক কলাম নাম ব্যবহার
            child_dosage = top.get('খাওয়ার নিয়ম( কিশোরদের  ক্ষেত্রে)', 'nan')
            parts.append(f"**খাওয়ার নিয়ম (কিশোরদের ক্ষেত্রে):**{child_dosage}\n")
            
            # বিস্তারিত তথ্য - কার্যকারিতা থেকে নেওয়া এবং পরিষ্কার করা
            details = top.get('ওষুধের কার্যকারিতা', 'N/A')
            if isinstance(details, str) and 'কার্যকারিতা :' in details:
                details = details.replace('কার্যকারিতা :', '').strip()
            parts.append(f"**বিস্তারিত তথ্য:**\n")
            parts.append(f"**ওষুধের বিস্তারিত তথ্য:**{details}\n")

        # অতিরিক্ত তথ্য
        if all_source_results:
            for i, r in enumerate(all_source_results[:2], 1):
                ctx = r.get('context') or r.get('full_content', '')
                if ctx:
                    cleaned_ctx = ctx.strip()
                    if len(cleaned_ctx) > 300:
                        cleaned_ctx = cleaned_ctx[:300] + "..."
                    
                    if i == 1:
                        parts.append(f"{cleaned_ctx}\n")

        return "".join(parts)
    except Exception as e:
        return f"❌ এক্সপার্ট রেসপন্স তৈরি করতে সমস্যা: {e}"

def simple_chatbot():
    """Simple chatbot with Expert Mode"""
    
    print("=" * 70)
    print("💊 Simple Expert Mode Chatbot")
    print("=" * 70)
    print("✅ Expert Mode (Dibedex Format) is ENABLED")
    print("🔍 Type a medicine name to get information in Expert format")
    print("❌ Type 'quit' to exit")
    print("=" * 70)
    
    # Load Excel data
    try:
        df = pd.read_excel('medicine_data.xlsx')
        print(f"📊 Loaded {len(df)} medicines from Excel")
    except Exception as e:
        print(f"❌ Error loading Excel file: {e}")
        return
    
    while True:
        query = input("\n🔍 Enter medicine name: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not query:
            continue
        
        # Search for medicine
        search_results = []
        for _, row in df.iterrows():
            if query.lower() in str(row['Name']).lower():
                search_results.append(row.to_dict())
        
        if not search_results:
            print("❌ Medicine not found. Try another name.")
            continue
        
        # Simulate source results
        source_results = [{
            'context': 'সজনে পাতার নির্যাস ডায়াবেটিস নিয়ন্ত্রণে বিশেষভাবে কার্যকর। এটি রক্তে শর্করার মাত্রা নিয়ন্ত্রণ করে এবং ইনসুলিন সংবেদনশীলতা বৃদ্ধি করে।'
        }]
        
        # Generate response using Expert Mode
        response = format_expert_response(query, search_results, source_results)
        
        print("\n💊 Expert Mode Response:")
        print("-" * 50)
        print(response)
        print("-" * 50)

if __name__ == "__main__":
    simple_chatbot()
