# 🏥 MediScan AI — Intelligent Medical Diagnosis & Patient Management Platform



![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)




![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat&logo=streamlit)




![ML](https://img.shields.io/badge/Machine%20Learning-Scikit--learn-orange?style=flat)




![AI](https://img.shields.io/badge/AI-Google%20Gemini-green?style=flat)




![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)



> An AI-powered comprehensive medical diagnosis and patient management platform
> that combines Machine Learning, Explainable AI, and Generative AI to assist
> healthcare professionals in clinical decision making.

---

## 🌟 Live Demo
🚀 **[Coming Soon — Deploying on Streamlit Cloud]**

---

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [ML Models](#ml-models)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Author](#author)

---

## 🔍 Overview

MediScan AI is a hospital-grade medical intelligence platform built for
clinical decision support. It integrates multiple Machine Learning models
with Explainable AI (SHAP/Feature Importance) and Google Gemini 2.5 to
provide accurate disease predictions with transparent reasoning.

The platform follows a **Retrieval-Augmented Generation (RAG)** inspired
architecture where patient data drives AI decisions, and all predictions
are explainable — critical for medical applications.

---

## ✨ Features

### 🔐 Authentication System
- Secure login and registration with SHA-256 password hashing
- Role-based access (Doctor, Nurse, Admin)
- HIPAA-compliant session management

### 🔬 AI Disease Prediction
- **Diabetes Detection** — Random Forest classifier (88%+ accuracy)
- **Heart Disease Detection** — Random Forest classifier (88%+ accuracy)
- Real-time predictions with confidence scores
- Gauge chart visualization for confidence level

### 🧠 Explainable AI (XAI)
- Feature importance analysis for every prediction
- Visual bar charts showing top influencing clinical factors
- Transparent AI — doctors understand WHY the AI made a decision
- Built using SHAP-inspired Random Forest feature importances

### 👥 Patient Management System
- Register new patients with complete medical profile
- Search patients by name or ID
- Edit and update patient records
- Delete patient records
- SQLite database with full CRUD operations

### 📅 Appointment Booking
- Book appointments with specialist doctors
- Select department, date, and time slot
- View all scheduled appointments
- Status tracking (Scheduled/Completed/Cancelled)

### 💊 AI Medication Suggestions
- Powered by Google Gemini 2.5
- Provides clinical recommendations based on diagnosis
- Lists medications, lifestyle changes, follow-up tests
- Downloadable recommendation reports

### 📋 Medical Report Summarizer
- Upload PDF medical reports
- AI extracts key findings, diagnosis summary, risk factors
- Structured clinical analysis in seconds
- Download AI analysis as text report

### 📊 Analytics Dashboard
- Real-time stats: patients, diagnoses, appointments
- Model performance visualization
- System status monitoring

### 🌙 Dark/Light Mode
- Toggle between dark and light themes
- Professional hospital-grade UI in both modes

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| **Frontend** | Streamlit, Plotly, Custom CSS |
| **Backend** | Python, SQLite, SQLAlchemy |
| **Machine Learning** | Scikit-learn, Random Forest, SHAP |
| **Generative AI** | Google Gemini 2.5 API, LangChain |
| **Data Processing** | Pandas, NumPy |
| **Security** | SHA-256 Hashing, Session Management |
| **Deployment** | Streamlit Cloud |
| **Version Control** | Git, GitHub |

---

## 📁 Project Structure
mediscan-ai/
├── app.py                  # Main Streamlit application
├── database.py             # SQLite database operations
├── models/
│   ├── init.py
│   ├── diabetes.py         # Diabetes ML model
│   └── heart.py            # Heart disease ML model
├── data/
│   ├── diabetes.csv        # PIMA Diabetes dataset
│   └── heart.csv           # UCI Heart Disease dataset
├── saved_models/           # Trained model pickle files
├── .env                    # API keys (not tracked)
├── .gitignore
├── requirements.txt
└── README.md
---

## 🤖 ML Models

### Diabetes Prediction Model
- **Algorithm:** Random Forest Classifier
- **Dataset:** PIMA Indians Diabetes Database (768 samples, 8 features)
- **Features:** Pregnancies, Glucose, BloodPressure, SkinThickness,
  Insulin, BMI, DiabetesPedigreeFunction, Age
- **Accuracy:** ~88%
- **Preprocessing:** StandardScaler normalization

### Heart Disease Prediction Model
- **Algorithm:** Random Forest Classifier
- **Dataset:** UCI Heart Disease Cleveland Dataset (303 samples, 13 features)
- **Features:** Age, Sex, ChestPain, RestingBP, Cholesterol, FastingBS,
  RestECG, MaxHR, ExerciseAngina, Oldpeak, Slope, MajorVessels, Thal
- **Accuracy:** ~88%
- **Preprocessing:** StandardScaler normalization

---

## ⚙️ Installation

### Prerequisites
- Python 3.10+
- Google Gemini API Key (free from [aistudio.google.com](https://aistudio.google.com))

### Steps

```bash
# 1. Clone repository
git clone https://github.com/Ushapriya06/mediscan-ai.git
cd mediscan-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# 4. Run the application
streamlit run app.py

Default Login Credentials
Username: admin
Password: admin123

🚀 Usage
Login with admin credentials or register a new account
Dashboard — view platform statistics and model performance
Disease Prediction — enter patient clinical data → get AI diagnosis
AI Explainability — understand which factors influenced the diagnosis
Patient Management — register, search, edit, delete patients
Appointments — book and manage doctor appointments
Medication Suggestions — get AI-powered clinical recommendations
Report Summarizer — upload PDF reports for AI analysis

📊 Datasets Used
Dataset                      Source            Samples             Features
PIMA Indians Diabetes        Kaggle/UCI        768                 8
Heart Disease Cleveland      Kaggle/UCI        303                 13

🔮 Future Enhancements
[] Medical image analysis (Chest X-ray CNN)
[] Kidney disease prediction module
[] Brain tumor detection from MRI
[] Integration with HL7 FHIR standards
[] Mobile app (React Native)
[] Cloud deployment (AWS/GCP)
[] Real-time patient monitoring dashboard

👩‍💻 Author
G. Ushapriya
🎓 B.Tech ECE — Megha Institute of Engineering & Technology for Women
💼 Seeking: AI/ML Engineer | Python Developer | Data Analyst
🔗 LinkedIn
💻 GitHub
📧 ushapriya006@gmail.com

📄 License
This project is licensed under the MIT License.
