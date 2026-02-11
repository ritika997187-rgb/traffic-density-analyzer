import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
import time

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Traffic Density Analyzer", page_icon="🚦")

# ================= STYLISH DARK UI =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #000000, #1a1a1a);
    color: white;
}
h1, h2, h3 {
    text-align: center;
    color: #00ffcc;
}
div.stButton > button {
    background: linear-gradient(90deg, #00ffcc, #00b3ff);
    color: black;
    font-weight: bold;
    border-radius: 12px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.title("🚦 Smart Traffic Density Analyzer")

# ================= LOAD DATA =================
df = pd.read_csv("TrafficTwoMonth.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Time"] = pd.to_datetime(df["Time"]).dt.time

# If no latitude/longitude in dataset, create demo ones
if "Latitude" not in df.columns:
    df["Latitude"] = 28.6139   # Delhi demo
    df["Longitude"] = 77.2090

# ================= INPUT =================
st.markdown("## 📍 Enter Traffic Details")

location = st.selectbox("Select Location", df["Location"].unique())
day = st.number_input("Enter Day", 1, 31, 1)
selected_time = st.time_input("Select Time", datetime.now().time())
weather = st.selectbox("Select Weather", ["Clear", "Rainy", "Foggy"])

# ================= ANALYZE =================
if st.button("🚀 Analyze Traffic"):

    # Animated Loading
    with st.spinner("🔄 Analyzing traffic data..."):
        time.sleep(2)

    filtered = df[
        (df["Location"] == location) &
        (df["Date"].dt.day == day) &
        (df["Time"] == selected_time)
    ]

    if filtered.empty:
        st.warning("No data available.")
    else:
        vehicles = int(filtered.iloc[0]["CarCount"])
        day_name = filtered.iloc[0]["Day of the Week"]
        lat = filtered.iloc[0]["Latitude"]
        lon = filtered.iloc[0]["Longitude"]
        hour = selected_time.hour

        if (8 <= hour <= 10) or (17 <= hour <= 20) or weather in ["Rainy", "Foggy"]:
            traffic = "High Traffic 🔴"
        elif vehicles < 20:
            traffic = "Low Traffic 🟢"
        else:
            traffic = "Moderate Traffic 🟡"

        # ================= RESULT =================
        st.success(f"""
📍 Location: {location}  
📅 Day: {day_name}  
⏰ Time: {selected_time}  
🌦️ Weather: {weather}  
🚗 Vehicles: {vehicles}  
🚦 Traffic: {traffic}
""")

        # ================= GOOGLE MAP VIEW =================
        st.markdown("## 🗺 Live Location Map")
        map_df = pd.DataFrame({
            "lat": [lat],
            "lon": [lon]
        })
        st.map(map_df)

        # ================= AUTO VOICE ENGLISH + HINDI =================
        english_voice = (
            f"Traffic analysis result. "
            f"Location is {location}. "
            f"Day is {day_name}. "
            f"Time is {selected_time}. "
            f"Weather is {weather}. "
            f"Traffic level is {traffic}."
        )

        hindi_voice = (
            f"ट्रैफिक विश्लेषण परिणाम। "
            f"स्थान है {location}. "
            f"दिन है {day_name}. "
            f"समय है {selected_time}. "
            f"मौसम है {weather}. "
            f"ट्रैफिक स्तर है {traffic}."
        )

        components.html(
            f"""
            <script>
                function speakText(text, lang) {{
                    var msg = new SpeechSynthesisUtterance(text);
                    msg.lang = lang;
                    msg.rate = 0.9;
                    msg.pitch = 1.1;
                    window.speechSynthesis.speak(msg);
                }}

                window.speechSynthesis.cancel();

                speakText("{english_voice}", "en-IN");

                setTimeout(function() {{
                    speakText("{hindi_voice}", "hi-IN");
                }}, 5000);
            </script>
            """,
            height=0
        )

st.markdown("---")
st.caption("🚦 AI Traffic Density Analyzer | Smart City Project")
st.caption("🚦 Traffic Density Analyzer | Mini Project | By Mohit kumar Singh")
