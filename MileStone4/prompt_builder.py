def calculate_bmi(weight, height):
    height_m = height / 100
    return weight / (height_m ** 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal Weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def build_prompt(name, gender, height, weight, goal, fitness_level, equipment):

    bmi = calculate_bmi(weight, height)
    bmi_status = bmi_category(bmi)

    equipment_list = ", ".join(equipment) if equipment else "No Equipment"
    if fitness_level.lower() == "beginner":
        total_days = 7
    elif fitness_level.lower() == "intermediate":
        total_days = 15
    else:
        total_days = 21
    prompt = f"""
You are a certified professional fitness trainer.

Create a workout plan for **{total_days} days (Day 1 to Day {total_days})**.
USER PROFILE
Name: {name}
Gender: {gender}
Height: {height} cm
Weight: {weight} kg
BMI: {bmi:.2f} ({bmi_status})
Goal: {goal}
Fitness Level: {fitness_level}
Available Equipment: {equipment_list}

Also suggest exactly 3 fitness activity goals in this STRICT format:

Activity: <name>
Target: <number + unit>

Rules:
- ONLY output Activity and Target (no extra text)
- ALWAYS use weekly targets
- Use correct units:
  • Yoga / Stretching → hours/week
  • Strength training → hours/week
  • Cardio → km/week
  • Walking / Steps → steps/week
- Do NOT include reasons or explanations
- Do NOT include ranges (only one number)

Example:

Activity: Yoga
Target: 3 hours/week

Activity: Running
Target: 12 km/week

Activity: Walking
Target: 56000 steps/week

INSTRUCTIONS

1. Create a workout plan for **5 days (Day 1 to Day 5)**.
2. Each day must target a **specific muscle group**.
3. Each day must contain **4 exercises**.
4. For each exercise include:
   - Exercise name
   - Sets
   - Reps
   - Rest time
5. Adjust difficulty based on **fitness level and BMI category**.
6. Avoid unsafe or extremely advanced exercises for beginners.
7. Exercises must be realistic and can be performed at home or gym based on available equipment.

OUTPUT FORMAT (follow this strictly)

Day 1: <Muscle Group>

Exercise: <Exercise Name>
Sets: X
Reps: X
Rest: X seconds

Exercise: <Exercise Name>
Sets: X
Reps: X
Rest: X seconds

Repeat until Day {total_days}.

IMPORTANT:
Return ONLY the workout plan.
Do NOT include explanations or extra text.
"""

    return prompt, bmi, bmi_status