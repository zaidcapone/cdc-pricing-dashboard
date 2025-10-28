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

# Custom CSS for main dashboard
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
</style>
""", unsafe_allow_html=True)

# Configuration
API_KEY = "AIzaSyA3P-ZpLjDdVtGB82_1kaWuO7lNbKDj9HU"
CDC_SHEET_ID = "1qWgVT0l76VsxQzYExpLfioBHprd3IvxJzjQWv3RryJI"

def main_dashboard():
    """Main dashboard with tabs"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏢 Multi-Client Business Dashboard</h1>
        <p>Centralized Management • Real-time Data • Professional Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs - ADDED CEO SPECIALS TAB
    tab1, tab2, tab3 = st.tabs(["🏢 CLIENTS", "📅 ETD SHEET", "⭐ CEO SPECIAL PRICES"])
    
    with tab1:
        clients_tab()
    
    with tab2:
        etd_tab()
        
    with tab3:
        ceo_specials_tab()

def clients_tab():
    """Clients management tab"""
    st.subheader("Client Selection")
    
    # Client selection
    client = st.selectbox(
        "Select Client:",
        ["CDC", "Client 2", "Client 3", "Client 4"],
        key="client_select"
    )
    
    if client == "CDC":
        cdc_dashboard()
    else:
        st.info(f"🔧 {client} dashboard coming soon...")

def etd_tab():
    """ETD Sheet tab"""
    st.subheader("📅 ETD Sheet - Live View")
    st.info("🔧 ETD Sheet integration will be added when ready")
    st.write("This tab will display your live ETD data when available")

