import streamlit as st
import pandas as pd
import requests

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
    .tab-content {
        padding: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

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
        etd_tab()

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
    """ETD Sheet tab - direct view of your online sheet"""
    st.subheader("📅 ETD Sheet - Live View")
    
    # ETD Sheet configuration
    ETD_SHEET_ID = "your-etd-sheet-id-here"  # You'll provide this
    API_KEY = "AIzaSyA3P-ZpLjDdVtGB82_1kaWuO7lNbKDj9HU"
    
    try:
        # Load ETD data
        etd_url = f"https://sheets.googleapis.com/v4/spreadsheets/{ETD_SHEET_ID}/values/Sheet1!A:Z?key={API_KEY}"
        response = requests.get(etd_url)
        
        if response.status_code == 200:
            data = response.json()
            values = data.get('values', [])
            
            if values:
                # Convert to DataFrame for nice display
                headers = values[0]
                rows = values[1:] if len(values) > 1 else []
                
                if rows:
                    df = pd.DataFrame(rows, columns=headers)
                    st.success(f"✅ ETD Sheet Loaded: {len(rows)} records")
                    
                    # Search and filter
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        search_term = st.text_input("🔍 Search ETD data...")
                    with col2:
                        st.metric("Total Records", len(rows))
                    
                    # Filter data if search term
                    if search_term:
                        mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
                        filtered_df = df[mask]
                        st.write(f"**Filtered Results ({len(filtered_df)} records):**")
                        st.dataframe(filtered_df, use_container_width=True)
                    else:
                        st.dataframe(df, use_container_width=True)
                else:
                    st.warning("ETD sheet has headers but no data rows")
            else:
                st.error("ETD sheet is empty or not accessible")
        else:
            st.error(f"❌ Could not load ETD sheet. Error: {response.status_code}")
            
    except Exception as e:
        st.error(f"❌ ETD connection error: {str(e)}")
        st.info("Please provide the ETD Sheet ID to connect")

def cdc_dashboard():
    """Your existing CDC dashboard - copied from previous working version"""
    
    # CDC-specific CSS
    st.markdown("""
    <style>
        .cdc-header {
            background: linear-gradient(135deg, #991B1B, #7F1D1D);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        .search-card {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            border: 2px solid #991B1B;
            margin-bottom: 1rem;
        }
        .price-card {
            background: #FEE2E2;
            padding: 1rem;
            border-radius: 6px;
            border-left: 4px solid #991B1B;
            margin: 0.5rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="cdc-header">
        <h2 style="margin:0;">📊 CDC Pricing Dashboard</h2>
        <p style="margin:0; opacity:0.9;">Backaldrin & Bateel • Live Google Sheets Data</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Your existing CDC dashboard code goes here
    # [PASTE YOUR ENTIRE WORKING CDC DASHBOARD CODE HERE]
    # This should include all the search, auto-suggestions, price display logic
    
    st.info("🔧 CDC dashboard content would be loaded here")
    st.write("This is where your complete CDC pricing dashboard appears")
    st.write("We'll integrate the full working CDC code here")

# Run the main dashboard
if __name__ == "__main__":
    main_dashboard()
