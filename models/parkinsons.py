import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os

def train_parkinsons_model():
    df = pd.read_csv("data/parkinsons.csv")
    if 'name' in df.columns:
        df = df.drop('name', axis=1)
    X = df.drop('status', axis=1)
    y = df['status']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    os.makedirs("saved_models", exist_ok=True)
    with open("saved_models/parkinsons_model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open("saved_models/parkinsons_scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
    with open("saved_models/parkinsons_features.pkl", "wb") as f:
        pickle.dump(list(X.columns), f)
    return accuracy

def predict_parkinsons(input_data):
    with open("saved_models/parkinsons_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("saved_models/parkinsons_scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    input_array = np.array(input_data, dtype=float).reshape(1, -1)
    input_scaled = scaler.transform(input_array)
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0]
    confidence = round(max(probability) * 100, 2)
    result = "Positive" if prediction == 1 else "Negative"
    return result, confidence

def explain_parkinsons(input_data):
    with open("saved_models/parkinsons_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("saved_models/parkinsons_features.pkl", "rb") as f:
        features = pickle.load(f)
    importances = model.feature_importances_
    importance_dict = dict(zip(features, importances))
    sorted_features = sorted(
        importance_dict.items(), key=lambda x: x[1], reverse=True
    )
    return sorted_features