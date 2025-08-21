#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the new expert response format
"""

import pandas as pd
from medicine_chatbot import format_expert_response

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
