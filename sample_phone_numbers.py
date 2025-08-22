#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📱 Sample Phone Numbers Generator
WhatsApp Marketing এর জন্য sample ফোন নম্বর Excel ফাইল তৈরি করে
"""

import pandas as pd
import random

def generate_sample_phone_numbers():
    """Sample ফোন নম্বর তৈরি করে Excel ফাইলে সেভ করে"""
    
    # Sample names
    names = [
        "আহমেদ আলী", "ফাতেমা বেগম", "মোহাম্মদ রহমান", "আয়েশা খাতুন",
        "আব্দুল করিম", "রাহেলা সুলতানা", "হাসান মাহমুদ", "নাজমা আক্তার",
        "ইব্রাহিম হোসেন", "সাবরিনা ইয়াসমিন", "মুস্তাফা আহমেদ", "রেহানা পারভীন",
        "আব্দুল্লাহ খান", "মরিয়ম বেগম", "রফিকুল ইসলাম", "তানিয়া আহমেদ",
        "শাহজাহান আলী", "নুসরাত জাহান", "মাহমুদুর রহমান", "ফারজানা আক্তার"
    ]
    
    # Generate phone numbers
    phone_numbers = []
    for i in range(20):
        # Bangladesh format: +8801XXXXXXXXX
        prefix = random.choice(['71', '72', '73', '74', '75', '76', '77', '78', '79'])
        number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        phone_numbers.append(f"+8801{prefix}{number}")
    
    # Generate emails
    emails = []
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
    for name in names:
        clean_name = name.replace(' ', '').lower()
        domain = random.choice(domains)
        emails.append(f"{clean_name}@{domain}")
    
    # Create DataFrame
    data = {
        'Name': names,
        'Phone Number': phone_numbers,
        'Email': emails,
        'City': ['ঢাকা', 'চট্টগ্রাম', 'সিলেট', 'রাজশাহী', 'খুলনা'] * 4
    }
    
    df = pd.DataFrame(data)
    
    # Save to Excel
    df.to_excel('sample_phone_numbers.xlsx', index=False)
    print("✅ Sample phone numbers Excel file created: sample_phone_numbers.xlsx")
    print(f"📱 Total phone numbers: {len(df)}")
    
    # Display sample
    print("\n📋 Sample data:")
    print(df.head())
    
    return df

if __name__ == "__main__":
    generate_sample_phone_numbers()
