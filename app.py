# ============================================
# MULTI-CLIENT PRICING DASHBOARD - CONSOLIDATED EDITION
# ============================================
# Author: Zaid F. Al-Shami
# Version: 6.0 (Consolidated - 5 Tabs)
# Last Updated: 07 April 2026
# ============================================

import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime
from io import BytesIO
import re

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Multi-Client Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# PROFESSIONAL CSS (Condensed but保留了所有重要样式)
# ============================================
st.markdown("""
<style>
    /* Hide Streamlit default header */
    header {display: none !important;}
    .main .block-container {padding-top: 0rem !important;}
    footer {display: none !important;}
    
    /* ===== GLOBAL STYLES ===== */

    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    .main { padding: 0rem 1rem; }
    
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 10px; }
    ::-webkit-scrollbar-thumb { background: #c1c1c1; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #a8a8a8; }
    
    .dashboard-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .dashboard-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: white;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .dashboard-subtitle {
        color: #94a3b8;
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
    }
    
    .modern-card {
        background: white;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 1.25rem;
        color: white;
        text-align: center;
    }
    
    .stat-value { font-size: 2rem; font-weight: 700; margin: 0.5rem 0; }
    .stat-label { font-size: 0.85rem; opacity: 0.9; text-transform: uppercase; }
    
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1e293b;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .subsection-header {
        font-size: 1rem;
        font-weight: 600;
        color: #475569;
        margin: 1rem 0 0.75rem 0;
    }
    
    .price-card-primary {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border-left: 4px solid #dc2626;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        color: #1e293b !important;
    }
    
    .price-card-secondary {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border-left: 4px solid #f59e0b;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        color: #1e293b !important;
    }
    
    .price-card-info {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-left: 4px solid #3b82f6;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        color: #1e293b !important;
    }
    
    .badge-success { background: #d1fae5; color: #065f46; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; }
    .badge-warning { background: #fed7aa; color: #9a3412; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; }
    .badge-danger { background: #fee2e2; color: #991b1b; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; }
    .badge-info { background: #dbeafe; color: #1e40af; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
        border-right: 1px solid #334155 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p {
        color: #f1f5f9 !important;
    }
    
    [data-testid="stSidebar"] .stButton button {
        background: transparent !important;
        color: #cbd5e1 !important;
        border: 1px solid #334155 !important;
        text-align: left !important;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background: #334155 !important;
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
    }
    
    .announcement-item {
        background: linear-gradient(135deg, #1e3a5f 0%, #1e293b 100%) !important;
        border-left: 3px solid #3b82f6 !important;
        padding: 0.75rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: #bae6fd !important;
    }
    
    .dashboard-footer {
        text-align: center;
        padding: 1.5rem;
        color: #94a3b8;
        font-size: 0.8rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 2rem;
    }
    
    /* Fix for card text colors */
    .price-card-primary div, .price-card-primary p, .price-card-primary strong, .price-card-primary span,
    .price-card-secondary div, .price-card-secondary p, .price-card-secondary strong, .price-card-secondary span,
    .price-card-info div, .price-card-info p, .price-card-info strong, .price-card-info span {
        color: #1e293b !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# CONFIGURATION
# ============================================
API_KEY = "AIzaSyA3P-ZpLjDdVtGB82_1kaWuO7lNbKDj9HU"
CDC_SHEET_ID = "1qWgVT0l76VsxQzYExpLfioBHprd3IvxJzjQWv3RryJI"

# User authentication
USERS = {
    "admin": {"password": "123456", "clients": ["CDC", "CoteDivoire", "CakeArt", "SweetHouse", "Cameron", "Qzine", "MEPT"]},
    "ceo": {"password": "123456", "clients": ["CDC", "CoteDivoire", "CakeArt", "SweetHouse", "Cameron", "Qzine", "MEPT"]},
    "zaid": {"password": "123456", "clients": ["CDC"]},
    "mohammad": {"password": "123456", "clients": ["CoteDivoire"]},
    "Khalid": {"password": "123456", "clients": ["CakeArt", "SweetHouse"]},
    "Rotana": {"password": "123456", "clients": ["CDC"]},
    "Abed": {"password": "123456", "clients": ["Qzine", "MEPT"]}
}

# Client data sheets mapping
CLIENT_SHEETS = {
    "CDC": {"ceo_special": "CDC_CEO_Special_Prices", "palletizing": "Palletizing_Data"},
    "CoteDivoire": {"ceo_special": "CoteDivoire_CEO_Special_Prices", "palletizing": "Palletizing_Data"},
    "CakeArt": {"ceo_special": "CakeArt_CEO_Special_Prices", "palletizing": "Palletizing_Data"},
    "SweetHouse": {"ceo_special": "SweetHouse_CEO_Special_Prices", "palletizing": "Palletizing_Data"},
    "Cameron": {"ceo_special": "Cameron_CEO_Special_Prices", "palletizing": "Palletizing_Data"},
    "Qzine": {"ceo_special": "Qzine_CEO_Special_Prices", "palletizing": "Palletizing_Data"},
    "MEPT": {"ceo_special": "MEPT_CEO_Special_Prices", "palletizing": "Palletizing_Data"}
}

# Sheet names
PRODUCT_CATALOG_SHEET = "FullProductList"
PRICES_SHEET = "Prices"
GENERAL_PRICES_SHEET = "General_prices"

# ============================================
# HELPER FUNCTIONS
# ============================================

@st.cache_data(ttl=300)
def load_sheet_data(sheet_name, start_row=0):
    """Universal Google Sheets loader"""
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
                headers_count = len(headers)
                rows = values[start_row + 1:] if len(values) > start_row + 1 else []
                
                padded_rows = []
                for row in rows:
                    if len(row) < headers_count:
                        row = row + [''] * (headers_count - len(row))
                    elif len(row) > headers_count:
                        row = row[:headers_count]
                    padded_rows.append(row)
                
                df = pd.DataFrame(padded_rows, columns=headers)
                df = df.replace('', pd.NA)
                return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading {sheet_name}: {str(e)}")
        return pd.DataFrame()

def get_all_clients_from_master():
    """Get list of all unique clients from Clients_CoC sheet"""
    try:
        master_df = load_sheet_data("Clients_CoC")
        if not master_df.empty and 'Client' in master_df.columns:
            return sorted(master_df['Client'].dropna().unique().tolist())
        return []
    except:
        return []

@st.cache_data(ttl=300)
def get_google_sheets_data(client="CDC"):
    """Load client data from Clients_CoC master sheet"""
    try:
        master_df = load_sheet_data("Clients_CoC")
        
        if master_df.empty:
            return {"Backaldrin": {}, "Bateel": {}}
        
        client_df = master_df[master_df['Client'] == client].copy()
        
        if client_df.empty:
            return {"Backaldrin": {}, "Bateel": {}}
        
        backaldrin_df = client_df[client_df['Supplier'] == 'Backaldrin']
        bateel_df = client_df[client_df['Supplier'] == 'Bateel']
        
        def convert_df_to_dict(df):
            result = {}
            if df.empty:
                return result
            
            article_col = 'Article_Number'
            product_col = 'Product_Name'
            price_col = 'Price'
            order_col = 'Order_Number'
            date_col = 'Order_Date'
            year_col = 'Year'
            hs_code_col = 'HS_Code'
            packaging_col = 'Packaging'
            quantity_col = 'Quantity'
            weight_col = 'Total_Weight'
            total_price_col = 'Total_Price'
            
            if article_col not in df.columns:
                return result
            
            for _, row in df.iterrows():
                article = str(row.get(article_col, '')).strip()
                if not article or article == 'nan':
                    continue
                    
                if article not in result:
                    result[article] = {'names': [], 'prices': [], 'orders': []}
                
                product_name = str(row.get(product_col, '')).strip()
                if product_name and product_name != 'nan' and product_name not in result[article]['names']:
                    result[article]['names'].append(product_name)
                
                price_str = str(row.get(price_col, '')).strip()
                if price_str and price_str != 'nan':
                    try:
                        price_float = float(price_str)
                        result[article]['prices'].append(price_float)
                    except:
                        pass
                
                order_details = {
                    'order_no': str(row.get(order_col, '')).strip() if order_col in df else '',
                    'date': str(row.get(date_col, '')).strip() if date_col in df else '',
                    'year': str(row.get(year_col, '')).strip() if year_col in df else '',
                    'product_name': product_name,
                    'article': article,
                    'hs_code': str(row.get(hs_code_col, '')).strip() if hs_code_col in df else '',
                    'packaging': str(row.get(packaging_col, '')).strip() if packaging_col in df else '',
                    'quantity': str(row.get(quantity_col, '')).strip() if quantity_col in df else '',
                    'total_weight': str(row.get(weight_col, '')).strip() if weight_col in df else '',
                    'price': str(row.get(price_col, '')).strip() if price_col in df else '',
                    'total_price': str(row.get(total_price_col, '')).strip() if total_price_col in df else ''
                }
                result[article]['orders'].append(order_details)
            
            return result
        
        return {"Backaldrin": convert_df_to_dict(backaldrin_df), "Bateel": convert_df_to_dict(bateel_df)}
        
    except Exception as e:
        st.error(f"Error loading data for {client}: {str(e)}")
        return {"Backaldrin": {}, "Bateel": {}}

@st.cache_data(ttl=600)
def load_product_catalog():
    """Load product catalog"""
    try:
        df = load_sheet_data(PRODUCT_CATALOG_SHEET)
        if not df.empty and 'Article_Number' in df.columns:
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading product catalog: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=600)
def load_prices_data():
    """Load all prices data"""
    try:
        df = load_sheet_data(PRICES_SHEET)
        if not df.empty:
            if 'Price' in df.columns:
                df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading prices data: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=600)
def load_general_prices_data():
    """Load General_prices data"""
    try:
        df = load_sheet_data(GENERAL_PRICES_SHEET)
        if not df.empty:
            if 'NEW EXW' in df.columns:
                df['NEW EXW'] = pd.to_numeric(df['NEW EXW'], errors='coerce')
            if 'UNT WGT' in df.columns:
                df['UNT WGT'] = pd.to_numeric(df['UNT WGT'], errors='coerce')
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading general prices: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_ceo_special_prices(client="CDC"):
    """Load CEO special prices"""
    try:
        sheet_name = CLIENT_SHEETS[client]["ceo_special"]
        df = load_sheet_data(sheet_name)
        if not df.empty:
            required_cols = ['Article_Number', 'Product_Name', 'Special_Price', 'Currency', 'Incoterm']
            if all(col in df.columns for col in required_cols):
                return df
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=180)
def load_etd_data(sheet_id, sheet_name):
    """Load ETD data"""
    try:
        import urllib.parse
        encoded_sheet = urllib.parse.quote(sheet_name)
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{encoded_sheet}!A:Z?key={API_KEY}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            values = data.get('values', [])
            if values and len(values) > 13:
                headers = values[13]
                rows = values[14:] if len(values) > 14 else []
                df = pd.DataFrame(rows, columns=headers)
                return df
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

def add_to_search_history(search_term, client, supplier, article_num=None):
    """Add search to history"""
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
    
    st.session_state.search_history.insert(0, {
        'timestamp': datetime.now(),
        'search_term': search_term,
        'client': client,
        'supplier': supplier,
        'article_num': article_num
    })
    
    if len(st.session_state.search_history) > 20:
        st.session_state.search_history = st.session_state.search_history[:20]

def format_time_ago(timestamp):
    """Format timestamp"""
    diff = datetime.now() - timestamp
    if diff.days > 0:
        return f"{diff.days}d ago"
    elif diff.seconds >= 3600:
        return f"{diff.seconds // 3600}h ago"
    elif diff.seconds >= 60:
        return f"{diff.seconds // 60}m ago"
    return "Just now"

def check_login():
    """Check login status"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'user_clients' not in st.session_state:
        st.session_state.user_clients = []
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "📋 CLIENT ORDERS"
    return st.session_state.logged_in

def login_page():
    """Login page - Compact version"""
    # Create a simple centered container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <style>
            .compact-login {
                background: white;
                border-radius: 16px;
                padding: 2rem;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                margin-top: 3rem;
            }
            .compact-login h1 {
                font-size: 1.5rem;
                text-align: center;
                margin-bottom: 0.5rem;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .compact-login p {
                text-align: center;
                color: #64748b;
                font-size: 0.85rem;
                margin-bottom: 1.5rem;
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="compact-login">', unsafe_allow_html=True)
        st.markdown('<h1>📊 Multi-Client Dashboard</h1>', unsafe_allow_html=True)
        st.markdown('<p>Sign in to access your dashboard</p>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username", key="login_username")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
            submit = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit:
                if username in USERS and USERS[username]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_clients = USERS[username]["clients"]
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        st.markdown('</div>', unsafe_allow_html=True)

def logout_button():
    """Logout button"""
    if st.button("🚪 Logout", key="logout_header", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user_clients = []
        st.rerun()

# ============================================
# TAB 1: CLIENT ORDERS (Merged: CLIENTS + CLIENT'S ORDERS)
# ============================================

def client_orders_tab():
    """Consolidated Client Orders Tab - Search orders by client"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0891b2, #0e7c8c); padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem;">
        <h2 style="margin:0; color: white;">📋 Client Orders</h2>
        <p style="margin:0; opacity:0.9; color: white;">Search order history by article, product name, or HS code • Filter by date</p>
    </div>
    """, unsafe_allow_html=True)
    
    available_clients = st.session_state.user_clients
    client = st.selectbox("Select Client:", available_clients, key="client_orders_client")
    
    if not client:
        st.warning("No clients available")
        return
    
    with st.spinner(f"Loading data for {client}..."):
        DATA = get_google_sheets_data(client)
    
    if not DATA.get("Backaldrin") and not DATA.get("Bateel"):
        st.error(f"No data found for {client}")
        return
    
    supplier = st.radio("Select Supplier:", ["Backaldrin", "Bateel"], horizontal=True, key="client_orders_supplier")
    supplier_data = DATA.get(supplier, {})
    
    # Search Section
    st.markdown("<div class='subsection-header'>🔍 Search Orders</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_term = st.text_input("Search by Article, Product, or HS Code:", placeholder="e.g., 1-366, Chocolate...", key="client_orders_search")
    with col2:
        search_type = st.selectbox("Search Type:", ["All", "Article Number", "Product Name", "HS Code"], key="client_orders_search_type")
    with col3:
        if st.button("🔍 Search", type="primary", use_container_width=True, key="client_orders_search_btn"):
            if search_term:
                add_to_search_history(search_term, client, supplier)
    
    # Date Filter Section
    st.markdown("<div class='subsection-header'>📅 Date Filter (Optional)</div>", unsafe_allow_html=True)
    
    filter_type = st.radio("Filter by:", ["All Time", "Year", "Date Range"], horizontal=True, key="client_orders_filter_type")
    
    selected_year = None
    start_date = None
    end_date = None
    
    if filter_type == "Year":
        available_years = set()
        for article_num, article_data in supplier_data.items():
            for order in article_data.get('orders', []):
                year = order.get('year', '')
                if year and year != 'nan':
                    year_str = str(year).strip()
                    if year_str.isdigit() and len(year_str) == 4:
                        available_years.add(year_str)
        available_years = sorted(list(available_years), reverse=True)
        if available_years:
            selected_year = st.selectbox("Select Year:", available_years, key="client_orders_year")
    
    elif filter_type == "Date Range":
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("From Date:", value=datetime.now().date() - pd.Timedelta(days=365), key="client_orders_start")
        with col2:
            end_date = st.date_input("To Date:", value=datetime.now().date(), key="client_orders_end")
    
    # Search and Display Results
    if search_term:
        search_results = []
        search_lower = search_term.lower()
        
        for article_num, article_data in supplier_data.items():
            match_found = False
            match_type = ""
            
            if search_type in ["All", "Article Number"]:
                if search_lower in article_num.lower():
                    match_found = True
                    match_type = "Article Number"
            
            if not match_found and search_type in ["All", "Product Name"]:
                for name in article_data.get('names', []):
                    if search_lower in str(name).lower():
                        match_found = True
                        match_type = "Product Name"
                        break
            
            if not match_found and search_type in ["All", "HS Code"]:
                for order in article_data.get('orders', []):
                    hs_code = str(order.get('hs_code', '')).lower()
                    if search_lower in hs_code:
                        match_found = True
                        match_type = "HS Code"
                        break
            
            if match_found and article_data.get('orders'):
                product_name = article_data['names'][0] if article_data.get('names') else ""
                prices = article_data.get('prices', [])
                
                search_results.append({
                    'article': article_num,
                    'product_name': product_name,
                    'match_type': match_type,
                    'orders_count': len(article_data.get('orders', [])),
                    'min_price': min(prices) if prices else None,
                    'max_price': max(prices) if prices else None,
                    'article_data': article_data
                })
        
        if search_results:
            st.success(f"Found {len(search_results)} matching items")
            
            # Display stats
            col1, col2, col3 = st.columns(3)
            col1.metric("Items Found", len(search_results))
            total_orders = sum(r['orders_count'] for r in search_results)
            col2.metric("Total Orders", total_orders)
            
            all_prices = []
            for r in search_results:
                if r['min_price']:
                    all_prices.append(r['min_price'])
                if r['max_price']:
                    all_prices.append(r['max_price'])
            if all_prices:
                col3.metric("Price Range", f"${min(all_prices):.2f} - ${max(all_prices):.2f}")
            
            # Display each result
            for result in search_results:
                # Filter orders by date
                filtered_orders = result['article_data'].get('orders', []).copy()
                
                if filter_type == "Year" and selected_year:
                    filtered_orders = []
                    for order in result['article_data'].get('orders', []):
                        order_year = order.get('year', '')
                        if order_year and order_year != 'nan':
                            year_str = str(order_year).strip()
                            if year_str.isdigit() and len(year_str) == 4 and year_str == selected_year:
                                filtered_orders.append(order)
                        elif order.get('date', ''):
                            date_str = str(order.get('date', '')).strip()
                            for fmt in ['%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']:
                                try:
                                    date_obj = datetime.strptime(date_str, fmt)
                                    if str(date_obj.year) == selected_year:
                                        filtered_orders.append(order)
                                    break
                                except:
                                    continue
                
                elif filter_type == "Date Range" and start_date and end_date:
                    filtered_orders = []
                    for order in result['article_data'].get('orders', []):
                        date_str = str(order.get('date', '')).strip()
                        if date_str and date_str != 'nan':
                            for fmt in ['%d.%m.%Y', '%d/%m/%Y', '%d-%m-%m', '%Y-%m-%d']:
                                try:
                                    date_obj = datetime.strptime(date_str, fmt)
                                    if start_date <= date_obj.date() <= end_date:
                                        filtered_orders.append(order)
                                    break
                                except:
                                    continue
                
                filter_info = ""
                if filter_type == "Year" and selected_year:
                    filter_info = f" | Year: {selected_year}"
                elif filter_type == "Date Range" and start_date and end_date:
                    filter_info = f" | {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
                
                with st.expander(f"📦 {result['article']} - {result['product_name']} | {len(filtered_orders)} orders{filter_info}", expanded=False):
                    if not filtered_orders:
                        st.info(f"No orders found in selected date range. Total orders available: {result['orders_count']}")
                    else:
                        for order in filtered_orders:
                            price_display = order.get('price', 'N/A')
                            try:
                                price_val = float(str(price_display).replace('$', '').replace(',', '').strip())
                                price_display = f"${price_val:.2f}"
                            except:
                                price_display = f"${price_display}" if price_display != 'N/A' else 'N/A'
                            
                            st.markdown(f"""
                            <div class="price-card-primary" style="margin-bottom: 0.5rem;">
                                <div style="display: flex; justify-content: space-between;">
                                    <div>
                                        <strong>Order:</strong> {order.get('order_no', 'N/A')}<br>
                                        <strong>Date:</strong> {order.get('date', 'N/A')}
                                    </div>
                                    <div>
                                        <strong>Price:</strong> {price_display}/kg
                                    </div>
                                </div>
                                <div style="margin-top: 0.5rem; font-size: 0.85rem; color: #64748b;">
                                    {order.get('quantity', 'N/A')} units • {order.get('total_weight', 'N/A')} kg
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
        else:
            st.warning(f"No results found for '{search_term}'")
    else:
        st.info("Enter a search term above to find order history")

# ============================================
# TAB 2: PRICING HUB (Merged: PRICES + ALL PRICES + PRICE INTELLIGENCE)
# ============================================

def pricing_hub_tab():
    """Consolidated Pricing Hub - Customer prices, General prices, and Price Intelligence"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #7c3aed, #6d28d9); padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem;">
        <h2 style="margin:0; color: white;">💰 Pricing Hub</h2>
        <p style="margin:0; opacity:0.9; color: white;">Customer prices • General price list • Cross-client price intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create sub-tabs within Pricing Hub
    sub_tab1, sub_tab2, sub_tab3 = st.tabs(["🏢 Customer Prices", "📊 General Price List", "🔍 Price Intelligence"])
    
    # SUB-TAB 1: Customer Prices
    with sub_tab1:
        st.markdown("<div class='subsection-header'>🏢 Customer Price Database</div>", unsafe_allow_html=True)
        
        with st.spinner("Loading customer prices..."):
            prices_data = load_prices_data()
        
        if prices_data.empty:
            st.warning("Customer prices data not found")
        else:
            st.success(f"Loaded {len(prices_data)} price records")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Records", len(prices_data))
            col2.metric("Unique Customers", prices_data['Customer'].nunique())
            col3.metric("Unique Items", prices_data['Item Code'].nunique())
            col4.metric("Avg Price", f"${prices_data['Price'].mean():.2f}")
            
            # Filters
            col1, col2 = st.columns(2)
            with col1:
                customers = ["All"] + sorted(prices_data['Customer'].dropna().unique().tolist())
                selected_customer = st.selectbox("Filter by Customer:", customers, key="hub_customer")
            with col2:
                search_price = st.text_input("Search by Item Code or Name:", placeholder="Enter article or product name...", key="hub_search")
            
            filtered_data = prices_data.copy()
            if selected_customer != "All":
                filtered_data = filtered_data[filtered_data['Customer'] == selected_customer]
            if search_price:
                mask = filtered_data['Item Code'].astype(str).str.contains(search_price, case=False, na=False)
                mask = mask | filtered_data['Item Name'].astype(str).str.contains(search_price, case=False, na=False)
                filtered_data = filtered_data[mask]
            
            st.markdown(f"**Found {len(filtered_data)} records**")
            
            if not filtered_data.empty:
                for _, record in filtered_data.head(50).iterrows():
                    with st.expander(f"💰 {record['Item Code']} - {record['Item Name']}", expanded=False):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Customer:** {record['Customer']}")
                            st.markdown(f"**Customer Name:** {record['Customer Name']}")
                            st.markdown(f"**Salesman:** {record['Salesman']}")
                        with col2:
                            st.markdown(f"**Item Code:** {record['Item Code']}")
                            st.markdown(f"**Customer Article:** {record['Customer Article No']}")
                            st.markdown(f"**Packing:** {record['Packing/kg']} kg")
                            st.markdown(f"**Price:** <span style='font-size: 1.25rem; font-weight: 700; color: #059669;'>${record['Price']:.2f}</span>", unsafe_allow_html=True)
                
                if len(filtered_data) > 50:
                    st.info(f"Showing 50 of {len(filtered_data)} records. Use filters to narrow down.")
    
    # SUB-TAB 2: General Price List
    with sub_tab2:
        st.markdown("<div class='subsection-header'>📊 General Price List (All Items)</div>", unsafe_allow_html=True)
        
        with st.spinner("Loading general prices..."):
            general_data = load_general_prices_data()
        
        if general_data.empty:
            st.warning("General prices data not found")
        else:
            st.success(f"Loaded {len(general_data)} items")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Items", len(general_data))
            if 'CATEG.' in general_data.columns:
                col2.metric("Categories", general_data['CATEG.'].nunique())
            if 'NEW EXW' in general_data.columns:
                col3.metric("Avg Price", f"${general_data['NEW EXW'].mean():.2f}")
                col4.metric("Price Range", f"${general_data['NEW EXW'].min():.2f} - ${general_data['NEW EXW'].max():.2f}")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                search_general = st.text_input("Search by Article or Description:", placeholder="Enter article number or description...", key="general_search")
            with col2:
                if 'CATEG.' in general_data.columns:
                    categories = ["All"] + sorted(general_data['CATEG.'].dropna().unique().tolist())
                    category_filter = st.selectbox("Category:", categories, key="general_category")
                else:
                    category_filter = "All"
            
            filtered_general = general_data.copy()
            if search_general:
                mask = filtered_general.astype(str).apply(lambda x: x.str.contains(search_general, case=False, na=False)).any(axis=1)
                filtered_general = filtered_general[mask]
            if category_filter != "All" and 'CATEG.' in general_data.columns:
                filtered_general = filtered_general[filtered_general['CATEG.'] == category_filter]
            
            st.markdown(f"**Found {len(filtered_general)} items**")
            
            if not filtered_general.empty:
                for _, item in filtered_general.head(30).iterrows():
                    with st.expander(f"📦 {item.get('ART#', 'N/A')} - {item.get('DESCRIPTION', 'N/A')}", expanded=False):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Article:** {item.get('ART#', 'N/A')}")
                            st.markdown(f"**Description:** {item.get('DESCRIPTION', 'N/A')}")
                            st.markdown(f"**Category:** {item.get('CATEG.', 'N/A')}")
                        with col2:
                            if 'NEW EXW' in item and pd.notna(item.get('NEW EXW')):
                                st.markdown(f"**Price:** <span style='font-size: 1.25rem; font-weight: 700; color: #059669;'>${item['NEW EXW']:.2f}</span>", unsafe_allow_html=True)
                            st.markdown(f"**Unit Weight:** {item.get('UNT WGT', 'N/A')} kg")
                            st.markdown(f"**UOM:** {item.get('UOM', 'N/A')}")
    
    # SUB-TAB 3: Price Intelligence
    with sub_tab3:
        st.markdown("<div class='subsection-header'>🔍 Cross-Client Price Intelligence</div>", unsafe_allow_html=True)
        
        available_clients = st.session_state.user_clients
        
        if len(available_clients) < 2:
            st.warning(f"You need access to at least 2 clients to compare prices. Current access: {', '.join(available_clients)}")
        else:
            col1, col2 = st.columns([2, 1])
            with col1:
                selected_clients = st.multiselect("Select clients to compare:", options=available_clients, default=available_clients[:2], key="intel_clients")
            with col2:
                search_intel = st.text_input("Article or product name:", placeholder="e.g., 1-366, Chocolate...", key="intel_search")
            
            if st.button("Analyze Prices Across Clients", use_container_width=True, type="primary", key="intel_analyze"):
                if search_intel and selected_clients:
                    st.markdown(f"<div class='subsection-header'>Analysis Results: '{search_intel}'</div>", unsafe_allow_html=True)
                    
                    all_results = []
                    for client in selected_clients:
                        client_data = get_google_sheets_data(client)
                        
                        for supplier in ["Backaldrin", "Bateel"]:
                            supplier_data = client_data.get(supplier, {})
                            
                            for article_num, article_data in supplier_data.items():
                                article_match = search_intel.lower() in article_num.lower()
                                product_match = any(search_intel.lower() in name.lower() for name in article_data.get('names', []))
                                
                                if article_match or product_match:
                                    prices = article_data.get('prices', [])
                                    all_results.append({
                                        'Client': client,
                                        'Supplier': supplier,
                                        'Article': article_num,
                                        'Product': article_data.get('names', ['N/A'])[0],
                                        'Min Price': f"${min(prices):.2f}" if prices else 'N/A',
                                        'Max Price': f"${max(prices):.2f}" if prices else 'N/A',
                                        'Records': len(prices)
                                    })
                    
                    if all_results:
                        results_df = pd.DataFrame(all_results)
                        st.dataframe(results_df, use_container_width=True, hide_index=True)
                        
                        # Summary stats
                        st.markdown("---")
                        st.markdown("**Summary Statistics**")
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Total Matches", len(all_results))
                        
                        valid_prices = [float(r['Min Price'].replace('$', '')) for r in all_results if r['Min Price'] != 'N/A']
                        if valid_prices:
                            col2.metric("Lowest Price", f"${min(valid_prices):.2f}")
                            col3.metric("Highest Price", f"${max(valid_prices):.2f}")
                    else:
                        st.warning(f"No results found for '{search_intel}'")
                else:
                    if not search_intel:
                        st.error("Please enter an article number or product name")
                    if not selected_clients:
                        st.error("Please select at least one client")

# ============================================
# TAB 3: SPECIAL PRICES (CEO Special Prices)
# ============================================

def special_prices_tab():
    """CEO Special Prices Tab"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #d97706, #b45309); padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem;">
        <h2 style="margin:0; color: white;">⭐ CEO Special Prices</h2>
        <p style="margin:0; opacity:0.9; color: white;">Exclusive pricing • Limited time offers • VIP client rates</p>
    </div>
    """, unsafe_allow_html=True)
    
    available_clients = st.session_state.user_clients
    client = st.selectbox("Select Client:", available_clients, key="special_client")
    
    if not client:
        st.warning("No clients available")
        return
    
    with st.spinner(f"Loading special prices for {client}..."):
        special_data = load_ceo_special_prices(client)
    
    if special_data.empty:
        st.warning(f"No CEO special prices found for {client}")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Special Offers", len(special_data))
    if 'Expiry_Date' in special_data.columns:
        active_count = len(special_data[special_data['Expiry_Date'] >= datetime.now().strftime('%Y-%m-%d')])
        col2.metric("Active Offers", active_count)
    col3.metric("Currencies", special_data['Currency'].nunique())
    
    col1, col2 = st.columns([2, 1])
    with col1:
        search_special = st.text_input("Search by article or product name...", key="special_search")
    with col2:
        show_active = st.checkbox("Show Active Only", value=True, key="special_active")
    
    filtered_special = special_data.copy()
    if search_special:
        mask = filtered_special.astype(str).apply(lambda x: x.str.contains(search_special, case=False, na=False)).any(axis=1)
        filtered_special = filtered_special[mask]
    if show_active and 'Expiry_Date' in filtered_special.columns:
        filtered_special = filtered_special[filtered_special['Expiry_Date'] >= datetime.now().strftime('%Y-%m-%d')]
    
    st.markdown(f"**Found {len(filtered_special)} special offers**")
    
    if not filtered_special.empty:
        for _, special in filtered_special.iterrows():
            is_active = special['Expiry_Date'] >= datetime.now().strftime('%Y-%m-%d') if 'Expiry_Date' in special else True
            status = "🟢 Active" if is_active else "🔴 Expired"
            
            try:
                price_display = f"{float(special['Special_Price']):.2f}"
            except:
                price_display = str(special['Special_Price'])
            
            st.markdown(f"""
            <div class="price-card-secondary">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{special['Article_Number']} - {special['Product_Name']}</strong>
                        <div style="font-size: 1.1rem; font-weight: 700; color: #b45309;">💰 {price_display} {special['Currency']}/kg</div>
                        <div style="font-size: 0.8rem; color: #64748b;">{status} • {special.get('Incoterm', 'N/A')}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# TAB 4: PRODUCTS & LOGISTICS (Merged: PRODUCT CATALOG + PALLETIZING)
# ============================================

def products_logistics_tab():
    """Consolidated Products & Logistics - Product catalog and pallet calculator"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0ea5e9, #0284c7); padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem;">
        <h2 style="margin:0; color: white;">📦 Products & Logistics</h2>
        <p style="margin:0; opacity:0.9; color: white;">Complete product catalog • Pallet calculator • Logistics planning</p>
    </div>
    """, unsafe_allow_html=True)
    
    sub_tab1, sub_tab2 = st.tabs(["📋 Product Catalog", "📦 Pallet Calculator"])
    
    # SUB-TAB 1: Product Catalog
    with sub_tab1:
        st.markdown("<div class='subsection-header'>📋 Complete Product Catalog</div>", unsafe_allow_html=True)
        
        with st.spinner("Loading product catalog..."):
            catalog_data = load_product_catalog()
        
        if catalog_data.empty:
            st.warning("Product catalog not found")
        else:
            st.success(f"Loaded {len(catalog_data)} products")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Products", len(catalog_data))
            if 'Supplier' in catalog_data.columns:
                col2.metric("Suppliers", catalog_data['Supplier'].nunique())
            if 'Category' in catalog_data.columns:
                col3.metric("Categories", catalog_data['Category'].nunique())
            col4.metric("Unique Articles", catalog_data['Article_Number'].nunique())
            
            col1, col2 = st.columns([2, 1])
            with col1:
                search_catalog = st.text_input("Search by article or product name...", key="catalog_search_input")
            with col2:
                if 'Supplier' in catalog_data.columns:
                    supplier_filter = st.selectbox("Supplier:", ["All"] + list(catalog_data['Supplier'].unique()), key="catalog_supplier_filter")
                else:
                    supplier_filter = "All"
            
            filtered_catalog = catalog_data.copy()
            if search_catalog:
                mask = filtered_catalog.astype(str).apply(lambda x: x.str.contains(search_catalog, case=False, na=False)).any(axis=1)
                filtered_catalog = filtered_catalog[mask]
            if supplier_filter != "All" and 'Supplier' in catalog_data.columns:
                filtered_catalog = filtered_catalog[filtered_catalog['Supplier'] == supplier_filter]
            
            st.markdown(f"**Found {len(filtered_catalog)} products**")
            
            if not filtered_catalog.empty:
                for _, product in filtered_catalog.head(30).iterrows():
                    card_class = "price-card-primary" if product.get('Supplier') == 'Backaldrin' else "price-card-secondary"
                    with st.expander(f"📦 {product['Article_Number']} - {product['Product_Name']}", expanded=False):
                        st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Article:** {product['Article_Number']}")
                            st.markdown(f"**Product:** {product['Product_Name']}")
                            if 'Supplier' in product:
                                st.markdown(f"**Supplier:** {product['Supplier']}")
                        with col2:
                            if 'Category' in product and product['Category']:
                                st.markdown(f"**Category:** {product['Category']}")
                            if 'UOM' in product and product['UOM']:
                                st.markdown(f"**UOM:** {product['UOM']}")
                        if 'Common_Description' in product and product['Common_Description']:
                            st.markdown(f"**Description:** {product['Common_Description']}")
                        st.markdown('</div>', unsafe_allow_html=True)
                
                if len(filtered_catalog) > 30:
                    st.info(f"Showing 30 of {len(filtered_catalog)} products. Use filters to narrow down.")
    
    # SUB-TAB 2: Pallet Calculator
    with sub_tab2:
        st.markdown("<div class='subsection-header'>📦 Quick Pallet Calculator</div>", unsafe_allow_html=True)
        
        # Standard items for quick calculation
        standard_items = {
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
            selected_item = st.selectbox("Select Item:", list(standard_items.keys()), key="pallet_item")
            quantity = st.number_input("Quantity:", min_value=1, value=100, step=1, key="pallet_qty")
            uom = st.selectbox("Unit of Measure:", ["Cartons", "KGs", "Pallets"], key="pallet_uom")
        
        with col2:
            if selected_item == "Custom Item":
                st.info("Enter custom item details:")
                packing = st.text_input("Packing:", value="5kg", key="custom_packing")
                cartons_per_pallet = st.number_input("Cartons per Pallet:", min_value=1, value=100, step=1, key="custom_cartons")
                weight_per_carton = st.number_input("Weight per Carton (kg):", min_value=0.1, value=5.0, step=0.1, key="custom_weight")
            else:
                item_data = standard_items[selected_item]
                packing = item_data["packing"]
                cartons_per_pallet = item_data["cartons_per_pallet"]
                weight_per_carton = item_data["weight_per_carton"]
                st.info(f"**Standard Packing:** {packing}")
                st.info(f"**Cartons per Pallet:** {cartons_per_pallet}")
                st.info(f"**Weight per Carton:** {weight_per_carton} kg")
        
        if quantity > 0 and cartons_per_pallet > 0:
            if uom == "Cartons":
                total_cartons = quantity
            elif uom == "KGs":
                total_cartons = quantity / weight_per_carton
            else:
                total_cartons = quantity * cartons_per_pallet
            
            full_pallets = int(total_cartons // cartons_per_pallet)
            partial_cartons = total_cartons % cartons_per_pallet
            total_weight = total_cartons * weight_per_carton
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{full_pallets:,.0f}</div>
                    <div class="stat-label">Full Pallets</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{partial_cartons:,.0f}</div>
                    <div class="stat-label">Partial Cartons</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{total_weight:,.0f} kg</div>
                    <div class="stat-label">Total Weight</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.info(f"**Container Info:** A 40ft container holds approximately 30 pallets max. Your order fills {(full_pallets / 30 * 100):.1f}% of container capacity.")

# ============================================
# TAB 5: ORDER TRACKING (Merged: ETD SHEET + SAMPLES REQUEST)
# ============================================

def order_tracking_tab():
    """Consolidated Order Tracking - ETD management and sample requests"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #059669, #047857); padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem;">
        <h2 style="margin:0; color: white;">📅 Order Tracking</h2>
        <p style="margin:0; opacity:0.9; color: white;">ETD management • Order status • Sample requests</p>
    </div>
    """, unsafe_allow_html=True)
    
    sub_tab1, sub_tab2 = st.tabs(["🚢 ETD Management", "🎁 Samples Request"])
    
    # SUB-TAB 1: ETD Management
    with sub_tab1:
        st.markdown("<div class='subsection-header'>🚢 ETD Dashboard</div>", unsafe_allow_html=True)
        
        ETD_SHEET_ID = "1eA-mtD3aK_n9VYNV_bxnmqm58IywF0f5-7vr3PT51hs"
        AVAILABLE_MONTHS = ["October 2025", "November 2025"]
        
        selected_month = st.selectbox("Select Month:", AVAILABLE_MONTHS, key="etd_month")
        
        with st.spinner(f"Loading {selected_month} ETD data..."):
            etd_data = load_etd_data(ETD_SHEET_ID, selected_month)
        
        if etd_data.empty:
            st.warning(f"No ETD data found for {selected_month}")
        else:
            st.success(f"Loaded {len(etd_data)} orders for {selected_month}")
            
            # Stats
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Orders", len(etd_data))
            if 'Status' in etd_data.columns:
                shipped = len(etd_data[etd_data['Status'].str.lower() == 'shipped'])
                col2.metric("Shipped", shipped)
                production = len(etd_data[etd_data['Status'].str.lower().str.contains('production', na=False)])
                col3.metric("In Production", production)
            
            # Filters
            col1, col2 = st.columns(2)
            with col1:
                if 'Client Name' in etd_data.columns:
                    clients = ["All"] + sorted(etd_data['Client Name'].dropna().unique())
                    client_filter = st.selectbox("Filter by Client:", clients, key="etd_client")
                else:
                    client_filter = "All"
            with col2:
                status_filter = st.selectbox("Filter by Status:", ["All", "Shipped", "In Production", "Pending", "Need ETD"], key="etd_status")
            
            filtered_etd = etd_data.copy()
            if client_filter != "All" and 'Client Name' in etd_data.columns:
                filtered_etd = filtered_etd[filtered_etd['Client Name'] == client_filter]
            if status_filter != "All" and status_filter != "Need ETD" and 'Status' in etd_data.columns:
                filtered_etd = filtered_etd[filtered_etd['Status'] == status_filter]
            
            st.markdown(f"**Found {len(filtered_etd)} orders**")
            
            if not filtered_etd.empty:
                for _, order in filtered_etd.iterrows():
                    status = order.get('Status', 'Unknown')
                    status_icon = {'Shipped': '🟢', 'In Production': '🟡', 'Pending': '🟠'}.get(status, '⚫')
                    
                    with st.expander(f"{status_icon} Order {order.get('Order No.', 'N/A')} - {order.get('Client Name', 'N/A')}", expanded=False):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown(f"**Client:** {order.get('Client Name', 'N/A')}")
                            st.markdown(f"**Employee:** {order.get('Concerned Employee', 'N/A')}")
                        with col2:
                            st.markdown(f"**Status:** {status}")
                            st.markdown(f"**Confirmation:** {order.get('Confirmation Date', 'N/A')}")
                        with col3:
                            st.markdown(f"**Loading:** {order.get('Scheduled Date For Loading', 'N/A')}")
                        
                        st.markdown("---")
                        st.markdown("**Supplier ETD Status**")
                        
                        for supplier in ['Backaldrine', 'bateel']:
                            etd_col = f"ETD _{supplier}" if supplier != 'bateel' else 'ETD_bateel'
                            etd_value = order.get(etd_col, '')
                            
                            if pd.isna(etd_value) or str(etd_value).strip() == '':
                                st.markdown(f"**{supplier}:** ❌ No ETD")
                            elif 'NEED ETD' in str(etd_value).upper():
                                st.markdown(f"**{supplier}:** <span class='badge-danger'>NEED ETD</span>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"**{supplier}:** 📅 {etd_value}")
    
    # SUB-TAB 2: Samples Request
    with sub_tab2:
        st.markdown("<div class='subsection-header'>🎁 Samples Request Form</div>", unsafe_allow_html=True)
        
        # Initialize session state for samples
        if 'sample_items' not in st.session_state:
            st.session_state.sample_items = []
        
        catalog_data = load_product_catalog()
        article_to_product = {}
        
        if not catalog_data.empty and 'Article_Number' in catalog_data.columns and 'Product_Name' in catalog_data.columns:
            for _, row in catalog_data.iterrows():
                article = str(row['Article_Number']).strip()
                product = str(row['Product_Name']).strip()
                if article and article != 'nan' and product and product != 'nan':
                    article_to_product[article] = product
        
        # Request form
        col1, col2 = st.columns(2)
        
        with col1:
            request_date = st.date_input("Request Date", value=datetime.now().date(), key="sample_date")
            requested_by = st.text_input("Requested By *", placeholder="Enter your full name", key="sample_by")
            department = st.selectbox("Department", ["Sales", "Marketing", "R&D", "Production", "Quality Control", "Other"], key="sample_dept")
        
        with col2:
            going_to = st.text_input("Recipient Name *", placeholder="Enter recipient name", key="sample_recipient")
            address = st.text_area("Address *", placeholder="Enter complete delivery address", height=80, key="sample_address")
            delivery_method = st.selectbox("Delivery Method", ["Courier", "Pickup", "Mail", "Express Delivery", "Freight"], key="sample_delivery")
        
        st.markdown("---")
        st.markdown("**Add Sample Items:**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            article_input = st.text_input("Article Number", placeholder="e.g., 1-366", key="sample_article")
            default_product = article_to_product.get(article_input, "")
            product_input = st.text_input("Product Name", value=default_product, key="sample_product")
        with col2:
            quantity = st.number_input("Quantity", min_value=1, value=1, step=1, key="sample_qty")
            unit_weight = st.number_input("Unit Weight (kg)", min_value=0.0, step=0.1, format="%.2f", key="sample_weight", value=0.0)
        with col3:
            logo_required = st.radio("Logo Required?", ["No", "Yes"], horizontal=True, key="sample_logo")
            notes = st.text_input("Notes (Optional)", key="sample_notes")
        
        if st.button("➕ Add Item", use_container_width=True, key="add_sample"):
            if article_input and product_input:
                st.session_state.sample_items.append({
                    'article': article_input,
                    'product': product_input,
                    'quantity': quantity,
                    'unit_weight': unit_weight,
                    'logo': logo_required,
                    'notes': notes
                })
                st.rerun()
            else:
                st.error("Please enter both Article Number and Product Name")
        
        # Display current items
        if st.session_state.sample_items:
            st.markdown(f"**Sample Items ({len(st.session_state.sample_items)}):**")
            for idx, item in enumerate(st.session_state.sample_items):
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    st.write(f"{item['article']} - {item['product']}")
                with col2:
                    st.write(f"Qty: {item['quantity']}")
                with col3:
                    st.write(f"Weight: {item['unit_weight']} kg")
                with col4:
                    if st.button("🗑️", key=f"remove_{idx}"):
                        st.session_state.sample_items.pop(idx)
                        st.rerun()
            
            if st.button("🗑️ Clear All Items", use_container_width=True):
                st.session_state.sample_items = []
                st.rerun()
        
        # Submit button
        if st.button("📤 SUBMIT SAMPLES REQUEST", use_container_width=True, type="primary", key="submit_samples"):
            if not requested_by:
                st.error("Please enter Requested By")
            elif not going_to:
                st.error("Please enter Recipient Name")
            elif not address:
                st.error("Please enter Address")
            elif not st.session_state.sample_items:
                st.error("Please add at least one sample item")
            else:
                st.balloons()
                st.success(f"✅ Samples request submitted successfully! Request ID: SAMP-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
                
                # Display summary
                st.markdown("### Request Summary")
                st.markdown(f"**Requested By:** {requested_by}")
                st.markdown(f"**Recipient:** {going_to}")
                st.markdown(f"**Address:** {address}")
                st.markdown(f"**Total Items:** {len(st.session_state.sample_items)}")
                
                # Option to reset
                if st.button("📋 New Request", key="new_sample"):
                    st.session_state.sample_items = []
                    st.rerun()

# ============================================
# MAIN DASHBOARD
# ============================================

def main_dashboard():
    """Main dashboard with 5 consolidated tabs"""
    
    # Header
    st.markdown(f"""
    <div class="dashboard-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div class="dashboard-title">
                    <span>📊</span> Multi-Client Command Center
                </div>
                <div class="dashboard-subtitle">
                    Consolidated Dashboard • Real-time pricing intelligence • Order tracking
                </div>
            </div>
            <div>
                <span class="badge-info">👤 {st.session_state.username}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Navigation - 5 consolidated tabs
    with st.sidebar:
        st.markdown("### 📋 Navigation")
        
        tabs = [
            "📋 CLIENT ORDERS",
            "💰 PRICING HUB", 
            "⭐ SPECIAL PRICES",
            "📦 PRODUCTS & LOGISTICS",
            "📅 ORDER TRACKING"
        ]
        
        for tab in tabs:
            is_active = st.session_state.get('active_tab', '📋 CLIENT ORDERS') == tab
            button_label = f"▶️ {tab}" if is_active else tab
            
            if st.button(
                button_label,
                key=f"tab_{tab}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.active_tab = tab
                st.rerun()
        
        st.markdown("---")
        
        # Recent Searches
        if st.session_state.get('search_history'):
            st.markdown("### 🔍 Recent Searches")
            for i, history_item in enumerate(st.session_state.search_history[:5]):
                time_ago = format_time_ago(history_item['timestamp'])
                if st.button(f"{history_item['search_term'][:30]}", key=f"hist_{i}", use_container_width=True):
                    st.session_state.active_tab = "📋 CLIENT ORDERS"
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### 📢 Updates")
        announcements = [
            "✅ Dashboard consolidated to 5 tabs!",
            "🚀 Faster navigation and loading",
            "⭐ Save time with smarter organization"
        ]
        for announcement in announcements:
            st.markdown(f'<div class="announcement-item">{announcement}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        logout_button()
    
    # Main Content - Display selected tab
    st.markdown(f"<div class='section-header'>{st.session_state.active_tab}</div>", unsafe_allow_html=True)
    
    if st.session_state.active_tab == "📋 CLIENT ORDERS":
        client_orders_tab()
    elif st.session_state.active_tab == "💰 PRICING HUB":
        pricing_hub_tab()
    elif st.session_state.active_tab == "⭐ SPECIAL PRICES":
        special_prices_tab()
    elif st.session_state.active_tab == "📦 PRODUCTS & LOGISTICS":
        products_logistics_tab()
    elif st.session_state.active_tab == "📅 ORDER TRACKING":
        order_tracking_tab()
    
    # Footer
    st.markdown(f"""
    <div class="dashboard-footer">
        Multi-Client Dashboard v6.0 (Consolidated) | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)

# ============================================
# MAIN EXECUTION
# ============================================
if __name__ == "__main__":
    if not check_login():
        login_page()
    else:
        main_dashboard()
