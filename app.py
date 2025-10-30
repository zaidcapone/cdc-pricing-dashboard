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

# Professional Dark Theme CSS based on your Envato template
st.markdown("""
<style>
    /* Root Variables - Dark Theme */
    :root {
        --bs-blue: #0d6efd;
        --bs-dark-blue: #0a58ca;
        --bs-indigo: #6610f2;
        --bs-purple: #6f42c1;
        --bs-pink: #d63384;
        --bs-red: #dc3545;
        --bs-orange: #fd7e14;
        --bs-yellow: #ffc107;
        --bs-green: #198754;
        --bs-teal: #20c997;
        --bs-cyan: #0dcaf0;
        --bs-black: #000;
        --bs-primary: #0d6efd;
        --bs-secondary: #6c757d;
        --bs-success: #02c27a;
        --bs-info: #0dcaf0;
        --bs-warning: #ffc107;
        --bs-danger: #fc185a;
        --bs-light: #f8f9fa;
        --bs-dark: #212529;
        --bs-heading-color: #dee2e6;
        --bs-body-color: #dee2e6;
        --bs-body-bg: #212529;
        --bs-body-bg-2: #181c1f;
        --bs-border-color: #495057;
    }

    /* Main Background */
    .stApp {
        background-color: var(--bs-body-bg);
        color: var(--bs-body-color);
    }

    /* Headers - Professional Gradient */
    .main-header {
        background: linear-gradient(310deg, #7928ca, #ff0080) !important;
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        border: none;
        box-shadow: 0 4px 20px 0 rgba(0,0,0,0.3);
    }

    .cdc-header {
        background: linear-gradient(310deg, #3494e6, #ec6ead) !important;
        color: white;
        padding: 1.8rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: none;
        box-shadow: 0 2px 15px 0 rgba(0,0,0,0.2);
    }

    .ceo-header {
        background: linear-gradient(310deg, #f7971e, #ffd200) !important;
        color: white;
        padding: 1.8rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: none;
        box-shadow: 0 2px 15px 0 rgba(0,0,0,0.2);
    }

    .intelligence-header {
        background: linear-gradient(310deg, #17ad37, #98ec2d) !important;
        color: white;
        padding: 1.8rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: none;
        box-shadow: 0 2px 15px 0 rgba(0,0,0,0.2);
    }

    /* Cards - Modern Dark Design */
    .price-card {
        background: linear-gradient(135deg, #2b3035, #343a40) !important;
        padding: 1.8rem;
        border-radius: 12px;
        border-left: 5px solid var(--bs-danger);
        margin: 0.8rem 0;
        color: var(--bs-body-color);
        font-weight: 500;
        border: 1px solid var(--bs-border-color);
        box-shadow: 0 2px 10px 0 rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }

    .price-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px 0 rgba(0,0,0,0.2);
    }

    .special-price-card {
        background: linear-gradient(135deg, #2b3035, #343a40) !important;
        padding: 1.8rem;
        border-radius: 12px;
        border-left: 5px solid var(--bs-warning);
        margin: 0.8rem 0;
        color: var(--bs-body-color);
        font-weight: 500;
        border: 1px solid var(--bs-border-color);
        box-shadow: 0 2px 10px 0 rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }

    .stat-card {
        background: linear-gradient(135deg, #2b3035, #343a40);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid var(--bs-border-color);
        text-align: center;
        color: var(--bs-body-color);
        box-shadow: 0 4px 15px 0 rgba(0,0,0,0.2);
        transition: transform 0.2s ease;
    }

    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px 0 rgba(0,0,0,0.3);
    }

    .intelligence-stat-card {
        background: linear-gradient(135deg, #2b3035, #343a40);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid var(--bs-success);
        text-align: center;
        color: var(--bs-body-color);
        box-shadow: 0 4px 15px 0 rgba(0,0,0,0.2);
    }

    /* Statistics Numbers */
    .stat-number {
        font-size: 2.5em;
        font-weight: bold;
        color: var(--bs-primary);
        margin: 0;
        background: linear-gradient(310deg, #7928ca, #ff0080);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .intelligence-stat-number {
        font-size: 2.5em;
        font-weight: bold;
        color: var(--bs-success);
        margin: 0;
        background: linear-gradient(310deg, #17ad37, #98ec2d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .stat-label {
        font-size: 0.9em;
        color: var(--bs-secondary);
        margin: 0;
        font-weight: 500;
    }

    /* Price Boxes */
    .price-box {
        background: linear-gradient(310deg, #ee0979, #ff6a00);
        color: white;
        padding: 1.2rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 3px 12px 0 rgba(0,0,0,0.2);
        margin: 0.8rem 0;
        border: none;
        transition: transform 0.2s ease;
    }

    .price-box:hover {
        transform: scale(1.02);
    }

    .intelligence-price-box {
        background: linear-gradient(310deg, #17ad37, #98ec2d);
        color: white;
        padding: 1.2rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 3px 12px 0 rgba(0,0,0,0.2);
        margin: 0.8rem 0;
        border: none;
    }

    .special-price-box {
        background: linear-gradient(310deg, #f7971e, #ffd200);
        color: white;
        padding: 1.2rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 3px 12px 0 rgba(0,0,0,0.2);
        margin: 0.8rem 0;
        border: none;
    }

    /* Order Info */
    .order-info {
        background: rgba(255,255,255,0.1);
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.3rem 0;
        font-size: 0.85em;
        color: rgba(255,255,255,0.9);
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* Sections */
    .export-section {
        background: linear-gradient(135deg, #2b3035, #343a40);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid var(--bs-info);
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px 0 rgba(0,0,0,0.2);
    }

    .ceo-section {
        background: linear-gradient(135deg, #2b3035, #343a40);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid var(--bs-warning);
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px 0 rgba(0,0,0,0.2);
    }

    .intelligence-section {
        background: linear-gradient(135deg, #2b3035, #343a40);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid var(--bs-success);
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px 0 rgba(0,0,0,0.2);
    }

    /* Login Container */
    .login-container {
        max-width: 450px;
        margin: 100px auto;
        padding: 3rem;
        background: linear-gradient(135deg, #2b3035, #343a40);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        border: 1px solid var(--bs-border-color);
    }

    /* Streamlit Components Restyling */
    .stButton>button {
        background: linear-gradient(310deg, #7928ca, #ff0080) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(121, 40, 202, 0.4) !important;
    }

    .stSelectbox>div>div, .stTextInput>div>div>input {
        background: #2b3035 !important;
        border: 1px solid var(--bs-border-color) !important;
        color: var(--bs-body-color) !important;
        border-radius: 8px !important;
    }

    .stRadio>div {
        background: #2b3035;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid var(--bs-border-color);
    }

    .stTabs [data-baseweb="tab-list"] {
        background: #2b3035;
        border-radius: 12px;
        padding: 0.5rem;
        border: 1px solid var(--bs-border-color);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--bs-body-color) !important;
        border-radius: 8px !important;
        margin: 0 0.2rem !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(310deg, #7928ca, #ff0080) !important;
        color: white !important;
    }

    /* Sidebar */
    .css-1d391kg, .css-1lcbmhc {
        background: #181c1f !important;
        border-right: 1px solid var(--bs-border-color) !important;
    }

    /* Success/Error Messages */
    .stAlert {
        border-radius: 10px !important;
        border: 1px solid !important;
    }

    .stSuccess {
        background: rgba(2, 194, 122, 0.1) !important;
        border-color: var(--bs-success) !important;
    }

    .stError {
        background: rgba(252, 24, 90, 0.1) !important;
        border-color: var(--bs-danger) !important;
    }

    .stInfo {
        background: rgba(13, 202, 240, 0.1) !important;
        border-color: var(--bs-info) !important;
    }

    .stWarning {
        background: rgba(255, 193, 7, 0.1) !important;
        border-color: var(--bs-warning) !important;
    }

    /* Metrics */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #2b3035, #343a40) !important;
        border: 1px solid var(--bs-border-color) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        box-shadow: 0 4px 15px 0 rgba(0,0,0,0.2) !important;
    }

    /* Dataframes */
    .dataframe {
        background: #2b3035 !important;
        border: 1px solid var(--bs-border-color) !important;
        border-radius: 10px !important;
    }

    /* Text Colors */
    h1, h2, h3, h4, h5, h6 {
        color: var(--bs-heading-color) !important;
    }

    p, div, span {
        color: var(--bs-body-color) !important;
    }
</style>
""", unsafe_allow_html=True)

