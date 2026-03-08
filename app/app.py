import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ===== Load Model =====
model = joblib.load("churn_model.pkl")
scaler = joblib.load("scaler.pkl")

# ===== Page Config =====
st.set_page_config(page_title="Customer Churn Predictor", page_icon="📊", layout="wide")
st.title("📊 Customer Churn Predictor")
st.markdown("Predict whether a customer will leave or stay.")

# ===== Input Form =====
st.header("Enter Customer Details")

col1, col2, col3 = st.columns(3)

with col1:
    tenure = st.slider("Tenure (months)", 0, 72, 12)
    MonthlyCharges = st.number_input("Monthly Charges ($)", 0.0, 150.0, 50.0)
    TotalCharges = st.number_input("Total Charges ($)", 0.0, 10000.0, 600.0)
    SeniorCitizen = st.selectbox("Senior Citizen", [0, 1])

with col2:
    gender = st.selectbox("Gender", ["Male", "Female"])
    Partner = st.selectbox("Partner", ["Yes", "No"])
    Dependents = st.selectbox("Dependents", ["Yes", "No"])
    PhoneService = st.selectbox("Phone Service", ["Yes", "No"])

with col3:
    Contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    InternetService = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    PaymentMethod = st.selectbox("Payment Method", [
        "Electronic check", "Mailed check",
        "Bank transfer (automatic)", "Credit card (automatic)"])
    PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"])

# ===== Predict Button =====
if st.button("🔍 Predict Churn"):
    input_dict = {
        'SeniorCitizen': SeniorCitizen,
        'tenure': tenure,
        'MonthlyCharges': MonthlyCharges,
        'TotalCharges': TotalCharges,
        'gender_Male': 1 if gender == 'Male' else 0,
        'Partner_Yes': 1 if Partner == 'Yes' else 0,
        'Dependents_Yes': 1 if Dependents == 'Yes' else 0,
        'PhoneService_Yes': 1 if PhoneService == 'Yes' else 0,
        'MultipleLines_No phone service': 0,
        'MultipleLines_Yes': 0,
        'InternetService_Fiber optic': 1 if InternetService == 'Fiber optic' else 0,
        'InternetService_No': 1 if InternetService == 'No' else 0,
        'OnlineSecurity_No internet service': 0,
        'OnlineSecurity_Yes': 0,
        'OnlineBackup_No internet service': 0,
        'OnlineBackup_Yes': 0,
        'DeviceProtection_No internet service': 0,
        'DeviceProtection_Yes': 0,
        'TechSupport_No internet service': 0,
        'TechSupport_Yes': 0,
        'StreamingTV_No internet service': 0,
        'StreamingTV_Yes': 0,
        'StreamingMovies_No internet service': 0,
        'StreamingMovies_Yes': 0,
        'Contract_One year': 1 if Contract == 'One year' else 0,
        'Contract_Two year': 1 if Contract == 'Two year' else 0,
        'PaperlessBilling_Yes': 1 if PaperlessBilling == 'Yes' else 0,
        'PaymentMethod_Credit card (automatic)': 1 if PaymentMethod == 'Credit card (automatic)' else 0,
        'PaymentMethod_Electronic check': 1 if PaymentMethod == 'Electronic check' else 0,
        'PaymentMethod_Mailed check': 1 if PaymentMethod == 'Mailed check' else 0,
    }

    input_df = pd.DataFrame([input_dict])
    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1]

    st.divider()
    if prediction == 1:
        st.error(f"⚠️ High Risk: This customer has a {probability*100:.1f}% chance of churning!")
    else:
        st.success(f"✅ Low Risk: This customer has only a {probability*100:.1f}% chance of churning.")