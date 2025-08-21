#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💊 উন্নত মেডিসিন চ্যাটবট - বাংলা ভাষায় সম্পূর্ণ সমর্থন
PDF, Word, Excel, API সমর্থন সহ
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

class AdvancedMedicineChatbot:
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
            'কি', 'কোন', 'কাদের', 'কার', 'কাকে', 'কি', 'কি', 'কি', 'কি', 'কি', 
            'হয়', 'হয়েছে', 'হবে', 'করতে', 'করে', 'করবে', 'আছে', 'নেই', 'থাকবে',
            'এটা', 'এটি', 'সেটা', 'সেটি', 'এই', 'সেই', 'যে', 'যা', 'যার', 'যাদের',
            'আমি', 'আমরা', 'তুমি', 'তোমরা', 'সে', 'তারা', 'আপনি', 'আপনারা',
            'এখানে', 'সেখানে', 'যেখানে', 'কোথায়', 'কোথাও', 'কোথাও', 'কোথাও',
            'এখন', 'তখন', 'কখন', 'সবসময়', 'কখনও', 'কখনও', 'কখনও', 'কখনও',
            'ভালো', 'খারাপ', 'বড়', 'ছোট', 'নতুন', 'পুরানো', 'সুন্দর', 'কুৎসিত',
            'সহজ', 'কঠিন', 'দ্রুত', 'ধীর', 'গরম', 'ঠান্ডা', 'উষ্ণ', 'শীতল'
        ])
        self.load_data()
        self.preprocess_data()
        
