#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 উন্নত AI মেডিসিন চ্যাটবট
ChatGPT/Cursor AI স্টাইলে বিস্তারিত এবং সুন্দর উত্তর প্রদান করে
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
    page_title="🤖 উন্নত AI মেডিসিন চ্যাটবট",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    .bot-message {
        background-color: #f3e5f5;
        border-left-color: #9c27b0;
    }
    .info-box {
        background-color: #e8f5e8;
        border: 1px solid #4caf50;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3e0;
        border: 1px solid #ff9800;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .code-block {
        background-color: #f5f5f5;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class AdvancedMedicineChatbot:
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
            self.medicine_data = pd.DataFrame()
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text for better matching"""
        text = text.lower().strip()
        # Remove special characters but keep Bengali text
        text = re.sub(r'[^\w\s\u0980-\u09FF]', ' ', text)
        return text
    
    def find_medicine_info(self, query: str) -> Dict[str, Any]:
        """Find medicine information based on query"""
        if self.medicine_data.empty:
            return {"found": False, "message": "ডেটা পাওয়া যায়নি"}
        
        query_processed = self.preprocess_text(query)
        
        # Search in medicine names
        matches = []
        for idx, row in self.medicine_data.iterrows():
            medicine_name = str(row.get('medicine_name', '')).lower()
            generic_name = str(row.get('generic_name', '')).lower()
            indication = str(row.get('indication', '')).lower()
            
            if (query_processed in medicine_name or 
                query_processed in generic_name or 
                query_processed in indication):
                matches.append(row.to_dict())
        
        if matches:
            return {"found": True, "data": matches}
        else:
            return {"found": False, "message": "কোন মেডিসিন পাওয়া যায়নি"}
    
    def generate_detailed_response(self, query: str, medicine_info: Dict[str, Any]) -> str:
        """Generate detailed, well-structured response like ChatGPT"""
        
        if not medicine_info["found"]:
            return self.generate_not_found_response(query)
        
        medicines = medicine_info["data"]
        response_parts = []
        
        # Header
        response_parts.append("## 🔍 **আপনার প্রশ্নের বিস্তারিত উত্তর**")
        response_parts.append(f"**প্রশ্ন:** {query}")
        response_parts.append("")
        
        # Summary
        if len(medicines) == 1:
            response_parts.append("### 📋 **মেডিসিনের সংক্ষিপ্ত তথ্য**")
        else:
            response_parts.append(f"### 📋 **পাওয়া গেছে {len(medicines)}টি মেডিসিন**")
        
        response_parts.append("")
        
        # Detailed information for each medicine
        for i, medicine in enumerate(medicines, 1):
            response_parts.append(f"#### 💊 **{i}. {medicine.get('medicine_name', 'নাম জানা নেই')}**")
            response_parts.append("")
            
            # Basic information
            if medicine.get('generic_name'):
                response_parts.append(f"**জেনেরিক নাম:** {medicine['generic_name']}")
            if medicine.get('strength'):
                response_parts.append(f"**শক্তি:** {medicine['strength']}")
            if medicine.get('dosage_form'):
                response_parts.append(f"**ডোজ ফর্ম:** {medicine['dosage_form']}")
            
            response_parts.append("")
            
            # Indication
            if medicine.get('indication'):
                response_parts.append("**📝 ব্যবহারের কারণ:**")
                response_parts.append(f"> {medicine['indication']}")
                response_parts.append("")
            
            # Dosage
            if medicine.get('dosage'):
                response_parts.append("**💊 ডোজ নির্দেশনা:**")
                response_parts.append(f"> {medicine['dosage']}")
                response_parts.append("")
            
            # Side effects
            if medicine.get('side_effects'):
                response_parts.append("**⚠️ পার্শ্ব প্রতিক্রিয়া:**")
                response_parts.append(f"> {medicine['side_effects']}")
                response_parts.append("")
            
            # Precautions
            if medicine.get('precautions'):
                response_parts.append("**🚨 সতর্কতা:**")
                response_parts.append(f"> {medicine['precautions']}")
                response_parts.append("")
            
            # Contraindications
            if medicine.get('contraindications'):
                response_parts.append("**❌ নিষিদ্ধ:**")
                response_parts.append(f"> {medicine['contraindications']}")
                response_parts.append("")
            
            response_parts.append("---")
            response_parts.append("")
        
        # Additional information
        response_parts.append("### 💡 **গুরুত্বপূর্ণ পরামর্শ**")
        response_parts.append("")
        response_parts.append("🔸 **চিকিৎসকের পরামর্শ নিন:** এই তথ্যগুলো শুধুমাত্র শিক্ষামূলক উদ্দেশ্যে।")
        response_parts.append("")
        response_parts.append("🔸 **ডোজ অনুসরণ করুন:** চিকিৎসকের নির্দেশিত ডোজ অনুসরণ করুন।")
        response_parts.append("")
        response_parts.append("🔸 **পার্শ্ব প্রতিক্রিয়া লক্ষ্য করুন:** কোন অস্বাভাবিক লক্ষণ দেখা দিলে চিকিৎসকের সাথে যোগাযোগ করুন।")
        response_parts.append("")
        response_parts.append("🔸 **নিয়মিত চেকআপ:** নিয়মিত চিকিৎসকের কাছে যান।")
        
        return "\n".join(response_parts)
    
    def generate_not_found_response(self, query: str) -> str:
        """Generate helpful response when medicine not found"""
        response = f"""
## 🔍 **আপনার প্রশ্নের উত্তর**

**প্রশ্ন:** {query}

### ❌ **মেডিসিন পাওয়া যায়নি**

দুঃখিত, আপনার অনুসন্ধানকৃত মেডিসিন আমাদের ডেটাবেসে পাওয়া যায়নি।

### 💡 **সাহায্যকারী পরামর্শ**

🔸 **সঠিক বানান:** মেডিসিনের নাম সঠিকভাবে লিখেছেন কিনা চেক করুন
🔸 **জেনেরিক নাম:** মেডিসিনের জেনেরিক নাম দিয়ে অনুসন্ধান করুন
🔸 **চিকিৎসকের পরামর্শ:** আপনার চিকিৎসকের সাথে যোগাযোগ করুন
🔸 **ফার্মেসি:** নিকটস্থ ফার্মেসিতে জিজ্ঞাসা করুন

### 📞 **জরুরি যোগাযোগ**

🆘 **জরুরি সেবা:** ৯৯৯
🏥 **নিকটস্থ হাসপাতাল:** আপনার এলাকার হাসপাতালে যোগাযোগ করুন

### 🔄 **আরও অনুসন্ধান**

আপনি অন্য মেডিসিন সম্পর্কে জিজ্ঞাসা করতে পারেন অথবা সাধারণ স্বাস্থ্য পরামর্শ চাইতে পারেন।
        """
        return response
    
    def generate_health_advice(self, query: str) -> str:
        """Generate general health advice"""
        advice_templates = [
            "## 🏥 **সাধারণ স্বাস্থ্য পরামর্শ**\n\nআপনার প্রশ্নের উত্তরে কিছু সাধারণ পরামর্শ:\n\n🔸 **নিয়মিত ব্যায়াম করুন**\n🔸 **সুষম খাবার খান**\n🔸 **পর্যাপ্ত ঘুমান**\n🔸 **নিয়মিত চেকআপ করুন**",
            
            "## 💪 **স্বাস্থ্যকর জীবনযাপন**\n\nসুস্থ থাকার জন্য:\n\n🥗 **পুষ্টিকর খাবার**\n🏃‍♂️ **নিয়মিত ব্যায়াম**\n😴 **পর্যাপ্ত বিশ্রাম**\n🚭 **ধূমপান ত্যাগ করুন**",
            
            "## 🧘‍♀️ **মানসিক স্বাস্থ্য**\n\nমানসিক সুস্থতার জন্য:\n\n😊 **ইতিবাচক চিন্তা করুন**\n🧘‍♀️ **মেডিটেশন করুন**\n👥 **সামাজিক যোগাযোগ বজায় রাখুন**\n📚 **নতুন কিছু শিখুন**"
        ]
        
        return random.choice(advice_templates)
    
    def process_query(self, query: str) -> str:
        """Process user query and generate response"""
        # Add to conversation history
        self.conversation_history.append({"user": query, "timestamp": datetime.now()})
        
        # Check if it's a general health question
        health_keywords = ['স্বাস্থ্য', 'পরামর্শ', 'উপদেশ', 'জীবনযাপন', 'ব্যায়াম', 'খাবার', 'ঘুম']
        query_lower = query.lower()
        
        if any(keyword in query_lower for keyword in health_keywords):
            return self.generate_health_advice(query)
        
        # Search for medicine
        medicine_info = self.find_medicine_info(query)
        return self.generate_detailed_response(query, medicine_info)

def main():
    """Main application"""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 উন্নত AI মেডিসিন চ্যাটবট</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ **নিয়ন্ত্রণ প্যানেল**")
        
        # About section
        st.subheader("ℹ️ **সম্পর্কে**")
        st.info("""
        এই চ্যাটবট ChatGPT/Cursor AI স্টাইলে বিস্তারিত এবং সুন্দর উত্তর প্রদান করে।
        
        **বৈশিষ্ট্যসমূহ:**
        - 🔍 স্মার্ট অনুসন্ধান
        - 📋 বিস্তারিত তথ্য
        - 💡 সহায়ক পরামর্শ
        - 🎨 সুন্দর UI
        """)
        
        # Statistics
        st.subheader("📊 **পরিসংখ্যান**")
        if 'chatbot' in st.session_state:
            st.metric("মোট প্রশ্ন", len(st.session_state.chatbot.conversation_history))
        
        # Clear chat button
        if st.button("🗑️ চ্যাট মুছুন"):
            if 'chatbot' in st.session_state:
                st.session_state.chatbot.conversation_history = []
            st.rerun()
    
    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = AdvancedMedicineChatbot()
    
    # Main chat interface
    st.subheader("💬 **চ্যাট করুন**")
    
    # Chat input
    user_input = st.text_input(
        "আপনার প্রশ্ন লিখুন:",
        placeholder="যেমন: Paracetamol, Aspirin, বা সাধারণ স্বাস্থ্য পরামর্শ..."
    )
    
    # Send button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        send_button = st.button("🚀 পাঠান", use_container_width=True)
    
    # Process query
    if send_button and user_input:
        with st.spinner("🤖 উত্তর তৈরি করা হচ্ছে..."):
            response = st.session_state.chatbot.process_query(user_input)
            
            # Display response
            st.markdown("---")
            st.markdown(response, unsafe_allow_html=True)
            
            # Add to chat history
            st.session_state.chatbot.conversation_history.append({
                "bot": response, 
                "timestamp": datetime.now()
            })
    
    # Example queries
    st.subheader("💡 **উদাহরণ প্রশ্ন**")
    example_queries = [
        "Paracetamol সম্পর্কে জানতে চাই",
        "Aspirin এর পার্শ্ব প্রতিক্রিয়া কী?",
        "সুস্থ থাকার জন্য পরামর্শ দিন",
        "নিয়মিত ব্যায়ামের উপকারিতা"
    ]
    
    cols = st.columns(2)
    for i, query in enumerate(example_queries):
        with cols[i % 2]:
            if st.button(query, key=f"example_{i}"):
                with st.spinner("🤖 উত্তর তৈরি করা হচ্ছে..."):
                    response = st.session_state.chatbot.process_query(query)
                    st.markdown("---")
                    st.markdown(response, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        🤖 উন্নত AI মেডিসিন চ্যাটবট | ChatGPT/Cursor AI স্টাইল উত্তর
        <br>
        ⚠️ এই তথ্যগুলো শুধুমাত্র শিক্ষামূলক উদ্দেশ্যে। চিকিৎসকের পরামর্শ নিন।
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
