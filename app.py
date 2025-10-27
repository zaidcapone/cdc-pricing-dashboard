import streamlit as st
import pandas as pd

# Initialize session state
if 'selected_article' not in st.session_state:
    st.session_state.selected_article = None

# Custom CSS with professional design
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #991B1B, #7F1D1D);
        color: white;
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .search-card {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        border: 2px solid #991B1B;
        margin-bottom: 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .price-card {
        background: linear-gradient(135deg, #FEE2E2, #FECACA);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 5px solid #991B1B;
        margin: 0.5rem 0;
        color: #1F2937;
        font-weight: 500;
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #991B1B;
        text-align: center;
        color: #1F2937;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stat-number {
        font-size: 2em;
        font-weight: bold;
        color: #991B1B;
        margin: 0;
    }
    .stat-label {
        font-size: 0.9em;
        color: #6B7280;
        margin: 0;
    }
    .price-box {
        background: #991B1B;
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Sample data
SAMPLE_DATA = {
    "Backaldrin": {
        "1-366": {
            "prices": [2.40, 2.45, 2.38, 2.42],
            "names": ["Moist Muffin Vanilla Mix", "موسيت مفن فانيلا ميكس"]
        },
        "1-367": {
            "prices": [2.55, 2.60, 2.58],
            "names": ["Moist Muffin Chocolate", "موسيت مفن شوكولاتة"]
        },
        "1-368": {
            "prices": [2.35, 2.40, 2.38],
            "names": ["Classic Croissant Mix", "خليط كرواسون كلاسيك"]
        }
    },
    "Bateel": {
        "1001": {
            "prices": [3.20, 3.25, 3.18, 3.22],
            "names": ["Premium Date Mix", "خليط التمر الفاخر"]
        },
        "1002": {
            "prices": [4.15, 4.20, 4.18],
            "names": ["Chocolate Date Spread", "معجون التمر بالشوكولاتة"]
        }
    }
}

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 style="margin:0; font-size:2.5em;">📊 CDC Pricing Dashboard</h1>
        <p style="margin:10px 0 0 0; font-size:1.2em; opacity:0.9;">Real-time Price Tracking & Historical Data</p>
    </div>
    """, unsafe_allow_html=True)

    # Supplier selection
    st.subheader("🏢 Select Supplier")
    supplier = st.radio("", ["Backaldrin", "Bateel"], horizontal=True, label_visibility="collapsed")

    # Search section
    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    st.subheader("🔍 Search Historical Prices")
    
    col1, col2 = st.columns(2)
    with col1:
        article = st.text_input("**ARTICLE NUMBER**", placeholder="e.g., 1-366, 1-367...", value=st.session_state.selected_article or "")
    with col2:
        product = st.text_input("**PRODUCT NAME**", placeholder="e.g., Moist Muffin, Date Mix...")
    
    # Auto-suggestions with click-to-select
    search_term = article or product
    if search_term:
        suggestions = []
        supplier_data = SAMPLE_DATA[supplier]
        
        for article_num, data in supplier_data.items():
            # Match article number
            if search_term.lower() in article_num.lower():
                suggestions.append({
                    "type": "article",
                    "value": article_num,
                    "display": f"🔢 {article_num} - {data['names'][0]}"
                })
            # Match product names
            for name in data['names']:
                if search_term.lower() in name.lower():
                    suggestions.append({
                        "type": "product", 
                        "value": article_num,
                        "display": f"📝 {article_num} - {name}"
                    })
        
        if suggestions:
            st.markdown("**💡 Quick Suggestions (Click to select):**")
            # Remove duplicates by article number
            unique_suggestions = {}
            for sugg in suggestions:
                if sugg["value"] not in unique_suggestions:
                    unique_suggestions[sugg["value"]] = sugg
            
            for i, suggestion in enumerate(list(unique_suggestions.values())[:4]):
                if st.button(suggestion["display"], key=f"sugg_{i}", use_container_width=True):
                    # Set the article number when clicked
                    st.session_state.selected_article = suggestion["value"]
                    st.rerun()
    
    if st.button("🚀 SEARCH HISTORICAL PRICES", use_container_width=True, type="primary"):
        handle_search(article, product, supplier)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Auto-search when suggestion is selected
    if st.session_state.selected_article and not st.session_state.get('searched', False):
        article_to_search = st.session_state.selected_article
        supplier_data = SAMPLE_DATA[supplier]
        if article_to_search in supplier_data:
            display_results(article_to_search, supplier_data[article_to_search], supplier)
            st.session_state.searched = True

def handle_search(article, product, supplier):
    search_term = article or product
    if not search_term:
        st.error("❌ Please enter an article number or product name")
        return
    
    # Clear previous selection
    if 'selected_article' in st.session_state:
        del st.session_state.selected_article
    st.session_state.searched = True
    
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
    st.success(f"✅ **Article {article}** found in **{supplier}**")
    
    # Product names
    st.subheader("📝 Product Names")
    for name in data['names']:
        st.markdown(f'<div class="price-card">{name}</div>', unsafe_allow_html=True)
    
    # Statistics
    prices = data['prices']
    st.subheader("📊 Price Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">{}</div>
            <div class="stat-label">Total Records</div>
        </div>
        """.format(len(prices)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">${:.2f}</div>
            <div class="stat-label">Min Price/kg</div>
        </div>
        """.format(min(prices)), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">${:.2f}</div>
            <div class="stat-label">Max Price/kg</div>
        </div>
        """.format(max(prices)), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">${:.2f}</div>
            <div class="stat-label">Avg Price/kg</div>
        </div>
        """.format(sum(prices)/len(prices)), unsafe_allow_html=True)
    
    # Price history
    st.subheader("💵 Historical Prices (per kg)")
    cols = st.columns(4)
    for i, price in enumerate(prices):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="price-box">
                <div style="font-size: 1.4em; font-weight: bold;">${price:.2f}</div>
                <div style="font-size: 0.8em; opacity: 0.9;">Record #{i+1}</div>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
