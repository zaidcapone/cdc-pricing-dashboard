
import streamlit as st
import pandas as pd

st.set_page_config(page_title="CDC Pricing Dashboard", layout="wide")

st.markdown('<style>.main-header{background:#991B1B;color:white;padding:2rem;border-radius:10px;}</style>', unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>📊 CDC Pricing Dashboard</h1><p>Backaldrin & Bateel • Live Prices</p></div>', unsafe_allow_html=True)

supplier = st.radio("SELECT SUPPLIER:", ["Backaldrin", "Bateel"], horizontal=True)
article = st.text_input("🔍 ARTICLE NUMBER")
product = st.text_input("📝 PRODUCT NAME")

if st.button("🚀 SEARCH PRICES"):
    st.success(f"Searching {supplier}...")
