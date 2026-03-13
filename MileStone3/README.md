# FitPlan AI – Personalized Fitness Plan Generator

## Milestone 3: Login System with OTP Verification

FitPlan AI is a web application designed to generate personalized fitness plans using artificial intelligence. The application collects user fitness information and produces structured workout plans tailored to individual goals and physical characteristics.

This milestone focuses on implementing a **secure login system with database connectivity and OTP verification** using the **Flask web framework**.

---

# Project Objective

The objective of this milestone is to implement a **secure authentication system** that allows users to:

* Register using their email and password
* Log in using stored credentials
* Verify their identity using a **6-digit OTP sent via email**
* Access the application dashboard only after successful OTP verification

The system ensures that only authenticated users can generate personalized fitness plans.

---

# Technologies Used

### Backend

Flask (Python Web Framework)

### Database

SQLite

### Email Service

Flask-Mail (for sending OTP)

### Frontend

HTML, CSS, JavaScript, Jinja2 Templates

### AI Integration

Prompt engineering and model API integration for generating personalized workout plans.

---

# Features Implemented in Milestone 3

## 1. User Signup

Users can register by providing:

* Email ID
* Password

The credentials are stored securely in the SQLite database.

---

## 2. Login System

The login system verifies user credentials by checking the entered email and password against the stored records in the database.

---

## 3. OTP Generation

After successful login, the system generates a **6-digit One-Time Password (OTP)**.

Example:

```id="otpgen"
otp = random.randint(100000, 999999)
```

---

## 4. OTP Email Verification

The generated OTP is sent to the user's registered email using **Flask-Mail**.

Users must enter the OTP to complete the login process.

---

## 5. Secure Dashboard Access

Users can only access the application dashboard after successful OTP verification. Unauthorized users are redirected to the login page.

---

# System Workflow

1. User signs up with email and password.
2. User credentials are stored in the database.
3. User logs in using registered credentials.
4. A 6-digit OTP is generated.
5. OTP is sent to the user's email.
6. User enters the OTP on the verification page.
7. If the OTP is correct, access to the dashboard is granted.
8. The user can generate a personalized fitness plan.

---

# Folder Structure

```id="fsstruct"
FitPlan-AI/
└── Milestone3/
    ├── app.py
    ├── database.py
    ├── auth.py
    ├── email_utils.py
    ├── requirements.txt
    ├── README.md
    └── screenshots/
```

---

# File Description

### app.py

Main Flask application containing routes for login, signup, OTP verification, dashboard access, and workout plan generation.

### database.py

Handles database connection and table creation for storing user credentials.

### auth.py

Contains authentication logic including:

* Registering users
* Verifying login credentials
* Updating user profiles

### email_utils.py

Responsible for:

* OTP generation
* Sending OTP emails via Flask-Mail.

### requirements.txt

Lists all Python dependencies required to run the application.

### screenshots/

Contains screenshots demonstrating the working of the application.

---

# Screenshots

Click the links below to view the screenshots of the application.

Login Page
(Screenshots/loginPage.png)

Signup Page
(Screenshots/signupPage.png)

OTP Verification Page
(Screenshots/otp_verification.png)

Dashboard
(Screenshots/mainPage.png)


---

# Running the Application Locally

### Clone the Repository

```id="clonecmd"
git clone https://github.com/YOUR_USERNAME/FitPlan-AI-Personalized-Fitness-Plan-Generator.git
```

---

### Navigate to the Project Folder

```id="navcmd"
cd FitPlan-AI/Milestone3
```

---

### Install Dependencies

```id="instcmd"
pip install -r requirements.txt
```

---

### Run the Flask Application

```id="runflaskcmd"
python app.py
```

---

### Open in Browser

```id="browsercmd"
http://127.0.0.1:5000
```

---

# Future Improvements

* Password hashing for stronger security
* Multi-factor authentication
* Fitness progress tracking
* Nutrition and diet recommendation system
* Mobile responsive UI improvements

---

# Author

Sneha G Kudur
FitPlan AI – Personalized Fitness Plan Generator
Milestone 3 Implementation

