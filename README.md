# 🏥 MediScan AI — Intelligent Medical Diagnosis & Patient Management Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat\&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat\&logo=streamlit)
![ML](https://img.shields.io/badge/Machine%20Learning-Scikit--learn-orange?style=flat)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-green?style=flat)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)

> An AI-powered comprehensive medical diagnosis and patient management platform
> that combines Machine Learning, Explainable AI, and Generative AI to assist
> healthcare professionals in clinical decision making.

---

## 🌟 Live Demo
🚀 **[Live App](https://mediscan-ai-tkuv.onrender.com)**

---

## 📋 Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Tech Stack](#tech-stack)
* [Project Structure](#project-structure)
* [ML Models](#ml-models)
* [Installation](#installation)
* [Usage](#usage)
* [Datasets](#datasets)
* [Future Enhancements](#future-enhancements)
* [Author](#author)

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

* Secure login and registration with SHA-256 password hashing
* Role-based access (Doctor, Nurse, Admin)
* Session management

### 🔬 AI Disease Prediction

* **Diabetes Detection** — Random Forest classifier (~88% accuracy)

* **Heart Disease Detection** — Random Forest classifier (~88% accuracy)

* **Kidney Disease Detection** — ML-based classification

* **Liver Disease Detection** — Predicts liver disorders

* **Parkinson’s Disease Detection** — SVM/ML-based classification

* Real-time predictions with confidence scores

* Gauge chart visualization for confidence

### 🧠 Explainable AI (XAI)

* Feature importance analysis for every prediction
* Visual bar charts showing key influencing factors
* Transparent AI — understand WHY predictions are made

### 👥 Patient Management System

* Register new patients
* Search patients by name or ID
* Update and delete patient records
* SQLite database with CRUD operations

### 📅 Appointment Booking

* Book appointments with specialists
* Select department, date, and time
* Track appointment status

### 💊 AI Medication Suggestions

* Powered by Google Gemini 2.5
* Provides:

  * Medications
  * Lifestyle recommendations
  * Follow-up tests

### 📋 Medical Report Summarizer

* Upload PDF reports
* Extract diagnosis, risk factors, key insights
* Generate structured summaries

### 📊 Analytics Dashboard

* Real-time stats: patients, diagnoses, appointments
* Model performance insights

### 🌙 UI Features

* Dark/Light mode
* Clean, professional interface

### 📊 Analytics Dashboard
- Disease distribution pie chart
- Positive vs negative case statistics
- Recent patients and diagnoses tracking
- Appointment status distribution

### 📧 Email Notifications
- Automated appointment confirmation emails
- Diagnosis result notifications
- Professional HTML email templates

### 📄 Professional PDF Reports
- Hospital-style letterhead diagnosis reports
- Includes AI feature importance breakdown
- Downloadable clinical documentation

### ☁️ Cloud Database
- Migrated from SQLite to Supabase PostgreSQL
- Real persistent cloud database
- Deployed on Render with always-accessible data

---

## 🛠️ Tech Stack

## 🛠️ Tech Stack

| Category            |    Technology                                   |
|-------------------  |-----------------------------------------------  |
| Frontend            | Streamlit, Plotly, Custom CSS                   |
| Backend             | Python                                          |
| Database            | Supabase PostgreSQL (Cloud)                     |
| Machine Learning    | Scikit-learn, Random Forest, Feature Importance |
| Generative AI       | Google Gemini 2.5 API                           |
| Data Processing     | Pandas, NumPy                                   |
| PDF Generation      | FPDF2                                           |
| Email Service       | SMTP (Gmail), smtplib                           |
| Security            | SHA-256 Hashing, Session Management             |
| Hosting             | Render                                          |
| Version Control     | Git, GitHub                                     |
---

## 📁 Project Structure

mediscan-ai/
├── app.py
├── database.py
├── models/
│   ├── diabetes.py
│   ├── heart.py
│   ├── kidney.py
│   ├── liver.py
│   └── parkinsons.py
├── data/
├── saved_models/
├── .env
├── .gitignore
├── requirements.txt
└── README.md

---

## 🤖 ML Models

### Diabetes Prediction Model

* **Algorithm:** Random Forest
* **Dataset:** PIMA Diabetes Dataset
* **Accuracy:** ~88%

### Heart Disease Prediction Model

* **Algorithm:** Random Forest
* **Dataset:** UCI Heart Disease Dataset
* **Accuracy:** ~88%

### Kidney Disease Prediction Model

* **Algorithm:** Random Forest / Logistic Regression
* **Dataset:** Chronic Kidney Disease Dataset
* **Goal:** Early detection

### Liver Disease Prediction Model

* **Algorithm:** Decision Tree / Random Forest
* **Dataset:** Indian Liver Patient Dataset

### Parkinson’s Disease Prediction Model

* **Algorithm:** Support Vector Machine (SVM)
* **Dataset:** UCI Parkinson’s Dataset
* **Features:** Voice measurements (jitter, shimmer, etc.)
* **Accuracy:** ~85–90%

---

## ⚙️ Installation

### Prerequisites

* Python 3.10+
* Google Gemini API Key

### Steps

```bash
git clone https://github.com/Ushapriya06/mediscan-ai.git
cd mediscan-ai
pip install -r requirements.txt
```

Create `.env` file:

```bash
GOOGLE_API_KEY=your_api_key_here
```

Run:

```bash
streamlit run app.py
```

---

## 🚀 Usage

1. Login or register
2. Use dashboard for overview
3. Enter patient data for disease prediction
4. View explainable AI results
5. Manage patients and appointments
6. Generate AI recommendations
7. Upload reports for summarization

---

## 📊 Datasets

| Dataset        | Source       |
| -------------- | ------------ |
| Diabetes       | UCI / Kaggle |
| Heart Disease  | UCI          |
| Kidney Disease | UCI          |
| Liver Disease  | ILPD         |
| Parkinson’s    | UCI          |

---

## 🔮 Future Enhancements

* Medical image analysis (X-ray, MRI)
* Mobile application
* Cloud deployment (AWS/GCP)
* Real-time monitoring
* Hospital integration APIs

---

## 👩‍💻 Author

**G. Ushapriya**

* GitHub: https://github.com/Ushapriya06
* LinkedIn: https://linkedin.com/in/usha-priya-3830072a9
* Email: [ushapriya006@gmail.com](mailto:ushapriya006@gmail.com)

---

## 📄 License

MIT License

---

Built with ❤️ by Ushapriya | MediScan AI 🚀
