#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 সুপার উন্নত AI মেডিসিন চ্যাটবট
ChatGPT/Cursor AI স্টাইলে সর্বোচ্চ মানের বিস্তারিত এবং সুন্দর উত্তর প্রদান করে
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import json
import re
from typing import List, Dict, Any
import random

# Page configuration
st.set_page_config(
    page_title="🚀 সুপার উন্নত AI মেডিসিন চ্যাটবট",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .chat-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    .info-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

class SuperAdvancedMedicineChatbot:
    def __init__(self):
        self.medicine_data = None
        self.conversation_history = []
        self.search_analytics = {}
        self.load_data()
        
    def load_data(self):
        """Load medicine data with enhanced error handling"""
        try:
            self.medicine_data = pd.read_excel('medicine_data.xlsx')
            self.medicine_data = self.medicine_data.fillna('')
            st.success("✅ মেডিসিন ডেটা সফলভাবে লোড হয়েছে!")
            st.info(f"📊 **ডেটা পরিসংখ্যান:** {len(self.medicine_data)}টি মেডিসিন লোড হয়েছে")
        except Exception as e:
            st.error(f"❌ ডেটা লোড করতে সমস্যা: {e}")
            self.medicine_data = pd.DataFrame()
    
    def preprocess_text(self, text: str) -> str:
        """Enhanced text preprocessing"""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s\u0980-\u09FF]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def find_medicine_info(self, query: str) -> Dict[str, Any]:
        """Enhanced medicine search with multiple strategies"""
        if self.medicine_data.empty:
            return {"found": False, "message": "ডেটা পাওয়া যায়নি"}
        
        query_processed = self.preprocess_text(query)
        self.search_analytics[query_processed] = self.search_analytics.get(query_processed, 0) + 1
        
        matches = []
        
        # Multiple search strategies
        for idx, row in self.medicine_data.iterrows():
            medicine_name = str(row.get('medicine_name', '')).lower()
            generic_name = str(row.get('generic_name', '')).lower()
            indication = str(row.get('indication', '')).lower()
            
            if (query_processed in medicine_name or 
                query_processed in generic_name or 
                query_processed in indication):
                matches.append(row.to_dict())
        
        # Remove duplicates
        unique_matches = []
        seen = set()
        for match in matches:
            medicine_id = match.get('medicine_name', '')
            if medicine_id not in seen:
                seen.add(medicine_id)
                unique_matches.append(match)
        
        if unique_matches:
            return {"found": True, "data": unique_matches[:5]}
        else:
            return {"found": False, "message": "কোন মেডিসিন পাওয়া যায়নি"}
    
    def generate_super_detailed_response(self, query: str, medicine_info: Dict[str, Any]) -> str:
        """Generate super detailed, ChatGPT-style response"""
        
        if not medicine_info["found"]:
            return self.generate_enhanced_not_found_response(query)
        
        medicines = medicine_info["data"]
        response_parts = []
        
        # Enhanced header
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response_parts.append("## 🚀 **আপনার প্রশ্নের সর্বোচ্চ মানের উত্তর**")
        response_parts.append(f"**⏰ সময়:** {current_time}")
        response_parts.append(f"**🔍 প্রশ্ন:** {query}")
        response_parts.append("")
        
        # Summary
        if len(medicines) == 1:
            response_parts.append("### 📋 **মেডিসিনের বিস্তারিত তথ্য**")
        else:
            response_parts.append(f"### 📋 **পাওয়া গেছে {len(medicines)}টি মেডিসিন**")
        response_parts.append("")
        
        # Detailed information for each medicine
        for i, medicine in enumerate(medicines, 1):
            response_parts.append(f"#### 💊 **{i}. {medicine.get('medicine_name', 'নাম জানা নেই')}**")
            response_parts.append("")
            
            # Basic information
            basic_info = []
            if medicine.get('generic_name'):
                basic_info.append(f"**জেনেরিক নাম:** {medicine['generic_name']}")
            if medicine.get('strength'):
                basic_info.append(f"**শক্তি:** {medicine['strength']}")
            if medicine.get('dosage_form'):
                basic_info.append(f"**ডোজ ফর্ম:** {medicine['dosage_form']}")
            
            if basic_info:
                response_parts.append("**📊 মৌলিক তথ্য:**")
                response_parts.extend(basic_info)
                response_parts.append("")
            
            # Detailed sections
            sections = [
                ('indication', '📝 **ব্যবহারের কারণ:**'),
                ('dosage', '💊 **ডোজ নির্দেশনা:**'),
                ('side_effects', '⚠️ **পার্শ্ব প্রতিক্রিয়া:**'),
                ('precautions', '🚨 **সতর্কতা:**'),
                ('contraindications', '❌ **নিষিদ্ধ:**')
            ]
            
            for field, title in sections:
                if medicine.get(field):
                    response_parts.append(title)
                    response_parts.append(f"> {medicine[field]}")
                    response_parts.append("")
            
            response_parts.append("---")
            response_parts.append("")
        
        # Enhanced additional information
        response_parts.append("### 💡 **গুরুত্বপূর্ণ পরামর্শ এবং সতর্কতা**")
        response_parts.append("")
        
        advice_points = [
            "🔸 **চিকিৎসকের পরামর্শ নিন:** এই তথ্যগুলো শুধুমাত্র শিক্ষামূলক উদ্দেশ্যে।",
            "🔸 **ডোজ অনুসরণ করুন:** চিকিৎসকের নির্দেশিত ডোজ অনুসরণ করুন।",
            "🔸 **পার্শ্ব প্রতিক্রিয়া লক্ষ্য করুন:** কোন অস্বাভাবিক লক্ষণ দেখা দিলে চিকিৎসকের সাথে যোগাযোগ করুন।",
            "🔸 **নিয়মিত চেকআপ:** নিয়মিত চিকিৎসকের কাছে যান।",
            "🔸 **অন্যান্য মেডিসিনের সাথে মিথস্ক্রিয়া:** অন্য মেডিসিন খাওয়ার আগে চিকিৎসকের পরামর্শ নিন।"
        ]
        
        for point in advice_points:
            response_parts.append(point)
            response_parts.append("")
        
        # Emergency contact
        response_parts.append("### 🆘 **জরুরি যোগাযোগ**")
        response_parts.append("")
        response_parts.append("**📞 জরুরি সেবা:** ৯৯৯")
        response_parts.append("**🏥 নিকটস্থ হাসপাতাল:** আপনার এলাকার হাসপাতালে যোগাযোগ করুন")
        
        return "\n".join(response_parts)
    
    def generate_enhanced_not_found_response(self, query: str) -> str:
        """Generate enhanced response when medicine not found"""
        response = f"""
## 🔍 **আপনার প্রশ্নের উত্তর**

**⏰ সময়:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**🔍 প্রশ্ন:** {query}

### ❌ **মেডিসিন পাওয়া যায়নি**

দুঃখিত, আপনার অনুসন্ধানকৃত মেডিসিন আমাদের ডেটাবেসে পাওয়া যায়নি।

### 💡 **সাহায্যকারী পরামর্শ**

🔸 **সঠিক বানান:** মেডিসিনের নাম সঠিকভাবে লিখেছেন কিনা চেক করুন
🔸 **জেনেরিক নাম:** মেডিসিনের জেনেরিক নাম দিয়ে অনুসন্ধান করুন
🔸 **ব্যবহারের কারণ:** লক্ষণ বা রোগের নাম দিয়ে অনুসন্ধান করুন
🔸 **চিকিৎসকের পরামর্শ:** আপনার চিকিৎসকের সাথে যোগাযোগ করুন

### 🔍 **অনুসন্ধানের টিপস**

**সঠিক নাম লিখুন:**
- Paracetamol (প্যারাসিটামল)
- Aspirin (অ্যাসপিরিন)
- Ibuprofen (আইবুপ্রোফেন)

**লক্ষণ অনুসন্ধান:**
- জ্বর
- ব্যথা
- মাথাব্যথা
- কাশি

### 📞 **জরুরি যোগাযোগ**

🆘 **জরুরি সেবা:** ৯৯৯
🏥 **নিকটস্থ হাসপাতাল:** আপনার এলাকার হাসপাতালে যোগাযোগ করুন
        """
        return response
    
    def generate_enhanced_health_advice(self, query: str) -> str:
        """Generate enhanced health advice"""
        advice_templates = [
            f"""
## 🏥 **সাধারণ স্বাস্থ্য পরামর্শ**

**⏰ সময়:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**🔍 প্রশ্ন:** {query}

### 💪 **সুস্থ থাকার মূল নীতি**

#### 🥗 **পুষ্টিকর খাবার**
- **সবুজ শাকসবজি:** প্রতিদিন অন্তত ৩-৪ পরিবেশন
- **ফলমূল:** ভিটামিন সি সমৃদ্ধ ফল বেশি খান
- **প্রোটিন:** মাছ, মাংস, ডিম, দুধ নিয়মিত খান
- **জল:** দিনে ৮-১০ গ্লাস পানি পান করুন

#### 🏃‍♂️ **নিয়মিত ব্যায়াম**
- **কার্ডিও:** সপ্তাহে ৩-৪ দিন ৩০ মিনিট
- **শক্তি প্রশিক্ষণ:** সপ্তাহে ২-৩ দিন
- **যোগব্যায়াম:** মানসিক শান্তির জন্য
- **হাঁটা:** প্রতিদিন ১০,০০০ পদক্ষেপ

#### 😴 **পর্যাপ্ত বিশ্রাম**
- **ঘুম:** রাতে ৭-৯ ঘন্টা ঘুমান
- **নিয়মিত সময়:** প্রতিদিন একই সময়ে ঘুমান
- **শান্ত পরিবেশ:** ঘুমের জন্য উপযুক্ত পরিবেশ তৈরি করুন

### 🚨 **সতর্কতা**
- ধূমপান এবং মদ্যপান ত্যাগ করুন
- নিয়মিত চেকআপ করুন
- চাপ কম রাখুন
            """,
            
            f"""
## 💪 **স্বাস্থ্যকর জীবনযাপন গাইড**

**⏰ সময়:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**🔍 প্রশ্ন:** {query}

### 🎯 **লক্ষ্য নির্ধারণ**

#### 📊 **স্বাস্থ্য লক্ষ্য**
- **ওজন নিয়ন্ত্রণ:** স্বাস্থ্যকর BMI বজায় রাখুন
- **রক্তচাপ:** নিয়মিত রক্তচাপ চেক করুন
- **রক্তে শর্করা:** ডায়াবেটিস ঝুঁকি কম রাখুন
- **কোলেস্টেরল:** স্বাস্থ্যকর কোলেস্টেরল মাত্রা

#### 🥗 **খাদ্যাভ্যাস**
- **সকালের নাস্তা:** কখনও বাদ দিবেন না
- **মাঝারি খাবার:** দিনে ৩ বার প্রধান খাবার
- **স্ন্যাকস:** স্বাস্থ্যকর স্ন্যাকস খান
- **জল:** পর্যাপ্ত পানি পান করুন

#### 🏃‍♂️ **শারীরিক কার্যকলাপ**
- **নিয়মিত ব্যায়াম:** সপ্তাহে ১৫০ মিনিট
- **শক্তি প্রশিক্ষণ:** সপ্তাহে ২ দিন
- **নমনীয়তা:** স্ট্রেচিং এবং যোগব্যায়াম
- **সক্রিয় জীবনযাপন:** বেশি হাঁটা, কম বসা

### 🧘‍♀️ **মানসিক সুস্থতা**

#### 😊 **ইতিবাচক মনোভাব**
- **কৃতজ্ঞতা:** প্রতিদিন কৃতজ্ঞতা প্রকাশ করুন
- **আত্মবিশ্বাস:** নিজের উপর বিশ্বাস রাখুন
- **সহনশীলতা:** অন্যদের প্রতি সহনশীল হন
- **আশাবাদ:** ভবিষ্যতের প্রতি আশাবাদী হন
            """
        ]
        
        return random.choice(advice_templates)
    
    def process_query(self, query: str) -> str:
        """Process user query and generate enhanced response"""
        self.conversation_history.append({
            "user": query, 
            "timestamp": datetime.now(),
            "query_type": "medicine" if not self.is_health_question(query) else "health"
        })
        
        if self.is_health_question(query):
            return self.generate_enhanced_health_advice(query)
        
        medicine_info = self.find_medicine_info(query)
        return self.generate_super_detailed_response(query, medicine_info)
    
    def is_health_question(self, query: str) -> bool:
        """Check if query is about general health"""
        health_keywords = [
            'স্বাস্থ্য', 'পরামর্শ', 'উপদেশ', 'জীবনযাপন', 'ব্যায়াম', 
            'খাবার', 'ঘুম', 'সুস্থ', 'ফিটনেস', 'পুষ্টি', 'ডায়েট'
        ]
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in health_keywords)
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get chatbot analytics"""
        return {
            "total_queries": len(self.conversation_history),
            "medicine_queries": len([q for q in self.conversation_history if q.get("query_type") == "medicine"]),
            "health_queries": len([q for q in self.conversation_history if q.get("query_type") == "health"]),
            "popular_searches": dict(sorted(self.search_analytics.items(), key=lambda x: x[1], reverse=True)[:5])
        }

def main():
    """Main application with enhanced features"""
    
    # Enhanced header
    st.markdown('<h1 class="main-header">🚀 সুপার উন্নত AI মেডিসিন চ্যাটবট</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">ChatGPT/Cursor AI স্টাইলে সর্বোচ্চ মানের বিস্তারিত এবং সুন্দর উত্তর প্রদান করে</p>', unsafe_allow_html=True)
    
    # Enhanced sidebar
    with st.sidebar:
        st.markdown("## 🎛️ **নিয়ন্ত্রণ প্যানেল**")
        
        # About section
        with st.expander("ℹ️ **সম্পর্কে**", expanded=True):
            st.info("""
            **🚀 সুপার উন্নত AI চ্যাটবট**
            
            **✨ বৈশিষ্ট্যসমূহ:**
            - 🔍 স্মার্ট অনুসন্ধান
            - 📋 বিস্তারিত তথ্য
            - 💡 সহায়ক পরামর্শ
            - 🎨 সুন্দর UI
            - 📊 পরিসংখ্যান
            - 🔄 চ্যাট ইতিহাস
            """)
        
        # Statistics
        if 'chatbot' in st.session_state:
            analytics = st.session_state.chatbot.get_analytics()
            
            st.markdown("### 📊 **পরিসংখ্যান**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("মোট প্রশ্ন", analytics["total_queries"])
                st.metric("মেডিসিন প্রশ্ন", analytics["medicine_queries"])
            
            with col2:
                st.metric("স্বাস্থ্য প্রশ্ন", analytics["health_queries"])
            
            # Popular searches
            if analytics["popular_searches"]:
                st.markdown("### 🔥 **জনপ্রিয় অনুসন্ধান**")
                for search, count in analytics["popular_searches"].items():
                    st.text(f"• {search}: {count} বার")
        
        # Clear chat button
        if st.button("🗑️ চ্যাট মুছুন", use_container_width=True):
            if 'chatbot' in st.session_state:
                st.session_state.chatbot.conversation_history = []
                st.session_state.chatbot.search_analytics.clear()
            st.rerun()
    
    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = SuperAdvancedMedicineChatbot()
    
    # Main chat interface
    st.markdown("## 💬 **চ্যাট করুন**")
    
    # Enhanced chat input
    user_input = st.text_input(
        "আপনার প্রশ্ন লিখুন:",
        placeholder="যেমন: Paracetamol, Aspirin, জ্বরের মেডিসিন, বা সাধারণ স্বাস্থ্য পরামর্শ..."
    )
    
    # Send button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        send_button = st.button("🚀 উত্তর পান", use_container_width=True)
    
    # Process query
    if send_button and user_input:
        with st.spinner("🤖 সর্বোচ্চ মানের উত্তর তৈরি করা হচ্ছে..."):
            response = st.session_state.chatbot.process_query(user_input)
            
            # Display response in enhanced container
            st.markdown("---")
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            st.markdown(response, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add to chat history
            st.session_state.chatbot.conversation_history.append({
                "bot": response, 
                "timestamp": datetime.now()
            })
    
    # Enhanced example queries
    st.markdown("## 💡 **উদাহরণ প্রশ্ন**")
    
    example_categories = {
        "💊 মেডিসিন অনুসন্ধান": [
            "Paracetamol সম্পর্কে জানতে চাই",
            "Aspirin এর পার্শ্ব প্রতিক্রিয়া কী?",
            "জ্বরের জন্য কোন মেডিসিন ভালো?"
        ],
        "🏥 স্বাস্থ্য পরামর্শ": [
            "সুস্থ থাকার জন্য পরামর্শ দিন",
            "নিয়মিত ব্যায়ামের উপকারিতা",
            "মানসিক স্বাস্থ্য ভালো রাখার উপায়"
        ]
    }
    
    for category, queries in example_categories.items():
        st.markdown(f"### {category}")
        cols = st.columns(len(queries))
        for i, query in enumerate(queries):
            with cols[i]:
                if st.button(query, key=f"example_{category}_{i}"):
                    with st.spinner("🤖 সর্বোচ্চ মানের উত্তর তৈরি করা হচ্ছে..."):
                        response = st.session_state.chatbot.process_query(query)
                        st.markdown("---")
                        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
                        st.markdown(response, unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <h3>🚀 সুপার উন্নত AI মেডিসিন চ্যাটবট</h3>
        <p>ChatGPT/Cursor AI স্টাইলে সর্বোচ্চ মানের উত্তর প্রদান করে</p>
        <p>⚠️ এই তথ্যগুলো শুধুমাত্র শিক্ষামূলক উদ্দেশ্যে। চিকিৎসকের পরামর্শ নিন।</p>
        <p>🆘 জরুরি অবস্থায়: ৯৯৯</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
