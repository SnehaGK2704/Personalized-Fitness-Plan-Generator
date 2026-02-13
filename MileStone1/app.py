import streamlit as st
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

    /* Input fields */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        background-color: #1e1e2f !important;
        color: white !important;
        border-radius: 10px !important;
    }

    textarea, input {
        color: white !important;
    }

    /* Button */
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

    /* JSON block */
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

    /* Input fields */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        background-color: white !important;
        border-radius: 10px !important;
    }

    /* Button */
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

    /* JSON block */
    .stJson {
        background-color: #f1f5f9 !important;
        border-radius: 12px;
    }
}

</style>
""", unsafe_allow_html=True)



st.set_page_config(page_title="FitPlan AI", page_icon="🏋️", layout="wide")

# ---------------- SESSION STATE ----------------
if "profile_generated" not in st.session_state:
    st.session_state.profile_generated = False
if "profile_data" not in st.session_state:
    st.session_state.profile_data = {}

# ---------------- LAYOUT ----------------
col1, col2 = st.columns([1.2, 1])

# ================= LEFT SIDE =================
with col1:
    st.header("🧍 Your Fitness Profile")

    st.subheader("👤 Personal Information")
    name = st.text_input("Name *")
    height_cm = st.number_input("Height (cm) *", min_value=0.0)
    weight_kg = st.number_input("Weight (kg) *", min_value=0.0)

    st.subheader("🎯 Fitness Goal")
    goal = st.selectbox(
        "Select your Goal",
        ["Build Muscle", "Weight Loss", "Strength Gain", "Abs Building", "Flexibility"]
    )

    st.subheader("🏋️ Available Equipment")
    equipment = st.multiselect(
        "Select available equipment",
        [
            "Dumbbells",
            "Resistance Bands",
            "Yoga Mat",
            "Treadmill",
            "Cycle",
            "Skipping Rope",
            "Pullup Bar",
            "No Equipment"
        ]
    )

    st.subheader("📊 Fitness Level")
    fitness_level = st.radio(
        "Select your fitness level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    generate = st.button("🚀 Generate Plan")

# ---------------- BMI FUNCTIONS ----------------
def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi <= 24.9:
        return "Normal"
    elif 25 <= bmi <= 29.9:
        return "Overweight"
    else:
        return "Obese"

# ---------------- PROCESS ----------------
if generate:
    if name.strip() == "" or height_cm <= 0 or weight_kg <= 0:
        st.error("⚠️ Please fill all required fields correctly.")
        st.session_state.profile_generated = False
    else:
        bmi = calculate_bmi(height_cm, weight_kg)
        category = bmi_category(bmi)

        st.session_state.profile_data = {
            "Name": name,
            "Height (cm)": height_cm,
            "Weight (kg)": weight_kg,
            "BMI": bmi,
            "BMI Category": category,
            "Goal": goal,
            "Equipment": equipment,
            "Fitness Level": fitness_level
        }

        st.session_state.profile_generated = True

# ================= RIGHT SIDE =================
with col2:
    st.header("📋 Profile Summary")

    if st.session_state.profile_generated:
        st.success("Profile saved")
        st.json(st.session_state.profile_data)
