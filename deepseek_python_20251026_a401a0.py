import streamlit as st

st.title("CDC Pricing Dashboard")
st.write("Search: 1-366 or 1001")
article = st.text_input("Article Number")
if article:
    st.write(f"Searching: {article}")