def save_uploaded_file_to_data_source(uploaded_file):
    """UploadedFile ডিস্কে সেভ করুন: ./data source/<timestamp>_<filename>"""
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
            st.success(f"✅ ডেটা সফলভাবে লোড হয়েছে! মোট {len(self.data)} টি ওষুধ পাওয়া গেছে।")
        except Exception as e:
            st.error(f"❌ ডেটা লোড করতে সমস্যা হয়েছে: {str(e)}")
            return None
    
    def add_pdf_file(self, pdf_file):
        """PDF ফাইল থেকে টেক্সট এক্সট্র্যাক্ট করুন"""
        if not PDF_AVAILABLE:
            st.error("❌ PDF সমর্থন নেই। PyPDF2 ইনস্টল করুন।")
            return False
            
        try:
            saved_path = save_uploaded_file_to_data_source(pdf_file)
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
                st.success(f"✅ PDF ফাইল '{pdf_file.name}' সফলভাবে যোগ হয়েছে")
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
            saved_path = save_uploaded_file_to_data_source(word_file)
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
                st.success(f"✅ Word ফাইল '{word_file.name}' সফলভাবে যোগ হয়েছে")
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
            saved_path = save_uploaded_file_to_data_source(excel_file)
            df = pd.read_excel(excel_file)
            
            if len(df) > 0:
                # Excel ডেটাকে টেক্সটে রূপান্তর করুন
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
                st.success(f"✅ Excel ফাইল '{excel_file.name}' সফলভাবে যোগ হয়েছে ({len(df)} সারি)")
                return True
            else:
                st.warning("⚠️ Excel ফাইলে কোন ডেটা নেই")
                return False
                
        except Exception as e:
            st.error(f"❌ Excel ফাইল প্রসেস করতে সমস্যা: {str(e)}")
            return False
    
    def add_api_data(self, api_url, api_key=None):
        """API থেকে ডেটা সংগ্রহ করুন"""
        try:
            headers = {}
            if api_key:
                headers['Authorization'] = f'Bearer {api_key}'
                headers['X-API-Key'] = api_key
            
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # API ডেটাকে টেক্সটে রূপান্তর করুন
            text_content = json.dumps(data, indent=2, ensure_ascii=False)
            
            self.api_data.append({
                'url': api_url,
                'content': text_content,
                'raw_data': data,
                'source': 'API',
                'upload_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status': 'success'
            })
            
            st.success(f"✅ API ডেটা সফলভাবে যোগ হয়েছে")
            return True
            
        except requests.exceptions.RequestException as e:
            st.error(f"❌ API কল করতে সমস্যা: {str(e)}")
            return False
        except json.JSONDecodeError:
            st.error("❌ API থেকে JSON ডেটা পাওয়া যায়নি")
            return False
        except Exception as e:
            st.error(f"❌ API ডেটা প্রসেস করতে সমস্যা: {str(e)}")
            return False
    
    def update_all_sources(self):
        """সব উৎসের ডেটা একত্রিত করুন"""
        self.all_sources = []
        
        # মূল Excel ডেটা যোগ করুন
        if self.data is not None:
            for idx, row in self.data.iterrows():
                self.all_sources.append({
                    'source': 'Main Excel',
                    'filename': self.excel_file,
                    'content': ' '.join([str(val) for val in row.values if pd.notna(val)]),
                    'row_index': idx,
                    'data': row.to_dict()
                })
        
        # আপলোড করা Excel ডেটা যোগ করুন
        for excel_item in self.excel_data:
            for idx, row in excel_item['dataframe'].iterrows():
                self.all_sources.append({
                    'source': 'Uploaded Excel',
                    'filename': excel_item['filename'],
                    'content': ' '.join([str(val) for val in row.values if pd.notna(val)]),
                    'row_index': idx,
                    'data': row.to_dict(),
                    'upload_time': excel_item['upload_time']
                })
        
        # PDF ডেটা যোগ করুন
        for pdf_item in self.pdf_data:
            self.all_sources.append({
                'source': 'PDF',
                'filename': pdf_item['filename'],
                'content': pdf_item['content'],
                'upload_time': pdf_item['upload_time']
            })
        
        # Word ডেটা যোগ করুন
        for word_item in self.word_data:
            self.all_sources.append({
                'source': 'Word',
                'filename': word_item['filename'],
                'content': word_item['content'],
                'upload_time': word_item['upload_time']
            })
        
        # API ডেটা যোগ করুন
        for api_item in self.api_data:
            self.all_sources.append({
                'source': 'API',
                'url': api_item['url'],
                'content': api_item['content'],
                'upload_time': api_item['upload_time']
            })
    
    def preprocess_data(self):
        """সার্চের জন্য ডেটা প্রিপ্রসেস করুন"""
        if self.data is None:
            return
            
        # সব টেক্সট কলাম খুঁজে বের করুন
        text_columns = []
        for col in self.data.columns:
            if self.data[col].dtype == 'object':  # টেক্সট কলাম
                text_columns.append(col)
        
        # প্রতিটি ওষুধের জন্য সম্মিলিত টেক্সট তৈরি করুন
        self.data['combined_text'] = self.data[text_columns].fillna('').astype(str).agg(' '.join, axis=1)
        
        # টেক্সট পরিষ্কার করুন
        self.data['cleaned_text'] = self.data['combined_text'].apply(self.clean_text)
        
        # TF-IDF ভেক্টরাইজার তৈরি করুন
        self.vectorizer = TfidfVectorizer(
            max_features=2000,
            ngram_range=(1, 3),
            min_df=1,
            stop_words=None  # বাংলা স্টপ ওয়ার্ডস ম্যানুয়ালি হ্যান্ডল করব
        )
        
        # TF-IDF ম্যাট্রিক্স তৈরি করুন
        self.tfidf_matrix = self.vectorizer.fit_transform(self.data['cleaned_text'])
    
    def clean_text(self, text):
        """টেক্সট পরিষ্কার এবং প্রিপ্রসেস করুন"""
        # লোয়ারকেস করুন
        text = text.lower()
        
        # বিশেষ ক্যারেক্টার সরান কিন্তু বাংলা টেক্সট রাখুন
        text = re.sub(r'[^\w\s\u0980-\u09FF]', ' ', text)
        
        # অতিরিক্ত স্পেস সরান
        text = re.sub(r'\s+', ' ', text).strip()
        
        # বাংলা স্টপ ওয়ার্ডস সরান
        words = text.split()
        filtered_words = [word for word in words if word not in self.bengali_stop_words]
        
        return ' '.join(filtered_words)
    
    def search_all_sources(self, query, top_k=5):
        """সব উৎস থেকে সার্চ করুন"""
        self.update_all_sources()
        
        if not self.all_sources:
            return []
        
        results = []
        
        for source in self.all_sources:
            # টেক্সট পরিষ্কার করুন
            cleaned_content = self.clean_text(source['content'])
            cleaned_query = self.clean_text(query)
            
            # সরল কীওয়ার্ড ম্যাচিং
            query_words = cleaned_query.split()
            content_words = cleaned_content.split()
            
            # ম্যাচ স্কোর গণনা করুন
            matches = sum(1 for word in query_words if word in content_words)
            if matches > 0:
                score = matches / len(query_words)
                
                # কনটেক্সট খুঁজে বের করুন
                context = self.extract_context(source['content'], query, 200)
                
                results.append({
                    'source': source['source'],
                    'filename': source.get('filename', source.get('url', 'Unknown')),
                    'score': score,
                    'context': context,
                    'full_content': source['content'][:500] + "..." if len(source['content']) > 500 else source['content'],
                    'upload_time': source.get('upload_time', ''),
                    'data': source.get('data', {})
                })
        
        # স্কোর অনুযায়ী সাজান
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
    
    def extract_context(self, text, query, context_length=200):
        """কোয়েরির আশেপাশের কনটেক্সট এক্সট্র্যাক্ট করুন"""
        query_lower = query.lower()
        text_lower = text.lower()
        
        # কোয়েরির প্রথম ম্যাচ খুঁজুন
        start_pos = text_lower.find(query_lower)
        
        if start_pos == -1:
            # কোয়েরি শব্দগুলি খুঁজুন
            query_words = query_lower.split()
            for word in query_words:
                pos = text_lower.find(word)
                if pos != -1:
                    start_pos = pos
                    break
        
        if start_pos == -1:
            return text[:context_length] + "..." if len(text) > context_length else text
        
        # কনটেক্সট এক্সট্র্যাক্ট করুন
        start = max(0, start_pos - context_length // 2)
        end = min(len(text), start_pos + len(query) + context_length // 2)
        
        context = text[start:end]
        
        if start > 0:
            context = "..." + context
        if end < len(text):
            context = context + "..."
        
        return context
    
    def search_medicines(self, query, top_k=5):
        """প্রশ্নের ভিত্তিতে ওষুধ খুঁজুন"""
        if self.data is None or self.vectorizer is None:
            return []
        
        # প্রশ্ন পরিষ্কার করুন
        cleaned_query = self.clean_text(query)
        
        # প্রশ্নকে TF-IDF ভেক্টরে রূপান্তর করুন
        query_vector = self.vectorizer.transform([cleaned_query])
        
        # সিমিলারিটি গণনা করুন
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # শীর্ষ ম্যাচগুলি পান
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.05:  # ন্যূনতম সিমিলারিটি থ্রেশহোল্ড
                medicine_info = self.data.iloc[idx].to_dict()
                medicine_info['similarity_score'] = similarities[idx]
                results.append(medicine_info)
        
        return results
    
    def get_medicine_details(self, medicine_name):
        """নির্দিষ্ট ওষুধের বিস্তারিত তথ্য পান"""
        if self.data is None:
            return None
        
        # প্রথমে সঠিক ম্যাচ খুঁজুন
        exact_match = self.data[self.data.iloc[:, 0].str.contains(medicine_name, case=False, na=False)]
        
        if len(exact_match) > 0:
            return exact_match.iloc[0].to_dict()
        
        # সঠিক ম্যাচ না থাকলে ফাজি সার্চ ব্যবহার করুন
        results = self.search_medicines(medicine_name, top_k=1)
        if results:
            return results[0]
        
        return None

def main():
    st.set_page_config(
        page_title="💊 উন্নত মেডিসিন চ্যাটবট",
        page_icon="💊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # কাস্টম CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 3.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .chat-container {
        background: linear-gradient(135deg, #f0f2f6 0%, #e6f3ff 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .medicine-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .medicine-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .source-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .upload-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 2px dashed #dee2e6;
    }
    .stButton > button {
        background: linear-gradient(45deg, #1f77b4, #2e86ab);
        color: white;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        border: none;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #2e86ab, #1f77b4);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .search-box {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        margin: 1rem 0;
    }
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # হেডার
    st.markdown('<h1 class="main-header">💊 উন্নত মেডিসিন চ্যাটবট</h1>', unsafe_allow_html=True)
    st.markdown("### 🎯 PDF, Word, Excel, API সহ সব উৎস থেকে ওষুধের তথ্য খুঁজুন!")
    
    # চ্যাটবট ইনিশিয়ালাইজ করুন
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = AdvancedMedicineChatbot('medicine_data.xlsx')
    
    # সাইডবার
    with st.sidebar:
        st.header("🔧 অতিরিক্ত অপশন")
        
        # ডেটা তথ্য দেখান
        if st.session_state.chatbot.data is not None:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.metric("📊 মোট ওষুধ", len(st.session_state.chatbot.data))
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.metric("📋 কলাম সংখ্যা", len(st.session_state.chatbot.data.columns))
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ইউনিফাইড আপলোড সেকশন
        st.subheader("📁 সব ফাইল আপলোড করুন")
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        
        # ট্যাব সিস্টেম
        tab1, tab2, tab3, tab4 = st.tabs(["📄 PDF", "📝 Word", "📊 Excel", "🌐 API"])
        
        with tab1:
            st.write("**PDF ফাইল আপলোড করুন**")
            pdf_file = st.file_uploader("PDF ফাইল নির্বাচন করুন", type=['pdf'], key="pdf_upload")
            if pdf_file:
                if st.button("📄 PDF যোগ করুন", key="add_pdf"):
                    st.session_state.chatbot.add_pdf_file(pdf_file)
        
        with tab2:
            st.write("**Word ফাইল আপলোড করুন**")
            word_file = st.file_uploader("Word ফাইল নির্বাচন করুন", type=['docx', 'doc'], key="word_upload")
            if word_file:
                if st.button("📝 Word যোগ করুন", key="add_word"):
                    st.session_state.chatbot.add_word_file(word_file)
        
        with tab3:
            st.write("**Excel ফাইল আপলোড করুন**")
            excel_file = st.file_uploader("Excel ফাইল নির্বাচন করুন", type=['xlsx', 'xls'], key="excel_upload")
            if excel_file:
                if st.button("📊 Excel যোগ করুন", key="add_excel"):
                    st.session_state.chatbot.add_excel_file(excel_file)
        
        with tab4:
            st.write("**API সংযোগ করুন**")
            api_url = st.text_input("API URL:", placeholder="https://api.example.com/medicines", key="api_url")
            api_key = st.text_input("API Key (ঐচ্ছিক):", type="password", placeholder="your-api-key", key="api_key")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔗 API যোগ করুন", key="add_api") and api_url:
                    st.session_state.chatbot.add_api_data(api_url, api_key)
            with col2:
                if st.button("🗑️ সব মুছুন", key="clear_all"):
                    st.session_state.chatbot.pdf_data = []
                    st.session_state.chatbot.word_data = []
                    st.session_state.chatbot.excel_data = []
                    st.session_state.chatbot.api_data = []
                    st.success("✅ সব ডেটা মুছে ফেলা হয়েছে")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # আপলোড করা ফাইল দেখান
        if (st.session_state.chatbot.pdf_data or st.session_state.chatbot.word_data or 
            st.session_state.chatbot.excel_data or st.session_state.chatbot.api_data):
            st.subheader("📋 আপলোড করা ফাইল")
            
            for pdf in st.session_state.chatbot.pdf_data:
                st.info(f"📄 {pdf['filename']} ({pdf['upload_time']})")
            
            for word in st.session_state.chatbot.word_data:
                st.info(f"📝 {word['filename']} ({word['upload_time']})")
            
            for excel in st.session_state.chatbot.excel_data:
                st.info(f"📊 {excel['filename']} ({excel['upload_time']})")
            
            for api in st.session_state.chatbot.api_data:
                st.info(f"🌐 {api['url']} ({api['upload_time']})")
        
        # নির্দিষ্ট ওষুধ খুঁজুন
        st.subheader("🔍 নির্দিষ্ট ওষুধ খুঁজুন")
        specific_medicine = st.text_input("ওষুধের নাম লিখুন:", placeholder="যেমন: Paracetamol")
        
        col1, col2 = st.columns(2)
        with col1:
            search_specific = st.button("🔍 খুঁজুন")
        with col2:
            clear_specific = st.button("🗑️ মুছুন")
        
        if search_specific and specific_medicine:
            result = st.session_state.chatbot.get_medicine_details(specific_medicine)
            if result:
                st.success("✅ ওষুধ পাওয়া গেছে!")
                st.markdown('<div class="medicine-card">', unsafe_allow_html=True)
                for key, value in result.items():
                    if key not in ['combined_text', 'cleaned_text', 'similarity_score']:
                        st.write(f"**{key}:** {value}")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("❌ ওষুধ পাওয়া যায়নি")
        
        if clear_specific:
            st.rerun()
    
    # মূল চ্যাট ইন্টারফেস
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # সার্চ টাইপ নির্বাচন
    search_type = st.radio(
        "🔍 সার্চ টাইপ নির্বাচন করুন:",
        ["📊 মূল Excel ডেটা", "🌐 সব উৎস (PDF/Word/Excel/API)"],
        horizontal=True
    )
    
    # চ্যাট হিস্টরি
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # চ্যাট হিস্টরি দেখান
    for message in st.session_state.chat_history:
        if message['type'] == 'user':
            st.markdown(f"**👤 আপনি:** {message['content']}")
        else:
            st.markdown(f"**🤖 চ্যাটবট:** {message['content']}")
    
    # ব্যবহারকারীর ইনপুট
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    user_query = st.text_input("আপনার প্রশ্ন লিখুন:", placeholder="যেমন: জ্বরের ওষুধ কি কি আছে?")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        search_button = st.button("🔍 খুঁজুন")
    with col2:
        clear_button = st.button("🗑️ চ্যাট মুছুন")
    with col3:
        st.markdown("💡 **পরামর্শ:** ওষুধের নাম, উপকারিতা, পার্শ্বপ্রতিক্রিয়া সম্পর্কে জিজ্ঞাসা করুন")
    
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()
    
    if search_button and user_query:
        # ব্যবহারকারীর বার্তা হিস্টরিতে যোগ করুন
        st.session_state.chat_history.append({
            'type': 'user',
            'content': user_query
        })
        
        if search_type == "📊 মূল Excel ডেটা":
            # শুধু মূল Excel ডেটা থেকে সার্চ
            results = st.session_state.chatbot.search_medicines(user_query, top_k=3)
            
            if results:
                response = "🔍 আপনার প্রশ্নের জন্য নিম্নলিখিত ওষুধগুলি পাওয়া গেছে:\n\n"
                
                for i, result in enumerate(results, 1):
                    response += f"**{i}. {result.get(list(result.keys())[0], 'Unknown Medicine')}**\n"
                    
                    # মূল তথ্য যোগ করুন
                    for key, value in result.items():
                        if key not in ['combined_text', 'cleaned_text', 'similarity_score'] and pd.notna(value) and str(value).strip():
                            response += f"   • **{key}:** {value}\n"
                    
                    response += f"   • **মিলের হার:** {result.get('similarity_score', 0):.1%}\n\n"
            else:
                response = """❌ দুঃখিত, আপনার প্রশ্নের সাথে মিলে এমন কোন ওষুধ পাওয়া যায়নি।

💡 **পরামর্শ:**
• ভিন্ন শব্দ ব্যবহার করে চেষ্টা করুন
• ওষুধের সাধারণ নাম ব্যবহার করুন
• ইংরেজি বা বাংলা উভয় ভাষায় চেষ্টা করুন"""
        
        else:
            # সব উৎস থেকে সার্চ
            results = st.session_state.chatbot.search_all_sources(user_query, top_k=5)
            
            if results:
                response = "🔍 সব উৎস থেকে আপনার প্রশ্নের ফলাফল:\n\n"
                
                for i, result in enumerate(results, 1):
                    source_icon = {
                        'Main Excel': '📊',
                        'Uploaded Excel': '📊',
                        'PDF': '📄',
                        'Word': '📝',
                        'API': '🌐'
                    }.get(result['source'], '📄')
                    
                    response += f"**{i}. {source_icon} {result['source']} - {result['filename']}**\n"
                    response += f"   • **স্কোর:** {result['score']:.1%}\n"
                    response += f"   • **কনটেক্সট:** {result['context']}\n"
                    
                    if result['data']:
                        response += "   • **তথ্য:**\n"
                        for key, value in result['data'].items():
                            if pd.notna(value) and str(value).strip():
                                response += f"     - {key}: {value}\n"
                    
                    response += "\n"
            else:
                response = """❌ দুঃখিত, কোন উৎস থেকে আপনার প্রশ্নের সাথে মিলে এমন তথ্য পাওয়া যায়নি।

💡 **পরামর্শ:**
• PDF, Word, Excel ফাইল বা API যোগ করুন
• ভিন্ন শব্দ ব্যবহার করে চেষ্টা করুন
• ইংরেজি বা বাংলা উভয় ভাষায় চেষ্টা করুন"""
        
        # বটের উত্তর হিস্টরিতে যোগ করুন
        st.session_state.chat_history.append({
            'type': 'bot',
            'content': response
        })
        
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ফুটার
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**💊 স্বাস্থ্য সুরক্ষা**")
        st.markdown("সঠিক ওষুধ ব্যবহার করুন")
    with col2:
        st.markdown("**🔍 স্মার্ট সার্চ**")
        st.markdown("সব উৎস থেকে তথ্য")
    with col3:
        st.markdown("**🌐 বহু উৎস সমর্থন**")
        st.markdown("PDF, Word, Excel, API সহ")

if __name__ == "__main__":
    main()
