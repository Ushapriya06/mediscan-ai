import streamlit as st
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
                <p style='color:{subtext}; margin:8px 0 0 0; font-size:14px'>
                    Medical Intelligence Platform
                </p>
            </div>
        """, unsafe_allow_html=True)

        tab_login, tab_register = st.tabs(["🔑 Login", "📝 Register"])

        with tab_login:
            st.markdown("<br>", unsafe_allow_html=True)
            username = st.text_input("Username",
                placeholder="Enter username", key="login_user")
            password = st.text_input("Password", type="password",
                placeholder="Enter password", key="login_pass")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign In", use_container_width=True, key="signin"):
                if username and password:
                    from database import verify_user
                    if verify_user(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("Invalid username or password!")
                else:
                    st.error("Please enter credentials!")
            st.markdown(f"""
            <p style='color:{subtext}; font-size:12px; text-align:center'>
            Default: <b>admin</b> / <b>admin123</b>
            </p>
            """, unsafe_allow_html=True)

        with tab_register:
            st.markdown("<br>", unsafe_allow_html=True)
            new_user = st.text_input("Username",
                placeholder="Choose username", key="reg_user")
            new_pass = st.text_input("Password", type="password",
                placeholder="Min 6 characters", key="reg_pass")
            confirm_pass = st.text_input("Confirm Password",
                type="password", key="reg_confirm")
            role = st.selectbox("Role",
                ["doctor", "nurse", "admin"], key="reg_role")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create Account",
                        use_container_width=True, key="register"):
                if new_user and new_pass and confirm_pass:
                    if new_pass != confirm_pass:
                        st.error("Passwords don't match!")
                    elif len(new_pass) < 6:
                        st.error("Min 6 characters!")
                    else:
                        from database import create_user
                        if create_user(new_user, new_pass, role):
                            st.success("Account created! Login now.")
                        else:
                            st.error("Username already exists!")
                else:
                    st.error("Fill all fields!")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <p style='text-align:center; color:{subtext};
                  font-size:12px; margin-top:16px'>
            🔒 HIPAA Compliant | Secure Medical Platform
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
            st.session_state.models_trained = True
            st.session_state.diabetes_acc = diabetes_acc
            st.session_state.heart_acc = heart_acc
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
        "🔬  Disease Prediction",
        "👥  Patient Management",
        "📅  Appointments",
        "💊  Medication Suggestions",
        "📋  Report Summarizer"
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
                        color:{text}; margin:8px 0'>2</div>
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

    tab1, tab2 = st.tabs([
        "🩸  Diabetes Assessment",
        "❤️  Cardiac Assessment"
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
                report = generate_report(
                    patient_name_d or "Unknown",
                    "Diabetes", result, confidence,
                    sorted_features,
                    st.session_state.username
                )
                st.download_button(
                    "📥 Download Diagnosis Report",
                    data=report,
                    file_name=f"diabetes_report_{time.strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
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
                report = generate_report(
                    patient_name_h or "Unknown",
                    "Heart Disease", result, confidence,
                    sorted_features,
                    st.session_state.username
                )
                st.download_button(
                    "📥 Download Diagnosis Report",
                    data=report,
                    file_name=f"cardiac_report_{time.strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    key="h_download"
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
    st.markdown(f"""
    <div class='nav-bar'>
        <div>
            <div style='font-size:20px; font-weight:700; color:{text}'>
                Appointment Booking
            </div>
            <div style='font-size:13px; color:{subtext}'>
                Schedule and manage patient appointments
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📅  Book Appointment", "📋  All Appointments"])

    with tab1:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### Book New Appointment")
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            apt_patient = st.text_input("Patient Name", key="apt_patient")
            apt_doctor = st.selectbox("Doctor", [
                "Dr. Rajesh Kumar — Cardiologist",
                "Dr. Priya Sharma — Diabetologist",
                "Dr. Anil Mehta — General Physician",
                "Dr. Sunita Rao — Neurologist",
                "Dr. Vikram Singh — Pulmonologist"
            ], key="apt_doctor")
            apt_dept = st.selectbox("Department", [
                "Cardiology", "Diabetology",
                "General Medicine", "Neurology", "Pulmonology"
            ], key="apt_dept")
        with col2:
            apt_date = st.date_input("Appointment Date", key="apt_date")
            apt_time = st.selectbox("Time Slot", [
                "09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM",
                "11:00 AM", "11:30 AM", "02:00 PM", "02:30 PM",
                "03:00 PM", "03:30 PM", "04:00 PM", "04:30 PM"
            ], key="apt_time")
            apt_reason = st.text_area(
                "Reason for Visit", key="apt_reason", height=100
            )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📅 Book Appointment",
                     use_container_width=True, key="book_apt"):
            if apt_patient:
                add_appointment(
                    apt_patient, apt_doctor, apt_dept,
                    str(apt_date), apt_time, apt_reason
                )
                st.success(f"""
                ✅ Appointment booked!
                **Patient:** {apt_patient}
                **Doctor:** {apt_doctor}
                **Date:** {apt_date} at {apt_time}
                """)
            else:
                st.warning("Please enter patient name!")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("#### All Appointments")
        df_apt = get_all_appointments()
        if len(df_apt) > 0:
            st.dataframe(df_apt, use_container_width=True, height=400)
            st.markdown(f"""
            <p style='color:{subtext}; font-size:13px'>
                Total: {len(df_apt)} appointments
            </p>
            """, unsafe_allow_html=True)
        else:
            st.info("No appointments scheduled yet!")
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