# FitPlan AI – Personalized Fitness Plan Generator

## Milestone 4: Application Finalization & Deployment

FitPlan AI is a web application designed to generate personalized workout plans using artificial intelligence. The application collects user fitness information and produces structured workout plans tailored to individual goals and physical characteristics.

This milestone focuses on finalizing the application, improving user experience, integrating the AI model using NVIDIA API (free endpoint), and preparing the project for deployment.

---

# Project Objective

The objective of this milestone is to build a complete end-to-end system that allows users to:

* Register and securely authenticate using OTP verification  
* Log in and access a personalized dashboard  
* Provide fitness-related inputs  
* Generate AI-powered workout plans  
* View structured and readable fitness plans  

The system ensures a smooth, secure, and user-friendly experience.

---

# Technologies Used

### Backend  
Flask (Python Web Framework)

### Database  
SQLite

### Email Service  
Flask-Mail (for OTP verification)

### Frontend  
HTML, CSS, JavaScript, Jinja2 Templates

### AI Integration  
NVIDIA API (Free Endpoint)

### Visualization  
Chart.js

---

# Features Implemented in Milestone 4

## 1. User Authentication System

* User Signup with email and password  
* Secure Login system  
* OTP generation and verification  
* Resend OTP functionality  

---

## 2. Input Validation

Validation implemented for:

* Age  
* Height  
* Weight  
* Required fitness fields  

---

## 3. AI Workout Plan Generation

* Personalized workout plans using NVIDIA API  
* Dynamic prompt construction  
* Structured output for readability  

---

## 4. Dashboard

* Displays user details  
* Shows analytics using charts  
* Navigation between features  

---

## 5. Improved UI/UX

* Clean layout  
* Structured plan display  
* Smooth navigation  

---

## 6. Error Handling

* Handles invalid inputs  
* Handles API failures  
* Displays user-friendly messages  

---

# System Workflow

1. User signs up  
2. User logs in  
3. OTP is generated and sent  
4. User verifies OTP  
5. Dashboard access granted  
6. User enters fitness data  
7. AI generates workout plan  
8. Plan is displayed  

---
# Folder Structure

```bash
FITPLAN_AI/
├── static/
│   ├── css/
│   │   └── main.css
│   └── js/
│       └── main.js
├── templates/
│   ├── analytics.html
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── otp.html
│   ├── profile_setup.html
│   ├── schedule.html
│   ├── signup.html
│   └── workout_plan.html
├── .env
├── app.py
├── auth.py
├── database.py
├── email_utils.py
├── model_api.py
├── prompt_builder.py
└── requirements.txt
```

---

### screenshots/  
Application screenshots.

---

# Screenshots

## Login Page
![Login Page](screenshots/loginPage.png)

## Signup Page
![Signup Page](screenshots/signupPage.png)

## OTP Verification
![OTP Verification](screenshots/otp_varification.png)

## Dashboard
![Dashboard](screenshots/mainPage.png)

## Workout Plan
![Workout Plan](screenshots/plan.png)

---

# Database

SQLite database (`database.db`) is used for storing user data.

The database is created automatically and is not included in the repository.

---

# Features Summary

* Authentication with OTP  
* AI-based workout generation  
* NVIDIA API integration  
* Input validation  
* Dashboard with analytics  
* Structured UI  
* Error handling  

---

# Future Improvements

* Add diet recommendations  
* Improve mobile responsiveness  
* Advanced tracking features  

---

# Author

Sneha G Kudur  
FitPlan AI – Personalized Fitness Plan Generator  
Milestone 4 Implementation
