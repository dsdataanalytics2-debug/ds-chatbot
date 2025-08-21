#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple test for expert response format
"""

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
            
            # Name
            name = top.get('Medicine Name', top.get('Name', 'N/A'))
            parts.append(f"**Name:**{name}\n")
            
            # Regular Price
            price = top.get('Price (৳)', top.get('Regular Price', 'N/A'))
            parts.append(f"**Regular Price:**{price}\n")
            
            # Company Name
            company = top.get('Company Name', top.get('Manufacturer', 'N/A'))
            parts.append(f"**Company Name:**{company}\n")
            
            # Medicine Group
            group = top.get('Medicine Group', top.get('Category', 'N/A'))
            parts.append(f"**Medicine Group:**{group}\n")
            
            # কার্যকারিতা
            uses = top.get('Uses', top.get('কার্যকারিতা', 'N/A'))
            parts.append(f"**ওষুধের কার্যকারিতা:**{uses}\n")
            
            # খাওয়ার নিয়ম (প্রাপ্তবয়স্ক)
            adult_dosage = top.get('Dosage', top.get('খাওয়ার নিয়ম (প্রাপ্তবয়স্ক)', 'nan'))
            parts.append(f"**খাওয়ার নিয়ম (প্রাপ্তবয়স্ক ক্ষেত্রে):**{adult_dosage}\n")
            
            # খাওয়ার নিয়ম (কিশোর)
            child_dosage = top.get('Child Dosage', top.get('খাওয়ার নিয়ম (কিশোরদের ক্ষেত্রে)', 'nan'))
            parts.append(f"**খাওয়ার নিয়ম (কিশোরদের ক্ষেত্রে):**{child_dosage}\n")
            
            # বিস্তারিত তথ্য
            details = top.get('Description', top.get('বিস্তারিত তথ্য', 'N/A'))
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

def test_expert_format():
    """Test the expert response format"""
    
    # Sample Excel data
    sample_excel_data = [{
        'Medicine Name': 'Dibedex 60 capsules',
        'Price (৳)': '900',
        'Company Name': 'Index Laboratories (AyU) Ltd.',
        'Medicine Group': 'Ayurvedic',
        'Uses': 'ডায়াবেটিস এর জন্য কার্যকর',
        'Dosage': 'nan',
        'Child Dosage': 'nan',
        'Description': 'যা মূলত সজনে পাতার নির্যাস থেকে তৈরি, শরীরের জন্য বেশ কিছু উপকারী গুণাবলী রয়েছে।'
    }]
    
    # Sample source data
    sample_source_data = [{
        'context': 'সজনে পাতার নির্যাস ডায়াবেটিস নিয়ন্ত্রণে বিশেষভাবে কার্যকর। এটি রক্তে শর্করার মাত্রা নিয়ন্ত্রণ করে এবং ইনসুলিন সংবেদনশীলতা বৃদ্ধি করে।'
    }]
    
    # Test the expert format
    query = "Dibedex"
    response = format_expert_response(query, sample_excel_data, sample_source_data)
    
    print("=" * 60)
    print("🧪 Expert Format Test Results")
    print("=" * 60)
    print(response)
    print("=" * 60)
    
    # Check if the format matches the expected structure
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
    
    print("\n🎯 Expert format test completed!")

if __name__ == "__main__":
    test_expert_format()
