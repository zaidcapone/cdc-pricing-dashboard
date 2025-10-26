import streamlit as st
import pandas as pd

# Sample data
sample_data = {
    "Backaldrin": {
        "1-366": {"prices": [2.40, 2.45, 2.38], "names": ["Moist Muffin Vanilla Mix", "موسيت مفن فانيلا ميكس"]},
        "1-367": {"prices": [2.55, 2.60], "names": ["Moist Muffin Chocolate", "موسيت مفن شوكولاتة"]},
        "1-368": {"prices": [2.35, 2.40], "names": ["Classic Croissant Mix", "خليط كرواسون كلاسيك"]}
    },
    "Bateel": {
        "1001": {"prices": [3.20, 3.25], "names": ["Premium Date Mix", "خليط التمر الفاخر"]},
        "1002": {"prices": [4.15, 4.20], "names": ["Chocolate Date Spread", "معجون التمر بالشوكولاتة"]}
    }
}

# Custom CSS with dark red theme
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
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .price-card {
        background: linear-gradient(135deg, #FEE2E2, #FECACA);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 5px solid #991B1B;
        margin: 0.5rem 0;
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 2px solid #991B1B;
        text-align: center;
        margin: 0.5rem;
    }
    .suggestion-item {
        padding: 0.75rem;
        border-bottom: 1px solid #E5E7EB;
        cursor: pointer;
    }
    .suggestion-item:hover {
        background-color: #FEE2E2;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 style="margin:0; font-size:2.5em;">📊 CDC Pricing Dashboard</h1>
        <p style="margin:10px 0 0 0; font-size:1.3em; opacity:0.9;">Backaldrin & Bateel • Live Price Tracking</p>
    </div>
    """, unsafe_allow_html=True)

    # Supplier Selection
    supplier = st.radio(
        "SELECT SUPPLIER:",
        ["Backaldrin", "Bateel"],
        horizontal=True,
        key="supplier"
    )

    # Search Section
    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    st.subheader("🔍 Search Historical Prices")
    
    col1, col2 = st.columns(2)
    
    with col1:
        article_input = st.text_input(
            "ARTICLE NUMBER",
            placeholder="e.g., 1-366, 1001...",
            key="article"
        )
    
    with col2:
        product_input = st.text_input(
            "PRODUCT NAME", 
            placeholder="e.g., Moist Muffin, Date Mix...",
            key="product"
        )
    
    # Auto-suggestions
    search_term = article_input or product_input
    if search_term:
        suggestions = []
        supplier_data = sample_data[supplier]
        
        for article, data in supplier_data.items():
            # Match by article number
            if search_term.lower() in article.lower():
                suggestions.append({
                    "type": "article",
                    "value": article,
                    "display": f"{article} - {data['names'][0]}"
                })
            # Match by product name
            for name in data['names']:
                if search_term.lower() in name.lower():
                    suggestions.append({
                        "type": "product", 
                        "value": article,
                        "display": f"{article} - {name}"
                    })
        
        if suggestions:
            st.markdown("**💡 Suggestions:**")
            for suggestion in suggestions[:6]:
                if st.button(suggestion["display"], key=suggestion["display"]):
                    st.session_state.article = suggestion["value"]
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Search Action
    if st.button("🚀 SEARCH HISTORICAL PRICES", use_container_width=True):
        search_article = article_input or (st.session_state.get('article', ''))
        
        if search_article and search_article in sample_data[supplier]:
            data = sample_data[supplier][search_article]
            
            # Product Names
            st.markdown("**📝 Product Names:**")
            for name in data['names']:
                st.markdown(f'<div class="price-card">{name}</div>', unsafe_allow_html=True)
            
            # Statistics
            prices = data['prices']
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown('<div class="stat-card">', unsafe_allow_html=True)
                st.metric("Total Records", len(prices))
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
            
            # Price History
            st.subheader("💵 Historical Prices (per kg)")
            cols = st.columns(4)
            for i, price in enumerate(prices):
                with cols[i % 4]:
                    st.markdown(f'''
                    <div style="background: #991B1B; color: white; padding: 1rem; border-radius: 8px; text-align: center;">
                        <div style="font-size: 1.5em; font-weight: bold;">${price:.2f}</div>
                        <div style="font-size: 0.8em;">Record #{i+1}</div>
                    </div>
                    ''', unsafe_allow_html=True)
        
        else:
            st.error("❌ No results found. Try a different search term.")

if __name__ == "__main__":
    main()
