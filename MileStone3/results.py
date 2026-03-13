import streamlit as st
from model_api import query_model

st.set_page_config(page_title="Workout Plan", layout="centered")
st.markdown("""
<style>

/* ===============================
   GLOBAL SMOOTHNESS
================================= */
* {
    transition: background 0.3s ease, color 0.3s ease;
}

/* ===============================
   🌙 DARK MODE – Violet Teal
================================= */
@media (prefers-color-scheme: dark) {

    .stApp {
        background: linear-gradient(135deg, #2b1e4a, #243b55, #1b998b);
        color: #ffffff;
    }

    h1, h2, h3, h4, h5, h6, label, span, p {
        color: #ffffff !important;
    }

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        background-color: #1e1e2f !important;
        color: white !important;
        border-radius: 10px !important;
    }

    textarea, input {
        color: white !important;
    }

    .stButton > button {
        background: linear-gradient(to right, #9d4edd, #1b998b);
        color: white;
        border-radius: 12px;
        height: 50px;
        font-weight: 600;
        border: none;
    }

    .stButton > button:hover {
        opacity: 0.9;
    }

    .stJson {
        background-color: #0f172a !important;
        border-radius: 12px;
    }
}

/* ===============================
   ☀️ LIGHT MODE – Aqua Blue
================================= */
@media (prefers-color-scheme: light) {

    .stApp {
        background: linear-gradient(135deg, #e0f7fa, #b2ebf2, #80deea);
        color: #1a1a1a;
    }

    h1, h2, h3, h4, h5, h6, label, span, p {
        color: #1a1a1a !important;
    }

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        background-color: white !important;
        border-radius: 10px !important;
    }

    .stButton > button {
        background: linear-gradient(to right, #00b4d8, #0077b6);
        color: white;
        border-radius: 12px;
        height: 50px;
        font-weight: 600;
        border: none;
    }

    .stButton > button:hover {
        opacity: 0.9;
    }

    .stJson {
        background-color: #f1f5f9 !important;
        border-radius: 12px;
    }
}

</style>
""", unsafe_allow_html=True)


st.title("📋 Your Personalized Workout Plan")
st.markdown("---")

if "prompt" not in st.session_state:
    st.warning("No workout data found. Please generate a plan first.")
    st.stop()

with st.spinner("Generating your personalized plan..."):
    response = query_model(st.session_state.prompt)

st.markdown(response)

bmi = st.session_state.bmi
bmi_status = st.session_state.bmi_status

if bmi_status == "Normal Weight":
    st.success(f"Calculated BMI: {bmi:.2f} ({bmi_status})")
elif bmi_status == "Underweight":
    st.info(f"Calculated BMI: {bmi:.2f} ({bmi_status})")
else:
    st.warning(f"Calculated BMI: {bmi:.2f} ({bmi_status})")

if st.button("⬅ Back to Home"):
    st.switch_page("app.py")