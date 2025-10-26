import streamlit as st
import pandas as pd

# Sample data - replace this with your Google Sheets connection later
sample_data = {
    "1-366": ["Moist Muffin Vanilla Mix", "موسيت مفن فانيلا ميكس"],
    "1-367": ["Moist Muffin Chocolate", "موسيت مفن شوكولاتة"],
    "1001": ["Premium Date Mix", "خليط التمر الفاخر"]
}

st.title("CDC Pricing Dashboard")
st.write("Search by article number or product name")

# Search input with suggestions
search_term = st.text_input("Start typing article number or product name...")

# Show suggestions
if search_term:
    suggestions = []
    for article, names in sample_data.items():
        if search_term.lower() in article.lower():
            suggestions.append(f"{article} - {names[0]}")
        for name in names:
            if search_term.lower() in name.lower():
                suggestions.append(f"{article} - {name}")
    
    if suggestions:
        st.write("**Suggestions:**")
        for suggestion in suggestions[:5]:  # Show top 5
            st.write(f"• {suggestion}")

if st.button("Search Prices"):
    if search_term:
        st.success(f"Searching: {search_term}")
        # Add your price lookup logic here
    else:
        st.warning("Please enter something to search")
