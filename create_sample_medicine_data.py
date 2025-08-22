#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💊 Sample Medicine Data Generator
মেডিকেল চ্যাটবট এর জন্য sample ওষুধের তথ্য Excel ফাইলে তৈরি করে
"""

import pandas as pd

def create_sample_medicine_data():
    """Sample মেডিকেল ডেটা তৈরি করে Excel ফাইলে সেভ করে"""
    
    # Sample medicine data
    data = {
        'Medicine Name': [
            'Paracetamol', 'Ibuprofen', 'Omeprazole', 'Metformin', 'Amlodipine',
            'Atorvastatin', 'Omeprazole', 'Cetirizine', 'Ranitidine', 'Diclofenac',
            'Aspirin', 'Loratadine', 'Pantoprazole', 'Simvastatin', 'Losartan',
            'Glimepiride', 'Gliclazide', 'Insulin', 'Warfarin', 'Furosemide'
        ],
        'Bengali Name': [
            'প্যারাসিটামল', 'আইবুপ্রোফেন', 'ওমেপ্রাজোল', 'মেটফরমিন', 'অ্যামলোডিপাইন',
            'অ্যাটরভাস্ট্যাটিন', 'ওমেপ্রাজোল', 'সিটিরিজিন', 'রানিটিডিন', 'ডিক্লোফেনাক',
            'অ্যাসপিরিন', 'লোরাটাডিন', 'প্যান্টোপ্রাজোল', 'সিমভাস্ট্যাটিন', 'লোসার্টান',
            'গ্লিমেপিরাইড', 'গ্লিক্লাজাইড', 'ইনসুলিন', 'ওয়ারফারিন', 'ফুরোসেমাইড'
        ],
        'Category': [
            'Pain Relief', 'Pain Relief', 'Gastric', 'Diabetes', 'Blood Pressure',
            'Cholesterol', 'Gastric', 'Allergy', 'Gastric', 'Pain Relief',
            'Pain Relief', 'Allergy', 'Gastric', 'Cholesterol', 'Blood Pressure',
            'Diabetes', 'Diabetes', 'Diabetes', 'Blood Thinner', 'Diuretic'
        ],
        'Uses': [
            'জ্বর ও ব্যথা কমায়', 'ব্যথা ও প্রদাহ কমায়', 'গ্যাস্ট্রিক সমস্যা সমাধান', 'ডায়াবেটিস নিয়ন্ত্রণ', 'উচ্চ রক্তচাপ নিয়ন্ত্রণ',
            'কোলেস্টেরল কমায়', 'গ্যাস্ট্রিক আলসার চিকিৎসা', 'অ্যালার্জি প্রতিরোধ', 'গ্যাস্ট্রিক অ্যাসিড কমায়', 'ব্যথা ও প্রদাহ কমায়',
            'ব্যথা কমায় ও রক্ত পাতলা করে', 'অ্যালার্জি প্রতিরোধ', 'গ্যাস্ট্রিক সমস্যা সমাধান', 'কোলেস্টেরল কমায়', 'উচ্চ রক্তচাপ নিয়ন্ত্রণ',
            'ডায়াবেটিস নিয়ন্ত্রণ', 'ডায়াবেটিস নিয়ন্ত্রণ', 'ডায়াবেটিস নিয়ন্ত্রণ', 'রক্ত জমাট বাঁধা প্রতিরোধ', 'মূত্রবর্ধক'
        ],
        'Side Effects': [
            'পেটে ব্যথা, বমি বমি ভাব', 'পেটে ব্যথা, মাথা ব্যথা', 'মাথা ব্যথা, বমি বমি ভাব', 'বমি বমি ভাব, ডায়রিয়া', 'মাথা ব্যথা, ফুলে যাওয়া',
            'মাংসপেশিতে ব্যথা, পেটে ব্যথা', 'মাথা ব্যথা, বমি বমি ভাব', 'ঘুম ঘুম ভাব, শুষ্ক মুখ', 'মাথা ব্যথা, বমি বমি ভাব', 'পেটে ব্যথা, বমি বমি ভাব',
            'পেটে ব্যথা, রক্তক্ষরণ', 'মাথা ব্যথা, শুষ্ক মুখ', 'মাথা ব্যথা, বমি বমি ভাব', 'মাংসপেশিতে ব্যথা, পেটে ব্যথা', 'মাথা ব্যথা, ফুলে যাওয়া',
            'রক্তে শর্করা কমে যাওয়া, মাথা ঘোরা', 'রক্তে শর্করা কমে যাওয়া, মাথা ঘোরা', 'রক্তে শর্করা কমে যাওয়া, ওজন বাড়া', 'রক্তক্ষরণ, বমি বমি ভাব', 'মূত্রত্যাগ বেড়ে যাওয়া, রক্তচাপ কমে যাওয়া'
        ],
        'Dosage': [
            '500-1000mg 4-6 ঘণ্টা পর', '200-400mg 4-6 ঘণ্টা পর', '20mg দিনে একবার', '500mg দিনে দুইবার', '5-10mg দিনে একবার',
            '10-20mg দিনে একবার', '20mg দিনে একবার', '10mg দিনে একবার', '150mg দিনে দুইবার', '50mg দিনে দুইবার',
            '75-150mg দিনে একবার', '10mg দিনে একবার', '40mg দিনে একবার', '20-40mg দিনে একবার', '50mg দিনে একবার',
            '1-2mg দিনে একবার', '80mg দিনে দুইবার', 'ইনজেকশন', '5mg দিনে একবার', '40mg দিনে একবার'
        ],
        'Price (BDT)': [
            '2.50', '5.00', '8.00', '3.50', '6.00',
            '12.00', '8.00', '4.00', '3.00', '7.00',
            '1.50', '4.00', '10.00', '15.00', '8.00',
            '5.00', '4.50', '150.00', '2.00', '3.50'
        ],
        'Availability': [
            'Available', 'Available', 'Available', 'Available', 'Available',
            'Available', 'Available', 'Available', 'Available', 'Available',
            'Available', 'Available', 'Available', 'Available', 'Available',
            'Available', 'Available', 'Available', 'Available', 'Available'
        ]
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to Excel
    df.to_excel('medicine_data.xlsx', index=False)
    print("✅ Sample medicine data Excel file created: medicine_data.xlsx")
    print(f"💊 Total medicines: {len(df)}")
    
    # Display sample
    print("\n📋 Sample data:")
    print(df.head())
    
    # Display categories
    print(f"\n🏥 Medicine categories: {df['Category'].nunique()}")
    print("Categories:", ', '.join(df['Category'].unique()))
    
    return df

if __name__ == "__main__":
    create_sample_medicine_data()
