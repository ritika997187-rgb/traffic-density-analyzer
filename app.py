import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Traffic Density Analyzer",
    layout="centered"
)

# ================= STYLISH DARK UI =================
st.markdown("""
<style>
.stApp {
    background-color: #000000;
    color: white;
}
h1, h2, h3 {
    text-align: center;
}
.stButton>button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size:18px;
}
</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown("# 🚦 AI Traffic Density Analyzer")

# ================= LOAD DATA =================
df = pd.read_csv("TrafficTwoMonth.csv")
df["Time"] = pd.to_datetime(df["Time"]).dt.time

# ================= INPUT SECTION =================
st.markdown("## 📍 Location Details")

# Manual Locations (since CSV doesn't have it)
location = st.selectbox(
    "Select Location",
    ["Main Road", "City Center", "Highway", "Market Area"]
)

weather = st.selectbox(
    "Select Weather",
    ["Clear ☀️", "Rainy 🌧️", "Foggy 🌫️"]
)

selected_time = st.time_input(
    "Select Time",
    datetime.now().time()
)

# ================= ANALYZE BUTTON =================
if st.button("🔍 Analyze Traffic"):

    filtered = df[df["Time"] == selected_time]

    if filtered.empty:
        st.warning("No data found for selected time.")
    else:
        row = filtered.iloc[0]

        total = row["Total"]
        traffic_status = row["Traffic Situation"]
        day_name = row["Day of the week"]

        # Extra logic for weather
        if "Rainy" in weather or "Foggy" in weather:
            traffic_status = "Heavy"

        # ================= OUTPUT =================
        st.markdown("## 📊 Traffic Analysis Result")

        st.info(f"📍 Location: {location}")
        st.info(f"📅 Day: {day_name}")
        st.info(f"⏰ Time: {selected_time}")
        st.info(f"🌦️ Weather: {weather}")
        st.info(f"🚗 Total Vehicles: {total}")

        if traffic_status.lower() == "heavy":
            st.error("🚦 Traffic: HEAVY 🔴")
            message_en = "Traffic is heavy. Please avoid travelling now."
            message_hi = "ट्रैफिक बहुत ज्यादा है। कृपया अभी यात्रा करने से बचें।"

        elif traffic_status.lower() == "normal":
            st.warning("🚦 Traffic: NORMAL 🟡")
            message_en = "Traffic is normal. Drive carefully."
            message_hi = "ट्रैफिक सामान्य है। सावधानी से वाहन चलाएं।"

        else:
            st.success("🚦 Traffic: LOW 🟢")
            message_en = "Traffic is low. Best time to travel."
            message_hi = "ट्रैफिक कम है। यात्रा के लिए सबसे अच्छा समय।"

        # ================= AUTO FEMALE VOICE =================
        components.html(f"""
        <script>
        function speak(text, lang) {{
            var msg = new SpeechSynthesisUtterance(text);
            msg.lang = lang;
            msg.rate = 0.9;
            msg.pitch = 1.2;

            var voices = speechSynthesis.getVoices();
            for (var i = 0; i < voices.length; i++) {{
                if (voices[i].lang.includes(lang)) {{
                    msg.voice = voices[i];
                    break;
                }}
            }}

            speechSynthesis.speak(msg);
        }}

        speechSynthesis.cancel();
        speak("{message_en}", "en-IN");

        setTimeout(function() {{
            speak("{message_hi}", "hi-IN");
        }}, 4000);
        </script>
        """, height=0)

# ================= FOOTER =================
st.markdown("---")
st.caption("🚦 AI Traffic Density Analyzer | Smart City Mini Project | By Mohit Kumar Singh")
