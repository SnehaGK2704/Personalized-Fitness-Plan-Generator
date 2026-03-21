from calendar import day_name
import re

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import create_tables
from email_utils import init_mail, generate_otp, send_otp
from auth import verify_user, register_user, update_profile
from model_api import query_model
from prompt_builder import build_prompt
import sqlite3, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fitplan_secret_key")

init_mail(app)
create_tables()

otp_store = {}  # {email: otp}

# ─── Auth ───────────────────────────────────────────────

@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        user = verify_user(email, password)
        if user:
            otp = generate_otp()
            otp_store[email] = otp
            send_otp(app, email, otp)
            session["pending_email"] = email
            return jsonify({"success": True, "redirect": url_for("verify_otp_login")})
        return jsonify({"success": False, "message": "Invalid credentials"})
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        try:
            register_user(email, password)
            otp = generate_otp()
            otp_store[email] = otp
            send_otp(app, email, otp)
            session["pending_email"] = email
            session["pending_name"] = name
            return jsonify({"success": True, "redirect": url_for("verify_otp_signup")})
        except Exception as e:
            return jsonify({"success": False, "message": "Email already registered"})
    return render_template("signup.html")


@app.route("/verify-otp-login", methods=["GET", "POST"])
def verify_otp_login():
    if request.method == "POST":
        data = request.get_json()
        otp_input = data.get("otp")
        email = session.get("pending_email")
        if otp_store.get(email) == otp_input:
            otp_store.pop(email, None)
            from database import get_db
            conn = get_db()
            user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
            conn.close()
            session["user_id"] = user[0]
            session["user_email"] = user[1]
            session["user_name"] = user[3] or "User"
            session.pop("pending_email", None)
            return jsonify({"success": True, "redirect": url_for("dashboard")})
        return jsonify({"success": False, "message": "Invalid OTP"})
    return render_template("otp.html", action="login")


@app.route("/verify-otp-signup", methods=["GET", "POST"])
def verify_otp_signup():
    if request.method == "POST":
        data = request.get_json()
        otp_input = data.get("otp")
        email = session.get("pending_email")
        if otp_store.get(email) == otp_input:
            otp_store.pop(email, None)
            from database import get_db
            conn = get_db()
            user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
            conn.close()
            session["user_id"] = user[0]
            session["user_email"] = user[1]
            session["user_name"] = session.get("pending_name", "User")
            session.pop("pending_email", None)
            session.pop("pending_name", None)
            return jsonify({"success": True, "redirect": url_for("profile_setup")})
        return jsonify({"success": False, "message": "Invalid OTP"})
    return render_template("otp.html", action="signup")


@app.route("/resend-otp", methods=["POST"])
def resend_otp():
    email = session.get("pending_email")
    if email:
        otp = generate_otp()
        otp_store[email] = otp
        send_otp(app, email, otp)
        return jsonify({"success": True})
    return jsonify({"success": False})


