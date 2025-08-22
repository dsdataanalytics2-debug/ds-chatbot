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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
    }
    
    .logo-image {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        margin-right: 1.5rem;
        border: 4px solid white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        transition: all 0.3s ease;
    }
    
    .logo-image:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 35px rgba(0,0,0,0.5);
    }
    
    .search-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2.5rem;
        border-radius: 25px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        margin: 2rem 0;
        border: 1px solid #e9ecef;
        position: relative;
        overflow: hidden;
    }
    
    .search-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(102, 126, 234, 0.03), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
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
    
    /* Enhanced Google-style search input */
    .stTextInput > div > div > input {
        border: 2px solid #e0e0e0 !important;
        border-radius: 30px !important;
        padding: 15px 25px !important;
        font-size: 18px !important;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08) !important;
        transition: all 0.4s ease !important;
        background: white !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.2) !important;
        transform: translateY(-3px) !important;
        background: #fafbfc !important;
    }
    
    /* Enhanced Google-style search button */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 15px 30px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.6) !important;
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%) !important;
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
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
        border-left: 6px solid #667eea;
        transition: all 0.3s ease;
        border: 1px solid #e9ecef;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
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
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
        color: #333 !important;
        border: 2px solid #dee2e6 !important;
        border-radius: 25px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.4s ease !important;
        margin: 8px !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button[data-testid="baseButton-secondary"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button[data-testid="baseButton-secondary"]:hover::before {
        left: 100%;
    }
    
    .stButton > button[data-testid="baseButton-secondary"]:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-color: #667eea !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4) !important;
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
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #dee2e6;
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    
    /* Enhanced search categories */
    .search-category {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Quick search buttons */
    .quick-search-btn {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        margin: 5px !important;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3) !important;
    }
    
    .quick-search-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(40, 167, 69, 0.5) !important;
    }
    
    /* Voice search button */
    .voice-search-btn {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        margin: 5px !important;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3) !important;
    }
    
    .voice-search-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.5) !important;
    }
    
    /* Smart search button */
    .smart-search-btn {
        background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        margin: 5px !important;
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.3) !important;
    }
    
    .smart-search-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(108, 92, 231, 0.5) !important;
    }
    
    /* Recent search button */
    .recent-search-btn {
        background: linear-gradient(135deg, #fd79a8 0%, #fdcb6e 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        margin: 5px !important;
        box-shadow: 0 4px 15px rgba(253, 121, 168, 0.3) !important;
    }
    
    .recent-search-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(253, 121, 168, 0.5) !important;
    }
    
    /* Popular search buttons */
    .popular-search-btn {
        background: linear-gradient(135deg, #00b894 0%, #00cec9 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        margin: 8px !important;
        box-shadow: 0 6px 20px rgba(0, 184, 148, 0.3) !important;
        width: 100% !important;
    }
    
    .popular-search-btn:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 30px rgba(0, 184, 148, 0.5) !important;
    }
    
    /* Category buttons */
    .category-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        margin: 8px !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3) !important;
        width: 100% !important;
    }
    
    .category-btn:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.5) !important;
    }
    
    /* Enhanced selectbox */
    .stSelectbox > div > div > div {
        border-radius: 15px !important;
        border: 2px solid #e0e0e0 !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div > div:hover {
        border-color: #667eea !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Search suggestions container */
    .search-suggestions {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        border: 1px solid #dee2e6;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
    }
    
    /* Floating action button */
    .fab {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 24px;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        cursor: pointer;
        transition: all 0.3s ease;
        z-index: 1000;
    }
    
    .fab:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6);
    }
    
    /* Facebook Messenger style chat results */
    .chat-result-container {
        background: #f0f2f5;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 2rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .chat-message {
        background: white;
        border-radius: 18px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        position: relative;
        max-width: 80%;
        word-wrap: break-word;
    }
    
    .chat-message.user {
        background: #0084ff;
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 5px;
    }
    
    .chat-message.bot {
        background: white;
        color: #333;
        margin-right: auto;
        border-bottom-left-radius: 5px;
    }
    
    .chat-message.bot::before {
        content: '';
        position: absolute;
        left: -8px;
        top: 15px;
        width: 0;
        height: 0;
        border: 8px solid transparent;
        border-right-color: white;
    }
    
    .chat-message.user::after {
        content: '';
        position: absolute;
        right: -8px;
        top: 15px;
        width: 0;
        height: 0;
        border: 8px solid transparent;
        border-left-color: #0084ff;
    }
    
    .chat-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        padding: 0.5rem;
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
    }
    
    .chat-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 18px;
    }
    
    .chat-info {
        flex: 1;
    }
    
    .chat-name {
        font-weight: bold;
        font-size: 1.1rem;
        margin: 0;
    }
    
    .chat-status {
        font-size: 0.9rem;
        opacity: 0.8;
        margin: 0;
    }
    
    .chat-time {
        font-size: 0.8rem;
        opacity: 0.6;
    }
    
    .chat-content {
        line-height: 1.6;
    }
    
    .chat-typing {
        display: flex;
        align-items: center;
        padding: 1rem;
        background: white;
        border-radius: 18px;
        margin: 1rem 0;
        max-width: 80%;
        margin-right: auto;
        border-bottom-left-radius: 5px;
    }
    
    .typing-dots {
        display: flex;
        gap: 4px;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #999;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .typing-dot:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
        40% { transform: scale(1); opacity: 1; }
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
        """ফাইল আপলোড প্রসেসিং এবং সেভ"""
        try:
            file_type = uploaded_file.type
            file_name = uploaded_file.name
            file_content = uploaded_file.read()
            
            # Create timestamp for unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"{timestamp}_{file_name.replace(' ', '_')}"
            
            if file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                # Excel file - save to data_files folder
                file_path = f"uploads/data_files/{safe_filename}"
                with open(file_path, "wb") as f:
                    f.write(file_content)
                
                # Try different engines for Excel file
                try:
                    # First try openpyxl engine
                    df = pd.read_excel(file_path, engine='openpyxl')
                    st.success(f"✅ Excel ফাইল সফলভাবে আপলোড এবং সেভ হয়েছে! 📁 {file_path}")
                    st.info(f"📊 মোট {len(df)} টি রো এবং {len(df.columns)} টি কলাম")
                    return df
                except Exception as e1:
                    try:
                        # Try xlrd engine for older Excel files
                        df = pd.read_excel(file_path, engine='xlrd')
                        st.success(f"✅ Excel ফাইল সফলভাবে আপলোড এবং সেভ হয়েছে! 📁 {file_path}")
                        st.info(f"📊 মোট {len(df)} টি রো এবং {len(df.columns)} টি কলাম")
                        return df
                    except Exception as e2:
                        try:
                            # Try odf engine for OpenDocument files
                            df = pd.read_excel(file_path, engine='odf')
                            st.success(f"✅ Excel ফাইল সফলভাবে আপলোড এবং সেভ হয়েছে! 📁 {file_path}")
                            st.info(f"📊 মোট {len(df)} টি রো এবং {len(df.columns)} টি কলাম")
                            return df
                        except Exception as e3:
                            st.error(f"❌ Excel ফাইল পড়তে সমস্যা: {str(e3)}")
                            st.info("💡 ফাইলটি সেভ হয়েছে কিন্তু পড়তে সমস্যা। অন্য ফরম্যাটে সেভ করে আবার চেষ্টা করুন।")
                            return None
                            
            elif file_type == "text/csv":
                # CSV file - save to data_files folder
                file_path = f"uploads/data_files/{safe_filename}"
                with open(file_path, "wb") as f:
                    f.write(file_content)
                
                df = pd.read_csv(file_path)
                st.success(f"✅ CSV ফাইল সফলভাবে আপলোড এবং সেভ হয়েছে! 📁 {file_path}")
                st.info(f"📊 মোট {len(df)} টি রো এবং {len(df.columns)} টি কলাম")
                return df
                
            elif file_type == "application/pdf":
                # PDF file - save to documents folder
                if PDF_AVAILABLE:
                    file_path = f"uploads/documents/{safe_filename}"
                    with open(file_path, "wb") as f:
                        f.write(file_content)
                    
                    pdf_reader = PyPDF2.PdfReader(file_path)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                    st.success(f"✅ PDF ফাইল সফলভাবে আপলোড এবং সেভ হয়েছে! 📁 {file_path}")
                    return {"type": "pdf", "text": text, "name": file_name, "path": file_path}
                else:
                    st.error("❌ PDF সমর্থন নেই")
                    return None
                    
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                # Word file - save to documents folder
                if PDF_AVAILABLE:
                    file_path = f"uploads/documents/{safe_filename}"
                    with open(file_path, "wb") as f:
                        f.write(file_content)
                    
                    doc = docx.Document(file_path)
                    text = ""
                    for paragraph in doc.paragraphs:
                        text += paragraph.text + "\n"
                    st.success(f"✅ Word ফাইল সফলভাবে আপলোড এবং সেভ হয়েছে! 📁 {file_path}")
                    return {"type": "docx", "text": text, "name": file_name, "path": file_path}
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
    # Check if there's a search query first
    search_query = st.session_state.get('search_query', '')
    
    # Show search results at the very top if query exists
    if search_query:
        # Facebook Messenger style chat results
        st.markdown("""
        <div class="chat-result-container">
            <div class="chat-header">
                <div class="chat-avatar">🏥</div>
                <div class="chat-info">
                    <div class="chat-name">DIGITAL SEBE CHATBOT</div>
                    <div class="chat-status">Online • Medical AI Assistant</div>
                </div>
                <div class="chat-time">Just now</div>
            </div>
        """, unsafe_allow_html=True)
        
        # User message
        st.markdown(f"""
        <div class="chat-message user">
            <div class="chat-content">
                <strong>🔍 আপনার প্রশ্ন:</strong><br>
                {search_query}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Bot typing indicator
        st.markdown("""
        <div class="chat-message bot">
            <div class="chat-typing">
                <div class="typing-dots">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
                <span style="margin-left: 10px; color: #666;">Typing...</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Bot response
        if len(search_query.split()) == 1:  # Single word search
            # Show comprehensive information in chat style
            comprehensive_info = chatbot.get_comprehensive_info(search_query)
            
            # Split comprehensive info into multiple chat messages
            info_parts = comprehensive_info.split('\n\n')
            
            for i, part in enumerate(info_parts):
                if part.strip() and not part.startswith('#'):
                    # Clean up the text for chat display
                    clean_text = part.replace('**', '').replace('---', '').strip()
                    if clean_text and len(clean_text) > 10:
                        st.markdown(f"""
                        <div class="chat-message bot">
                            <div class="chat-content">
                                {clean_text}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Also show detailed results in chat style
            results = chatbot.search_medicine(search_query)
            if results:
                st.markdown(f"""
                <div class="chat-message bot">
                    <div class="chat-content">
                        <strong>✅ {len(results)} টি ফলাফল পাওয়া গেছে</strong><br>
                        নিচে বিস্তারিত তথ্য দেখুন:
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Display results in chat style
                for i, result in enumerate(results[:5]):  # Show first 5 results
                    result_text = f"""
                    <strong>💊 ফলাফল {i+1}</strong><br>
                    <strong>সাদৃশ্য:</strong> {result['similarity']:.2f}<br>
                    """
                    
                    # Add key information
                    for key, value in result['data'].items():
                        if key != 'index' and str(value) != 'nan' and str(value).strip():
                            result_text += f"<strong>{key}:</strong> {value}<br>"
                    
                    st.markdown(f"""
                    <div class="chat-message bot">
                        <div class="chat-content">
                            {result_text}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:  # Multi-word search
            results = chatbot.search_medicine(search_query)
            if results:
                st.markdown(f"""
                <div class="chat-message bot">
                    <div class="chat-content">
                        <strong>✅ {len(results)} টি ফলাফল পাওয়া গেছে</strong><br>
                        আপনার প্রশ্নের উত্তর নিচে দেওয়া হলো:
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Display results in chat style
                for i, result in enumerate(results[:5]):  # Show first 5 results
                    result_text = f"""
                    <strong>📋 ফলাফল {i+1}</strong><br>
                    <strong>সাদৃশ্য:</strong> {result['similarity']:.2f}<br>
                    """
                    
                    # Add key information
                    for key, value in result['data'].items():
                        if key != 'index' and str(value) != 'nan' and str(value).strip():
                            result_text += f"<strong>{key}:</strong> {value}<br>"
                    
                    st.markdown(f"""
                    <div class="chat-message bot">
                        <div class="chat-content">
                            {result_text}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="chat-message bot">
                    <div class="chat-content">
                        <strong>ℹ️ কোনো ফলাফল পাওয়া যায়নি</strong><br>
                        অন্য কীওয়ার্ড দিয়ে চেষ্টা করুন।
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Close chat container
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <div class="logo-container">
            <img src="data:image/jpeg;base64,{}" class="logo-image" alt="DIGITAL SEBE LOGO">
            <div>
                <h1 style="margin: 0; font-size: 3rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🏥 DIGITAL SEBE CHATBOT</h1>
                <p style="font-size: 1.3rem; margin-top: 0.5rem; opacity: 0.9;">আপনার বিশ্বস্ত মেডিকেল AI সহকারী</p>
                <p style="font-size: 1rem; margin-top: 0.5rem; opacity: 0.8;">সব ধরনের স্বাস্থ্য সম্পর্কিত প্রশ্নের উত্তর পেতে এখানে অনুসন্ধান করুন</p>
            </div>
        </div>
    </div>
    """.format(base64.b64encode(open("chatbot pic.jpg", "rb").read()).decode()), unsafe_allow_html=True)
    
    # Main search section with enhanced styling - MOVED UP
    st.markdown("""
    <div class="search-suggestions">
        <h3 style="text-align: center; color: #333; margin-bottom: 2rem; font-size: 1.8rem;">🔍 মূল অনুসন্ধান</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Search input with enhanced options
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        current_search = st.text_input(
            "🔍 আপনার প্রশ্ন বা কীওয়ার্ড লিখুন...",
            placeholder="যেমন: ডায়াবেটিস, হৃদরোগ, লিভার সমস্যা ইত্যাদি",
            key="home_search",
            label_visibility="collapsed",
            value=search_query,
            help="আপনার মেডিকেল প্রশ্ন বা কীওয়ার্ড এখানে লিখুন"
        )
    
    with col2:
        search_category = st.selectbox(
            "📂 ক্যাটাগরি",
            ["সব", "রোগ", "ওষুধ", "লক্ষণ", "চিকিৎসা", "খাদ্যতালিকা"],
            key="search_category",
            help="অনুসন্ধানের ক্যাটাগরি নির্বাচন করুন"
        )
    
    with col3:
        search_type = st.selectbox(
            "🔍 ধরন",
            ["সাধারণ", "বিস্তারিত", "দ্রুত"],
            key="search_type",
            help="অনুসন্ধানের ধরন নির্বাচন করুন"
        )
    
    # Enhanced Search button row with better styling
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("🔍 অনুসন্ধান করুন", type="primary", use_container_width=True,
                    help="মূল অনুসন্ধান শুরু করুন"):
            if current_search:
                st.session_state.search_query = current_search
                st.rerun()
    
    with col2:
        if st.button("🎯 স্মার্ট সার্চ", use_container_width=True,
                    help="ক্যাটাগরি এবং ধরন সহ স্মার্ট অনুসন্ধান"):
            if current_search:
                # Smart search with category and type
                smart_query = f"{current_search} {search_category} {search_type}"
                st.session_state.search_query = smart_query
                st.rerun()
    
    with col3:
        if st.button("📱 ভয়েস সার্চ", use_container_width=True,
                    help="ভয়েস সার্চ ব্যবহার করুন"):
            st.info("🎤 ভয়েস সার্চ: 'ডায়াবেটিসের লক্ষণ কী?' বলুন")
            # Simulate voice search
            if current_search:
                st.session_state.search_query = current_search
                st.rerun()
    
    with col4:
        if st.button("🔄 রিসেন্ট সার্চ", use_container_width=True,
                    help="সাম্প্রতিক অনুসন্ধান দেখুন"):
            # Show recent searches
            if 'recent_searches' not in st.session_state:
                st.session_state.recent_searches = []
            
            if st.session_state.recent_searches:
                st.info("📋 সাম্প্রতিক অনুসন্ধান:")
                for i, recent in enumerate(st.session_state.recent_searches[-5:]):
                    if st.button(f"🔍 {recent}", key=f"recent_{i}"):
                        st.session_state.search_query = recent
                        st.rerun()
            else:
                st.info("📋 কোনো সাম্প্রতিক অনুসন্ধান নেই")
    
    st.markdown("---")
    
    # Quick search suggestions with enhanced styling - MOVED DOWN AND MADE SMALLER
    st.markdown("""
    <div class="search-suggestions">
        <h3 style="text-align: center; color: #333; margin-bottom: 1.5rem; font-size: 1.5rem;">⚡ দ্রুত অনুসন্ধান অপশন</h3>
        <p style="text-align: center; color: #666; margin-bottom: 1.5rem; font-size: 0.9rem;">জনপ্রিয় মেডিকেল প্রশ্নগুলো এক ক্লিকে অনুসন্ধান করুন</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search categories with enhanced styling - MADE SMALLER
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="search-category" style="padding: 0.7rem; margin: 0.5rem 0;">
            <h4 style="margin: 0; color: white; font-size: 0.9rem;">🏥 রোগের ধরন</h4>
        </div>
        """, unsafe_allow_html=True)
        disease_types = ["ডায়াবেটিস", "হৃদরোগ", "ক্যান্সার", "হাঁপানি", "গ্যাস্ট্রিক"]
        for disease in disease_types:
            if st.button(f"🔍 {disease}", key=f"disease_{disease}", use_container_width=True, 
                        help=f"{disease} সম্পর্কে বিস্তারিত জানুন"):
                st.session_state.search_query = disease
                st.rerun()
    
    with col2:
        st.markdown("""
        <div class="search-category" style="padding: 0.7rem; margin: 0.5rem 0;">
            <h4 style="margin: 0; color: white; font-size: 0.9rem;">💊 ওষুধের ধরন</h4>
        </div>
        """, unsafe_allow_html=True)
        medicine_types = ["এন্টিবায়োটিক", "পেইন কিলার", "ভিটামিন", "ইনসুলিন", "অ্যান্টি-ডায়াবেটিক"]
        for med in medicine_types:
            if st.button(f"🔍 {med}", key=f"med_{med}", use_container_width=True,
                        help=f"{med} সম্পর্কে বিস্তারিত জানুন"):
                st.session_state.search_query = med
                st.rerun()
    
    with col3:
        st.markdown("""
        <div class="search-category" style="padding: 0.7rem; margin: 0.5rem 0;">
            <h4 style="margin: 0; color: white; font-size: 0.9rem;">🔬 লক্ষণ ও চিকিৎসা</h4>
        </div>
        """, unsafe_allow_html=True)
        symptoms = ["জ্বর", "মাথাব্যথা", "পেটব্যথা", "কাশি", "বমি"]
        for symptom in symptoms:
            if st.button(f"🔍 {symptom}", key=f"symptom_{symptom}", use_container_width=True,
                        help=f"{symptom} সম্পর্কে বিস্তারিত জানুন"):
                st.session_state.search_query = symptom
                st.rerun()
    
    st.markdown("---")
    
    # Popular searches in a beautiful grid - MADE SMALLER
    st.markdown("""
    <div class="search-suggestions">
        <h3 style="text-align: center; color: #333; margin-bottom: 1.5rem; font-size: 1.5rem;">🚀 জনপ্রিয় অনুসন্ধান</h3>
        <p style="text-align: center; color: #666; margin-bottom: 1.5rem; font-size: 0.9rem;">সবচেয়ে জনপ্রিয় মেডিকেল প্রশ্নগুলো</p>
    </div>
    """, unsafe_allow_html=True)
    
    popular_searches = [
        "ডায়াবেটিসের লক্ষণ", "হৃদরোগের চিকিৎসা", "লিভার সমস্যার সমাধান",
        "গ্যাস্ট্রিকের ওষুধ", "হাঁপানির প্রতিকার", "ক্যান্সারের লক্ষণ",
        "রক্তচাপ নিয়ন্ত্রণ", "মাথাব্যথার ওষুধ", "পেটব্যথার সমাধান"
    ]
    
    cols = st.columns(3)
    for i, search in enumerate(popular_searches):
        col_idx = i % 3
        with cols[col_idx]:
            if st.button(f"⚡ {search}", key=f"popular_{i}", use_container_width=True,
                        help=f"{search} সম্পর্কে জানুন"):
                st.session_state.search_query = search
                st.rerun()
    
    # Save search to recent searches
    if current_search and current_search not in st.session_state.get('recent_searches', []):
        if 'recent_searches' not in st.session_state:
            st.session_state.recent_searches = []
        st.session_state.recent_searches.append(current_search)
        # Keep only last 10 searches
        if len(st.session_state.recent_searches) > 10:
            st.session_state.recent_searches = st.session_state.recent_searches[-10:]
    
    # Enhanced search tips section
    st.markdown("""
    <div class="feature-card">
        <h3 style="color: #667eea; text-align: center;">💡 অনুসন্ধান টিপস</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem;">
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; border-left: 4px solid #28a745;">
                <strong>🔍 একক শব্দ:</strong> "ডায়াবেটিস" লিখলে সব তথ্য পাবেন
            </div>
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; border-left: 4px solid #ffc107;">
                <strong>🎯 বিস্তারিত প্রশ্ন:</strong> "ডায়াবেটিসের লক্ষণ কী?" লিখুন
            </div>
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; border-left: 4px solid #17a2b8;">
                <strong>📂 ক্যাটাগরি:</strong> রোগ, ওষুধ, লক্ষণ ইত্যাদি নির্বাচন করুন
            </div>
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; border-left: 4px solid #dc3545;">
                <strong>⚡ দ্রুত সার্চ:</strong> জনপ্রিয় বোতামগুলো ব্যবহার করুন
            </div>
        </div>
    </div>
    
    <!-- How it works section with enhanced styling -->
    <div class="feature-card">
        <h3 style="color: #667eea; text-align: center;">🤖 আমাদের চ্যাটবট কিভাবে কাজ করে</h3>
        <div style="padding: 1.5rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin-top: 1rem;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem;">
                <div style="background: white; padding: 1rem; border-radius: 12px; border-left: 5px solid #667eea; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                    <strong style="color: #667eea;">🔍 স্মার্ট অনুসন্ধান:</strong> আপনার প্রশ্নের সাথে সম্পর্কিত সব তথ্য খুঁজে বের করে
                </div>
                <div style="background: white; padding: 1rem; border-radius: 12px; border-left: 5px solid #667eea; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                    <strong style="color: #667eea;">💊 মেডিকেল ডেটাবেস:</strong> হাজার হাজার ওষুধ এবং চিকিৎসা পদ্ধতির তথ্য
                </div>
                <div style="background: white; padding: 1rem; border-radius: 12px; border-left: 5px solid #667eea; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                    <strong style="color: #667eea;">📱 WhatsApp Marketing:</strong> একসাথে অনেক নম্বরে মেসেজ পাঠানো
                </div>
                <div style="background: white; padding: 1rem; border-radius: 12px; border-left: 5px solid #667eea; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                    <strong style="color: #667eea;">📁 ফাইল আপলোড:</strong> Excel, PDF, Word ফাইল আপলোড করে তথ্য যোগ করা
                </div>
                <div style="background: white; padding: 1rem; border-radius: 12px; border-left: 5px solid #667eea; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                    <strong style="color: #667eea;">💬 AI চ্যাট:</strong> ChatGPT এর মত বুদ্ধিমান কথোপকথন
                </div>
                <div style="background: white; padding: 1rem; border-radius: 12px; border-left: 5px solid #667eea; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                    <strong style="color: #667eea;">🎯 ক্যাটাগরি ভিত্তিক:</strong> রোগ, ওষুধ, লক্ষণ অনুযায়ী ভাগ করে তথ্য প্রদান
                </div>
            </div>
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
            # Save phone number file to uploads/phone_numbers folder
            file_content = phone_file.read()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"{timestamp}_{phone_file.name.replace(' ', '_')}"
            file_path = f"uploads/phone_numbers/{safe_filename}"
            
            with open(file_path, "wb") as f:
                f.write(file_content)
            
            if phone_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                # Excel file - try different engines
                try:
                    df = pd.read_excel(file_path, engine='openpyxl')
                except Exception as e1:
                    try:
                        df = pd.read_excel(file_path, engine='xlrd')
                    except Exception as e2:
                        try:
                            df = pd.read_excel(file_path, engine='odf')
                        except Exception as e3:
                            st.error(f"❌ Excel ফাইল পড়তে সমস্যা: {str(e3)}")
                            return
            else:
                df = pd.read_csv(file_path)
            
            # Display phone numbers
            st.success(f"✅ {len(df)} টি ফোন নম্বর লোড এবং সেভ হয়েছে! 📁 {file_path}")
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
            try:
                # Save API key file to uploads/api_keys folder
                file_content = api_key_file.read()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_filename = f"{timestamp}_{api_key_file.name.replace(' ', '_')}"
                file_path = f"uploads/api_keys/{safe_filename}"
                
                with open(file_path, "wb") as f:
                    f.write(file_content)
                
                st.success(f"✅ API কী ফাইল সফলভাবে আপলোড এবং সেভ হয়েছে! 📁 {file_path}")
                
                # Read and display API key content (masked)
                content = file_content.decode('utf-8')
                
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
    st.markdown("---")
    st.markdown("### 📋 আপলোড করা ফাইলের তালিকা")
    
    # Check uploads folders for files
    import os
    
    # Data files
    if os.path.exists("uploads/data_files"):
        data_files = [f for f in os.listdir("uploads/data_files") if f.endswith(('.xlsx', '.csv'))]
        if data_files:
            st.markdown("#### 📊 ডেটা ফাইল")
            for file in data_files:
                file_path = f"uploads/data_files/{file}"
                file_size = os.path.getsize(file_path)
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"📁 {file}")
                with col2:
                    st.write(f"📏 {file_size} bytes")
                with col3:
                    if st.button(f"🗑️ মুছুন", key=f"del_data_{file}"):
                        try:
                            os.remove(file_path)
                            st.success(f"✅ {file} মুছে ফেলা হয়েছে!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ ফাইল মুছতে সমস্যা: {str(e)}")
    
    # API key files
    if os.path.exists("uploads/api_keys"):
        api_files = [f for f in os.listdir("uploads/api_keys") if f.endswith(('.txt', '.env', '.json', '.yaml', '.yml'))]
        if api_files:
            st.markdown("#### 🔑 API কী ফাইল")
            for file in api_files:
                file_path = f"uploads/api_keys/{file}"
                file_size = os.path.getsize(file_path)
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"🔑 {file}")
                with col2:
                    st.write(f"📏 {file_size} bytes")
                with col3:
                    if st.button(f"🗑️ মুছুন", key=f"del_api_{file}"):
                        try:
                            os.remove(file_path)
                            st.success(f"✅ {file} মুছে ফেলা হয়েছে!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ ফাইল মুছতে সমস্যা: {str(e)}")
    
    # Document files
    if os.path.exists("uploads/documents"):
        doc_files = [f for f in os.listdir("uploads/documents") if f.endswith(('.pdf', '.docx'))]
        if doc_files:
            st.markdown("#### 📚 ডকুমেন্ট ফাইল")
            for file in doc_files:
                file_path = f"uploads/documents/{file}"
                file_size = os.path.getsize(file_path)
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"📖 {file}")
                with col2:
                    st.write(f"📏 {file_size} bytes")
                with col3:
                    if st.button(f"🗑️ মুছুন", key=f"del_doc_{file}"):
                        try:
                            os.remove(file_path)
                            st.success(f"✅ {file} মুছে ফেলা হয়েছে!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ ফাইল মুছতে সমস্যা: {str(e)}")
    
    # Phone number files
    if os.path.exists("uploads/phone_numbers"):
        phone_files = [f for f in os.listdir("uploads/phone_numbers") if f.endswith(('.xlsx', '.csv'))]
        if phone_files:
            st.markdown("#### 📞 ফোন নম্বর ফাইল")
            for file in phone_files:
                file_path = f"uploads/phone_numbers/{file}"
                file_size = os.path.getsize(file_path)
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"📱 {file}")
                with col2:
                    st.write(f"📏 {file_size} bytes")
                with col3:
                    if st.button(f"🗑️ মুছুন", key=f"del_phone_{file}"):
                        try:
                            os.remove(file_path)
                            st.success(f"✅ {file} মুছে ফেলা হয়েছে!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ ফাইল মুছতে সমস্যা: {str(e)}")
    
    # Check if no files uploaded
    total_files = 0
    for folder in ["data_files", "api_keys", "documents", "phone_numbers"]:
        if os.path.exists(f"uploads/{folder}"):
            total_files += len([f for f in os.listdir(f"uploads/{folder}")])
    
    if total_files == 0:
        st.info("📁 কোনো ফাইল আপলোড করা হয়নি। উপরে ফাইল আপলোড করুন।")
    else:
        st.success(f"📁 মোট {total_files} টি ফাইল আপলোড করা হয়েছে!")

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
