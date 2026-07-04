# 🏥 MediScan AI — Intelligent Medical Diagnosis & Patient Management Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat&logo=streamlit)
![ML](https://img.shields.io/badge/Machine%20Learning-Scikit--learn-orange?style=flat)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-green?style=flat)
![Database](https://img.shields.io/badge/Database-Supabase%20PostgreSQL-3ECF8E?style=flat)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)

> An AI-powered comprehensive medical diagnosis and patient management platform that combines Machine Learning, Explainable AI, and Generative AI to assist healthcare professionals in clinical decision making.

---

## 🌟 Live Demo

🚀 **[Launch MediScan AI](https://mediscan-ai-tkuv.onrender.com)**

> ⚠️ Note: Free tier hosting may take 30-50 seconds to wake up on first visit.

**Demo Credentials:**
| Username | Password |
|---|---|
| admin | admin123 |

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#️-tech-stack)
- [Project Structure](#-project-structure)
- [ML Models](#-ml-models)
- [Installation](#️-installation)
- [Usage](#-usage)
- [Future Enhancements](#-future-enhancements)
- [Author](#️-author)

---

## 🔍 Overview

MediScan AI is a hospital-grade medical intelligence platform built for clinical decision support. It integrates multiple Machine Learning models with Explainable AI and Google Gemini 2.5 to provide accurate disease predictions with transparent reasoning — critical for real medical applications.

The platform is backed by a cloud-hosted **Supabase PostgreSQL** database ensuring real persistent data storage, deployed on **Render** for professional always-on hosting.

---

## ✨ Features

### 🔐 Authentication System
- Secure registration and login with **SHA-256 password hashing**
- Role-based access control — Doctor, Nurse, Admin
- Persistent cloud-based user accounts via Supabase PostgreSQL
- Session management with secure logout

### 🔬 AI Disease Prediction — 5 Modules
- 🩸 **Diabetes Detection** — Random Forest classifier (88%+ accuracy)
- ❤️ **Heart Disease Detection** — Random Forest classifier (88%+ accuracy)
- 🫘 **Kidney Disease Detection** — Random Forest classifier (85%+ accuracy)
- 🩺 **Liver Disease Detection** — Random Forest classifier (83%+ accuracy)
- 🧠 **Parkinson's Disease Detection** — Random Forest classifier (90%+ accuracy)
- Real-time predictions with confidence scores and gauge chart visualisation

### 🧠 Explainable AI (XAI)
- Feature importance analysis for every single prediction
- Visual horizontal bar charts showing top influencing clinical factors
- Transparent AI — doctors understand WHY the AI made each decision
- Critical for medical applications where AI trust is essential

### 👥 Patient Management System
- Register new patients with complete medical profile
- Search patients by name or patient ID
- Edit and update existing patient records
- Delete patient records with confirmation
- Full CRUD operations backed by Supabase cloud database

### 📅 Smart Appointment Booking
- Dynamic doctor listing from cloud database
- Doctor specialisation and years of experience displayed
- Department-wise appointment filtering
- Multiple time slot selection (9 AM — 4:30 PM)
- Appointment status tracking — Scheduled, Completed, Cancelled
- Automated email confirmation on successful booking

### 💊 AI Medication Suggestions
- Powered by **Google Gemini 2.5 API**
- Clinical recommendations tailored to diagnosis result
- Covers: Immediate Actions, Recommended Medications, Lifestyle Changes, Follow-up Tests, Warning Signs
- Downloadable recommendation reports

### 📋 Medical Report Summarizer
- Upload PDF medical reports of any length
- AI extracts and structures key findings instantly
- Covers: Key Findings, Diagnosis Summary, Recommended Actions, Critical Values, Risk Assessment
- Download AI analysis as text report

### 📊 Analytics Dashboard
- Disease distribution pie chart across all 5 modules
- Positive vs negative case comparison bar chart
- Recent patient registrations activity table
- Recent diagnoses tracking table
- Appointment status distribution chart

### 📄 Professional PDF Diagnosis Reports
- Hospital-style letterhead with MediScan AI branding
- Patient details, diagnosis result, confidence score
- AI feature importance bar chart visualisation
- Clinical disclaimer and footer
- One-click download after every diagnosis

### 📧 Email Notifications
- Automated HTML appointment confirmation emails
- Diagnosis result notification emails
- Professional email templates with hospital branding
- Gmail SMTP integration

### 🌙 Dark / Light Mode
- One-click toggle between dark and light themes
- Professional hospital EHR-style UI in both modes
- All components adapt dynamically to selected theme

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| **Frontend** | Streamlit, Plotly, Custom CSS |
| **Backend** | Python 3.10+ |
| **Cloud Database** | Supabase PostgreSQL |
| **Machine Learning** | Scikit-learn, Random Forest, Feature Importance |
| **Generative AI** | Google Gemini 2.5 API |
| **Data Processing** | Pandas, NumPy, SimpleImputer |
| **PDF Generation** | FPDF2 |
| **Email Service** | smtplib, Gmail SMTP |
| **Security** | SHA-256 Hashing, Session Management |
| **Hosting** | Render |
| **Version Control** | Git, GitHub |

---

## 📁 Project Structure

```
mediscan-ai/
├── app.py                    # Main Streamlit application
├── database.py               # Supabase PostgreSQL operations
├── models/
│   ├── __init__.py
│   ├── diabetes.py           # Diabetes prediction model
│   ├── heart.py              # Heart disease prediction model
│   ├── kidney.py             # Kidney disease prediction model
│   ├── liver.py              # Liver disease prediction model
│   └── parkinsons.py         # Parkinson's prediction model
├── data/
│   ├── diabetes.csv          # PIMA Indians Diabetes Dataset
│   ├── heart.csv             # UCI Heart Disease Dataset
│   ├── kidney_disease.csv    # Chronic Kidney Disease Dataset
│   ├── liver_disease.csv     # Indian Liver Patient Dataset
│   └── parkinsons.csv        # UCI Parkinson's Voice Dataset
├── saved_models/             # Trained model .pkl files
├── .env                      # API keys (not tracked)
├── .gitignore
├── Procfile                  # Render deployment config
├── requirements.txt
└── README.md
```

---

## 🤖 ML Models

| Disease | Algorithm | Dataset | Samples | Features | Accuracy |
|---|---|---|---|---|---|
| Diabetes | Random Forest | PIMA Indians Diabetes | 768 | 8 | 88%+ |
| Heart Disease | Random Forest | UCI Cleveland | 303 | 13 | 88%+ |
| Kidney Disease | Random Forest | Chronic Kidney Disease | 400 | 11 | 85%+ |
| Liver Disease | Random Forest | Indian Liver Patient | 583 | 10 | 83%+ |
| Parkinson's | Random Forest | UCI Parkinson's Voice | 197 | 22 | 90%+ |

**Preprocessing Pipeline:**
1. Handle missing values — SimpleImputer (median strategy)
2. Encode categorical variables — LabelEncoder
3. Normalise features — StandardScaler
4. Split data — 80% training / 20% testing
5. Train — RandomForestClassifier (n_estimators=100)
6. Serialise — pickle (.pkl files)

---

## ⚙️ Installation

### Prerequisites
- Python 3.10+
- Google Gemini API Key — free from [aistudio.google.com](https://aistudio.google.com)
- Supabase account — free from [supabase.com](https://supabase.com)
- Gmail App Password for email notifications (optional)

### Steps

```bash
# 1. Clone repository
git clone https://github.com/Ushapriya06/mediscan-ai.git
cd mediscan-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
GOOGLE_API_KEY=your_gemini_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
EMAIL_USER=your_gmail_address
EMAIL_PASSWORD=your_gmail_app_password

# 4. Run the application
streamlit run app.py
```

### Default Login
```
Username: admin
Password: admin123
```

---

## 🚀 Usage

1. **Login** — use demo credentials or register a new account
2. **Dashboard** — view real-time platform statistics and AI model performance
3. **Analytics** — explore disease trends, patient activity and appointment stats
4. **Disease Prediction** — enter patient clinical data and get AI diagnosis across 5 modules
5. **AI Explainability** — understand which clinical factors influenced the diagnosis
6. **Patient Management** — register, search, edit and delete patient records
7. **Appointments** — book appointments, track status and receive email confirmations
8. **Medication Suggestions** — get AI-powered clinical recommendations for 8 diseases
9. **Report Summarizer** — upload PDF medical reports for instant AI analysis
10. **Settings** — manage profile email for notification preferences

---

## 🔮 Future Enhancements

- [ ] Medical image analysis — Chest X-ray pneumonia detection using CNN
- [ ] Doctor-specific dashboards with personal patient queues
- [ ] Multi-language support — Telugu, Hindi, Tamil
- [ ] Mobile-responsive Progressive Web App (PWA)
- [ ] Integration with HL7 FHIR healthcare standards
- [ ] Real-time AI health assistant chat
- [ ] Telemedicine video consultation integration

---

## 📊 Datasets Used

| Dataset | Source | Link |
|---|---|---|
| PIMA Indians Diabetes | Kaggle/UCI | kaggle.com/uciml/pima-indians-diabetes-database |
| Heart Disease Cleveland | Kaggle/UCI | kaggle.com/datasets/ronitf/heart-disease-uci |
| Chronic Kidney Disease | Kaggle | kaggle.com/datasets/mansoordaku/ckdisease |
| Indian Liver Patient | Kaggle/UCI | kaggle.com/datasets/uciml/indian-liver-patient-records |
| Parkinson's Disease | Kaggle/UCI | kaggle.com/datasets/vikasukani/parkinsons-disease-data-set |

---

## 👩‍💻 Author

**G. Ushapriya**
- 🎓 B.Tech ECE — Megha Institute of Engineering and Technology for Women (CGPA: 8.55)
- 📍 Hyderabad, India
- 🔗 [LinkedIn](https://linkedin.com/in/usha-priya-3830072a9)
- 💻 [GitHub](https://github.com/Ushapriya06)
- 📧 ushapriya006@gmail.com

---

## 📄 License

This project is licensed under the MIT License.

---

<p align="center">
Built with ❤️ by G. Ushapriya | MediScan AI v2.0 | Powered by Google Gemini 2.5
</p>
