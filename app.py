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
df["Time"] = pd.to_datetime(df["Time"], format="%I:%M:%S %p").dt.time

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
        day_name = filtered.iloc[0]["Day of the week"]
        hour = selected_time.hour

        # ================= WEATHER EFFECT =================
        if weather == "Rainy":
            vehicles += 10
        elif weather == "Foggy":
            vehicles += 5
        elif weather == "Stormy":
            vehicles += 15

        # ================= OUTPUT =================
        st.markdown("### 📊 Traffic Analysis")

        st.info(f"📍 Location: {location}")
        st.info(f"📅 Day: {day_name}")
        st.info(f"⏰ Time: {selected_time}")
        st.info(f"🚗 Vehicle Count (Adjusted): {vehicles}")
        st.info(f"🌦️ Weather: {weather}")

        # ================= TRAFFIC LOGIC =================
        if 8 <= hour <= 10 or 17 <= hour <= 20:
            traffic = "High Traffic 🔴"
            reasons = [
                "Office peak hours",
                "High vehicle movement"
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
                "Normal traffic flow"
            ]

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

        # ================= GRAPH =================
        st.markdown("### 📈 Traffic Trend (Same Day)")
        day_data = df[df["Date"] == day].sort_values("Time")
        st.line_chart(day_data.set_index("Time")["CarCount"])
        st.caption("🚦 Traffic Density Analyzer | Mini Project | By Mohit kumar Singh")
