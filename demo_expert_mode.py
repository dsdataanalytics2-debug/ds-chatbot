#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script for Expert Mode functionality
"""

import pandas as pd

def demo_expert_mode():
    """Demo the expert mode functionality"""
    
    print("=" * 70)
    print("👨‍💻 Expert Mode Demo - Dibedex Format")
    print("=" * 70)
    
    print("🎯 This demo shows how the Expert Mode formats medicine information")
    print("📋 The format follows the exact structure you requested:")
    print()
    
    print("✅ Expected Format:")
    print("**Name:** [Medicine Name]")
    print("**Regular Price:** [Price]")
    print("**Company Name:** [Manufacturer]")
    print("**Medicine Group:** [Category]")
    print("**ওষুধের কার্যকারিতা:** [Uses]")
    print("**খাওয়ার নিয়ম (প্রাপ্তবয়স্ক ক্ষেত্রে):** [Adult Dosage]")
    print("**খাওয়ার নিয়ম (কিশোরদের ক্ষেত্রে):** [Child Dosage]")
    print("**বিস্তারিত তথ্য:**")
    print("**ওষুধের বিস্তারিত তথ্য:** [Description]")
    print()
    
    try:
        # Read Excel data
        df = pd.read_excel('medicine_data.xlsx')
        
        print("📊 Sample Data from Excel:")
        if len(df) > 0:
            sample = df.iloc[0]
            print(f"  Name: {sample['Name']}")
            print(f"  Regular Price: {sample['Regular Price']}")
            print(f"  Company Name: {sample['Company Name']}")
            print(f"  Medicine Group: {sample['Medicine Group']}")
            print(f"  কার্যকারিতা: {sample['ওষুধের কার্যকারিতা']}")
            print()
        
        print("🚀 How to Use Expert Mode:")
        print("1. Open the chatbot at http://localhost:8502")
        print("2. In the sidebar, check '👨‍💻 এক্সপার্ট মোড (Dibedex ফরম্যাট)'")
        print("3. Type a medicine name (e.g., 'Dibedex')")
        print("4. Press Enter or click '🔍 খুঁজুন'")
        print("5. Get the response in Expert format!")
        print()
        
        print("🎨 Example Output:")
        print("**Name:**Dibedex 60 capsules")
        print("**Regular Price:**900")
        print("**Company Name:**Index Laboratories (AyU) Ltd.")
        print("**Medicine Group:**Ayurvedic")
        print("**ওষুধের কার্যকারিতা:**ডায়াবেটিস এর জন্য কার্যকর")
        print("**খাওয়ার নিয়ম (প্রাপ্তবয়স্ক ক্ষেত্রে):**nan")
        print("**খাওয়ার নিয়ম (কিশোরদের ক্ষেত্রে):**nan")
        print("**বিস্তারিত তথ্য:**")
        print("**ওষুধের বিস্তারিত তথ্য:**ডায়াবেটিস এর জন্য কার্যকর")
        print()
        
        print("✨ Features:")
        print("• Clean, professional format")
        print("• Bengali medical terminology")
        print("• Consistent structure for all medicines")
        print("• Handles missing data gracefully (shows 'nan')")
        print("• Integrates with uploaded documents")
        print()
        
        print("🔧 Technical Details:")
        print("• Function: format_expert_response()")
        print("• Priority: Highest (overrides other modes)")
        print("• Compatibility: Works with existing Excel structure")
        print("• Customizable: Easy to modify format")
        print()
        
        print("🎯 Ready to test! Open http://localhost:8502 and enable Expert Mode")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure medicine_data.xlsx exists in the current directory")

if __name__ == "__main__":
    demo_expert_mode()
