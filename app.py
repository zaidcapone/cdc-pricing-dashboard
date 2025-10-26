
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CDC Pricing Dashboard",
    page_icon="📊", 
    layout="wide"
)

# Custom CSS with your exact brand colors
st.markdown("""
<style>
    .main-header {
        background-color: #991B1B;
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .search-card {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        border: 2px solid #991B1B;
        margin: 1rem 0;
    }
    .stButton button {
        background-color: #991B1B;
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 8px;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header with your brand
    st.markdown("""
    <div class="main-header">
        <h1 style="margin:0;">📊 CDC Pricing Dashboard</h1>
        <p style="margin:10px 0 0 0; font-size:1.2em;">Backaldrin & Bateel • Live Price Search</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("✅ ONLINE DASHBOARD READY!")
    
    # Supplier tabs
    supplier = st.radio(
        "SELECT SUPPLIER:",
        ["Backaldrin", "Bateel"],
        horizontal=True,
        label_visibility="visible"
    )
    
    # Search section
    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    st.subheader("🔍 Search Historical Prices")
    
    col1, col2 = st.columns(2)
    with col1:
        article = st.text_input("ARTICLE NUMBER", placeholder="1-366, 1001, etc.")
    with col2:
        product = st.text_input("PRODUCT NAME", placeholder="Moist Muffin, Date Mix, etc.")
    
    if st.button("🚀 SEARCH HISTORICAL PRICES"):
        if article or product:
            st.success(f"🔍 Searching {supplier}...")
            st.info("📈 Price history will display here")
            # Demo data
            if article == "1-366":
                st.write("**Moist Muffin Vanilla Mix**")
                st.write("Prices: $2.40/kg, $2.45/kg, $2.38/kg")
            elif article == "1001":
                st.write("**Premium Date Mix**") 
                st.write("Prices: $3.20/kg, $3.25/kg")
            else:
                st.write("**Enter 1-366 or 1001 to see demo prices**")
        else:
            st.warning("Please enter article number or product name")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Features list
    st.subheader("🎯 Features")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**Supplier Switching**")
        st.write("Backaldrin ↔ Bateel")
    with col2:
        st.write("**Dual Search**")
        st.write("Article # + Product Name")
    with col3:
        st.write("**Price History**")
        st.write("Historical pricing data")

if __name__ == "__main__":
    main()
