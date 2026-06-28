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