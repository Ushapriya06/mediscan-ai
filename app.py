import time
from fpdf import FPDF
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import Counter
import streamlit as st
# mediscan AI v2.0 - Analytics, PDF Reports, Email Notifications
from database import init_db
init_db()

st.set_page_config(
    page_title="MediScan AI | Medical Intelligence Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Theme ──────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if st.session_state.dark_mode:
    bg = "#0F172A"
    card_bg = "#1E293B"
    text = "#F1F5F9"
    subtext = "#94A3B8"
    border = "#334155"
    sidebar_bg = "#0F172A"
    input_bg = "#1E293B"
else:
    bg = "#F4F6F9"
    card_bg = "#FFFFFF"
    text = "#1A2035"
    subtext = "#64748B"
    border = "#DDE1E7"
    sidebar_bg = "#1A2035"
    input_bg = "#FAFBFC"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * {{ font-family: 'Inter', sans-serif; }}
    .stApp {{ background-color: {bg}; }}
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid #2D3456;
    }}
    [data-testid="stSidebar"] * {{ color: #A9B4C8 !important; }}
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {{ color: white !important; }}
    .nav-bar {{
        background: {card_bg};
        padding: 15px 30px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 24px;
        border-left: 4px solid #0066CC;
    }}
    .stat-card {{
        background: {card_bg};
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border-top: 3px solid #0066CC;
    }}
    .stat-card-green {{ border-top-color: #00897B; }}
    .stat-card-red {{ border-top-color: #E53935; }}
    .stat-card-purple {{ border-top-color: #7B1FA2; }}
    .stat-card-orange {{ border-top-color: #F57C00; }}
    .section-card {{
        background: {card_bg};
        padding: 28px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }}
    .stButton > button {{
        background-color: #0066CC;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        font-size: 14px;
    }}
    .stButton > button:hover {{
        background-color: #0052A3;
        color: white;
    }}
    .login-container {{
        background: {card_bg};
        padding: 48px;
        border-radius: 16px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    }}
    h1 {{ color: {text} !important; font-weight: 700 !important; }}
    h2 {{ color: {text} !important; font-weight: 600 !important; }}
    h3 {{ color: {text} !important; font-weight: 600 !important; }}
    p {{ color: {subtext}; }}
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    header {{ visibility: hidden; }}
    .stTabs [data-baseweb="tab-list"] {{
        background: {bg};
        border-radius: 8px;
        padding: 4px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        border-radius: 6px;
        color: {subtext};
        font-weight: 500;
    }}
    .stTabs [aria-selected="true"] {{
        background: {card_bg} !important;
        color: #0066CC !important;
    }}
    .stTextInput > div > div > input {{
        border: 1px solid {border};
        border-radius: 8px;
        background: {input_bg};
        color: {text};
    }}
    .stSelectbox > div > div {{
        border: 1px solid {border};
        border-radius: 8px;
        background: {input_bg};
    }}
</style>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ── Login Page ─────────────────────────────────
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1.2, 1, 1.2])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='login-container'>
            <div style='text-align:center; margin-bottom:32px'>
                <div style='background:#E8F0FE; width:72px; height:72px;
                            border-radius:16px; display:inline-flex;
                            align-items:center; justify-content:center;
                            font-size:36px; margin-bottom:16px'>🏥</div>
                <h2 style='color:{text}; margin:0; font-size:24px'>
                    MediScan AI
                </h2>
                <p style='color:{subtext}; margin:4px 0 0 0; font-size:13px'>
                    Medical Intelligence Platform
                </p>
            </div>
        """, unsafe_allow_html=True)

        tab_login, tab_register = st.tabs(["🔑 Sign In", "📝 Create Account"])

        with tab_login:
            st.markdown("<br>", unsafe_allow_html=True)
            login_username = st.text_input(
                "Username",
                placeholder="Enter your username",
                key="login_user"
            )
            login_password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_pass"
            )
            remember_me = st.checkbox("Remember me", key="remember")
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Sign In →", use_container_width=True,
                        key="signin"):
                if login_username and login_password:
                    if len(login_password) < 6:
                        st.error("Password must be at least 6 characters!")
                    else:
                        from database import verify_user
                        user = verify_user(login_username, login_password)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.username = login_username
                            st.session_state.user_role = user.get("role", "doctor")
                            st.session_state.full_name = user.get("full_name", login_username)
                            st.rerun()
                        else:
                            st.error("❌ Invalid username or password!")
                else:
                    st.error("Please enter both username and password!")

            st.markdown(f"""
            <p style='color:{subtext}; font-size:12px;
                      text-align:center; margin-top:16px'>
            Demo: <b>admin</b> / <b>admin123</b>
            </p>
            """, unsafe_allow_html=True)

        with tab_register:
            st.markdown("<br>", unsafe_allow_html=True)
            reg_fullname = st.text_input(
                "Full Name",
                placeholder="Dr. Your Name",
                key="reg_fullname"
            )
            reg_username = st.text_input(
                "Username",
                placeholder="Choose a username",
                key="reg_user"
            )
            reg_email = st.text_input(
                "Email Address",
                placeholder="your@email.com",
                key="reg_email"
            )
            reg_phone = st.text_input(
                "Phone Number",
                placeholder="+91 XXXXX XXXXX",
                key="reg_phone"
            )
            reg_role = st.selectbox(
                "Role",
                ["doctor", "nurse", "admin"],
                key="reg_role"
            )
            reg_pass = st.text_input(
                "Password",
                type="password",
                placeholder="Minimum 8 characters",
                key="reg_pass"
            )
            reg_confirm = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Repeat your password",
                key="reg_confirm"
            )

            # Password strength indicator
            if reg_pass:
                strength = 0
                tips = []
                if len(reg_pass) >= 8:
                    strength += 1
                else:
                    tips.append("at least 8 characters")
                if any(c.isupper() for c in reg_pass):
                    strength += 1
                else:
                    tips.append("one uppercase letter")
                if any(c.isdigit() for c in reg_pass):
                    strength += 1
                else:
                    tips.append("one number")
                if any(c in "!@#$%^&*" for c in reg_pass):
                    strength += 1
                else:
                    tips.append("one special character")

                colors = ["#E74C3C", "#E67E22", "#F1C40F", "#27AE60"]
                labels = ["Weak", "Fair", "Good", "Strong"]
                st.markdown(f"""
                <div style='margin:8px 0'>
                    <div style='display:flex; gap:4px; margin-bottom:4px'>
                        {''.join([f"<div style='height:4px; flex:1; border-radius:2px; background:{colors[min(strength-1,3)] if i < strength else '#E0E0E0'}'></div>" for i in range(4)])}
                    </div>
                    <span style='font-size:12px; color:{colors[min(strength-1,3)] if strength > 0 else "#E0E0E0"}'>
                        {'Password strength: ' + labels[min(strength-1,3)] if strength > 0 else ''}
                        {' — Add: ' + ', '.join(tips) if tips else ' ✅'}
                    </span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            terms = st.checkbox(
                "I agree to the Terms of Service and Privacy Policy",
                key="terms"
            )

            if st.button("Create Account →",
                        use_container_width=True, key="register"):
                errors = []
                if not reg_fullname:
                    errors.append("Full name is required")
                if not reg_username:
                    errors.append("Username is required")
                elif len(reg_username) < 3:
                    errors.append("Username must be at least 3 characters")
                if not reg_email or "@" not in reg_email:
                    errors.append("Valid email is required")
                if not reg_pass:
                    errors.append("Password is required")
                elif len(reg_pass) < 8:
                    errors.append("Password must be at least 8 characters")
                elif reg_pass != reg_confirm:
                    errors.append("Passwords do not match")
                if not terms:
                    errors.append("Please accept terms and conditions")

                if errors:
                    for e in errors:
                        st.error(f"❌ {e}")
                else:
                    from database import (create_user, username_exists,
                                         email_exists)
                    if username_exists(reg_username):
                        st.error("❌ Username already taken!")
                    elif email_exists(reg_email):
                        st.error("❌ Email already registered!")
                    else:
                        success, msg = create_user(
                            reg_username, reg_pass, reg_role,
                            reg_fullname, reg_email, reg_phone
                        )
                        if success:
                            st.success(f"✅ {msg} Please sign in!")
                        else:
                            st.error(f"❌ {msg}")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <p style='text-align:center; color:{subtext};
                  font-size:12px; margin-top:16px'>
            🔒 HIPAA Compliant | Secure Medical Platform | SHA-256 Encrypted
        </p>
        """, unsafe_allow_html=True)
    st.stop()

# ── Imports after login ────────────────────────
from database import (get_dashboard_stats, add_patient, get_all_patients,
                      search_patients, update_patient, delete_patient,
                      add_diagnosis, add_appointment, get_all_appointments,
                      update_appointment_status)
from models.diabetes import train_diabetes_model, predict_diabetes, explain_diabetes
from models.heart import train_heart_model, predict_heart, explain_heart
from models.kidney import train_kidney_model, predict_kidney, explain_kidney
from models.liver import train_liver_model, predict_liver, explain_liver
from models.parkinsons import train_parkinsons_model, predict_parkinsons, explain_parkinsons
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ── Train Models ───────────────────────────────
if "models_trained" not in st.session_state:
    with st.spinner("Initializing AI models..."):
        try:
            diabetes_acc = train_diabetes_model()
            heart_acc = train_heart_model()
            kidney_acc = train_kidney_model()
            liver_acc = train_liver_model()
            parkinsons_acc = train_parkinsons_model()
            st.session_state.models_trained = True
            st.session_state.diabetes_acc = diabetes_acc
            st.session_state.heart_acc = heart_acc
            st.session_state.kidney_acc = kidney_acc
            st.session_state.liver_acc = liver_acc
            st.session_state.parkinsons_acc = parkinsons_acc
        except Exception as e:
            st.error(f"Model error: {e}")

# ── Sidebar ────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='padding:24px 0 16px 0'>
        <div style='display:flex; align-items:center; gap:12px'>
            <div style='background:#0066CC; width:36px; height:36px;
                        border-radius:8px; display:flex;
                        align-items:center; justify-content:center;
                        font-size:18px'>🏥</div>
            <div>
                <div style='color:white; font-weight:700; font-size:16px'>
                    MediScan AI
                </div>
                <div style='color:#64748B; font-size:11px'>
                    v2.0 Medical Platform
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#2D3456'>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:#252D45; padding:12px 16px;
                border-radius:8px; margin-bottom:20px'>
        <div style='color:#94A3B8; font-size:11px;
                    text-transform:uppercase; letter-spacing:1px'>
            Signed in as
        </div>
        <div style='color:white; font-weight:600;
                    font-size:14px; margin-top:2px'>
            {st.session_state.username}
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("", [
        "🏠  Dashboard",
        "📊  Analytics",
        "🔬  Disease Prediction",
        "👥  Patient Management",
        "📅  Appointments",
        "💊  Medication Suggestions",
        "📋  Report Summarizer",
        "⚙️  Settings"
    ])

    st.markdown("<hr style='border-color:#2D3456'>", unsafe_allow_html=True)

    # Dark mode toggle
    dark_label = "☀️ Light Mode" if st.session_state.dark_mode else "🌙 Dark Mode"
    if st.button(dark_label, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    if st.button("Sign Out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# ── Email Notification ─────────────────────────
def send_email(to_email, subject, body):
    try:
        sender = os.getenv("EMAIL_USER")
        password = os.getenv("EMAIL_PASSWORD")
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        return True
    except Exception as e:
        return False

def appointment_email(patient_name, doctor, date, time, to_email):
    subject = "MediScan AI — Appointment Confirmation"
    body = f"""
    <div style="font-family: Arial; max-width: 600px; margin: auto;
                border: 1px solid #ddd; border-radius: 10px; overflow: hidden">
        <div style="background: #1A5276; padding: 20px; text-align: center">
            <h1 style="color: white; margin: 0">🏥 MediScan AI</h1>
            <p style="color: #AED6F1; margin: 5px 0">Medical Intelligence Platform</p>
        </div>
        <div style="padding: 30px">
            <h2 style="color: #1A5276">Appointment Confirmed ✅</h2>
            <p>Dear <b>{patient_name}</b>,</p>
            <p>Your appointment has been successfully booked.</p>
            <div style="background: #EBF5FB; padding: 15px;
                        border-radius: 8px; margin: 20px 0">
                <p><b>👨‍⚕️ Doctor:</b> {doctor}</p>
                <p><b>📅 Date:</b> {date}</p>
                <p><b>⏰ Time:</b> {time}</p>
            </div>
            <p>Please arrive 10 minutes before your appointment.</p>
            <p>For any queries contact us at mediscan@hospital.com</p>
        </div>
        <div style="background: #EBF5FB; padding: 15px; text-align: center">
            <p style="color: #666; font-size: 12px">
            MediScan AI | Powered by Google Gemini 2.5
            </p>
        </div>
    </div>
    """
    return send_email(to_email, subject, body)

def diagnosis_email(patient_name, disease, result,
                    confidence, to_email):
    color = "#E74C3C" if result == "Positive" else "#27AE60"
    subject = f"MediScan AI — {disease} Diagnosis Report"
    body = f"""
    <div style="font-family: Arial; max-width: 600px; margin: auto;
                border: 1px solid #ddd; border-radius: 10px; overflow: hidden">
        <div style="background: #1A5276; padding: 20px; text-align: center">
            <h1 style="color: white; margin: 0">🏥 MediScan AI</h1>
            <p style="color: #AED6F1; margin: 5px 0">Medical Intelligence Platform</p>
        </div>
        <div style="padding: 30px">
            <h2 style="color: #1A5276">Diagnosis Report</h2>
            <p>Dear <b>{patient_name}</b>,</p>
            <p>Your AI diagnosis results are ready.</p>
            <div style="background: #EBF5FB; padding: 15px;
                        border-radius: 8px; margin: 20px 0">
                <p><b>🔬 Disease Assessed:</b> {disease}</p>
                <p><b>📊 Result:</b>
                    <span style="color: {color}; font-weight: bold">
                        {result}
                    </span>
                </p>
                <p><b>🎯 AI Confidence:</b> {confidence}%</p>
            </div>
            <p style="color: #E74C3C">
                <b>⚠️ Important:</b> This is an AI-assisted diagnosis.
                Please consult a qualified physician for medical advice.
            </p>
        </div>
        <div style="background: #EBF5FB; padding: 15px; text-align: center">
            <p style="color: #666; font-size: 12px">
            MediScan AI | HIPAA Compliant | Powered by Google Gemini 2.5
            </p>
        </div>
    </div>
    """
    return send_email(to_email, subject, body)

# ── PDF Report Generator ───────────────────────
def generate_pdf_report(patient_name, disease, result,
                        confidence, features, username,
                        suggestions):
    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_fill_color(26, 82, 118)
    pdf.rect(0, 0, 210, 35, "F")
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(10, 8)
    pdf.cell(0, 10, "MEDISCAN AI", ln=True, align="C")
    pdf.set_font("Helvetica", size=10)
    pdf.set_xy(10, 20)
    pdf.cell(0, 8, "Medical Intelligence Platform | Clinical Diagnosis Report",
             ln=True, align="C")

    # Report details
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(10, 45)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "PATIENT DIAGNOSIS REPORT", ln=True)

    pdf.set_font("Helvetica", size=10)
    pdf.set_fill_color(235, 245, 251)
    pdf.rect(10, 58, 190, 35, "F")
    pdf.set_xy(15, 62)
    pdf.cell(90, 7,
             f"Patient Name: {patient_name.encode('latin-1', 'replace').decode('latin-1')}")
    pdf.cell(90, 7, f"Generated By: Dr. {username}", ln=True)
    pdf.set_xy(15, 72)
    pdf.cell(90, 7, f"Disease Assessed: {disease}")
    pdf.cell(90, 7,
             f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    # Result
    pdf.set_xy(10, 100)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "DIAGNOSIS RESULT", ln=True)
    if result == "Positive":
        pdf.set_fill_color(231, 76, 60)
    else:
        pdf.set_fill_color(39, 174, 96)
    pdf.set_text_color(255, 255, 255)
    pdf.rect(10, 110, 190, 20, "F")
    pdf.set_xy(10, 114)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(95, 10, f"Result: {result}", align="C")
    pdf.cell(95, 10, f"AI Confidence: {confidence}%",
             align="C", ln=True)

    # Feature importance
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(10, 138)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "TOP INFLUENCING FACTORS (AI EXPLAINABILITY)", ln=True)
    pdf.set_font("Helvetica", size=10)
    for i, (feat, imp) in enumerate(features[:5], 1):
        feat_clean = str(feat).encode(
            'latin-1', 'replace'
        ).decode('latin-1')
        pdf.set_xy(15, 148 + (i-1)*10)
        pdf.set_fill_color(214, 234, 248)
        bar_width = int(imp * 150)
        pdf.rect(15, 149 + (i-1)*10, bar_width, 6, "F")
        pdf.set_xy(15, 148 + (i-1)*10)
        pdf.cell(0, 8,
                 f"{i}. {feat_clean}: {round(imp*100, 1)}%")

    # Disclaimer
    pdf.set_xy(10, 210)
    pdf.set_fill_color(254, 249, 231)
    pdf.rect(10, 208, 190, 25, "F")
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.set_xy(15, 212)
    pdf.multi_cell(180, 6,
        "DISCLAIMER: This report is generated by MediScan AI and is "
        "intended for doctor reference only. It does not replace "
        "professional medical advice, diagnosis, or treatment. "
        "Always consult a qualified physician.")

    # Footer
    pdf.set_fill_color(26, 82, 118)
    pdf.rect(0, 275, 210, 22, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", size=9)
    pdf.set_xy(10, 280)
    pdf.cell(0, 8,
             "MediScan AI v2.0 | Powered by Google Gemini 2.5 | "
             "HIPAA Compliant | mediscan-ai-tkuv.onrender.com",
             align="C")

    return bytes(pdf.output())

# ── Helper: AI Medication Suggestions ─────────
def get_medication_suggestions(disease, result, patient_info):
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"""You are a clinical AI assistant supporting doctors.
A patient has been assessed for {disease}.
Result: {result}
Patient Info: {patient_info}

Provide a structured clinical recommendation:
1. **Immediate Actions**
2. **Recommended Medications** (generic names only)
3. **Lifestyle Changes**
4. **Follow-up Tests**
5. **Warning Signs to Watch**

Important: This is for doctor reference only. Always consult a physician."""
    response = model.generate_content(prompt)
    return response.text

# ── Helper: Generate Diagnosis Report ─────────
def generate_report(patient_name, disease, result,
                    confidence, features, username):
    content = f"""
MEDISCAN AI — CLINICAL DIAGNOSIS REPORT
{"="*50}
Generated by: {username}
Date: {time.strftime("%Y-%m-%d %H:%M:%S")}
{"="*50}

PATIENT INFORMATION
Patient Name: {patient_name}
Disease Assessed: {disease}

DIAGNOSIS RESULT
Result: {result}
Confidence: {confidence}%

AI FEATURE IMPORTANCE
"""
    for i, (feat, imp) in enumerate(features[:5], 1):
        content += f"{i}. {feat}: {round(imp*100, 2)}%\n"
    content += f"""
{"="*50}
DISCLAIMER: This report is AI-generated and should
be reviewed by a qualified medical professional.
MediScan AI v2.0 | HIPAA Compliant
{"="*50}
"""
    return content

# ── Dashboard ──────────────────────────────────
if page == "🏠  Dashboard":
    st.markdown(f"""
    <div class='nav-bar'>
        <div>
            <div style='font-size:20px; font-weight:700; color:{text}'>
                Dashboard
            </div>
            <div style='font-size:13px; color:{subtext}'>
                MediScan AI Platform Overview
            </div>
        </div>
        <div style='color:#22C55E; font-size:13px'>
            🟢 All systems operational
        </div>
    </div>
    """, unsafe_allow_html=True)

    total_patients, total_diagnoses, positive_cases, total_appointments = get_dashboard_stats()

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"""
        <div class='stat-card'>
            <div style='color:{subtext}; font-size:11px; font-weight:600;
                        text-transform:uppercase; letter-spacing:1px'>
                Total Patients
            </div>
            <div style='font-size:32px; font-weight:700;
                        color:{text}; margin:8px 0'>{total_patients}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='stat-card stat-card-green'>
            <div style='color:{subtext}; font-size:11px; font-weight:600;
                        text-transform:uppercase; letter-spacing:1px'>
                Diagnoses
            </div>
            <div style='font-size:32px; font-weight:700;
                        color:{text}; margin:8px 0'>{total_diagnoses}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='stat-card stat-card-red'>
            <div style='color:{subtext}; font-size:11px; font-weight:600;
                        text-transform:uppercase; letter-spacing:1px'>
                Positive Cases
            </div>
            <div style='font-size:32px; font-weight:700;
                        color:{text}; margin:8px 0'>{positive_cases}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class='stat-card stat-card-orange'>
            <div style='color:{subtext}; font-size:11px; font-weight:600;
                        text-transform:uppercase; letter-spacing:1px'>
                Appointments
            </div>
            <div style='font-size:32px; font-weight:700;
                        color:{text}; margin:8px 0'>{total_appointments}</div>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
        <div class='stat-card stat-card-purple'>
            <div style='color:{subtext}; font-size:11px; font-weight:600;
                        text-transform:uppercase; letter-spacing:1px'>
                AI Models
            </div>
            <div style='font-size:32px; font-weight:700;
                        color:{text}; margin:8px 0'>5</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown(f"<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### 📊 AI Model Performance")
        if "diabetes_acc" in st.session_state:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=["Diabetes", "Heart Disease"],
                y=[
                    round(st.session_state.diabetes_acc * 100, 1),
                    round(st.session_state.heart_acc * 100, 1)
                ],
                marker_color=["#0066CC", "#00897B"],
                width=0.4,
                text=[
                    f"{round(st.session_state.diabetes_acc*100,1)}%",
                    f"{round(st.session_state.heart_acc*100,1)}%"
                ],
                textposition="outside"
            ))
            fig.update_layout(
                plot_bgcolor=card_bg,
                paper_bgcolor=card_bg,
                yaxis=dict(range=[0,100], gridcolor=border,
                           ticksuffix="%", color=subtext),
                xaxis=dict(gridcolor=card_bg, color=subtext),
                margin=dict(t=20, b=20),
                height=280,
                font=dict(family="Inter", size=13, color=text)
            )
            st.plotly_chart(fig, use_container_width=True, key="dash_bar")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### ⚙️ System Status")
        st.markdown("<br>", unsafe_allow_html=True)
        systems = [
            ("Diabetes AI Model", "Active"),
            ("Heart Disease Model", "Active"),
            ("Patient Database", "Connected"),
            ("Appointments System", "Ready"),
            ("Report Summarizer", "Ready"),
        ]
        for name, status in systems:
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between;
                        align-items:center; padding:10px 0;
                        border-bottom:1px solid {border}'>
                <span style='color:{text}; font-size:14px'>{name}</span>
                <span style='background:#DCFCE7; color:#166534;
                             padding:3px 10px; border-radius:20px;
                             font-size:12px; font-weight:600'>
                    ● {status}
                </span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ── Analytics ─────────────────────────────────
elif page == "📊  Analytics":
    from database import get_analytics, get_recent_diagnoses, get_recent_patients
    st.markdown(f"""
    <div class='nav-bar'>
        <div>
            <div style='font-size:20px; font-weight:700; color:{text}'>
                Analytics Dashboard
            </div>
            <div style='font-size:13px; color:{subtext}'>
                Platform insights and statistics
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    analytics = get_analytics()

    # Disease distribution
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### 🔬 Diagnoses by Disease")
        if analytics["diseases"]:
            disease_counts = Counter(
                [d["disease"] for d in analytics["diseases"]]
            )
            fig = px.pie(
                values=list(disease_counts.values()),
                names=list(disease_counts.keys()),
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(
                paper_bgcolor=card_bg,
                font=dict(family="Inter", color=text),
                margin=dict(t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True,
                          key="analytics_pie")
        else:
            st.info("No diagnoses recorded yet!")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### 📊 Positive vs Negative Cases")
        if analytics["positive"] + analytics["negative"] > 0:
            fig = go.Figure(go.Bar(
                x=["Positive Cases", "Negative Cases"],
                y=[analytics["positive"], analytics["negative"]],
                marker_color=["#E74C3C", "#27AE60"],
                text=[analytics["positive"], analytics["negative"]],
                textposition="outside"
            ))
            fig.update_layout(
                plot_bgcolor=card_bg,
                paper_bgcolor=card_bg,
                font=dict(family="Inter", color=text),
                margin=dict(t=20, b=20),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True,
                          key="analytics_bar")
        else:
            st.info("No diagnoses recorded yet!")
        st.markdown("</div>", unsafe_allow_html=True)

    # Recent activity
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### 👥 Recent Patients")
        recent_patients = get_recent_patients()
        if len(recent_patients) > 0:
            st.dataframe(
                recent_patients[["id", "name", "age",
                                "gender", "created_at"]],
                use_container_width=True
            )
        else:
            st.info("No patients registered yet!")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### 🔬 Recent Diagnoses")
        recent_dx = get_recent_diagnoses()
        if len(recent_dx) > 0:
            st.dataframe(
                recent_dx[["disease", "prediction",
                           "confidence", "date"]],
                use_container_width=True
            )
        else:
            st.info("No diagnoses recorded yet!")
        st.markdown("</div>", unsafe_allow_html=True)

    # Appointment stats
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("#### 📅 Appointment Status Distribution")
    if analytics["appointments"]:
        apt_counts = Counter(
            [a["status"] for a in analytics["appointments"]]
        )
        fig = px.bar(
            x=list(apt_counts.keys()),
            y=list(apt_counts.values()),
            color=list(apt_counts.keys()),
            color_discrete_map={
                "Scheduled": "#3498DB",
                "Completed": "#27AE60",
                "Cancelled": "#E74C3C"
            }
        )
        fig.update_layout(
            plot_bgcolor=card_bg,
            paper_bgcolor=card_bg,
            font=dict(family="Inter", color=text),
            margin=dict(t=20, b=20),
            height=250,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True,
                      key="apt_bar")
    else:
        st.info("No appointments recorded yet!")
    st.markdown("</div>", unsafe_allow_html=True)

# ── Disease Prediction ─────────────────────────
elif page == "🔬  Disease Prediction":
    st.markdown(f"""
    <div class='nav-bar'>
        <div>
            <div style='font-size:20px; font-weight:700; color:{text}'>
                Disease Prediction
            </div>
            <div style='font-size:13px; color:{subtext}'>
                AI-powered clinical decision support
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🩸  Diabetes",
        "❤️  Cardiac",
        "🫘  Kidney",
        "🩺  Liver",
        "🧠  Parkinson's"
    ])

    # ── Diabetes Tab ───────────────────────────
    with tab1:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### Patient Clinical Data — Diabetes")
        st.markdown("<br>", unsafe_allow_html=True)

        patient_name_d = st.text_input(
            "Patient Name (optional)", key="d_name"
        )
        col1, col2 = st.columns(2)
        with col1:
            pregnancies = st.number_input("Pregnancies", 0, 20, 0)
            glucose = st.number_input("Glucose Level (mg/dL)", 0, 300, 120)
            blood_pressure = st.number_input(
                "Blood Pressure (mm Hg)", 0, 150, 70
            )
            skin_thickness = st.number_input("Skin Thickness (mm)", 0, 100, 20)
        with col2:
            insulin = st.number_input("Insulin (mu U/ml)", 0, 900, 80)
            bmi = st.number_input("BMI", 0.0, 70.0, 25.0)
            dpf = st.number_input(
                "Diabetes Pedigree Function", 0.0, 3.0, 0.5
            )
            age = st.number_input("Patient Age", 1, 120, 30)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Run Diabetes Analysis", use_container_width=True,
                     key="run_diabetes"):
            with st.spinner("Processing..."):
                result, confidence = predict_diabetes([
                    pregnancies, glucose, blood_pressure,
                    skin_thickness, insulin, bmi, dpf, age
                ])

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("### 📊 Diagnosis Results")
                col1, col2 = st.columns([2, 1])
                with col1:
                    if result == "Positive":
                        st.error("**Diagnosis: Diabetes Risk Detected**")
                        st.warning(
                            "Recommend immediate physician consultation."
                        )
                    else:
                        st.success(
                            "**Diagnosis: No Diabetes Risk Detected**"
                        )
                        st.info(
                            "Patient shows no significant diabetes markers."
                        )
                with col2:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=confidence,
                        number={"suffix": "%"},
                        title={"text": "Confidence",
                               "font": {"size": 14}},
                        gauge={
                            "axis": {"range": [0, 100]},
                            "bar": {"color": "#0066CC",
                                    "thickness": 0.3},
                            "bgcolor": card_bg,
                            "borderwidth": 0,
                            "steps": [
                                {"range": [0, 60],
                                 "color": "#F0F4F8"},
                                {"range": [60, 80],
                                 "color": "#DBEAFE"},
                                {"range": [80, 100],
                                 "color": "#BFDBFE"}
                            ]
                        }
                    ))
                    fig.update_layout(
                        height=200,
                        margin=dict(t=30, b=0, l=10, r=10),
                        paper_bgcolor=card_bg,
                        font=dict(family="Inter", color=text)
                    )
                    st.plotly_chart(fig, use_container_width=True,
                                   key="d_gauge")

                # SHAP
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("#### 🧠 AI Explainability")
                sorted_features = explain_diabetes([
                    pregnancies, glucose, blood_pressure,
                    skin_thickness, insulin, bmi, dpf, age
                ])
                shap_df = pd.DataFrame(
                    sorted_features, columns=["Feature", "Impact"]
                )
                fig_shap = px.bar(
                    shap_df, x="Impact", y="Feature",
                    orientation="h", color="Impact",
                    color_continuous_scale=["#DBEAFE", "#0066CC"],
                    title="Feature Importance"
                )
                fig_shap.update_layout(
                    plot_bgcolor=card_bg,
                    paper_bgcolor=card_bg,
                    height=300,
                    margin=dict(t=40, b=20),
                    font=dict(family="Inter", size=12, color=text),
                    showlegend=False,
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_shap, use_container_width=True,
                               key="d_shap")

                # Save diagnosis
                if patient_name_d:
                    add_diagnosis(0, "Diabetes", result, confidence)

                # Download report
                pdf_data = generate_pdf_report(
                    patient_name_d or "Unknown",
                    "Diabetes", result, confidence,
                    sorted_features,
                    st.session_state.username,
                    ""
                )
                st.download_button(
                    "📥 Download PDF Report",
                    data=pdf_data,
                    file_name=f"diabetes_report_{time.strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    key="d_download"
                )

                # Medication suggestions
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("#### 💊 AI Medication Suggestions")
                with st.spinner("Getting AI recommendations..."):
                    suggestions = get_medication_suggestions(
                        "Diabetes",
                        result,
                        f"Age: {age}, BMI: {bmi}, Glucose: {glucose}"
                    )
                    st.markdown(f"""
                    <div style='background:{card_bg}; padding:20px;
                                border-radius:8px;
                                border-left:4px solid #0066CC'>
                        {suggestions}
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Cardiac Tab ────────────────────────────
    with tab2:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### Patient Clinical Data — Cardiac")
        st.markdown("<br>", unsafe_allow_html=True)

        patient_name_h = st.text_input(
            "Patient Name (optional)", key="h_name"
        )
        col1, col2 = st.columns(2)
        with col1:
            age_h = st.number_input("Patient Age", 1, 120, 50, key="h_age")
            sex = st.selectbox(
                "Sex", [0, 1],
                format_func=lambda x: "Female" if x == 0 else "Male"
            )
            cp = st.number_input("Chest Pain Type (0-3)", 0, 3, 0)
            trestbps = st.number_input(
                "Resting Blood Pressure", 0, 250, 120
            )
            chol = st.number_input(
                "Serum Cholesterol (mg/dl)", 0, 600, 200
            )
            fbs = st.selectbox(
                "Fasting Blood Sugar > 120 mg/dl", [0, 1]
            )
            restecg = st.number_input(
                "Resting ECG Results (0-2)", 0, 2, 0
            )
        with col2:
            thalach = st.number_input("Maximum Heart Rate", 0, 250, 150)
            exang = st.selectbox("Exercise Induced Angina", [0, 1])
            oldpeak = st.number_input("ST Depression", 0.0, 10.0, 0.0)
            slope = st.number_input(
                "Slope of ST Segment (0-2)", 0, 2, 1
            )
            ca = st.number_input("Major Vessels (0-3)", 0, 3, 0)
            thal = st.number_input("Thalassemia (0-3)", 0, 3, 2)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Run Cardiac Analysis",
                     use_container_width=True, key="run_cardiac"):
            with st.spinner("Processing..."):
                result, confidence = predict_heart([
                    age_h, sex, cp, trestbps, chol, fbs,
                    restecg, thalach, exang, oldpeak, slope, ca, thal
                ])

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("### 📊 Diagnosis Results")
                col1, col2 = st.columns([2, 1])
                with col1:
                    if result == "Positive":
                        st.error(
                            "**Diagnosis: Cardiac Risk Detected**"
                        )
                        st.warning(
                            "Recommend immediate cardiologist referral."
                        )
                    else:
                        st.success(
                            "**Diagnosis: No Cardiac Risk Detected**"
                        )
                        st.info(
                            "No significant cardiac risk markers."
                        )
                with col2:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=confidence,
                        number={"suffix": "%"},
                        title={"text": "Confidence",
                               "font": {"size": 14}},
                        gauge={
                            "axis": {"range": [0, 100]},
                            "bar": {"color": "#00897B",
                                    "thickness": 0.3},
                            "bgcolor": card_bg,
                            "borderwidth": 0,
                            "steps": [
                                {"range": [0, 60],
                                 "color": "#F0FDF4"},
                                {"range": [60, 80],
                                 "color": "#DCFCE7"},
                                {"range": [80, 100],
                                 "color": "#BBF7D0"}
                            ]
                        }
                    ))
                    fig.update_layout(
                        height=200,
                        margin=dict(t=30, b=0, l=10, r=10),
                        paper_bgcolor=card_bg,
                        font=dict(family="Inter", color=text)
                    )
                    st.plotly_chart(fig, use_container_width=True,
                                   key="h_gauge")

                # SHAP
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("#### 🧠 AI Explainability")
                sorted_features = explain_heart([
                    age_h, sex, cp, trestbps, chol, fbs,
                    restecg, thalach, exang, oldpeak, slope, ca, thal
                ])
                shap_df = pd.DataFrame(
                    sorted_features, columns=["Feature", "Impact"]
                )
                fig_heart = px.bar(
                    shap_df, x="Impact", y="Feature",
                    orientation="h", color="Impact",
                    color_continuous_scale=["#DCFCE7", "#00897B"],
                    title="Feature Importance — Cardiac"
                )
                fig_heart.update_layout(
                    plot_bgcolor=card_bg,
                    paper_bgcolor=card_bg,
                    height=300,
                    margin=dict(t=40, b=20),
                    font=dict(family="Inter", size=12, color=text),
                    showlegend=False,
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_heart, use_container_width=True,
                               key="h_shap")

                # Save diagnosis
                if patient_name_h:
                    add_diagnosis(0, "Heart Disease", result, confidence)

                # Download report
                pdf_data = generate_pdf_report(
                    patient_name_d or "Unknown",
                    "Cardiac", result, confidence,
                    sorted_features,
                    st.session_state.username,
                    ""
                )
                st.download_button(
                    "📥 Download PDF Report",
                    data=pdf_data,
                    file_name=f"cardiac_report_{time.strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    key="d_download"
                )

                # Medication suggestions
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("#### 💊 AI Medication Suggestions")
                with st.spinner("Getting AI recommendations..."):
                    suggestions = get_medication_suggestions(
                        "Heart Disease",
                        result,
                        f"Age: {age_h}, Cholesterol: {chol}, BP: {trestbps}"
                    )
                    st.markdown(f"""
                    <div style='background:{card_bg}; padding:20px;
                                border-radius:8px;
                                border-left:4px solid #00897B'>
                        {suggestions}
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# ── Kidney Tab ─────────────────────────────
    with tab3:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### Patient Clinical Data — Kidney Disease")
        st.markdown("<br>", unsafe_allow_html=True)
        patient_name_k = st.text_input("Patient Name (optional)", key="k_name")
        col1, col2 = st.columns(2)
        with col1:
            age_k = st.number_input("Age", 1, 120, 40, key="k_age")
            bp_k = st.number_input("Blood Pressure (mm/Hg)", 0, 200, 80, key="k_bp")
            bgr_k = st.number_input("Blood Glucose Random (mgs/dl)", 0, 500, 120, key="k_bgr")
            bu_k = st.number_input("Blood Urea (mgs/dl)", 0, 200, 30, key="k_bu")
            sc_k = st.number_input("Serum Creatinine (mgs/dl)", 0.0, 20.0, 1.0, key="k_sc")
            sod_k = st.number_input("Sodium (mEq/L)", 0, 200, 140, key="k_sod")
        with col2:
            pot_k = st.number_input("Potassium (mEq/L)", 0.0, 10.0, 4.0, key="k_pot")
            hemo_k = st.number_input("Hemoglobin (gms)", 0.0, 20.0, 12.0, key="k_hemo")
            pcv_k = st.number_input("Packed Cell Volume", 0, 60, 40, key="k_pcv")
            wc_k = st.number_input("White Blood Cell Count (cells/cumm)", 0, 20000, 8000, key="k_wc")
            rc_k = st.number_input("Red Blood Cell Count (millions/cmm)", 0.0, 10.0, 4.5, key="k_rc")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Run Kidney Analysis", use_container_width=True, key="run_kidney"):
            with st.spinner("Processing..."):
                result, confidence = predict_kidney([
                    age_k, bp_k, bgr_k, bu_k, sc_k,
                    sod_k, pot_k, hemo_k, pcv_k, wc_k, rc_k
                ])
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("### 📊 Diagnosis Results")
                col1, col2 = st.columns([2, 1])
                with col1:
                    if result == "Positive":
                        st.error("**Diagnosis: Chronic Kidney Disease Detected**")
                        st.warning("Recommend immediate nephrologist consultation.")
                    else:
                        st.success("**Diagnosis: No Kidney Disease Detected**")
                        st.info("Patient shows no significant kidney disease markers.")
                with col2:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=confidence,
                        number={"suffix": "%"},
                        title={"text": "Confidence", "font": {"size": 14}},
                        gauge={
                            "axis": {"range": [0, 100]},
                            "bar": {"color": "#7B1FA2", "thickness": 0.3},
                            "bgcolor": card_bg,
                            "borderwidth": 0,
                            "steps": [
                                {"range": [0, 60], "color": "#F3E5F5"},
                                {"range": [60, 80], "color": "#CE93D8"},
                                {"range": [80, 100], "color": "#AB47BC"}
                            ]
                        }
                    ))
                    fig.update_layout(
                        height=200,
                        margin=dict(t=30, b=0, l=10, r=10),
                        paper_bgcolor=card_bg,
                        font=dict(family="Inter", color=text)
                    )
                    st.plotly_chart(fig, use_container_width=True, key="k_gauge")

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("#### 🧠 AI Explainability")
                sorted_features = explain_kidney([
                    age_k, bp_k, bgr_k, bu_k, sc_k,
                    sod_k, pot_k, hemo_k, pcv_k, wc_k, rc_k
                ])
                shap_df = pd.DataFrame(sorted_features, columns=["Feature", "Impact"])
                fig_k = px.bar(
                    shap_df, x="Impact", y="Feature", orientation="h",
                    color="Impact",
                    color_continuous_scale=["#F3E5F5", "#7B1FA2"],
                    title="Feature Importance — Kidney"
                )
                fig_k.update_layout(
                    plot_bgcolor=card_bg, paper_bgcolor=card_bg,
                    height=300, margin=dict(t=40, b=20),
                    font=dict(family="Inter", size=12, color=text),
                    showlegend=False, coloraxis_showscale=False
                )
                st.plotly_chart(fig_k, use_container_width=True, key="k_shap")

                if patient_name_k:
                    add_diagnosis(0, "Kidney Disease", result, confidence)

                pdf_data = generate_pdf_report(
                    patient_name_d or "Unknown",
                    "Kidney", result, confidence,
                    sorted_features,
                    st.session_state.username,
                    ""
                )
                st.download_button(
                    "📥 Download PDF Report",
                    data=pdf_data,
                    file_name=f"kidney_report_{time.strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    key="d_download"
                )

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("#### 💊 AI Medication Suggestions")
                with st.spinner("Getting recommendations..."):
                    suggestions = get_medication_suggestions(
                        "Kidney Disease", result,
                        f"Age: {age_k}, Creatinine: {sc_k}, Hemoglobin: {hemo_k}"
                    )
                    st.markdown(suggestions)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Liver Tab ──────────────────────────────
    with tab4:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### Patient Clinical Data — Liver Disease")
        st.markdown("<br>", unsafe_allow_html=True)
        patient_name_l = st.text_input("Patient Name (optional)", key="l_name")
        col1, col2 = st.columns(2)
        with col1:
            age_l = st.number_input("Age", 1, 120, 40, key="l_age")
            gender_l = st.selectbox("Gender", [0, 1],
                format_func=lambda x: "Female" if x == 0 else "Male", key="l_gender")
            total_bilirubin = st.number_input("Total Bilirubin", 0.0, 80.0, 1.0, key="l_tb")
            direct_bilirubin = st.number_input("Direct Bilirubin", 0.0, 20.0, 0.3, key="l_db")
            alkaline_phosphotase = st.number_input("Alkaline Phosphotase", 0, 2000, 200, key="l_ap")
        with col2:
            alamine = st.number_input("Alamine Aminotransferase", 0, 2000, 35, key="l_alt")
            aspartate = st.number_input("Aspartate Aminotransferase", 0, 5000, 35, key="l_ast")
            total_proteins = st.number_input("Total Proteins", 0.0, 10.0, 6.5, key="l_tp")
            albumin = st.number_input("Albumin", 0.0, 6.0, 3.5, key="l_alb")
            ag_ratio = st.number_input("Albumin/Globulin Ratio", 0.0, 3.0, 1.0, key="l_agr")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Run Liver Analysis", use_container_width=True, key="run_liver"):
            with st.spinner("Processing..."):
                result, confidence = predict_liver([
                    age_l, gender_l, total_bilirubin, direct_bilirubin,
                    alkaline_phosphotase, alamine, aspartate,
                    total_proteins, albumin, ag_ratio
                ])
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("### 📊 Diagnosis Results")
                col1, col2 = st.columns([2, 1])
                with col1:
                    if result == "Positive":
                        st.error("**Diagnosis: Liver Disease Detected**")
                        st.warning("Recommend immediate hepatologist consultation.")
                    else:
                        st.success("**Diagnosis: No Liver Disease Detected**")
                        st.info("Patient shows no significant liver disease markers.")
                with col2:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=confidence,
                        number={"suffix": "%"},
                        title={"text": "Confidence", "font": {"size": 14}},
                        gauge={
                            "axis": {"range": [0, 100]},
                            "bar": {"color": "#F57C00", "thickness": 0.3},
                            "bgcolor": card_bg,
                            "borderwidth": 0,
                            "steps": [
                                {"range": [0, 60], "color": "#FFF3E0"},
                                {"range": [60, 80], "color": "#FFCC80"},
                                {"range": [80, 100], "color": "#FFA726"}
                            ]
                        }
                    ))
                    fig.update_layout(
                        height=200,
                        margin=dict(t=30, b=0, l=10, r=10),
                        paper_bgcolor=card_bg,
                        font=dict(family="Inter", color=text)
                    )
                    st.plotly_chart(fig, use_container_width=True, key="l_gauge")

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("#### 🧠 AI Explainability")
                sorted_features = explain_liver([
                    age_l, gender_l, total_bilirubin, direct_bilirubin,
                    alkaline_phosphotase, alamine, aspartate,
                    total_proteins, albumin, ag_ratio
                ])
                shap_df = pd.DataFrame(sorted_features, columns=["Feature", "Impact"])
                fig_l = px.bar(
                    shap_df, x="Impact", y="Feature", orientation="h",
                    color="Impact",
                    color_continuous_scale=["#FFF3E0", "#F57C00"],
                    title="Feature Importance — Liver"
                )
                fig_l.update_layout(
                    plot_bgcolor=card_bg, paper_bgcolor=card_bg,
                    height=300, margin=dict(t=40, b=20),
                    font=dict(family="Inter", size=12, color=text),
                    showlegend=False, coloraxis_showscale=False
                )
                st.plotly_chart(fig_l, use_container_width=True, key="l_shap")

                if patient_name_l:
                    add_diagnosis(0, "Liver Disease", result, confidence)

                pdf_data = generate_pdf_report(
                    patient_name_d or "Unknown",
                    "Liver", result, confidence,
                    sorted_features,
                    st.session_state.username,
                    ""
                )
                st.download_button(
                    "📥 Download PDF Report",
                    data=pdf_data,
                    file_name=f"liver_report_{time.strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    key="d_download"
                )
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("#### 💊 AI Medication Suggestions")
                with st.spinner("Getting recommendations..."):
                    suggestions = get_medication_suggestions(
                        "Liver Disease", result,
                        f"Age: {age_l}, Bilirubin: {total_bilirubin}, Albumin: {albumin}"
                    )
                    st.markdown(suggestions)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Parkinson's Tab ────────────────────────
    with tab5:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### Patient Clinical Data — Parkinson's Disease")
        st.info("Enter voice measurement values from clinical assessment")
        st.markdown("<br>", unsafe_allow_html=True)
        patient_name_p = st.text_input("Patient Name (optional)", key="p_name")
        col1, col2 = st.columns(2)
        with col1:
            fo = st.number_input("MDVP Fo Hz (Avg vocal freq)", 80.0, 270.0, 154.0, key="p_fo")
            fhi = st.number_input("MDVP Fhi Hz (Max vocal freq)", 100.0, 600.0, 197.0, key="p_fhi")
            flo = st.number_input("MDVP Flo Hz (Min vocal freq)", 60.0, 240.0, 116.0, key="p_flo")
            jitter_percent = st.number_input("MDVP Jitter %", 0.0, 1.0, 0.006, format="%.4f", key="p_jp")
            jitter_abs = st.number_input("MDVP Jitter Abs", 0.0, 0.01, 0.00004, format="%.5f", key="p_ja")
            rap = st.number_input("MDVP RAP", 0.0, 0.1, 0.003, format="%.4f", key="p_rap")
            ppq = st.number_input("MDVP PPQ", 0.0, 0.1, 0.003, format="%.4f", key="p_ppq")
            ddp = st.number_input("Jitter DDP", 0.0, 0.1, 0.009, format="%.4f", key="p_ddp")
            shimmer = st.number_input("MDVP Shimmer", 0.0, 1.0, 0.03, format="%.4f", key="p_sh")
            shimmer_db = st.number_input("MDVP Shimmer dB", 0.0, 3.0, 0.28, key="p_shdb")
            apq3 = st.number_input("Shimmer APQ3", 0.0, 0.1, 0.015, format="%.4f", key="p_apq3")
        with col2:
            apq5 = st.number_input("Shimmer APQ5", 0.0, 0.2, 0.02, format="%.4f", key="p_apq5")
            apq = st.number_input("MDVP APQ", 0.0, 0.2, 0.024, format="%.4f", key="p_apq")
            dda = st.number_input("Shimmer DDA", 0.0, 0.2, 0.046, format="%.4f", key="p_dda")
            nhr = st.number_input("NHR", 0.0, 0.5, 0.025, format="%.4f", key="p_nhr")
            hnr = st.number_input("HNR", 0.0, 35.0, 21.0, key="p_hnr")
            rpde = st.number_input("RPDE", 0.0, 1.0, 0.5, key="p_rpde")
            dfa = st.number_input("DFA", 0.0, 1.0, 0.72, key="p_dfa")
            spread1 = st.number_input("Spread1", -10.0, 0.0, -5.7, key="p_s1")
            spread2 = st.number_input("Spread2", 0.0, 0.5, 0.22, key="p_s2")
            d2 = st.number_input("D2", 0.0, 4.0, 2.3, key="p_d2")
            ppe = st.number_input("PPE", 0.0, 0.5, 0.18, key="p_ppe")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Run Parkinson's Analysis",
                     use_container_width=True, key="run_parkinsons"):
            with st.spinner("Processing..."):
                result, confidence = predict_parkinsons([
                    fo, fhi, flo, jitter_percent, jitter_abs,
                    rap, ppq, ddp, shimmer, shimmer_db,
                    apq3, apq5, apq, dda, nhr, hnr,
                    rpde, dfa, spread1, spread2, d2, ppe
                ])
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("### 📊 Diagnosis Results")
                col1, col2 = st.columns([2, 1])
                with col1:
                    if result == "Positive":
                        st.error("**Diagnosis: Parkinson's Disease Detected**")
                        st.warning("Recommend immediate neurologist consultation.")
                    else:
                        st.success("**Diagnosis: No Parkinson's Disease Detected**")
                        st.info("Patient shows no significant Parkinson's markers.")
                with col2:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=confidence,
                        number={"suffix": "%"},
                        title={"text": "Confidence", "font": {"size": 14}},
                        gauge={
                            "axis": {"range": [0, 100]},
                            "bar": {"color": "#1565C0", "thickness": 0.3},
                            "bgcolor": card_bg,
                            "borderwidth": 0,
                            "steps": [
                                {"range": [0, 60], "color": "#E3F2FD"},
                                {"range": [60, 80], "color": "#90CAF9"},
                                {"range": [80, 100], "color": "#42A5F5"}
                            ]
                        }
                    ))
                    fig.update_layout(
                        height=200,
                        margin=dict(t=30, b=0, l=10, r=10),
                        paper_bgcolor=card_bg,
                        font=dict(family="Inter", color=text)
                    )
                    st.plotly_chart(fig, use_container_width=True, key="p_gauge")

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("#### 🧠 AI Explainability")
                sorted_features = explain_parkinsons([
                    fo, fhi, flo, jitter_percent, jitter_abs,
                    rap, ppq, ddp, shimmer, shimmer_db,
                    apq3, apq5, apq, dda, nhr, hnr,
                    rpde, dfa, spread1, spread2, d2, ppe
                ])
                shap_df = pd.DataFrame(sorted_features, columns=["Feature", "Impact"])
                fig_p = px.bar(
                    shap_df.head(10), x="Impact", y="Feature",
                    orientation="h", color="Impact",
                    color_continuous_scale=["#E3F2FD", "#1565C0"],
                    title="Top 10 Feature Importance — Parkinson's"
                )
                fig_p.update_layout(
                    plot_bgcolor=card_bg, paper_bgcolor=card_bg,
                    height=300, margin=dict(t=40, b=20),
                    font=dict(family="Inter", size=12, color=text),
                    showlegend=False, coloraxis_showscale=False
                )
                st.plotly_chart(fig_p, use_container_width=True, key="p_shap")

                if patient_name_p:
                    add_diagnosis(0, "Parkinson's Disease", result, confidence)

                pdf_data = generate_pdf_report(
                    patient_name_d or "Unknown",
                    "Parkinsons", result, confidence,
                    sorted_features,
                    st.session_state.username,
                    ""
                )
                st.download_button(
                    "📥 Download PDF Report",
                    data=pdf_data,
                    file_name=f"parkinsons_report_{time.strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    key="d_download"
                )

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("#### 💊 AI Medication Suggestions")
                with st.spinner("Getting recommendations..."):
                    suggestions = get_medication_suggestions(
                        "Parkinson's Disease", result,
                        f"Voice HNR: {hnr}, RPDE: {rpde}, DFA: {dfa}"
                    )
                    st.markdown(suggestions)
        st.markdown("</div>", unsafe_allow_html=True)

