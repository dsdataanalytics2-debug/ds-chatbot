#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏥 DIGITAL SEBE CHATBOT - Advanced Medical AI Assistant
সব ধরনের মেডিকেল প্রশ্নের উত্তর এবং WhatsApp Marketing সমর্থন সহ
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import warnings
import requests
import json
from pathlib import Path
import io
import base64
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from streamlit_chat import message
import pywhatkit as pwk
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

warnings.filterwarnings('ignore')

# PDF এবং Word ফাইল প্রসেসিং এর জন্য
try:
    import PyPDF2
    import docx
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    st.warning("PDF/Word সমর্থনের জন্য PyPDF2 এবং python-docx ইনস্টল করুন")

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Page configuration
st.set_page_config(
    page_title="🏥 DIGITAL SEBE CHATBOT",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .search-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    .search-bar {
        border: 2px solid #e0e0e0;
        border-radius: 50px;
        padding: 1rem 2rem;
        font-size: 1.2rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .search-bar:focus {
        border-color: #667eea;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        outline: none;
        transform: translateY(-2px);
    }
    
    /* Google-style search input */
    .stTextInput > div > div > input {
        border: 2px solid #e0e0e0 !important;
        border-radius: 25px !important;
        padding: 12px 20px !important;
        font-size: 16px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Google-style search button */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
    }
    
    .suggestion-chip {
        display: inline-block;
        background: #f0f2f5;
        padding: 0.5rem 1rem;
        margin: 0.5rem;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .suggestion-chip:hover {
        background: #667eea;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #667eea;
    }
    
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    .whatsapp-section {
        background: linear-gradient(135deg, #25d366 0%, #128c7e 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
    }
    
    .upload-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        border: 2px dashed #667eea;
        margin: 2rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Enhanced suggestion buttons */
    .stButton > button[data-testid="baseButton-secondary"] {
        background: #f8f9fa !important;
        color: #333 !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 25px !important;
        padding: 10px 20px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        margin: 5px !important;
    }
    
    .stButton > button[data-testid="baseButton-secondary"]:hover {
        background: #667eea !important;
        color: white !important;
        border-color: #667eea !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Search results styling */
    .search-results {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    /* Metrics styling */
    .stMetric {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

class DigitalSebeChatbot:
    def __init__(self):
        self.data = None
        self.vectorizer = None
        self.tfidf_matrix = None
        self.uploaded_files = []
        self.all_sources = []
        self.chat_history = []
        self.bengali_stop_words = set([
            'এবং', 'অথবা', 'কিন্তু', 'যদি', 'তবে', 'কেন', 'কিভাবে', 'কোথায়', 'কখন', 
            'কি', 'কোন', 'কাদের', 'কার', 'কাকে', 'হয়', 'হয়েছে', 'হবে', 'করতে', 'করে', 'করবে', 
            'আছে', 'নেই', 'থাকবে', 'এটা', 'এটি', 'সেটা', 'সেটি', 'এই', 'সেই', 'যে', 'যা', 'যার', 'যাদের',
            'আমি', 'আমরা', 'তুমি', 'তোমরা', 'সে', 'তারা', 'আপনি', 'আপনারা',
            'এখানে', 'সেখানে', 'যেখানে', 'কোথায়', 'কোথাও', 'এখন', 'তখন', 'কখন', 'সবসময়', 'কখনও',
            'ভালো', 'খারাপ', 'বড়', 'ছোট', 'নতুন', 'পুরানো', 'সুন্দর', 'কুৎসিত',
            'সহজ', 'কঠিন', 'দ্রুত', 'ধীর', 'গরম', 'ঠান্ডা', 'উষ্ণ', 'শীতল'
        ])
        self.load_data()
        self.preprocess_data()
    
    def load_data(self):
        """Excel ফাইল থেকে ডেটা লোড করুন"""
        try:
            if os.path.exists('medicine_data.xlsx'):
                # Try different engines for Excel file
                try:
                    # First try openpyxl engine
                    self.data = pd.read_excel('medicine_data.xlsx', engine='openpyxl')
                    st.success(f"✅ ডেটা সফলভাবে লোড হয়েছে! মোট {len(self.data)} টি ওষুধ পাওয়া গেছে।")
                except Exception as e1:
                    try:
                        # Try xlrd engine for older Excel files
                        self.data = pd.read_excel('medicine_data.xlsx', engine='xlrd')
                        st.success(f"✅ ডেটা সফলভাবে লোড হয়েছে! মোট {len(self.data)} টি ওষুধ পাওয়া গেছে।")
                    except Exception as e2:
                        try:
                            # Try odf engine for OpenDocument files
                            self.data = pd.read_excel('medicine_data.xlsx', engine='odf')
                            st.success(f"✅ ডেটা সফলভাবে লোড হয়েছে! মোট {len(self.data)} টি ওষুধ পাওয়া গেছে।")
                        except Exception as e3:
                            # If all engines fail, try reading as CSV
                            try:
                                self.data = pd.read_csv('medicine_data.xlsx', encoding='utf-8')
                                st.success(f"✅ ডেটা CSV হিসেবে লোড হয়েছে! মোট {len(self.data)} টি ওষুধ পাওয়া গেছে।")
                            except Exception as e4:
                                st.error(f"❌ সব engine দিয়ে ডেটা লোড করতে ব্যর্থ: {str(e4)}")
                                st.info("💡 ফাইল আপলোড পেজে নতুন ডেটা আপলোড করুন।")
                                self.data = None
            else:
                st.warning("⚠️ medicine_data.xlsx ফাইল পাওয়া যায়নি। নতুন ফাইল আপলোড করুন।")
                self.data = None
        except Exception as e:
            st.error(f"❌ ডেটা লোড করতে সমস্যা হয়েছে: {str(e)}")
            self.data = None
    
    def preprocess_data(self):
        """ডেটা প্রিপ্রসেসিং"""
        if self.data is not None and len(self.data) > 0:
            try:
                # Combine all text columns
                text_columns = []
                for col in self.data.columns:
                    if self.data[col].dtype == 'object':
                        text_columns.append(col)
                
                if text_columns:
                    combined_text = self.data[text_columns].fillna('').astype(str).agg(' '.join, axis=1)
                    
                    # Create TF-IDF vectorizer
                    self.vectorizer = TfidfVectorizer(
                        max_features=1000,
                        stop_words=list(self.bengali_stop_words),
                        ngram_range=(1, 2)
                    )
                    
                    # Fit and transform
                    self.tfidf_matrix = self.vectorizer.fit_transform(combined_text)
                    st.success("✅ ডেটা প্রিপ্রসেসিং সম্পন্ন হয়েছে!")
            except Exception as e:
                st.error(f"❌ ডেটা প্রিপ্রসেসিং এ সমস্যা: {str(e)}")
    
    def search_medicine(self, query, top_k=10):
        """ওষুধ অনুসন্ধান - উন্নত"""
        if self.vectorizer is None or self.tfidf_matrix is None:
            return []
        
        try:
            # Transform query
            query_vector = self.vectorizer.transform([query])
            
            # Calculate similarity
            similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            
            # Get top matches with higher threshold for single word searches
            if len(query.split()) == 1:  # Single word search
                # Lower threshold for single words to get more comprehensive results
                threshold = 0.05
                top_k = min(15, len(similarities))  # More results for single words
            else:  # Multi-word search
                threshold = 0.1
                top_k = min(top_k, len(similarities))
            
            # Get top matches
            top_indices = similarities.argsort()[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > threshold:
                    result = {
                        'index': idx,
                        'similarity': similarities[idx],
                        'data': self.data.iloc[idx].to_dict()
                    }
                    results.append(result)
            
            # Sort by similarity
            results.sort(key=lambda x: x['similarity'], reverse=True)
            
            return results
            
        except Exception as e:
            st.error(f"❌ অনুসন্ধানে সমস্যা: {str(e)}")
            return []
    
    def get_comprehensive_info(self, query):
        """কমপ্রিহেনসিভ তথ্য প্রদান - Cursor AI এর মত"""
        try:
            # Search for relevant information
            search_results = self.search_medicine(query)
            
            if not search_results:
                return f"দুঃখিত, '{query}' সম্পর্কে কোনো তথ্য পাওয়া যায়নি।"
            
            # Generate comprehensive response
            response = f"# 🔍 '{query}' সম্পর্কে বিস্তারিত তথ্য\n\n"
            
            # Add summary
            response += f"**মোট {len(search_results)} টি সম্পর্কিত তথ্য পাওয়া গেছে।**\n\n"
            
            # Group by category if possible
            categories = {}
            for result in search_results:
                category = result['data'].get('Category', 'অন্যান্য')
                if category not in categories:
                    categories[category] = []
                categories[category].append(result)
            
            # Show results by category
            for category, results in categories.items():
                response += f"## 📂 {category}\n\n"
                
                for i, result in enumerate(results):
                    response += f"### 💊 {result['data'].get('Medicine Name', 'নাম নেই')}\n"
                    response += f"**বাংলা নাম:** {result['data'].get('Bengali Name', 'নাম নেই')}\n\n"
                    response += f"**ব্যবহার:** {result['data'].get('Uses', 'তথ্য নেই')}\n\n"
                    response += f"**পার্শ্বপ্রতিক্রিয়া:** {result['data'].get('Side Effects', 'তথ্য নেই')}\n\n"
                    response += f"**মাত্রা:** {result['data'].get('Dosage', 'তথ্য নেই')}\n\n"
                    response += f"**মূল্য:** {result['data'].get('Price (BDT)', 'তথ্য নেই')}\n\n"
                    response += f"**সাদৃশ্য স্কোর:** {result['similarity']:.2f}\n\n"
                    response += "---\n\n"
            
            # Add general advice
            response += "## 💡 সাধারণ পরামর্শ\n\n"
            response += f"'{query}' সম্পর্কে আরও বিস্তারিত জানতে চাইলে আমাদের AI চ্যাট ব্যবহার করুন। "
            response += "এছাড়াও আপনার ডাক্তারের সাথে পরামর্শ করুন।\n\n"
            
            return response
            
        except Exception as e:
            return f"দুঃখিত, একটি ত্রুটি ঘটেছে: {str(e)}"
    
    def process_file_upload(self, uploaded_file):
        """ফাইল আপলোড প্রসেসিং"""
        try:
            file_type = uploaded_file.type
            file_name = uploaded_file.name
            
            if file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                # Excel file - try different engines
                try:
                    # First try openpyxl engine
                    df = pd.read_excel(uploaded_file, engine='openpyxl')
                    st.success(f"✅ Excel ফাইল সফলভাবে আপলোড হয়েছে! মোট {len(df)} টি রো")
                    return df
                except Exception as e1:
                    try:
                        # Try xlrd engine for older Excel files
                        df = pd.read_excel(uploaded_file, engine='xlrd')
                        st.success(f"✅ Excel ফাইল সফলভাবে আপলোড হয়েছে! মোট {len(df)} টি রো")
                        return df
                    except Exception as e2:
                        try:
                            # Try odf engine for OpenDocument files
                            df = pd.read_excel(uploaded_file, engine='odf')
                            st.success(f"✅ Excel ফাইল সফলভাবে আপলোড হয়েছে! মোট {len(df)} টি রো")
                            return df
                        except Exception as e3:
                            st.error(f"❌ Excel ফাইল পড়তে সমস্যা: {str(e3)}")
                            st.info("💡 ফাইলটি অন্য ফরম্যাটে সেভ করে আবার চেষ্টা করুন।")
                            return None
            elif file_type == "text/csv":
                # CSV file
                df = pd.read_csv(uploaded_file)
                st.success(f"✅ CSV ফাইল সফলভাবে আপলোড হয়েছে! মোট {len(df)} টি রো")
                return df
            elif file_type == "application/pdf":
                # PDF file
                if PDF_AVAILABLE:
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                    st.success(f"✅ PDF ফাইল সফলভাবে আপলোড হয়েছে!")
                    return {"type": "pdf", "text": text, "name": file_name}
                else:
                    st.error("❌ PDF সমর্থন নেই")
                    return None
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                # Word file
                if PDF_AVAILABLE:
                    doc = docx.Document(uploaded_file)
                    text = ""
                    for paragraph in doc.paragraphs:
                        text += paragraph.text + "\n"
                    st.success(f"✅ Word ফাইল সফলভাবে আপলোড হয়েছে!")
                    return {"type": "docx", "text": text, "name": file_name}
                else:
                    st.error("❌ Word সমর্থন নেই")
                    return None
            else:
                st.error("❌ অসমর্থিত ফাইল ফরম্যাট")
                return None
        except Exception as e:
            st.error(f"❌ ফাইল প্রসেসিং এ সমস্যা: {str(e)}")
            return None
    
    def send_whatsapp_message(self, phone_numbers, message):
        """WhatsApp মেসেজ পাঠানো"""
        try:
            success_count = 0
            failed_count = 0
            
            for phone in phone_numbers:
                try:
                    # Format phone number
                    if not phone.startswith('+'):
                        if phone.startswith('0'):
                            phone = '+88' + phone[1:]
                        else:
                            phone = '+88' + phone
                    
                    # Send message using pywhatkit
                    pwk.sendwhatmsg_instantly(
                        phone_no=phone,
                        message=message,
                        wait_time=15,
                        tab_close=True
                    )
                    success_count += 1
                    time.sleep(2)  # Delay between messages
                    
                except Exception as e:
                    failed_count += 1
                    st.error(f"❌ {phone} নম্বরে মেসেজ পাঠাতে সমস্যা: {str(e)}")
            
            return success_count, failed_count
            
        except Exception as e:
            st.error(f"❌ WhatsApp মেসেজ পাঠানোতে সমস্যা: {str(e)}")
            return 0, 0

def main():
    # Initialize chatbot
    chatbot = DigitalSebeChatbot()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h2>🏥</h2>
            <h3>DIGITAL SEBE</h3>
            <p>Advanced Medical AI</p>
        </div>
        """, unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title="মেনু",
            options=["🏠 হোম", "🔍 অনুসন্ধান", "💬 চ্যাট", "📱 WhatsApp Marketing", "📁 ফাইল আপলোড", "ℹ️ সাহায্য"],
            icons=["house", "search", "chat", "whatsapp", "upload", "info-circle"],
            menu_icon="cast",
            default_index=0,
        )
    
    # Main content area
    if selected == "🏠 হোম":
        show_home_page(chatbot)
    elif selected == "🔍 অনুসন্ধান":
        show_search_page(chatbot)
    elif selected == "💬 চ্যাট":
        show_chat_page(chatbot)
    elif selected == "📱 WhatsApp Marketing":
        show_whatsapp_page(chatbot)
    elif selected == "📁 ফাইল আপলোড":
        show_upload_page(chatbot)
    elif selected == "ℹ️ সাহায্য":
        show_help_page()

def show_home_page(chatbot):
    """হোম পেজ দেখানো"""
    st.markdown("""
    <div class="main-header">
        <h1>🏥 DIGITAL SEBE CHATBOT</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">আপনার বিশ্বস্ত মেডিকেল AI সহকারী</p>
        <p style="font-size: 1rem; margin-top: 0.5rem;">সব ধরনের স্বাস্থ্য সম্পর্কিত প্রশ্নের উত্তর পেতে এখানে অনুসন্ধান করুন</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Google-style Search Bar
    st.markdown("""
    <div class="search-container">
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: #333; font-size: 2rem; margin-bottom: 1rem;">🔍 আপনার প্রশ্ন অনুসন্ধান করুন</h2>
            <p style="color: #666; font-size: 1.1rem;">Google এর মত সহজে অনুসন্ধান করুন</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Centered search input with Google-like styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        search_query = st.text_input(
            "🔍 আপনার প্রশ্ন বা কীওয়ার্ড লিখুন...",
            placeholder="যেমন: ডায়াবেটিস, হৃদরোগ, লিভার সমস্যা ইত্যাদি",
            key="home_search",
            label_visibility="collapsed"
        )
        
        # Search button
        if st.button("🔍 অনুসন্ধান করুন", type="primary", use_container_width=True):
            if search_query:
                st.session_state.search_query = search_query
                st.rerun()
    
    # Show search results at the top if query exists
    if search_query or st.session_state.get('search_query'):
        query = search_query or st.session_state.get('search_query')
        if query:
            st.markdown("---")
            st.markdown(f"### 🔍 '{query}' এর জন্য অনুসন্ধান ফলাফল")
            
            # Use comprehensive search for better results
            if len(query.split()) == 1:  # Single word search
                # Show comprehensive information
                comprehensive_info = chatbot.get_comprehensive_info(query)
                st.markdown(comprehensive_info)
                
                # Also show detailed results
                results = chatbot.search_medicine(query)
                if results:
                    st.success(f"✅ {len(results)} টি ফলাফল পাওয়া গেছে")
                    
                    # Display results in a better format
                    for i, result in enumerate(results):
                        with st.expander(f"📋 বিস্তারিত ফলাফল {i+1} - সাদৃশ্য: {result['similarity']:.2f}", expanded=False):
                            col1, col2 = st.columns([1, 3])
                            with col1:
                                st.metric("সাদৃশ্য", f"{result['similarity']:.2f}")
                            with col2:
                                for key, value in result['data'].items():
                                    if key != 'index':
                                        st.write(f"**{key}:** {value}")
            else:  # Multi-word search
                results = chatbot.search_medicine(query)
                if results:
                    st.success(f"✅ {len(results)} টি ফলাফল পাওয়া গেছে")
                    
                    # Display results in a better format
                    for i, result in enumerate(results):
                        with st.expander(f"📋 ফলাফল {i+1} - সাদৃশ্য: {result['similarity']:.2f}", expanded=True):
                            col1, col2 = st.columns([1, 3])
                            with col1:
                                st.metric("সাদৃশ্য", f"{result['similarity']:.2f}")
                            with col2:
                                for key, value in result['data'].items():
                                    if key != 'index':
                                        st.write(f"**{key}:** {value}")
                else:
                    st.info("ℹ️ কোনো ফলাফল পাওয়া যায়নি। অন্য কীওয়ার্ড দিয়ে চেষ্টা করুন।")
    
    # Enhanced Search Suggestions
    st.markdown("""
    <div class="feature-card">
        <h3>🔍 জনপ্রিয় অনুসন্ধান</h3>
        <p>নিচের বিষয়গুলো সম্পর্কে জানতে ক্লিক করুন:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Better organized suggestions
    suggestions = [
        "ডায়াবেটিস", "হৃদরোগ", "লিভারের সমস্যা", "কিডনির সমস্যা",
        "গ্যাস্ট্রিক", "যৌন সমস্যা ও টেস্টোস্টেরন", "হাঁপানি", "ক্যান্সার"
    ]
    
    # Create a more organized grid
    cols = st.columns(4)
    for i, suggestion in enumerate(suggestions):
        col_idx = i % 4
        with cols[col_idx]:
            if st.button(f"🔍 {suggestion}", key=f"sugg_{i}", use_container_width=True):
                st.session_state.home_search = suggestion
                st.rerun()
    
    # How it works section with better styling
    st.markdown("""
    <div class="feature-card">
        <h3>🤖 আমাদের চ্যাটবট কিভাবে কাজ করে</h3>
        <div style="padding: 1rem; background: #f8f9fa; border-radius: 10px;">
            <ul style="list-style: none; padding: 0;">
                <li style="margin: 0.5rem 0; padding: 0.5rem; background: white; border-radius: 8px; border-left: 4px solid #667eea;">
                    <strong>🔍 স্মার্ট অনুসন্ধান:</strong> আপনার প্রশ্নের সাথে সম্পর্কিত সব তথ্য খুঁজে বের করে
                </li>
                <li style="margin: 0.5rem 0; padding: 0.5rem; background: white; border-radius: 8px; border-left: 4px solid #667eea;">
                    <strong>💊 মেডিকেল ডেটাবেস:</strong> হাজার হাজার ওষুধ এবং চিকিৎসা পদ্ধতির তথ্য
                </li>
                <li style="margin: 0.5rem 0; padding: 0.5rem; background: white; border-radius: 8px; border-left: 4px solid #667eea;">
                    <strong>📱 WhatsApp Marketing:</strong> একসাথে অনেক নম্বরে মেসেজ পাঠানো
                </li>
                <li style="margin: 0.5rem 0; padding: 0.5rem; background: white; border-radius: 8px; border-left: 4px solid #667eea;">
                    <strong>📁 ফাইল আপলোড:</strong> Excel, PDF, Word ফাইল আপলোড করে তথ্য যোগ করা
                </li>
                <li style="margin: 0.5rem 0; padding: 0.5rem; background: white; border-radius: 8px; border-left: 4px solid #667eea;">
                    <strong>💬 AI চ্যাট:</strong> ChatGPT এর মত বুদ্ধিমান কথোপকথন
                </li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_search_page(chatbot):
    """অনুসন্ধান পেজ দেখানো"""
    st.markdown("""
    <div class="main-header">
        <h2>🔍 মেডিকেল অনুসন্ধান</h2>
        <p>আপনার স্বাস্থ্য সম্পর্কিত প্রশ্নের উত্তর খুঁজুন</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Advanced search
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "আপনার প্রশ্ন লিখুন...",
            placeholder="যেমন: ডায়াবেটিসের লক্ষণ, হৃদরোগের চিকিৎসা, লিভার সমস্যার সমাধান",
            key="search_page_query"
        )
    
    with col2:
        search_type = st.selectbox(
            "অনুসন্ধানের ধরন",
            ["সব", "লক্ষণ", "চিকিৎসা", "ওষুধ", "খাদ্যতালিকা"]
        )
    
    if search_query:
        results = chatbot.search_medicine(search_query)
        if results:
            st.success(f"✅ '{search_query}' এর জন্য {len(results)} টি ফলাফল পাওয়া গেছে")
            
            # Display results in tabs
            tab1, tab2 = st.tabs(["📋 ফলাফল", "📊 বিশ্লেষণ"])
            
            with tab1:
                for i, result in enumerate(results):
                    with st.expander(f"ফলাফল {i+1} - সাদৃশ্য: {result['similarity']:.2f}"):
                        for key, value in result['data'].items():
                            st.write(f"**{key}:** {value}")
            
            with tab2:
                if len(results) > 1:
                    # Similarity chart
                    similarities = [r['similarity'] for r in results]
                    labels = [f"ফলাফল {i+1}" for i in range(len(results))]
                    
                    fig = px.bar(
                        x=labels,
                        y=similarities,
                        title="ফলাফলের সাদৃশ্য স্কোর",
                        labels={"x": "ফলাফল", "y": "সাদৃশ্য স্কোর"}
                    )
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ℹ️ কোনো ফলাফল পাওয়া যায়নি। অন্য কীওয়ার্ড দিয়ে চেষ্টা করুন।")

def show_chat_page(chatbot):
    """চ্যাট পেজ দেখানো"""
    st.markdown("""
    <div class="main-header">
        <h2>💬 AI চ্যাট</h2>
        <p>ChatGPT এর মত বুদ্ধিমান কথোপকথন করুন</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Chat input
    user_input = st.chat_input("আপনার প্রশ্ন লিখুন...")
    
    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Generate AI response
        ai_response = generate_ai_response(user_input, chatbot)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Clear chat button
    if st.button("🗑️ চ্যাট মুছুন"):
        st.session_state.messages = []
        st.rerun()

def generate_ai_response(user_input, chatbot):
    """AI রেসপন্স জেনারেট করা - Cursor AI এর মত উন্নত"""
    try:
        # Check if it's a medical question
        medical_keywords = ['ডায়াবেটিস', 'হৃদরোগ', 'লিভার', 'কিডনি', 'গ্যাস্ট্রিক', 'হাঁপানি', 'ক্যান্সার', 
                           'ওষুধ', 'চিকিৎসা', 'লক্ষণ', 'প্রতিকার', 'খাবার', 'ডায়েট', 'ব্যায়াম']
        
        is_medical = any(keyword in user_input for keyword in medical_keywords)
        
        if is_medical:
            # Use comprehensive search for medical questions
            comprehensive_info = chatbot.get_comprehensive_info(user_input)
            return comprehensive_info
        else:
            # For general questions, provide helpful response
            response = f"# 💬 আপনার প্রশ্ন: {user_input}\n\n"
            response += "আপনার প্রশ্নটি মেডিকেল বিষয়ের সাথে সম্পর্কিত নয়। "
            response += "আমি একটি মেডিকেল AI সহকারী, তাই স্বাস্থ্য সম্পর্কিত প্রশ্ন জিজ্ঞাসা করুন।\n\n"
            response += "## 💡 উদাহরণ প্রশ্ন:\n"
            response += "- ডায়াবেটিসের লক্ষণ কী?\n"
            response += "- হৃদরোগের চিকিৎসা কী?\n"
            response += "- লিভার সমস্যার জন্য কী খাবেন?\n"
            response += "- গ্যাস্ট্রিকের ওষুধ কী?\n\n"
            response += "আপনার স্বাস্থ্য সম্পর্কিত যেকোনো প্রশ্ন জিজ্ঞাসা করতে পারেন!"
            
            return response
        
    except Exception as e:
        return f"দুঃখিত, একটি ত্রুটি ঘটেছে: {str(e)}"

def show_whatsapp_page(chatbot):
    """WhatsApp Marketing পেজ দেখানো"""
    st.markdown("""
    <div class="whatsapp-section">
        <h2>📱 WhatsApp Marketing</h2>
        <p>একসাথে অনেক নম্বরে মেসেজ পাঠান</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload for phone numbers
    st.markdown("""
    <div class="upload-section">
        <h3>📞 ফোন নম্বর আপলোড করুন</h3>
        <p>Excel বা CSV ফাইলে ফোন নম্বরগুলো রাখুন</p>
    </div>
    """, unsafe_allow_html=True)
    
    phone_file = st.file_uploader(
        "ফোন নম্বর ফাইল আপলোড করুন",
        type=['xlsx', 'csv'],
        key="phone_file"
    )
    
    phone_numbers = []
    if phone_file:
        try:
            if phone_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                # Excel file - try different engines
                try:
                    df = pd.read_excel(phone_file, engine='openpyxl')
                except Exception as e1:
                    try:
                        df = pd.read_excel(phone_file, engine='xlrd')
                    except Exception as e2:
                        try:
                            df = pd.read_excel(phone_file, engine='odf')
                        except Exception as e3:
                            st.error(f"❌ Excel ফাইল পড়তে সমস্যা: {str(e3)}")
                            return
            else:
                df = pd.read_csv(phone_file)
            
            # Display phone numbers
            st.success(f"✅ {len(df)} টি ফোন নম্বর লোড হয়েছে")
            st.dataframe(df.head(10))
            
            # Extract phone numbers
            for col in df.columns:
                if 'phone' in col.lower() or 'mobile' in col.lower() or 'number' in col.lower():
                    phone_numbers = df[col].dropna().astype(str).tolist()
                    break
            
            if not phone_numbers:
                # Try first column if no phone column found
                phone_numbers = df.iloc[:, 0].dropna().astype(str).tolist()
            
        except Exception as e:
            st.error(f"❌ ফাইল পড়তে সমস্যা: {str(e)}")
    
    # Message input
    message_text = st.text_area(
        "মেসেজ লিখুন",
        placeholder="আপনার মেসেজ এখানে লিখুন...",
        height=150
    )
    
    # Send button
    if st.button("📤 মেসেজ পাঠান", disabled=not phone_numbers or not message_text):
        if phone_numbers and message_text:
            with st.spinner("মেসেজ পাঠানো হচ্ছে..."):
                success, failed = chatbot.send_whatsapp_message(phone_numbers, message_text)
                
                if success > 0:
                    st.success(f"✅ {success} টি মেসেজ সফলভাবে পাঠানো হয়েছে!")
                if failed > 0:
                    st.warning(f"⚠️ {failed} টি মেসেজ পাঠানো যায়নি")
        else:
            st.warning("⚠️ ফোন নম্বর এবং মেসেজ উভয়ই প্রয়োজন")

def show_upload_page(chatbot):
    """ফাইল আপলোড পেজ দেখানো"""
    st.markdown("""
    <div class="main-header">
        <h2>📁 ফাইল আপলোড</h2>
        <p>নতুন তথ্য যোগ করুন</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different upload types
    tab1, tab2, tab3 = st.tabs(["📊 ডেটা ফাইল", "🔑 API কী", "📚 ডকুমেন্ট"])
    
    with tab1:
        st.markdown("""
        <div class="upload-section">
            <h3>📊 ডেটা ফাইল আপলোড করুন</h3>
            <p>মেডিকেল ডেটা, ফোন নম্বর ইত্যাদি Excel/CSV ফাইলে আপলোড করুন</p>
        </div>
        """, unsafe_allow_html=True)
        
        data_files = st.file_uploader(
            "ডেটা ফাইল নির্বাচন করুন",
            type=['xlsx', 'csv'],
            accept_multiple_files=True,
            key="data_files"
        )
        
        if data_files:
            st.success(f"✅ {len(data_files)} টি ডেটা ফাইল আপলোড হয়েছে")
            
            for uploaded_file in data_files:
                st.write(f"📁 {uploaded_file.name}")
                
                # Process file
                result = chatbot.process_file_upload(uploaded_file)
                
                if result is not None:
                    if isinstance(result, pd.DataFrame):
                        st.dataframe(result.head())
                        st.info(f"📊 মোট {len(result)} টি রো এবং {len(result.columns)} টি কলাম")
                    elif isinstance(result, dict):
                        st.write(f"**ফাইল ধরন:** {result['type']}")
                        st.write(f"**ফাইল নাম:** {result['name']}")
    
    with tab2:
        st.markdown("""
        <div class="upload-section">
            <h3>🔑 API কী আপলোড করুন</h3>
            <p>WhatsApp API, OpenAI API ইত্যাদি কী ফাইল আপলোড করুন</p>
        </div>
        """, unsafe_allow_html=True)
        
        # API Key upload
        api_key_file = st.file_uploader(
            "API কী ফাইল নির্বাচন করুন",
            type=['txt', 'env', 'json', 'yaml', 'yml'],
            key="api_key_file"
        )
        
        if api_key_file:
            st.success(f"✅ API কী ফাইল আপলোড হয়েছে: {api_key_file.name}")
            
            # Read and display API key content (masked)
            try:
                content = api_key_file.read().decode('utf-8')
                
                # Mask sensitive information
                masked_content = content
                if 'API_KEY' in content or 'api_key' in content:
                    masked_content = re.sub(r'(API_KEY|api_key)\s*[:=]\s*([^\s\n]+)', r'\1: ********', masked_content)
                if 'SECRET' in content or 'secret' in content:
                    masked_content = re.sub(r'(SECRET|secret)\s*[:=]\s*([^\s\n]+)', r'\1: ********', masked_content)
                
                st.text_area("API কী বিষয়বস্তু (মাস্ক করা)", masked_content, height=200)
                
                # Save API key to .env file
                if st.button("💾 .env ফাইলে সেভ করুন"):
                    try:
                        with open('.env', 'w', encoding='utf-8') as f:
                            f.write(content)
                        st.success("✅ API কী .env ফাইলে সফলভাবে সেভ হয়েছে!")
                    except Exception as e:
                        st.error(f"❌ .env ফাইলে সেভ করতে সমস্যা: {str(e)}")
                        
            except Exception as e:
                st.error(f"❌ API কী ফাইল পড়তে সমস্যা: {str(e)}")
        
        # Manual API key input
        st.markdown("---")
        st.markdown("### 🔑 ম্যানুয়াল API কী ইনপুট")
        
        col1, col2 = st.columns(2)
        with col1:
            api_name = st.text_input("API নাম", placeholder="যেমন: OpenAI, WhatsApp")
        with col2:
            api_key = st.text_input("API কী", placeholder="sk-...", type="password")
        
        if st.button("💾 API কী সেভ করুন", disabled=not api_name or not api_key):
            try:
                # Append to .env file
                with open('.env', 'a', encoding='utf-8') as f:
                    f.write(f"\n{api_name.upper()}_API_KEY={api_key}")
                st.success(f"✅ {api_name} API কী সফলভাবে সেভ হয়েছে!")
            except Exception as e:
                st.error(f"❌ API কী সেভ করতে সমস্যা: {str(e)}")
    
    with tab3:
        st.markdown("""
        <div class="upload-section">
            <h3>📚 ডকুমেন্ট আপলোড করুন</h3>
            <p>মেডিকেল ডকুমেন্ট, গবেষণা পত্র ইত্যাদি PDF/Word ফাইলে আপলোড করুন</p>
        </div>
        """, unsafe_allow_html=True)
        
        doc_files = st.file_uploader(
            "ডকুমেন্ট ফাইল নির্বাচন করুন",
            type=['pdf', 'docx'],
            accept_multiple_files=True,
            key="doc_files"
        )
        
        if doc_files:
            st.success(f"✅ {len(doc_files)} টি ডকুমেন্ট ফাইল আপলোড হয়েছে")
            
            for uploaded_file in doc_files:
                st.write(f"📁 {uploaded_file.name}")
                
                # Process file
                result = chatbot.process_file_upload(uploaded_file)
                
                if result is not None:
                    if isinstance(result, dict):
                        st.write(f"**ফাইল ধরন:** {result['type']}")
                        st.write(f"**ফাইল নাম:** {result['name']}")
                        if 'text' in result:
                            with st.expander("📖 ফাইলের বিষয়বস্তু দেখুন"):
                                st.text(result['text'][:1000] + "..." if len(result['text']) > 1000 else result['text'])
    
    # Show uploaded files summary
    if st.session_state.get('upload_files') or st.session_state.get('data_files') or st.session_state.get('doc_files'):
        st.markdown("---")
        st.markdown("### 📋 আপলোড করা ফাইলের তালিকা")
        
        all_files = []
        if st.session_state.get('data_files'):
            all_files.extend(st.session_state.get('data_files', []))
        if st.session_state.get('doc_files'):
            all_files.extend(st.session_state.get('doc_files', []))
        
        if all_files:
            for i, file in enumerate(all_files):
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"📁 {file.name}")
                with col2:
                    st.write(f"📏 {file.size} bytes")
                with col3:
                    if st.button(f"🗑️ মুছুন", key=f"del_{i}"):
                        # Remove file from session state
                        if file in st.session_state.get('data_files', []):
                            st.session_state.data_files.remove(file)
                        if file in st.session_state.get('doc_files', []):
                            st.session_state.doc_files.remove(file)
                        st.rerun()

def show_help_page():
    """সাহায্য পেজ দেখানো"""
    st.markdown("""
    <div class="main-header">
        <h2>ℹ️ সাহায্য</h2>
        <p>DIGITAL SEBE CHATBOT ব্যবহার করার নির্দেশিকা</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>🔍 অনুসন্ধান কিভাবে করবেন</h3>
        <ol>
            <li>হোম পেজে গিয়ে সার্চ বারে আপনার প্রশ্ন লিখুন</li>
            <li>অথবা জনপ্রিয় অনুসন্ধান বোতামে ক্লিক করুন</li>
            <li>আপনার প্রশ্নের সাথে সম্পর্কিত সব তথ্য দেখতে পাবেন</li>
        </ol>
    </div>
    
    <div class="feature-card">
        <h3>💬 চ্যাট কিভাবে করবেন</h3>
        <ol>
            <li>চ্যাট পেজে গিয়ে আপনার প্রশ্ন লিখুন</li>
            <li>AI আপনার প্রশ্নের উত্তর দেবে</li>
            <li>চ্যাট ইতিহাস সংরক্ষিত থাকবে</li>
        </ol>
    </div>
    
    <div class="feature-card">
        <h3>📱 WhatsApp Marketing কিভাবে করবেন</h3>
        <ol>
            <li>Excel বা CSV ফাইলে ফোন নম্বরগুলো রাখুন</li>
            <li>ফাইল আপলোড করুন</li>
            <li>মেসেজ লিখুন</li>
            <li>মেসেজ পাঠান বোতামে ক্লিক করুন</li>
        </ol>
    </div>
    
    <div class="feature-card">
        <h3>📁 ফাইল আপলোড কিভাবে করবেন</h3>
        <ol>
            <li>ফাইল আপলোড পেজে যান</li>
            <li>সমর্থিত ফরম্যাটের ফাইল নির্বাচন করুন</li>
            <li>ফাইল আপলোড করুন</li>
            <li>ফাইলের বিষয়বস্তু দেখুন</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
