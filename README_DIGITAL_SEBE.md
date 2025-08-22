# 🏥 DIGITAL SEBE CHATBOT

## 📋 বিবরণ
**DIGITAL SEBE CHATBOT** একটি উন্নত মেডিকেল AI সহকারী যা সব ধরনের স্বাস্থ্য সম্পর্কিত প্রশ্নের উত্তর দিতে পারে। Google এর মত সুন্দর সার্চ বার, WhatsApp Marketing, এবং ফাইল আপলোড সহ সব feature রয়েছে।

## ✨ প্রধান বৈশিষ্ট্য

### 🔍 স্মার্ট অনুসন্ধান
- Google এর মত সুন্দর সার্চ বার
- বাঙালি ভাষায় অনুসন্ধান
- জনপ্রিয় অনুসন্ধান সাজেশন
- সাদৃশ্য স্কোর সহ ফলাফল

### 💬 AI চ্যাট
- ChatGPT এর মত বুদ্ধিমান কথোপকথন
- চ্যাট ইতিহাস সংরক্ষণ
- স্বয়ংক্রিয় উত্তর জেনারেশন

### 📱 WhatsApp Marketing
- একসাথে অনেক নম্বরে মেসেজ পাঠানো
- Excel/CSV ফাইল থেকে ফোন নম্বর লোড
- স্বয়ংক্রিয় মেসেজ ফরম্যাটিং

### 📁 ফাইল আপলোড
- **Excel (.xlsx)**: মেডিকেল ডেটা
- **CSV (.csv)**: ফোন নম্বর তালিকা
- **PDF (.pdf)**: মেডিকেল ডকুমেন্ট
- **Word (.docx)**: চিকিৎসা নির্দেশিকা

### 🎨 সুন্দর UI/UX
- Modern gradient design
- Responsive layout
- Interactive elements
- Professional styling

## 🚀 ইনস্টলেশন

### প্রয়োজনীয়তা
- Python 3.8+
- Windows 10/11

### ধাপ 1: ফাইল ডাউনলোড
```bash
# সব ফাইল ডাউনলোড করুন
git clone <repository-url>
cd medicine-Chatbot
```

### ধাপ 2: প্যাকেজ ইনস্টল
```bash
# প্রয়োজনীয় প্যাকেজ ইনস্টল করুন
pip install -r requirements_digital_sebe.txt
```

### ধাপ 3: চ্যাটবট চালু করুন
```bash
# Python দিয়ে চালান
python run_digital_sebe.py

# অথবা Windows batch file দিয়ে
run_digital_sebe.bat
```

## 📖 ব্যবহার পদ্ধতি

### 🔍 অনুসন্ধান
1. **হোম পেজে** সার্চ বারে আপনার প্রশ্ন লিখুন
2. **জনপ্রিয় অনুসন্ধান** বোতামে ক্লিক করুন
3. **অথবা** অনুসন্ধান পেজে গিয়ে advanced search করুন

### 💬 চ্যাট
1. **চ্যাট পেজে** যান
2. আপনার প্রশ্ন লিখুন
3. AI আপনার প্রশ্নের উত্তর দেবে

### 📱 WhatsApp Marketing
1. **WhatsApp Marketing পেজে** যান
2. Excel/CSV ফাইলে ফোন নম্বর রাখুন
3. ফাইল আপলোড করুন
4. মেসেজ লিখুন
5. **মেসেজ পাঠান** বোতামে ক্লিক করুন

### 📁 ফাইল আপলোড
1. **ফাইল আপলোড পেজে** যান
2. সমর্থিত ফরম্যাটের ফাইল নির্বাচন করুন
3. ফাইল আপলোড করুন
4. ফাইলের বিষয়বস্তু দেখুন

## 🎯 জনপ্রিয় অনুসন্ধান

- **ডায়াবেটিস** - লক্ষণ, চিকিৎসা, খাদ্যতালিকা
- **হৃদরোগ** - কারণ, প্রতিরোধ, ওষুধ
- **লিভারের সমস্যা** - লক্ষণ, চিকিৎসা, খাবার
- **কিডনির সমস্যা** - রোগ, চিকিৎসা, খাদ্যতালিকা
- **গ্যাস্ট্রিক** - কারণ, প্রতিকার, ওষুধ
- **যৌন সমস্যা ও টেস্টোস্টেরন** - কারণ, চিকিৎসা
- **হাঁপানি** - লক্ষণ, প্রতিরোধ, ওষুধ

## 🔧 কনফিগারেশন

