#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💊 উন্নত মেডিসিন চ্যাটবট - অরগানাইজড এবং ইউজার ফ্রেন্ডলি ভার্সন
Modern এবং Responsive Frontend Design
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

class ImprovedMedicineChatbot:
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

def create_sidebar():
    """Improved sidebar with better organization"""
    with st.sidebar:
        # Logo and branding
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 2rem;">
            <h2 style="color: white; margin: 0;">💊 মেডিসিন চ্যাটবট</h2>
            <p style="color: white; margin: 0; font-size: 0.9rem;">AI-Powered Medicine Assistant</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu
        st.markdown("### 🧭 নেভিগেশন মেনু")
        page = st.selectbox(
            "পেজ নির্বাচন করুন:",
            ["🏠 হোম", "🔍 ওষুধ খুঁজুন", "📁 ফাইল আপলোড", "📊 ডেটা দেখুন", "ℹ️ সাহায্য"]
        )
        
        # Quick stats
        if 'chatbot' in st.session_state and st.session_state.chatbot.data is not None:
            st.markdown("### 📊 পরিসংখ্যান")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("মোট ওষুধ", len(st.session_state.chatbot.data))
            with col2:
                st.metric("কলাম", len(st.session_state.chatbot.data.columns))
        
        # Quick search
        st.markdown("### ⚡ দ্রুত খোঁজ")
        quick_search = st.text_input("ওষুধের নাম:", placeholder="যেমন: Paracetamol", key="quick_search")
        if st.button("🔍 খুঁজুন", key="quick_search_btn") and quick_search:
            st.session_state.quick_search_result = quick_search
        
        # File management
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

def create_main_interface():
    """Modern main interface with card-based layout"""
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
    
    # Feature cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
                    text-align: center; border-left: 5px solid #667eea;">
            <h3 style="color: #667eea;">🔍</h3>
            <h4>স্মার্ট সার্চ</h4>
            <p>বাংলা ও ইংরেজি উভয় ভাষায় খুঁজুন</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
                    text-align: center; border-left: 5px solid #764ba2;">
            <h3 style="color: #764ba2;">📁</h3>
            <h4>মাল্টি ফরম্যাট</h4>
            <p>PDF, Word, Excel ফাইল সাপোর্ট</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
                    text-align: center; border-left: 5px solid #2ecc71;">
            <h3 style="color: #2ecc71;">🤖</h3>
            <h4>AI পাওয়ার্ড</h4>
            <p>মেশিন লার্নিং দিয়ে সঠিক ফলাফল</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
                    text-align: center; border-left: 5px solid #e74c3c;">
            <h3 style="color: #e74c3c;">🌐</h3>
            <h4>API সংযোগ</h4>
            <p>বাহ্যিক ডেটাবেস থেকে তথ্য</p>
        </div>
        """, unsafe_allow_html=True)

def create_search_interface():
    """Enhanced search interface with professional layout"""
    st.markdown("## 🔍 ওষুধ খুঁজুন")
    
    # Search tabs
    tab1, tab2, tab3 = st.tabs(["🔍 সাধারণ খোঁজ", "🎯 নির্দিষ্ট ওষুধ", "🌐 সব উৎস"])
    
    with tab1:
        st.markdown("### সাধারণ খোঁজ - মূল ডেটাবেস থেকে")
        
        # Create a professional search container
        with st.container():
            # Search input and controls in one row
            col1, col2, col3 = st.columns([4, 1, 1])
            
            with col1:
                search_query = st.text_input(
                    "আপনার প্রশ্ন লিখুন:",
                    placeholder="যেমন: জ্বরের ওষুধ কি কি আছে?",
                    key="general_search"
                )
            
            with col2:
                search_results_count = st.selectbox(
                    "ফলাফল সংখ্যা:",
                    [3, 5, 10],
                    index=1,
                    key="results_count"
                )
            
            with col3:
                search_btn = st.button("🔍 খুঁজুন", key="general_search_btn", type="primary", use_container_width=True)
        
        # Clear search button below search input
        if search_query:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🗑️ সার্চ মুছুন", key="clear_search", type="secondary"):
                    st.session_state.general_search = ""
                    st.rerun()
        
        # Search results with better organization
        if search_btn and search_query and 'chatbot' in st.session_state:
            with st.spinner("🔍 খুঁজছি..."):
                results = st.session_state.chatbot.search_medicines(search_query, top_k=search_results_count)
            
            if results:
                st.success(f"✅ {len(results)} টি ওষুধ পাওয়া গেছে!")
                
                # Results in organized cards
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
                            # Similarity score in a metric box
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
        
        # Professional layout for specific medicine search
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                medicine_name = st.text_input(
                    "ওষুধের সঠিক নাম লিখুন:",
                    placeholder="যেমন: Paracetamol",
                    key="specific_medicine"
                )
            
            with col2:
                specific_search_btn = st.button(
                    "🎯 বিস্তারিত খুঁজুন", 
                    key="specific_search_btn", 
                    type="primary",
                    use_container_width=True
                )
        
        # Clear button for specific search
        if medicine_name:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🗑️ নাম মুছুন", key="clear_specific", type="secondary"):
                    st.session_state.specific_medicine = ""
                    st.rerun()
        
        # Search results for specific medicine
        if specific_search_btn and medicine_name:
            if 'chatbot' in st.session_state:
                with st.spinner("🎯 খুঁজছি..."):
                    result = st.session_state.chatbot.get_medicine_details(medicine_name)
                
                if result:
                    st.success("✅ ওষুধের তথ্য পাওয়া গেছে!")
                    
                    # Create professional info card
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                                padding: 2rem; border-radius: 15px; margin: 1rem 0;
                                border-left: 5px solid #667eea;">
                    """, unsafe_allow_html=True)
                    
                    # Organize medicine information
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
        
        # Professional layout for all sources search
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                all_sources_query = st.text_input(
                    "খোঁজার শব্দ:",
                    placeholder="যেমন: antibiotics",
                    key="all_sources_search"
                )
            
            with col2:
                all_sources_btn = st.button(
                    "🌐 সব উৎস থেকে খুঁজুন", 
                    key="all_sources_btn", 
                    type="primary",
                    use_container_width=True
                )
        
        # Clear button for all sources search
        if all_sources_query:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🗑️ শব্দ মুছুন", key="clear_all_sources", type="secondary"):
                    st.session_state.all_sources_search = ""
                    st.rerun()
        
        if all_sources_btn and all_sources_query:
            st.warning("⚠️ এই ফিচারটি এখনো তৈরি হচ্ছে...")
            st.info("💡 শীঘ্রই PDF, Word, Excel এবং API থেকে সার্চ করার সুবিধা আসবে")

