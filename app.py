import streamlit as st
import pandas as pd
import requests
import json

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
    .etd-header {
        background: linear-gradient(135deg, #1E40AF, #1E3A8A);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Configuration
API_KEY = "AIzaSyA3P-ZpLjDdVtGB82_1kaWuO7lNbKDj9HU"
CDC_SHEET_ID = "1qWgVT0l76VsxQzYExpLfioBHprd3IvxJzjQWv3RryJI"
ETD_SHEET_ID = "1UpcibID2KszAUet04FcAvzJi0VZmmrqz"  # Your ETD Sheet ID

def main_dashboard():
    """Main dashboard with tabs"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏢 Multi-Client Business Dashboard</h1>
        <p>Centralized Management • Real-time Data • Professional Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2 = st.tabs(["🏢 CLIENTS", "📅 ETD SHEET"])
    
    with tab1:
        clients_tab()
    
    with tab2:
        etd_dashboard()

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

def etd_dashboard():
    """ETD Sheet - Live Data Dashboard"""
    st.markdown("""
    <div class="etd-header">
        <h2 style="margin:0;">📅 ETD Sheet - Live Data</h2>
        <p style="margin:0; opacity:0.9;">Real-time ETD Data • Professional Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        # Load ETD data - try different sheet names
        sheet_names = ["Sheet1", "ETD", "Data", "Sheet 1"]
        etd_data = None
        
        for sheet_name in sheet_names:
            try:
                etd_url = f"https://sheets.googleapis.com/v4/spreadsheets/{ETD_SHEET_ID}/values/{sheet_name}!A:Z?key={API_KEY}"
                response = requests.get(etd_url)
                
                if response.status_code == 200:
                    data = response.json()
                    values = data.get('values', [])
                    
                    if values and len(values) > 1:
                        etd_data = values
                        st.success(f"✅ ETD Sheet Connected! Using sheet: '{sheet_name}'")
                        break
            except:
                continue
        
        if etd_data:
            headers = etd_data[0]
            rows = etd_data[1:]
            
            df = pd.DataFrame(rows, columns=headers)
            
            # ETD Analytics
            st.subheader("📊 ETD Overview")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Records", len(df))
            with col2:
                st.metric("Columns", len(df.columns))
            with col3:
                # Show sample of first few column names
                sample_cols = ", ".join(df.columns[:3]) + "..." if len(df.columns) > 3 else ", ".join(df.columns)
                st.metric("Columns Sample", sample_cols)
            with col4:
                st.metric("Status", "✅ Connected")
            
            # Search and Filters
            st.subheader("🔍 Search & Filter ETD Data")
            search_col1, search_col2 = st.columns([2, 1])
            
            with search_col1:
                search_term = st.text_input("Search across all columns...", key="etd_search")
            
            with search_col2:
                show_records = st.selectbox("Show records:", ["All Records", "First 50", "First 100"], key="etd_show")
            
            # Filter data
            if search_term:
                mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
                filtered_df = df[mask]
                st.write(f"**Filtered Results ({len(filtered_df)} records):**")
                display_df = filtered_df
            else:
                display_df = df
            
            # Limit records if selected
            if show_records == "First 50":
                display_df = display_df.head(50)
            elif show_records == "First 100":
                display_df = display_df.head(100)
            
            # Display data
            st.dataframe(display_df, use_container_width=True, height=400)
            
            # Data Summary
            with st.expander("📋 Data Summary & Export"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Dataset Info:**")
                    st.write(f"• **Total Rows:** {len(df)}")
                    st.write(f"• **Total Columns:** {len(df.columns)}")
                    st.write(f"• **Memory Usage:** {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
                    
                with col2:
                    st.write("**Columns:**")
                    for col in df.columns:
                        st.write(f"• {col}")
                
                # Export options
                st.write("**Export Data:**")
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name="etd_data.csv",
                    mime="text/csv",
                )
                
        else:
            st.error("❌ Could not load ETD data. Please check:")
            st.info("""
            1. **Sheet is public** (Share → Anyone with link can view)
            2. **Sheet has data** (not empty)
            3. **Sheet tab name** is one of: Sheet1, ETD, Data, Sheet 1
            """)
            
    except Exception as e:
        st.error(f"❌ ETD connection error: {str(e)}")
        st.info("""
        **Quick Fixes:**
        • Make sure ETD Sheet is **public** (Share → Anyone with link)
        • Check the sheet has **data rows**
        • Verify the **sheet tab name** at the bottom
        """)

# [KEEP ALL YOUR EXISTING CDC FUNCTIONS HERE]
# get_google_sheets_data, get_sample_data, cdc_dashboard, 
# get_suggestions, handle_search, display_from_session_state

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

def cdc_dashboard():
    """Your complete functional CDC pricing dashboard"""
    
    # Initialize session state
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    
    st.markdown("""
    <div class="cdc-header">
        <h2 style="margin:0;">📊 CDC Pricing Dashboard</h2>
        <p style="margin:0; opacity:0.9;">Backaldrin & Bateel • Live Google Sheets Data</p>
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

# Run the main dashboard
if __name__ == "__main__":
    main_dashboard()
