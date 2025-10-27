import streamlit as st
import pandas as pd

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
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        margin: 0.5rem 0;
    }
    .order-info {
        background: #F3F4F6;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.25rem 0;
        font-size: 0.8em;
        color: #6B7280;
    }
</style>
""", unsafe_allow_html=True)

# Sample data with order numbers
SAMPLE_DATA = {
    "Backaldrin": {
        "1-366": {
            "prices": [2.40, 2.45, 2.38, 2.42],
            "names": ["Moist Muffin Vanilla Mix", "موسيت مفن فانيلا ميكس"],
            "orders": [
                {"price": 2.40, "order_no": "ORD-001", "date": "2024-01-15"},
                {"price": 2.45, "order_no": "ORD-002", "date": "2024-02-20"},
                {"price": 2.38, "order_no": "ORD-003", "date": "2024-03-10"},
                {"price": 2.42, "order_no": "ORD-004", "date": "2024-04-05"}
            ]
        },
        "1-367": {
            "prices": [2.55, 2.60, 2.58],
            "names": ["Moist Muffin Chocolate", "موسيت مفن شوكولاتة"],
            "orders": [
                {"price": 2.55, "order_no": "ORD-005", "date": "2024-01-20"},
                {"price": 2.60, "order_no": "ORD-006", "date": "2024-02-25"},
                {"price": 2.58, "order_no": "ORD-007", "date": "2024-03-15"}
            ]
        },
        "1-368": {
            "prices": [2.35, 2.40, 2.38],
            "names": ["Classic Croissant Mix", "خليط كرواسون كلاسيك"],
            "orders": [
                {"price": 2.35, "order_no": "ORD-008", "date": "2024-01-10"},
                {"price": 2.40, "order_no": "ORD-009", "date": "2024-02-15"},
                {"price": 2.38, "order_no": "ORD-010", "date": "2024-03-20"}
            ]
        }
    },
    "Bateel": {
        "1001": {
            "prices": [3.20, 3.25, 3.18, 3.22],
            "names": ["Premium Date Mix", "خليط التمر الفاخر"],
            "orders": [
                {"price": 3.20, "order_no": "ORD-101", "date": "2024-01-18"},
                {"price": 3.25, "order_no": "ORD-102", "date": "2024-02-22"},
                {"price": 3.18, "order_no": "ORD-103", "date": "2024-03-12"},
                {"price": 3.22, "order_no": "ORD-104", "date": "2024-04-08"}
            ]
        },
        "1002": {
            "prices": [4.15, 4.20, 4.18],
            "names": ["Chocolate Date Spread", "معجون التمر بالشوكولاتة"],
            "orders": [
                {"price": 4.15, "order_no": "ORD-105", "date": "2024-01-25"},
                {"price": 4.20, "order_no": "ORD-106", "date": "2024-02-28"},
                {"price": 4.18, "order_no": "ORD-107", "date": "2024-03-18"}
            ]
        }
    }
}

def main():
    # Initialize session state
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 style="margin:0; font-size:2.5em;">📊 CDC Pricing Dashboard</h1>
        <p style="margin:10px 0 0 0; font-size:1.2em; opacity:0.9;">Professional Price Tracking • Ready for Business Use</p>
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
        article = st.text_input("**ARTICLE NUMBER**", placeholder="e.g., 1-366, 1-367...")
    with col2:
        product = st.text_input("**PRODUCT NAME**", placeholder="e.g., Moist Muffin, Date Mix...")
    
    # Auto-suggestions
    search_term = article or product
    if search_term:
        suggestions = get_suggestions(search_term, supplier, SAMPLE_DATA)
        if suggestions:
            st.markdown("**💡 Quick Suggestions:**")
            for i, suggestion in enumerate(suggestions[:4]):
                with st.form(key=f"form_{i}"):
                    if st.form_submit_button(suggestion["display"], use_container_width=True):
                        st.session_state.search_results = {
                            "article": suggestion["value"],
                            "supplier": supplier
                        }
                        st.rerun()
    
    # Manual search
    if st.button("🚀 SEARCH HISTORICAL PRICES", use_container_width=True, type="primary"):
        handle_search(article, product, supplier, SAMPLE_DATA)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Display results from session state
    if st.session_state.search_results:
        display_from_session_state(SAMPLE_DATA)

def get_suggestions(search_term, supplier, data):
    suggestions = []
    supplier_data = data[supplier]
    
    for article_num, article_data in supplier_data.items():
        if search_term.lower() in article_num.lower():
            suggestions.append({
                "type": "article",
                "value": article_num,
                "display": f"🔢 {article_num} - {article_data['names'][0] if article_data['names'] else 'No Name'}"
            })
        for name in article_data['names']:
            if search_term.lower() in name.lower():
                suggestions.append({
                    "type": "product", 
                    "value": article_num,
                    "display": f"📝 {article_num} - {name}"
                })
    
    # Remove duplicates
    unique_suggestions = {}
    for sugg in suggestions:
        if sugg["value"] not in unique_suggestions:
            unique_suggestions[sugg["value"]] = sugg
    
    return list(unique_suggestions.values())

def handle_search(article, product, supplier, data):
    search_term = article or product
    if not search_term:
        st.error("❌ Please enter an article number or product name")
        return
    
    found = False
    for article_num, article_data in data[supplier].items():
        article_match = article and article == article_num
        product_match = product and any(product.lower() in name.lower() for name in article_data['names'])
        
        if article_match or product_match:
            st.session_state.search_results = {
                "article": article_num,
                "supplier": supplier
            }
            found = True
            break
    
    if not found:
        st.error(f"❌ No results found for '{search_term}' in {supplier}")

def display_from_session_state(data):
    results = st.session_state.search_results
    article = results["article"]
    supplier = results["supplier"]
    
    if article not in data[supplier]:
        st.error("❌ Article not found in current data")
        return
        
    article_data = data[supplier][article]
    
    st.success(f"✅ **Article {article}** found in **{supplier}**")
    
    # Product names
    st.subheader("📝 Product Names")
    for name in article_data['names']:
        st.markdown(f'<div class="price-card">{name}</div>', unsafe_allow_html=True)
    
    # Statistics
    prices = article_data['prices']
    st.subheader("📊 Price Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(prices)}</div>
            <div class="stat-label">Total Records</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">${min(prices):.2f}</div>
            <div class="stat-label">Min Price/kg</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">${max(prices):.2f}</div>
            <div class="stat-label">Max Price/kg</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">${sum(prices)/len(prices):.2f}</div>
            <div class="stat-label">Avg Price/kg</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Price history with order numbers
    st.subheader("💵 Historical Prices with Order Details")
    cols = st.columns(2)
    for i, order in enumerate(article_data['orders']):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="price-box">
                <div style="font-size: 1.3em; font-weight: bold;">${order['price']:.2f}/kg</div>
                <div class="order-info">
                    <strong>Order:</strong> {order['order_no']}<br>
                    <strong>Date:</strong> {order['date']}
                </div>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