def create_file_upload_interface():
    """Enhanced file upload interface with professional layout"""
    st.markdown("## 📁 ফাইল আপলোড করুন")
    
    # Upload tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📄 PDF", "📝 Word", "📊 Excel", "🌐 API"])
    
    with tab1:
        st.markdown("### PDF ফাইল আপলোড")
        st.info("📄 মেডিসিন সংক্রান্ত PDF ফাইল আপলোড করুন")
        
        # Professional file upload container
        with st.container():
            st.markdown("---")
            
            # File uploader with better styling
            pdf_file = st.file_uploader(
                "PDF ফাইল নির্বাচন করুন:",
                type=['pdf'],
                key="pdf_upload",
                help="সর্বোচ্চ ফাইল সাইজ: 200MB"
            )
            
            if pdf_file:
                # File information in organized cards
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    <div style="background: #f0f8ff; padding: 1rem; border-radius: 10px; border-left: 4px solid #667eea;">
                        <h4 style="margin: 0; color: #667eea;">📄 ফাইল তথ্য</h4>
                        <p style="margin: 0.5rem 0;"><strong>নাম:</strong> {}</p>
                        <p style="margin: 0.5rem 0;"><strong>সাইজ:</strong> {:.1f} KB</p>
                    </div>
                    """.format(pdf_file.name, pdf_file.size / 1024), unsafe_allow_html=True)
                
                with col2:
                    if st.button("📄 PDF যোগ করুন", key="add_pdf", type="primary", use_container_width=True):
                        if 'chatbot' in st.session_state:
                            with st.spinner("PDF প্রসেস হচ্ছে..."):
                                success = st.session_state.chatbot.add_pdf_file(pdf_file)
                            if success:
                                st.success("✅ PDF ফাইল সফলভাবে যোগ হয়েছে!")
                                st.balloons()
                            else:
                                st.error("❌ PDF ফাইল যোগ করতে সমস্যা হয়েছে")
                
                st.markdown("---")
    
    with tab2:
        st.markdown("### Word ফাইল আপলোড")
        st.info("📝 মেডিসিন সংক্রান্ত Word ডকুমেন্ট আপলোড করুন")
        
        # Professional file upload container
        with st.container():
            st.markdown("---")
            
            # File uploader with better styling
            word_file = st.file_uploader(
                "Word ফাইল নির্বাচন করুন:",
                type=['docx', 'doc'],
                key="word_upload",
                help="সর্বোচ্চ ফাইল সাইজ: 200MB"
            )
            
            if word_file:
                # File information in organized cards
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    <div style="background: #f0f8ff; padding: 1rem; border-radius: 10px; border-left: 4px solid #764ba2;">
                        <h4 style="margin: 0; color: #764ba2;">📝 ফাইল তথ্য</h4>
                        <p style="margin: 0.5rem 0;"><strong>নাম:</strong> {}</p>
                        <p style="margin: 0.5rem 0;"><strong>সাইজ:</strong> {:.1f} KB</p>
                    </div>
                    """.format(word_file.name, word_file.size / 1024), unsafe_allow_html=True)
                
                with col2:
                    if st.button("📝 Word যোগ করুন", key="add_word", type="primary", use_container_width=True):
                        if 'chatbot' in st.session_state:
                            with st.spinner("Word ফাইল প্রসেস হচ্ছে..."):
                                success = st.session_state.chatbot.add_word_file(word_file)
                            if success:
                                st.success("✅ Word ফাইল সফলভাবে যোগ হয়েছে!")
                                st.balloons()
                            else:
                                st.error("❌ Word ফাইল যোগ করতে সমস্যা হয়েছে")
                
                st.markdown("---")
    
    with tab3:
        st.markdown("### Excel ফাইল আপলোড")
        st.info("📊 মেডিসিন ডেটাবেস Excel ফাইল আপলোড করুন")
        
        # Professional file upload container
        with st.container():
            st.markdown("---")
            
            # File uploader with better styling
            excel_file = st.file_uploader(
                "Excel ফাইল নির্বাচন করুন:",
                type=['xlsx', 'xls'],
                key="excel_upload",
                help="সর্বোচ্চ ফাইল সাইজ: 200MB"
            )
            
            if excel_file:
                # File information in organized cards
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    <div style="background: #f0f8ff; padding: 1rem; border-radius: 10px; border-left: 4px solid #2ecc71;">
                        <h4 style="margin: 0; color: #2ecc71;">📊 ফাইল তথ্য</h4>
                        <p style="margin: 0.5rem 0;"><strong>নাম:</strong> {}</p>
                        <p style="margin: 0.5rem 0;"><strong>সাইজ:</strong> {:.1f} KB</p>
                    </div>
                    """.format(excel_file.name, excel_file.size / 1024), unsafe_allow_html=True)
                
                with col2:
                    if st.button("📊 Excel যোগ করুন", key="add_excel", type="primary", use_container_width=True):
                        if 'chatbot' in st.session_state:
                            with st.spinner("Excel ফাইল প্রসেস হচ্ছে..."):
                                success = st.session_state.chatbot.add_excel_file(excel_file)
                            if success:
                                st.success("✅ Excel ফাইল সফলভাবে যোগ হয়েছে!")
                                st.balloons()
                            else:
                                st.error("❌ Excel ফাইল যোগ করতে সমস্যা হয়েছে")
                
                st.markdown("---")
    
    with tab4:
        st.markdown("### API সংযোগ")
        st.info("🌐 বাহ্যিক ডেটাবেস API সংযোগ করুন")
        
        # Professional API connection container
        with st.container():
            st.markdown("---")
            
            # API inputs in organized layout
            col1, col2 = st.columns(2)
            
            with col1:
                api_url = st.text_input(
                    "API URL:",
                    placeholder="https://api.example.com/medicines",
                    key="api_url",
                    help="API endpoint URL লিখুন"
                )
            
            with col2:
                api_key = st.text_input(
                    "API Key (ঐচ্ছিক):",
                    type="password",
                    placeholder="your-api-key",
                    key="api_key",
                    help="API authentication key"
                )
            
            # API connection button
            if api_url:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🔗 API সংযোগ করুন", key="add_api", type="primary", use_container_width=True):
                        st.warning("⚠️ API ফিচারটি এখনো তৈরি হচ্ছে...")
                        st.info("💡 শীঘ্রই API সংযোগের সুবিধা আসবে")
            
            st.markdown("---")
    
    # File management summary
    if 'chatbot' in st.session_state:
        chatbot = st.session_state.chatbot
        total_files = (len(chatbot.pdf_data) + len(chatbot.word_data) + 
                      len(chatbot.excel_data) + len(chatbot.api_data))
        
        if total_files > 0:
            st.markdown("### 📋 আপলোড করা ফাইলসমূহ")
            
            # Create summary cards
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📄 PDF ফাইল", len(chatbot.pdf_data))
            
            with col2:
                st.metric("📝 Word ফাইল", len(chatbot.word_data))
            
            with col3:
                st.metric("📊 Excel ফাইল", len(chatbot.excel_data))
            
            with col4:
                st.metric("🌐 API সংযোগ", len(chatbot.api_data))
            
            # Clear all files button
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🗑️ সব ফাইল মুছুন", key="clear_all_files", type="secondary"):
                    chatbot.pdf_data = []
                    chatbot.word_data = []
                    chatbot.excel_data = []
                    chatbot.api_data = []
                    st.success("✅ সব ফাইল মুছে ফেলা হয়েছে")
                    st.rerun()

def create_data_view_interface():
    """Data viewing and management interface with professional layout"""
    st.markdown("## 📊 ডেটা দেখুন")
    
    if 'chatbot' not in st.session_state or st.session_state.chatbot.data is None:
        st.warning("❌ কোন ডেটা লোড হয়নি। প্রথমে Excel ফাইল লোড করুন।")
        return
    
    data = st.session_state.chatbot.data
    
    # Data overview in professional cards
    st.markdown("### 📈 ডেটা ওভারভিউ")
    
    # Create metric cards with better styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 1.5rem; border-radius: 15px; text-align: center;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">
            <h3 style="margin: 0; font-size: 2rem;">{}</h3>
            <p style="margin: 0.5rem 0; font-size: 1.1rem;">মোট রেকর্ড</p>
        </div>
        """.format(len(data)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); 
                    color: white; padding: 1.5rem; border-radius: 15px; text-align: center;
                    box-shadow: 0 4px 15px rgba(46, 204, 113, 0.3);">
            <h3 style="margin: 0; font-size: 2rem;">{}</h3>
            <p style="margin: 0.5rem 0; font-size: 1.1rem;">কলাম সংখ্যা</p>
        </div>
        """.format(len(data.columns)), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); 
                    color: white; padding: 1.5rem; border-radius: 15px; text-align: center;
                    box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);">
            <h3 style="margin: 0; font-size: 2rem;">{}</h3>
            <p style="margin: 0.5rem 0; font-size: 1.1rem;">PDF ফাইল</p>
        </div>
        """.format(len(st.session_state.chatbot.pdf_data)), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%); 
                    color: white; padding: 1.5rem; border-radius: 15px; text-align: center;
                    box-shadow: 0 4px 15px rgba(243, 156, 18, 0.3);">
            <h3 style="margin: 0; font-size: 2rem;">{}</h3>
            <p style="margin: 0.5rem 0; font-size: 1.1rem;">Word ফাইল</p>
        </div>
        """.format(len(st.session_state.chatbot.word_data)), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Data table with professional layout
    st.markdown("### 📋 ডেটা টেবিল")
    
    # Pagination controls in organized layout
    with st.container():
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown("**পেজিনেশন সেটিংস:**")
        
        with col2:
            page_size = st.selectbox(
                "প্রতি পেজে রেকর্ড:",
                [10, 25, 50, 100],
                index=1,
                key="page_size"
            )
        
        with col3:
            total_pages = len(data) // page_size + (1 if len(data) % page_size > 0 else 0)
            page_number = st.selectbox(
                "পেজ নম্বর:",
                range(1, total_pages + 1),
                key="page_number"
            )
    
    # Calculate page boundaries
    start_idx = (page_number - 1) * page_size
    end_idx = start_idx + page_size
    
    # Page info
    st.info(f"📄 **পেজ {page_number}** - রেকর্ড {start_idx + 1} থেকে {min(end_idx, len(data))} (মোট {len(data)} রেকর্ড)")
    
    # Data table with better styling
    st.dataframe(
        data.iloc[start_idx:end_idx],
        use_container_width=True,
        height=400
    )
    
    # Pagination navigation
    if total_pages > 1:
        st.markdown("**পেজ নেভিগেশন:**")
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
        
        with col1:
            if page_number > 1:
                if st.button("⬅️ আগের পেজ", key="prev_page"):
                    st.session_state.page_number = page_number - 1
                    st.rerun()
        
        with col2:
            if page_number < total_pages:
                if st.button("পরের পেজ ➡️", key="next_page"):
                    st.session_state.page_number = page_number + 1
                    st.rerun()
        
        with col3:
            st.markdown(f"**পেজ {page_number} / {total_pages}**")
        
        with col4:
            if st.button("🏠 প্রথম পেজ", key="first_page"):
                st.session_state.page_number = 1
                st.rerun()
        
        with col5:
            if st.button("🔚 শেষ পেজ", key="last_page"):
                st.session_state.page_number = total_pages
                st.rerun()
    
    st.markdown("---")
    
    # Column information with professional layout
    st.markdown("### 📈 কলাম তথ্য")
    
    # Create column info data
    col_info = []
    for col in data.columns:
        col_info.append({
            'কলাম নাম': col,
            'ডেটা টাইপ': str(data[col].dtype),
            'মোট মান': data[col].count(),
            'খালি মান': data[col].isnull().sum(),
            'ইউনিক মান': data[col].nunique()
        })
    
    # Display column info in organized table
    col_info_df = pd.DataFrame(col_info)
    
    # Add color coding for better visualization
    def color_code_column_info(val, col_name):
        if col_name == 'খালি মান':
            if val > 0:
                return 'background-color: #ffebee; color: #c62828;'
            else:
                return 'background-color: #e8f5e8; color: #2e7d32;'
        elif col_name == 'ইউনিক মান':
            if val == 1:
                return 'background-color: #fff3e0; color: #ef6c00;'
            else:
                return 'background-color: #e3f2fd; color: #1565c0;'
        return ''
    
    # Apply styling and display
    styled_df = col_info_df.style.apply(
        lambda x: [color_code_column_info(val, col) for val, col in zip(x, col_info_df.columns)],
        axis=1
    )
    
    st.dataframe(styled_df, use_container_width=True, height=300)
    
    # Quick actions
    st.markdown("---")
    st.markdown("### ⚡ দ্রুত অ্যাকশন")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 ডেটা এক্সপোর্ট", key="export_data", type="secondary"):
            # Create CSV for download
            csv = data.to_csv(index=False)
            st.download_button(
                label="📥 CSV ডাউনলোড করুন",
                data=csv,
                file_name=f"medicine_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("🔍 ডেটা বিশ্লেষণ", key="analyze_data", type="secondary"):
            st.info("💡 ডেটা বিশ্লেষণ ফিচারটি শীঘ্রই আসবে")
    
    with col3:
        if st.button("🔄 রিফ্রেশ", key="refresh_data", type="secondary"):
            st.rerun()

def create_help_interface():
    """Help and FAQ interface"""
    st.markdown("## ℹ️ সাহায্য ও নির্দেশনা")
    
    # FAQ
    st.markdown("### ❓ প্রায়শই জিজ্ঞাসিত প্রশ্ন")
    
    with st.expander("🔍 কিভাবে ওষুধ খুঁজবো?"):
        st.markdown("""
        **সহজ পদ্ধতি:**
        1. সাইডবারে 'ওষুধ খুঁজুন' নির্বাচন করুন
        2. সার্চ বক্সে ওষুধের নাম বা উপসর্গ লিখুন
        3. 'খুঁজুন' বাটনে ক্লিক করুন
        
        **উদাহরণ:**
        - "Paracetamol"
        - "জ্বরের ওষুধ"
        - "ব্যথানাশক"
        """)
    
    with st.expander("📁 কোন ধরনের ফাইল আপলোড করতে পারি?"):
        st.markdown("""
        **সমর্থিত ফাইল ফরম্যাট:**
        - 📄 **PDF**: মেডিসিন তথ্যের PDF ডকুমেন্ট
        - 📝 **Word**: .docx এবং .doc ফাইল
        - 📊 **Excel**: .xlsx এবং .xls ডেটাবেস
        - 🌐 **API**: বাহ্যিক ডেটাবেস সংযোগ
        
        **সর্বোচ্চ ফাইল সাইজ:** 200MB
        """)
    
    with st.expander("🔧 কোন সমস্যা হলে কি করবো?"):
        st.markdown("""
        **সাধারণ সমাধান:**
        1. পেজ রিফ্রেশ করুন (F5)
        2. ফাইল আবার আপলোড করুন
        3. ইন্টারনেট সংযোগ চেক করুন
        4. ব্রাউজার ক্যাশ পরিষ্কার করুন
        
        **যোগাযোগ:** support@medicinechatbot.com
        """)
    
    # Usage guide
    st.markdown("### 📖 ব্যবহারের নির্দেশনা")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🚀 দ্রুত শুরু:**
        1. প্রথমে Excel ডেটা লোড করুন
        2. সাইডবার থেকে পেজ নির্বাচন করুন
        3. সার্চ করে ওষুধ খুঁজুন
        4. প্রয়োজনে অতিরিক্ত ফাইল যোগ করুন
        """)
    
    with col2:
        st.markdown("""
        **💡 টিপস:**
        - বাংলা ও ইংরেজি উভয় ভাষায় লিখুন
        - সংক্ষিপ্ত শব্দ ব্যবহার করুন
        - সঠিক বানান ব্যবহার করুন
        - একাধিক কীওয়ার্ড ব্যবহার করুন
        """)

