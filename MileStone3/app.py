from flask import Flask, render_template, request, redirect, session
import sqlite3

from database import create_tables
from auth import verify_user, register_user, update_profile
from email_utils import init_mail, generate_otp, send_otp

from prompt_builder import build_prompt
from model_api import query_model

app = Flask(__name__)
app.secret_key = "fitplan_secret_key"

# Initialize mail
init_mail(app)

# Create database tables
create_tables()


# ---------------- LOGIN ----------------

@app.route("/", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = verify_user(email, password)

        if user:

            otp = generate_otp()

            session["otp"] = otp
            session["temp_user"] = user

            send_otp(app, email, otp)

            return redirect("/verify-otp")

        else:
            error = "Invalid email or password"

    return render_template("login.html", error=error)


# ---------------- OTP VERIFICATION ----------------

@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():

    error = None

    if request.method == "POST":

        user_otp = request.form["otp"]

        if user_otp == session.get("otp"):

            user = session.get("temp_user")

            session["user_id"] = user[0]
            session["name"] = user[3]

            if user[3] is None or user[4] is None or user[5] is None or user[6] is None:
                return redirect("/setup-profile")

            return redirect("/home")

        else:
            error = "Invalid OTP"

    return render_template("verify_otp.html", error=error)


# ---------------- SIGNUP ----------------

@app.route("/signup", methods=["GET", "POST"])
def signup():

    error = None

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        try:
            register_user(email, password)
            return redirect("/")

        except sqlite3.IntegrityError:
            error = "Email already registered. Please login."

    return render_template("signup.html", error=error)


# ---------------- PROFILE SETUP ----------------

@app.route("/setup-profile", methods=["GET", "POST"])
def setup_profile():

    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        height = request.form["height"]
        weight = request.form["weight"]

        update_profile(session["user_id"], name, age, height, weight)

        session["name"] = name

        return redirect("/home")

    return render_template("setup_profile.html")


# ---------------- HOME DASHBOARD ----------------

@app.route("/home")
def home():

    if "user_id" not in session:
        return redirect("/")

    return render_template("index.html", name=session["name"])


# ---------------- GENERATE WORKOUT ----------------

@app.route("/generate", methods=["POST"])
def generate():

    if "user_id" not in session:
        return redirect("/")

    name = session["name"]

    age = request.form["age"]
    gender = request.form["gender"]
    height = request.form["height"]
    weight = request.form["weight"]
    goal = request.form["goal"]
    fitness_level = request.form["fitness_level"]

    equipment = request.form.getlist("equipment")

    prompt, bmi, bmi_status = build_prompt(
        name=name,
        gender=gender,
        height=float(height),
        weight=float(weight),
        goal=goal,
        fitness_level=fitness_level,
        equipment=equipment
    )

    prompt += f"\nAge: {age}"

    plan = query_model(prompt)

    return render_template(
        "result.html",
        plan=plan,
        bmi=bmi,
        bmi_status=bmi_status
    )


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)