# ── Patient Management ─────────────────────────
elif page == "👥  Patient Management":
    st.markdown(f"""
    <div class='nav-bar'>
        <div>
            <div style='font-size:20px; font-weight:700; color:{text}'>
                Patient Management
            </div>
            <div style='font-size:13px; color:{subtext}'>
                Register, search, edit and manage patient records
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "➕  New Patient",
        "🔍  Search & Edit",
        "📋  All Patients"
    ])

    with tab1:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### Register New Patient")
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", key="new_name")
            age = st.number_input("Age", 1, 120, 25, key="new_age")
            gender = st.selectbox(
                "Gender", ["Male", "Female", "Other"], key="new_gender"
            )
            blood_group = st.selectbox(
                "Blood Group",
                ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"],
                key="new_bg"
            )
        with col2:
            contact = st.text_input("Contact Number", key="new_contact")
            email = st.text_input("Email Address", key="new_email")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Register Patient",
                     use_container_width=True, key="reg_patient"):
            if name:
                pid = add_patient(
                    name, age, gender, blood_group, contact, email
                )
                st.success(
                    f"Patient **{name}** registered! ID: **{pid}**"
                )
            else:
                st.warning("Patient name is required!")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### 🔍 Search Patient")
        search_query = st.text_input(
            "Search by name or patient ID",
            placeholder="Type name or ID...",
            key="search_q"
        )
        if search_query:
            results = search_patients(search_query)
            if len(results) > 0:
                st.success(f"Found {len(results)} patient(s)")
                st.dataframe(results, use_container_width=True)

                st.markdown("#### ✏️ Edit Patient")
                patient_id = st.number_input(
                    "Enter Patient ID to edit",
                    min_value=1, key="edit_id"
                )
                patient_row = results[results["id"] == patient_id]
                if len(patient_row) > 0:
                    p = patient_row.iloc[0]
                    col1, col2 = st.columns(2)
                    with col1:
                        e_name = st.text_input(
                            "Full Name", value=p["name"], key="e_name"
                        )
                        e_age = st.number_input(
                            "Age", 1, 120,
                            int(p["age"]), key="e_age"
                        )
                        e_gender = st.selectbox(
                            "Gender",
                            ["Male", "Female", "Other"],
                            index=["Male", "Female", "Other"].index(
                                p["gender"]
                            ) if p["gender"] in [
                                "Male", "Female", "Other"
                            ] else 0,
                            key="e_gender"
                        )
                        e_bg = st.selectbox(
                            "Blood Group",
                            ["A+","A-","B+","B-","O+","O-","AB+","AB-"],
                            key="e_bg"
                        )
                    with col2:
                        e_contact = st.text_input(
                            "Contact",
                            value=p["contact"] or "",
                            key="e_contact"
                        )
                        e_email = st.text_input(
                            "Email",
                            value=p["email"] or "",
                            key="e_email"
                        )

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("💾 Save Changes",
                                     use_container_width=True,
                                     key="save_edit"):
                            update_patient(
                                patient_id, e_name, e_age,
                                e_gender, e_bg, e_contact, e_email
                            )
                            st.success("Patient updated successfully!")
                    with col2:
                        if st.button("🗑️ Delete Patient",
                                     use_container_width=True,
                                     key="del_patient"):
                            delete_patient(patient_id)
                            st.success("Patient deleted!")
                            st.rerun()
            else:
                st.info("No patients found!")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### All Patient Records")
        df = get_all_patients()
        if len(df) > 0:
            st.dataframe(df, use_container_width=True, height=400)
            st.markdown(f"""
            <p style='color:{subtext}; font-size:13px'>
                Total: {len(df)} patients
            </p>
            """, unsafe_allow_html=True)
        else:
            st.info("No patients registered yet!")
        st.markdown("</div>", unsafe_allow_html=True)

# ── Appointments ───────────────────────────────
elif page == "📅  Appointments":
    from database import (get_all_doctors, get_booked_slots,
                          add_appointment, get_all_appointments,
                          update_appointment_status, cancel_appointment)
    import datetime as dt

    st.markdown(f"""
    <div class='nav-bar'>
        <div>
            <div style='font-size:20px; font-weight:700; color:{text}'>
                Appointment Booking
            </div>
            <div style='font-size:13px; color:{subtext}'>
                Book and manage patient appointments
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "📅 Book Appointment",
        "📋 All Appointments",
        "🔍 Find My Appointment"
    ])

    with tab1:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### 👨‍⚕️ Select Doctor")

        doctors_df = get_all_doctors()
        if len(doctors_df) == 0:
            st.warning("No doctors available!")
        else:
            # Doctor cards
            cols = st.columns(3)
            selected_doctor_id = st.session_state.get(
                "selected_doctor_id", None
            )
            selected_doctor_name = st.session_state.get(
                "selected_doctor_name", None
            )
            selected_dept = st.session_state.get(
                "selected_dept", None
            )

            for i, (_, doc) in enumerate(doctors_df.iterrows()):
                with cols[i % 3]:
                    is_selected = selected_doctor_id == doc["id"]
                    border_color = "#0066CC" if is_selected else border
                    st.markdown(f"""
                    <div style='border:2px solid {border_color};
                                border-radius:12px; padding:15px;
                                background:{card_bg}; margin-bottom:10px;
                                cursor:pointer'>
                        <div style='font-size:20px; text-align:center'>
                            👨‍⚕️
                        </div>
                        <div style='font-weight:600; color:{text};
                                    font-size:14px; text-align:center'>
                            {doc['name']}
                        </div>
                        <div style='color:#0066CC; font-size:12px;
                                    text-align:center'>
                            {doc['specialization']}
                        </div>
                        <div style='color:{subtext}; font-size:11px;
                                    text-align:center'>
                            {doc['experience']} years exp.
                        </div>
                        <div style='color:{subtext}; font-size:10px;
                                    text-align:center; margin-top:4px'>
                            {doc.get('qualification', '')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(
                        "✅ Selected" if is_selected else "Select",
                        key=f"doc_{doc['id']}",
                        use_container_width=True
                    ):
                        st.session_state.selected_doctor_id = int(doc["id"])
                        st.session_state.selected_doctor_name = doc["name"]
                        st.session_state.selected_dept = doc["specialization"]
                        st.rerun()

            if selected_doctor_id:
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown(f"#### 📅 Book with {selected_doctor_name}")

                col1, col2 = st.columns(2)
                with col1:
                    apt_patient = st.text_input(
                        "Patient Full Name *",
                        placeholder="Enter patient name",
                        key="apt_patient"
                    )
                    apt_email = st.text_input(
                        "Patient Email",
                        placeholder="For confirmation email",
                        key="apt_email"
                    )
                    apt_phone = st.text_input(
                        "Patient Phone",
                        placeholder="+91 XXXXX XXXXX",
                        key="apt_phone"
                    )

                with col2:
                    min_date = dt.date.today() + dt.timedelta(days=1)
                    max_date = dt.date.today() + dt.timedelta(days=30)
                    apt_date = st.date_input(
                        "Appointment Date *",
                        min_value=min_date,
                        max_value=max_date,
                        key="apt_date"
                    )

                    # Get booked slots
                    booked = get_booked_slots(selected_doctor_id, apt_date)
                    all_slots = [
                        "09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM",
                        "11:00 AM", "11:30 AM", "12:00 PM",
                        "02:00 PM", "02:30 PM", "03:00 PM",
                        "03:30 PM", "04:00 PM", "04:30 PM"
                    ]
                    available_slots = [
                        s for s in all_slots if s not in booked
                    ]

                    if available_slots:
                        st.markdown(f"""
                        <p style='color:{subtext}; font-size:12px'>
                        ✅ {len(available_slots)} slots available on {apt_date}
                        </p>
                        """, unsafe_allow_html=True)
                        apt_time = st.selectbox(
                            "Available Time Slots *",
                            available_slots,
                            key="apt_time"
                        )
                    else:
                        st.error("❌ No slots available on this date!")
                        apt_time = None

                    # Show booked slots
                    if booked:
                        st.markdown(f"""
                        <p style='color:#E74C3C; font-size:11px'>
                        🔴 Booked: {', '.join(booked)}
                        </p>
                        """, unsafe_allow_html=True)

                apt_reason = st.text_area(
                    "Reason for Visit",
                    placeholder="Describe symptoms or reason...",
                    height=80,
                    key="apt_reason"
                )

                st.markdown("<br>", unsafe_allow_html=True)
                if st.button(
                    "📅 Confirm Appointment",
                    use_container_width=True,
                    key="book_apt"
                ):
                    if apt_patient and apt_time:
                        booking_id = add_appointment(
                            apt_patient,
                            selected_doctor_id,
                            selected_doctor_name,
                            selected_dept,
                            apt_date,
                            apt_time,
                            apt_reason,
                            apt_email,
                            apt_phone
                        )
                        st.success(f"""
                        ✅ **Appointment Confirmed!**

                        🎫 **Booking ID: {booking_id}**
                        👤 Patient: {apt_patient}
                        👨‍⚕️ Doctor: {selected_doctor_name}
                        🏥 Department: {selected_dept}
                        📅 Date: {apt_date}
                        ⏰ Time: {apt_time}

                        *Save your Booking ID for reference*
                        """)
                        if apt_email:
                            sent = appointment_email(
                                apt_patient,
                                selected_doctor_name,
                                str(apt_date),
                                apt_time,
                                apt_email
                            )
                            if sent:
                                st.info(f"📧 Confirmation sent to {apt_email}")
                        # Clear selection
                        st.session_state.selected_doctor_id = None
                        st.session_state.selected_doctor_name = None
                        st.session_state.selected_dept = None
                    else:
                        st.warning("Please fill patient name and select a time slot!")

        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### 📋 All Appointments")

        df_apt = get_all_appointments()
        if len(df_apt) > 0:
            # Filter options
            col1, col2, col3 = st.columns(3)
            with col1:
                status_filter = st.selectbox(
                    "Filter by Status",
                    ["All", "Scheduled", "Completed", "Cancelled"],
                    key="apt_status_filter"
                )
            with col2:
                doctor_filter = st.selectbox(
                    "Filter by Doctor",
                    ["All"] + list(df_apt["doctor"].unique()),
                    key="apt_doctor_filter"
                )
            with col3:
                search_apt = st.text_input(
                    "Search patient",
                    placeholder="Patient name...",
                    key="apt_search"
                )

            filtered = df_apt.copy()
            if status_filter != "All":
                filtered = filtered[
                    filtered["status"] == status_filter
                ]
            if doctor_filter != "All":
                filtered = filtered[
                    filtered["doctor"] == doctor_filter
                ]
            if search_apt:
                filtered = filtered[
                    filtered["patient_name"].str.contains(
                        search_apt, case=False, na=False
                    )
                ]

            st.dataframe(filtered, use_container_width=True, height=400)
            st.markdown(f"""
            <p style='color:{subtext}; font-size:13px'>
                Showing {len(filtered)} of {len(df_apt)} appointments
            </p>
            """, unsafe_allow_html=True)

            # Update status
            st.markdown("#### ✏️ Update Appointment Status")
            col1, col2, col3 = st.columns(3)
            with col1:
                apt_id = st.number_input(
                    "Appointment ID", min_value=1, key="apt_id_update"
                )
            with col2:
                new_status = st.selectbox(
                    "New Status",
                    ["Scheduled", "Completed", "Cancelled"],
                    key="new_status"
                )
            with col3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Update", use_container_width=True,
                            key="update_apt"):
                    update_appointment_status(apt_id, new_status)
                    st.success("✅ Status updated!")
                    st.rerun()
        else:
            st.info("No appointments yet!")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### 🔍 Find My Appointment")
        booking_search = st.text_input(
            "Enter Booking ID",
            placeholder="e.g. AB12CD34",
            key="booking_search"
        )
        if booking_search:
            df_apt = get_all_appointments()
            if len(df_apt) > 0:
                match = df_apt[
                    df_apt["booking_id"] == booking_search.upper()
                ]
                if len(match) > 0:
                    row = match.iloc[0]
                    status_color = {
                        "Scheduled": "#3498DB",
                        "Completed": "#27AE60",
                        "Cancelled": "#E74C3C"
                    }.get(row["status"], "#666")
                    st.markdown(f"""
                    <div style='background:{card_bg}; padding:24px;
                                border-radius:12px;
                                border-left:4px solid #0066CC'>
                        <h3 style='color:{text}'>Appointment Details</h3>
                        <p><b>🎫 Booking ID:</b> {row['booking_id']}</p>
                        <p><b>👤 Patient:</b> {row['patient_name']}</p>
                        <p><b>👨‍⚕️ Doctor:</b> {row['doctor']}</p>
                        <p><b>🏥 Department:</b> {row['department']}</p>
                        <p><b>📅 Date:</b> {row['date']}</p>
                        <p><b>⏰ Time:</b> {row['time']}</p>
                        <p><b>📝 Reason:</b> {row.get('reason', 'N/A')}</p>
                        <p><b>Status:</b>
                            <span style='color:{status_color};
                                         font-weight:600'>
                                ● {row['status']}
                            </span>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    if row["status"] == "Scheduled":
                        if st.button("❌ Cancel Appointment",
                                    key="cancel_apt"):
                            cancel_appointment(booking_search.upper())
                            st.success("Appointment cancelled!")
                            st.rerun()
                else:
                    st.error("❌ Booking ID not found!")
        st.markdown("</div>", unsafe_allow_html=True)

# ── Medication Suggestions ─────────────────────
elif page == "💊  Medication Suggestions":
    st.markdown(f"""
    <div class='nav-bar'>
        <div>
            <div style='font-size:20px; font-weight:700; color:{text}'>
                AI Medication Suggestions
            </div>
            <div style='font-size:13px; color:{subtext}'>
                AI-powered clinical recommendations for doctors
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.warning("⚕️ For doctor reference only. Always consult a physician.")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        med_disease = st.selectbox("Disease", [
            "Diabetes", "Heart Disease", "Hypertension",
            "Pneumonia", "Kidney Disease", "Liver Disease",
            "Thyroid Disorder", "Anemia"
        ])
        med_result = st.selectbox(
            "Diagnosis Result", ["Positive", "Negative"]
        )
    with col2:
        med_age = st.number_input("Patient Age", 1, 120, 40)
        med_gender = st.selectbox("Gender", ["Male", "Female"])
        med_notes = st.text_area(
            "Additional Notes (symptoms, vitals, etc.)",
            height=100
        )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💊 Get AI Recommendations",
                 use_container_width=True, key="get_meds"):
        with st.spinner("AI is generating recommendations..."):
            patient_info = f"""
            Age: {med_age}, Gender: {med_gender}, Notes: {med_notes}
            """
            suggestions = get_medication_suggestions(
                med_disease, med_result, patient_info
            )
            st.markdown("### 🤖 AI Clinical Recommendations")
            st.markdown("---")
            st.markdown(suggestions)

            # Download
            st.download_button(
                "📥 Download Recommendations",
                data=suggestions,
                file_name=f"medication_suggestions_{time.strftime('%Y%m%d')}.txt",
                mime="text/plain",
                key="med_download"
            )
    st.markdown("</div>", unsafe_allow_html=True)

# ── Report Summarizer ──────────────────────────
elif page == "📋  Report Summarizer":
    from PyPDF2 import PdfReader
    st.markdown(f"""
    <div class='nav-bar'>
        <div>
            <div style='font-size:20px; font-weight:700; color:{text}'>
                AI Report Summarizer
            </div>
            <div style='font-size:13px; color:{subtext}'>
                Upload medical reports for AI analysis
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload Medical Report (PDF)", type=["pdf"]
    )
    if uploaded_file:
        with st.spinner("Reading document..."):
            pdf_reader = PdfReader(uploaded_file)
            report_text = ""
            for p in pdf_reader.pages:
                report_text += p.extract_text()
        st.success(
            f"Document loaded — {len(report_text):,} characters, "
            f"{len(pdf_reader.pages)} page(s)"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🤖 Analyze Report",
                     use_container_width=True, key="analyze_report"):
            with st.spinner("AI is analyzing..."):
                model = genai.GenerativeModel("gemini-2.5-flash")
                prompt = f"""You are a clinical AI assistant.
Analyze this medical report and provide:
**1. Key Findings**
**2. Diagnosis Summary**
**3. Recommended Actions**
**4. Critical Values**
**5. Risk Assessment**

Report:
{report_text[:3000]}"""
                response = model.generate_content(prompt)
                st.markdown("#### 🤖 Clinical Analysis")
                st.markdown("---")
                st.markdown(response.text)

                st.download_button(
                    "📥 Download Analysis",
                    data=response.text,
                    file_name=f"report_analysis_{time.strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    key="report_download"
                )
    else:
        st.markdown(f"""
        <div style='text-align:center; padding:48px; color:{subtext}'>
            <div style='font-size:48px'>📋</div>
            <p>Upload a PDF medical report to begin analysis</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Settings ──────────────────────────────────
elif page == "⚙️  Settings":
    from database import update_user_email, get_user_email
    st.markdown(f"""
    <div class='nav-bar'>
        <div>
            <div style='font-size:20px; font-weight:700; color:{text}'>
                Account Settings
            </div>
            <div style='font-size:13px; color:{subtext}'>
                Manage your profile and preferences
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["👤  Profile", "🔔  Notifications"])

    with tab1:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### Update Profile")
        st.markdown(f"""
        <div style='background:{card_bg}; padding:15px;
                    border-radius:8px; border-left:4px solid #0066CC;
                    margin-bottom:20px'>
            <p style='margin:0; color:{text}'><b>Username:</b>
                {st.session_state.username}</p>
        </div>
        """, unsafe_allow_html=True)

        current_email = get_user_email(st.session_state.username)
        new_email = st.text_input(
            "Email Address",
            value=current_email or "",
            placeholder="Enter your email for notifications"
        )
        if st.button("💾 Save Email", use_container_width=True):
            if new_email:
                update_user_email(st.session_state.username, new_email)
                st.success("✅ Email saved successfully!")
            else:
                st.warning("Please enter an email address!")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### Email Notifications")
        st.info("""
        📧 Email notifications will be sent for:
        - Appointment confirmations
        - Diagnosis results
        - Important health alerts

        Add your email in the Profile tab to enable notifications.
        """)
        email = get_user_email(st.session_state.username)
        if email:
            st.success(f"✅ Notifications enabled for: **{email}**")
        else:
            st.warning("⚠️ Add your email in Profile tab to enable notifications!")
        st.markdown("</div>", unsafe_allow_html=True)
