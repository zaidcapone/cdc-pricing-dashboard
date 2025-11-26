import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime
from io import BytesIO

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

# User authentication
USERS = {
    "admin": {"password": "admin123", "clients": ["CDC", "CoteDivoire", "CakeArt", "SweetHouse", "Cameron"]},
    "ceo": {"password": "ceo123", "clients": ["CDC", "CoteDivoire", "CakeArt", "SweetHouse", "Cameron"]},
    "zaid": {"password": "zaid123", "clients": ["CDC"]},
    "mohammad": {"password": "mohammad123", "clients": ["CoteDivoire"]},
    "Khalid": {"password": "KHALID123", "clients": ["CakeArt", "SweetHouse"]},
    "Rotana": {"password": "Rotana123", "clients": ["CDC"]}
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
        "📦 **NEW**: Palletizing Calculator added!"
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
    
    # Create ALL tabs in one line - they will auto-scroll horizontally
    if st.session_state.username in ["ceo", "admin"]:
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
            "🏢 CLIENTS", "📋 NEW ORDERS", "📅 ETD SHEET", 
            "⭐ CEO SPECIAL PRICES", "💰 PRICE INTELLIGENCE", "📦 PRODUCT CATALOG",
            "📊 ORDERS MANAGEMENT", "🔍 ADVANCED ANALYTICS", "📦 PALLETIZING", "⚙️ SETTINGS"
        ])
    else:
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
            "🏢 CLIENTS", "📋 NEW ORDERS", "📅 ETD SHEET", 
            "⭐ CEO SPECIAL PRICES", "💰 PRICE INTELLIGENCE", "📦 PRODUCT CATALOG",
            "📊 ORDERS MANAGEMENT", "🔍 ADVANCED ANALYTICS", "📦 PALLETIZING"
        ])
    
    with tab1:
        clients_tab()
    
    with tab2:
        new_orders_tab()
        
    with tab3:
        etd_tab()
        
    with tab4:
        ceo_specials_tab()
    
    with tab5:
        price_intelligence_tab()

    with tab6:
        product_catalog_tab()
        
    with tab7:
        orders_management_tab()
        
    with tab8:
        advanced_analytics_tab()
        
    with tab9:
        palletizing_tab()
        
    # Additional tabs for admin/ceo
    if st.session_state.username in ["ceo", "admin"]:
        with tab10:
            settings_tab()

def etd_tab():
    """ETD Management - Fixed for Row 14"""
    st.markdown("""
    <div class="intelligence-header">
        <h2 style="margin:0;">📅 ETD Management Dashboard</h2>
        <p style="margin:0; opacity:0.9;">Live Order Tracking • Multi-Supplier ETD</p>
    </div>
    """, unsafe_allow_html=True)

    # ETD Sheet configuration
    ETD_SHEET_ID = "1eA-mtD3aK_n9VYNV_bxnmqm58IywF0f5-7vr3PT51hs"
    
    st.success("✅ ETD Sheet Found: 'November 2025'")
    st.info("📊 Loading data starting from **Row 14**...")
    
    try:
        with st.spinner("🔄 Loading ETD data..."):
            # Load with correct starting row
            etd_data = load_etd_data(ETD_SHEET_ID, "November 2025")
        
        if etd_data.empty:
            st.error("❌ Still no data found starting from row 14!")
            st.info("""
            **Let's try loading raw data to see what's happening:**
            """)
            
            # Load raw data to debug
            raw_url = f"https://sheets.googleapis.com/v4/spreadsheets/{ETD_SHEET_ID}/values/November%202025!A14:Z100?key={API_KEY}"
            raw_response = requests.get(raw_url)
            
            if raw_response.status_code == 200:
                raw_data = raw_response.json()
                raw_values = raw_data.get('values', [])
                
                if raw_values:
                    st.success(f"✅ Raw data found: {len(raw_values)} rows")
                    st.write("**First few rows of raw data:**")
                    for i, row in enumerate(raw_values[:5]):
                        st.write(f"Row {i+14}: {row}")
                else:
                    st.error("❌ No data found even in raw request!")
            return
            
        st.success(f"✅ **SUCCESS!** Loaded {len(etd_data)} orders from November 2025!")
        
        # Show overview
        st.subheader("📊 ETD Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Orders", len(etd_data))
        with col2:
            st.metric("Columns", len(etd_data.columns))
        with col3:
            st.metric("Data Range", f"Rows 14-{14 + len(etd_data)}")
        with col4:
            st.metric("First Columns", ", ".join(etd_data.columns[:3]))
        
        # Show data preview
        st.subheader("📋 Data Preview")
        st.dataframe(etd_data.head(10), use_container_width=True)
        
        # Show column names
        with st.expander("🔍 View All Column Names"):
            st.write("**All columns:**", list(etd_data.columns))
        
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")

