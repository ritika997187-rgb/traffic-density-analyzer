import streamlit as st
import pandas as pd
from datetime import time

st.set_page_config(page_title="Traffic Density Analyzer")

st.title("🚦 Traffic Density Analyzer")

# Load CSV
df = pd.read_csv("TrafficTwoMonth.csv")

# Convert date & time
# CSV Date is only day number (10, 11, 12...)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date
    df["Time"],
    format="%I:%M:%S %p",
    errors="coerce"
).dt.time
df["Time"] = pd.to_datetime(df["Time"]).dt.time

# User inputs
selected_date = st.date_input("Select Date")
selected_time = st.time_input("Select Time", value=time(9, 0))

if st.button("Analyze Traffic"):
    filtered = df[
    (df["Date"] == selected_date.day) &
    (df["Time"] == selected_time)
    ]

    if filtered.empty:
        st.warning("No data available for selected date & time")
    else:
        vehicles = filtered["Vehicles"].iloc[0]

        st.write(f"🚗 Vehicles Count: **{vehicles}**")

        if vehicles < 20:
            st.success("Low Traffic 🟢")
        elif vehicles < 50:
            st.warning("Moderate Traffic 🟡")
        else:
            st.error("High Traffic 🔴")