def ceo_specials_tab():
    """CEO Special Prices tab"""
    st.markdown("""
    <div class="ceo-header">
        <h2 style="margin:0;">⭐ CEO Special Prices</h2>
        <p style="margin:0; opacity:0.9;">Exclusive Pricing • Limited Time Offers • VIP Client Rates</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load CEO special prices
    ceo_data = load_ceo_special_prices()
    
    if ceo_data.empty:
        st.warning("⚠️ No CEO special prices found. Please add data to 'CEO_Special_Prices' sheet.")
        st.info("""
        **To add CEO special prices:**
        1. Go to your Google Sheet
        2. Add a new tab called **'CEO_Special_Prices'**
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
    st.subheader("📊 CEO Specials Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Special Offers", len(ceo_data))
    with col2:
        active_offers = len(ceo_data[ceo_data['Expiry_Date'] >= datetime.now().strftime('%Y-%m-%d')])
        st.metric("Active Offers", active_offers)
    with col3:
        # SAFE AVERAGE CALCULATION - handles multiple currencies and formats
        try:
            # Convert to numeric, coerce errors to NaN
            prices = pd.to_numeric(ceo_data['Special_Price'], errors='coerce')
            avg_price = prices.mean()
            if pd.notna(avg_price):
                st.metric("Avg Special Price", f"${avg_price:.2f}")
            else:
                st.metric("Avg Special Price", "N/A")
        except:
            st.metric("Avg Special Price", "N/A")
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
    st.subheader("🎯 Special Price List")
    
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
                file_name=f"ceo_special_prices_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            st.download_button(
                label="📄 Download Summary",
                data=f"""
CEO Special Prices Summary
==========================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Total Offers: {len(filtered_data)}
Active Offers: {len(filtered_data[filtered_data['Expiry_Date'] >= datetime.now().strftime('%Y-%m-%d')])}

Special Prices:
{chr(10).join([f"• {row['Article_Number']} - {row['Product_Name']}: {row['Special_Price']} {row['Currency']} (Incoterm: {row['Incoterm']}, Until: {row['Expiry_Date']})" for _, row in filtered_data.iterrows()])}
                """,
                file_name=f"ceo_specials_summary_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.info("No CEO special prices match your search criteria.")

def load_ceo_special_prices():
    """Load CEO special prices from Google Sheets - UPDATED FOR 8 COLUMNS"""
    try:
        ceo_url = f"https://sheets.googleapis.com/v4/spreadsheets/{CDC_SHEET_ID}/values/CEO_Special_Prices!A:Z?key={API_KEY}"
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
                    st.error(f"Missing required columns. Found: {list(df.columns)}")
                    return pd.DataFrame()
                
        return pd.DataFrame()
        
    except Exception as e:
        st.error(f"Error loading CEO special prices: {str(e)}")
        return pd.DataFrame()

# [KEEP ALL YOUR EXISTING FUNCTIONS BELOW - NO CHANGES NEEDED]
# get_google_sheets_data, get_sample_data, cdc_dashboard, 
# get_suggestions, handle_search, display_from_session_state, 
# create_export_data

def get_google_sheets_data():
    """Load data from Google Sheets using API key"""
    try:
        # Load Backaldrin data
        backaldrin_url = f"https://sheets.googleapis.com/v4/spreadsheets/{CDC_SHEET_ID}/values/Backaldrin!A:Z?key={API_KEY}"
        backaldrin_response = requests.get(backaldrin_url)
        
        # Load Bateel data
        bateel_url = f"https://sheets.googleapis.com/v4/spreadsheets/{CDC_SHEET_ID}/values/Bateel!A:Z?key={API_KEY}"
        bateel_response = requests.get(bateel_url)
        
        data = {"Backaldrin": {}, "Bateel": {}}
        
        # Process Backaldrin data
        if backaldrin_response.status_code == 200:
            backaldrin_values = backaldrin_response.json().get('values', [])
            if len(backaldrin_values) > 1:
                for row in backaldrin_values[1:]:
                    if len(row) >= 5:
                        article = str(row[2]) if len(row) > 2 else ""
                        product_name = row[3] if len(row) > 3 else ""
                        price = row[4] if len(row) > 4 else ""
                        order_no = row[0] if len(row) > 0 else ""
                        order_date = row[1] if len(row) > 1 else ""
                        
                        if article and price:
                            if article not in data["Backaldrin"]:
                                data["Backaldrin"][article] = {
                                    "prices": [],
                                    "names": [],
                                    "orders": []
                                }
                            
                            try:
                                price_float = float(price)
                                data["Backaldrin"][article]["prices"].append(price_float)
                                data["Backaldrin"][article]["orders"].append({
                                    "price": price_float,
                                    "order_no": order_no,
                                    "date": order_date
                                })
                                
                                if product_name and product_name not in data["Backaldrin"][article]["names"]:
                                    data["Backaldrin"][article]["names"].append(product_name)
                            except ValueError:
                                continue
        
        # Process Bateel data
        if bateel_response.status_code == 200:
            bateel_values = bateel_response.json().get('values', [])
            if len(bateel_values) > 1:
                for row in bateel_values[1:]:
                    if len(row) >= 5:
                        article = str(row[2]) if len(row) > 2 else ""
                        product_name = row[3] if len(row) > 3 else ""
                        price = row[4] if len(row) > 4 else ""
                        order_no = row[0] if len(row) > 0 else ""
                        order_date = row[1] if len(row) > 1 else ""
                        
                        if article and price:
                            if article not in data["Bateel"]:
                                data["Bateel"][article] = {
                                    "prices": [],
                                    "names": [],
                                    "orders": []
                                }
                            
                            try:
                                price_float = float(price)
                                data["Bateel"][article]["prices"].append(price_float)
                                data["Bateel"][article]["orders"].append({
                                    "price": price_float,
                                    "order_no": order_no,
                                    "date": order_date
                                })
                                
                                if product_name and product_name not in data["Bateel"][article]["names"]:
                                    data["Bateel"][article]["names"].append(product_name)
                            except ValueError:
                                continue
        
        return data
        
    except Exception as e:
        return get_sample_data()

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

def create_export_data(article_data, article, supplier):
    """Create export data in different formats"""
    # Create DataFrame for export
    export_data = []
    for order in article_data['orders']:
        export_data.append({
            'Article_Number': article,
            'Supplier': supplier,
            'Product_Name': article_data['names'][0] if article_data['names'] else 'N/A',
            'Price_per_kg': order['price'],
            'Order_Number': order['order_no'],
            'Order_Date': order['date'],
            'Export_Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return pd.DataFrame(export_data)

def cdc_dashboard():
    """Your complete functional CDC pricing dashboard with export features"""
    
    # Initialize session state
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'export_data' not in st.session_state:
        st.session_state.export_data = None
    
    st.markdown("""
    <div class="cdc-header">
        <h2 style="margin:0;">📊 CDC Pricing Dashboard</h2>
        <p style="margin:0; opacity:0.9;">Backaldrin & Bateel • Live Google Sheets Data • Export Ready</p>
    </div>
    """, unsafe_allow_html=True)

    # Data source selection
    col1, col2 = st.columns([3, 1])
    with col1:
        data_source = st.radio("Data Source:", ["Sample Data", "Google Sheets"], horizontal=True, key="cdc_data_source")
    with col2:
        if st.button("🔄 Refresh Data", use_container_width=True, type="secondary", key="cdc_refresh"):
            st.rerun()
    
    # Load data
    if data_source == "Google Sheets":
        DATA = get_google_sheets_data()
        st.success("✅ Connected to Google Sheets - Live Data!")
    else:
        DATA = get_sample_data()
        st.info("📊 Using sample data - Switch to Google Sheets for live data")

    # Supplier selection
    st.subheader("🏢 Select Supplier")
    supplier = st.radio("", ["Backaldrin", "Bateel"], horizontal=True, label_visibility="collapsed", key="cdc_supplier")

    # Search section
    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    st.subheader("🔍 Search Historical Prices")
    
    col1, col2 = st.columns(2)
    with col1:
        article = st.text_input("**ARTICLE NUMBER**", placeholder="e.g., 1-366, 1-367...", key="cdc_article")
    with col2:
        product = st.text_input("**PRODUCT NAME**", placeholder="e.g., Moist Muffin, Date Mix...", key="cdc_product")
    
    # Auto-suggestions
    search_term = article or product
    if search_term:
        suggestions = get_suggestions(search_term, supplier, DATA)
        if suggestions:
            st.markdown("**💡 Quick Suggestions:**")
            for i, suggestion in enumerate(suggestions[:4]):
                with st.form(key=f"cdc_form_{i}"):
                    if st.form_submit_button(suggestion["display"], use_container_width=True):
                        st.session_state.search_results = {
                            "article": suggestion["value"],
                            "supplier": supplier
                        }
                        st.rerun()
    
    # Manual search
    if st.button("🚀 SEARCH HISTORICAL PRICES", use_container_width=True, type="primary", key="cdc_search"):
        handle_search(article, product, supplier, DATA)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Display results from session state
    if st.session_state.search_results:
        display_from_session_state(DATA)

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
            # Prepare export data
            st.session_state.export_data = create_export_data(article_data, article_num, supplier)
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
                file_name=f"cdc_pricing_{article}_{datetime.now().strftime('%Y%m%d')}.csv",
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
                    file_name=f"cdc_pricing_{article}_{datetime.now().strftime('%Y%m%d')}.xlsx",
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
CDC Pricing Summary Report
==========================

Article: {article}
Supplier: {supplier}
Product: {export_df['Product_Name'].iloc[0]}
Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Price Statistics:
• Total Records: {len(export_df)}
• Minimum Price: ${min(prices):.2f}/kg
• Maximum Price: ${max(prices):.2f}/kg  
• Average Price: ${sum(prices)/len(prices):.2f}/kg

Orders Included: {', '.join(export_df['Order_Number'].tolist())}
                """,
                file_name=f"cdc_summary_{article}_{datetime.now().strftime('%Y%m%d')}.txt",
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
    main_dashboard()
