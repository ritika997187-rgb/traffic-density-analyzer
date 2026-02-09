import streamlit as st

st.set_page_config(page_title="Traffic Density Analyzer")

st.title("🚦 Traffic Density Analyzer")

road = st.text_input("Enter Road Name")
vehicles = st.number_input("Enter Number of Vehicles", min_value=0, step=1)

if st.button("Analyze"):
    if vehicles < 20:
        st.success("Low Traffic 🟢")
    elif vehicles < 50:
        st.warning("Moderate Traffic 🟡")
    else:
        st.error("High Traffic 🔴")
