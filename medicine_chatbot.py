#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💊 Digital SeBa Chatbot - বাংলা ভাষায় সম্পূর্ণ সমর্থন
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

class MedicineChatbot:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.data = None
        self.vectorizer = None
        self.tfidf_matrix = None
        self.uploaded_files = []
        self.all_sources = []
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
            self.data = pd.read_excel(self.excel_file)
            st.success(f"✅ ডেটা সফলভাবে লোড হয়েছে! মোট {len(self.data)} টি ওষুধ পাওয়া গেছে।")
        except Exception as e:
            st.error(f"❌ ডেটা লোড করতে সমস্যা হয়েছে: {str(e)}")
            return None
    
    def add_file(self, uploaded_file, file_type):
        """ফাইল যোগ করুন"""
        try:
            if file_type == "PDF":
                if not PDF_AVAILABLE:
                    st.error("❌ PDF সমর্থন নেই। PyPDF2 ইনস্টল করুন।")
                    return False
                
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                text_content = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text_content += page.extract_text() + "\n"
                
                if text_content.strip():
                    saved_path = save_uploaded_file_to_data_source(uploaded_file)
                    self.uploaded_files.append({
                        'filename': uploaded_file.name,
                        'content': text_content,
                        'source': 'PDF',
                        'upload_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'saved_path': saved_path
                    })
                    st.success(f"✅ PDF ফাইল '{uploaded_file.name}' সফলভাবে যোগ হয়েছে")
                    return True
                else:
                    st.warning("⚠️ PDF ফাইল থেকে কোন টেক্সট পাওয়া যায়নি")
                    return False
                    
            elif file_type == "Word":
                if not PDF_AVAILABLE:
                    st.error("❌ Word সমর্থন নেই। python-docx ইনস্টল করুন।")
                    return False
                
                doc = docx.Document(uploaded_file)
                text_content = ""
                
                for paragraph in doc.paragraphs:
                    text_content += paragraph.text + "\n"
                
                if text_content.strip():
                    saved_path = save_uploaded_file_to_data_source(uploaded_file)
                    self.uploaded_files.append({
                        'filename': uploaded_file.name,
                        'content': text_content,
                        'source': 'Word',
                        'upload_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'saved_path': saved_path
                    })
                    st.success(f"✅ Word ফাইল '{uploaded_file.name}' সফলভাবে যোগ হয়েছে")
                    return True
                else:
                    st.warning("⚠️ Word ফাইল থেকে কোন টেক্সট পাওয়া যায়নি")
                    return False
                    
            elif file_type == "Excel":
                df = pd.read_excel(uploaded_file)
                
                if len(df) > 0:
                    # Excel ডেটাকে টেক্সটে রূপান্তর করুন
                    text_content = ""
                    for idx, row in df.iterrows():
                        row_text = " ".join([str(val) for val in row.values if pd.notna(val)])
                        text_content += row_text + "\n"
                    
                    saved_path = save_uploaded_file_to_data_source(uploaded_file)
                    self.uploaded_files.append({
                        'filename': uploaded_file.name,
                        'content': text_content,
                        'dataframe': df,
                        'source': 'Excel',
                        'upload_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'saved_path': saved_path
                    })
                    st.success(f"✅ Excel ফাইল '{uploaded_file.name}' সফলভাবে যোগ হয়েছে ({len(df)} সারি)")
                    return True
                else:
                    st.warning("⚠️ Excel ফাইলে কোন ডেটা নেই")
                    return False
                    
        except Exception as e:
            st.error(f"❌ {file_type} ফাইল প্রসেস করতে সমস্যা: {str(e)}")
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
            
            self.uploaded_files.append({
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
        
        # আপলোড করা ফাইল যোগ করুন
        for file_item in self.uploaded_files:
            if file_item['source'] == 'Excel':
                # Excel ফাইলের জন্য প্রতিটি সারি আলাদাভাবে যোগ করুন
                for idx, row in file_item['dataframe'].iterrows():
                    self.all_sources.append({
                        'source': 'Uploaded Excel',
                        'filename': file_item['filename'],
                        'content': ' '.join([str(val) for val in row.values if pd.notna(val)]),
                        'row_index': idx,
                        'data': row.to_dict(),
                        'upload_time': file_item['upload_time']
                    })
            else:
                # PDF, Word, API এর জন্য
                self.all_sources.append({
                    'source': file_item['source'],
                    'filename': file_item.get('filename', file_item.get('url', 'Unknown')),
                    'content': file_item['content'],
                    'upload_time': file_item['upload_time']
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
    
    def search_all_sources(self, query, top_k=5, return_all=False):
        """সব উৎস থেকে সার্চ করুন
        return_all=True হলে যতগুলো ম্যাচ আছে সব ফেরত দেয়
        """
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
        if return_all or not top_k:
            return results
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

    def is_single_word(self, query: str) -> bool:
        """একটি শব্দ কিনা নির্ধারণ করুন (কমপক্ষে 2 অক্ষর)"""
        cleaned = self.clean_text(query).strip()
        parts = cleaned.split()
        return len(parts) == 1 and len(parts[0]) >= 2

    def build_full_info_response(self, query: str) -> str:
        """এক-কথার সার্চের জন্য সব উৎস থেকে বিস্তারিত তথ্য সুন্দরভাবে সাজিয়ে রেসপন্স বানান"""
        results = self.search_all_sources(query, return_all=True)
        if not results:
            return (
                "❌ **দুঃখিত, আপনার শব্দটির সাথে মিলে এমন তথ্য পাওয়া যায়নি।**\n\n"
                "💡 **পরামর্শ:** ভিন্ন শব্দ ব্যবহার করে আবার চেষ্টা করুন।"
            )

        lines = [f"## 💊 {query} সম্পর্কে বিস্তারিত তথ্য\n"]
        count = 0
        
        for item in results:
            # কনটেক্সট/ডেটা যুক্ত করুন
            if item.get('data'):
                for k, v in item['data'].items():
                    if pd.notna(v) and str(v).strip():
                        lines.append(f"**{k}:** {v}\n")
            
            if item.get('context'):
                ctx = item['context'].strip()
                if len(ctx) > 300:
                    ctx = ctx[:300] + "..."
                lines.append(f"{ctx}\n")
            else:
                # কাঁচা কনটেন্ট থেকে সীমিত অংশ
                raw = item.get('full_content', '')
                if raw:
                    snippet = raw.strip()
                    if len(snippet) > 300:
                        snippet = snippet[:300] + "..."
                    lines.append(f"{snippet}\n")
            
            lines.append("---\n")
            count += 1

        if count > 0:
            lines.append(f"**মোট {count}টি তথ্য পাওয়া গেছে**")
        return "\n".join(lines)
    
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

def format_structured_response(query: str, excel_results, all_source_results):
    """প্রশ্নের জন্য সুন্দর detail আকারে উত্তর তৈরি করুন"""
    try:
        # হাইলাইট ফাংশন
        def highlight(text: str, q: str) -> str:
            try:
                import re as _re
                tokens = [t for t in (q or '').split() if t]
                if not tokens:
                    return text
                pattern = _re.compile(r"(" + "|".join(_re.escape(t) for t in tokens) + r")", _re.IGNORECASE)
                return pattern.sub(r'<mark class="hl">\\1</mark>', text)
            except Exception:
                return text

        parts = []
        parts.append(f"## 💊 {query} সম্পর্কে তথ্য\n")

        if not excel_results and not all_source_results:
            parts.append("❌ **দুঃখিত, আপনার প্রশ্নের সাথে মিলে এমন তথ্য পাওয়া যায়নি।**\n")
            parts.append("💡 **পরামর্শ:** ভিন্ন শব্দ ব্যবহার করে আবার চেষ্টা করুন।\n")
            return "".join(parts)

        # মূল ওষুধের তথ্য
        if excel_results:
            top = excel_results[0]
            shown = 0
            for k, v in top.items():
                if k in ['combined_text', 'cleaned_text', 'similarity_score']:
                    continue
                if v is None or not str(v).strip():
                    continue
                parts.append(f"**{k}:** {v}\n")
                shown += 1
                if shown >= 8:
                    break

        # অতিরিক্ত তথ্য (উৎস উল্লেখ ছাড়া)
        if all_source_results:
            parts.append("\n### 📋 বিস্তারিত তথ্য\n")
            for i, r in enumerate(all_source_results[:3], 1):
                ctx = r.get('context') or r.get('full_content', '')
                if ctx:
                    # টেক্সট পরিষ্কার করুন
                    cleaned_ctx = ctx.strip()
                    if len(cleaned_ctx) > 200:
                        cleaned_ctx = cleaned_ctx[:200] + "..."
                    
                    parts.append(f"{cleaned_ctx}\n")
                    if i < len(all_source_results[:3]):
                        parts.append("---\n")

        return "".join(parts)
    except Exception as e:
        return f"❌ রেসপন্স ফরম্যাট করতে সমস্যা: {e}"

def format_expert_response(query: str, excel_results, all_source_results):
    """এক্সপার্ট ডেভেলপার Dibedex এর জন্য নির্দিষ্ট ফরম্যাটে উত্তর"""
    try:
        parts = []
        
        if not excel_results and not all_source_results:
            parts.append("❌ **দুঃখিত, আপনার প্রশ্নের সাথে মিলে এমন তথ্য পাওয়া যায়নি।**\n")
            return "".join(parts)

        # মূল ওষুধের তথ্য - নির্দিষ্ট ফরম্যাটে
        if excel_results:
            top = excel_results[0]
            
            # Name - সঠিক কলাম নাম ব্যবহার
            name = top.get('Name', 'N/A')
            parts.append(f"**Name:**{name}\n")
            
            # Regular Price - সঠিক কলাম নাম ব্যবহার
            price = top.get('Regular Price', 'N/A')
            parts.append(f"**Regular Price:**{price}\n")
            
            # Company Name - সঠিক কলাম নাম ব্যবহার
            company = top.get('Company Name', 'N/A')
            parts.append(f"**Company Name:**{company}\n")
            
            # Medicine Group - সঠিক কলাম নাম ব্যবহার
            group = top.get('Medicine Group', 'N/A')
            parts.append(f"**Medicine Group:**{group}\n")
            
            # কার্যকারিতা - সঠিক কলাম নাম ব্যবহার এবং পরিষ্কার করা
            uses = top.get('ওষুধের কার্যকারিতা', 'N/A')
            # "কার্যকারিতা :" অংশ সরানো
            if isinstance(uses, str) and 'কার্যকারিতা :' in uses:
                uses = uses.replace('কার্যকারিতা :', '').strip()
            parts.append(f"**ওষুধের কার্যকারিতা:**{uses}\n")
            
            # খাওয়ার নিয়ম (প্রাপ্তবয়স্ক) - সঠিক কলাম নাম ব্যবহার
            adult_dosage = top.get('খাওয়ার নিয়ম( প্রাপ্তবয়স্ক ক্ষেত্রে)', 'nan')
            parts.append(f"**খাওয়ার নিয়ম (প্রাপ্তবয়স্ক ক্ষেত্রে):**{adult_dosage}\n")
            
            # খাওয়ার নিয়ম (কিশোর) - সঠিক কলাম নাম ব্যবহার
            child_dosage = top.get('খাওয়ার নিয়ম( কিশোরদের  ক্ষেত্রে)', 'nan')
            parts.append(f"**খাওয়ার নিয়ম (কিশোরদের ক্ষেত্রে):**{child_dosage}\n")
            
            # বিস্তারিত তথ্য - কার্যকারিতা থেকে নেওয়া এবং পরিষ্কার করা
            details = top.get('ওষুধের কার্যকারিতা', 'N/A')
            if isinstance(details, str) and 'কার্যকারিতা :' in details:
                details = details.replace('কার্যকারিতা :', '').strip()
            parts.append(f"**বিস্তারিত তথ্য:**\n")
            parts.append(f"**ওষুধের বিস্তারিত তথ্য:**{details}\n")

        # অতিরিক্ত তথ্য
        if all_source_results:
            for i, r in enumerate(all_source_results[:2], 1):
                ctx = r.get('context') or r.get('full_content', '')
                if ctx:
                    cleaned_ctx = ctx.strip()
                    if len(cleaned_ctx) > 300:
                        cleaned_ctx = cleaned_ctx[:300] + "..."
                    
                    if i == 1:
                        parts.append(f"{cleaned_ctx}\n")

        return "".join(parts)
    except Exception as e:
        return f"❌ এক্সপার্ট রেসপন্স তৈরি করতে সমস্যা: {e}"
    
def format_strict_response(query: str, excel_results, all_source_results):
    """স্ট্রিক্ট মোডে সুন্দর detail আকারে উত্তর"""
    try:
        parts = []
        parts.append(f"## 💊 {query} সম্পর্কে তথ্য\n")

        chatbot = getattr(st.session_state, 'chatbot', None)
        med_details = chatbot.get_medicine_details(query) if chatbot is not None else None
        if med_details:
            for key, value in med_details.items():
                if key in ['combined_text', 'cleaned_text', 'similarity_score']:
                    continue
                if value is None or not str(value).strip():
                    continue
                parts.append(f"**{key}:** {value}\n")
            return "".join(parts)

        def tokenize(text: str) -> list:
            if chatbot is not None:
                return (chatbot.clean_text(text) or '').split()
            import re as _re
            text = text.lower()
            text = _re.sub(r'[^\w\s\u0980-\u09FF]', ' ', text)
            return [t for t in text.split() if t]

        q_tokens = set(tokenize(query))
        if not q_tokens:
            parts.append("❌ **দুঃখিত, প্রাসঙ্গিক তথ্য পাওয়া যায়নি।**\n")
            return "".join(parts)

        matches = []
        for r in (all_source_results or []):
            text = r.get('context') or r.get('full_content') or ''
            if q_tokens.issubset(set(tokenize(text))):
                matches.append(r)

        if not matches:
            parts.append("❌ **দুঃখিত, প্রাসঙ্গিক তথ্য পাওয়া যায়নি।**\n")
            return "".join(parts)

        parts.append("### 📋 বিস্তারিত তথ্য\n")
        for i, r in enumerate(matches[:3], 1):
            ctx = r.get('context') or r.get('full_content', '')
            if ctx:
                # টেক্সট পরিষ্কার করুন
                cleaned_ctx = ctx.strip()
                if len(cleaned_ctx) > 200:
                    cleaned_ctx = cleaned_ctx[:200] + "..."
                
                parts.append(f"{cleaned_ctx}\n")
                if i < len(matches[:3]):
                    parts.append("---\n")

        return "".join(parts)
    except Exception as e:
        return f"❌ স্ট্রিক্ট রেসপন্স তৈরি করতে সমস্যা: {e}"
    
    def get_medicine_categories(self):
        """ওষুধের ক্যাটাগরি পান"""
        if self.data is None:
            return []
        
        categories = []
        for col in self.data.columns:
            if col not in ['combined_text', 'cleaned_text']:
                categories.append(col)
        
        return categories
    
    def filter_by_category(self, category, value):
        """ক্যাটাগরি অনুযায়ী ফিল্টার করুন"""
        if self.data is None or category not in self.data.columns:
            return []
        
        filtered_data = self.data[self.data[category].astype(str).str.contains(value, case=False, na=False)]
        return filtered_data.to_dict('records')

def save_uploaded_file_to_data_source(uploaded_file):
    """UploadedFile ডিস্কে সেভ করুন: <script_dir>/data source/<timestamp>_<filename>"""
    try:
        base_dir = Path(__file__).resolve().parent
        data_dir = base_dir / "data source"
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

def main():
    st.set_page_config(
        page_title="Digital SeBa Chatbot",
        page_icon="💊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # কাস্টম CSS - সত্যিকারের চ্যাটবটের মত
    st.markdown("""
    <style>
    /* Logo Container */
    .logo-container {
        text-align: center;
        margin: 2rem 0;
        padding: 1rem;
    }
    
    .logo-wrapper {
        display: inline-block;
        background: white;
        border-radius: 50%;
        padding: 1rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
        border: 3px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }
    
    .logo-wrapper:hover {
        transform: scale(1.05) rotate(2deg);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
        border-color: rgba(102, 126, 234, 0.3);
        animation: logoGlow 2s ease-in-out infinite;
    }
    
    @keyframes logoGlow {
        0%, 100% { box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3); }
        50% { box-shadow: 0 12px 40px rgba(102, 126, 234, 0.5), 0 0 20px rgba(102, 126, 234, 0.3); }
    }
    
    .logo-image {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        transition: all 0.3s ease;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
    }
    
    .logo-image:hover {
        filter: drop-shadow(0 8px 16px rgba(102, 126, 234, 0.3));
        transform: scale(1.05);
    }
    
    /* Main Header */
    .main-header {
        font-size: 4rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .main-header:hover {
        transform: scale(1.02);
        text-shadow: 3px 3px 6px rgba(0,0,0,0.15);
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 0;
        height: 3px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        transition: width 0.3s ease;
        border-radius: 2px;
    }
    
    .main-header:hover::after {
        width: 200px;
    }
    
    .main-header:hover {
        transform: scale(1.02);
        text-shadow: 3px 3px 6px rgba(0,0,0,0.15);
        animation: headerGlow 2s ease-in-out infinite;
    }
    
    @keyframes headerGlow {
        0%, 100% { text-shadow: 3px 3px 6px rgba(0,0,0,0.15); }
        50% { text-shadow: 3px 3px 6px rgba(0,0,0,0.15), 0 0 20px rgba(102, 126, 234, 0.3); }
    }
    
    /* Subtitle */
    .subtitle {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
        font-style: italic;
        transition: all 0.3s ease;
        opacity: 0.8;
    }
    
    .subtitle:hover {
        opacity: 1;
        color: #667eea;
        transform: scale(1.02);
        animation: subtitleGlow 2s ease-in-out infinite;
    }
    
    @keyframes subtitleGlow {
        0%, 100% { color: #667eea; }
        50% { color: #764ba2; }
    }
    
    /* Chat Container */
    .chat-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .chat-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .chat-container:hover::before {
        opacity: 1;
    }
    
    .chat-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    
    /* Medicine Cards */
    .medicine-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .medicine-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .medicine-card:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-left-color: #764ba2;
        animation: medicineGlow 2s ease-in-out infinite;
    }
    
    @keyframes medicineGlow {
        0%, 100% { border-left-color: #764ba2; }
        50% { border-left-color: #667eea; }
    }
    
    .medicine-card:hover::before {
        opacity: 1;
    }
    
    .medicine-card::after {
        content: '💊';
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 1.5rem;
        opacity: 0.3;
        transition: all 0.3s ease;
    }
    
    .medicine-card:hover::after {
        opacity: 1;
        transform: scale(1.2) rotate(5deg);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        border: none;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #764ba2, #667eea);
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        border-radius: 30px;
        animation: buttonGlow 2s ease-in-out infinite;
    }
    
    @keyframes buttonGlow {
        0%, 100% { box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4); }
        50% { box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4), 0 0 20px rgba(102, 126, 234, 0.3); }
    }
    
    /* Search Container */
    .search-container {
        margin: 2rem 0;
        display: flex;
        justify-content: center;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .search-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.02) 0%, rgba(118, 75, 162, 0.02) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
        border-radius: 20px;
    }
    
    .search-container:hover::before {
        opacity: 1;
    }
    
    .search-bar-wrapper {
        position: relative;
        width: 100%;
        max-width: 600px;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 50px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
        border: 2px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .search-bar-wrapper:hover {
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
        border-color: rgba(102, 126, 234, 0.3);
        transform: translateY(-2px);
    }
    
    .search-bar-wrapper:focus-within {
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
        border-color: #667eea;
        transform: translateY(-2px);
        animation: float 2s ease-in-out infinite;
        background: linear-gradient(135deg, #ffffff 0%, #f0f2ff 100%);
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(-2px); }
        50% { transform: translateY(-5px); }
    }
    
    .search-icon {
        position: absolute;
        left: 20px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
        color: #667eea;
        z-index: 2;
        transition: all 0.3s ease;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: translateY(-50%) scale(1); }
        50% { transform: translateY(-50%) scale(1.1); }
        100% { transform: translateY(-50%) scale(1); }
    }
    
    .search-bar-wrapper:focus-within .search-icon {
        animation: none;
        transform: translateY(-50%) scale(1.2);
        color: #764ba2;
        animation: iconGlow 2s ease-in-out infinite;
    }
    
    @keyframes iconGlow {
        0%, 100% { color: #764ba2; }
        50% { color: #667eea; }
    }
    
    .search-input-container {
        position: relative;
        width: 100%;
    }
    
    .search-input {
        width: 100%;
        padding: 20px 20px 20px 60px;
        border: none;
        outline: none;
        font-size: 1.1rem;
        background: transparent;
        color: #333;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        transition: all 0.3s ease;
    }
    
    .search-input:focus {
        color: #667eea;
        font-weight: 500;
        transform: scale(1.01);
    }
    
    .search-input:focus::placeholder {
        color: #667eea;
        opacity: 0.7;
    }
    
    .search-input::placeholder {
        color: #999;
        font-style: italic;
    }
    
    .search-suggestions {
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: white;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.3s ease;
        z-index: 1000;
    }
    
    .search-suggestions.show {
        max-height: 300px;
        border-top: 1px solid rgba(102, 126, 234, 0.1);
        animation: slideDown 0.3s ease;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .suggestion-item {
        padding: 15px 20px;
        cursor: pointer;
        transition: all 0.2s ease;
        border-bottom: 1px solid rgba(102, 126, 234, 0.05);
        font-size: 1rem;
        color: #333;
        position: relative;
    }
    
    .suggestion-item:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        color: #667eea;
        transform: translateX(5px);
        padding-left: 25px;
    }
    
    .suggestion-item:last-child {
        border-bottom: none;
    }
    
    .suggestion-item::before {
        content: '🔍';
        margin-right: 10px;
        opacity: 0;
        transition: opacity 0.2s ease;
    }
    
    .suggestion-item:hover::before {
        opacity: 1;
        animation: suggestionGlow 2s ease-in-out infinite;
    }
    
    @keyframes suggestionGlow {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }

    /* সুন্দর Detail Answer formatting */
    .detail-answer {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.02) 0%, rgba(118, 75, 162, 0.02) 100%);
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-radius: 15px;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }
    
    .detail-answer:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.15);
    }
    
    .detail-answer h2 {
        color: #667eea;
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.75rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(102, 126, 234, 0.1);
    }
    
    .detail-answer h3 {
        color: #764ba2;
        font-size: 1.3rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-left: 4px solid #764ba2;
        padding-left: 1rem;
        font-weight: 600;
    }
    
    .detail-answer p {
        line-height: 1.8;
        margin-bottom: 1rem;
        color: #333;
        font-size: 1.1rem;
        text-align: justify;
    }
    
    .detail-answer strong {
        color: #667eea;
        font-weight: 700;
        font-size: 1.1rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
        margin-right: 0.5rem;
    }
    
    .detail-answer ul {
        margin-left: 2rem;
        margin-bottom: 1.5rem;
    }
    
    .detail-answer li {
        margin-bottom: 0.75rem;
        line-height: 1.7;
        font-size: 1.05rem;
    }
    
    .detail-answer hr {
        border: none;
        border-top: 2px solid #e0e0e0;
        margin: 2rem 0;
        border-radius: 1px;
    }
    
    mark.hl { 
        background: linear-gradient(135deg, #fff4a3 0%, #ffe066 100%); 
        padding: 0.2rem 0.5rem; 
        border-radius: 5px;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(255, 244, 163, 0.3);
    }
    
    /* Enhanced markdown styling for detail answers */
    .detail-answer h2, .detail-answer h3 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 600;
    }
    
    .detail-answer h2::before {
        content: '💊 ';
        margin-right: 0.5rem;
        font-size: 1.5rem;
        animation: pulse 2s infinite;
    }
    
    .detail-answer h3::before {
        content: '📋 ';
        margin-right: 0.5rem;
        font-size: 1.2rem;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Search Box */
    .search-box {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .search-box:focus-within {
        border-color: #667eea;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);
    }
    
    /* Stats Cards */
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        border: 2px solid transparent;
    }
    
    .stats-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .stats-card:hover::before {
        opacity: 1;
    }
    
    .stats-card:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        border: 2px solid rgba(102, 126, 234, 0.1);
    }
    
    /* Chat Messages */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .user-message::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .user-message:hover::before {
        opacity: 1;
    }
    
    .bot-message {
        background: white;
        color: #333;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        max-width: 80%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .bot-message::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .bot-message:hover::before {
        opacity: 1;
    }
    
    /* Welcome Section */
    .welcome-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .welcome-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .welcome-section:hover::before {
        opacity: 1;
    }
    
    /* Features Grid */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .features-grid::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.02) 0%, rgba(118, 75, 162, 0.02) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
        border-radius: 20px;
    }
    
    .features-grid:hover::before {
        opacity: 1;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        border: 2px solid transparent;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .feature-card:hover::before {
        opacity: 1;
    }
    
    .feature-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        border: 2px solid rgba(102, 126, 234, 0.1);
    }
    
    /* Upload Section */
    .upload-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 2px dashed #dee2e6;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .upload-section:hover {
        border-color: #667eea;
        background: linear-gradient(135deg, #f0f2ff 0%, #e8ecff 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.1);
    }
    
    .upload-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .upload-section:hover::before {
        opacity: 1;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-right: 2px solid rgba(102, 126, 234, 0.1);
    }
    
    /* Sidebar hover effects */
    .css-1d391kg:hover {
        background: linear-gradient(135deg, #f0f2ff 0%, #e8ecff 100%);
        border-right-color: rgba(102, 126, 234, 0.3);
    }
    
    /* Hide Streamlit elements */
    .stDeployButton {
        display: none;
    }
    
    #MainMenu {
        visibility: hidden;
    }
    
    footer {
        visibility: hidden;
    }
    
    /* Overall page animations */
    body {
        animation: pageLoad 1s ease-out;
    }
    
    @keyframes pageLoad {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Selection color */
    ::selection {
        background: rgba(102, 126, 234, 0.3);
        color: #333;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .search-bar-wrapper:focus-within {
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
        border-color: #667eea;
        transform: translateY(-2px);
        animation: float 2s ease-in-out infinite;
        background: linear-gradient(135deg, #ffffff 0%, #f0f2ff 100%);
    }
    
    .search-bar-wrapper:focus-within .search-icon {
        animation: none;
        transform: translateY(-50%) scale(1.2);
        color: #764ba2;
        animation: iconGlow 2s ease-in-out infinite;
    }
    
    .search-bar-wrapper:focus-within .search-input {
        color: #667eea;
        font-weight: 500;
        transform: scale(1.01);
    }
    
    .search-bar-wrapper:focus-within .search-input::placeholder {
        color: #667eea;
        opacity: 0.7;
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    
    /* Enhanced search bar animations */
    .search-bar-wrapper:focus-within::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        opacity: 1;
        animation: searchGlow 2s ease-in-out infinite;
    }
    
    @keyframes searchGlow {
        0%, 100% { opacity: 0.1; }
        50% { opacity: 0.3; }
    }
    
    /* Search input focus effects */
    .search-input:focus {
        color: #667eea;
        font-weight: 500;
        transform: scale(1.01);
        background: rgba(102, 126, 234, 0.02);
    }
    
    .search-input:focus::placeholder {
        color: #667eea;
        opacity: 0.7;
        transform: translateY(-2px);
    }
    
    /* Enhanced search bar interactions */
    .search-bar-wrapper:hover .search-icon {
        transform: translateY(-50%) scale(1.1);
        color: #764ba2;
    }
    
    .search-bar-wrapper:hover .search-input::placeholder {
        color: #667eea;
        opacity: 0.8;
    }
    
    /* Search bar active state */
    .search-bar-wrapper.active {
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.3);
        border-color: #667eea;
        transform: translateY(-3px);
    }
    
    .search-bar-wrapper.active .search-icon {
        color: #764ba2;
        animation: activeIconPulse 1.5s ease-in-out infinite;
    }
    
    @keyframes activeIconPulse {
        0%, 100% { transform: translateY(-50%) scale(1.1); }
        50% { transform: translateY(-50%) scale(1.2); }
    }
    
    /* Enhanced suggestion animations */
    .suggestion-item {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .suggestion-item::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        width: 0;
        height: 100%;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        transition: width 0.3s ease;
        z-index: -1;
    }
    
    .suggestion-item:hover::before {
        width: 100%;
    }
    
    .suggestion-item:hover {
        transform: translateX(10px) scale(1.02);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
        color: #667eea;
        font-weight: 500;
    }
    
    /* Search bar typing indicator */
    .search-bar-wrapper.typing .search-icon {
        animation: typingIndicator 1s ease-in-out infinite;
    }
    
    @keyframes typingIndicator {
        0%, 100% { transform: translateY(-50%) scale(1); }
        50% { transform: translateY(-50%) scale(1.1); }
    }
    </style>
    
    <script>
    // Enhanced search functionality
    document.addEventListener('DOMContentLoaded', function() {
        const searchInput = document.getElementById('main-search-input');
        const suggestions = document.getElementById('search-suggestions');
        const hiddenInput = document.querySelector('input[data-testid="stTextInput"]');
        
        if (searchInput && hiddenInput) {
            // Show suggestions on focus
            searchInput.addEventListener('focus', function() {
                showSuggestions();
                // Move text upward effect
                document.querySelector('.welcome-section').style.transform = 'translateY(-20px)';
                document.querySelector('.features-grid').style.transform = 'translateY(-20px)';
                document.querySelector('.search-container').style.transform = 'translateY(-10px)';
            });
            
            // Hide suggestions on blur
            searchInput.addEventListener('blur', function() {
                setTimeout(() => {
                    hideSuggestions();
                    // Reset text position
                    document.querySelector('.welcome-section').style.transform = 'translateY(0)';
                    document.querySelector('.features-grid').style.transform = 'translateY(0)';
                    document.querySelector('.search-container').style.transform = 'translateY(0)';
                }, 200);
            });
            
            // Handle input changes
            searchInput.addEventListener('input', function() {
                if (this.value.length > 0) {
                    showSuggestions();
                    // Move text upward more when typing
                    document.querySelector('.welcome-section').style.transform = 'translateY(-30px)';
                    document.querySelector('.features-grid').style.transform = 'translateY(-30px)';
                    document.querySelector('.search-container').style.transform = 'translateY(-15px)';
                    
                    // Update hidden input for Streamlit
                    hiddenInput.value = this.value;
                    hiddenInput.dispatchEvent(new Event('input', { bubbles: true }));
                } else {
                    hideSuggestions();
                    // Reset text position
                    document.querySelector('.welcome-section').style.transform = 'translateY(0)';
                    document.querySelector('.features-grid').style.transform = 'translateY(0)';
                    document.querySelector('.search-container').style.transform = 'translateY(0)';
                    
                    // Clear hidden input
                    hiddenInput.value = '';
                    hiddenInput.dispatchEvent(new Event('input', { bubbles: true }));
                }
            });
            
                    // Handle Enter key - MAIN SEARCH FUNCTIONALITY
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                const searchValue = this.value.trim();
                if (searchValue) {
                    // Set the value in Streamlit hidden search input
                    const hiddenInput = document.querySelector('input[data-testid="stTextInput"]');
                    if (hiddenInput) {
                        hiddenInput.value = searchValue;
                        hiddenInput.dispatchEvent(new Event('input', { bubbles: true }));
                        
                        // Update session state
                        if (window.parent && window.parent.postMessage) {
                            window.parent.postMessage({
                                type: 'streamlit:setComponentValue',
                                key: 'hidden_search',
                                value: searchValue
                            }, '*');
                        }
                        
                        // Trigger search automatically by finding and clicking the search button
                        setTimeout(() => {
                            const buttons = document.querySelectorAll('button');
                            let searchButton = null;
                            for (let button of buttons) {
                                if (button.textContent.includes('খুঁজুন') && !button.textContent.includes('মুছুন')) {
                                    searchButton = button;
                                    break;
                                }
                            }
                            if (searchButton) {
                                // Show loading state
                                showSearchLoading();
                                searchButton.click();
                                
                                // Hide loading after a delay
                                setTimeout(() => {
                                    hideSearchLoading();
                                }, 2000);
                            }
                        }, 100);
                    }
                    
                    // Hide suggestions
                    hideSuggestions();
                    
                    // Add visual feedback
                    searchInput.style.transform = 'scale(1.02)';
                    setTimeout(() => {
                        searchInput.style.transform = 'scale(1)';
                    }, 200);
                }
            }
        });
            
            // Add visual feedback for typing
            searchInput.addEventListener('input', function() {
                if (this.value.length > 0) {
                    this.style.borderLeft = '3px solid #667eea';
                    this.style.background = 'rgba(102, 126, 234, 0.02)';
                } else {
                    this.style.borderLeft = '';
                    this.style.background = '';
                }
            });
        }
        
        function showSuggestions() {
            if (suggestions) {
                suggestions.classList.add('show');
                // Add sample suggestions
                suggestions.innerHTML = `
                    <div class="suggestion-item">ডায়াবেটিস</div>
                    <div class="suggestion-item">জ্বরের ওষুধ</div>
                    <div class="suggestion-item">পার্শ্বপ্রতিক্রিয়া</div>
                    <div class="suggestion-item">মাথাব্যথা</div>
                    <div class="suggestion-item">এন্টিবায়োটিক</div>
                    <div class="suggestion-item">সর্দি কাশি</div>
                    <div class="suggestion-item">পেটের সমস্যা</div>
                    <div class="suggestion-item">অ্যালার্জি</div>
                `;
            }
        }
        
        function hideSuggestions() {
            if (suggestions) {
                suggestions.classList.remove('show');
            }
        }
        
        // Add click functionality to suggestions
        if (suggestions) {
            suggestions.addEventListener('click', function(e) {
                if (e.target.classList.contains('suggestion-item')) {
                    const selectedText = e.target.textContent;
                    searchInput.value = selectedText;
                    
                    // Update hidden input for Streamlit
                    const hiddenInput = document.querySelector('input[data-testid="stTextInput"]');
                    if (hiddenInput) {
                        hiddenInput.value = selectedText;
                        hiddenInput.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                    
                    // Hide suggestions
                    hideSuggestions();
                    
                    // Move text upward
                    document.querySelector('.welcome-section').style.transform = 'translateY(-30px)';
                    document.querySelector('.features-grid').style.transform = 'translateY(-30px)';
                    document.querySelector('.search-container').style.transform = 'translateY(-15px)';
                    
                    // Auto-trigger search
                    setTimeout(() => {
                        const buttons = document.querySelectorAll('button');
                        let searchButton = null;
                        for (let button of buttons) {
                            if (button.textContent.includes('খুঁজুন') && !button.textContent.includes('মুছুন')) {
                                searchButton = button;
                                break;
                            }
                        }
                        if (searchButton) {
                            // Show loading state
                            showSearchLoading();
                            searchButton.click();
                            
                            // Hide loading after a delay
                            setTimeout(() => {
                                hideSearchLoading();
                            }, 2000);
                        }
                    }, 100);
                }
            });
        }
        
        // Add keyboard navigation
        let currentSuggestion = -1;
        if (searchInput) {
            searchInput.addEventListener('keydown', function(e) {
                const suggestionItems = suggestions.querySelectorAll('.suggestion-item');
                
                if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    currentSuggestion = (currentSuggestion + 1) % suggestionItems.length;
                    updateSuggestionSelection(suggestionItems);
                } else if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    currentSuggestion = (currentSuggestion - 1 + suggestionItems.length) % suggestionItems.length;
                    updateSuggestionSelection(suggestionItems);
                } else if (e.key === 'Enter' && currentSuggestion >= 0) {
                    e.preventDefault();
                    const selectedText = suggestionItems[currentSuggestion].textContent;
                    searchInput.value = selectedText;
                    hideSuggestions();
                    currentSuggestion = -1;
                    
                    // Update hidden input for Streamlit
                    const hiddenInput = document.querySelector('input[data-testid="stTextInput"]');
                    if (hiddenInput) {
                        hiddenInput.value = selectedText;
                        hiddenInput.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                    
                    // Auto-trigger search
                    setTimeout(() => {
                        const buttons = document.querySelectorAll('button');
                        let searchButton = null;
                        for (let button of buttons) {
                            if (button.textContent.includes('খুঁজুন') && !button.textContent.includes('মুছুন')) {
                                searchButton = button;
                                break;
                            }
                        }
                        if (searchButton) {
                            // Show loading state
                            showSearchLoading();
                            searchButton.click();
                            
                            // Hide loading after a delay
                            setTimeout(() => {
                                hideSearchLoading();
                            }, 2000);
                        }
                    }, 100);
                }
            });
        }
        
        function updateSuggestionSelection(items) {
            items.forEach((item, index) => {
                if (index === currentSuggestion) {
                    item.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)';
                    item.style.color = '#667eea';
                    item.style.transform = 'translateX(10px)';
                } else {
                    item.style.background = '';
                    item.style.color = '#333';
                    item.style.transform = 'translateX(0)';
                }
            });
        }
        
        // Add real-time search suggestions based on medicine data
        function updateSearchSuggestions(query) {
            if (query.length < 2) return;
            
            // This would ideally fetch from your medicine data
            // For now, we'll use static suggestions
            const commonMedicines = [
                'ডায়াবেটিস', 'জ্বর', 'মাথাব্যথা', 'পার্শ্বপ্রতিক্রিয়া', 'এন্টিবায়োটিক',
                'সর্দি কাশি', 'পেটের সমস্যা', 'অ্যালার্জি', 'রক্তচাপ', 'হৃদরোগ',
                'ক্যান্সার', 'এডস', 'টিবি', 'ম্যালেরিয়া', 'ডেঙ্গু'
            ];
            
            const filtered = commonMedicines.filter(med => 
                med.toLowerCase().includes(query.toLowerCase())
            );
            
            if (filtered.length > 0 && suggestions) {
                suggestions.innerHTML = filtered.map(med => 
                    `<div class="suggestion-item">${med}</div>`
                ).join('');
                suggestions.classList.add('show');
            }
        }
        
        // Add real-time search as user types
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    if (this.value.length >= 2) {
                        updateSearchSuggestions(this.value);
                    } else if (this.value.length === 0) {
                        hideSuggestions();
                    }
                }, 300);
            });
            
            // Add immediate feedback for single character
            searchInput.addEventListener('input', function() {
                if (this.value.length === 1) {
                    this.style.borderLeft = '3px solid #667eea';
                    this.style.background = 'rgba(102, 126, 234, 0.02)';
                }
            });
        }
        
        // Initialize keyboard navigation
        setupKeyboardNavigation();
        
        // Add typing indicator
        function addTypingIndicator() {
            if (searchInput) {
                let typingTimer;
                searchInput.addEventListener('input', function() {
                    const wrapper = this.closest('.search-bar-wrapper');
                    if (wrapper) {
                        wrapper.classList.add('typing');
                        clearTimeout(typingTimer);
                        typingTimer = setTimeout(() => {
                            wrapper.classList.remove('typing');
                        }, 1000);
                    }
                });
            }
        }
        
        // Add active state management
        function addActiveStateManagement() {
            if (searchInput) {
                searchInput.addEventListener('focus', function() {
                    const wrapper = this.closest('.search-bar-wrapper');
                    if (wrapper) {
                        wrapper.classList.add('active');
                    }
                });
                
                searchInput.addEventListener('blur', function() {
                    const wrapper = this.closest('.search-bar-wrapper');
                    if (wrapper) {
                        wrapper.classList.remove('active');
                    }
                });
            }
        }
        
        // Initialize enhanced features
        addTypingIndicator();
        addActiveStateManagement();
        
        // Add search success feedback
        function addSearchSuccessFeedback() {
            if (searchInput) {
                searchInput.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        const wrapper = this.closest('.search-bar-wrapper');
                        if (wrapper) {
                            wrapper.style.transform = 'scale(1.02)';
                            wrapper.style.boxShadow = '0 15px 50px rgba(102, 126, 234, 0.4)';
                            
                            setTimeout(() => {
                                wrapper.style.transform = '';
                                wrapper.style.boxShadow = '';
                            }, 500);
                        }
                    }
                });
            }
        }
        
        addSearchSuccessFeedback();
        
        // Sync main search bar with hidden input
        function syncMainSearchBar() {
            const mainSearchInput = document.getElementById('main-search-input');
            const hiddenInput = document.querySelector('input[data-testid="stTextInput"]');
            
            if (mainSearchInput && hiddenInput) {
                // When main search bar changes, update hidden input
                mainSearchInput.addEventListener('input', function() {
                    hiddenInput.value = this.value;
                    hiddenInput.dispatchEvent(new Event('input', { bubbles: true }));
                    
                    // Also update the session state
                    if (window.parent && window.parent.postMessage) {
                        window.parent.postMessage({
                            type: 'streamlit:setComponentValue',
                            key: 'hidden_search',
                            value: this.value
                        }, '*');
                    }
                });
                
                // When hidden input changes, update main search bar
                hiddenInput.addEventListener('input', function() {
                    mainSearchInput.value = this.value;
                });
            }
        }
        
        // Initialize sync when page loads
        setTimeout(syncMainSearchBar, 1000);
        
        // Sync with session state on page load
        setTimeout(() => {
            const hiddenInput = document.querySelector('input[data-testid="stTextInput"]');
            const topSearchInput = document.getElementById('main-search-input');
            if (hiddenInput && topSearchInput && hiddenInput.value) {
                topSearchInput.value = hiddenInput.value;
            }
        }, 1500);
        
        // Enhanced enter key handling for main search bar
        if (searchInput) {
            searchInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    const searchValue = this.value.trim();
                    if (searchValue) {
                        // Update the hidden search input for Streamlit
                        const hiddenInput = document.querySelector('input[data-testid="stTextInput"]');
                        if (hiddenInput) {
                            hiddenInput.value = searchValue;
                            hiddenInput.dispatchEvent(new Event('input', { bubbles: true }));
                            
                            // Trigger search automatically by finding and clicking the search button
                            setTimeout(() => {
                                const buttons = document.querySelectorAll('button');
                                let searchButton = null;
                                for (let button of buttons) {
                                    if (button.textContent.includes('খুঁজুন') && !button.textContent.includes('মুছুন')) {
                                        searchButton = button;
                                        break;
                                    }
                                }
                                if (searchButton) {
                                    // Show loading state
                                    showSearchLoading();
                                    searchButton.click();
                                    
                                    // Hide loading after a delay
                                    setTimeout(() => {
                                        hideSearchLoading();
                                    }, 2000);
                                }
                            }, 100);
                        }
                        
                        // Hide suggestions
                        hideSuggestions();
                    }
                }
            });
        }
    });
    
    // Enhanced keyboard navigation for suggestions
    function setupKeyboardNavigation() {
        if (searchInput) {
            searchInput.addEventListener('keydown', function(e) {
                const suggestionItems = suggestions.querySelectorAll('.suggestion-item');
                
                if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    currentSuggestion = (currentSuggestion + 1) % suggestionItems.length;
                    updateSuggestionSelection(suggestionItems);
                    scrollToSuggestion(suggestionItems[currentSuggestion]);
                } else if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    currentSuggestion = (currentSuggestion - 1 + suggestionItems.length) % suggestionItems.length;
                    updateSuggestionSelection(suggestionItems);
                    scrollToSuggestion(suggestionItems[currentSuggestion]);
                } else if (e.key === 'Escape') {
                    hideSuggestions();
                    currentSuggestion = -1;
                }
            });
        }
    }
    
    function scrollToSuggestion(element) {
        if (element && suggestions) {
            element.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }
    
    // Enhanced suggestion handling
    function enhanceSuggestions() {
        const suggestionItems = document.querySelectorAll('.suggestion-item');
        suggestionItems.forEach(item => {
            item.addEventListener('mouseenter', function() {
                this.style.transform = 'translateX(10px) scale(1.02)';
                this.style.boxShadow = '0 4px 15px rgba(102, 126, 234, 0.2)';
            });
            
            item.addEventListener('mouseleave', function() {
                this.style.transform = 'translateX(0) scale(1)';
                this.style.boxShadow = '';
            });
        });
    }
    
    // Call enhance suggestions when showing suggestions
    const originalShowSuggestions = showSuggestions;
    showSuggestions = function() {
        originalShowSuggestions();
        setTimeout(enhanceSuggestions, 100);
    };
    
    // Add loading state for search
    function showSearchLoading() {
        const searchIcon = document.querySelector('.search-icon');
        if (searchIcon) {
            searchIcon.textContent = '⏳';
            searchIcon.style.animation = 'spin 1s linear infinite';
        }
    }
    
    function hideSearchLoading() {
        const searchIcon = document.querySelector('.search-icon');
        if (searchIcon) {
            searchIcon.textContent = '🔍';
            searchIcon.style.animation = '';
        }
    }
    
    // Add spin animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes spin {
            from { transform: translateY(-50%) rotate(0deg); }
            to { transform: translateY(-50%) rotate(360deg); }
        }
    `;
    document.head.appendChild(style);
    
            // Enhanced enter key handling with loading
        if (searchInput) {
            searchInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    const searchValue = this.value.trim();
                    if (searchValue) {
                        // Show loading state
                        showSearchLoading();
                        
                        // Update the hidden search input for Streamlit
                        const hiddenInput = document.querySelector('input[data-testid="stTextInput"]');
                        if (hiddenInput) {
                            hiddenInput.value = searchValue;
                            hiddenInput.dispatchEvent(new Event('input', { bubbles: true }));
                            
                            // Trigger search automatically
                            setTimeout(() => {
                                const buttons = document.querySelectorAll('button');
                                let searchButton = null;
                                for (let button of buttons) {
                                    if (button.textContent.includes('খুঁজুন') && !button.textContent.includes('মুছুন')) {
                                        searchButton = button;
                                        break;
                                    }
                                }
                                if (searchButton) {
                                    searchButton.click();
                                    
                                    // Hide loading after search
                                    setTimeout(() => {
                                        hideSearchLoading();
                                    }, 2000);
                                } else {
                                    hideSearchLoading();
                                }
                            }, 100);
                        }
                        
                        // Hide suggestions
                        hideSuggestions();
                    }
                }
            });
        }
    </script>
    """, unsafe_allow_html=True)
    
    # লোগো এবং হেডার সেকশন
    st.markdown("""
    <div class="logo-container">
        <div class="logo-wrapper">
            <img src="data:image/jpeg;base64,{}" alt="Chatbot Logo" class="logo-image">
        </div>
    </div>
    """.format(base64.b64encode(open("chatbot pic.jpg", "rb").read()).decode()), unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">💊 Digital SeBa Chatbot</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">আপনার স্বাস্থ্য সাথী - স্মার্ট ওষুধ পরামর্শ</p>', unsafe_allow_html=True)
    
    # Simple search section - no duplicate search bars
    
    # Initialize session state for search
    if 'main_query' not in st.session_state:
        st.session_state.main_query = ""
    
    # Anchor for scrolling to results
    st.markdown('<div id="results-top"></div>', unsafe_allow_html=True)
    # Search results display area (above search bar)
    st.markdown("### 🔍 সার্চ ফলাফল")
    
    # চ্যাট হিস্টরি
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    # উপরে শুধু একবার ফলাফল দেখান
    for message in st.session_state.chat_history:
        if message['type'] == 'user':
            st.markdown(f'<div class="user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
        else:
            # Detail আকারে উত্তর প্রদর্শন (box নয়)
            st.markdown(f'<div class="detail-answer">{message["content"]}</div>', unsafe_allow_html=True)
    
    
    # Add some spacing
    st.markdown("---")
    
    # Main search input and button on the same line
    st.markdown("### 🔍 ওষুধ খুঁজুন")
    col1, col2 = st.columns([4, 1])
    with col1:
        search_input = st.text_input("🔍 ওষুধ খুঁজুন", key="main_search", placeholder="যেমন: ডায়াবেটিস, জ্বর, Paracetamol...")
    with col2:
        search_button = st.button("খুঁজুন", key="search_btn", use_container_width=True)
    
    # Auto-search when Enter is pressed
    if search_input and search_input != st.session_state.get('last_search', ''):
        st.session_state.last_search = search_input
        if search_input.strip():
            st.session_state.main_query = search_input
            # Auto-trigger search
            st.session_state.auto_search = True
    
    # ওয়েলকাম সেকশন (ছোট করা)
    st.markdown("""
    <div class="welcome-section">
        <h3>🎯 আপনার ওষুধ সম্পর্কে জানতে চান?</h3>
        <p>আমি আপনাকে সাহায্য করব ওষুধের নাম, উপকারিতা, পার্শ্বপ্রতিক্রিয়া এবং ডোজ সম্পর্কে জানতে।</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ফিচার গ্রিড
    st.markdown("""
    <div class="features-grid">
        <div class="feature-card">
            <h3>🔍 স্মার্ট সার্চ</h3>
            <p>আপনার প্রশ্নের সঠিক উত্তর খুঁজে বের করুন</p>
        </div>
        <div class="feature-card">
            <h3>💊 বিস্তারিত তথ্য</h3>
            <p>ওষুধের সম্পূর্ণ তথ্য জানুন</p>
        </div>
        <div class="feature-card">
            <h3>🌐 বাংলা সমর্থন</h3>
            <p>আপনার ভাষায় সহজ ব্যবহার</p>
        </div>
        <div class="feature-card">
            <h3>⚡ দ্রুত ফলাফল</h3>
            <p>কয়েক সেকেন্ডে সঠিক উত্তর</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # চ্যাটবট ইনিশিয়ালাইজ করুন
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = MedicineChatbot('medicine_data.xlsx')
    
    # সাইডবার
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2>🔧 অতিরিক্ত অপশন</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # ডেটা তথ্য দেখান (শুধু মোট ওষুধ)
        if st.session_state.chatbot.data is not None:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.metric("📊 মোট ওষুধ", len(st.session_state.chatbot.data))
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Strict mode toggle
        strict_default = st.session_state.get('strict_mode', True)
        strict_mode = st.checkbox("🔒 স্ট্রিক্ট মোড (শুধু প্রাসঙ্গিক তথ্য)", value=strict_default)
        st.session_state.strict_mode = strict_mode
        
        # Expert mode toggle (Dibedex format) - FORCE ENABLED
        expert_mode = True  # Force enable for testing
        st.session_state.expert_mode = expert_mode
        st.success("✅ Expert Mode (Dibedex Format) is ENABLED")
        
        # Debug info
        st.info(f"🔍 Debug: Expert Mode = {expert_mode}, Strict Mode = {strict_mode}")
        
        # কুইক সার্চ (সহজে এক-কথার সার্চের জন্য)
        st.subheader("⚡ কুইক সার্চ")
        quick_query = st.text_input("একটি শব্দ লিখুন (যেমন: ডায়াবেটিস)", key="quick_word")
        do_quick = st.button("সব তথ্য দেখাও", key="quick_go")
        if do_quick and quick_query:
            st.session_state.chat_history.append({
                'type': 'user',
                'content': quick_query
            })
            # সব উৎস থেকে সব তথ্য
            response = st.session_state.chatbot.build_full_info_response(quick_query)
            st.session_state.chat_history.append({'type': 'bot', 'content': response})

        # ফাইল আপলোড সেকশন
        st.subheader("📁 ফাইল আপলোড করুন")
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        
        # ট্যাব সিস্টেম
        tab1, tab2, tab3, tab4 = st.tabs(["📄 PDF", "📝 Word", "📊 Excel", "🌐 API"])
        
        with tab1:
            st.write("**PDF ফাইল আপলোড করুন**")
            pdf_file = st.file_uploader("PDF ফাইল নির্বাচন করুন", type=['pdf'], key="pdf_upload")
            if pdf_file:
                if st.button("📄 PDF যোগ করুন", key="add_pdf"):
                    st.session_state.chatbot.add_file(pdf_file, "PDF")
        
        with tab2:
            st.write("**Word ফাইল আপলোড করুন**")
            word_file = st.file_uploader("Word ফাইল নির্বাচন করুন", type=['docx', 'doc'], key="word_upload")
            if word_file:
                if st.button("📝 Word যোগ করুন", key="add_word"):
                    st.session_state.chatbot.add_file(word_file, "Word")
        
        with tab3:
            st.write("**Excel ফাইল আপলোড করুন**")
            excel_file = st.file_uploader("Excel ফাইল নির্বাচন করুন", type=['xlsx', 'xls'], key="excel_upload")
            if excel_file:
                if st.button("📊 Excel যোগ করুন", key="add_excel"):
                    st.session_state.chatbot.add_file(excel_file, "Excel")
        
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
                    st.session_state.chatbot.uploaded_files = []
                    st.success("✅ সব ডেটা মুছে ফেলা হয়েছে")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # আপলোড করা ফাইল দেখান
        if st.session_state.chatbot.uploaded_files:
            st.subheader("📋 যোগ করা ডেটা")
            
            for file_item in st.session_state.chatbot.uploaded_files:
                source_icon = {
                    'PDF': '📄',
                    'Word': '📝',
                    'Excel': '📊',
                    'API': '🌐'
                }.get(file_item['source'], '📄')
                
                # সহজ ভাষায় উৎস নাম
                source_name = {
                    'PDF': 'পিডিএফ ডকুমেন্ট',
                    'Word': 'ওয়ার্ড ডকুমেন্ট', 
                    'Excel': 'এক্সেল ফাইল',
                    'API': 'অনলাইন ডেটা'
                }.get(file_item['source'], file_item['source'])
                
                filename = file_item.get('filename', file_item.get('url', 'Unknown'))
                st.info(f"{source_icon} {source_name}: {filename}")
        
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
                st.markdown("### 💊 ওষুধের তথ্য")
                for key, value in result.items():
                    if key not in ['combined_text', 'cleaned_text', 'similarity_score']:
                        st.markdown(f"**{key}:** {value}")
            else:
                st.warning("❌ ওষুধ পাওয়া যায়নি")
        
        if clear_specific:
            pass
    
    # মূল চ্যাট ইন্টারফেস
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # সার্চ টাইপ নির্বাচন
    search_type = st.radio(
        "🔍 সার্চ টাইপ নির্বাচন করুন:",
        ["📊 মূল Excel ডেটা", "🌐 সব উৎস (PDF/Word/Excel/API)"],
        horizontal=True,
        key="search_type_radio"
    )
    
    # সাজেশন ও রিসেন্ট কুয়েরি (চিপস)
    st.caption("দ্রুত সাজেশন:")
    example_queries = ["ডায়াবেটিস", "জ্বর", "পার্শ্বপ্রতিক্রিয়া", "মাথাব্যথা", "এন্টিবায়োটিক", "সর্দি কাশি"]
    eq_cols = st.columns(6)
    for i, q in enumerate(example_queries):
        if eq_cols[i % 6].button(q, key=f"exq_{i}"):
            st.session_state.main_query = q
            # Auto-trigger search for example queries
            st.session_state.chat_history.append({
                'type': 'user',
                'content': q
            })
            
            # স্ট্রাকচার্ড রেসপন্স
            excel_results = st.session_state.chatbot.search_medicines(q, top_k=5)
            all_source_results = st.session_state.chatbot.search_all_sources(q, top_k=10)
            if st.session_state.get('expert_mode', False):
                response = format_expert_response(q, excel_results, all_source_results)
            elif st.session_state.get('strict_mode', False):
                response = format_strict_response(q, excel_results, all_source_results)
            else:
                response = format_structured_response(q, excel_results, all_source_results)
            st.session_state.chat_history.append({'type': 'bot', 'content': response})

    if 'recent_queries' in st.session_state and st.session_state.recent_queries:
        st.caption("সম্প্রতি সার্চ:")
        rq_cols = st.columns(6)
        for i, q in enumerate(st.session_state.recent_queries[:12]):
            if rq_cols[i % 6].button(q, key=f"rq_{i}"):
                st.session_state.main_query = q
                # Auto-trigger search for recent queries
                st.session_state.chat_history.append({
                    'type': 'user',
                    'content': q
                })
                
                # স্ট্রাকচার্ড রেসপন্স (রিসেন্ট কুয়েরি)
                excel_results = st.session_state.chatbot.search_medicines(q, top_k=5)
                all_source_results = st.session_state.chatbot.search_all_sources(q, top_k=10)
                if st.session_state.get('expert_mode', False):
                    response = format_expert_response(q, excel_results, all_source_results)
                elif st.session_state.get('strict_mode', False):
                    response = format_strict_response(q, excel_results, all_source_results)
                else:
                    response = format_structured_response(q, excel_results, all_source_results)
                st.session_state.chat_history.append({'type': 'bot', 'content': response})
    
    # Clear and chat management buttons
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        clear_input_button = st.button("🧹 ইনপুট মুছুন", use_container_width=True)
    with c2:
        clear_button = st.button("🗑️ চ্যাট মুছুন", use_container_width=True)
    with c3:
        st.markdown("💡 সার্চ বারে টাইপ করে Enter চাপুন বা খুঁজুন বাটন চাপুন")
    
    if clear_input_button:
        st.session_state.main_query = ""
        st.session_state.last_search = ""
        st.rerun()

    if clear_button:
        st.session_state.chat_history = []

    # Process search when button is clicked or auto-search is triggered
    should_search = search_button or st.session_state.get('auto_search', False)
    
    if should_search and search_input:
        # ব্যবহারকারীর বার্তা হিস্টরিতে যোগ করুন
        st.session_state.chat_history.append({
            'type': 'user',
            'content': st.session_state.main_query
        })
        
        # রিসেন্ট কুয়েরি আপডেট
        rq = st.session_state.get('recent_queries', [])
        qtext = st.session_state.main_query
        if qtext in rq:
            rq.remove(qtext)
        rq.insert(0, qtext)
        st.session_state.recent_queries = rq[:12]

        # স্ট্রাকচার্ড রেসপন্স (মেইন সার্চ)
        excel_results = st.session_state.chatbot.search_medicines(qtext, top_k=5)
        all_source_results = st.session_state.chatbot.search_all_sources(qtext, top_k=10)
        if st.session_state.get('expert_mode', False):
            response = format_expert_response(qtext, excel_results, all_source_results)
        elif st.session_state.get('strict_mode', False):
            response = format_strict_response(qtext, excel_results, all_source_results)
        else:
            response = format_structured_response(qtext, excel_results, all_source_results)
        # বটের উত্তর হিস্টরিতে যোগ করুন
        st.session_state.chat_history.append({
            'type': 'bot',
            'content': response
        })
        # Scroll to top results area
        st.markdown("""
        <script>
        const el = document.getElementById('results-top');
        if (el) { el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
        </script>
        """, unsafe_allow_html=True)
        
        # Reset auto-search flag
        st.session_state.auto_search = False
    
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
