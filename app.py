import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Traffic Density Analyzer")

st.title("🚦 Traffic Density Analyzer")

# Load CSV
df = pd.read_csv("TrafficTwoMonth.csv")

# Clean columns
df["Date"] = df["Date"].astype(int)
df["Time"] = pd.to_datetime(df["Time"], format="%I:%M:%S %p").dt.time

# Location selection
st.subheader("📍 Location Details")

locations = ["MG Road", "Ring Road", "Market Area", "Highway"]
location = st.selectbox("Select Location", locations)
day = st.number_input(
    "Enter Day (Date number only, e.g. 10)",
    min_value=1,
    max_value=31,
    step=1
)

selected_time = st.time_input("Select Time")

if st.button("Analyze Traffic"):
    filtered = df[
        (df["Date"] == day) &
        (df["Time"] == selected_time)
    ]

    if filtered.empty:
        st.warning("No data available for selected day & time")
    else:
        vehicles = int(filtered["CarCount"].values[0])

        st.info(f"📍 Location: {location if location else 'Not specified'}")
        st.info(f"🚗 Vehicles count: {vehicles}")

        if vehicles < 20:
            st.success("Low Traffic 🟢")
        elif vehicles < 50:
            st.warning("Moderate Traffic 🟡")
        else:
            st.error("High Traffic 🔴")
