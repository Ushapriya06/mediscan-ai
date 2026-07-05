import hashlib
import random
import string
from supabase import create_client
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime, timedelta

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def init_db():
    pass

# ── Auth Functions ─────────────────────────────
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def verify_user(username, password):
    hashed = hash_password(password)
    result = supabase.table("users").select("*").eq(
        "username", username
    ).eq("password", hashed).execute()
    if result.data:
        # Update last login
        supabase.table("users").update({
            "last_login": datetime.now().isoformat()
        }).eq("username", username).execute()
        return result.data[0]
    return None

def create_user(username, password, role="doctor",
                full_name="", email="", phone=""):
    hashed = hash_password(password)
    try:
        supabase.table("users").insert({
            "username": username,
            "password": hashed,
            "role": role,
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "is_verified": True
        }).execute()
        return True, "Account created successfully!"
    except Exception as e:
        if "duplicate" in str(e).lower():
            return False, "Username already exists!"
        return False, "Registration failed. Try again!"

def username_exists(username):
    result = supabase.table("users").select(
        "username"
    ).eq("username", username).execute()
    return len(result.data) > 0

def email_exists(email):
    result = supabase.table("users").select(
        "email"
    ).eq("email", email).execute()
    return len(result.data) > 0

def update_password(username, new_password):
    hashed = hash_password(new_password)
    supabase.table("users").update({
        "password": hashed
    }).eq("username", username).execute()

def get_user_by_email(email):
    result = supabase.table("users").select("*").eq(
        "email", email
    ).execute()
    return result.data[0] if result.data else None

def update_user_email(username, email):
    supabase.table("users").update({
        "email": email
    }).eq("username", username).execute()

def get_user_email(username):
    result = supabase.table("users").select(
        "email"
    ).eq("username", username).execute()
    if result.data and result.data[0].get("email"):
        return result.data[0]["email"]
    return None

def get_user_profile(username):
    result = supabase.table("users").select("*").eq(
        "username", username
    ).execute()
    return result.data[0] if result.data else None

def update_user_profile(username, full_name, email, phone):
    supabase.table("users").update({
        "full_name": full_name,
        "email": email,
        "phone": phone
    }).eq("username", username).execute()

# ── Patient Functions ──────────────────────────
def add_patient(name, age, gender, blood_group, contact, email):
    result = supabase.table("patients").insert({
        "name": name,
        "age": age,
        "gender": gender,
        "blood_group": blood_group,
        "contact": contact,
        "email": email
    }).execute()
    return result.data[0]["id"]

def get_all_patients():
    result = supabase.table("patients").select("*").execute()
    return pd.DataFrame(result.data) if result.data else pd.DataFrame()

def search_patients(query):
    if str(query).isdigit():
        result = supabase.table("patients").select("*").eq(
            "id", int(query)
        ).execute()
    else:
        result = supabase.table("patients").select("*").ilike(
            "name", f"%{query}%"
        ).execute()
    return pd.DataFrame(result.data) if result.data else pd.DataFrame()

def update_patient(patient_id, name, age, gender,
                   blood_group, contact, email):
    supabase.table("patients").update({
        "name": name, "age": age, "gender": gender,
        "blood_group": blood_group, "contact": contact,
        "email": email
    }).eq("id", patient_id).execute()

def delete_patient(patient_id):
    supabase.table("patients").delete().eq(
        "id", patient_id
    ).execute()

# ── Diagnosis Functions ────────────────────────
def add_diagnosis(patient_id, disease, prediction, confidence):
    supabase.table("diagnoses").insert({
        "patient_id": patient_id,
        "disease": disease,
        "prediction": prediction,
        "confidence": confidence
    }).execute()

def get_patient_diagnoses(patient_id):
    result = supabase.table("diagnoses").select("*").eq(
        "patient_id", patient_id
    ).execute()
    return pd.DataFrame(result.data) if result.data else pd.DataFrame()

def get_recent_diagnoses():
    result = supabase.table("diagnoses").select(
        "*"
    ).order("date", desc=True).limit(10).execute()
    return pd.DataFrame(result.data) if result.data else pd.DataFrame()

def get_recent_patients():
    result = supabase.table("patients").select(
        "*"
    ).order("created_at", desc=True).limit(5).execute()
    return pd.DataFrame(result.data) if result.data else pd.DataFrame()

# ── Doctor Functions ───────────────────────────
def get_all_doctors():
    result = supabase.table("doctors").select("*").eq(
        "available", True
    ).execute()
    return pd.DataFrame(result.data) if result.data else pd.DataFrame()

def get_doctor_by_id(doctor_id):
    result = supabase.table("doctors").select("*").eq(
        "id", doctor_id
    ).execute()
    return result.data[0] if result.data else None

# ── Appointment Functions ──────────────────────
def get_booked_slots(doctor_id, date):
    result = supabase.table("appointments").select(
        "time"
    ).eq("doctor_id", doctor_id).eq(
        "date", str(date)
    ).neq("status", "Cancelled").execute()
    return [r["time"] for r in result.data]

def add_appointment(patient_name, doctor_id, doctor_name,
                    department, date, time, reason,
                    patient_email="", patient_phone=""):
    booking_id = ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=8)
    )
    supabase.table("appointments").insert({
        "patient_name": patient_name,
        "doctor_id": doctor_id,
        "doctor": doctor_name,
        "department": department,
        "date": str(date),
        "time": time,
        "reason": reason,
        "patient_email": patient_email,
        "patient_phone": patient_phone,
        "booking_id": booking_id,
        "status": "Scheduled"
    }).execute()
    return booking_id

def get_all_appointments():
    result = supabase.table("appointments").select(
        "*"
    ).order("date", desc=False).execute()
    return pd.DataFrame(result.data) if result.data else pd.DataFrame()

def update_appointment_status(appointment_id, status):
    supabase.table("appointments").update({
        "status": status
    }).eq("id", appointment_id).execute()

def cancel_appointment(booking_id):
    supabase.table("appointments").update({
        "status": "Cancelled"
    }).eq("booking_id", booking_id).execute()

# ── Analytics Functions ────────────────────────
def get_analytics():
    diseases = supabase.table("diagnoses").select("disease").execute()
    patients = supabase.table("patients").select("created_at").execute()
    positive = supabase.table("diagnoses").select(
        "*", count="exact"
    ).eq("prediction", "Positive").execute()
    negative = supabase.table("diagnoses").select(
        "*", count="exact"
    ).eq("prediction", "Negative").execute()
    appointments = supabase.table("appointments").select("status").execute()
    return {
        "diseases": diseases.data,
        "patients": patients.data,
        "positive": positive.count or 0,
        "negative": negative.count or 0,
        "appointments": appointments.data
    }

def get_dashboard_stats():
    patients = supabase.table("patients").select(
        "*", count="exact"
    ).execute()
    diagnoses = supabase.table("diagnoses").select(
        "*", count="exact"
    ).execute()
    positive = supabase.table("diagnoses").select(
        "*", count="exact"
    ).eq("prediction", "Positive").execute()
    appointments = supabase.table("appointments").select(
        "*", count="exact"
    ).execute()
    return (
        patients.count or 0,
        diagnoses.count or 0,
        positive.count or 0,
        appointments.count or 0
    )
