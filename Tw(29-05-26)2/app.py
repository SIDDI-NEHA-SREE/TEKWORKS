import streamlit as st
import pandas as pd
import numpy as np
import pickle
import json
import os

st.set_page_config(page_title="Loan Risk Predictor Gateway", layout="wide")
st.title("🏦 Local Bank Engine: Loan Risk Predictor Portal")
st.write("Isolated local host acting as a substitute for an AWS API Gateway integration setup.")

# =====================================================================
# 1. COMPONENT PIPELINE DEPENDENCY LOADER
# =====================================================================
@st.cache_resource
def load_pipeline_components():
    # Targets the active running folder directory securely
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    component_names = ['scaler.pkl', 'pca.pkl', 'kmeans.pkl', 'logistic_regression.pkl', 'random_forest.pkl']
    loaded_objects = {}
    
    for name in component_names:
        full_path = os.path.join(base_dir, name)
        with open(full_path, 'rb') as f:
            loaded_objects[name.replace('.pkl', '')] = pickle.load(f)
            
    return loaded_objects

try:
    pipeline = load_pipeline_components()
except FileNotFoundError:
    st.error("❌ Component mapping error: Please verify all 5 .pkl configuration files are placed in this exact project folder folder layout.")
    st.stop()

# =====================================================================
# 2. APP INPUT STRUCTURE UI
# =====================================================================
st.subheader("Customer Transaction Input Vectors")
col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Age", min_value=18, max_value=100, value=35)
    income = st.number_input("Annual Income ($)", min_value=1000, max_value=500000, value=75000)
    loan_amount = st.number_input("Requested Loan Amount ($)", min_value=500, max_value=1000000, value=25000)

with col2:
    credit_score = st.slider("Credit Score Metric Rating", min_value=300, max_value=850, value=680)
    months_employed = st.number_input("Months in Active Continuous Employment", min_value=0, max_value=600, value=48)

with col3:
    interest_rate = st.slider("Interest Rate Target (%)", min_value=1.0, max_value=35.0, value=11.5, step=0.1)
    dti_ratio = st.slider("Debt-to-Income (DTI) Ratio Proportion", min_value=0.0, max_value=1.0, value=0.35, step=0.01)

# =====================================================================
# 3. BACKGROUND EXECUTION LOOPS (Substitution of AWS Endpoint logic)
# =====================================================================
if st.button("Transmit Payload to POST /loan/predict"):
    
    # Structure input mapping matrix
    raw_payload = {
        "Age": age,
        "Income": income,
        "LoanAmount": loan_amount,
        "CreditScore": credit_score,
        "MonthsEmployed": months_employed,
        "InterestRate": interest_rate,
        "DTIRatio": dti_ratio
    }
    
    input_df = pd.DataFrame([raw_payload])
    
    # Process 1: Scaling standard data arrays
    scaled_data = pipeline['scaler'].transform(input_df)
    
    # Process 2: K-Means segmentation profiling cluster grouping
    customer_segment = int(pipeline['kmeans'].predict(scaled_data)[0])
    
    # Process 3: Dimensional matrix reductions via PCA transforms
    pca_data = pipeline['pca'].transform(scaled_data)
    
    # Process 4: Algorithm Classifications 
    # Logistic Regression prediction layer (Approved vs Rejected status maps)
    lr_binary_output = pipeline['logistic_regression'].predict(pca_data)[0]
    decision = "APPROVED" if lr_binary_output == 0 else "REJECTED"
    
    # Random Forest default probability tracking metrics layer
    risk_probability = pipeline['random_forest'].predict_proba(pca_data)[0][1] * 100
    
    if risk_probability >= 65:
        risk_tier = "HIGH"
    elif risk_probability >= 35:
        risk_tier = "MEDIUM"
    else:
        risk_tier = "LOW"

    # =====================================================================
    # 4. JSON OUTPUT (POST /loan/predict simulation)
    # =====================================================================
    api_gateway_response = {
        "status": 200,
        "endpoint": "POST /loan/predict",
        "response_body": {
            "loan_decision": decision,
            "default_risk_probability": round(float(risk_probability), 2),
            "risk_level": risk_tier,
            "assigned_customer_segment": customer_segment,
            "pca_coordinates": [round(float(coord), 4) for coord in pca_data[0]]
        }
    }
    
    st.success("Calculations complete. Array structured safely.")
    
    ui_left, ui_right = st.columns(2)
    with ui_left:
        st.metric("Logistic Regression Decision", decision)
        st.metric("K-Means Assigned Group", f"Segment {customer_segment}")
    with ui_right:
        st.metric("Random Forest Risk Scale", f"{round(risk_probability, 1)}%")
        st.metric("Assigned Risk Category Tier", risk_tier)
        
    st.subheader("Raw JSON Response Body Output (POST /loan/predict structure)")
    st.json(api_gateway_response)
