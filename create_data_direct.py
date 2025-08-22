#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💊 Sample Data Generator - No External Dependencies
মেডিকেল চ্যাটবট এর জন্য sample ডেটা CSV ফাইলে তৈরি করে
"""

import csv
import random

def create_sample_medicine_data():
    """Sample মেডিকেল ডেটা তৈরি করে CSV ফাইলে সেভ করে"""
    
    # Sample medicine data
    data = [
        ['Medicine Name', 'Bengali Name', 'Category', 'Uses', 'Side Effects', 'Dosage', 'Price (BDT)', 'Availability'],
        ['Paracetamol', 'প্যারাসিটামল', 'Pain Relief', 'জ্বর ও ব্যথা কমায়', 'পেটে ব্যথা, বমি বমি ভাব', '500-1000mg 4-6 ঘণ্টা পর', '2.50', 'Available'],
        ['Ibuprofen', 'আইবুপ্রোফেন', 'Pain Relief', 'ব্যথা ও প্রদাহ কমায়', 'পেটে ব্যথা, মাথা ব্যথা', '200-400mg 4-6 ঘণ্টা পর', '5.00', 'Available'],
        ['Omeprazole', 'ওমেপ্রাজোল', 'Gastric', 'গ্যাস্ট্রিক সমস্যা সমাধান', 'মাথা ব্যথা, বমি বমি ভাব', '20mg দিনে একবার', '8.00', 'Available'],
        ['Metformin', 'মেটফরমিন', 'Diabetes', 'ডায়াবেটিস নিয়ন্ত্রণ', 'বমি বমি ভাব, ডায়রিয়া', '500mg দিনে দুইবার', '3.50', 'Available'],
        ['Amlodipine', 'অ্যামলোডিপাইন', 'Blood Pressure', 'উচ্চ রক্তচাপ নিয়ন্ত্রণ', 'মাথা ব্যথা, ফুলে যাওয়া', '5-10mg দিনে একবার', '6.00', 'Available'],
        ['Atorvastatin', 'অ্যাটরভাস্ট্যাটিন', 'Cholesterol', 'কোলেস্টেরল কমায়', 'মাংসপেশিতে ব্যথা, পেটে ব্যথা', '10-20mg দিনে একবার', '12.00', 'Available'],
        ['Cetirizine', 'সিটিরিজিন', 'Allergy', 'অ্যালার্জি প্রতিরোধ', 'ঘুম ঘুম ভাব, শুষ্ক মুখ', '10mg দিনে একবার', '4.00', 'Available'],
        ['Ranitidine', 'রানিটিডিন', 'Gastric', 'গ্যাস্ট্রিক অ্যাসিড কমায়', 'মাথা ব্যথা, বমি বমি ভাব', '150mg দিনে দুইবার', '3.00', 'Available'],
        ['Diclofenac', 'ডিক্লোফেনাক', 'Pain Relief', 'ব্যথা ও প্রদাহ কমায়', 'পেটে ব্যথা, বমি বমি ভাব', '50mg দিনে দুইবার', '7.00', 'Available'],
        ['Aspirin', 'অ্যাসপিরিন', 'Pain Relief', 'ব্যথা কমায় ও রক্ত পাতলা করে', 'পেটে ব্যথা, রক্তক্ষরণ', '75-150mg দিনে একবার', '1.50', 'Available']
    ]
    
    # Save to CSV
    with open('medicine_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    
    print("✅ Sample medicine data CSV file created: medicine_data.csv")
    print(f"💊 Total medicines: {len(data)-1}")
    
    # Display sample
    print("\n📋 Sample data:")
    for row in data[:5]:
        print(row)
    
    return data

def create_sample_phone_numbers():
    """Sample ফোন নম্বর তৈরি করে CSV ফাইলে সেভ করে"""
    
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
    
    # Create data
    data = [
        ['Name', 'Phone Number', 'Email', 'City']
    ]
    
    cities = ['ঢাকা', 'চট্টগ্রাম', 'সিলেট', 'রাজশাহী', 'খুলনা']
    for i in range(20):
        data.append([
            names[i],
            phone_numbers[i],
            emails[i],
            cities[i % 5]
        ])
    
    # Save to CSV
    with open('sample_phone_numbers.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    
    print("✅ Sample phone numbers CSV file created: sample_phone_numbers.csv")
    print(f"📱 Total phone numbers: {len(data)-1}")
    
    # Display sample
    print("\n📋 Sample data:")
    for row in data[:5]:
        print(row)
    
    return data

if __name__ == "__main__":
    print("🏥 DIGITAL SEBE CHATBOT - Sample Data Generator")
    print("=" * 60)
    
    # Create medicine data
    create_sample_medicine_data()
    print()
    
    # Create phone numbers
    create_sample_phone_numbers()
    print()
    
    print("🎉 সব sample data সফলভাবে তৈরি হয়েছে!")
    print("📁 ফাইলগুলো: medicine_data.csv, sample_phone_numbers.csv")
