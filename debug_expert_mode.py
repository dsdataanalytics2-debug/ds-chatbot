#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug script to check Expert Mode functionality
"""

import streamlit as st
import pandas as pd
from medicine_chatbot import format_expert_response, format_structured_response, format_strict_response

def debug_expert_mode():
    """Debug the expert mode functionality"""
    
    print("=" * 70)
    print("🔍 Expert Mode Debug")
    print("=" * 70)
    
    # Sample data
    sample_excel_data = [{
        'Name': 'Dibedex 60 capsules',
        'Regular Price': '900',
        'Company Name': 'Index Laboratories (AyU) Ltd.',
        'Medicine Group': 'Ayurvedic',
        'ওষুধের কার্যকারিতা': 'কার্যকারিতা :ডায়াবেটিস এর জন্য কার্যকর',
        'খাওয়ার নিয়ম( প্রাপ্তবয়স্ক ক্ষেত্রে)': 'nan',
        'খাওয়ার নিয়ম( কিশোরদের  ক্ষেত্রে)': 'nan'
    }]
    
    sample_source_data = [{
        'context': 'সজনে পাতার নির্যাস ডায়াবেটিস নিয়ন্ত্রণে বিশেষভাবে কার্যকর।'
    }]
    
    query = "Dibedex"
    
    print("📊 Testing different response formats:")
    print()
    
    # Test Expert Mode
    print("1️⃣ Expert Mode Response:")
    expert_response = format_expert_response(query, sample_excel_data, sample_source_data)
    print(expert_response)
    print("-" * 50)
    
    # Test Structured Mode
    print("2️⃣ Structured Mode Response:")
    structured_response = format_structured_response(query, sample_excel_data, sample_source_data)
    print(structured_response)
    print("-" * 50)
    
    # Test Strict Mode
    print("3️⃣ Strict Mode Response:")
    strict_response = format_strict_response(query, sample_excel_data, sample_source_data)
    print(strict_response)
    print("-" * 50)
    
    print("🔍 Mode Detection Logic:")
    print("if expert_mode: use format_expert_response")
    print("elif strict_mode: use format_strict_response")
    print("else: use format_structured_response")
    print()
    
    print("💡 If you're getting structured/strict format instead of expert format:")
    print("1. Make sure Expert Mode checkbox is checked in sidebar")
    print("2. Check if st.session_state.expert_mode is True")
    print("3. Verify the mode priority logic in the response generation")
    print()
    
    print("🎯 Expected Expert Mode Output:")
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
    debug_expert_mode()
