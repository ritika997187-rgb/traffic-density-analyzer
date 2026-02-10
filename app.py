import streamlit as st
import pandas as pd

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Traffic Density Analyzer",
    page_icon="🚦",
    layout="centered"
)

# ================= BLACK BACKGROUND =================
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

st.markdown("""
### 📌 Project Objective
Analyze traffic density using **date, time, location and weather**
to support better **traffic management and decision making**.
""")

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

# ================= WEATHER =================
st.subheader("🌦️ Weather Condition")

weather = st.selectbox(
    "Select Weather",
    ["Sunny ☀️", "Rainy 🌧️", "Foggy 🌫️"]
)

# ================= DATE & TIME =================
st.subheader("📅 Date & Time Input")

day = st.number_input(
    "Enter Day (1–31)",
    min_value=1,
    max_value=31,
    step=1
)

selected_time = st.time_input("Select Time")

# ================= ANALYZE BUTTON =================
if st.button("Analyze Traffic 🚗"):

    filtered = df[
        (df["Date"] == day) &
        (df["Time"] == selected_time)
    ]

    if filtered.empty:
        st.warning("❌ No data available for selected inputs")

    else:
        vehicles = int(filtered["CarCount"].values[0])
        day_name = filtered.iloc[0]["Day of the week"]
        hour = selected_time.hour

        # ================= OUTPUT =================
        st.markdown("### 📊 Traffic Analysis Result")

        st.info(f"📍 Location: {location}")
        st.info(f"🌦️ Weather: {weather}")
        st.info(f"📅 Day: {day_name}")
        st.info(f"⏰ Time: {selected_time}")
        st.info(f"🚗 Vehicle Count: {vehicles}")

        # ================= TRAFFIC LOGIC (WITH WEATHER) =================
        if (8 <= hour <= 10 or 17 <= hour <= 20) or "Rainy" in weather or "Foggy" in weather:
            traffic = "High Traffic 🔴"
            reasons = [
                "Peak hours or adverse weather",
                "Reduced visibility and slow movement"
            ]

        elif vehicles < 20 and "Sunny" in weather:
            traffic = "Low Traffic 🟢"
            reasons = [
                "Low vehicle density",
                "Clear weather conditions"
            ]

        else:
            traffic = "Moderate Traffic 🟡"
            reasons = [
                "Normal traffic flow",
                "Average weather impact"
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
        # ================= VOICE OUTPUT =================
st.markdown("### 🔊 Voice Traffic Alert")

voice_text = f"""
Traffic Analysis Result.
Location: {location}.
Weather: {weather}.
Traffic level is {traffic}.
"""

st.components.v1.html(
    f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{voice_text}");
    window.speechSynthesis.speak(msg);
    </script>
    """,
    height=0
)

        if "Rainy" in weather or "Foggy" in weather:
            st.warning("Poor weather detected. Drive slowly and maintain safe distance.")
        elif traffic.startswith("High"):
            st.warning("Avoid this route now. Try after peak hours.")
        elif traffic.startswith("Moderate"):
            st.info("Traffic is manageable. Drive carefully.")
        else:
            st.success("Best time to travel. Smooth and safe route.")

        # ================= GRAPH =================
        st.markdown("### 📈 Traffic Trend (Same Day)")

        day_data = df[df["Date"] == day].sort_values("Time")

        if not day_data.empty:
            st.line_chart(
                day_data.set_index("Time")["CarCount"]
            )
        else:
            st.warning("Not enough data to display graph")

# ================= FOOTER =================
st.markdown("---")
st.caption("🚦 Traffic Density Analyzer | Mini Project | By Mohit kumar Singh")
