import hashlib
from supabase import create_client
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def init_db():
    # Tables already created in Supabase dashboard
    pass

def verify_user(username, password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    result = supabase.table("users").select("*").eq(
        "username", username
    ).eq("password", hashed).execute()
    return len(result.data) > 0

def create_user(username, password, role="doctor"):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    try:
        supabase.table("users").insert({
            "username": username,
            "password": hashed,
            "role": role
        }).execute()
        return True
    except:
        return False

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
    return pd.DataFrame(result.data)

def search_patients(query):
    if str(query).isdigit():
        result = supabase.table("patients").select("*").eq(
            "id", int(query)
        ).execute()
    else:
        result = supabase.table("patients").select("*").ilike(
            "name", f"%{query}%"
        ).execute()
    return pd.DataFrame(result.data)

def update_patient(patient_id, name, age, gender,
                   blood_group, contact, email):
    supabase.table("patients").update({
        "name": name,
        "age": age,
        "gender": gender,
        "blood_group": blood_group,
        "contact": contact,
        "email": email
    }).eq("id", patient_id).execute()

def delete_patient(patient_id):
    supabase.table("patients").delete().eq(
        "id", patient_id
    ).execute()

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
    return pd.DataFrame(result.data)

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

def add_appointment(patient_name, doctor, department,
                    date, time, reason):
    supabase.table("appointments").insert({
        "patient_name": patient_name,
        "doctor": doctor,
        "department": department,
        "date": date,
        "time": time,
        "reason": reason
    }).execute()

def get_all_appointments():
    result = supabase.table("appointments").select("*").execute()
    return pd.DataFrame(result.data)

def update_appointment_status(appointment_id, status):
    supabase.table("appointments").update({
        "status": status
    }).eq("id", appointment_id).execute()

def get_analytics():
    # Diagnoses per disease
    diseases = supabase.table("diagnoses").select(
        "disease"
    ).execute()
    
    # Monthly registrations
    patients = supabase.table("patients").select(
        "created_at"
    ).execute()
    
    # Positive vs negative
    positive = supabase.table("diagnoses").select(
        "*", count="exact"
    ).eq("prediction", "Positive").execute()
    
    negative = supabase.table("diagnoses").select(
        "*", count="exact"
    ).eq("prediction", "Negative").execute()
    
    # Appointments by status
    appointments = supabase.table("appointments").select(
        "status"
    ).execute()
    
    return {
        "diseases": diseases.data,
        "patients": patients.data,
        "positive": positive.count or 0,
        "negative": negative.count or 0,
        "appointments": appointments.data
    }

def get_recent_diagnoses():
    result = supabase.table("diagnoses").select(
        "*"
    ).order("date", desc=True).limit(10).execute()
    return pd.DataFrame(result.data)

def get_recent_patients():
    result = supabase.table("patients").select(
        "*"
    ).order("created_at", desc=True).limit(5).execute()
    return pd.DataFrame(result.data)

def update_user_email(username, email):
    supabase.table("users").update({
        "email": email
    }).eq("username", username).execute()

def get_user_email(username):
    result = supabase.table("users").select(
        "email"
    ).eq("username", username).execute()
    if result.data and result.data[0]["email"]:
        return result.data[0]["email"]
    return None

def get_all_doctors():
    result = supabase.table("doctors").select("*").eq(
        "available", True
    ).execute()
    return pd.DataFrame(result.data)

def add_doctor(name, specialization, experience):
    supabase.table("doctors").insert({
        "name": name,
        "specialization": specialization,
        "experience": experience
    }).execute()