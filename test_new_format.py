#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
টেস্ট স্ক্রিপ্ট - নতুন সুন্দর উত্তর ফরম্যাট
"""

import streamlit as st
from medicine_chatbot import MedicineChatbot, format_structured_response, format_strict_response

def main():
    st.set_page_config(
        page_title="নতুন উত্তর ফরম্যাট টেস্ট",
        page_icon="💊",
        layout="wide"
    )
    
    st.title("💊 নতুন সুন্দর উত্তর ফরম্যাট টেস্ট")
    st.markdown("---")
    
    # চ্যাটবট ইনিশিয়ালাইজ করুন
    try:
        chatbot = MedicineChatbot('medicine_data.xlsx')
        st.success("✅ চ্যাটবট সফলভাবে লোড হয়েছে!")
    except Exception as e:
        st.error(f"❌ চ্যাটবট লোড করতে সমস্যা: {e}")
        return
    
    # টেস্ট প্রশ্ন
    test_queries = [
        "ডায়াবেটিস",
        "জ্বরের ওষুধ", 
        "মাথাব্যথা",
        "পার্শ্বপ্রতিক্রিয়া",
        "এন্টিবায়োটিক"
    ]
    
    st.subheader("🔍 টেস্ট প্রশ্ন নির্বাচন করুন:")
    selected_query = st.selectbox("প্রশ্ন নির্বাচন করুন:", test_queries)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 সাধারণ মোড")
        if st.button("সাধারণ মোডে খুঁজুন", key="normal_search"):
            excel_results = chatbot.search_medicines(selected_query, top_k=3)
            all_source_results = chatbot.search_all_sources(selected_query, top_k=5)
            response = format_structured_response(selected_query, excel_results, all_source_results)
            
            st.markdown("### ফলাফল:")
            st.markdown(f'<div class="detail-answer">{response}</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("🔒 স্ট্রিক্ট মোড")
        if st.button("স্ট্রিক্ট মোডে খুঁজুন", key="strict_search"):
            excel_results = chatbot.search_medicines(selected_query, top_k=3)
            all_source_results = chatbot.search_all_sources(selected_query, top_k=5)
            response = format_strict_response(selected_query, excel_results, all_source_results)
            
            st.markdown("### ফলাফল:")
            st.markdown(f'<div class="detail-answer">{response}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # কাস্টম প্রশ্ন
    st.subheader("✍️ কাস্টম প্রশ্ন")
    custom_query = st.text_input("আপনার প্রশ্ন লিখুন:", placeholder="যেমন: কোন ওষুধের পার্শ্বপ্রতিক্রিয়া কি?")
    
    if custom_query:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("সাধারণ মোডে খুঁজুন", key="custom_normal"):
                excel_results = chatbot.search_medicines(custom_query, top_k=3)
                all_source_results = chatbot.search_all_sources(custom_query, top_k=5)
                response = format_structured_response(custom_query, excel_results, all_source_results)
                
                st.markdown("### ফলাফল:")
                st.markdown(f'<div class="detail-answer">{response}</div>', unsafe_allow_html=True)
        
        with col2:
            if st.button("স্ট্রিক্ট মোডে খুঁজুন", key="custom_strict"):
                excel_results = chatbot.search_medicines(custom_query, top_k=3)
                all_source_results = chatbot.search_all_sources(custom_query, top_k=5)
                response = format_strict_response(custom_query, excel_results, all_source_results)
                
                st.markdown("### ফলাফল:")
                st.markdown(f'<div class="detail-answer">{response}</div>', unsafe_allow_html=True)
    
    # CSS স্টাইল
    st.markdown("""
    <style>
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
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