def main():
    # Page configuration
    st.set_page_config(
        page_title="💊 স্মার্ট মেডিসিন চ্যাটবট",
        page_icon="💊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for modern design
    st.markdown("""
    <style>
    /* Main styling */
    .main > div {
        padding-top: 2rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #764ba2, #667eea);
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Metric styling */
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        border: 1px solid #dee2e6;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 0.5rem 1rem;
        background: #f8f9fa;
        border: 1px solid #dee2e6;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Animation */
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
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        try:
            st.session_state.chatbot = ImprovedMedicineChatbot('medicine_data.xlsx')
            if st.session_state.chatbot.data is not None:
                st.success(f"✅ ডেটা সফলভাবে লোড হয়েছে! মোট {len(st.session_state.chatbot.data)} টি ওষুধ পাওয়া গেছে।")
        except Exception as e:
            st.error(f"❌ চ্যাটবট লোড করতে সমস্যা: {str(e)}")
            st.stop()
    
    # Create sidebar and get selected page
    selected_page = create_sidebar()
    
    # Route to appropriate page
    if selected_page == "🏠 হোম":
        create_main_interface()
        
        # Quick access features on home page
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 ওষুধ খুঁজতে শুরু করুন", key="start_search", type="primary"):
                st.session_state.page = "🔍 ওষুধ খুঁজুন"
                st.rerun()
        
        with col2:
            if st.button("📁 ফাইল আপলোড করুন", key="start_upload", type="secondary"):
                st.session_state.page = "📁 ফাইল আপলোড"
                st.rerun()
        
        with col3:
            if st.button("📊 ডেটা দেখুন", key="view_data", type="secondary"):
                st.session_state.page = "📊 ডেটা দেখুন"
                st.rerun()
    
    elif selected_page == "🔍 ওষুধ খুঁজুন":
        create_search_interface()
    
    elif selected_page == "📁 ফাইল আপলোড":
        create_file_upload_interface()
    
    elif selected_page == "📊 ডেটা দেখুন":
        create_data_view_interface()
    
    elif selected_page == "ℹ️ সাহায্য":
        create_help_interface()
    
    # Footer
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
