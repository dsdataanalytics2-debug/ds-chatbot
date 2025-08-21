#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test expert format with real Excel data structure
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

def test_with_real_data():
    """Test with actual Excel data"""
    try:
        # Read actual Excel file
        df = pd.read_excel('medicine_data.xlsx')
        
        print("=" * 60)
        print("🧪 Testing with Real Excel Data")
        print("=" * 60)
        
        # Get first medicine data
        if len(df) > 0:
            first_medicine = df.iloc[0].to_dict()
            
            print("📊 First medicine data:")
            for key, value in first_medicine.items():
                print(f"  {key}: {value}")
            print()
            
            # Test expert format
            query = "Dibedex"
            excel_results = [first_medicine]
            all_source_results = [{
                'context': 'সজনে পাতার নির্যাস ডায়াবেটিস নিয়ন্ত্রণে বিশেষভাবে কার্যকর। এটি রক্তে শর্করার মাত্রা নিয়ন্ত্রণ করে এবং ইনসুলিন সংবেদনশীলতা বৃদ্ধি করে।'
            }]
            
            response = format_expert_response(query, excel_results, all_source_results)
            
            print("📝 Expert Format Response:")
            print(response)
            print("=" * 60)
            
            # Check if format matches expected structure
            expected_fields = [
                "**Name:**",
                "**Regular Price:**",
                "**Company Name:**",
                "**Medicine Group:**",
                "**ওষুধের কার্যকারিতা:**",
                "**খাওয়ার নিয়ম (প্রাপ্তবয়স্ক ক্ষেত্রে):**",
                "**খাওয়ার নিয়ম (কিশোরদের ক্ষেত্রে):**",
                "**বিস্তারিত তথ্য:**",
                "**ওষুধের বিস্তারিত তথ্য:**"
            ]
            
            print("\n✅ Format Verification:")
            for field in expected_fields:
                if field in response:
                    print(f"  ✓ {field} found")
                else:
                    print(f"  ❌ {field} missing")
            
            print("\n🎯 Real data test completed!")
            
        else:
            print("❌ No data found in Excel file")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_with_real_data()
