import streamlit as st
import pandas as pd

# Custom CSS with proper contrast
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
        background-color: #FFFFFF;
        padding: 2rem;
        border-radius: 10px;
        border: 2px solid #991B1B;
        margin-bottom: 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .price-card {
        background-color: #FEE2E2;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #991B1B;
        margin: 0.5rem 0;
        color: #1F2937;
    }
    .stat-card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 8px;
        border: 2px solid #991B1B;
        text-align: center;
        color: #1F2937;
    }
    .suggestion-box {
        background-color: #FFFFFF;
        border: 1px solid #D1D5DB;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #1F2937;
    }
    /* Make all text dark for contrast */
    .stApp {
        color: #1F2937;
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
        },
        "1-368": {
            "prices": [2.35, 2.40],
            "names": ["Classic Croissant Mix", "خليط كرواسون كلاسيك"]
        }
    },
    "Bateel": {
        "1001": {
            "prices": [3.20, 3.25, 3.18],
            "names": ["Premium Date Mix", "خليط التمر الفاخر"]
        },
        "1002": {
            "prices": [4.15, 4.20],
            "names": ["Chocolate Date Spread", "معجون التمر بالشوكولاتة"]
        }
    }
}

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 style="margin:0;">📊 CDC Pricing Dashboard</h1>
        <p style="margin:10px 0 0 0;">Backaldrin & Bateel • Historical Price Tracking</p>
    </div>
    """, unsafe_allow_html=True)

    # Supplier selection
    supplier = st.radio("SELECT SUPPLIER:", ["Backaldrin", "Bateel"], horizontal=True)

    # Search section
    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    st.subheader("🔍 Search Prices")
    
    col1, col2 = st.columns(2)
    with col1:
        article = st.text_input("ARTICLE NUMBER", placeholder="e.g., 1-366, 1-367...")
    with col2:
        product = st.text_input("PRODUCT NAME", placeholder="e.g., Moist Muffin, Date Mix...")
    
    # Auto-suggestions
    search_term = article or product
    if search_term:
        suggestions = []
        supplier_data = SAMPLE_DATA[supplier]
        
        for article_num, data in supplier_data.items():
            # Match article number
            if search_term.lower() in article_num.lower():
                suggestions.append(f"🔢 {article_num} - {data['names'][0]}")
            # Match product names
            for name in data['names']:
                if search_term.lower() in name.lower():
                    suggestions.append(f"📝 {article_num} - {name}")
        
        if suggestions:
            st.markdown("**💡 Suggestions:**")
            for suggestion in list(set(suggestions))[:5]:  # Remove duplicates, show top 5
                st.markdown(f'<div class="suggestion-box">{suggestion}</div>', unsafe_allow_html=True)
    
    search_clicked = st.button("🚀 SEARCH HISTORICAL PRICES", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Handle search
    if search_clicked:
        search_term = article or product
        if not search_term:
            st.error("❌ Please enter an article number or product name")
            return
        
        # Search logic
        found = False
        for article_num, data in SAMPLE_DATA[supplier].items():
            article_match = article and article == article_num
            product_match = product and any(product.lower() in name.lower() for name in data['names'])
            
            if article_match or product_match:
                found = True
                display_results(article_num, data, supplier)
                break
        
        if not found:
            st.error(f"❌ No results found for '{search_term}' in {supplier}")

def display_results(article, data, supplier):
    st.success(f"✅ Found in {supplier}")
    
    # Product names
    st.subheader("📝 Product Names")
    for name in data['names']:
        st.markdown(f'<div class="price-card">{name}</div>', unsafe_allow_html=True)
    
    # Statistics
    prices = data['prices']
    st.subheader("📊 Price Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.metric("Total Records", len(prices))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.metric("Min Price/kg", f"${min(prices):.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.metric("Max Price/kg", f"${max(prices):.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.metric("Avg Price/kg", f"${sum(prices)/len(prices):.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Price history
    st.subheader("💵 Historical Prices (per kg)")
    cols = st.columns(4)
    for i, price in enumerate(prices):
        with cols[i % 4]:
            st.markdown(f'''
            <div style="background: #991B1B; color: white; padding: 1rem; border-radius: 8px; text-align: center; margin: 0.5rem 0;">
                <div style="font-size: 1.3em; font-weight: bold;">${price:.2f}</div>
                <div style="font-size: 0.8em;">Record #{i+1}</div>
            </div>
            ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
