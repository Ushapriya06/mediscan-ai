import sqlite3
import pandas as pd
from datetime import datetime
import hashlib

def init_db():
    conn = sqlite3.connect("mediscan.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'doctor',
            created_at TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            blood_group TEXT,
            contact TEXT,
            email TEXT,
            created_at TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diagnoses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            disease TEXT,
            prediction TEXT,
            confidence REAL,
            date TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            doctor TEXT NOT NULL,
            department TEXT,
            date TEXT,
            time TEXT,
            reason TEXT,
            status TEXT DEFAULT 'Scheduled',
            created_at TEXT
        )
    """)
    conn.commit()
    hashed = hashlib.sha256("admin123".encode()).hexdigest()
    try:
        cursor.execute("""
            INSERT INTO users (username, password, role, created_at)
            VALUES (?, ?, ?, ?)
        """, ("admin", hashed, "admin",
              datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
    except:
        pass
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect("mediscan.db")
    cursor = conn.cursor()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hashed)
    )
    user = cursor.fetchone()
    conn.close()
    return user is not None

def create_user(username, password, role="doctor"):
    conn = sqlite3.connect("mediscan.db")
    cursor = conn.cursor()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    try:
        cursor.execute("""
            INSERT INTO users (username, password, role, created_at)
            VALUES (?, ?, ?, ?)
        """, (username, hashed, role,
              datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        result = True
    except:
        result = False
    conn.close()
    return result

def add_patient(name, age, gender, blood_group, contact, email):
    conn = sqlite3.connect("mediscan.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patients
        (name, age, gender, blood_group, contact, email, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, age, gender, blood_group, contact, email,
          datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    patient_id = cursor.lastrowid
    conn.close()
    return patient_id

def get_all_patients():
    conn = sqlite3.connect("mediscan.db")
    df = pd.read_sql_query("SELECT * FROM patients", conn)
    conn.close()
    return df

def search_patients(query):
    conn = sqlite3.connect("mediscan.db")
    if str(query).isdigit():
        df = pd.read_sql_query(
            "SELECT * FROM patients WHERE id=? OR name LIKE ?",
            conn, params=(int(query), f"%{query}%")
        )
    else:
        df = pd.read_sql_query(
            "SELECT * FROM patients WHERE name LIKE ?",
            conn, params=(f"%{query}%",)
        )
    conn.close()
    return df

def update_patient(patient_id, name, age, gender,
                   blood_group, contact, email):
    conn = sqlite3.connect("mediscan.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE patients SET name=?, age=?, gender=?,
        blood_group=?, contact=?, email=? WHERE id=?
    """, (name, age, gender, blood_group, contact, email, patient_id))
    conn.commit()
    conn.close()

def delete_patient(patient_id):
    conn = sqlite3.connect("mediscan.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id=?", (patient_id,))
    conn.commit()
    conn.close()

def add_diagnosis(patient_id, disease, prediction, confidence):
    conn = sqlite3.connect("mediscan.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO diagnoses
        (patient_id, disease, prediction, confidence, date)
        VALUES (?, ?, ?, ?, ?)
    """, (patient_id, disease, prediction, confidence,
          datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_patient_diagnoses(patient_id):
    conn = sqlite3.connect("mediscan.db")
    df = pd.read_sql_query(
        "SELECT * FROM diagnoses WHERE patient_id=?",
        conn, params=(patient_id,)
    )
    conn.close()
    return df

def get_dashboard_stats():
    conn = sqlite3.connect("mediscan.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM patients")
    total_patients = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM diagnoses")
    total_diagnoses = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COUNT(*) FROM diagnoses WHERE prediction='Positive'"
    )
    positive_cases = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM appointments")
    total_appointments = cursor.fetchone()[0]
    conn.close()
    return total_patients, total_diagnoses, positive_cases, total_appointments

def add_appointment(patient_name, doctor, department,
                    date, time, reason):
    conn = sqlite3.connect("mediscan.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO appointments
        (patient_name, doctor, department, date, time, reason, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (patient_name, doctor, department, date, time, reason,
          datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_all_appointments():
    conn = sqlite3.connect("mediscan.db")
    df = pd.read_sql_query(
        "SELECT * FROM appointments ORDER BY date, time",
        conn
    )
    conn.close()
    return df

def update_appointment_status(appointment_id, status):
    conn = sqlite3.connect("mediscan.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE appointments SET status=? WHERE id=?",
        (status, appointment_id)
    )
    conn.commit()
    conn.close()