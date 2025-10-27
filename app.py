import streamlit as st
import gspread
from google.oauth2 import service_account

def main():
    st.title("🔗 Google Sheets Connection Test")
    st.write("Testing connection to your CDC Pricing Database...")
    
    try:
        # Test connection to Google Sheets
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp"],
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        gc = gspread.authorize(credentials)
        
        # Open your sheet
        sheet = gc.open("CDC_Pricing_Database")
        st.success("✅ SUCCESS! Connected to Google Sheets!")
        st.write(f"**Sheet Name:** {sheet.title}")
        
        # Test reading Backaldrin data
        backaldrin_ws = sheet.worksheet("Backaldrin")
        backaldrin_data = backaldrin_ws.get_all_records()
        st.write(f"**Backaldrin Records:** {len(backaldrin_data)}")
        
        # Test reading Bateel data  
        bateel_ws = sheet.worksheet("Bateel")
        bateel_data = bateel_ws.get_all_records()
        st.write(f"**Bateel Records:** {len(bateel_data)}")
        
        # Show sample data if available
        if backaldrin_data:
            st.write("**Sample Backaldrin Data:**")
            st.dataframe(backaldrin_data[:3])  # Show first 3 records
        
        if bateel_data:
            st.write("**Sample Bateel Data:**")
            st.dataframe(bateel_data[:3])  # Show first 3 records
            
    except Exception as e:
        st.error(f"❌ Connection failed: {str(e)}")
        st.info("Please check: 1) Streamlit secrets are correct 2) Sheet is shared with service account")

if __name__ == "__main__":
    main()