### Environment Variables
`.env` ফাইলে নিচের ভেরিয়েবলগুলো রাখুন:
```env
# WhatsApp API keys (যদি প্রয়োজন হয়)
WHATSAPP_API_KEY=your_api_key
WHATSAPP_API_SECRET=your_api_secret

# Database configuration
DATABASE_URL=your_database_url
```

### Customization
- **Logo**: `chatbot pic.jpg` ফাইলটি পরিবর্তন করুন
- **Colors**: CSS variables পরিবর্তন করুন
- **Language**: বাঙালি টেক্সট পরিবর্তন করুন

## 📊 ডেটা স্ট্রাকচার

### Excel ফাইল ফরম্যাট
```csv
Medicine Name,Description,Symptoms,Treatment,Dosage,Price
Paracetamol,জ্বর ও ব্যথা কমায়,জ্বর,ব্যথা,500mg,2.50
```

### ফোন নম্বর ফাইল ফরম্যাট
```csv
Name,Phone Number,Email
John Doe,+8801712345678,john@example.com
Jane Smith,+8801812345678,jane@example.com
```

## 🐛 সমস্যা সমাধান

### সাধারণ সমস্যা
1. **প্যাকেজ ইনস্টল না হওয়া**
   ```bash
   pip install --upgrade pip
   pip install -r requirements_digital_sebe.txt
   ```

2. **Streamlit চালু না হওয়া**
   ```bash
   streamlit --version
   streamlit run digital_sebe_chatbot.py
   ```

3. **WhatsApp মেসেজ না পাঠানো**
   - ইন্টারনেট সংযোগ চেক করুন
   - ফোন নম্বর ফরম্যাট চেক করুন
   - pywhatkit ইনস্টল করুন

### Error Messages
- **"ডেটা লোড করতে সমস্যা"**: Excel ফাইল চেক করুন
- **"ফাইল আপলোড করতে সমস্যা"**: ফাইল ফরম্যাট চেক করুন
- **"অনুসন্ধানে সমস্যা"**: ইন্টারনেট সংযোগ চেক করুন

## 📱 WhatsApp Marketing Tips

### সফল মেসেজের জন্য
1. **সংক্ষিপ্ত মেসেজ** লিখুন (160 characters)
2. **স্পষ্ট ভাষা** ব্যবহার করুন
3. **Call-to-action** যোগ করুন
4. **সময়** বিবেচনা করুন

### ফোন নম্বর ফরম্যাট
- **বাংলাদেশ**: +8801712345678
- **ভারত**: +911234567890
- **যুক্তরাষ্ট্র**: +15551234567

## 🔒 নিরাপত্তা

### ডেটা সুরক্ষা
- আপলোড করা ফাইল স্থানীয়ভাবে সংরক্ষিত
- ব্যক্তিগত তথ্য শেয়ার করা হয় না
- SSL এনক্রিপশন সমর্থিত

### ব্যবহারকারী গোপনীয়তা
- চ্যাট ইতিহাস স্থানীয়ভাবে সংরক্ষিত
- সার্চ ইতিহাস সংরক্ষিত হয় না
- ব্যক্তিগত তথ্য সংগ্রহ করা হয় না

## 📞 সহায়তা

### যোগাযোগ
- **ইমেইল**: support@digitalsebe.com
- **ফোন**: +8801712345678
- **ওয়েবসাইট**: https://digitalsebe.com

### ডকুমেন্টেশন
- **User Guide**: [PDF Download]
- **API Documentation**: [Link]
- **Video Tutorials**: [YouTube Channel]

## 🚀 ভবিষ্যত পরিকল্পনা

### আসন্ন ফিচার
- [ ] Voice Search
- [ ] Image Recognition
- [ ] Multi-language Support
- [ ] Mobile App
- [ ] AI Voice Assistant
- [ ] Integration with Hospital Systems

### উন্নতি
- [ ] Better Bengali NLP
- [ ] Advanced Search Algorithms
- [ ] Real-time Updates
- [ ] Offline Mode
- [ ] Data Analytics Dashboard

## 📄 লাইসেন্স

এই প্রজেক্টটি **MIT License** এর অধীনে প্রকাশিত।

## 🙏 স্বীকৃতি

- **Streamlit** - Web App Framework
- **scikit-learn** - Machine Learning
- **NLTK** - Natural Language Processing
- **pywhatkit** - WhatsApp Integration
- **Plotly** - Data Visualization

---

**🏥 DIGITAL SEBE CHATBOT** - আপনার বিশ্বস্ত মেডিকেল AI সহকারী

*Made with ❤️ in Bangladesh*
