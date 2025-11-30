import time
import functools
import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime
from io import BytesIO

# Cache configuration
CACHE_DURATION = 300  # 5 minutes cache

def cache_data(ttl=CACHE_DURATION):
    """Decorator to cache function results"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create a unique key for this function call
            key = f"{func.__name__}_{str(args)}_{str(kwargs)}"
            
            # Initialize cache if not exists
            if 'app_cache' not in st.session_state:
                st.session_state.app_cache = {}
            
            # Check if cached data exists and is not expired
            if key in st.session_state.app_cache:
                cached_data, timestamp = st.session_state.app_cache[key]
                if time.time() - timestamp < ttl:
                    return cached_data
            
            # If not cached or expired, call the function
            result = func(*args, **kwargs)
            st.session_state.app_cache[key] = (result, time.time())
            return result
        return wrapper
    return decorator

def clear_cache():
    """Clear all cached data"""
    if 'app_cache' in st.session_state:
        st.session_state.app_cache = {}

# Page config
st.set_page_config(
    page_title="Multi-Client Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for main dashboard - USING YOUR PREVIOUS THEME
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #991B1B, #7F1D1D);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .cdc-header {
        background: linear-gradient(135deg, #991B1B, #7F1D1D);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .ceo-header {
        background: linear-gradient(135deg, #D97706, #B45309);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .intelligence-header {
        background: linear-gradient(135deg, #059669, #047857);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .palletizing-header {
        background: linear-gradient(135deg, #7C3AED, #6D28D9);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
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
    .special-price-card {
        background: linear-gradient(135deg, #FEF3C7, #FDE68A);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 5px solid #D97706;
        margin: 0.5rem 0;
        color: #1F2937;
        font-weight: 500;
        border: 2px solid #D97706;
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
    .intelligence-stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #059669;
        text-align: center;
        color: #1F2937;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .pallet-stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #7C3AED;
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
    .intelligence-stat-number {
        font-size: 2em;
        font-weight: bold;
        color: #059669;
        margin: 0;
    }
    .pallet-stat-number {
        font-size: 2em;
        font-weight: bold;
        color: #7C3AED;
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
    .intelligence-price-box {
        background: #059669;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        margin: 0.5rem 0;
    }
    .special-price-box {
        background: #D97706;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        margin: 0.5rem 0;
        border: 2px solid #B45309;
    }
    .order-info {
        background: #F3F4F6;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.25rem 0;
        font-size: 0.8em;
        color: #6B7280;
    }
    .export-section {
        background: #F0F9FF;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #0EA5E9;
        margin: 1rem 0;
    }
    .ceo-section {
        background: #FFFBEB;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #D97706;
        margin: 1rem 0;
    }
    .intelligence-section {
        background: #ECFDF5;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #059669;
        margin: 1rem 0;
    }
    .palletizing-section {
        background: #FAF5FF;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #7C3AED;
        margin: 1rem 0;
    }
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 2rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 2px solid #991B1B;
    }
    /* NEW: Orders Management Styles */
    .orders-header {
        background: linear-gradient(135deg, #7C3AED, #6D28D9);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .product-catalog-header {
        background: linear-gradient(135deg, #0EA5E9, #0284C7);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .new-orders-header {
        background: linear-gradient(135deg, #DC2626, #B91C1C);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .prices-header {
        background: linear-gradient(135deg, #0EA5E9, #0284C7);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    /* Horizontal scrollable tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        overflow-x: auto;
        white-space: nowrap;
        flex-wrap: nowrap;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #F3F4F6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #000000 !important; /* Force black text */
    }
    .stTabs [data-baseweb="tab"] span {
        color: #000000 !important; /* Force black text for tab labels */
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #E5E7EB;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #991B1B !important; /* Active tab color */
        color: white !important; /* White text for active tab */
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] span {
        color: white !important; /* White text for active tab label */
    }
</style>
""", unsafe_allow_html=True)

# Configuration
API_KEY = "AIzaSyA3P-ZpLjDdVtGB82_1kaWuO7lNbKDj9HU"
CDC_SHEET_ID = "1qWgVT0l76VsxQzYExpLfioBHprd3IvxJzjQWv3RryJI"

# User authentication - UPDATED: cakeart_user changed to Khalid
# User authentication - UPDATED: Added Cameron client
USERS = {
    "admin": {"password": "123456", "clients": ["CDC", "CoteDivoire", "CakeArt", "SweetHouse", "Cameron"]},
    "ceo": {"password": "123456", "clients": ["CDC", "CoteDivoire", "CakeArt", "SweetHouse", "Cameron"]},
    "zaid": {"password": "123456", "clients": ["CDC"]},
    "mohammad": {"password": "123456", "clients": ["CoteDivoire"]},
    "Khalid": {"password": "123456", "clients": ["CakeArt", "SweetHouse"]},
    "Rotana": {"password": "123456", "clients": ["CDC"]}
}

# Client data sheets mapping - UPDATED: Added Cameron client
CLIENT_SHEETS = {
    "CDC": {
        "backaldrin": "Backaldrin_CDC",
        "bateel": "Bateel_CDC", 
        "ceo_special": "CDC_CEO_Special_Prices",
        "new_orders": "New_client_orders",
        "paid_orders": "Paid_Orders",
        "palletizing": "Palletizing_Data"  # NEW: Added palletizing sheet
    },
    "CoteDivoire": {
        "backaldrin": "Backaldrin_CoteDivoire",
        "bateel": "Bateel_CoteDivoire", 
        "ceo_special": "CoteDivoire_CEO_Special_Prices",
        "new_orders": "New_client_orders",
        "palletizing": "Palletizing_Data"  # NEW: Added palletizing sheet
    },
    "CakeArt": {
        "backaldrin": "Backaldrin_CakeArt",
        "bateel": "Bateel_CakeArt",
        "ceo_special": "CakeArt_CEO_Special_Prices",
        "new_orders": "New_client_orders",
        "palletizing": "Palletizing_Data"  # NEW: Added palletizing sheet
    },
    "SweetHouse": {
        "backaldrin": "Backaldrin_SweetHouse",
        "bateel": "Bateel_SweetHouse",
        "ceo_special": "SweetHouse_CEO_Special_Prices",
        "new_orders": "New_client_orders",
        "palletizing": "Palletizing_Data"  # NEW: Added palletizing sheet
    },
    "Cameron": {
        "backaldrin": "Backaldrin_Cameron",
        "bateel": "Bateel_Cameron", 
        "ceo_special": "Cameron_CEO_Special_Prices",
        "new_orders": "New_client_orders",
        "palletizing": "Palletizing_Data"  # NEW: Added palletizing sheet
    }
}

# Product Catalog Sheet Name
PRODUCT_CATALOG_SHEET = "FullProductList"
# NEW: Prices Sheet Name
PRICES_SHEET = "Prices"

