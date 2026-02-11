import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
import time

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Traffic Density Analyzer",
    layout="centered"
)

# ================= STYLISH DARK UI =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #000000, #0f2027);
    color: white;
}
h1, h2, h3 {
    text-align: center;
}
div.stButton > button {
    background-color: #ff4b4b;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    padding: 0.5em 1em;
}
</style>
""", unsafe_allow_html=True)

st.markdown("# 🚦 AI Traffic Density Analyzer")

# ================= LOAD DATA =================
df = pd.read_csv("TrafficTwoMonth.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Time"] = pd.to_datetime(df["Time"]).dt.time

# ================= USER INPUT =================
st.markdown("## 📍 Location Details")

location = st.selectbox("Select Location", df["Location"].unique())
day = st.number_input("Enter Day (Date number)", 1, 31, 1)
selected_time = st.time_input("Select Time", datetime.now().time())
weather = st.selectbox("Select Weather", ["Clear", "Rainy", "Foggy"])

# ================= ANALYZE BUTTON =================
if st.button("🔍 Analyze Traffic"):

    with st.spinner("Analyzing traffic data... 🚀"):
        time.sleep(2)

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
            traffic_hindi = "भारी ट्रैफिक"
        elif vehicles < 20:
            traffic = "Low Traffic 🟢"
            traffic_hindi = "कम ट्रैफिक"
        else:
            traffic = "Moderate Traffic 🟡"
            traffic_hindi = "मध्यम ट्रैफिक"

        # ================= OUTPUT =================
        st.markdown("## 📊 Traffic Analysis Result")
        st.success(f"📍 Location: {location}")
        st.info(f"📅 Day: {day_name}")
        st.info(f"⏰ Time: {selected_time}")
        st.info(f"🌦️ Weather: {weather}")
        st.info(f"🚗 Vehicle Count: {vehicles}")
        st.markdown(f"### 🚦 {traffic}")

        # ================= GOOGLE MAP STYLE VIEW =================
        st.markdown("## 🗺️ Location Map View")
        map_data = pd.DataFrame({
            "lat": [28.6139],
            "lon": [77.2090]
        })
        st.map(map_data)

        # ================= AUTO VOICE (ENGLISH + HINDI) =================
        english_voice = f"""
        Traffic analysis result.
        Location is {location}.
        Today is {day_name}.
        Time is {selected_time}.
        Weather is {weather}.
        Traffic level is {traffic}.
        """

        hindi_voice = f"""
        ट्रैफिक विश्लेषण परिणाम।
        स्थान है {location}.
        आज है {day_name}.
        समय है {selected_time}.
        मौसम है {weather}.
        ट्रैफिक स्तर है {traffic_hindi}.
        """

        components.html(f"""
        <script>
        function speakText(text) {{
            var msg = new SpeechSynthesisUtterance(text);
            msg.lang = "en-IN";
            msg.rate = 0.9;
            msg.pitch = 1.1;
            msg.volume = 1;
            window.speechSynthesis.speak(msg);
        }}

        function speakHindi(text) {{
            var msg = new SpeechSynthesisUtterance(text);
            msg.lang = "hi-IN";
            msg.rate = 0.9;
            msg.pitch = 1.1;
            msg.volume = 1;
            window.speechSynthesis.speak(msg);
        }}

        window.speechSynthesis.cancel();
        speakText(`{english_voice}`);

        setTimeout(function() {{
            speakHindi(`{hindi_voice}`);
        }}, 6000);

        </script>
        """, height=0)

st.markdown("---")
st.caption("🚦 AI Traffic Density Analyzer | Smart City Project | By Mohit Kumar Singh")