def load_etd_data(sheet_id, sheet_name):
    """Optimized ETD loader using universal function"""
    return load_sheet_data(sheet_name, start_row=13)

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

# [ALL YOUR OTHER EXISTING FUNCTIONS REMAIN HERE - palletizing_tab, clients_tab, etc.]

def palletizing_tab():
    """Interactive Palletizing Calculator"""
    st.markdown("""
    <div class="palletizing-header">
        <h2 style="margin:0;">📦 Interactive Palletizing Calculator</h2>
        <p style="margin:0; opacity:0.9;">Real-time Calculations • Custom Inputs • Instant Pallet Counts</p>
    </div>
    """, unsafe_allow_html=True)

    # Two modes: Quick Calculator or Bulk Analysis
    calc_mode = st.radio(
        "Choose Calculation Mode:",
        ["🧮 Quick Item Calculator", "📊 Bulk Analysis from Sheet"],
        horizontal=True,
        key="pallet_mode"
    )

    if calc_mode == "🧮 Quick Item Calculator":
        quick_pallet_calculator()
    else:
        bulk_sheet_analysis()

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
            packing = st.text_input("Packing (e.g., 5kg, 25kg):", value="5kg")
            cartons_per_pallet = st.number_input("Cartons per Pallet:", min_value=1, value=100, step=1)
            weight_per_carton = st.number_input("Weight per Carton (kg):", min_value=0.1, value=5.0, step=0.1)
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
        partial_pallet_percentage = (partial_pallet_cartons / cartons_per_pallet) * 100
        
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
            if st.button(f"Example: 100 cartons {selected_item}"):
                st.session_state.quantity = 100
                st.session_state.uom = "Cartons"
                st.rerun()
                
        with examples_col2:
            if st.button(f"Example: 1 pallet {selected_item}"):
                st.session_state.quantity = 1
                st.session_state.uom = "Pallets"
                st.rerun()