@app.route("/profile-setup", methods=["GET", "POST"])
def profile_setup():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        data = request.get_json()
        update_profile(
            session["user_id"],
            data.get("name"),
            data.get("age"),
            data.get("height"),
            data.get("weight")
        )
        session["user_name"] = data.get("name")
        return jsonify({"success": True, "redirect": url_for("dashboard")})
    return render_template("profile_setup.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ─── Dashboard ──────────────────────────────────────────

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    from database import get_db
    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE id=?",
        (session["user_id"],)
    ).fetchone()

    weight_logs = conn.execute(
        "SELECT * FROM weight_logs WHERE user_id=? ORDER BY log_date DESC LIMIT 10",
        (session["user_id"],)
    ).fetchall()

    plans = conn.execute(
        "SELECT * FROM workout_plans WHERE user_id=? ORDER BY created_at DESC LIMIT 3",
        (session["user_id"],)
    ).fetchall()

    # ✅ Activity progress
    progress = conn.execute(
        "SELECT activity, current_value, target_value, unit, deadline FROM activity_progress WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()

    # ✅ Overview data
    activities = conn.execute(
        "SELECT activity, current_value, deadline FROM activity_progress WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()

    total_steps = 0
    total_target = 0
    total_hours = 0

    for act in activities:
        target_text = act[2]
        value = act[1]

        if "steps" in target_text:
            total_steps += value
            total_target += int(target_text.split()[0])

        elif "hours" in target_text:
            total_hours += value

    total_steps = int(total_steps)
    total_target = int(total_target)
    total_hours = round(total_hours, 1)

    # ✅ GRAPH DATA (FIXED)
    from datetime import datetime, timedelta

    today = datetime.today()
    week_data = []

    logs = conn.execute("""
        SELECT current_value FROM activity_progress
        WHERE user_id=? 
    """, (session["user_id"],)).fetchall()

    total = sum([log[0] for log in logs])

    # simple variation for demo (so graph moves)
    for i in range(7):
        week_data.append(total * (0.7 + i * 0.05))

    # ✅ CONVERT TO SVG POINTS
    max_val = max(week_data) if max(week_data) > 0 else 1

    points = []
    points_list = points
    for i, val in enumerate(week_data):
        x = i * 100
        y = 60 - (val / max_val * 40)
        points.append(f"{x},{y}")

    svg_points = " ".join(points)

    conn.close()

    return render_template(
        "dashboard.html",
        user=user,
        weight_logs=weight_logs,
        plans=plans,
        progress=progress,
        total_steps=total_steps,
        total_target=total_target,
        total_hours=total_hours,
        svg_points=svg_points,
        points_list=points_list
    )


@app.route("/log-weight", methods=["POST"])
def log_weight():
    if "user_id" not in session:
        return jsonify({"success": False})
    data = request.get_json()
    from database import get_db
    conn = get_db()
    conn.execute(
        "INSERT INTO weight_logs(user_id, weight) VALUES(?,?)",
        (session["user_id"], data.get("weight"))
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# ─── Workout Plan ────────────────────────────────────────

@app.route("/workout-plan", methods=["GET", "POST"])
def workout_plan():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        data = request.get_json()

        from database import get_db
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE id=?",
            (session["user_id"],)
        ).fetchone()
        conn.close()

        prompt, bmi, bmi_status = build_prompt(
            name=user[3] or session["user_name"],
            gender=data.get("gender", "Not specified"),
            height=user[5] or 170,
            weight=user[6] or 70,
            goal=data.get("goal"),
            fitness_level=data.get("fitness_level"),
            equipment=data.get("equipment", [])
        )

        plan_text = query_model(prompt)

        # ✅ PARSE ACTIVITIES (FIXED)
        activities = []

        lines = plan_text.split("\n")
        current_name = None

        for line in lines:
            if "Activity:" in line:
                current_name = line.split("Activity:")[1].strip()

            elif "Target:" in line and current_name:
                target = line.split("Target:")[1].strip()

                activities.append((
                    current_name,
                    0,
                    100,
                    "",
                    target
                ))

                current_name = None

        # ✅ SAVE ACTIVITIES (NEW BLOCK — OUTSIDE LOOP)
        conn = get_db()

        conn.execute(
            "DELETE FROM activity_progress WHERE user_id=?",
            (session["user_id"],)
        )

        for act in activities:
            conn.execute("""
                INSERT INTO activity_progress(user_id, activity, current_value, target_value, unit, deadline)
                VALUES(?,?,?,?,?,?)
            """, (session["user_id"], *act))

        conn.commit()
        conn.close()

        # ✅ YOUR ORIGINAL INSERT (UNCHANGED)
        conn = get_db()
        conn.execute(
            "INSERT INTO workout_plans(user_id, goal, fitness_level, equipment, plan) VALUES(?,?,?,?,?)",
            (
                session["user_id"],
                data.get("goal"),
                data.get("fitness_level"),
                ", ".join(data.get("equipment", [])),
                plan_text
            )
        )
        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "plan": plan_text,
            "bmi": round(bmi, 2),
            "bmi_status": bmi_status
        })

    from database import get_db
    conn = get_db()
    plans = conn.execute(
        "SELECT * FROM workout_plans WHERE user_id=? ORDER BY created_at DESC",
        (session["user_id"],)
    ).fetchall()
    conn.close()

    return render_template("workout_plan.html", plans=plans)
