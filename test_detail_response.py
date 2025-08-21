#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
টেস্ট স্ক্রিপ্ট - Detail আকারে উত্তর প্রদর্শন
"""

import streamlit as st
from medicine_chatbot import MedicineChatbot, format_structured_response, format_strict_response

def main():
    st.set_page_config(
        page_title="Detail Response Test",
        page_icon="💊",
        layout="wide"
    )
    
    st.title("💊 Detail আকারে উত্তর প্রদর্শন টেস্ট")
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
    /* Detail Answer formatting - no boxes */
    .detail-answer {
        background: transparent;
        padding: 1rem 0;
        margin: 1rem 0;
        border-left: 3px solid #667eea;
        padding-left: 1rem;
    }
    
    .detail-answer h2 {
        color: #667eea;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    .detail-answer h3 {
        color: #764ba2;
        font-size: 1.2rem;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        border-left: 3px solid #764ba2;
        padding-left: 0.75rem;
    }
    
    .detail-answer p {
        line-height: 1.6;
        margin-bottom: 0.75rem;
        color: #333;
    }
    
    .detail-answer strong {
        color: #667eea;
        font-weight: 600;
    }
    
    .detail-answer ul {
        margin-left: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .detail-answer li {
        margin-bottom: 0.5rem;
        line-height: 1.5;
    }
    
    .detail-answer hr {
        border: none;
        border-top: 1px solid #e0e0e0;
        margin: 1.5rem 0;
    }
    
    mark.hl { 
        background: #fff4a3; 
        padding: 0.1rem 0.3rem; 
        border-radius: 3px;
        font-weight: 500;
    }
    
    /* Enhanced markdown styling for detail answers */
    .detail-answer h2, .detail-answer h3 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 600;
    }
    
    .detail-answer h2::before {
        content: '💊 ';
        margin-right: 0.5rem;
    }
    
    .detail-answer h3::before {
        content: '📋 ';
        margin-right: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
