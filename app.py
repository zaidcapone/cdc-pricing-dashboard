import streamlit as st
import gspread
from google.oauth2 import service_account

def main():
    st.title("🔗 Google Sheets Connection Test")
    st.write("Testing connection...")
    
    try:
        # Create credentials from secrets
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp"],
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        
        # Authorize
        gc = gspread.authorize(credentials)
        st.success("✅ Step 1: Authorization successful!")
        
        # Open sheet
        sheet = gc.open("CDC_Pricing_Database")
        st.success("✅ Step 2: Sheet opened successfully!")
        st.write(f"**Sheet:** {sheet.title}")
        
        # Test reading worksheets
        backaldrin_ws = sheet.worksheet("Backaldrin")
        backaldrin_data = backaldrin_ws.get_all_records()
        st.success(f"✅ Step 3: Backaldrin data loaded! ({len(backaldrin_data)} records)")
        
        bateel_ws = sheet.worksheet("Bateel")
        bateel_data = bateel_ws.get_all_records()
        st.success(f"✅ Step 4: Bateel data loaded! ({len(bateel_data)} records)")
        
        # Show success
        st.balloons()
        st.success("🎉 ALL CONNECTIONS WORKING! Google Sheets is ready!")
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