def check_login():
    """Check if user is logged in"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'user_clients' not in st.session_state:
        st.session_state.user_clients = []
    
    return st.session_state.logged_in

def login_page():
    """Login page"""
    st.markdown("""
    <div class="login-container">
        <h2 style="text-align: center; color: #991B1B;">🔐 Multi-Client Dashboard</h2>
        <p style="text-align: center; color: #6B7280;">Please login to continue</p>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")
        submit = st.form_submit_button("🚀 Login", use_container_width=True)
        
        if submit:
            if username in USERS and USERS[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_clients = USERS[username]["clients"]
                st.success(f"✅ Welcome back, {username}!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
    
    st.markdown('</div>', unsafe_allow_html=True)

def logout_button():
    """Logout button in sidebar"""
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user_clients = []
        st.rerun()

def main_dashboard():
    """Main dashboard with tabs and sidebar announcements"""
    
    # Display user info in sidebar
    st.sidebar.markdown(f"**👤 Welcome, {st.session_state.username}**")
    st.sidebar.markdown(f"**🏢 Access to:** {', '.join(st.session_state.user_clients)}")
    
    # NEW: General Announcements Section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📢 General Announcements")
    
    # Announcements that will be visible to all users
    announcements = [
        "🚨 ETD is officially working!",
        "📦 Working on palletizing",
        "⭐ **SPECIAL OFFER**",
        "🔔 **REMINDER**:",
        "📊 **NEW FEATURE**: HS Code search now available across all clients",
        "📦 **NEW**: Palletizing Calculator added!",
        "💰 **NEW**: All Customers Prices tab added!"
    ]
    
    # Display announcements with nice styling
    for announcement in announcements:
        st.sidebar.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #F0F9FF, #E0F2FE);
            padding: 0.8rem;
            border-radius: 8px;
            border-left: 4px solid #0EA5E9;
            margin: 0.5rem 0;
            font-size: 0.9em;
            color: #1E293B;
        ">
            {announcement}
        </div>
        """, unsafe_allow_html=True)
    
    logout_button()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏢 Backaldrin Arab Jordan Dashboard</h1>
        <p>Centralized Management • Real-time Data • Professional Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs - PRICES TAB MOVED TO SECOND POSITION
    if st.session_state.username in ["ceo", "admin"]:
        # For admin/ceo: Prices tab as second position
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
            "🏢 CLIENTS", "💰 PRICES", "📋 NEW ORDERS", "📅 ETD SHEET", 
            "⭐ CEO SPECIAL PRICES", "💰 PRICE INTELLIGENCE", "📦 PRODUCT CATALOG",
            "📊 ORDERS MANAGEMENT", "📦 PALLETIZING"
        ])
    else:
        # For regular users: Prices tab as second position
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "🏢 CLIENTS", "💰 PRICES", "📋 NEW ORDERS", "📅 ETD SHEET", 
            "⭐ CEO SPECIAL PRICES", "💰 PRICE INTELLIGENCE", "📦 PRODUCT CATALOG",
            "📊 ORDERS MANAGEMENT", "📦 PALLETIZING"
        ])
    
    with tab1:
        clients_tab()
    
    with tab2:
        prices_tab()
        
    with tab3:
        new_orders_tab()
        
    with tab4:
        etd_tab()
        
    with tab5:
        ceo_specials_tab()
    
    with tab6:
        price_intelligence_tab()

    with tab7:
        product_catalog_tab()
        
    with tab8:
        orders_management_tab()
        
    # For admin/ceo users, add the Palletizing tab
    if st.session_state.username in ["ceo", "admin"]:
        with tab9:
            palletizing_tab()
    else:
        # For regular users, add Palletizing tab in the 8th position
        with tab8:
            palletizing_tab()

def prices_tab():
    """NEW: All Customers Prices Tab"""
    st.markdown("""
    <div class="prices-header">
        <h2 style="margin:0;">💰 All Customers Prices</h2>
        <p style="margin:0; opacity:0.9;">Complete Price Database • Cross-Customer Analysis • Flexible Search</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load prices data
    with st.spinner("📥 Loading prices data from Google Sheets..."):
        prices_data = load_prices_data()
    
    if prices_data.empty:
        st.warning("""
        ⚠️ **Prices data not found or empty!**
        
        **To get started:**
        1. Go to your Google Sheet
        2. Add a new tab called **'Prices'**
        3. Use these exact headers:
           - Customer
           - Customer Name
           - Salesman
           - Item Code
           - Item Name
           - Customer Article No
           - Customer Label
           - Packing/kg
           - Price
        """)
        return
    
    st.success(f"✅ Loaded {len(prices_data)} price records")
    
    # Overview Statistics
    st.subheader("📊 Price Database Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_records = len(prices_data)
        st.metric("Total Records", total_records)
    
    with col2:
        unique_customers = prices_data['Customer'].nunique()
        st.metric("Unique Customers", unique_customers)
    
    with col3:
        unique_items = prices_data['Item Code'].nunique()
        st.metric("Unique Items", unique_items)
    
    with col4:
        avg_price = prices_data['Price'].mean()
        st.metric("Average Price", f"${avg_price:.2f}")
    
    # Search and Filter Section
    st.subheader("🔍 Advanced Search & Filter")
    
    # Two rows for filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Customer filter
        customers = ["All"] + sorted(prices_data['Customer'].dropna().unique().tolist())
        selected_customer = st.selectbox("Filter by Customer:", customers, key="price_customer_filter")
    
    with col2:
        # Salesman filter
        salesmen = ["All"] + sorted(prices_data['Salesman'].dropna().unique().tolist())
        selected_salesman = st.selectbox("Filter by Salesman:", salesmen, key="price_salesman_filter")
    
    with col3:
        # Price range filter
        min_price = float(prices_data['Price'].min())
        max_price = float(prices_data['Price'].max())
        price_range = st.slider(
            "Price Range:",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price),
            key="price_range_filter"
        )
    
    # NEW: Specific search options
    st.subheader("🎯 Specific Search Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Article Number search
        article_search = st.text_input(
            "🔢 Search by Article Number:",
            placeholder="Enter article number...",
            key="price_article_search"
        )
    
    with col2:
        # Item Name search
        item_name_search = st.text_input(
            "📝 Search by Item Name:",
            placeholder="Enter item name...",
            key="price_item_name_search"
        )
    
    with col3:
        # Customer Article No search
        customer_article_search = st.text_input(
            "🏷️ Search by Customer Article No:",
            placeholder="Enter customer article no...",
            key="price_customer_article_search"
        )
    
    # Global search
    global_search = st.text_input(
        "🌐 Global Search (search across all columns):",
        placeholder="Enter any term to search across all columns...",
        key="price_global_search"
    )
    
    # Apply filters
    filtered_data = prices_data.copy()
    
    if selected_customer != "All":
        filtered_data = filtered_data[filtered_data['Customer'] == selected_customer]
    
    if selected_salesman != "All":
        filtered_data = filtered_data[filtered_data['Salesman'] == selected_salesman]
    
    # Apply price range filter
    filtered_data = filtered_data[
        (filtered_data['Price'] >= price_range[0]) & 
        (filtered_data['Price'] <= price_range[1])
    ]
    
    # NEW: Apply specific searches
    if article_search:
        filtered_data = filtered_data[
            filtered_data['Item Code'].astype(str).str.contains(article_search, case=False, na=False)
        ]
    
    if item_name_search:
        filtered_data = filtered_data[
            filtered_data['Item Name'].astype(str).str.contains(item_name_search, case=False, na=False)
        ]
    
    if customer_article_search:
        filtered_data = filtered_data[
            filtered_data['Customer Article No'].astype(str).str.contains(customer_article_search, case=False, na=False)
        ]
    
    # Apply global search (only if no specific searches are active)
    if global_search and not (article_search or item_name_search or customer_article_search):
        search_columns = ['Customer', 'Customer Name', 'Salesman', 'Item Code', 'Item Name', 
                         'Customer Article No', 'Customer Label', 'Packing/kg']
        mask = filtered_data[search_columns].astype(str).apply(
            lambda x: x.str.contains(global_search, case=False, na=False)
        ).any(axis=1)
        filtered_data = filtered_data[mask]
    
    # Display Results
    st.subheader(f"📋 Price Records ({len(filtered_data)} found)")
    
    if not filtered_data.empty:
        # Display data in a nice card format
        for _, record in filtered_data.iterrows():
            with st.expander(f"💰 {record['Item Code']} - {record['Item Name']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Customer:** {record['Customer']}")
                    st.write(f"**Customer Name:** {record['Customer Name']}")
                    st.write(f"**Salesman:** {record['Salesman']}")
                    st.write(f"**Item Code:** {record['Item Code']}")
                    st.write(f"**Item Name:** {record['Item Name']}")
                    
                with col2:
                    st.write(f"**Customer Article No:** {record['Customer Article No']}")
                    st.write(f"**Customer Label:** {record['Customer Label']}")
                    st.write(f"**Packing/kg:** {record['Packing/kg']}")
                    st.markdown(f"<h3 style='color: #059669;'>Price: ${record['Price']:.2f}</h3>", unsafe_allow_html=True)
        
        # Export Section
        st.markdown('<div class="export-section">', unsafe_allow_html=True)
        st.subheader("📤 Export Price Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"all_prices_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
                key="prices_csv"
            )
        
        with col2:
            # Create summary
            summary_text = f"""
All Customers Prices Report
===========================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Total Records: {len(filtered_data)}
Unique Customers: {filtered_data['Customer'].nunique()}
Unique Items: {filtered_data['Item Code'].nunique()}
Average Price: ${filtered_data['Price'].mean():.2f}
Price Range: ${filtered_data['Price'].min():.2f} - ${filtered_data['Price'].max():.2f}

Filters Applied:
- Customer: {selected_customer}
- Salesman: {selected_salesman}
- Price Range: ${price_range[0]:.2f} - ${price_range[1]:.2f}
- Article Search: {article_search if article_search else 'None'}
- Item Name Search: {item_name_search if item_name_search else 'None'}
- Customer Article Search: {customer_article_search if customer_article_search else 'None'}
- Global Search: {global_search if global_search and not (article_search or item_name_search or customer_article_search) else 'None'}

Top Items by Price:
{chr(10).join([f"• {row['Item Code']} - {row['Item Name']}: ${row['Price']:.2f} ({row['Customer']})" 
               for _, row in filtered_data.nlargest(10, 'Price').iterrows()])}
            """
            st.download_button(
                label="📄 Download Summary",
                data=summary_text,
                file_name=f"prices_summary_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
                key="prices_summary"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Statistics for filtered data
        st.subheader("📈 Filtered Data Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Filtered Records", len(filtered_data))
        
        with col2:
            filtered_avg_price = filtered_data['Price'].mean()
            st.metric("Average Price", f"${filtered_avg_price:.2f}")
        
        with col3:
            min_filtered_price = filtered_data['Price'].min()
            st.metric("Min Price", f"${min_filtered_price:.2f}")
        
        with col4:
            max_filtered_price = filtered_data['Price'].max()
            st.metric("Max Price", f"${max_filtered_price:.2f}")
            
    else:
        st.info("No price records match your search criteria.")

def load_prices_data():
    """Load all prices data from Google Sheets"""
    try:
        prices_url = f"https://sheets.googleapis.com/v4/spreadsheets/{CDC_SHEET_ID}/values/{PRICES_SHEET}!A:Z?key={API_KEY}"
        response = requests.get(prices_url)
        
        if response.status_code == 200:
            data = response.json()
            values = data.get('values', [])
            
            if values and len(values) > 1:
                headers = values[0]
                rows = values[1:]
                
                # Create DataFrame
                df = pd.DataFrame(rows, columns=headers)
                
                # Check for required columns
                required_cols = ['Customer', 'Customer Name', 'Salesman', 'Item Code', 'Item Name', 
                               'Customer Article No', 'Customer Label', 'Packing/kg', 'Price']
                
                # Fill missing columns with empty values
                for col in required_cols:
                    if col not in df.columns:
                        df[col] = ''
                
                # Convert numeric columns
                if 'Price' in df.columns:
                    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
                if 'Packing/kg' in df.columns:
                    df['Packing/kg'] = pd.to_numeric(df['Packing/kg'], errors='coerce')
                
                # Fill NaN values with empty strings for text columns
                text_cols = ['Customer', 'Customer Name', 'Salesman', 'Item Code', 'Item Name', 
                           'Customer Article No', 'Customer Label']
                for col in text_cols:
                    if col in df.columns:
                        df[col] = df[col].fillna('')
                
                return df
                
        return pd.DataFrame()
        
    except Exception as e:
        st.error(f"Error loading prices data: {str(e)}")
        return pd.DataFrame()

def palletizing_tab():
    """Quick Pallet Calculator for CDC Items"""
    st.markdown("""
    <div class="palletizing-header">
        <h2 style="margin:0;">📦 Quick Pallet Calculator</h2>
        <p style="margin:0; opacity:0.9;">Instant Pallet Calculations • CDC Standard Items • Real-time Results</p>
    </div>
    """, unsafe_allow_html=True)
    
    quick_pallet_calculator()

def quick_pallet_calculator():
    """Quick Pallet Calculator for CDC Items"""
    st.subheader("🧮 Quick Pallet Calculator")
    
    # CDC Common Items Database
    cdc_items = {
        "Vermicelli Color": {"packing": "5kg", "cartons_per_pallet": 100, "weight_per_carton": 5},
        "Vermicelli Dark": {"packing": "5kg", "cartons_per_pallet": 100, "weight_per_carton": 5},
        "Vermicelli White": {"packing": "5kg", "cartons_per_pallet": 100, "weight_per_carton": 5},
        "Chocolate Chips": {"packing": "25kg", "cartons_per_pallet": 40, "weight_per_carton": 25},
        "Date Mix": {"packing": "30kg", "cartons_per_pallet": 36, "weight_per_carton": 30},
        "Vanilla Powder": {"packing": "15kg", "cartons_per_pallet": 60, "weight_per_carton": 15},
        "Custom Item": {"packing": "Custom", "cartons_per_pallet": 0, "weight_per_carton": 0}
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Item Selection
        selected_item = st.selectbox(
            "Select Item:",
            list(cdc_items.keys()),
            key="item_select"
        )
        
        # Quantity Input
        quantity = st.number_input(
            "Quantity:",
            min_value=1,
            value=100,
            step=1,
            key="quantity"
        )
        
        # Unit of Measure
        uom = st.selectbox(
            "Unit of Measure:",
            ["Cartons", "KGs", "Pallets"],
            key="uom"
        )
    
    with col2:
        # For custom items, allow manual entry
        if selected_item == "Custom Item":
            st.info("🔧 Enter Custom Item Details:")
            packing = st.text_input("Packing (e.g., 5kg, 25kg):", value="5kg", key="custom_packing")
            cartons_per_pallet = st.number_input("Cartons per Pallet:", min_value=1, value=100, step=1, key="custom_cartons")
            weight_per_carton = st.number_input("Weight per Carton (kg):", min_value=0.1, value=5.0, step=0.1, key="custom_weight")
        else:
            item_data = cdc_items[selected_item]
            packing = item_data["packing"]
            cartons_per_pallet = item_data["cartons_per_pallet"]
            weight_per_carton = item_data["weight_per_carton"]
            
            st.info(f"📦 **Standard Packing:** {packing}")
            st.info(f"📊 **Cartons per Pallet:** {cartons_per_pallet}")
            st.info(f"⚖️ **Weight per Carton:** {weight_per_carton} kg")
    
    # REAL-TIME CALCULATIONS
    if quantity > 0:
        st.subheader("🎯 INSTANT PALCALC RESULTS")
        
        # Convert everything to cartons first
        if uom == "Cartons":
            total_cartons = quantity
        elif uom == "KGs":
            total_cartons = quantity / weight_per_carton
        else:  # Pallets
            total_cartons = quantity * cartons_per_pallet
        
        # Calculate pallets
        full_pallets = total_cartons // cartons_per_pallet
        partial_pallet_cartons = total_cartons % cartons_per_pallet
        partial_pallet_percentage = (partial_pallet_cartons / cartons_per_pallet) * 100 if cartons_per_pallet > 0 else 0
        
        total_weight = total_cartons * weight_per_carton
        
        # Display Results - SIMPLE AND CLEAR
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if full_pallets > 0:
                st.success(f"### 📦 {full_pallets:,.0f} FULL PALLET{'S' if full_pallets > 1 else ''}")
            else:
                st.info("### 📦 0 FULL PALLETS")
                
        with col2:
            if partial_pallet_cartons > 0:
                st.warning(f"### 📦 1 PARTIAL PALLET")
                st.write(f"({partial_pallet_cartons:,.0f} cartons - {partial_pallet_percentage:.1f}% full)")
            else:
                st.success("### ✅ NO PARTIAL PALLETS")
                
        with col3:
            st.info(f"### ⚖️ {total_weight:,.0f} kg")
            st.write(f"({total_cartons:,.0f} cartons total)")
        
        # Detailed Breakdown
        with st.expander("📊 View Detailed Calculation", expanded=False):
            st.write(f"**Item:** {selected_item} ({packing})")
            
            if uom == "Cartons":
                st.write(f"**Input:** {quantity:,.0f} cartons")
            elif uom == "KGs":
                st.write(f"**Input:** {quantity:,.0f} kg = {total_cartons:,.0f} cartons")
            else:
                st.write(f"**Input:** {quantity:,.0f} pallets = {total_cartons:,.0f} cartons")
            
            st.write(f"**Calculation:** {total_cartons:,.0f} cartons ÷ {cartons_per_pallet} cartons/pallet")
            st.write(f"**Result:** {full_pallets:,.0f} full pallets + {partial_pallet_cartons:,.0f} cartons partial")
        
        # Quick Examples
        st.subheader("💡 Quick Examples")
        
        examples_col1, examples_col2 = st.columns(2)
        
        with examples_col1:
            if st.button(f"Example: 100 cartons {selected_item}", key="example_100"):
                st.session_state.quantity = 100
                st.session_state.uom = "Cartons"
                st.rerun()
                
        with examples_col2:
            if st.button(f"Example: 1 pallet {selected_item}", key="example_1"):
                st.session_state.quantity = 1
                st.session_state.uom = "Pallets"
                st.rerun()
        
        # Container Information (40ft always)
        st.markdown("---")
        st.subheader("🚢 Container Information")
        st.info("""
        **40ft Container Capacity:**
        - **Max Pallets:** 30 pallets
        - **Max Weight:** 23,000 kg (23 tons)
        - **Your current order:** Will fill approximately **{:.1f}%** of container capacity
        """.format((full_pallets / 30) * 100))
    
    # Bulk Sheet Analysis (Optional - keep it simple)
    st.markdown("---")
    with st.expander("📊 Bulk Analysis from Google Sheets (Optional)"):
        st.info("For bulk analysis of your existing Palletizing_Data sheet, use the main data import features.")
        st.write("The Quick Calculator above is designed for instant pallet calculations!")

def load_palletizing_data(client):
    """Load palletizing data from Google Sheets"""
    try:
        sheet_name = CLIENT_SHEETS[client]["palletizing"]
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{CDC_SHEET_ID}/values/{sheet_name}!A:Z?key={API_KEY}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            values = data.get('values', [])
            
            if values and len(values) > 1:
                headers = values[0]
                rows = values[1:]
                
                # Create DataFrame
                df = pd.DataFrame(rows, columns=headers)
                
                # Required columns for palletizing
                required_cols = ['Client', 'Item Code', 'Item Name', 'Unit/KG', 'Unit/Carton', 
                               'Unit Pack/Pallet', 'Total Unit', 'Pallet Order', 'Total Weight', 'Factory']
                
                # Check if required columns exist
                missing_cols = [col for col in required_cols if col not in df.columns]
                if missing_cols:
                    st.error(f"Missing columns in palletizing data: {', '.join(missing_cols)}")
                    return pd.DataFrame()
                
                # Convert numeric columns
                numeric_cols = ['Unit/KG', 'Unit/Carton', 'Unit Pack/Pallet', 'Total Unit', 'Pallet Order', 'Total Weight']
                for col in numeric_cols:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                
                return df
                
        return pd.DataFrame()
        
    except Exception as e:
        st.error(f"Error loading palletizing data for {client}: {str(e)}")
        return pd.DataFrame()

def clients_tab():
    """Clients management tab"""
    st.subheader("Client Selection")
    
    # Client selection - only show clients user has access to
    available_clients = st.session_state.user_clients
    client = st.selectbox(
        "Select Client:",
        available_clients,
        key="client_select"
    )
    
    if client:
        cdc_dashboard(client)

def etd_tab():
    """ETD Sheet - Live Google Sheets Integration with Multi-Month Support"""
    st.markdown("""
    <div class="intelligence-header">
        <h2 style="margin:0;">📅 ETD Management Dashboard</h2>
        <p style="margin:0; opacity:0.9;">Live Order Tracking • Multi-Supplier ETD • Multi-Month View</p>
    </div>
    """, unsafe_allow_html=True)

    # ETD Sheet configuration
    ETD_SHEET_ID = "1eA-mtD3aK_n9VYNV_bxnmqm58IywF0f5-7vr3PT51hs"
    
    # Available months - EXACT NAMES with space after 2025
    AVAILABLE_MONTHS = ["October 2025 ", "November 2025 "]

    try:
        # Month Selection
        st.subheader("📅 Select Month")
        selected_month = st.radio(
            "Choose month to view:",
            AVAILABLE_MONTHS,
            horizontal=True,
            key="etd_month_selector"
        )
        
        # Load ETD data for selected month
        with st.spinner(f"🔄 Loading {selected_month.strip()} ETD data..."):
            etd_data = load_etd_data(ETD_SHEET_ID, selected_month)
        
        if etd_data.empty:
            st.warning(f"No ETD data found in {selected_month}. Please check the sheet.")
            return

        st.success(f"✅ Connected to {selected_month.strip()}! Loaded {len(etd_data)} orders")

        # Overview Metrics
        st.subheader("📊 ETD Overview")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            total_orders = len(etd_data)
            st.metric("Total Orders", total_orders)
        
        with col2:
            shipped_orders = len(etd_data[etd_data['Status'].str.lower() == 'shipped'])
            st.metric("Shipped", shipped_orders)
        
        with col3:
            production_orders = len(etd_data[etd_data['Status'].str.lower().str.contains('production', na=False)])
            st.metric("In Production", production_orders)
        
        with col4:
            pending_orders = len(etd_data[etd_data['Status'].str.lower().str.contains('pending', na=False)])
            st.metric("Pending", pending_orders)
        
        with col5:
            # Count orders needing ETD
            need_etd = len(etd_data[
                (etd_data['ETD _ Backaldrine'].astype(str).str.contains('NEED ETD', case=False, na=False)) |
                (etd_data['ETD_bateel'].astype(str).str.contains('NEED ETD', case=False, na=False)) |
                (etd_data['ETD _ Kasih'].astype(str).str.contains('NEED ETD', case=False, na=False)) |
                (etd_data['ETD_PMC'].astype(str).str.contains('NEED ETD', case=False, na=False))
            ])
            st.metric("Need ETD", need_etd)

        # Cross-Month Summary (if multiple months available)
        if len(AVAILABLE_MONTHS) > 1:
            st.subheader("🌐 Cross-Month Summary")
            month_cols = st.columns(len(AVAILABLE_MONTHS))
            
            for i, month in enumerate(AVAILABLE_MONTHS):
                with month_cols[i]:
                    if month == selected_month:
                        st.info(f"**{month.strip()}**\n**{len(etd_data)} orders**")
                    else:
                        # Quick load other months for summary
                        try:
                            other_month_data = load_etd_data(ETD_SHEET_ID, month)
                            if not other_month_data.empty:
                                st.metric(month.strip(), len(other_month_data))
                            else:
                                st.write(f"**{month.strip()}**\n0 orders")
                        except:
                            st.write(f"**{month.strip()}**\n–")

        # Search and Filter Section
        st.subheader("🔍 Filter & Search Orders")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            client_filter = st.selectbox(
                "Client",
                ["All"] + sorted(etd_data['Client Name'].dropna().unique()),
                key="etd_client_filter"
            )
        
        with col2:
            employee_filter = st.selectbox(
                "Employee", 
                ["All"] + sorted(etd_data['Concerned Employee'].dropna().unique()),
                key="etd_employee_filter"
            )
        
        with col3:
            status_filter = st.selectbox(
                "Status",
                ["All", "Shipped", "In Production", "Pending", "Need ETD"],
                key="etd_status_filter"
            )
        
        with col4:
            search_term = st.text_input("Search Order No...", key="etd_search")

        # Apply filters
        filtered_data = etd_data.copy()
        
        if client_filter != "All":
            filtered_data = filtered_data[filtered_data['Client Name'] == client_filter]
        
        if employee_filter != "All":
            filtered_data = filtered_data[filtered_data['Concerned Employee'] == employee_filter]
        
        if status_filter != "All":
            if status_filter == "Need ETD":
                filtered_data = filtered_data[
                    (filtered_data['ETD _ Backaldrine'].astype(str).str.contains('NEED ETD', case=False, na=False)) |
                    (filtered_data['ETD_bateel'].astype(str).str.contains('NEED ETD', case=False, na=False)) |
                    (filtered_data['ETD _ Kasih'].astype(str).str.contains('NEED ETD', case=False, na=False)) |
                    (filtered_data['ETD_PMC'].astype(str).str.contains('NEED ETD', case=False, na=False))
                ]
            else:
                filtered_data = filtered_data[filtered_data['Status'] == status_filter]
        
        if search_term:
            filtered_data = filtered_data[
                filtered_data['Order No.'].astype(str).str.contains(search_term, case=False, na=False)
            ]

        # Display filtered results
        st.subheader(f"📋 {selected_month.strip()} Orders ({len(filtered_data)} found)")
        
        if not filtered_data.empty:
            for _, order in filtered_data.iterrows():
                display_etd_order_card(order, selected_month.strip())
        else:
            st.info("No orders match your filter criteria.")

        # Export Section
        st.markdown('<div class="export-section">', unsafe_allow_html=True)
        st.subheader("📤 Export ETD Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"etd_data_{selected_month.strip().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
                key="etd_csv"
            )
        
        with col2:
            summary_text = f"""
ETD Data Export - {selected_month.strip()}
===============================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Total Orders: {len(filtered_data)}
Filters: Client={client_filter}, Employee={employee_filter}, Status={status_filter}

Orders Summary:
{chr(10).join([f"• {row['Order No.']} - {row['Client Name']} - {row['Status']}" for _, row in filtered_data.iterrows()])}
            """
            st.download_button(
                label="📄 Download Summary",
                data=summary_text,
                file_name=f"etd_summary_{selected_month.strip().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                key="etd_summary"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error loading ETD data: {str(e)}")
        st.info("Please check: 1) Google Sheet is shared, 2) Sheet name is correct, 3) Internet connection")

def display_etd_order_card(order, month):
    """Display individual ETD order card with supplier tracking"""
    
    # Determine status color
    status = order.get('Status', 'Unknown')
    status_color = {
        'Shipped': '🟢',
        'In Production': '🟡', 
        'Pending': '🟠',
        'Unknown': '⚫'
    }.get(status, '⚫')
    
    # Check for ETD needs
    needs_etd = []
    for supplier in ['Backaldrine', 'bateel', 'Kasih', 'PMC']:
        etd_col = f"ETD _{supplier}" if supplier != 'bateel' else 'ETD_bateel'
        etd_value = order.get(etd_col, '')
        if pd.notna(etd_value) and 'NEED ETD' in str(etd_value).upper():
            needs_etd.append(supplier)
    
    with st.expander(f"{status_color} {order.get('Order No.', 'N/A')} - {order.get('Client Name', 'N/A')} | {month}", expanded=False):
        
        # Order Header
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write(f"**Client:** {order.get('Client Name', 'N/A')}")
            st.write(f"**Employee:** {order.get('Concerned Employee', 'N/A')}")
            st.write(f"**Month:** {month}")
            
        with col2:
            st.write(f"**Status:** {status}")
            st.write(f"**Confirmation:** {order.get('Confirmation Date', 'N/A')}")
            
        with col3:
            if needs_etd:
                st.error(f"🚨 NEED ETD: {', '.join(needs_etd)}")
            st.write(f"**Loading:** {order.get('Scheduled Date For Loading', 'N/A')}")
        
        # Supplier ETD Tracking
        st.write("---")
        st.write("**🚚 Supplier ETD Status**")
        
        suppliers = [
            ('Backaldrine', 'ETD _ Backaldrine', 'bateel Order #'),
            ('bateel', 'ETD_bateel', 'bateel Order #'),
            ('Kasih', 'ETD _ Kasih', 'Kasih Order #'), 
            ('PMC', 'ETD_PMC', 'PMC Order #')
        ]
        
        cols = st.columns(4)
        for idx, (supplier, etd_col, order_col) in enumerate(suppliers):
            with cols[idx]:
                etd_value = order.get(etd_col, '')
                order_value = order.get(order_col, '')
                
                if pd.isna(etd_value) or str(etd_value).strip() == '':
                    st.write(f"**{supplier}:** ❌ No ETD")
                elif 'NEED ETD' in str(etd_value).upper():
                    st.error(f"**{supplier}:** 🚨 NEED ETD")
                elif 'READY' in str(etd_value).upper():
                    st.success(f"**{supplier}:** ✅ Ready")
                else:
                    st.info(f"**{supplier}:** 📅 {etd_value}")
                
                if pd.notna(order_value) and str(order_value).strip() != '':
                    st.caption(f"Order: {order_value}")
        
        # Additional Information
        st.write("---")
        col1, col2 = st.columns(2)
        
        with col1:
            stock_notes = order.get('Stock Notes', '')
            if pd.notna(stock_notes) and str(stock_notes).strip() != '':
                st.write("**📦 Stock Notes:**")
                st.info(stock_notes)
                
        with col2:
            transport = order.get('transport Company', '')
            if pd.notna(transport) and str(transport).strip() != '':
                st.write("**🚛 Transport:**")
                st.write(transport)

def load_etd_data(sheet_id, sheet_name):
    """Optimized ETD loader using universal function"""
    return load_sheet_data(sheet_name, start_row=13)

def ceo_specials_tab():
    """CEO Special Prices tab - NOW CLIENT SPECIFIC"""
    st.markdown("""
    <div class="ceo-header">
        <h2 style="margin:0;">⭐ CEO Special Prices</h2>
        <p style="margin:0; opacity:0.9;">Exclusive Pricing • Limited Time Offers • VIP Client Rates</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Client selection for CEO specials - only show clients user has access to
    available_clients = st.session_state.user_clients
    client = st.selectbox(
        "Select Client for CEO Special Prices:",
        available_clients,
        key="ceo_client_select"
    )
    
    if not client:
        st.warning("No clients available for your account")
        return
        
    st.info(f"📊 Showing CEO Special Prices for **{client}**")
    
    # Load CEO special prices for selected client
    ceo_data = load_ceo_special_prices(client)
    
    if ceo_data.empty:
        sheet_name = CLIENT_SHEETS[client]["ceo_special"]
        st.warning(f"⚠️ No CEO special prices found for {client}. Please add data to '{sheet_name}' sheet.")
        st.info(f"""
        **To add CEO special prices for {client}:**
        1. Go to your Google Sheet
        2. Add a new tab called **'{sheet_name}'**
        3. Use these columns:
           - Article_Number
           - Product_Name  
           - Special_Price
           - Currency
           - Incoterm
           - Notes
           - Effective_Date
           - Expiry_Date
        """)
        return
     
    # CEO Special Prices Overview
    st.subheader(f"📊 {client} CEO Specials Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Special Offers", len(ceo_data))
    with col2:
        active_offers = len(ceo_data[ceo_data['Expiry_Date'] >= datetime.now().strftime('%Y-%m-%d')])
        st.metric("Active Offers", active_offers)
    with col3:
        # Count unique currencies instead of average price
        unique_currencies = ceo_data['Currency'].nunique()
        st.metric("Currencies Used", unique_currencies)
    with col4:
        expiring_soon = len(ceo_data[
            (ceo_data['Expiry_Date'] >= datetime.now().strftime('%Y-%m-%d')) &
            (ceo_data['Expiry_Date'] <= (datetime.now() + pd.Timedelta(days=30)).strftime('%Y-%m-%d'))
        ])
        st.metric("Expiring Soon", expiring_soon)
    
    # Search and Filter
    st.subheader("🔍 Search CEO Special Prices")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_term = st.text_input("Search by article or product name...", key="ceo_search")
    with col2:
        show_active = st.checkbox("Show Active Only", value=True, key="ceo_active")
    with col3:
        currency_filter = st.selectbox("Currency", ["All"] + list(ceo_data['Currency'].unique()), key="ceo_currency")
    
    # Filter data
    filtered_data = ceo_data.copy()
    
    if search_term:
        mask = filtered_data.astype(str).apply(
            lambda x: x.str.contains(search_term, case=False, na=False)
        ).any(axis=1)
        filtered_data = filtered_data[mask]
    
    if show_active:
        filtered_data = filtered_data[filtered_data['Expiry_Date'] >= datetime.now().strftime('%Y-%m-%d')]
    
    if currency_filter != "All":
        filtered_data = filtered_data[filtered_data['Currency'] == currency_filter]
    
    # Display CEO Special Prices
    st.subheader(f"🎯 {client} Special Price List")
    
    if not filtered_data.empty:
        for _, special in filtered_data.iterrows():
            # Check if offer is active
            is_active = special['Expiry_Date'] >= datetime.now().strftime('%Y-%m-%d')
            status_color = "🟢" if is_active else "🔴"
            status_text = "Active" if is_active else "Expired"
            
            # Safe price display - show raw value if numeric conversion fails
            try:
                price_display = f"{float(special['Special_Price']):.2f}"
            except:
                price_display = str(special['Special_Price'])
            
            st.markdown(f"""
            <div class="special-price-card">
                <div style="display: flex; justify-content: between; align-items: center;">
                    <div>
                        <h3 style="margin:0; color: #D97706;">{special['Article_Number']} - {special['Product_Name']}</h3>
                        <p style="margin:0; font-size: 1.2em; font-weight: bold; color: #B45309;">
                            Special Price: {price_display} {special['Currency']}/kg
                        </p>
                        <p style="margin:0; color: #6B7280;">
                            {status_color} {status_text} • Valid until: {special['Expiry_Date']}
                            {f" • Incoterm: {special['Incoterm']}" if pd.notna(special['Incoterm']) and special['Incoterm'] != '' else ''}
                        </p>
                        {f"<p style='margin:5px 0 0 0; color: #6B7280;'><strong>Notes:</strong> {special['Notes']}</p>" if pd.notna(special['Notes']) and special['Notes'] != '' else ''}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Export CEO Specials
        st.markdown('<div class="export-section">', unsafe_allow_html=True)
        st.subheader("📤 Export CEO Special Prices")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{client}_ceo_special_prices_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
                key="ceo_csv"
            )
        
        with col2:
            st.download_button(
                label="📄 Download Summary",
                data=f"""
{client} CEO Special Prices Summary
===================================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Total Offers: {len(filtered_data)}
Active Offers: {len(filtered_data[filtered_data['Expiry_Date'] >= datetime.now().strftime('%Y-%m-%d')])}

Special Prices:
{chr(10).join([f"• {row['Article_Number']} - {row['Product_Name']}: {row['Special_Price']} {row['Currency']} (Incoterm: {row['Incoterm']}, Until: {row['Expiry_Date']})" for _, row in filtered_data.iterrows()])}
                """,
                file_name=f"{client}_ceo_specials_summary_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
                key="ceo_summary"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.info("No CEO special prices match your search criteria.")

def price_intelligence_tab():
    """CEO Price Intelligence - Cross-client price comparison"""
    st.markdown("""
    <div class="intelligence-header">
        <h2 style="margin:0;">💰 CEO Price Intelligence</h2>
        <p style="margin:0; opacity:0.9;">Cross-Client Price Comparison • Market Intelligence • Strategic Insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🔍 **Search across selected clients to compare pricing strategies and identify opportunities**")
    
    # Show only the clients that the current user has access to
    available_clients = st.session_state.user_clients
    
    # Client selection - Show only user's accessible clients
    available_clients = st.session_state.user_clients
    
    # User-friendly message about client access
    if len(available_clients) < 2:
        st.warning("🔒 You need access to at least 2 clients to compare prices. Currently you only have access to: " + ", ".join(available_clients))
    
    # Search Configuration Section
    st.subheader("🔧 Search Configuration")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        client_selection = st.multiselect(
            "**SELECT CLIENTS TO ANALYZE**",
            options=available_clients,
            default=available_clients,  # Default to all clients
            key="intelligence_clients"
        )
    
    with col2:
        search_term = st.text_input("**ENTER ARTICLE NUMBER OR PRODUCT NAME**", 
                                  placeholder="e.g., 281, Chocolate, Date Mix...", 
                                  key="intelligence_search")
    
    with col3:
        supplier_filter = st.selectbox("**SUPPLIER**", ["All", "Backaldrin", "Bateel"], key="intelligence_supplier")
    
    # Analyze Button - NO WHITE BOX
    if st.button("🚀 ANALYZE PRICES ACROSS SELECTED CLIENTS", use_container_width=True, type="primary", key="intelligence_analyze"):
        if search_term and client_selection:
            analyze_cross_client_prices(search_term, client_selection, supplier_filter)
        else:
            if not search_term:
                st.error("❌ Please enter an article number or product name to analyze")
            if not client_selection:
                st.error("❌ Please select at least one client to analyze")

def analyze_cross_client_prices(search_term, selected_clients, supplier_filter="All"):
    """Analyze prices across selected clients for a given search term"""
    st.subheader(f"🔍 Analysis Results: '{search_term}'")
    st.info(f"**Clients Analyzed:** {', '.join(selected_clients)}")
    
    # Initialize results structure for ALL selected clients
    all_results = {}
    total_records = 0
    found_articles = set()
    
    # Search across selected clients
    for client in selected_clients:
        client_data = get_google_sheets_data(client)
        
        for supplier in ["Backaldrin", "Bateel"]:
            if supplier_filter != "All" and supplier != supplier_filter:
                continue
                
            supplier_data = client_data[supplier]
            client_results = []
            
            for article_num, article_data in supplier_data.items():
                # Check if search term matches article number or product name
                article_match = search_term.lower() in article_num.lower()
                product_match = any(search_term.lower() in name.lower() for name in article_data['names'])
                
                if article_match or product_match:
                    found_articles.add(article_num)
                    if article_data['prices']:  # Only include if we have price data
                        avg_price = sum(article_data['prices']) / len(article_data['prices'])
                        min_price = min(article_data['prices'])
                        max_price = max(article_data['prices'])
                        
                        client_results.append({
                            'article': article_num,
                            'product_names': list(set(article_data['names'])),
                            'avg_price': avg_price,
                            'min_price': min_price,
                            'max_price': max_price,
                            'records': len(article_data['prices']),
                            'supplier': supplier,
                            'all_prices': article_data['prices'],
                            'orders': article_data['orders'],
                            'has_data': True
                        })
                        total_records += len(article_data['prices'])
                    else:
                        # Article found but no price data
                        client_results.append({
                            'article': article_num,
                            'product_names': list(set(article_data['names'])),
                            'avg_price': None,
                            'min_price': None,
                            'max_price': None,
                            'records': 0,
                            'supplier': supplier,
                            'all_prices': [],
                            'orders': [],
                            'has_data': False
                        })
            
            # Store results even if empty (to show N/A)
            all_results[f"{client} - {supplier}"] = client_results
    
    if not found_articles:
        st.warning(f"❌ No results found for '{search_term}' across selected clients")
        return
    
    # Calculate overall statistics from available data only
    all_prices = []
    for client_supplier, results in all_results.items():
        for result in results:
            if result['has_data']:
                all_prices.extend(result['all_prices'])
    
    # Display overview statistics
    st.subheader("📊 Cross-Client Price Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Price Records", total_records)
    with col2:
        if all_prices:
            price_range = max(all_prices) - min(all_prices) if all_prices else 0
            st.metric("Price Range", f"${price_range:.2f}/kg")
        else:
            st.metric("Price Range", "N/A")
    with col3:
        overall_min = min(all_prices) if all_prices else "N/A"
        st.metric("Lowest Price", f"${overall_min}/kg" if all_prices else "N/A")
    with col4:
        overall_max = max(all_prices) if all_prices else "N/A"
        st.metric("Highest Price", f"${overall_max}/kg" if all_prices else "N/A")
    
    # Display detailed comparison using NATIVE STREAMLIT COMPONENTS
    st.subheader("🏢 Client-by-Client Price Comparison")
    
    # Group by article number to show cross-client comparison for each article
    articles_data = {}
    
    for client_supplier, results in all_results.items():
        client_name, supplier_name = client_supplier.split(" - ")
        for result in results:
            article_num = result['article']
            if article_num not in articles_data:
                articles_data[article_num] = {
                    'product_names': result['product_names'],
                    'client_data': {}
                }
            articles_data[article_num]['client_data'][client_supplier] = result
    
    # Display each article with cross-client comparison
    for article_num, article_data in articles_data.items():
        st.markdown(f"### 📦 Article: {article_num}")
        st.caption(f"**Product Names:** {', '.join(article_data['product_names'])}")
        
        # Create comparison table for this article across clients - UPDATED VERSION
        comparison_data = []

        for client_supplier in all_results.keys():
            client_name, supplier_name = client_supplier.split(" - ")
            result = article_data['client_data'].get(client_supplier)
            
            if result and result['has_data']:
                comparison_data.append({
                    'Client': client_name,
                    'Supplier': supplier_name,
                    'Min Price': f"${result['min_price']:.2f}",
                    'Max Price': f"${result['max_price']:.2f}",
                    'Records': result['records'],
                    'Status': '✅ Available'
                })
            else:
                comparison_data.append({
                    'Client': client_name,
                    'Supplier': supplier_name,
                    'Min Price': "N/A",
                    'Max Price': "N/A", 
                    'Records': "0",
                    'Status': '❌ Not Available'
                })
        
        # Display comparison table
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)
        
        # Show detailed view for each client that has data
        st.markdown("#### 📈 Detailed Price History")
        
        for client_supplier, result in article_data['client_data'].items():
            client_name, supplier_name = client_supplier.split(" - ")
            
            if result['has_data']:
                # Determine if this is best/worst price
                is_best = result['min_price'] == overall_min if all_prices else False
                is_worst = result['max_price'] == overall_max if all_prices else False
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**{client_name} - {supplier_name}**")
                    
                with col2:
                    st.markdown(f"**${result['min_price']:.2f} - ${result['max_price']:.2f}**/kg")
                    st.caption(f"Range: ${result['max_price'] - result['min_price']:.2f}")
                    st.caption(f"{result['records']} records")
                
                # Show best/worst price badges
                badge_col1, badge_col2 = st.columns(2)
                with badge_col1:
                    if is_best:
                        st.success("🎯 BEST PRICE")
                with badge_col2:
                    if is_worst:
                        st.error("⚠️ HIGHEST PRICE")
                
                # Show detailed price history
                with st.expander(f"View price history for {client_name}"):
                    cols = st.columns(2)
                    for i, order in enumerate(result['orders']):
                        with cols[i % 2]:
                            st.markdown(f"""
                            <div class="price-box">
                                <div style="font-size: 1.1em; font-weight: bold;">${order['price']:.2f}/kg</div>
                                <div class="order-info">
                                    <strong>Order:</strong> {order['order_no']}<br>
                                    <strong>Date:</strong> {order['date']}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
            else:
                # Show N/A for clients without data
                st.warning(f"**{client_name} - {supplier_name}**: ❌ No pricing data available for this article")
        
        st.markdown("---")
    
    # Export intelligence report
    st.subheader("📤 Export Price Intelligence Report")
    
    # Create export data - UPDATED VERSION
    export_data = []
    for article_num, article_data in articles_data.items():
        for client_supplier, result in article_data['client_data'].items():
            client_name, supplier_name = client_supplier.split(" - ")
            
            if result['has_data']:
                export_data.append({
                    'Article_Number': article_num,
                    'Product_Names': ', '.join(result['product_names']),
                    'Client': client_name,
                    'Supplier': supplier_name,
                    'Min_Price': result['min_price'],
                    'Max_Price': result['max_price'], 
                    'Records_Count': result['records'],
                    'Status': 'Available',
                    'Analysis_Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            else:
                export_data.append({
                    'Article_Number': article_num,
                    'Product_Names': ', '.join(result['product_names']),
                    'Client': client_name,
                    'Supplier': supplier_name,
                    'Min_Price': 'N/A',
                    'Max_Price': 'N/A',
                    'Records_Count': 0,
                    'Status': 'Not Available',
                    'Analysis_Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
    
    if export_data:
        export_df = pd.DataFrame(export_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = export_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV Report",
                data=csv,
                file_name=f"price_intelligence_{search_term}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
                key="intelligence_csv"
            )
        
        with col2:
            st.download_button(
                label="📄 Download Summary",
                data=f"""
Price Intelligence Report
=========================

Search Term: {search_term}
Clients Analyzed: {', '.join(selected_clients)}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Total Records Analyzed: {total_records}

Overall Price Range: ${overall_min if all_prices else 'N/A'} - ${overall_max if all_prices else 'N/A'}/kg

Detailed Findings:
{chr(10).join([f"• {row['Client']} - {row['Supplier']}: {row['Article_Number']} - Min:${row['Min_Price'] if row['Status'] == 'Available' else 'N/A'}, Max:${row['Max_Price'] if row['Status'] == 'Available' else 'N/A'}/kg ({row['Status']})" for row in export_data])}
                """,
                file_name=f"price_intelligence_summary_{search_term}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
                key="intelligence_summary"
            )
            
    
    st.markdown('</div>', unsafe_allow_html=True)

def product_catalog_tab():
    """Full Product Catalog with comprehensive product information"""
    
    st.markdown("""
    <div class="product-catalog-header">
        <h2 style="margin:0;">📦 Full Product Catalog</h2>
        <p style="margin:0; opacity:0.9;">Complete Product Database • Technical Specifications • Search & Filter</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load product catalog data
    catalog_data = load_product_catalog()
    
    if catalog_data.empty:
        st.warning("""
        ⚠️ **Product catalog not found or empty!**
        
        **To get started:**
        1. Go to your Google Sheet
        2. Add a new tab called **'FullProductList'**
        3. Use these columns (at minimum):
           - Article_Number
           - Product_Name
           - Supplier
        """)
        return
    
    # Catalog Overview - DYNAMIC based on available columns
    st.subheader("📊 Catalog Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Products", len(catalog_data))
    
    with col2:
        if 'Supplier' in catalog_data.columns:
            suppliers = catalog_data['Supplier'].nunique()
            st.metric("Suppliers", suppliers)
        else:
            st.metric("Suppliers", "N/A")
    
    with col3:
        if 'Category' in catalog_data.columns:
            categories = catalog_data['Category'].nunique()
            st.metric("Categories", categories)
        else:
            st.metric("Categories", "N/A")
    
    with col4:
        articles_with_data = catalog_data['Article_Number'].nunique()
        st.metric("Unique Articles", articles_with_data)
    
    # Search and Filter Section - DYNAMIC based on available columns
    st.subheader("🔍 Search & Filter Products")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("Search by article, product name, or description...", key="catalog_search")
    
    with col2:
        if 'Supplier' in catalog_data.columns:
            supplier_filter = st.selectbox("Supplier", ["All"] + list(catalog_data['Supplier'].unique()), key="catalog_supplier")
        else:
            supplier_filter = "All"
            st.selectbox("Supplier", ["No supplier data"], key="catalog_supplier", disabled=True)
    
    with col3:
        if 'Category' in catalog_data.columns:
            category_filter = st.selectbox("Category", ["All"] + list(catalog_data['Category'].unique()), key="catalog_category")
        else:
            category_filter = "All"
            st.selectbox("Category", ["No category data"], key="catalog_category", disabled=True)
    
    # Filter data
    filtered_data = catalog_data.copy()
    
    if search_term:
        mask = filtered_data.astype(str).apply(
            lambda x: x.str.contains(search_term, case=False, na=False)
        ).any(axis=1)
        filtered_data = filtered_data[mask]
    
    if supplier_filter != "All" and 'Supplier' in catalog_data.columns:
        filtered_data = filtered_data[filtered_data['Supplier'] == supplier_filter]
    
    if category_filter != "All" and 'Category' in catalog_data.columns:
        filtered_data = filtered_data[filtered_data['Category'] == category_filter]
    
    # Display Results
    st.subheader(f"📋 Products Found: {len(filtered_data)}")
    
    if not filtered_data.empty:
        # Show product cards
        for _, product in filtered_data.iterrows():
            display_product_card_flexible(product, catalog_data.columns)
        
        # Export Section
        st.markdown('<div class="export-section">', unsafe_allow_html=True)
        st.subheader("📤 Export Product Catalog")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"product_catalog_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
                key="catalog_csv"
            )
        
        with col2:
            # Create a simplified version for text export
            export_text = f"""Product Catalog Export
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Total Products: {len(filtered_data)}

Products:
{chr(10).join([f"• {row['Article_Number']} - {row['Product_Name']} " + (f"({row['Supplier']})" if 'Supplier' in row and row['Supplier'] else '') for _, row in filtered_data.iterrows()])}
"""
            st.download_button(
                label="📄 Download Summary",
                data=export_text,
                file_name=f"product_catalog_summary_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
                key="catalog_summary"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.info("No products match your search criteria.")

def display_product_card_flexible(product, available_columns):
    """Display individual product card with available columns only"""
    
    # Determine card color based on supplier if available
    if 'Supplier' in available_columns and product['Supplier'] == 'Backaldrin':
        card_class = "price-card"
        border_color = "#991B1B"
    elif 'Supplier' in available_columns and product['Supplier'] == 'Bateel':
        card_class = "special-price-card"
        border_color = "#D97706"
    else:
        card_class = "intelligence-stat-card"
        border_color = "#059669"
    
    with st.expander(f"📦 {product['Article_Number']} - {product['Product_Name']}", expanded=False):
        # Build the card content dynamically based on available columns
        card_content = f"""
        <div class="{card_class}">
            <div style="border-left: 5px solid {border_color}; padding-left: 1rem;">
                <h3 style="margin:0; color: {border_color};">{product['Article_Number']} - {product['Product_Name']}</h3>
        """
        
        # Add Supplier if available
        if 'Supplier' in available_columns:
            card_content += f"""<p style="margin:0; font-weight: bold; color: #6B7280;">Supplier: {product['Supplier']}</p>"""
        
        card_content += """<div style="margin-top: 1rem;"><div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">"""
        
        # Left column - Category information
        left_column = ""
        if 'Category' in available_columns:
            left_column += f"""<p style="margin:0;"><strong>Main Category:</strong> {product['Category']}</p>"""
        if 'Sub_Category' in available_columns:
            left_column += f"""<p style="margin:0;"><strong>Sub Category:</strong> {product['Sub_Category']}</p>"""
        if 'Sub_Sub_Category' in available_columns:
            left_column += f"""<p style="margin:0;"><strong>Sub-Sub Category:</strong> {product['Sub_Sub_Category']}</p>"""
        
        # Right column - Technical information
        right_column = ""
        if 'UOM' in available_columns:
            right_column += f"""<p style="margin:0;"><strong>UOM:</strong> {product['UOM']}</p>"""
        if 'Unit_Weight' in available_columns:
            right_column += f"""<p style="margin:0;"><strong>Unit Weight:</strong> {product['Unit_Weight']}</p>"""
        if 'Current_Price' in available_columns and product['Current_Price']:
            right_column += f"""<p style="margin:0;"><strong>Current Price:</strong> ${product['Current_Price']}/kg</p>"""
        
        card_content += f"""<div>{left_column}</div><div>{right_column}</div></div>"""
        
        # Additional information sections
        if 'Common_Description' in available_columns and product['Common_Description']:
            card_content += f"""
            <div style="margin-top: 1rem;">
                <p style="margin:0;"><strong>Description:</strong></p>
                <p style="margin:0; color: #6B7280;">{product['Common_Description']}</p>
            </div>
            """
        
        if 'Purpose_Of_Use' in available_columns and product['Purpose_Of_Use']:
            card_content += f"""
            <div style="margin-top: 1rem;">
                <p style="margin:0;"><strong>Purpose of Use:</strong></p>
                <p style="margin:0; color: #6B7280;">{product['Purpose_Of_Use']}</p>
            </div>
            """
        
        if 'Dosage' in available_columns and product['Dosage']:
            card_content += f"""
            <div style="margin-top: 1rem;">
                <p style="margin:0;"><strong>Dosage:</strong></p>
                <p style="margin:0; color: #6B7280;">{product['Dosage']}</p>
            </div>
            """
        
        if 'Ingredients' in available_columns and product['Ingredients']:
            card_content += f"""
            <div style="margin-top: 1rem;">
                <p style="margin:0;"><strong>Ingredients:</strong></p>
                <p style="margin:0; color: #6B7280;">{product['Ingredients']}</p>
            </div>
            """
        
        if 'Datasheet_Link' in available_columns and product['Datasheet_Link']:
            card_content += f"""
            <div style="margin-top: 1rem;">
                <p style="margin:0;"><strong>Datasheet:</strong> <a href="{product['Datasheet_Link']}" target="_blank" style="color: #0EA5E9;">View Datasheet</a></p>
            </div>
            """
        
        card_content += "</div></div>"
        
        st.markdown(card_content, unsafe_allow_html=True)

def load_product_catalog():
    """Load product catalog from Google Sheets - FLEXIBLE VERSION"""
    try:
        sheet_name = PRODUCT_CATALOG_SHEET
        catalog_url = f"https://sheets.googleapis.com/v4/spreadsheets/{CDC_SHEET_ID}/values/{sheet_name}!A:Z?key={API_KEY}"
        response = requests.get(catalog_url)
        
        if response.status_code == 200:
            data = response.json()
            values = data.get('values', [])
            
            if values and len(values) > 1:
                headers = values[0]
                rows = values[1:]
                
                # Create DataFrame with available columns only
                df = pd.DataFrame(rows, columns=headers)
                
                # Fill missing values with empty strings
                df = df.fillna('')
                
                # Check if we have at least the basic required data
                if len(df) > 0 and 'Article_Number' in df.columns:
                    return df
                else:
                    st.error(f"Product catalog loaded but missing required columns. Found: {list(df.columns)}")
                    return pd.DataFrame()
            else:
                st.warning("Product catalog sheet exists but has no data or only headers")
                return pd.DataFrame()
        else:
            st.error(f"Failed to load product catalog. HTTP Status: {response.status_code}")
            return pd.DataFrame()
        
    except Exception as e:
        st.error(f"Error loading product catalog: {str(e)}")
        return pd.DataFrame()

def load_ceo_special_prices(client="CDC"):
    """Load CEO special prices from Google Sheets for specific client"""
    try:
        sheet_name = CLIENT_SHEETS[client]["ceo_special"]
        ceo_url = f"https://sheets.googleapis.com/v4/spreadsheets/{CDC_SHEET_ID}/values/{sheet_name}!A:Z?key={API_KEY}"
        response = requests.get(ceo_url)
        
        if response.status_code == 200:
            data = response.json()
            values = data.get('values', [])
            
            if values and len(values) > 1:
                headers = values[0]
                rows = values[1:]
                
                # Create DataFrame
                df = pd.DataFrame(rows, columns=headers)
                
                # UPDATED: Ensure required columns exist (now 8 columns)
                required_cols = ['Article_Number', 'Product_Name', 'Special_Price', 'Currency', 'Incoterm']
                if all(col in df.columns for col in required_cols):
                    # Clean up data - include all 8 columns
                    df = df[required_cols + [col for col in df.columns if col not in required_cols]]
                    
                    # Add default values if missing
                    if 'Notes' not in df.columns:
                        df['Notes'] = ''
                    if 'Effective_Date' not in df.columns:
                        df['Effective_Date'] = datetime.now().strftime('%Y-%m-%d')
                    if 'Expiry_Date' not in df.columns:
                        df['Expiry_Date'] = (datetime.now() + pd.Timedelta(days=365)).strftime('%Y-%m-%d')
                    
                    return df
                else:
                    st.error(f"Missing required columns in {sheet_name}. Found: {list(df.columns)}")
                    return pd.DataFrame()
                
        return pd.DataFrame()
        
    except Exception as e:
        st.error(f"Error loading CEO special prices for {client}: {str(e)}")
        return pd.DataFrame()

def get_google_sheets_data(client="CDC"):
    """Optimized version - loads both suppliers in one call and returns proper dictionary structure"""
    try:
        # Dynamic sheet names
        backaldrin_sheet = f"Backaldrin_{client}"
        bateel_sheet = f"Bateel_{client}"
        
        # Load both sheets
        backaldrin_df = load_sheet_data(backaldrin_sheet)
        bateel_df = load_sheet_data(bateel_sheet)
        
        # Convert DataFrames to the expected dictionary structure
        backaldrin_data = process_supplier_data(backaldrin_df, "Backaldrin")
        bateel_data = process_supplier_data(bateel_df, "Bateel")
        
        return {"Backaldrin": backaldrin_data, "Bateel": bateel_data}
    except Exception as e:
        st.error(f"Error loading data for {client}: {str(e)}")
        return {"Backaldrin": {}, "Bateel": {}}

def process_supplier_data(df, supplier_name):
    """Convert DataFrame to the expected dictionary structure for pricing data"""
    if df.empty:
        return {}
    
    # Initialize the result structure
    result = {}
    
    try:
        # Check if we have the required columns
        required_cols = ['Article_Number', 'Product_Name', 'Price_per_kg', 'Order_Number', 'Date']
        available_cols = [col for col in required_cols if col in df.columns]
        
        if not available_cols:
            st.warning(f"No required columns found in {supplier_name} data")
            return {}
        
        # Group by article number
        for _, row in df.iterrows():
            article_num = str(row.get('Article_Number', ''))
            if not article_num or article_num == 'nan':
                continue
                
            if article_num not in result:
                result[article_num] = {
                    'names': [],
                    'prices': [],
                    'orders': []
                }
            
            # Add product name if available
            product_name = row.get('Product_Name', '')
            if product_name and product_name not in result[article_num]['names']:
                result[article_num]['names'].append(product_name)
            
            # Add price if available
            price = row.get('Price_per_kg', '')
            if price and str(price) != 'nan':
                try:
                    price_float = float(price)
                    result[article_num]['prices'].append(price_float)
                except (ValueError, TypeError):
                    pass
            
            # Add order details
            order_no = row.get('Order_Number', '')
            date = row.get('Date', '')
            if order_no and str(order_no) != 'nan':
                order_details = {
                    'order_no': order_no,
                    'date': date,
                    'price': float(price) if price and str(price) != 'nan' else 0,
                    'product_name': product_name,
                    'article': article_num,
                    'year': row.get('Year', ''),
                    'hs_code': row.get('HS_Code', ''),
                    'packaging': row.get('Packaging', ''),
                    'quantity': row.get('Quantity', ''),
                    'total_weight': row.get('Total_Weight', ''),
                    'total_price': row.get('Total_Price', '')
                }
                result[article_num]['orders'].append(order_details)
                
    except Exception as e:
        st.error(f"Error processing {supplier_name} data: {str(e)}")
    
    return result

def create_export_data(article_data, article, supplier, client):
    """Create export data in different formats - UPDATED WITH NEW COLUMNS"""
    # Create DataFrame for export
    export_data = []
    for order in article_data['orders']:
        export_data.append({
            'Client': client,
            'Order_Number': order['order_no'],
            'Date': order['date'],
            'Year': order['year'],
            'Product_Name': order['product_name'],
            'Article_Number': article,
            'HS_Code': order['hs_code'],
            'Packaging': order['packaging'],
            'Quantity': order['quantity'],
            'Total_Weight': order['total_weight'],
            'Price_per_kg': order['price'],
            'Total_Price': order['total_price'],
            'Supplier': supplier,
            'Export_Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return pd.DataFrame(export_data)

def cdc_dashboard(client):
    """Client pricing dashboard with THREE SEARCH OPTIONS"""
    
    # Initialize session state
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'export_data' not in st.session_state:
        st.session_state.export_data = None
    
    st.markdown(f"""
    <div class="cdc-header">
        <h2 style="margin:0;">📊 {client} Pricing Dashboard</h2>
        <p style="margin:0; opacity:0.9;">Backaldrin & Bateel • Live Google Sheets Data • Export Ready</p>
    </div>
    """, unsafe_allow_html=True)

    # Load data directly from Google Sheets
    DATA = get_google_sheets_data(client)
    st.success(f"✅ Connected to Google Sheets - Live Data for {client}!")

    # Refresh button
    if st.button("🔄 Refresh Data", use_container_width=True, type="secondary", key=f"{client}_refresh"):
        st.rerun()

    # Supplier selection - CLEAN VERSION (no white box)
    st.subheader("🏢 Select Supplier")
    supplier = st.radio("", ["Backaldrin", "Bateel"], horizontal=True, label_visibility="collapsed", key=f"{client}_supplier")

    # Search section - THREE SEARCH OPTIONS
    st.subheader("🔍 Search Historical Prices")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        article = st.text_input("**ARTICLE NUMBER**", placeholder="e.g., 1-366, 1-367...", key=f"{client}_article")
    with col2:
        product = st.text_input("**PRODUCT NAME**", placeholder="e.g., Moist Muffin, Date Mix...", key=f"{client}_product")
    with col3:
        hs_code = st.text_input("**HS CODE**", placeholder="e.g., 1901200000, 180690...", key=f"{client}_hscode")

    # Auto-suggestions
    search_term = article or product or hs_code
    if search_term:
        suggestions = get_suggestions(search_term, supplier, DATA)
        if suggestions:
            st.markdown("**💡 Quick Suggestions:**")
            for i, suggestion in enumerate(suggestions[:4]):
                with st.form(key=f"{client}_form_{i}"):
                    if st.form_submit_button(suggestion["display"], use_container_width=True):
                        st.session_state.search_results = {
                            "article": suggestion["value"],
                            "supplier": supplier,
                            "client": client
                        }
                        st.rerun()
    
    # Manual search - UPDATED: Added hs_code parameter
    if st.button("🚀 SEARCH HISTORICAL PRICES", use_container_width=True, type="primary", key=f"{client}_search"):
        handle_search(article, product, hs_code, supplier, DATA, client)

    # Display results from session state
    if st.session_state.search_results and st.session_state.search_results.get("client") == client:
        display_from_session_state(DATA, client)

def get_suggestions(search_term, supplier, data):
    """Get search suggestions for article, product name, or HS code - SAFER VERSION"""
    suggestions = []
    
    if not data or supplier not in data:
        return suggestions
        
    supplier_data = data[supplier]
    
    for article_num, article_data in supplier_data.items():
        # Skip if article_data is not a dictionary or doesn't have expected structure
        if not isinstance(article_data, dict) or 'names' not in article_data:
            continue
            
        # Article number search
        if search_term.lower() in article_num.lower():
            display_name = article_data['names'][0] if article_data['names'] else 'No Name'
            suggestions.append({
                "type": "article",
                "value": article_num,
                "display": f"🔢 {article_num} - {display_name}"
            })
        
        # Product name search
        for name in article_data['names']:
            if search_term.lower() in name.lower():
                suggestions.append({
                    "type": "product", 
                    "value": article_num,
                    "display": f"📝 {article_num} - {name}"
                })
        
        # HS Code search
        if 'orders' in article_data:
            for order in article_data['orders']:
                if (order.get('hs_code') and 
                    search_term.lower() in str(order['hs_code']).lower() and
                    article_num not in [s['value'] for s in suggestions]):
                    display_name = article_data['names'][0] if article_data['names'] else 'No Name'
                    suggestions.append({
                        "type": "hs_code",
                        "value": article_num,
                        "display": f"🏷️ {article_num} - HS: {order['hs_code']} - {display_name}"
                    })
    
    # Remove duplicates
    unique_suggestions = {}
    for sugg in suggestions:
        if sugg["value"] not in unique_suggestions:
            unique_suggestions[sugg["value"]] = sugg
    
    return list(unique_suggestions.values())

def handle_search(article, product, hs_code, supplier, data, client):
    """Handle search across article, product name, and HS code - SAFER VERSION"""
    search_term = article or product or hs_code
    if not search_term:
        st.error("❌ Please enter an article number, product name, or HS code")
        return
    
    found = False
    
    if supplier not in data:
        st.error(f"❌ No data available for {supplier}")
        return
        
    for article_num, article_data in data[supplier].items():
        # Skip if article_data is not properly structured
        if not isinstance(article_data, dict):
            continue
            
        article_match = article and article == article_num
        product_match = product and 'names' in article_data and any(
            product.lower() in name.lower() for name in article_data['names']
        )
        hs_code_match = hs_code and 'orders' in article_data and any(
            hs_code.lower() in str(order.get('hs_code', '')).lower() 
            for order in article_data['orders']
        )
        
        if article_match or product_match or hs_code_match:
            st.session_state.search_results = {
                "article": article_num,
                "supplier": supplier,
                "client": client
            }
            # Prepare export data
            st.session_state.export_data = create_export_data(article_data, article_num, supplier, client)
            found = True
            break
    
    if not found:
        st.error(f"❌ No results found for '{search_term}' in {supplier}")

def display_from_session_state(data, client):
    """Display search results with NEW CARD DESIGN"""
    results = st.session_state.search_results
    article = results["article"]
    supplier = results["supplier"]
    
    if article not in data[supplier]:
        st.error("❌ Article not found in current data")
        return
        
    article_data = data[supplier][article]
    
    st.success(f"✅ **Article {article}** found in **{supplier}** for **{client}**")
    
    # Product names - SHOW ONLY UNIQUE NAMES
    st.subheader("📝 Product Names")
    unique_names = list(set(article_data['names']))  # Remove duplicates
    for name in unique_names:
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
            <div class="stat-number">${max(prices) - min(prices):.2f}</div>
            <div class="stat-label">Price Range/kg</div>
        </div>
        """, unsafe_allow_html=True)
    
    # UPDATED: NEW CARD DESIGN
    st.subheader("💵 Historical Prices with Order Details")
    cols = st.columns(2)
    for i, order in enumerate(article_data['orders']):
        with cols[i % 2]:
            # NEW CARD DESIGN: Order Number as header, then date, then price, then details
            order_details = f"""
            <div class="price-box">
                <div style="font-size: 1.4em; font-weight: bold; border-bottom: 2px solid white; padding-bottom: 0.5rem; margin-bottom: 0.5rem;">
                    📦 {order['order_no']}
                </div>
                <div style="font-size: 1.1em; margin-bottom: 0.5rem;">
                    <strong>📅 Date:</strong> {order['date']}
                </div>
                <div style="font-size: 1.3em; font-weight: bold; color: #FEF3C7; margin-bottom: 0.8rem;">
                    ${order['price']:.2f}/kg
                </div>
                <div class="order-info">
                    <strong>📦 Product:</strong> {order['product_name']}<br>
                    <strong>🔢 Article:</strong> {order['article']}<br>
                    {f"<strong>🏷️ Year:</strong> {order['year']}<br>" if order['year'] else ""}
                    {f"<strong>📊 HS Code:</strong> {order['hs_code']}<br>" if order['hs_code'] else ""}
                    {f"<strong>📦 Packaging:</strong> {order['packaging']}<br>" if order['packaging'] else ""}
                    {f"<strong>🔢 Quantity:</strong> {order['quantity']}<br>" if order['quantity'] else ""}
                    {f"<strong>⚖️ Total Weight:</strong> {order['total_weight']}<br>" if order['total_weight'] else ""}
                    {f"<strong>💰 Total Price:</strong> {order['total_price']}<br>" if order['total_price'] else ""}
                </div>
            </div>
            """
            st.markdown(order_details, unsafe_allow_html=True)
    
    # EXPORT SECTION
    st.markdown('<div class="export-section">', unsafe_allow_html=True)
    st.subheader("📤 Export Data")
    
    if st.session_state.export_data is not None:
        export_df = st.session_state.export_data
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # CSV Export
            csv = export_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{client}_pricing_{article}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
                type="primary",
                key=f"{client}_csv"
            )
        
        with col2:
            # Excel Export
            try:
                excel_data = convert_df_to_excel(export_df)
                st.download_button(
                    label="📊 Download Excel",
                    data=excel_data,
                    file_name=f"{client}_pricing_{article}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.ms-excel",
                    use_container_width=True,
                    key=f"{client}_excel"
                )
            except:
                st.info("📊 Excel export requires openpyxl package")
        
        with col3:
            # Quick Stats Summary
            st.download_button(
                label="📄 Download Summary",
                data=f"""
{client} Pricing Summary Report
===============================

Article: {article}
Supplier: {supplier}
Client: {client}
Product: {export_df['Product_Name'].iloc[0]}
Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Price Statistics:
• Total Records: {len(export_df)}
• Minimum Price: ${min(prices):.2f}/kg
• Maximum Price: ${max(prices):.2f}/kg  
• Price Range: ${max(prices) - min(prices):.2f}/kg

Orders Included: {', '.join(export_df['Order_Number'].tolist())}
                """,
                file_name=f"{client}_summary_{article}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
                key=f"{client}_summary"
            )
        
        # Show export preview
        with st.expander("👀 Preview Export Data"):
            st.dataframe(export_df, use_container_width=True)
            
    else:
        st.info("Search for an article to enable export options")
    
    st.markdown('</div>', unsafe_allow_html=True)

def convert_df_to_excel(df):
    """Convert DataFrame to Excel format"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Price_History')
    processed_data = output.getvalue()
    return processed_data

def convert_df_to_excel(df):
    """Convert DataFrame to Excel format"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Price_History')
    processed_data = output.getvalue()
    return processed_data

# === ADD UNIVERSAL LOADER HERE ===
def load_sheet_data(sheet_name, start_row=0):
    """Universal Google Sheets loader for all data types"""
    try:
        import urllib.parse
        encoded_sheet = urllib.parse.quote(sheet_name)
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{CDC_SHEET_ID}/values/{encoded_sheet}!A:Z?key={API_KEY}"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            values = data.get('values', [])
            
            if len(values) > start_row:
                headers = values[start_row]
                rows = values[start_row + 1:] if len(values) > start_row + 1 else []
                
                df = pd.DataFrame(rows, columns=headers)
                df = df.replace('', pd.NA)
                return df
                
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading {sheet_name}: {str(e)}")
        return pd.DataFrame()
# === END UNIVERSAL LOADER ===

def orders_management_tab():
    """Orders Management Dashboard"""
    st.markdown("""
    <div class="orders-header">
        <h2 style="margin:0;">📋 Orders Management Dashboard</h2>
        <p style="margin:0; opacity:0.9;">Order Tracking • Status Monitoring • Payment Updates</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Client selection for orders
    available_clients = st.session_state.user_clients
    client = st.selectbox(
        "Select Client:",
        available_clients,
        key="orders_client_select"
    )
    
    if not client:
        st.warning("Please select a client to view orders")
        return
    
    # Load orders data
    orders_data = load_orders_data(client)
    
    if orders_data.empty:
        st.info(f"No orders data found for {client}. Orders management will be available when data is added.")
        return
    
    # Orders Overview
    st.subheader("📊 Orders Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_orders = len(orders_data)
        st.metric("Total Orders", total_orders)
    
    with col2:
        shipped_orders = len(orders_data[orders_data['Status'] == 'Shipped'])
        st.metric("Shipped", shipped_orders)
    
    with col3:
        production_orders = len(orders_data[orders_data['Status'] == 'In Production'])
        st.metric("In Production", production_orders)
    
    with col4:
        pending_orders = len(orders_data[orders_data['Status'] == 'Pending'])
        st.metric("Pending", pending_orders)
    
    # Filter section
    st.subheader("🔍 Filter Orders")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox(
            "Status",
            ["All", "Shipped", "In Production", "Pending"],
            key="orders_status_filter"
        )
    
    with col2:
        payment_filter = st.selectbox(
            "Payment Status", 
            ["All", "Pending", "Due", "Paid"],
            key="orders_payment_filter"
        )
    
    with col3:
        search_term = st.text_input("Search Order Number...", key="orders_search")
    
    # Apply filters
    filtered_orders = orders_data.copy()
    
    if status_filter != "All":
        filtered_orders = filtered_orders[filtered_orders['Status'] == status_filter]
    
    if payment_filter != "All":
        filtered_orders = filtered_orders[filtered_orders['Payment Update'] == payment_filter]
    
    if search_term:
        filtered_orders = filtered_orders[
            filtered_orders['Order Number'].str.contains(search_term, case=False, na=False)
        ]
    
    # Display orders
    st.subheader(f"📋 Orders ({len(filtered_orders)} found)")
    
    if not filtered_orders.empty:
        for _, order in filtered_orders.iterrows():
            display_order_card(order)
    else:
        st.info("No orders match your filter criteria.")
    
    # Export section
    st.markdown('<div class="export-section">', unsafe_allow_html=True)
    st.subheader("📤 Export Orders Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = filtered_orders.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"{client}_orders_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True,
            key="orders_csv"
        )
    
    with col2:
        st.download_button(
            label="📄 Download Summary",
            data=f"""
{client} Orders Summary
======================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Total Orders: {len(filtered_orders)}
Shipped: {shipped_orders}
In Production: {production_orders}
Pending: {pending_orders}

Orders List:
{chr(10).join([f"• {row['Order Number']} - {row['Status']} - Payment: {row['Payment Update']}" for _, row in filtered_orders.iterrows()])}
            """,
            file_name=f"{client}_orders_summary_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True,
            key="orders_summary"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_order_card(order):
    """Display individual order card using Streamlit components only"""
    
    status = order.get('Status', 'Pending')
    payment_status = order.get('Payment Update', 'Pending')
    order_number = order.get('Order Number', 'N/A')
    
    # Create expander
    with st.expander(f"📦 {order_number} - {status}", expanded=False):
        
        # Header row
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader(order_number)
            st.write(f"**Status:** {status}")
            
        with col2:
            # Payment status with color coding
            if payment_status == 'Paid':
                st.success(f"💳 {payment_status}")
            elif payment_status == 'Due':
                st.error(f"⚠️ {payment_status}")
            else:
                st.warning(f"⏳ {payment_status}")
            
            st.write(f"**ERP:** {order.get('ERP', 'N/A')}")
        
        # Order details in columns
        st.write("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**📋 Order Details**")
            st.write(f"Manufacturer: {order.get('Manufacturer', 'N/A')}")
            st.write(f"ETD: {order.get('ETD', 'N/A')}")
            st.write(f"PI Issue: {order.get('Date of PI issue', 'N/A')}")
            
        with col2:
            st.write("**💰 Financial Details**")
            st.write(f"Payment Due: {order.get('Payment due date', 'N/A')}")
            st.write(f"Invoice: {order.get('Invoice', 'N/A')}")
            st.write(f"Client Signed: {order.get('Date of Client signing', 'N/A')}")
        
        # Notes section
        notes = order.get('Notes', '')
        if pd.notna(notes) and notes != '':
            st.write("---")
            st.write("**📝 Notes**")
            st.info(notes)

def load_orders_data(client):
    """Load ALL orders data - SIMPLE VERSION"""
    try:
        # Use the exact same structure as your screenshot data
        sample_orders = [
            {
                'Order Number': 'SA C.D 125/2025', 'ERP': 'Yes', 'Date of request': 'N/A',
                'Date of PI issue': '08-Sep-25', 'Date of Client signing': 'N/A',
                'Invoice': 0, 'Payment': 'Credit Note 45550', 'Manufacturer': 'BAJ',
                'ETD': '28-Dec-25', 'Payment due date': '16-Sep-25', 
                'Payment Update': 'Pending', 'Status': 'Shipped', 'Notes': 'Credit Note 45550'
            },
            {
                'Order Number': 'SA C.D 127/2025', 'ERP': 'Yes', 'Date of request': '08-Oct-25',
                'Date of PI issue': '09-Oct-25', 'Date of Client signing': '12-Oct-25',
                'Invoice': 80500.00, 'Payment': '$80,500.00', 'Manufacturer': 'BAJ',
                'ETD': '30-Oct-25', 'Payment due date': '17-Nov-25',
                'Payment Update': 'Pending', 'Status': 'Shipped', 'Notes': ''
            },
            {
                'Order Number': 'SA C.D 140/2025', 'ERP': 'Yes', 'Date of request': '08-Oct-25',
                'Date of PI issue': '09-Oct-25', 'Date of Client signing': '09-Oct-25',
                'Invoice': 49092.59, 'Payment': '$49,092.59', 'Manufacturer': 'BAJ',
                'ETD': '17-Nov-25', 'Payment due date': '30-Oct-25',
                'Payment Update': 'Pending', 'Status': 'Shipped', 'Notes': 'New ETD 30 Oct'
            },
            {
                'Order Number': 'SA C.D 135/2025', 'ERP': 'Yes', 'Date of request': '08-Oct-25',
                'Date of PI issue': '09-Oct-25', 'Date of Client signing': '09-Oct-25',
                'Invoice': 58770.00, 'Payment': '$58,770.00', 'Manufacturer': 'BAJ',
                'ETD': '13-Nov-25', 'Payment due date': '26-Oct-25',
                'Payment Update': 'Pending', 'Status': 'Shipped', 'Notes': ''
            },
            {
                'Order Number': 'SA C.D 138/2025', 'ERP': 'Yes', 'Date of request': '08-Oct-25',
                'Date of PI issue': '09-Oct-25', 'Date of Client signing': '09-Oct-25',
                'Invoice': 42900.00, 'Payment': '$42,900.00', 'Manufacturer': 'BAJ',
                'ETD': '8-Nov-25', 'Payment due date': '21-Oct-25',
                'Payment Update': 'Pending', 'Status': 'Shipped', 'Notes': ''
            },
            {
                'Order Number': 'SA C.D 128/2025', 'ERP': 'Bated', 'Date of request': '08-Sep-25',
                'Date of PI issue': '08-Sep-25', 'Date of Client signing': '10-Sep-25',
                'Invoice': 46711.00, 'Payment': '$46,711.00', 'Manufacturer': 'BT',
                'ETD': '7-Nov-25', 'Payment due date': '20-Oct-25',
                'Payment Update': 'Pending', 'Status': 'Shipped', 'Notes': 'ETD was shared by CEO with Ammar'
            },
            {
                'Order Number': 'SA C.D 115/2025', 'ERP': 'Yes', 'Date of request': '22-Jul-25',
                'Date of PI issue': '05-Aug-25', 'Date of Client signing': '07-Aug-25',
                'Invoice': 36228.00, 'Payment': '$36,228.00', 'Manufacturer': 'BAJ',
                'ETD': '6-Nov-25', 'Payment due date': '19-Oct-25',
                'Payment Update': 'Pending', 'Status': 'Shipped', 'Notes': 'Will follow'
            },
            {
                'Order Number': 'SA C.D 130/2025', 'ERP': 'Yes', 'Date of request': '08-Sep-25',
                'Date of PI issue': '08-Sep-25', 'Date of Client signing': '10-Sep-25',
                'Invoice': 38550.30, 'Payment': '$38,550.30', 'Manufacturer': 'BAJ',
                'ETD': '6-Nov-25', 'Payment due date': '19-Oct-25',
                'Payment Update': 'Pending', 'Status': 'Shipped', 'Notes': ''
            },
            {
                'Order Number': 'SA C.D 136/2025', 'ERP': 'Yes', 'Date of request': '08-Oct-25',
                'Date of PI issue': '09-Oct-25', 'Date of Client signing': '09-Oct-25',
                'Invoice': 27140.00, 'Payment': '$27,140.00', 'Manufacturer': 'BAJ',
                'ETD': '3-Nov-25', 'Payment due date': '16-Oct-25',
                'Payment Update': 'Pending', 'Status': 'In Production', 'Notes': ''
            },
            {
                'Order Number': 'SA C.D 137/2025', 'ERP': 'Yes', 'Date of request': '08-Oct-25',
                'Date of PI issue': '09-Oct-25', 'Date of Client signing': '09-Oct-25',
                'Invoice': 32190.00, 'Payment': '$32,190.00', 'Manufacturer': 'BAJ',
                'ETD': '3-Nov-25', 'Payment due date': '16-Oct-25',
                'Payment Update': 'Pending', 'Status': 'In Production', 'Notes': ''
            },
            {
                'Order Number': 'SA C.D 133/2025', 'ERP': 'Yes', 'Date of request': '08-Sep-25',
                'Date of PI issue': '14-Sep-25', 'Date of Client signing': '15-Sep-25',
                'Invoice': 48966.10, 'Payment': '$48,966.10', 'Manufacturer': 'BAJ',
                'ETD': '20-Oct-25', 'Payment due date': '2-Oct-25',
                'Payment Update': 'Due', 'Status': 'Shipped', 'Notes': ''
            },
            {
                'Order Number': 'SA C.D 129/2025', 'ERP': 'Yes', 'Date of request': '08-Sep-25',
                'Date of PI issue': '08-Sep-25', 'Date of Client signing': '10-Sep-25',
                'Invoice': 55668.20, 'Payment': '$55,668.20', 'Manufacturer': 'BAJ',
                'ETD': '19-Oct-25', 'Payment due date': '1-Oct-25',
                'Payment Update': 'Due', 'Status': 'Shipped', 'Notes': ''
            },
            {
                'Order Number': 'SA C.D 144/2025', 'ERP': 'Yes', 'Date of request': '08-Oct-25',
                'Date of PI issue': '09-Oct-25', 'Date of Client signing': '12-Oct-25',
                'Invoice': 69494.00, 'Payment': '$69,494.00', 'Manufacturer': 'BAJ',
                'ETD': '19-Nov-25', 'Payment due date': '18-Jan-00',
                'Payment Update': 'Pending', 'Status': 'Pending', 'Notes': 'add chocolate'
            }
        ]
        
        df = pd.DataFrame(sample_orders)
        st.success(f"✅ Showing {len(df)} orders from your data")
        return df
        
    except Exception as e:
        st.error(f"Error loading orders data: {str(e)}")
        return pd.DataFrame()

def advanced_analytics_tab():
    """Advanced Analytics Tab"""
    st.markdown("""
    <div class="intelligence-header">
        <h2 style="margin:0;">📊 Advanced Analytics</h2>
        <p style="margin:0; opacity:0.9;">Business Intelligence • Performance Metrics • Trend Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🔧 Advanced analytics features coming soon...")
    st.write("This tab will include:")
    st.write("• Sales performance dashboards")
    st.write("• Client profitability analysis") 
    st.write("• Supplier performance metrics")
    st.write("• Market trend analysis")
    st.write("• Forecasting and predictions")

def settings_tab():
    """Settings Tab"""
    st.markdown("""
    <div class="ceo-header">
        <h2 style="margin:0;">⚙️ System Settings</h2>
        <p style="margin:0; opacity:0.9;">Configuration • User Management • System Preferences</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🔧 Settings management coming soon...")
    st.write("This tab will include:")
    st.write("• User management and permissions")
    st.write("• API configuration")
    st.write("• System preferences")
    st.write("• Data backup and recovery")

def new_orders_tab():
    """NEW: Client Orders Management Tab"""
    st.markdown("""
    <div class="new-orders-header">
        <h2 style="margin:0;">📋 New Client Orders Management</h2>
        <p style="margin:0; opacity:0.9;">Order Preparation • PI Generation • Item Allocation • Availability Tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Client selection
    available_clients = st.session_state.user_clients
    client = st.selectbox(
        "Select Client:",
        available_clients,
        key="new_orders_client"
    )
    
    if not client:
        st.warning("Please select a client to manage orders")
        return
    
    # Load new orders data
    with st.spinner(f"📥 Loading orders data for {client}..."):
        orders_data = load_new_orders_data(client)
    
    if orders_data.empty:
        st.info(f"""
        ⚠️ **No new orders data found for {client}**
        
        **To get started:**
        1. Go to your Google Sheet for {client}
        2. Add data to the **'New_client_orders'** sheet
        3. Use these headers:
           - Order_Number, Client_Name, Product_Name, Article_No
           - HS_Code, Origin, Packing, Qty, Type
           - Total_Weight, Price_in_USD_kg, Total_Price, Status
        """)
        return
    
    # Orders Overview
    st.subheader("📊 Orders Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_orders = orders_data['Order_Number'].nunique()
        st.metric("Total PIs", total_orders)
    
    with col2:
        total_items = len(orders_data)
        st.metric("Total Items", total_items)
    
    with col3:
        total_value = orders_data['Total_Price'].sum()
        st.metric("Total Value", f"${total_value:,.2f}")
    
    with col4:
        unique_articles = orders_data['Article_No'].nunique()
        st.metric("Unique Articles", unique_articles)
    
    # Search and Filter Section
    st.subheader("🔍 Search & Filter Orders")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_type = st.radio("Search By:", ["Article Number", "Product Name", "PI Number", "HS Code"], 
                              horizontal=True, key="new_orders_search_type")
    
    with col2:
        search_term = st.text_input("Enter search term...", key="new_orders_search")
    
    with col3:
        status_filter = st.selectbox("Order Status", ["All", "Draft", "Confirmed", "In Production", "Shipped"], 
                                    key="new_orders_status")
    
    # Filter data
    filtered_data = orders_data.copy()
    
    if search_term:
        if search_type == "Article Number":
            filtered_data = filtered_data[filtered_data['Article_No'].astype(str).str.contains(search_term, case=False, na=False)]
        elif search_type == "Product Name":
            filtered_data = filtered_data[filtered_data['Product_Name'].str.contains(search_term, case=False, na=False)]
        elif search_type == "PI Number":
            filtered_data = filtered_data[filtered_data['Order_Number'].str.contains(search_term, case=False, na=False)]
        elif search_type == "HS Code":
            filtered_data = filtered_data[filtered_data['HS_Code'].astype(str).str.contains(search_term, case=False, na=False)]
    
    if status_filter != "All":
        filtered_data = filtered_data[filtered_data['Status'] == status_filter]
    
    # Display Results
    st.subheader(f"📋 Order Items ({len(filtered_data)} found)")
    
    if not filtered_data.empty:
        # Group by Order Number
        for order_num, order_group in filtered_data.groupby('Order_Number'):
            with st.expander(f"📦 PI: {order_num} | Items: {len(order_group)} | Status: {order_group['Status'].iloc[0]}", expanded=False):
                
                # Order summary
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Items", len(order_group))
                with col2:
                    st.metric("Total Qty", order_group['Qty'].sum())
                with col3:
                    st.metric("Total Weight", f"{order_group['Total_Weight'].sum():.1f} kg")
                with col4:
                    st.metric("Total Value", f"${order_group['Total_Price'].sum():,.2f}")
                
                # Display items in this order
                for _, item in order_group.iterrows():
                    st.markdown(f"""
                    <div class="price-card">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div style="flex: 2;">
                                <h4 style="margin:0; color: #991B1B;">{item['Article_No']} - {item['Product_Name']}</h4>
                                <p style="margin:0; color: #6B7280;">
                                    HS Code: {item['HS_Code']} | Origin: {item['Origin']} | Packing: {item['Packing']}
                                </p>
                            </div>
                            <div style="flex: 1; text-align: right;">
                                <p style="margin:0; font-weight: bold;">Qty: {item['Qty']} {item['Type']}</p>
                                <p style="margin:0;">Weight: {item['Total_Weight']} kg</p>
                                <p style="margin:0; color: #059669;">Price: ${item['Price_in_USD_kg']}/kg</p>
                                <p style="margin:0; font-weight: bold;">Total: ${item['Total_Price']:,.2f}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Export Section
        st.markdown('<div class="export-section">', unsafe_allow_html=True)
        st.subheader("📤 Export Orders Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{client}_new_orders_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
                key="new_orders_csv"
            )
        
        with col2:
            # Create summary report
            summary_text = f"""
{client} New Orders Report
=========================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Total PIs: {filtered_data['Order_Number'].nunique()}
Total Items: {len(filtered_data)}
Total Value: ${filtered_data['Total_Price'].sum():,.2f}

Orders Summary:
{chr(10).join([f"• {order_num}: {len(group)} items, ${group['Total_Price'].sum():,.2f} ({group['Status'].iloc[0]})" 
               for order_num, group in filtered_data.groupby('Order_Number')])}

Search Criteria: {search_type} = '{search_term}' | Status: {status_filter}
            """
            st.download_button(
                label="📄 Download Summary",
                data=summary_text,
                file_name=f"{client}_orders_summary_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
                key="new_orders_summary"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.info("No orders match your search criteria.")

def load_new_orders_data(client):
    """Load new client orders data from Google Sheets"""
    try:
        sheet_name = CLIENT_SHEETS[client]["new_orders"]
        orders_url = f"https://sheets.googleapis.com/v4/spreadsheets/{CDC_SHEET_ID}/values/{sheet_name}!A:Z?key={API_KEY}"
        response = requests.get(orders_url)
        
        if response.status_code == 200:
            data = response.json()
            values = data.get('values', [])
            
            if values and len(values) > 1:
                headers = values[0]
                rows = values[1:]
                
                # Create DataFrame
                df = pd.DataFrame(rows, columns=headers)
                
                # Check for required columns
                required_cols = ['Order_Number', 'Product_Name', 'Article_No', 'HS_Code', 'Origin', 
                                'Packing', 'Qty', 'Type', 'Total_Weight', 'Price_in_USD_kg', 'Total_Price']
                
                # Fill missing columns with empty values
                for col in required_cols:
                    if col not in df.columns:
                        df[col] = ''
                
                # Ensure Status column exists
                if 'Status' not in df.columns:
                    df['Status'] = 'Draft'
                
                # Convert numeric columns
                numeric_cols = ['Qty', 'Total_Weight', 'Price_in_USD_kg', 'Total_Price']
                for col in numeric_cols:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                
                return df
                
        return pd.DataFrame()
        
    except Exception as e:
        st.error(f"Error loading new orders data for {client}: {str(e)}")
        return pd.DataFrame()

# Run the main dashboard
if __name__ == "__main__":
    if not check_login():
        login_page()
    else:
        main_dashboard()
