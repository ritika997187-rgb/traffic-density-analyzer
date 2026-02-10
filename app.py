import streamlit as st
import pandas as pd
from datetime import datetime

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Traffic Density Analyzer",
    page_icon="🚦",
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

# ================= TITLE =================
st.title("🚦 Traffic Density Analyzer")

# ================= LOAD DATA =================
df = pd.read_csv("TrafficTwoMonth.csv")

# ================= CLEAN DATA =================
df["Date"] = df["Date"].astype(int)
df["Time"] = pd.to_datetime(df["Time"], format="%I:%M:%S %p").dt.time

# ================= LOCATION =================
st.subheader("📍 Location Details")

locations = [
    "MG Road",
    "Ring Road",
    "Market Area",
    "Highway",
    "Bus Stand",
    "Railway Station",
    "School Zone",
    "Hospital Area",
    "Industrial Area",
    "Residential Colony",
    "City Center"
]

location = st.selectbox("Select Location", locations)

# ================= DATE & TIME =================
day = st.number_input(
    "📅 Enter Day (1–31)",
    min_value=1,
    max_value=31,
    step=1
)

selected_time = st.time_input("⏰ Select Time")

# ================= ANALYZE BUTTON =================
if st.button("Analyze Traffic 🚗"):

    filtered = df[
        (df["Date"] == day) &
        (df["Time"] == selected_time)
    ]

    if filtered.empty:
        st.warning("❌ No data available for selected day & time")

    else:
        vehicles = int(filtered["CarCount"].values[0])
        day_name = filtered.iloc[0]["Day of the week"]
        hour = selected_time.hour

        # ================= OUTPUT =================
        st.markdown("### 📊 Traffic Analysis")

        st.info(f"📍 Location: {location}")
        st.info(f"📅 Day: {day_name}")
        st.info(f"⏰ Time: {selected_time}")
        st.info(f"🚗 Vehicle Count: {vehicles}")

        # ================= TRAFFIC LOGIC =================
        if 8 <= hour <= 10 or 17 <= hour <= 20:
            traffic = "High Traffic 🔴"
            reasons = [
                "Office peak hours",
                "High vehicle frequency"
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

        # ================= TRAFFIC LEVEL =================
        st.markdown("### 🚦 Traffic Level")
        st.success(traffic)

        st.markdown("**Reason:**")
        for r in reasons:
            st.write(f"• {r}")

        # ================= PEAK HOUR =================
        st.markdown("### ⏰ Peak Hour Indicator")
        if 8 <= hour <= 10 or 17 <= hour <= 20:
            st.error("Peak Hour: YES ⏱️")
        else:
            st.success("Peak Hour: NO ✅")

        # ================= SMART RECOMMENDATION =================
        st.markdown("### 🧠 Smart Recommendation")

        if traffic.startswith("High"):
            st.warning("Avoid this route now. Try after peak hours.")
        elif traffic.startswith("Moderate"):
            st.info("Traffic is manageable. Drive carefully.")
        else:
            st.success("Best time to travel. Smooth and safe route.")

        # ================= GRAPH =================
        st.markdown("### 📈 Traffic Trend (Same Day)")

        day_data = df[df["Date"] == day].sort_values("Time")
        st.line_chart(
            day_data.set_index("Time")["CarCount"]
)
