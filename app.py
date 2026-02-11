import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Traffic Density Analyzer",
    layout="centered"
)

# ================= DARK STYLISH UI =================
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
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown("# 🚦 AI Traffic Density Analyzer")

# ================= LOAD DATA =================
df = pd.read_csv("TrafficTwoMonth.csv")

df["Time"] = pd.to_datetime(df["Time"]).dt.time

# ================= INPUT =================
st.markdown("### ⏰ Select Time")

selected_time = st.time_input(
    "Choose Time",
    datetime.now().time()
)

# ================= BUTTON =================
if st.button("🔍 Analyze Traffic"):

    filtered = df[df["Time"] == selected_time]

    if filtered.empty:
        st.warning("No data found for selected time.")
    else:
        row = filtered.iloc[0]

        total = row["Total"]
        traffic_status = row["Traffic Situation"]
        day_name = row["Day of the week"]

        # ================= OUTPUT =================
        st.markdown("### 📊 Traffic Analysis")

        st.info(f"📅 Day: {day_name}")
        st.info(f"🚗 Total Vehicles: {total}")
        st.success(f"🚦 Traffic Condition: {traffic_status.upper()}")

        # ================= SMART MESSAGE =================
        if traffic_status.lower() == "heavy":
            message_en = "Traffic is heavy. Please avoid travelling now."
            message_hi = "ट्रैफिक बहुत ज्यादा है। अभी यात्रा करने से बचें।"
        elif traffic_status.lower() == "normal":
            message_en = "Traffic is normal. You can travel safely."
            message_hi = "ट्रैफिक सामान्य है। आप सुरक्षित यात्रा कर सकते हैं।"
        else:
            message_en = "Traffic is low. Best time to travel."
            message_hi = "ट्रैफिक कम है। यात्रा के लिए सबसे अच्छा समय।"

        st.markdown("### 🧠 Smart Recommendation")
        st.write(message_en)
        st.write(message_hi)

        # ================= AUTO FEMALE VOICE =================
        components.html(f"""
        <script>
        function speak(text, lang) {{
            var msg = new SpeechSynthesisUtterance(text);
            msg.lang = lang;
            msg.rate = 0.9;

            var voices = speechSynthesis.getVoices();
            for (var i = 0; i < voices.length; i++) {{
                if (voices[i].lang.includes(lang) && voices[i].name.toLowerCase().includes("female")) {{
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

st.markdown("---")
st.caption("🚦 AI Traffic Density Analyzer | Smart City Mini Project | By Mohit Kumar Singh")
