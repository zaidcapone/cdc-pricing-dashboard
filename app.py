import streamlit as st

st.title("CDC Pricing Dashboard")
st.write("Search prices")
article = st.text_input("Enter article number")
if st.button("Search"):
    st.write(f"Searching: {article}")
