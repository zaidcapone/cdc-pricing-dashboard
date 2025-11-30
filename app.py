import time
import functools
import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime
from io import BytesIO
import time
import functools

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
    /* Your existing CSS remains the same */
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
    /* ... (keep all your existing CSS styles) ... */
</style>
""", unsafe_allow_html=True)

# Configuration
API_KEY = "AIzaSyA3P-ZpLjDdVtGB82_1kaWuO7lNbKDj9HU"
CDC_SHEET_ID = "1qWgVT0l76VsxQzYExpLfioBHprd3IvxJzjQWv3RryJI"

# User authentication
USERS = {
    "admin": {"password": "123456", "clients": ["CDC", "CoteDivoire", "CakeArt", "SweetHouse", "Cameron"]},
    "ceo": {"password": "123456", "clients": ["CDC", "CoteDivoire", "CakeArt", "SweetHouse", "Cameron"]},
    "zaid": {"password": "123456", "clients": ["CDC"]},
    "mohammad": {"password": "123456", "clients": ["CoteDivoire"]},
    "Khalid": {"password": "123456", "clients": ["CakeArt", "SweetHouse"]},
    "Rotana": {"password": "123456", "clients": ["CDC"]}
}

# Client data sheets mapping
CLIENT_SHEETS = {
    "CDC": {
        "backaldrin": "Backaldrin_CDC",
        "bateel": "Bateel_CDC", 
        "ceo_special": "CDC_CEO_Special_Prices",
        "new_orders": "New_client_orders",
        "paid_orders": "Paid_Orders",
        "palletizing": "Palletizing_Data"
    },
    "CoteDivoire": {
        "backaldrin": "Backaldrin_CoteDivoire",
        "bateel": "Bateel_CoteDivoire", 
        "ceo_special": "CoteDivoire_CEO_Special_Prices",
        "new_orders": "New_client_orders",
        "palletizing": "Palletizing_Data"
    },
    "CakeArt": {
        "backaldrin": "Backaldrin_CakeArt",
        "bateel": "Bateel_CakeArt",
        "ceo_special": "CakeArt_CEO_Special_Prices",
        "new_orders": "New_client_orders",
        "palletizing": "Palletizing_Data"
    },
    "SweetHouse": {
        "backaldrin": "Backaldrin_SweetHouse",
        "bateel": "Bateel_SweetHouse",
        "ceo_special": "SweetHouse_CEO_Special_Prices",
        "new_orders": "New_client_orders",
        "palletizing": "Palletizing_Data"
    },
    "Cameron": {
        "backaldrin": "Backaldrin_Cameron",
        "bateel": "Bateel_Cameron", 
        "ceo_special": "Cameron_CEO_Special_Prices",
        "new_orders": "New_client_orders",
        "palletizing": "Palletizing_Data"
    }
}

# Product Catalog Sheet Name
PRODUCT_CATALOG_SHEET = "FullProductList"
PRICES_SHEET = "Prices"

# ==================== PERFORMANCE OPTIMIZATIONS ====================

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
                # Clear cache on login to get fresh data
                clear_cache()
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
        clear_cache()
        st.rerun()

def main_dashboard():
    """Main dashboard with performance optimizations"""
    
    # Display user info in sidebar
    st.sidebar.markdown(f"**👤 Welcome, {st.session_state.username}**")
    st.sidebar.markdown(f"**🏢 Access to:** {', '.join(st.session_state.user_clients)}")
    
    # Cache management in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚡ Performance")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🔄 Refresh Data", use_container_width=True):
            clear_cache()
            st.success("Cache cleared! Loading fresh data...")
            st.rerun()
    
    with col2:
        cache_size = len(st.session_state.get('app_cache', {}))
        st.metric("Cached Items", cache_size)
    
    # General Announcements
    st.sidebar.markdown("### 📢 General Announcements")
    announcements = [
        "🚨 ETD is officially working!",
        "📦 Working on palletizing",
        "⭐ **SPECIAL OFFER**",
        "🔔 **REMINDER**:",
        "📊 **NEW FEATURE**: HS Code search now available across all clients",
        "📦 **NEW**: Palletizing Calculator added!",
        "💰 **NEW**: All Customers Prices tab added!"
    ]
    
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
    
    # Create tabs with loading states
    if st.session_state.username in ["ceo", "admin"]:
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
            "🏢 CLIENTS", "💰 PRICES", "📋 NEW ORDERS", "📅 ETD SHEET", 
            "⭐ CEO SPECIAL PRICES", "💰 PRICE INTELLIGENCE", "📦 PRODUCT CATALOG",
            "📊 ORDERS MANAGEMENT", "📦 PALLETIZING"
        ])
    else:
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "🏢 CLIENTS", "💰 PRICES", "📋 NEW ORDERS", "📅 ETD SHEET", 
            "⭐ CEO SPECIAL PRICES", "💰 PRICE INTELLIGENCE", "📦 PRODUCT CATALOG",
            "📊 ORDERS MANAGEMENT", "📦 PALLETIZING"
        ])
    
    # Load tabs with individual loading states
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
        
    if st.session_state.username in ["ceo", "admin"]:
        with tab9:
            palletizing_tab()
    else:
        with tab8:
            palletizing_tab()

# ==================== OPTIMIZED DATA LOADING FUNCTIONS ====================

@cache_data(ttl=300)  # Cache for 5 minutes
def load_sheet_data(sheet_name, start_row=0):
    """Universal Google Sheets loader with caching"""
    try:
        import urllib.parse
        encoded_sheet = urllib.parse.quote(sheet_name)
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{CDC_SHEET_ID}/values/{encoded_sheet}!A:Z?key={API_KEY}"
        
        response = requests.get(url, timeout=30)  # Added timeout
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

@cache_data(ttl=300)
def get_google_sheets_data(client="CDC"):
    """Optimized version with caching"""
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
        required_cols = ['article_number', 'product_name', 'price_per_', 'order_number', 'order_date']
        available_cols = [col for col in required_cols if col in df.columns]
        
        if not available_cols:
            return {}
        
        # Group by article number
        for _, row in df.iterrows():
            article_num = str(row.get('article_number', ''))
            if not article_num or article_num == 'nan':
                continue
                
            if article_num not in result:
                result[article_num] = {
                    'names': [],
                    'prices': [],
                    'orders': []
                }
            
            # Add product name if available
            product_name = row.get('product_name', '')
            if product_name and product_name not in result[article_num]['names']:
                result[article_num]['names'].append(product_name)
            
            # Add price if available
            price = row.get('price_per_', '')
            if price and str(price) != 'nan':
                try:
                    price_float = float(price)
                    result[article_num]['prices'].append(price_float)
                except (ValueError, TypeError):
                    pass
            
            # Add order details
            order_no = row.get('order_number', '')
            date = row.get('order_date', '')
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

# ==================== OPTIMIZED TAB FUNCTIONS ====================

def clients_tab():
    """Clients management tab with loading optimization"""
    st.subheader("Client Selection")
    
    # Client selection - only show clients user has access to
    available_clients = st.session_state.user_clients
    client = st.selectbox(
        "Select Client:",
        available_clients,
        key="client_select"
    )
    
    if client:
        # Use a placeholder to prevent full rerun
        placeholder = st.empty()
        with placeholder.container():
            cdc_dashboard(client)

def cdc_dashboard(client):
    """Client pricing dashboard with performance optimizations"""
    
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

    # Load data with progress indicator
    with st.spinner(f"📥 Loading {client} data..."):
        DATA = get_google_sheets_data(client)
    
    if not DATA["Backaldrin"] and not DATA["Bateel"]:
        st.error(f"❌ No data found for {client}. Please check the Google Sheets.")
        return
        
    st.success(f"✅ Connected to Google Sheets - Live Data for {client}!")

    # Refresh button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh", use_container_width=True, type="secondary", key=f"{client}_refresh"):
            # Clear cache for this client only
            clear_cache()
            st.rerun()

    # Supplier selection
    st.subheader("🏢 Select Supplier")
    supplier = st.radio("", ["Backaldrin", "Bateel"], horizontal=True, label_visibility="collapsed", key=f"{client}_supplier")

    # Search section
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
                if st.button(suggestion["display"], use_container_width=True, key=f"{client}_sugg_{i}"):
                    st.session_state.search_results = {
                        "article": suggestion["value"],
                        "supplier": supplier,
                        "client": client
                    }
                    st.rerun()
    
    # Manual search
    if st.button("🚀 SEARCH HISTORICAL PRICES", use_container_width=True, type="primary", key=f"{client}_search"):
        with st.spinner("Searching..."):
            handle_search(article, product, hs_code, supplier, DATA, client)

    # Display results from session state
    if st.session_state.search_results and st.session_state.search_results.get("client") == client:
        display_from_session_state(DATA, client)
        

# ==================== ADD THE MISSING FUNCTIONS ====================

def etd_tab():
    """ETD Sheet with caching"""
    # [Add your existing etd_tab function here]
    pass

def ceo_specials_tab():
    """CEO Special Prices tab with caching"""
    # [Add your existing ceo_specials_tab function here]
    pass

def price_intelligence_tab():
    """CEO Price Intelligence with caching"""
    # [Add your existing price_intelligence_tab function here]
    pass

def product_catalog_tab():
    """Product Catalog with caching"""
    # [Add your existing product_catalog_tab function here]
    pass

def orders_management_tab():
    """Orders Management with caching"""
    # [Add your existing orders_management_tab function here]
    pass

def new_orders_tab():
    """New Orders with caching"""
    # [Add your existing new_orders_tab function here]
    pass

# Run the main dashboard
if __name__ == "__main__":
    if not check_login():
        login_page()
    else:
        main_dashboard()
