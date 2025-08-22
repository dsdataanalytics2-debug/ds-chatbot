#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 Manual Excel File Creator
বাহ্যিক dependencies ছাড়াই Excel ফাইল তৈরি করে
"""

import csv

def create_excel_like_csv():
    """Excel এর মত সুন্দর CSV ফাইল তৈরি করে"""
    
    # Medicine data with better formatting
    medicine_data = [
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
        ['Aspirin', 'অ্যাসপিরিন', 'Pain Relief', 'ব্যথা কমায় ও রক্ত পাতলা করে', 'পেটে ব্যথা, রক্তক্ষরণ', '75-150mg দিনে একবার', '1.50', 'Available'],
        ['Loratadine', 'লোরাটাডিন', 'Allergy', 'অ্যালার্জি প্রতিরোধ', 'মাথা ব্যথা, শুষ্ক মুখ', '10mg দিনে একবার', '4.00', 'Available'],
        ['Pantoprazole', 'প্যান্টোপ্রাজোল', 'Gastric', 'গ্যাস্ট্রিক সমস্যা সমাধান', 'মাথা ব্যথা, বমি বমি ভাব', '40mg দিনে একবার', '10.00', 'Available'],
        ['Simvastatin', 'সিমভাস্ট্যাটিন', 'Cholesterol', 'কোলেস্টেরল কমায়', 'মাংসপেশিতে ব্যথা, পেটে ব্যথা', '20-40mg দিনে একবার', '15.00', 'Available'],
        ['Losartan', 'লোসার্টান', 'Blood Pressure', 'উচ্চ রক্তচাপ নিয়ন্ত্রণ', 'মাথা ব্যথা, ফুলে যাওয়া', '50mg দিনে একবার', '8.00', 'Available'],
        ['Glimepiride', 'গ্লিমেপিরাইড', 'Diabetes', 'ডায়াবেটিস নিয়ন্ত্রণ', 'রক্তে শর্করা কমে যাওয়া, মাথা ঘোরা', '1-2mg দিনে একবার', '5.00', 'Available'],
        ['Gliclazide', 'গ্লিক্লাজাইড', 'Diabetes', 'ডায়াবেটিস নিয়ন্ত্রণ', 'রক্তে শর্করা কমে যাওয়া, মাথা ঘোরা', '80mg দিনে দুইবার', '4.50', 'Available'],
        ['Insulin', 'ইনসুলিন', 'Diabetes', 'ডায়াবেটিস নিয়ন্ত্রণ', 'রক্তে শর্করা কমে যাওয়া, ওজন বাড়া', 'ইনজেকশন', '150.00', 'Available'],
        ['Warfarin', 'ওয়ারফারিন', 'Blood Thinner', 'রক্ত জমাট বাঁধা প্রতিরোধ', 'রক্তক্ষরণ, বমি বমি ভাব', '5mg দিনে একবার', '2.00', 'Available'],
        ['Furosemide', 'ফুরোসেমাইড', 'Diuretic', 'মূত্রবর্ধক', 'মূত্রত্যাগ বেড়ে যাওয়া, রক্তচাপ কমে যাওয়া', '40mg দিনে একবার', '3.50', 'Available']
    ]
    
    # Save to CSV with better formatting
    with open('medicine_data.xlsx', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(medicine_data)
    
    print("✅ Enhanced medicine data saved to: medicine_data.xlsx")
    print(f"💊 Total medicines: {len(medicine_data)-1}")
    
    # Display categories
    categories = set()
    for row in medicine_data[1:]:
        categories.add(row[2])
    
    print(f"\n🏥 Medicine categories: {len(categories)}")
    print("Categories:", ', '.join(sorted(categories)))
    
    return medicine_data

def create_enhanced_phone_numbers():
    """Enhanced ফোন নম্বর তালিকা তৈরি করে"""
    
    # Sample names with more variety
    names = [
        "আহমেদ আলী", "ফাতেমা বেগম", "মোহাম্মদ রহমান", "আয়েশা খাতুন",
        "আব্দুল করিম", "রাহেলা সুলতানা", "হাসান মাহমুদ", "নাজমা আক্তার",
        "ইব্রাহিম হোসেন", "সাবরিনা ইয়াসমিন", "মুস্তাফা আহমেদ", "রেহানা পারভীন",
        "আব্দুল্লাহ খান", "মরিয়ম বেগম", "রফিকুল ইসলাম", "তানিয়া আহমেদ",
        "শাহজাহান আলী", "নুসরাত জাহান", "মাহমুদুর রহমান", "ফারজানা আক্তার",
        "রাশেদ আহমেদ", "নাজনীন আক্তার", "শফিকুল ইসলাম", "সাবরিনা সুলতানা",
        "আব্দুল মালেক", "রেহানা বেগম", "মাহমুদ আলী", "ফাতেমা খাতুন",
        "ইব্রাহিম খান", "নাজমা সুলতানা", "হাসান আহমেদ", "আয়েশা বেগম"
    ]
    
    # Generate phone numbers
    phone_numbers = []
    for i in range(30):
        # Bangladesh format: +8801XXXXXXXXX
        prefix = random.choice(['71', '72', '73', '74', '75', '76', '77', '78', '79'])
        number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        phone_numbers.append(f"+8801{prefix}{number}")
    
    # Generate emails
    emails = []
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'yahoo.co.uk']
    for name in names:
        clean_name = name.replace(' ', '').lower()
        domain = random.choice(domains)
        emails.append(f"{clean_name}@{domain}")
    
    # Create data
    data = [
        ['Name', 'Phone Number', 'Email', 'City', 'Profession']
    ]
    
    cities = ['ঢাকা', 'চট্টগ্রাম', 'সিলেট', 'রাজশাহী', 'খুলনা', 'বরিশাল', 'রংপুর', 'ময়মনসিংহ']
    professions = ['ডাক্তার', 'ইঞ্জিনিয়ার', 'শিক্ষক', 'ব্যবসায়ী', 'কর্মচারী', 'ছাত্র', 'গৃহিণী', 'চাকরিজীবী']
    
    for i in range(30):
        data.append([
            names[i],
            phone_numbers[i],
            emails[i],
            cities[i % len(cities)],
            professions[i % len(professions)]
        ])
    
    # Save to CSV
    with open('sample_phone_numbers.xlsx', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    
    print("✅ Enhanced phone numbers saved to: sample_phone_numbers.xlsx")
    print(f"📱 Total phone numbers: {len(data)-1}")
    
    return data

if __name__ == "__main__":
    import random
    
    print("🏥 DIGITAL SEBE CHATBOT - Enhanced Data Generator")
    print("=" * 60)
    
    # Create enhanced medicine data
    create_excel_like_csv()
    print()
    
    # Create enhanced phone numbers
    create_enhanced_phone_numbers()
    print()
    
    print("🎉 সব enhanced data সফলভাবে তৈরি হয়েছে!")
    print("📁 ফাইলগুলো: medicine_data.xlsx, sample_phone_numbers.xlsx")
    print("\n💡 এই ফাইলগুলো আপনার chatbot এ ব্যবহার করুন!")