@app.route("/analytics")
def analytics():
    if "user_id" not in session:
        return redirect(url_for("login"))

    from database import get_db
    conn = get_db()

    # Weight logs
    weight_logs = conn.execute(
        "SELECT weight, log_date FROM weight_logs WHERE user_id=? ORDER BY log_date ASC",
        (session["user_id"],)
    ).fetchall()

    # Total plans
    total_plans = conn.execute(
        "SELECT COUNT(*) FROM workout_plans WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()[0]

    # Active days
    active_days = conn.execute(
        "SELECT COUNT(DISTINCT log_date) FROM weight_logs WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()[0]

    conn.close()

    return render_template(
        "analytics.html",
        weight_logs=weight_logs,
        total_plans=total_plans,
        active_days=active_days
    )

@app.route("/schedule")
def schedule():
    if "user_id" not in session:
        return redirect(url_for("login"))

    from database import get_db
    conn = get_db()

    # ✅ get latest plan
    plan = conn.execute(
        "SELECT plan FROM workout_plans WHERE user_id=? ORDER BY created_at DESC LIMIT 1",
        (session["user_id"],)
    ).fetchone()

    rows = conn.execute(
    "SELECT day, completed FROM workout_schedule WHERE user_id=?",
    (session["user_id"],)
    ).fetchall()

    schedule = {row[0]: row[1] for row in rows}

    conn.close()
    import re

    days = []
    day_plans = {}

    if plan:
        text = plan[0]

    # split using Day X:
    parts = re.split(r'Day\s*(\d+):', text)

    # parts structure:
    # ['', '1', 'content...', '2', 'content...', ...]

    for i in range(1, len(parts), 2):
        day_num = parts[i]
        content = parts[i + 1].strip()

        day_name = f"Day {day_num}"

        days.append(day_name)
        day_plans[day_name] = content
    total_days = len(days)
    completed_days = sum(schedule.values()) if schedule else 0

    progress_percent = int((completed_days / total_days) * 100) if total_days else 0
                

    return render_template("schedule.html", days=days, 
                           day_plans=day_plans, 
                           full_plan=plan[0] if plan else "",
                           schedule=schedule,total_days=total_days,
                            completed_days=completed_days,
                            progress_percent=progress_percent)

@app.route("/toggle-day", methods=["POST"])
def toggle_day():
    if "user_id" not in session:
        return jsonify({"success": False})

    data = request.get_json()
    day = data.get("day").strip().replace(":", "")

    from database import get_db
    conn = get_db()

    existing = conn.execute(
    "SELECT completed FROM workout_schedule WHERE user_id=? AND day=?",
    (session["user_id"], day)
).fetchone()

    if existing:
        current = existing[0]   # this is completed
        new_val = 0 if current == 1 else 1
        conn.execute(
            "UPDATE workout_schedule SET completed=? WHERE user_id=? AND day=?",
            (new_val, session["user_id"], day)
        )
    else:
        conn.execute(
            "INSERT INTO workout_schedule(user_id, day, completed) VALUES(?,?,1)",
            (session["user_id"], day)
        )

    conn.commit()
    conn.close()

    return jsonify({"success": True})

#-----------------------------PROGRESS UPDATE ENDPOINT-----------------------------
@app.route("/update-progress", methods=["POST"])
def update_progress():
    if "user_id" not in session:
        return jsonify({"success": False})

    data = request.get_json()

    from database import get_db
    conn = get_db()

    conn.execute("""
        UPDATE activity_progress
        SET current_value = current_value + ?
        WHERE user_id=? AND activity=?
    """, (
        float(data["value"]),
        session["user_id"],
        data["activity"]
    ))

    conn.commit()
    conn.close()

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
