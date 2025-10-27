import streamlit as st
import pandas as pd

# Custom CSS for professional design
st.markdown("""
<style>
    .main-header {
        background-color: #991B1B;
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .search-card {
        background-color: #F8F9FA;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #DEE2E6;
        margin-bottom: 2rem;
    }
    .price-card {
        background-color: #FEE2E2;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #991B1B;
        margin: 0.5rem 0;
    }
    .stat-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #991B1B;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Sample data
SAMPLE_DATA = {
    "Backaldrin": {
        "1-366": {
            "prices": [2.40, 2.45, 2.38],
            "names": ["Moist Muffin Vanilla Mix", "موسيت مفن فانيلا ميكس"]
        },
        "1-367": {
            "prices": [2.55, 2.60],
            "names": ["Moist Muffin Chocolate", "موسيت مفن شوكولاتة"]
        }
    },
    "Bateel": {
        "1001": {
            "prices": [3.20, 3.25],
            "names": ["Premium Date Mix", "خليط التمر الفاخر"]
        }
    }
}

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📊 CDC Pricing Dashboard</h1>
        <p>Backaldrin & Bateel • Historical Price Tracking</p>
    </div>
    """, unsafe_allow_html=True)

    # Supplier selection
    supplier = st.radio("SELECT SUPPLIER:", ["Backaldrin", "Bateel"], horizontal=True)

    # Search section
    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    st.subheader("🔍 Search Prices")
    
    col1, col2 = st.columns(2)
    with col1:
        article = st.text_input("ARTICLE NUMBER", placeholder="e.g., 1-366")
    with col2:
        product = st.text_input("PRODUCT NAME", placeholder="e.g., Moist Muffin")
    
    search_clicked = st.button("🚀 SEARCH HISTORICAL PRICES", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Handle search
    if search_clicked:
        search_term = article or product
        if not search_term:
            st.error("Please enter an article number or product name")
            return
        
        # Search logic
        found = False
        for article_num, data in SAMPLE_DATA[supplier].items():
            if (article and article == article_num) or (product and any(product.lower() in name.lower() for name in data['names'])):
                found = True
                display_results(article_num, data, supplier)
                break
        
        if not found:
            st.error(f"No results found for '{search_term}' in {supplier}")

def display_results(article, data, supplier):
    st.success(f"✅ Found in {supplier}")
    
    # Product names
    st.subheader("Product Names")
    for name in data['names']:
        st.markdown(f'<div class="price-card">{name}</div>', unsafe_allow_html=True)
    
    # Statistics
    prices = data['prices']
    st.subheader("Price Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.metric("Records", len(prices))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.metric("Min Price", f"${min(prices):.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.metric("Max Price", f"${max(prices):.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.metric("Avg Price", f"${sum(prices)/len(prices):.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Price history
    st.subheader("Price History (per kg)")
    for i, price in enumerate(prices, 1):
        st.write(f"Record #{i}: ${price:.2f}")

if __name__ == "__main__":
    main()
