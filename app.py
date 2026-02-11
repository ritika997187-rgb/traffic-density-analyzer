import streamlit as st
import pandas as pd
from datetime import datetime

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Traffic Density Analyzer",
    layout="centered"
)

# ================= DARK THEME =================
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

# ================= TITLE =================
st.markdown("## 🚦 Traffic Density Analyzer")

# ================= LOAD DATA =================
df = pd.read_csv("TrafficTwoMonth.csv")

df["Date"] = pd.to_datetime(df["Date"])
df["Time"] = pd.to_datetime(df["Time"]).dt.time

# ================= INPUTS =================
st.markdown("### 📍 Location Details")

location = st.selectbox(
    "Select Location",
    df["Location"].unique()
)

day = st.number_input(
    "Enter Day (Date number)",
    min_value=1,
    max_value=31,
    value=1
)

selected_time = st.time_input(
    "Select Time",
    datetime.now().time()
)

weather = st.selectbox(
    "Select Weather",
    ["Clear", "Rainy", "Foggy"]
)

# ================= BUTTON =================
if st.button("🔍 Analyze Traffic"):

    filtered = df[
        (df["Location"] == location) &
        (df["Date"].dt.day == day) &
        (df["Time"] == selected_time)
    ]

    if filtered.empty:
        st.warning("No data available for selected inputs.")
    else:
        vehicles = int(filtered.iloc[0]["CarCount"])
        day_name = filtered.iloc[0]["Day of the Week"]
        hour = selected_time.hour

        # ================= TRAFFIC LOGIC =================
        if (8 <= hour <= 10) or (17 <= hour <= 20) or weather in ["Rainy", "Foggy"]:
            traffic = "High Traffic 🔴"
            reasons = [
                "Peak hours or bad weather",
                "Slow vehicle movement"
            ]
        elif vehicles < 20:
            traffic = "Low Traffic 🟢"
            reasons = [
                "Less vehicles",
                "Non-peak hours"
            ]
        else:
            traffic = "Moderate Traffic 🟡"
            reasons = [
                "Normal flow",
                "Manageable congestion"
            ]

        # ================= OUTPUT =================
        st.markdown("### 📊 Traffic Analysis")
        st.info(f"📍 Location: {location}")
        st.info(f"📅 Day: {day_name}")
        st.info(f"⏰ Time: {selected_time}")
        st.info(f"🌦️ Weather: {weather}")
        st.info(f"🚗 Vehicle Count: {vehicles}")

        st.markdown("### 🚦 Traffic Level")
        st.success(traffic)

        st.markdown("**Reason:**")
        for r in reasons:
            st.write(f"• {r}")

        # ================= PEAK HOUR =================
        st.markdown("### ⏰ Peak Hour Indicator")
        if 8 <= hour <= 10 or 17 <= hour <= 20:
            st.error("Peak Hour: YES ⏰")
        else:
            st.success("Peak Hour: NO ✅")

        # ================= SMART RECOMMENDATION =================
        st.markdown("### 🧠 Smart Recommendation")
        if traffic.startswith("High"):
            st.warning("Avoid travel now. Try after peak hours.")
        elif traffic.startswith("Moderate"):
            st.info("Traffic is manageable. Drive carefully.")
        else:
            st.success("Best time to travel. Smooth route.")

# ================= FOOTER =================
st.caption("🚦 AI Traffic Density Analyzer | Smart City Mini Project | By Mohit Kumar Singh")
