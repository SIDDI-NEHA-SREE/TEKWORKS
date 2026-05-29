import streamlit as st
import pandas as pd
import pickle
import json

# Set up page configuration
st.set_page_config(page_title="Employee Attrition Predictor", layout="centered")
st.title("🧑‍💼 Employee Attrition Predictor")
st.write("Local alternative to AWS SageMaker/API Gateway pipeline.")

# 1. Load the trained models
@st.cache_resource
def load_models():
    with open('logistic_regression.pkl', 'rb') as f:
        lr = pickle.load(f)
    with open('random_forest.pkl', 'rb') as f:
        rf = pickle.load(f)
    return lr, rf

try:
    lr_model, rf_model = load_models()
except FileNotFoundError:
    st.error("Error: Please ensure 'logistic_regression.pkl' and 'random_forest.pkl' are in the same folder as this script.")
    st.stop()

# 2. Sidebar/UI Input Elements
st.sidebar.header("Model Configuration")
model_choice = st.sidebar.selectbox("Select Model", ["Random Forest", "Logistic Regression"])

st.subheader("Input Employee Features")
age = st.number_input("Age", min_value=18, max_value=70, value=35)
monthly_income = st.number_input("Monthly Income ($)", min_value=1000, max_value=30000, value=4500)
job_satisfaction = st.slider("Job Satisfaction (1-4)", min_value=1, max_value=4, value=2)

# 3. Process Prediction on Button Click
if st.button("Predict Attrition"):
    # Format input data matching the training features layout
    input_data = pd.DataFrame([{
        "Age": age,
        "MonthlyIncome": monthly_income,
        "JobSatisfaction": job_satisfaction
    }])
    
    # Select chosen model
    selected_model = rf_model if model_choice == "Random Forest" else lr_model
    
    # Calculate probability of attrition (Class 1)
    probability = selected_model.predict_proba(input_data)[0][1] * 100
    
    # Assign Risk Level based on thresholds
    if probability >= 70:
        risk_level = "HIGH"
    elif probability >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
        
    # 4. Construct API-like JSON Output
    output_response = {
        "attrition_probability": round(probability, 1),
        "risk_level": risk_level
    }
    
    # Display Results
    st.subheader("API JSON Output Response")
    st.json(output_response)