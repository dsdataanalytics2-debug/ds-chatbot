#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 ChatGPT স্টাইলে উন্নত মেডিসিন চ্যাটবট
বিস্তারিত, সুন্দর এবং সহজবোধ্য উত্তর প্রদান করে
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import json
import re
from typing import List, Dict, Any, Tuple
import random
import time

# Page configuration
st.set_page_config(
    page_title="🤖 ChatGPT স্টাইল মেডিসিন চ্যাটবট",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for ChatGPT-style UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.2rem 1.5rem;
        border-radius: 18px 18px 4px 18px;
        margin-left: 20%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .bot-message {
        background: #f8f9fa;
        color: #2c3e50;
        padding: 1.5rem;
        border-radius: 18px 18px 18px 4px;
        margin-right: 20%;
        border: 1px solid #e9ecef;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 1px solid #2196f3;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
    }
    
    .medicine-card {
        background: white;
        border: 1px solid #e1e5e9;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

class ChatGPTStyleMedicineChatbot:
    def __init__(self):
        self.medicine_data = None
        self.conversation_history = []
        self.load_data()
        
    def load_data(self):
        """Load medicine data from Excel file"""
        try:
            self.medicine_data = pd.read_excel('medicine_data.xlsx')
            st.success("✅ মেডিসিন ডেটা সফলভাবে লোড হয়েছে!")
        except Exception as e:
            st.error(f"❌ ডেটা লোড করতে সমস্যা: {e}")
            # Create sample data if file not found
            self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample medicine data"""
        sample_data = {
            'Medicine Name': [
                'Dibedex 60 capsules', 'Paracetamol', 'Ibuprofen', 'Omeprazole', 'Cetirizine', 
                'Metformin', 'Amlodipine', 'Atorvastatin', 'Losartan', 'Pantoprazole', 'Montelukast'
            ],
            'Generic Name': [
                'Moringa Extract', 'Acetaminophen', 'Ibuprofen', 'Omeprazole', 'Cetirizine',
                'Metformin', 'Amlodipine', 'Atorvastatin', 'Losartan', 'Pantoprazole', 'Montelukast'
            ],
            'Uses': [
                'ডায়াবেটিস এর জন্য কার্যকর', 'জ্বর, ব্যথা, মাথাব্যথা', 'ব্যথা, প্রদাহ, জ্বর', 
                'পেটের আলসার, অ্যাসিডিটি', 'অ্যালার্জি, সর্দি, চুলকানি', 'টাইপ-২ ডায়াবেটিস নিয়ন্ত্রণ',
                'উচ্চ রক্তচাপ নিয়ন্ত্রণ', 'কোলেস্টেরল কমানো', 'উচ্চ রক্তচাপ নিয়ন্ত্রণ',
                'পেটের আলসার, অ্যাসিডিটি', 'অ্যাজমা, অ্যালার্জি প্রতিরোধ'
            ],
            'Side Effects': [
                'কোন পার্শ্বপ্রতিক্রিয়া নেই', 'মাথাব্যথা, বমি, পেটে ব্যথা', 'পেটে ব্যথা, বমি, মাথাব্যথা',
                'মাথাব্যথা, বমি, ডায়রিয়া', 'ঘুম, মাথাব্যথা, শুষ্ক মুখ',
                'বমি, ডায়রিয়া, পেটে ব্যথা', 'মাথাব্যথা, ফুলে যাওয়া, মাথা ঘোরা',
                'মাংসপেশিতে ব্যথা, বমি, মাথাব্যথা', 'মাথাব্যথা, মাথা ঘোরা, ক্লান্তি',
                'মাথাব্যথা, বমি, ডায়রিয়া', 'মাথাব্যথা, পেটে ব্যথা, বমি'
            ],
            'Dosage': [
                '১-২ ক্যাপসুল (দিনে ২ বার)', '৫০০-১০০০ মিগ্রা (৪-৬ ঘণ্টা পরপর)', 
                '২০০-৪০০ মিগ্রা (৬-৮ ঘণ্টা পরপর)', '২০ মিগ্রা (দিনে একবার)', '১০ মিগ্রা (দিনে একবার)',
                '৫০০-১০০০ মিগ্রা (দিনে ২-৩ বার)', '৫-১০ মিগ্রা (দিনে একবার)',
                '১০-৪০ মিগ্রা (দিনে একবার)', '৫০-১০০ মিগ্রা (দিনে একবার)',
                '৪০ মিগ্রা (দিনে একবার)', '১০ মিগ্রা (দিনে একবার)'
            ],
            'Price (৳)': [900, 5, 8, 15, 12, 20, 25, 30, 18, 22, 35]
        }
        self.medicine_data = pd.DataFrame(sample_data)
        st.info("📝 স্যাম্পল মেডিসিন ডেটা ব্যবহার করা হচ্ছে")
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text for better matching"""
        text = text.lower().strip()
        # Remove special characters but keep Bengali text
        text = re.sub(r'[^\w\s\u0980-\u09FF]', ' ', text)
        return text
    
    def find_medicine_info(self, query: str) -> List[Dict[str, Any]]:
        """Find medicine information based on query"""
        query = self.preprocess_text(query)
        results = []
        
        for _, row in self.medicine_data.iterrows():
            score = 0
            medicine_name = self.preprocess_text(str(row['Medicine Name']))
            generic_name = self.preprocess_text(str(row['Generic Name']))
            uses = self.preprocess_text(str(row['Uses']))
            
            # Check for exact matches
            if query in medicine_name or medicine_name in query:
                score += 10
            if query in generic_name or generic_name in query:
                score += 8
            if query in uses:
                score += 5
            
            # Check for partial matches
            query_words = query.split()
            for word in query_words:
                if word in medicine_name:
                    score += 2
                if word in generic_name:
                    score += 1.5
                if word in uses:
                    score += 1
            
            if score > 0:
                results.append({
                    'medicine': row.to_dict(),
                    'score': score
                })
        
        # Sort by score and return top results
        results.sort(key=lambda x: x['score'], reverse=True)
        return [r['medicine'] for r in results[:3]]
    
    def generate_detailed_response(self, query: str, medicines: List[Dict[str, Any]]) -> str:
        """Generate ChatGPT-style detailed response"""
        if not medicines:
            return self.generate_no_result_response(query)
        
        response = f"# 💊 আপনার প্রশ্নের বিস্তারিত উত্তর\n\n"
        response += f"**প্রশ্ন:** {query}\n\n"
        
        if len(medicines) == 1:
            med = medicines[0]
            response += self.generate_single_medicine_response(med)
        else:
            response += self.generate_multiple_medicines_response(medicines)
        
        response += self.generate_additional_info(query)
        return response
    
    def generate_single_medicine_response(self, medicine: Dict[str, Any]) -> str:
        """Generate detailed response for single medicine"""
        response = f"## 🎯 **{medicine['Medicine Name']}** সম্পর্কে বিস্তারিত তথ্য\n\n"
        
        response += f"### 📋 **মৌলিক তথ্য**\n"
        response += f"- **নাম:** {medicine['Medicine Name']}\n"
        response += f"- **জেনেরিক নাম:** {medicine['Generic Name']}\n"
        response += f"- **নিয়মিত মূল্য:** ৳{medicine['Price (৳)']}\n"
        response += f"- **কোম্পানির নাম:** {self.get_company_name(medicine)}\n"
        response += f"- **মেডিসিন গ্রুপ:** {self.get_medicine_group(medicine)}\n\n"
        
        response += f"### 💡 **ওষুধের কার্যকারিতা**\n"
        response += f"{medicine['Uses']}\n\n"
        
        response += f"### ⚠️ **পার্শ্বপ্রতিক্রিয়া**\n"
        response += f"{medicine['Side Effects']}\n\n"
        
        response += f"### 💊 **খাওয়ার নিয়ম**\n"
        response += f"**প্রাপ্তবয়স্ক ক্ষেত্রে:** {medicine['Dosage']}\n"
        response += f"**কিশোরদের ক্ষেত্রে:** {self.get_children_dosage(medicine)}\n\n"
        
        response += f"### 📖 **বিস্তারিত তথ্য**\n"
        response += f"**ওষুধের বিস্তারিত তথ্য:** {self.get_detailed_info(medicine)}\n\n"
        
        response += f"### 🔍 **বিস্তারিত বিশ্লেষণ**\n"
        response += self.generate_medicine_analysis(medicine)
        
        return response
    
    def generate_multiple_medicines_response(self, medicines: List[Dict[str, Any]]) -> str:
        """Generate response for multiple medicines"""
        response = "## 🔍 **আপনার প্রশ্নের সাথে সম্পর্কিত মেডিসিনসমূহ**\n\n"
        response += f"আপনার প্রশ্নের ভিত্তিতে **{len(medicines)}টি** মেডিসিন পাওয়া গেছে:\n\n"
        
        for i, medicine in enumerate(medicines, 1):
            response += f"### {i}. **{medicine['Medicine Name']}**\n"
            response += f"- **ব্যবহার:** {medicine['Uses']}\n"
            response += f"- **মূল্য:** ৳{medicine['Price (৳)']}\n"
            response += f"- **ডোজ:** {medicine['Dosage']}\n\n"
        
        response += "### 📊 **তুলনামূলক বিশ্লেষণ**\n"
        response += self.generate_comparison_analysis(medicines)
        
        return response
    
    def generate_medicine_analysis(self, medicine: Dict[str, Any]) -> str:
        """Generate detailed analysis of medicine"""
        analysis = ""
        
        # Price analysis
        price = medicine['Price (৳)']
        if price <= 10:
            analysis += f"💰 **মূল্য:** এই মেডিসিনটি **সাশ্রয়ী মূল্যে** পাওয়া যায় (৳{price})\n\n"
        elif price <= 20:
            analysis += f"💰 **মূল্য:** এই মেডিসিনটি **মাঝারি মূল্যে** পাওয়া যায় (৳{price})\n\n"
        else:
            analysis += f"💰 **মূল্য:** এই মেডিসিনটি **উচ্চ মূল্যে** পাওয়া যায় (৳{price})\n\n"
        
        # Usage analysis
        uses = medicine['Uses']
        if 'জ্বর' in uses or 'ব্যথা' in uses:
            analysis += "🌡️ **প্রকার:** এটি একটি **ব্যথানাশক এবং জ্বরনাশক** মেডিসিন\n\n"
        elif 'ডায়াবেটিস' in uses:
            analysis += "🩸 **প্রকার:** এটি একটি **ডায়াবেটিস নিয়ন্ত্রণকারী** মেডিসিন\n\n"
        elif 'রক্তচাপ' in uses:
            analysis += "❤️ **প্রকার:** এটি একটি **রক্তচাপ নিয়ন্ত্রণকারী** মেডিসিন\n\n"
        elif 'অ্যালার্জি' in uses:
            analysis += "🤧 **প্রকার:** এটি একটি **অ্যালার্জি প্রতিরোধকারী** মেডিসিন\n\n"
        
        return analysis
    
    def generate_comparison_analysis(self, medicines: List[Dict[str, Any]]) -> str:
        """Generate comparison analysis of multiple medicines"""
        analysis = ""
        
        # Price comparison
        prices = [med['Price (৳)'] for med in medicines]
        min_price = min(prices)
        max_price = max(prices)
        
        analysis += f"💰 **মূল্য তুলনা:**\n"
        analysis += f"- সর্বনিম্ন মূল্য: ৳{min_price}\n"
        analysis += f"- সর্বোচ্চ মূল্য: ৳{max_price}\n"
        analysis += f"- মূল্য পার্থক্য: ৳{max_price - min_price}\n\n"
        
        return analysis
    
    def get_company_name(self, medicine: Dict[str, Any]) -> str:
        """Get company name for medicine"""
        medicine_name = medicine['Medicine Name'].lower()
        
        # Sample company mappings
        company_mappings = {
            'dibedex': 'Index Laboratories (AyU) Ltd.',
            'paracetamol': 'Square Pharmaceuticals Ltd.',
            'ibuprofen': 'Beximco Pharmaceuticals Ltd.',
            'omeprazole': 'Incepta Pharmaceuticals Ltd.',
            'cetirizine': 'Renata Limited',
            'metformin': 'ACI Limited',
            'amlodipine': 'Drug International Limited',
            'atorvastatin': 'Opsonin Pharma Limited',
            'losartan': 'Healthcare Pharmaceuticals Ltd.',
            'pantoprazole': 'Eskayef Bangladesh Ltd.',
            'montelukast': 'Popular Pharmaceuticals Ltd.'
        }
        
        for key, company in company_mappings.items():
            if key in medicine_name:
                return company
        
        return "Index Laboratories (AyU) Ltd."
    
    def get_medicine_group(self, medicine: Dict[str, Any]) -> str:
        """Get medicine group"""
        uses = medicine['Uses'].lower()
        
        if 'ডায়াবেটিস' in uses:
            return "Ayurvedic"
        elif 'জ্বর' in uses or 'ব্যথা' in uses:
            return "Allopathic"
        elif 'অ্যালার্জি' in uses:
            return "Antihistamine"
        elif 'রক্তচাপ' in uses:
            return "Cardiovascular"
        elif 'পেট' in uses or 'অ্যাসিড' in uses:
            return "Gastrointestinal"
        else:
            return "General"
    
    def get_children_dosage(self, medicine: Dict[str, Any]) -> str:
        """Get children dosage information"""
        medicine_name = medicine['Medicine Name'].lower()
        uses = medicine['Uses'].lower()
        
        if 'dibedex' in medicine_name:
            return "চিকিৎসকের পরামর্শ অনুযায়ী"
        elif 'paracetamol' in medicine_name:
            return "১০-১৫ মিগ্রা/কেজি (৪-৬ ঘণ্টা পরপর)"
        elif 'ibuprofen' in medicine_name:
            return "৫-১০ মিগ্রা/কেজি (৬-৮ ঘণ্টা পরপর)"
        elif 'cetirizine' in medicine_name:
            return "৫ মিগ্রা (দিনে একবার)"
        elif 'ডায়াবেটিস' in uses:
            return "চিকিৎসকের পরামর্শ অনুযায়ী"
        else:
            return "চিকিৎসকের পরামর্শ অনুযায়ী"
    
    def get_detailed_info(self, medicine: Dict[str, Any]) -> str:
        """Get detailed information about medicine"""
        medicine_name = medicine['Medicine Name'].lower()
        uses = medicine['Uses'].lower()
        
        if 'dibedex' in medicine_name:
            return "যা মূলত সজনে পাতার নির্যাস থেকে তৈরি, শরীরের জন্য বেশ কিছু উপকারী উপাদান রয়েছে। ডায়াবেটিস নিয়ন্ত্রণে সহায়ক এবং প্রাকৃতিক উপাদান হওয়ায় পার্শ্বপ্রতিক্রিয়া নেই।"
        elif 'paracetamol' in medicine_name:
            return "যা মূলত অ্যাসিটামিনোফেন থেকে তৈরি, শরীরের জ্বর এবং ব্যথা কমাতে কার্যকর। এটি লিভারে বিপাক হয় এবং নিরাপদে ব্যবহার করা যায়।"
        elif 'ibuprofen' in medicine_name:
            return "যা মূলত নন-স্টেরয়েডাল অ্যান্টি-ইনফ্ল্যামেটরি ড্রাগ (NSAID), প্রদাহ এবং ব্যথা কমাতে কার্যকর। পেটের সমস্যা হতে পারে।"
        elif 'omeprazole' in medicine_name:
            return "যা মূলত প্রোটন পাম্প ইনহিবিটর, পেটের অ্যাসিড কমাতে কার্যকর। আলসার এবং অ্যাসিডিটি চিকিৎসায় ব্যবহৃত হয়।"
        elif 'cetirizine' in medicine_name:
            return "যা মূলত অ্যান্টিহিস্টামিন, অ্যালার্জি প্রতিক্রিয়া কমাতে কার্যকর। সর্দি, চুলকানি এবং অ্যালার্জিক রাইনাইটিসে ব্যবহৃত হয়।"
        elif 'metformin' in medicine_name:
            return "যা মূলত বিগুয়ানাইড শ্রেণীর ডায়াবেটিস মেডিসিন, রক্তে শর্করা নিয়ন্ত্রণে কার্যকর। লিভার এবং কিডনির উপর কাজ করে।"
        elif 'ডায়াবেটিস' in uses:
            return "যা মূলত সজনে পাতার নির্যাস থেকে তৈরি, শরীরের জন্য বেশ কিছু উপকারী উপাদান রয়েছে। ডায়াবেটিস নিয়ন্ত্রণে সহায়ক।"
        elif 'রক্তচাপ' in uses:
            return "যা মূলত রক্তনালী প্রসারণকারী, উচ্চ রক্তচাপ নিয়ন্ত্রণে কার্যকর। হার্টের উপর কাজ করে রক্তচাপ কমায়।"
        elif 'অ্যালার্জি' in uses:
            return "যা মূলত অ্যান্টিহিস্টামিন, অ্যালার্জি প্রতিক্রিয়া কমাতে কার্যকর। ইমিউন সিস্টেমের উপর কাজ করে।"
        else:
            return "যা মূলত প্রাকৃতিক উপাদান থেকে তৈরি, শরীরের বিভিন্ন সমস্যা সমাধানে কার্যকর। নিরাপদ এবং পার্শ্বপ্রতিক্রিয়া কম।"
    
    def generate_no_result_response(self, query: str) -> str:
        """Generate response when no medicine found"""
        response = f"# 🤔 আপনার প্রশ্নের উত্তর\n\n"
        response += f"**প্রশ্ন:** {query}\n\n"
        response += "## ❌ **কোন মেডিসিন পাওয়া যায়নি**\n\n"
        response += "দুঃখিত, আপনার প্রশ্নের সাথে সম্পর্কিত কোন মেডিসিন আমাদের ডেটাবেসে নেই।\n\n"
        response += "### 💡 **পরামর্শ:**\n"
        response += "1. **ভিন্ন শব্দে** প্রশ্ন করুন\n"
        response += "2. **মেডিসিনের জেনেরিক নাম** ব্যবহার করুন\n"
        response += "3. **রোগের লক্ষণ** উল্লেখ করুন\n"
        response += "4. **চিকিৎসকের পরামর্শ** নিন\n\n"
        
        return response
    
    def generate_additional_info(self, query: str) -> str:
        """Generate additional helpful information"""
        info = "\n---\n\n"
        info += "## 📚 **অতিরিক্ত তথ্য**\n\n"
        
        info += "### ⚠️ **সতর্কতা:**\n"
        info += "- এই তথ্য শুধুমাত্র **শিক্ষামূলক উদ্দেশ্যে**\n"
        info += "- **চিকিৎসকের পরামর্শ** ছাড়া মেডিসিন খাবেন না\n"
        info += "- **অ্যালার্জি** থাকলে সতর্কতা অবলম্বন করুন\n\n"
        
        info += "### 📞 **জরুরি যোগাযোগ:**\n"
        info += "- **জাতীয় জরুরি সেবা:** ৯৯৯\n"
        info += "- **স্বাস্থ্য বাতায়ন:** ১৬২৬৩\n"
        
        return info
    
    def display_message(self, message: str, is_user: bool = False):
        """Display message with proper styling"""
        if is_user:
            st.markdown(f"""
            <div class="user-message">
                {message}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bot-message">
                {message}
            </div>
            """, unsafe_allow_html=True)
    
    def run(self):
        """Run the chatbot"""
        # Header
        st.markdown('<h1 class="main-header">🤖 ChatGPT স্টাইল মেডিসিন চ্যাটবট</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 3rem;">আপনার স্বাস্থ্য সম্পর্কিত যেকোন প্রশ্ন করুন - বিস্তারিত এবং সহজবোধ্য উত্তর পাবেন</p>', unsafe_allow_html=True)
        
        # Sidebar
        with st.sidebar:
            st.header("⚙️ সেটিংস")
            
            # Clear chat button
            if st.button("🗑️ চ্যাট মুছুন"):
                st.session_state.messages = []
                st.rerun()
            
            st.markdown("---")
            
            # Statistics
            st.header("📊 পরিসংখ্যান")
            if 'messages' in st.session_state:
                st.metric("মোট বার্তা", len(st.session_state.messages))
            
            st.markdown("---")
            
            # About
            st.header("ℹ️ সম্পর্কে")
            st.info("""
            এই চ্যাটবট AI প্রযুক্তি ব্যবহার করে আপনার স্বাস্থ্য সম্পর্কিত প্রশ্নের উত্তর দেয়।
            
            **বৈশিষ্ট্যসমূহ:**
            - 🤖 AI চালিত উত্তর
            - 💊 মেডিসিন তথ্য
            - 📊 বিস্তারিত বিশ্লেষণ
            - 🎨 সুন্দর UI
            """)
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for message in st.session_state.messages:
            self.display_message(message["content"], message["role"] == "user")
        
        # Chat input
        user_input = st.text_input(
            "💬 আপনার প্রশ্ন লিখুন...",
            key="user_input",
            placeholder="যেমন: জ্বরের জন্য কি মেডিসিন খাব?"
        )
        
        # Send button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            send_button = st.button("🚀 পাঠান", use_container_width=True)
        
        # Process user input
        if send_button and user_input:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Show typing indicator
            with st.spinner("🤖 AI উত্তর তৈরি করছে..."):
                time.sleep(1)  # Simulate processing time
            
            # Generate response
            medicines = self.find_medicine_info(user_input)
            response = self.generate_detailed_response(user_input, medicines)
            
            # Add bot response
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Clear input
            st.rerun()

def main():
    """Main function"""
    chatbot = ChatGPTStyleMedicineChatbot()
    chatbot.run()

if __name__ == "__main__":
    main()
