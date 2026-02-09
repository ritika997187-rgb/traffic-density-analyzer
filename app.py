import streamlit as st
import pandas as pd
from datetime import time

# Page config
st.set_page_config(page_title="Traffic Density Analyzer")

st.title("🚦 Traffic Density Analyzer")

# Load CSV
df = pd.read_csv("TrafficTwoMonth.csv")

# ---- DATA CLEANING ----

# Date column (sirf day number hai, jaise 10, 11 etc.)
df["Date"] = df["Date"].astype(int)

# Time column (12:00:00 AM format)
df["Time"] = pd.to_datetime(
    df["Time"],
    format="%I:%M:%S %p",
    errors="coerce"
).dt.time

# ---- USER INPUTS ----

selected_day = st.number_input(
    "Enter Day (Date number only, e.g. 10)",
    min_value=1,
    max_value=31,
    step=1
)

selected_time = st.time_input(
    "Select Time",
    value=time(9, 0)
)

# ---- ANALYSIS ----

if st.button("Analyze Traffic"):
    filtered = df[
        (df["Date"] == selected_day) &
        (df["Time"] == selected_time)
    ]

    if filtered.empty:
        st.warning("No data available for selected date & time")
    else:
        avg_cars = int(filtered["CarCount"].mean())
        st.success(f"Average Vehicles: {avg_cars}")

        if avg_cars < 20:
            st.success("Low Traffic 🟢")
        elif avg_cars < 50:
            st.warning("Moderate Traffic 🟡")
        else:
            st.error("High Traffic 🔴")