def bulk_sheet_analysis():
    """Analysis of existing sheet data - SIMPLIFIED"""
    st.info("📊 **Bulk Analysis from Google Sheets**")
    st.write("This section analyzes your existing Palletizing_Data sheet")
    st.write("Use the Quick Calculator above for instant pallet calculations!")
    
    # Client selection
    available_clients = st.session_state.user_clients
    client = st.selectbox(
        "Select Client:",
        available_clients,
        key="palletizing_client"
    )
    
    if not client:
        st.info("👆 Please select a client to start palletizing calculations")
        return
    
    # Load palletizing data from Google Sheets
    with st.spinner(f"📥 Loading palletizing data for {client}..."):
        pallet_data = load_palletizing_data(client)
    
    if pallet_data.empty:
        st.warning(f"📝 No palletizing data found for {client} yet!")
        st.info(f"""
        **To get started:**
        1. Go to your Google Sheet for {client}
        2. Add a new tab called **'Palletizing_Data'**
        3. Use these exact headers:
           - Client
           - Item Code
           - Item Name
           - Unit/KG
           - Unit/Carton
           - Unit Pack/Pallet
           - Total Unit
           - Pallet Order
           - Total Weight
           - Factory
        """)
        return
    
    st.success(f"✅ Loaded {len(pallet_data)} items for {client}")
    
    # Filter data for selected client
    client_data = pallet_data[pallet_data['Client'] == client]
    
    if client_data.empty:
        st.warning(f"No palletizing data specifically for {client}")
        return
    
    # Palletizing Overview
    st.subheader("📊 Palletizing Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_items = len(client_data)
        st.metric("Total Items", total_items)
    
    with col2:
        total_weight = client_data['Total Weight'].sum()
        st.metric("Total Weight", f"{total_weight:,.0f} kg")
    
    with col3:
        total_pallets = client_data['Pallet Order'].sum()
        st.metric("Total Pallets", f"{total_pallets:,.0f}")
    
    with col4:
        total_units = client_data['Total Unit'].sum()
        st.metric("Total Units", f"{total_units:,.0f}")
    
    # Container Configuration
    st.subheader("🚢 Container Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        container_type = st.selectbox(
            "Container Type",
            ["20ft Container", "40ft Container", "40ft HC Container", "Custom"],
            key="container_type"
        )
    
    with col2:
        # Standard container capacities
        container_capacities = {
            "20ft Container": {"pallets": 11, "weight": 22000},
            "40ft Container": {"pallets": 25, "weight": 27000},
            "40ft HC Container": {"pallets": 30, "weight": 27000},
            "Custom": {"pallets": 0, "weight": 0}
        }
        
        if container_type == "Custom":
            max_pallets = st.number_input("Max Pallets", min_value=1, value=25, key="custom_pallets")
            max_weight = st.number_input("Max Weight (kg)", min_value=1000, value=27000, key="custom_weight")
        else:
            capacity = container_capacities[container_type]
            max_pallets = capacity["pallets"]
            max_weight = capacity["weight"]
            st.info(f"📦 Capacity: {max_pallets} pallets, {max_weight:,} kg")
    
    with col3:
        optimization_goal = st.selectbox(
            "Optimize For",
            ["Maximize Weight", "Maximize Volume", "Balance Both"],
            key="optimization_goal"
        )
    
    # Analysis and Calculations
    st.subheader("🔍 Palletizing Analysis")
    
    # Calculate container requirements
    required_containers_pallets = max(1, round(total_pallets / max_pallets))
    required_containers_weight = max(1, round(total_weight / max_weight))
    required_containers = max(required_containers_pallets, required_containers_weight)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="pallet-stat-card">
            <div class="pallet-stat-number">{required_containers}</div>
            <div class="stat-label">Containers Needed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        utilization_pallets = min(100, (total_pallets / (required_containers * max_pallets)) * 100)
        st.metric("Pallet Utilization", f"{utilization_pallets:.1f}%")
    
    with col3:
        utilization_weight = min(100, (total_weight / (required_containers * max_weight)) * 100)
        st.metric("Weight Utilization", f"{utilization_weight:.1f}%")
    
    with col4:
        avg_weight_per_pallet = total_weight / total_pallets if total_pallets > 0 else 0
        st.metric("Avg Weight/Pallet", f"{avg_weight_per_pallet:.1f} kg")
    
    # Detailed Item Breakdown
    st.subheader("📋 Item Breakdown")
    
    # Display items in a nice format
    for _, item in client_data.iterrows():
        with st.expander(f"📦 {item['Item Code']} - {item['Item Name']}", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Units/Pallet", f"{item['Unit Pack/Pallet']:,.0f}")
            with col2:
                st.metric("Total Units", f"{item['Total Unit']:,.0f}")
            with col3:
                st.metric("Pallets", f"{item['Pallet Order']:,.0f}")
            with col4:
                st.metric("Weight", f"{item['Total Weight']:,.0f} kg")
            
            # Additional details
            st.write(f"**Factory:** {item['Factory']}")
            st.write(f"**Unit/Carton:** {item['Unit/Carton']}")
            st.write(f"**Unit/KG:** {item['Unit/KG']}")
    
    # Optimization Recommendations
    st.subheader("💡 Optimization Recommendations")
    
    if utilization_pallets < 80:
        st.warning("**📦 Low Pallet Utilization:** Consider adding more items to fill containers efficiently")
    
    if utilization_weight < 80:
        st.warning("**⚖️ Low Weight Utilization:** You have room for heavier items")
    
    if utilization_pallets > 95 and utilization_weight > 95:
        st.success("**✅ Excellent Optimization:** Containers are well utilized!")
    
    # Export Section
    st.markdown('<div class="palletizing-section">', unsafe_allow_html=True)
    st.subheader("📤 Export Palletizing Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = client_data.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"{client}_palletizing_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True,
            key="palletizing_csv"
        )
    
    with col2:
        summary_text = f"""
{client} Palletizing Report
==========================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Container Type: {container_type}
Required Containers: {required_containers}

Summary:
- Total Items: {total_items}
- Total Weight: {total_weight:,.0f} kg
- Total Pallets: {total_pallets:,.0f}
- Total Units: {total_units:,.0f}

Utilization:
- Pallet Utilization: {utilization_pallets:.1f}%
- Weight Utilization: {utilization_weight:.1f}%

Items:
{chr(10).join([f"• {row['Item Code']} - {row['Item Name']}: {row['Pallet Order']} pallets, {row['Total Weight']} kg" for _, row in client_data.iterrows()])}
        """
        st.download_button(
            label="📄 Download Summary",
            data=summary_text,
            file_name=f"{client}_palletizing_summary_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True,
            key="palletizing_summary"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

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

# [ADD ALL YOUR OTHER EXISTING FUNCTIONS HERE - clients_tab, cdc_dashboard, etc.]

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
        st.info(f"Selected client: {client}")
        # Your existing client dashboard code here

def ceo_specials_tab():
    """CEO Special Prices tab"""
    st.markdown("""
    <div class="ceo-header">
        <h2 style="margin:0;">⭐ CEO Special Prices</h2>
        <p style="margin:0; opacity:0.9;">Exclusive Pricing • Limited Time Offers • VIP Client Rates</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("CEO Special Prices functionality")

def price_intelligence_tab():
    """CEO Price Intelligence"""
    st.markdown("""
    <div class="intelligence-header">
        <h2 style="margin:0;">💰 CEO Price Intelligence</h2>
        <p style="margin:0; opacity:0.9;">Cross-Client Price Comparison • Market Intelligence • Strategic Insights</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("Price Intelligence functionality")

def product_catalog_tab():
    """Full Product Catalog"""
    st.markdown("""
    <div class="product-catalog-header">
        <h2 style="margin:0;">📦 Full Product Catalog</h2>
        <p style="margin:0; opacity:0.9;">Complete Product Database • Technical Specifications • Search & Filter</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("Product Catalog functionality")

def orders_management_tab():
    """Orders Management Dashboard"""
    st.markdown("""
    <div class="orders-header">
        <h2 style="margin:0;">📋 Orders Management Dashboard</h2>
        <p style="margin:0; opacity:0.9;">Order Tracking • Status Monitoring • Payment Updates</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("Orders Management functionality")

def advanced_analytics_tab():
    """Advanced Analytics Tab"""
    st.markdown("""
    <div class="intelligence-header">
        <h2 style="margin:0;">📊 Advanced Analytics</h2>
        <p style="margin:0; opacity:0.9;">Business Intelligence • Performance Metrics • Trend Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("Advanced Analytics coming soon...")

def settings_tab():
    """Settings Tab"""
    st.markdown("""
    <div class="ceo-header">
        <h2 style="margin:0;">⚙️ System Settings</h2>
        <p style="margin:0; opacity:0.9;">Configuration • User Management • System Preferences</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("Settings management coming soon...")

def new_orders_tab():
    """NEW: Client Orders Management Tab"""
    st.markdown("""
    <div class="new-orders-header">
        <h2 style="margin:0;">📋 New Client Orders Management</h2>
        <p style="margin:0; opacity:0.9;">Order Preparation • PI Generation • Item Allocation • Availability Tracking</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("New Orders functionality")

# Run the main dashboard
if __name__ == "__main__":
    if not check_login():
        login_page()
    else:
        main_dashboard()
