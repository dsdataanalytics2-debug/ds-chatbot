#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💊 PROFESSIONAL মেডিসিন চ্যাটবট - COMPLETELY REORGANIZED UI
Modern এবং Professional Frontend Design with Better UX
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
warnings.filterwarnings('ignore')

# PDF এবং Word ফাইল প্রসেসিং এর জন্য
try:
    import PyPDF2
    import docx
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class ProfessionalMedicineChatbot:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.data = None
        self.vectorizer = None
        self.tfidf_matrix = None
        self.pdf_data = []
        self.word_data = []
        self.excel_data = []
        self.api_data = []
        self.all_sources = []
        self.bengali_stop_words = set([
            'এবং', 'অথবা', 'কিন্তু', 'যদি', 'তবে', 'কেন', 'কিভাবে', 'কোথায়', 'কখন', 
            'কি', 'কোন', 'কাদের', 'কার', 'কাকে', 'হয়', 'হয়েছে', 'হবে', 'করতে', 'করে', 
            'করবে', 'আছে', 'নেই', 'থাকবে', 'এটা', 'এটি', 'সেটা', 'সেটি', 'এই', 'সেই'
        ])
        self.load_data()
        self.preprocess_data()

    def save_uploaded_file_to_data_source(self, uploaded_file):
        """UploadedFile ডিস্কে সেভ করুন"""
        try:
            data_dir = Path("data source")
            data_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = uploaded_file.name
            dest_path = data_dir / f"{timestamp}_{safe_name}"
            
            try:
                bytes_data = uploaded_file.getbuffer()
                with open(dest_path, "wb") as f:
                    f.write(bytes_data)
            except Exception:
                content = uploaded_file.read()
                with open(dest_path, "wb") as f:
                    f.write(content)
                try:
                    uploaded_file.seek(0)
                except Exception:
                    pass
            return str(dest_path)
        except Exception as e:
            st.warning(f"ফাইল সেভ করতে সমস্যা: {e}")
            return ""

    def load_data(self):
        """Excel ফাইল থেকে ডেটা লোড করুন"""
        try:
            self.data = pd.read_excel(self.excel_file)
            return True
        except Exception as e:
            st.error(f"❌ ডেটা লোড করতে সমস্যা হয়েছে: {str(e)}")
            return False

    def add_pdf_file(self, pdf_file):
        """PDF ফাইল থেকে টেক্সট এক্সট্র্যাক্ট করুন"""
        if not PDF_AVAILABLE:
            st.error("❌ PDF সমর্থন নেই। PyPDF2 ইনস্টল করুন।")
            return False
            
        try:
            saved_path = self.save_uploaded_file_to_data_source(pdf_file)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text_content = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += page.extract_text() + "\n"
            
            if text_content.strip():
                self.pdf_data.append({
                    'filename': pdf_file.name,
                    'content': text_content,
                    'source': 'PDF',
                    'upload_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'saved_path': saved_path
                })
                return True
            else:
                st.warning("⚠️ PDF ফাইল থেকে কোন টেক্সট পাওয়া যায়নি")
                return False
                
        except Exception as e:
            st.error(f"❌ PDF ফাইল প্রসেস করতে সমস্যা: {str(e)}")
            return False

    def add_word_file(self, word_file):
        """Word ফাইল থেকে টেক্সট এক্সট্র্যাক্ট করুন"""
        if not PDF_AVAILABLE:
            st.error("❌ Word সমর্থন নেই। python-docx ইনস্টল করুন।")
            return False
            
        try:
            saved_path = self.save_uploaded_file_to_data_source(word_file)
            doc = docx.Document(word_file)
            text_content = ""
            
            for paragraph in doc.paragraphs:
                text_content += paragraph.text + "\n"
            
            if text_content.strip():
                self.word_data.append({
                    'filename': word_file.name,
                    'content': text_content,
                    'source': 'Word',
                    'upload_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'saved_path': saved_path
                })
                return True
            else:
                st.warning("⚠️ Word ফাইল থেকে কোন টেক্সট পাওয়া যায়নি")
                return False
                
        except Exception as e:
            st.error(f"❌ Word ফাইল প্রসেস করতে সমস্যা: {str(e)}")
            return False

    def add_excel_file(self, excel_file):
        """Excel ফাইল থেকে ডেটা লোড করুন"""
        try:
            saved_path = self.save_uploaded_file_to_data_source(excel_file)
            df = pd.read_excel(excel_file)
            
            if len(df) > 0:
                text_content = ""
                for idx, row in df.iterrows():
                    row_text = " ".join([str(val) for val in row.values if pd.notna(val)])
                    text_content += row_text + "\n"
                
                self.excel_data.append({
                    'filename': excel_file.name,
                    'content': text_content,
                    'dataframe': df,
                    'source': 'Excel',
                    'upload_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'saved_path': saved_path
                })
                return True
            else:
                st.warning("⚠️ Excel ফাইলে কোন ডেটা নেই")
                return False
                
        except Exception as e:
            st.error(f"❌ Excel ফাইল প্রসেস করতে সমস্যা: {str(e)}")
            return False

    def clean_text(self, text):
        """টেক্সট পরিষ্কার এবং প্রিপ্রসেস করুন"""
        text = text.lower()
        text = re.sub(r'[^\w\s\u0980-\u09FF]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        words = text.split()
        filtered_words = [word for word in words if word not in self.bengali_stop_words]
        return ' '.join(filtered_words)

    def preprocess_data(self):
        """সার্চের জন্য ডেটা প্রিপ্রসেস করুন"""
        if self.data is None:
            return
            
        text_columns = []
        for col in self.data.columns:
            if self.data[col].dtype == 'object':
                text_columns.append(col)
        
        self.data['combined_text'] = self.data[text_columns].fillna('').astype(str).agg(' '.join, axis=1)
        self.data['cleaned_text'] = self.data['combined_text'].apply(self.clean_text)
        
        self.vectorizer = TfidfVectorizer(
            max_features=2000,
            ngram_range=(1, 3),
            min_df=1,
            stop_words=None
        )
        
        self.tfidf_matrix = self.vectorizer.fit_transform(self.data['cleaned_text'])

    def search_medicines(self, query, top_k=5):
        """প্রশ্নের ভিত্তিতে ওষুধ খুঁজুন"""
        if self.data is None or self.vectorizer is None:
            return []
        
        cleaned_query = self.clean_text(query)
        query_vector = self.vectorizer.transform([cleaned_query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.05:
                medicine_info = self.data.iloc[idx].to_dict()
                medicine_info['similarity_score'] = similarities[idx]
                results.append(medicine_info)
        
        return results
    
    def get_medicine_details(self, medicine_name):
        """নির্দিষ্ট ওষুধের বিস্তারিত তথ্য খুঁজুন"""
        if self.data is None:
            return None
        
        # Search for exact match first
        for col in self.data.columns:
            if self.data[col].dtype == 'object':
                matches = self.data[self.data[col].str.contains(medicine_name, case=False, na=False)]
                if len(matches) > 0:
                    return matches.iloc[0].to_dict()
        
        # If no exact match, use similarity search
        results = self.search_medicines(medicine_name, top_k=1)
        if results:
            return results[0]
        
        return None

def create_professional_sidebar():
    """Professional sidebar with organized layout"""
    with st.sidebar:
        # Logo and branding with professional styling
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
            <h2 style="color: white; margin: 0; font-size: 1.5rem;">💊 মেডিসিন চ্যাটবট</h2>
            <p style="color: white; margin: 0; font-size: 0.9rem;">Professional AI Assistant</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu with professional organization
        st.markdown("### 🧭 নেভিগেশন মেনু")
        page = st.selectbox(
            "পেজ নির্বাচন করুন:",
            ["🏠 হোম", "🔍 ওষুধ খুঁজুন", "📁 ফাইল আপলোড", "📊 ডেটা দেখুন", "ℹ️ সাহায্য"]
        )
        
        # Quick stats with professional layout
        if 'chatbot' in st.session_state and st.session_state.chatbot.data is not None:
            st.markdown("---")
            st.markdown("### 📊 পরিসংখ্যান")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("মোট ওষুধ", len(st.session_state.chatbot.data))
            with col2:
                st.metric("কলাম", len(st.session_state.chatbot.data.columns))
        
        # Quick search with professional styling
        st.markdown("---")
        st.markdown("### ⚡ দ্রুত খোঁজ")
        quick_search = st.text_input("ওষুধের নাম:", placeholder="যেমন: Paracetamol", key="quick_search")
        if st.button("🔍 খুঁজুন", key="quick_search_btn") and quick_search:
            st.session_state.quick_search_result = quick_search
        
        # File management with professional organization
        st.markdown("---")
        st.markdown("### 📁 ফাইল ম্যানেজমেন্ট")
        uploaded_files_count = 0
        if 'chatbot' in st.session_state:
            chatbot = st.session_state.chatbot
            uploaded_files_count = (len(chatbot.pdf_data) + len(chatbot.word_data) + 
                                  len(chatbot.excel_data) + len(chatbot.api_data))
        
        st.info(f"📁 আপলোড করা ফাইল: {uploaded_files_count}")
        
        if st.button("🗑️ সব ফাইল মুছুন", key="clear_all_files"):
            if 'chatbot' in st.session_state:
                chatbot = st.session_state.chatbot
                chatbot.pdf_data = []
                chatbot.word_data = []
                chatbot.excel_data = []
                chatbot.api_data = []
                st.success("✅ সব ফাইল মুছে ফেলা হয়েছে")
        
        return page

def create_professional_main_interface():
    """Professional main interface with organized layout and proper spacing"""
    st.markdown("## 🏠 হোম - স্মার্ট মেডিসিন চ্যাটবট")
    st.markdown("---")
    
    # Professional header with organized layout
    st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h1 style="font-size: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                   background-clip: text; margin-bottom: 1rem;">
            💊 স্মার্ট মেডিসিন চ্যাটবট
        </h1>
        <p style="font-size: 1.2rem; color: #666; margin-bottom: 2rem;">
            বুদ্ধিমত্তা সম্পন্ন AI দিয়ে ওষুধের তথ্য খুঁজে নিন
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards with professional spacing and organization
    st.markdown("### 🚀 মূল বৈশিষ্ট্যসমূহ")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 2.5rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); 
                    text-align: center; border-left: 5px solid #667eea; margin-bottom: 1.5rem; transition: all 0.3s ease;">
            <h3 style="color: #667eea; margin-bottom: 1.5rem; font-size: 2rem;">🔍</h3>
            <h4 style="margin-bottom: 1.5rem; color: #333;">স্মার্ট সার্চ</h4>
            <p style="color: #666; line-height: 1.6; margin: 0;">বাংলা ও ইংরেজি উভয় ভাষায় খুঁজুন</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 2.5rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); 
                    text-align: center; border-left: 5px solid #764ba2; margin-bottom: 1.5rem; transition: all 0.3s ease;">
            <h3 style="color: #764ba2; margin-bottom: 1.5rem; font-size: 2rem;">📁</h3>
            <h4 style="margin-bottom: 1.5rem; color: #333;">মাল্টি ফরম্যাট</h4>
            <p style="color: #666; line-height: 1.6; margin: 0;">PDF, Word, Excel ফাইল সাপোর্ট</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: white; padding: 2.5rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); 
                    text-align: center; border-left: 5px solid #2ecc71; margin-bottom: 1.5rem; transition: all 0.3s ease;">
            <h3 style="color: #2ecc71; margin-bottom: 1.5rem; font-size: 2rem;">🤖</h3>
            <h4 style="margin-bottom: 1.5rem; color: #333;">AI পাওয়ার্ড</h4>
            <p style="color: #666; line-height: 1.6; margin: 0;">মেশিন লার্নিং দিয়ে সঠিক ফলাফল</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: white; padding: 2.5rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); 
                    text-align: center; border-left: 5px solid #e74c3c; margin-bottom: 1.5rem; transition: all 0.3s ease;">
            <h3 style="color: #e74c3c; margin-bottom: 1.5rem; font-size: 2rem;">🌐</h3>
            <h4 style="margin-bottom: 1.5rem; color: #333;">API সংযোগ</h4>
            <p style="color: #666; line-height: 1.6; margin: 0;">বাহ্যিক ডেটাবেস থেকে তথ্য</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick access section with professional organization and spacing
    st.markdown("---")
    st.markdown("### ⚡ দ্রুত অ্যাক্সেস")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 ওষুধ খুঁজতে শুরু করুন", key="start_search", type="primary", use_container_width=True):
            st.session_state.page = "🔍 ওষুধ খুঁজুন"
            st.rerun()
    
    with col2:
        if st.button("📁 ফাইল আপলোড করুন", key="start_upload", type="secondary", use_container_width=True):
            st.session_state.page = "📁 ফাইল আপলোড"
            st.rerun()
    
    with col3:
        if st.button("📊 ডেটা দেখুন", key="view_data", type="secondary", use_container_width=True):
            st.session_state.page = "📊 ডেটা দেখুন"
            st.rerun()
    
    # System status section with professional organization
    if 'chatbot' in st.session_state and st.session_state.chatbot.data is not None:
        st.markdown("---")
        st.markdown("### 📊 সিস্টেম স্ট্যাটাস")
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💊 মোট ওষুধ", len(st.session_state.chatbot.data))
        
        with col2:
            st.metric("📋 কলাম সংখ্যা", len(st.session_state.chatbot.data.columns))
        
        with col3:
            st.metric("📁 আপলোড ফাইল", 
                     len(st.session_state.chatbot.pdf_data) + 
                     len(st.session_state.chatbot.word_data) + 
                     len(st.session_state.chatbot.excel_data))
        
        with col4:
            st.metric("🌐 API সংযোগ", len(st.session_state.chatbot.api_data))

