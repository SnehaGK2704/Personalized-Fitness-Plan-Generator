import streamlit as st
from prompt_builder import build_prompt

st.set_page_config(page_title="FitPlan AI", layout="centered")

# ---------------- TITLE ---------------- #

st.title("🏋️‍♀️ FitPlan AI")
st.markdown("### Your Personal AI Fitness Trainer")
st.markdown("---")

# ---------------- CUSTOM STYLING ---------------- #

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

# ---------------- INPUT ---------------- #

name = st.text_input("Enter Your Name")
age = st.number_input("Age", min_value=10, max_value=100, step=1)
gender = st.radio("Gender", ["Male", "Female"])
height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0)
weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0)

goal = st.selectbox(
    "Fitness Goal",
    ["Build Muscle", "Lose Weight", "Improve Endurance", "General Fitness"]
)

fitness_level = st.radio(
    "Fitness Level",
    ["Beginner", "Intermediate", "Advanced"]
)

equipment = st.multiselect(
    "Available Equipment",
    [
        "No Equipment", "Dumbbells", "Barbell",
        "Pull-up Bar", "Resistance Bands",
        "Treadmill", "Kettlebells", "Full Gym"
    ]
)

# ---------------- GENERATE ---------------- #

if st.button("Generate Workout Plan"):

    if height > 0 and weight > 0 and age > 0:

        prompt, bmi, bmi_status = build_prompt(
            name=name,
            gender=gender,
            height=height,
            weight=weight,
            goal=goal,
            fitness_level=fitness_level,
            equipment=equipment,
        )

        prompt += f"\nAge: {age} years\nAdjust intensity appropriately."

        # Store in session_state for next page
        st.session_state.prompt = prompt
        st.session_state.bmi = bmi
        st.session_state.bmi_status = bmi_status

        st.switch_page("pages/results.py")

    else:
        st.warning("Please enter valid age, height, and weight.")