import streamlit as st
import pandas as pd
from datetime import datetime

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Traffic Density Analyzer",
    layout="centered"
)

# ================= DARK BACKGROUND =================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🚦 Traffic Density Analyzer")

# ================= LOAD DATA =================
df = pd.read_csv("TrafficTwoMonth.csv")

# ================= CLEAN DATA =================
df["Date"] = df["Date"].astype(int)
df["Time"] = pd.to_datetime(df["Time"]).dt.time

# ================= INPUT SECTION =================
st.subheader("📍 Location Details")

locations = [
    "Main Road",
    "Ring Road",
    "Market Area",
    "Highway",
    "Bus Stand",
    "Railway Station",
    "School Zone",
    "Hospital Area",
    "Residential Colony",
    "City Center"
]

location = st.selectbox("Select Location", locations)

day = st.number_input(
    "Enter Day (Date number)",
    min_value=1,
    max_value=31,
    step=1
)

selected_time = st.time_input("Select Time")

weather = st.selectbox(
    "Select Weather",
    ["Clear", "Rainy", "Foggy", "Stormy"]
)

# ================= ANALYZE BUTTON =================
if st.button("🔍 Analyze Traffic"):

    filtered = df[
        (df["Date"] == day) &
        (df["Time"] == selected_time)
    ]

    if filtered.empty:
        st.warning("No data available for selected inputs")
    else:
        vehicles = int(filtered["CarCount"].values[0])
        day_name = filtered.iloc[0]["Day"]

        hour = selected_time.hour

        if weather == "Rainy":
            vehicles += 10
        elif weather == "Foggy":
            vehicles += 5
        elif weather == "Stormy":
            vehicles += 15

        st.markdown("### 📊 Traffic Analysis")

        st.info(f"📍 Location: {location}")
        st.info(f"📅 Day: {day_name}")
        st.info(f"⏰ Time: {selected_time}")
        st.info(f"🚗 Vehicle Count (Adjusted): {vehicles}")
        st.info(f"🌦️ Weather: {weather}")

        if 8 <= hour <= 10 or 17 <= hour <= 20:
            traffic = "High Traffic 🔴"
        elif vehicles < 20:
            traffic = "Low Traffic 🟢"
        else:
            traffic = "Moderate Traffic 🟡"

        st.markdown("### 🚦 Traffic Level")
        st.success(traffic)

        st.markdown("### 📈 Traffic Trend (Same Day)")
        day_data = df[df["Date"] == day].sort_values("Time")
        st.line_chart(day_data.set_index("Time")["CarCount"])