def create_professional_search_interface():
    """PROFESSIONAL SEARCH INTERFACE - COMPLETELY REORGANIZED FOR BETTER UX"""
    st.markdown("## 🔍 ওষুধ খুঁজুন")
    st.markdown("---")
    
    # Search tabs with professional organization
    tab1, tab2, tab3 = st.tabs(["🔍 সাধারণ খোঁজ", "🎯 নির্দিষ্ট ওষুধ", "🌐 সব উৎস"])
    
    with tab1:
        st.markdown("### সাধারণ খোঁজ - মূল ডেটাবেস থেকে")
        st.markdown("---")
        
        # Professional search container with organized layout
        with st.container():
            # Search input and controls in organized row
            col1, col2, col3 = st.columns([4, 1, 1])
            
            with col1:
                search_query = st.text_input(
                    "আপনার প্রশ্ন লিখুন:",
                    placeholder="যেমন: জ্বরের ওষুধ কি কি আছে?",
                    key="general_search",
                    help="বাংলা বা ইংরেজি ভাষায় লিখুন"
                )
            
            with col2:
                search_results_count = st.selectbox(
                    "সার্চ টাইপ নির্বাচন করুন:",
                    [3, 5, 10],
                    index=1,
                    key="results_count"
                )
            
            with col3:
                search_btn = st.button("🔍 খুঁজুন", key="general_search_btn", type="primary", use_container_width=True)
        
        # Clear search button positioned logically below search input
        if search_query:
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🗑️ সার্চ মুছুন", key="clear_search", type="secondary"):
                    st.session_state.general_search = ""
                    st.rerun()
            st.markdown("---")
        
        # Search results with professional organization
        if search_btn and search_query and 'chatbot' in st.session_state:
            with st.spinner("🔍 খুঁজছি..."):
                results = st.session_state.chatbot.search_medicines(search_query, top_k=search_results_count)
            
            if results:
                st.success(f"✅ {len(results)} টি ওষুধ পাওয়া গেছে!")
                st.markdown("---")
                
                # Results in professional cards with organized layout
                for i, result in enumerate(results, 1):
                    with st.expander(f"🔸 ওষুধ {i}: {result.get(list(result.keys())[0], 'Unknown')}", expanded=False):
                        # Create two columns for better layout
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            # Medicine details in organized format
                            st.markdown("**📋 ওষুধের তথ্য:**")
                            for key, value in result.items():
                                if key not in ['combined_text', 'cleaned_text'] and pd.notna(value):
                                    st.markdown(f"• **{key}:** {value}")
                        
                        with col2:
                            # Similarity score in a professional metric box
                            similarity = result.get('similarity_score', 0)
                            st.metric(
                                "মিলের হার", 
                                f"{similarity:.1%}",
                                delta=f"{similarity:.1%}"
                            )
            else:
                st.warning("❌ কোন ওষুধ পাওয়া যায়নি")
                st.info("💡 **পরামর্শ:** ভিন্ন শব্দ ব্যবহার করে চেষ্টা করুন")
    
    with tab2:
        st.markdown("### নির্দিষ্ট ওষুধের তথ্য")
        st.markdown("---")
        
        # Professional layout for specific medicine search
        with st.container():
            # Search input and button in organized layout
            col1, col2 = st.columns([3, 1])
            
            with col1:
                medicine_name = st.text_input(
                    "ওষুধের সঠিক নাম লিখুন:",
                    placeholder="যেমন: Paracetamol",
                    key="specific_medicine",
                    help="ওষুধের সঠিক নাম লিখুন"
                )
            
            with col2:
                specific_search_btn = st.button(
                    "🎯 বিস্তারিত খুঁজুন", 
                    key="specific_search_btn", 
                    type="primary",
                    use_container_width=True
                )
        
        # Clear button positioned logically below search input
        if medicine_name:
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🗑️ নাম মুছুন", key="clear_specific", type="secondary"):
                    st.session_state.specific_medicine = ""
                    st.rerun()
            st.markdown("---")
        
        # Search results for specific medicine
        if specific_search_btn and medicine_name:
            if 'chatbot' in st.session_state:
                with st.spinner("🎯 খুঁজছি..."):
                    result = st.session_state.chatbot.get_medicine_details(medicine_name)
                
                if result:
                    st.success("✅ ওষুধের তথ্য পাওয়া গেছে!")
                    st.markdown("---")
                    
                    # Create professional info card with enhanced styling
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                                padding: 2rem; border-radius: 15px; margin: 1rem 0;
                                border-left: 5px solid #667eea; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
                    """, unsafe_allow_html=True)
                    
                    # Organize medicine information professionally
                    st.markdown("**💊 ওষুধের বিস্তারিত তথ্য:**")
                    for key, value in result.items():
                        if key not in ['combined_text', 'cleaned_text', 'similarity_score'] and pd.notna(value):
                            st.markdown(f"• **{key}:** {value}")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error("❌ ওষুধ পাওয়া যায়নি")
                    st.info("💡 **পরামর্শ:** সঠিক বানান ব্যবহার করুন")
    
    with tab3:
        st.markdown("### সব উৎস থেকে খোঁজ")
        st.info("📁 আপলোড করা PDF, Word, Excel এবং API ডেটা থেকে খুঁজুন")
        st.markdown("---")
        
        # Professional layout for all sources search
        with st.container():
            # Search input and button in organized layout
            col1, col2 = st.columns([3, 1])
            
            with col1:
                all_sources_query = st.text_input(
                    "খোঁজার শব্দ:",
                    placeholder="যেমন: antibiotics",
                    key="all_sources_search",
                    help="সব উৎস থেকে খোঁজার জন্য শব্দ লিখুন"
                )
            
            with col2:
                all_sources_btn = st.button(
                    "🌐 সব উৎস থেকে খুঁজুন", 
                    key="all_sources_btn", 
                    type="primary",
                    use_container_width=True
                )
        
        # Clear button positioned logically below search input
        if all_sources_query:
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🗑️ শব্দ মুছুন", key="clear_all_sources", type="secondary"):
                    st.session_state.all_sources_search = ""
                    st.rerun()
            st.markdown("---")
        
        if all_sources_btn and all_sources_query:
            st.warning("⚠️ এই ফিচারটি এখনো তৈরি হচ্ছে...")
            st.info("💡 শীঘ্রই PDF, Word, Excel এবং API থেকে সার্চ করার সুবিধা আসবে")

def main():
    # Force refresh mechanism for UI changes
    if 'ui_version' not in st.session_state:
        st.session_state.ui_version = "PROFESSIONAL_UI_v2.0"
        st.rerun()
    
    # Page configuration
    st.set_page_config(
        page_title="💊 Professional মেডিসিন চ্যাটবট",
        page_icon="💊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for professional design
    st.markdown("""
    <style>
    /* Professional styling with better spacing */
    .main > div {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Professional sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        border-right: 2px solid rgba(102, 126, 234, 0.1);
    }
    
    /* Enhanced button styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #764ba2, #667eea);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
    /* Professional input styling */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem 1rem;
        transition: all 0.3s ease;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        transform: translateY(-1px);
    }
    
    /* Professional metric styling */
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(0,0,0,0.15);
    }
    
    /* Professional expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        border: 1px solid #dee2e6;
        padding: 1rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
        transform: translateY(-1px);
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Professional tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #e9ecef;
        transform: translateY(-1px);
    }
    
    /* Professional selectbox styling */
    .stSelectbox > div > div > div {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Professional file uploader styling */
    .stFileUploader > div > div > div {
        border-radius: 12px;
        border: 2px dashed #dee2e6;
        background: #f8f9fa;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div > div > div:hover {
        border-color: #667eea;
        background: #f0f2ff;
    }
    
    /* Professional dataframe styling */
    .stDataFrame > div > div > div {
        border-radius: 12px;
        border: 1px solid #dee2e6;
        overflow: hidden;
    }
    
    /* Professional info boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Professional spinner styling */
    .stSpinner > div > div {
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Professional container spacing */
    .element-container {
        margin-bottom: 1.5rem;
    }
    
    /* Professional divider styling */
    hr {
        border: none;
        border-top: 2px solid #e0e0e0;
        margin: 2rem 0;
        border-radius: 1px;
    }
    
    /* Hide Streamlit branding for professional look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Smooth animations for better UX */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .element-container {
        animation: slideIn 0.5s ease-out;
    }
    
    /* Professional focus states */
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus-within,
    .stFileUploader > div > div > div:focus-within {
        outline: none;
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        try:
            st.session_state.chatbot = ProfessionalMedicineChatbot('medicine_data.xlsx')
            if st.session_state.chatbot.data is not None:
                st.success(f"✅ ডেটা সফলভাবে লোড হয়েছে! মোট {len(st.session_state.chatbot.data)} টি ওষুধ পাওয়া গেছে।")
        except Exception as e:
            st.error(f"❌ চ্যাটবট লোড করতে সমস্যা: {str(e)}")
            st.stop()
    
    # Create sidebar and get selected page
    selected_page = create_professional_sidebar()
    
    # Route to appropriate page
    if selected_page == "🏠 হোম":
        create_professional_main_interface()
    
    elif selected_page == "🔍 ওষুধ খুঁজুন":
        create_professional_search_interface()
    
    elif selected_page == "📁 ফাইল আপলোড":
        st.markdown("## 📁 ফাইল আপলোড করুন")
        st.info("💡 এই ফিচারটি শীঘ্রই আসবে")
    
    elif selected_page == "📊 ডেটা দেখুন":
        st.markdown("## 📊 ডেটা দেখুন")
        st.info("💡 এই ফিচারটি শীঘ্রই আসবে")
    
    elif selected_page == "ℹ️ সাহায্য":
        st.markdown("## ℹ️ সাহায্য ও নির্দেশনা")
        st.info("💡 এই ফিচারটি শীঘ্রই আসবে")
    
    # Professional footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h4>💊 নিরাপদ ব্যবহার</h4>
            <p>সবসময় ডাক্তারের পরামর্শ নিন</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h4>🔍 স্মার্ট সার্চ</h4>
            <p>AI দিয়ে সঠিক তথ্য খুঁজুন</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h4>📱 সব ডিভাইসে</h4>
            <p>মোবাইল ও কম্পিউটারে ব্যবহার করুন</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
