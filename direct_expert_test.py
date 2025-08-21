#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct test for Expert Mode functionality
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

def simulate_chatbot_response(query, expert_mode=True, strict_mode=False):
    """Simulate chatbot response with different modes"""
    
    # Read Excel data
    df = pd.read_excel('medicine_data.xlsx')
    
    # Search for medicine
    search_results = []
    for _, row in df.iterrows():
        if query.lower() in str(row['Name']).lower():
            search_results.append(row.to_dict())
    
    if not search_results:
        return "❌ Medicine not found"
    
    # Simulate source results
    source_results = [{
        'context': 'সজনে পাতার নির্যাস ডায়াবেটিস নিয়ন্ত্রণে বিশেষভাবে কার্যকর। এটি রক্তে শর্করার মাত্রা নিয়ন্ত্রণ করে এবং ইনসুলিন সংবেদনশীলতা বৃদ্ধি করে।'
    }]
    
    # Mode selection logic (same as chatbot)
    if expert_mode:
        print("🎯 Using Expert Mode (format_expert_response)")
        return format_expert_response(query, search_results, source_results)
    elif strict_mode:
        print("🎯 Using Strict Mode (format_strict_response)")
        return "Strict mode response would be here"
    else:
        print("🎯 Using Structured Mode (format_structured_response)")
        return "Structured mode response would be here"

def test_expert_mode():
    """Test expert mode functionality"""
    
    print("=" * 70)
    print("🧪 Direct Expert Mode Test")
    print("=" * 70)
    
    query = "Dibedex"
    
    print(f"🔍 Query: {query}")
    print()
    
    # Test with Expert Mode ON
    print("1️⃣ Expert Mode = True:")
    response = simulate_chatbot_response(query, expert_mode=True, strict_mode=False)
    print(response)
    print("-" * 50)
    
    # Test with Expert Mode OFF
    print("2️⃣ Expert Mode = False:")
    response = simulate_chatbot_response(query, expert_mode=False, strict_mode=False)
    print(response)
    print("-" * 50)
    
    print("✅ Expected Expert Mode Output:")
    print("**Name:**Dibedex 60 capsules")
    print("**Regular Price:**900")
    print("**Company Name:**Index Laboratories (AyU) Ltd.")
    print("**Medicine Group:**Ayurvedic")
    print("**ওষুধের কার্যকারিতা:**ডায়াবেটিস এর জন্য কার্যকর")
    print("**খাওয়ার নিয়ম (প্রাপ্তবয়স্ক ক্ষেত্রে):**nan")
    print("**খাওয়ার নিয়ম (কিশোরদের ক্ষেত্রে):**nan")
    print("**বিস্তারিত তথ্য:**")
    print("**ওষুধের বিস্তারিত তথ্য:**ডায়াবেটিস এর জন্য কার্যকর")
    print("=" * 70)

if __name__ == "__main__":
    test_expert_mode()