# Configuration
API_KEY = "AIzaSyA3P-ZpLjDdVtGB82_1kaWuO7lNbKDj9HU"
CDC_SHEET_ID = "1qWgVT0l76VsxQzYExpLfioBHprd3IvxJzjQWv3RryJI"

# User authentication - UPDATED: cakeart_user changed to Khalid
USERS = {
    "admin": {"password": "admin123", "clients": ["CDC", "CoteDivoire", "CakeArt"]},
    "ceo": {"password": "ceo123", "clients": ["CDC", "CoteDivoire", "CakeArt"]},
    "zaid": {"password": "zaid123", "clients": ["CDC"]},
    "mohammad": {"password": "mohammad123", "clients": ["CoteDivoire"]},
    "Khalid": {"password": "khalid123", "clients": ["CakeArt"]}  # CHANGED: cakeart_user to Khalid
}

# Client data sheets mapping - UPDATED WITH CakeArt
CLIENT_SHEETS = {
    "CDC": {
        "backaldrin": "Backaldrin_CDC",
        "bateel": "Bateel_CDC",
        "ceo_special": "CDC_CEO_Special_Prices"
    },
    "CoteDivoire": {
        "backaldrin": "Backaldrin_CoteDivoire",
        "bateel": "Bateel_CoteDivoire", 
        "ceo_special": "CoteDivoire_CEO_Special_Prices"
    },
    "CakeArt": {
        "backaldrin": "Backaldrin_CakeArt",
        "bateel": "Bateel_CakeArt",
        "ceo_special": "CakeArt_CEO_Special_Prices"
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
        <h2 style="text-align: center; margin-bottom: 1rem;">🚀 Multi-Client Dashboard</h2>
        <p style="text-align: center; color: var(--bs-secondary); margin-bottom: 2rem;">Professional Business Intelligence Platform</p>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")
        submit = st.form_submit_button("🎯 Login", use_container_width=True)
        
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
    """Main dashboard with tabs"""
    
    # Display user info in sidebar
    st.sidebar.markdown(f"**👤 Welcome, {st.session_state.username}**")
    st.sidebar.markdown(f"**🏢 Access to:** {', '.join(st.session_state.user_clients)}")
    logout_button()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 style="margin:0; font-size: 2.5em;">🏢 Multi-Client Business Dashboard</h1>
        <p style="margin:0; opacity:0.9; font-size: 1.2em;">Professional Analytics • Real-time Intelligence • Strategic Insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs - ADDED PRODUCT CATALOG TAB
    if st.session_state.username in ["ceo", "admin"]:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏢 CLIENTS", "📅 ETD SHEET", "⭐ CEO SPECIAL PRICES", "💰 PRICE INTELLIGENCE", "📦 PRODUCT CATALOG"])
    else:
        tab1, tab2, tab3, tab4 = st.tabs(["🏢 CLIENTS", "📅 ETD SHEET", "⭐ CEO SPECIAL PRICES", "📦 PRODUCT CATALOG"])
    
    with tab1:
        clients_tab()
    
    with tab2:
        etd_tab()
        
    with tab3:
        ceo_specials_tab()
    
    # Only show Price Intelligence tab for CEO/Admin
    if st.session_state.username in ["ceo", "admin"]:
        with tab4:
            price_intelligence_tab()

    # Product Catalog tab for all users
    if st.session_state.username in ["ceo", "admin"]:
        with tab5:
            product_catalog_tab()
    else:
        with tab4:
            product_catalog_tab()

# ... (rest of your existing functions remain exactly the same - they'll automatically use the new styling)
# [ALL YOUR EXISTING FUNCTIONS GO HERE - clients_tab(), etd_tab(), ceo_specials_tab(), etc.]

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
    """ETD Sheet tab"""
    st.subheader("📅 ETD Sheet - Live View")
    st.info("🔧 ETD Sheet integration will be added when ready")
    st.write("This tab will display your live ETD data when available")

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
                        <h3 style="margin:0; color: #ffc107;">{special['Article_Number']} - {special['Product_Name']}</h3>
                        <p style="margin:0; font-size: 1.2em; font-weight: bold; color: #ffd200;">
                            Special Price: {price_display} {special['Currency']}/kg
                        </p>
                        <p style="margin:0; color: #adb5bd;">
                            {status_color} {status_text} • Valid until: {special['Expiry_Date']}
                            {f" • Incoterm: {special['Incoterm']}" if pd.notna(special['Incoterm']) and special['Incoterm'] != '' else ''}
                        </p>
                        {f"<p style='margin:5px 0 0 0; color: #adb5bd;'><strong>Notes:</strong> {special['Notes']}</p>" if pd.notna(special['Notes']) and special['Notes'] != '' else ''}
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
                use_container_width=True
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
                use_container_width=True
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
    
    # Client selection - CEO can select specific clients or all - UPDATED WITH CakeArt
    available_clients = ["CDC", "CoteDivoire", "CakeArt"]
    
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
                use_container_width=True
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
                use_container_width=True
            )
            
    
    st.markdown('</div>', unsafe_allow_html=True)

def product_catalog_tab():
    """Full Product Catalog with comprehensive product information"""
    
    st.markdown("""
    <div class="intelligence-header">
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
                use_container_width=True
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
                use_container_width=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.info("No products match your search criteria.")

def display_product_card_flexible(product, available_columns):
    """Display individual product card with available columns only"""
    
    # Determine card color based on supplier if available
    if 'Supplier' in available_columns and product['Supplier'] == 'Backaldrin':
        card_class = "price-card"
        border_color = "#fc185a"
    elif 'Supplier' in available_columns and product['Supplier'] == 'Bateel':
        card_class = "special-price-card"
        border_color = "#ffc107"
    else:
        card_class = "intelligence-stat-card"
        border_color = "#02c27a"
    
    with st.expander(f"📦 {product['Article_Number']} - {product['Product_Name']}", expanded=False):
        # Build the card content dynamically based on available columns
        card_content = f"""
        <div class="{card_class}">
            <div style="border-left: 5px solid {border_color}; padding-left: 1rem;">
                <h3 style="margin:0; color: {border_color};">{product['Article_Number']} - {product['Product_Name']}</h3>
        """
        
        # Add Supplier if available
        if 'Supplier' in available_columns:
            card_content += f"""<p style="margin:0; font-weight: bold; color: #adb5bd;">Supplier: {product['Supplier']}</p>"""
        
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
                <p style="margin:0; color: #adb5bd;">{product['Common_Description']}</p>
            </div>
            """
        
        if 'Purpose_Of_Use' in available_columns and product['Purpose_Of_Use']:
            card_content += f"""
            <div style="margin-top: 1rem;">
                <p style="margin:0;"><strong>Purpose of Use:</strong></p>
                <p style="margin:0; color: #adb5bd;">{product['Purpose_Of_Use']}</p>
            </div>
            """
        
        if 'Dosage' in available_columns and product['Dosage']:
            card_content += f"""
            <div style="margin-top: 1rem;">
                <p style="margin:0;"><strong>Dosage:</strong></p>
                <p style="margin:0; color: #adb5bd;">{product['Dosage']}</p>
            </div>
            """
        
        if 'Ingredients' in available_columns and product['Ingredients']:
            card_content += f"""
            <div style="margin-top: 1rem;">
                <p style="margin:0;"><strong>Ingredients:</strong></p>
                <p style="margin:0; color: #adb5bd;">{product['Ingredients']}</p>
            </div>
            """
        
        if 'Datasheet_Link' in available_columns and product['Datasheet_Link']:
            card_content += f"""
            <div style="margin-top: 1rem;">
                <p style="margin:0;"><strong>Datasheet:</strong> <a href="{product['Datasheet_Link']}" target="_blank" style="color: #0dcaf0;">View Datasheet</a></p>
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
    """Load data from Google Sheets using API key - CLEAN VERSION"""
    try:
        # Get client-specific sheet names
        client_sheets = CLIENT_SHEETS[client]
        
        # Load Backaldrin data for specific client
        backaldrin_url = f"https://sheets.googleapis.com/v4/spreadsheets/{CDC_SHEET_ID}/values/{client_sheets['backaldrin']}!A:Z?key={API_KEY}"
        backaldrin_response = requests.get(backaldrin_url)
        
        # Load Bateel data for specific client
        bateel_url = f"https://sheets.googleapis.com/v4/spreadsheets/{CDC_SHEET_ID}/values/{client_sheets['bateel']}!A:Z?key={API_KEY}"
        bateel_response = requests.get(bateel_url)
        
        data = {"Backaldrin": {}, "Bateel": {}}
        
        def process_sheet_data(values, supplier_name, sheet_name):
            """Process sheet data using header names instead of positions"""
            if not values or len(values) < 2:
                return
                
            headers = [str(h).strip().lower() for h in values[0]]
            rows = values[1:]
            
            # Find column indices by header name
            try:
                order_no_idx = headers.index("order_number")
                order_date_idx = headers.index("order_date") 
                article_idx = headers.index("article_number")
                product_idx = headers.index("product_name")
                price_idx = headers.index("price_per_kg")
            except ValueError:
                return
            
            for row in rows:
                if len(row) > max(order_no_idx, order_date_idx, article_idx, product_idx, price_idx):
                    article = str(row[article_idx]).strip() if article_idx < len(row) and row[article_idx] else ""
                    product_name = row[product_idx] if product_idx < len(row) and row[product_idx] else ""
                    price_str = row[price_idx] if price_idx < len(row) and row[price_idx] else ""
                    order_no = row[order_no_idx] if order_no_idx < len(row) and row[order_no_idx] else ""
                    order_date = row[order_date_idx] if order_date_idx < len(row) and row[order_date_idx] else ""
                    
                    if article and price_str and article != "":
                        # CLEAN THE PRICE - remove currency and other text
                        try:
                            # Remove currency symbols and text, keep only numbers and decimals
                            cleaned_price = ''.join(c for c in price_str if c.isdigit() or c == '.' or c == '-')
                            if cleaned_price and cleaned_price != '.':
                                price_float = float(cleaned_price)
                            else:
                                continue
                        except ValueError:
                            continue
                        
                        if article not in data[supplier_name]:
                            data[supplier_name][article] = {
                                "prices": [],
                                "names": [],
                                "orders": []
                            }
                        
                        data[supplier_name][article]["prices"].append(price_float)
                        data[supplier_name][article]["orders"].append({
                            "price": price_float,
                            "order_no": order_no,
                            "date": order_date
                        })
                        
                        if product_name and product_name.strip() != "":
                            data[supplier_name][article]["names"].append(product_name)
                        else:
                            # If no product name, add a placeholder
                            data[supplier_name][article]["names"].append("No Name")
        
        # Process Backaldrin data
        if backaldrin_response.status_code == 200:
            backaldrin_values = backaldrin_response.json().get('values', [])
            process_sheet_data(backaldrin_values, "Backaldrin", client_sheets['backaldrin'])
        
        # Process Bateel data
        if bateel_response.status_code == 200:
            bateel_values = bateel_response.json().get('values', [])
            process_sheet_data(bateel_values, "Bateel", client_sheets['bateel'])
        
        return data
        
    except Exception as e:
        st.error(f"Error loading data for {client}: {str(e)}")
        return {"Backaldrin": {}, "Bateel": {}}

def get_sample_data():
    """Fallback sample data"""
    return {
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
            }
        }
    }

def create_export_data(article_data, article, supplier, client):
    """Create export data in different formats"""
    # Create DataFrame for export
    export_data = []
    for order in article_data['orders']:
        export_data.append({
            'Client': client,
            'Article_Number': article,
            'Supplier': supplier,
            'Product_Name': article_data['names'][0] if article_data['names'] else 'N/A',
            'Price_per_kg': order['price'],
            'Order_Number': order['order_no'],
            'Order_Date': order['date'],
            'Export_Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return pd.DataFrame(export_data)

def cdc_dashboard(client):
    """Client pricing dashboard with export features - NOW CLIENT SPECIFIC"""
    
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

    # Search section - CLEAN VERSION (no white box)
    st.subheader("🔍 Search Historical Prices")
    
    col1, col2 = st.columns(2)
    with col1:
        article = st.text_input("**ARTICLE NUMBER**", placeholder="e.g., 1-366, 1-367...", key=f"{client}_article")
    with col2:
        product = st.text_input("**PRODUCT NAME**", placeholder="e.g., Moist Muffin, Date Mix...", key=f"{client}_product")
    
    # Auto-suggestions
    search_term = article or product
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
    
    # Manual search
    if st.button("🚀 SEARCH HISTORICAL PRICES", use_container_width=True, type="primary", key=f"{client}_search"):
        handle_search(article, product, supplier, DATA, client)

    # Display results from session state
    if st.session_state.search_results and st.session_state.search_results.get("client") == client:
        display_from_session_state(DATA, client)

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

def handle_search(article, product, supplier, data, client):
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
                type="primary"
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
                    use_container_width=True
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
                use_container_width=True
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

# Run the main dashboard
if __name__ == "__main__":
    if not check_login():
        login_page()
    else:
        main_dashboard()
