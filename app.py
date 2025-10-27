import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account
from datetime import datetime

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
    .data-management {
        background: #F0F9FF;
        padding: 2rem;
        border-radius: 10px;
        border: 2px solid #0EA5E9;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Google Sheets Configuration
def connect_to_google_sheets():
    try:
        # Create connection using Streamlit secrets
        credentials_dict = {
            "type": st.secrets["gcp"]["type"],
            "project_id": st.secrets["gcp"]["project_id"],
            "private_key_id": st.secrets["gcp"]["private_key_id"],
            "private_key": st.secrets["gcp"]["private_key"],
            "client_email": st.secrets["gcp"]["client_email"],
            "client_id": st.secrets["gcp"]["client_id"],
            "auth_uri": st.secrets["gcp"]["auth_uri"],
            "token_uri": st.secrets["gcp"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["gcp"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["gcp"]["client_x509_cert_url"]
        }
        
        credentials = service_account.Credentials.from_service_account_info(
            credentials_dict,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        gc = gspread.authorize(credentials)
        
        # Open your Google Sheet
        sheet = gc.open("CDC_Pricing_Database")
        return sheet
    except Exception as e:
        st.error(f"❌ Google Sheets connection failed: {str(e)}")
        return None

def load_data_from_sheets():
    """Load data from Google Sheets and format it for the dashboard"""
    sheet = connect_to_google_sheets()
    if not sheet:
        return get_sample_data()
    
    try:
        data = {"Backaldrin": {}, "Bateel": {}}
        
        # Load Backaldrin data
        backaldrin_ws = sheet.worksheet("Backaldrin")
        backaldrin_records = backaldrin_ws.get_all_records()
        
        for record in backaldrin_records:
            if record.get('Article_Number') and record.get('Price_per_kg'):
                article = str(record['Article_Number'])
                if article not in data["Backaldrin"]:
                    data["Backaldrin"][article] = {
                        "prices": [],
                        "names": [],
                        "orders": []
                    }
                
                # Add price
                data["Backaldrin"][article]["prices"].append(float(record['Price_per_kg']))
                
                # Add product name if not already there
                product_name = record.get('Product_Name', '')
                if product_name and product_name not in data["Backaldrin"][article]["names"]:
                    data["Backaldrin"][article]["names"].append(product_name)
                
                # Add order details
                data["Backaldrin"][article]["orders"].append({
                    "price": float(record['Price_per_kg']),
                    "order_no": record.get('Order_Number', 'N/A'),
                    "date": record.get('Order_Date', 'N/A')
                })
        
        # Load Bateel data
        bateel_ws = sheet.worksheet("Bateel")
        bateel_records = bateel_ws.get_all_records()
        
        for record in bateel_records:
            if record.get('Article_Number') and record.get('Price_per_kg'):
                article = str(record['Article_Number'])
                if article not in data["Bateel"]:
                    data["Bateel"][article] = {
                        "prices": [],
                        "names": [],
                        "orders": []
                    }
                
                data["Bateel"][article]["prices"].append(float(record['Price_per_kg']))
                
                product_name = record.get('Product_Name', '')
                if product_name and product_name not in data["Bateel"][article]["names"]:
                    data["Bateel"][article]["names"].append(product_name)
                
                data["Bateel"][article]["orders"].append({
                    "price": float(record['Price_per_kg']),
                    "order_no": record.get('Order_Number', 'N/A'),
                    "date": record.get('Order_Date', 'N/A')
                })
        
        return data
        
    except Exception as e:
        st.error(f"❌ Error loading data from Google Sheets: {str(e)}")
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

def add_order_to_sheets(supplier, article, product_name, price, order_no, order_date):
    """Add a new order to Google Sheets"""
    try:
        sheet = connect_to_google_sheets()
        if not sheet:
            return False, "Failed to connect to Google Sheets"
        
        worksheet = sheet.worksheet(supplier)
        
        # Add new row
        new_row = [
            order_no,
            order_date,
            article,
            product_name,
            float(price),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        
        worksheet.append_row(new_row)
        return True, "Order added successfully!"
        
    except Exception as e:
        return False, f"Error adding order: {str(e)}"

def main():
    # Initialize session state
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    
    # Load data
    SAMPLE_DATA = load_data_from_sheets()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 style="margin:0; font-size:2.5em;">📊 CDC Pricing Dashboard</h1>
        <p style="margin:10px 0 0 0; font-size:1.2em; opacity:0.9;">Live Google Sheets Integration • Real-time Data</p>
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

    # Data Management Section
    st.markdown('<div class="data-management">', unsafe_allow_html=True)
    st.subheader("📥 Add New Order to Google Sheets")
    
    with st.form("add_order_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            new_supplier = st.selectbox("Supplier", ["Backaldrin", "Bateel"])
            new_article = st.text_input("Article Number*")
        with col2:
            new_product = st.text_input("Product Name*")
            new_price = st.number_input("Price per kg*", min_value=0.0, step=0.01, format="%.2f")
        with col3:
            new_order_no = st.text_input("Order Number*")
            new_date = st.text_input("Order Date*", placeholder="YYYY-MM-DD")
        
        if st.form_submit_button("💾 Add Order to Database", use_container_width=True):
            if all([new_article, new_product, new_price > 0, new_order_no, new_date]):
                success, message = add_order_to_sheets(
                    new_supplier, new_article, new_product, new_price, new_order_no, new_date
                )
                if success:
                    st.success(f"✅ {message}")
                    st.info("🔄 Refresh the page to see updated data")
                else:
                    st.error(f"❌ {message}")
            else:
                st.error("❌ Please fill all required fields (*)")
    
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
