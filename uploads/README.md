# 📁 UPLOADS FOLDER STRUCTURE

এই folder এ সব আপলোড করা ফাইল organized ভাবে সেভ হয়।

## 📂 Folder Structure

### 📊 `data_files/`
- **Excel (.xlsx)** এবং **CSV (.csv)** ফাইল
- মেডিকেল ডেটা, ওষুধের তালিকা ইত্যাদি
- ফাইল নাম: `YYYYMMDD_HHMMSS_original_filename.xlsx`

### 🔑 `api_keys/`
- **Text (.txt)**, **Environment (.env)**, **JSON (.json)**, **YAML (.yml)** ফাইল
- WhatsApp API, OpenAI API ইত্যাদি কী
- ফাইল নাম: `YYYYMMDD_HHMMSS_original_filename.txt`

### 📚 `documents/`
- **PDF (.pdf)** এবং **Word (.docx)** ফাইল
- মেডিকেল ডকুমেন্ট, গবেষণা পত্র ইত্যাদি
- ফাইল নাম: `YYYYMMDD_HHMMSS_original_filename.pdf`

### 📞 `phone_numbers/`
- **Excel (.xlsx)** এবং **CSV (.csv)** ফাইল
- WhatsApp Marketing এর জন্য ফোন নম্বর তালিকা
- ফাইল নাম: `YYYYMMDD_HHMMSS_original_filename.xlsx`

## 💾 File Naming Convention

সব ফাইলের নাম timestamp সহ unique হয়:
- **Format:** `YYYYMMDD_HHMMSS_original_filename.extension`
- **Example:** `20250822_162530_medicine_list.xlsx`

## 🗑️ File Management

- ফাইলগুলো **permanently** সেভ হয়
- Chatbot এ **delete** বোতাম দিয়ে ফাইল মুছা যায়
- ফাইল আপলোড করার পর **file path** দেখানো হয়

## 🔒 Security Features

- API key ফাইলগুলো **masked** ভাবে দেখানো হয়
- Sensitive information (API_KEY, SECRET) **hidden** থাকে
- ফাইল access শুধু chatbot এর মাধ্যমে

## 📱 Usage

1. **ফাইল আপলোড করুন** chatbot এ
2. **ফাইল সেভ হবে** appropriate folder এ
3. **ফাইল path দেখুন** success message এ
4. **ফাইল মুছুন** delete বোতাম দিয়ে

---
*Created by DIGITAL SEBE CHATBOT - Advanced Medical AI Assistant*
