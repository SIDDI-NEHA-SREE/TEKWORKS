import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

st.set_page_config(page_title="Credit Card Fraud Detector Engine", layout="wide")
st.title("🛡️ Credit Card Fraud Detection Gateway")
st.write("Isolated local host acting as a substitute for an AWS API Gateway integration setup.")

# =====================================================================
# 1. DEPENDENCY LOADER MODULE
# =====================================================================
@st.cache_resource
def load_pipeline_components():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    component_names = ['scaler.pkl', 'logistic_regression.pkl', 'random_forest.pkl', 'isolation_forest.pkl']
    loaded_objects = {}
    
    for name in component_names:
        full_path = os.path.join(base_dir, name)
        with open(full_path, 'rb') as f:
            loaded_objects[name.replace('.pkl', '')] = pickle.load(f)
            
    return loaded_objects

try:
    pipeline = load_pipeline_components()
except FileNotFoundError:
    st.error("❌ Pipeline components missing. Verify that all 4 required .pkl files are stored directly in this folder.")
    st.stop()

# =====================================================================
# 2. UI LAYOUT & INPUT PAYLOAD REPLICATION
# =====================================================================
st.subheader("Transaction Input Vector Payload (Simulating API Input JSON)")
col1, col2, col3 = st.columns(3)

with col1:
    amount = st.number_input("Amount (Transaction value in USD)", min_value=0.0, max_value=100000.0, value=12000.0, step=10.0)
with col2:
    v1 = st.number_input("V1 (PCA Component 1)", value=-1.23, step=0.01)
with col3:
    v2 = st.number_input("V2 (PCA Component 2)", value=2.56, step=0.01)

# =====================================================================
# 3. BACKGROUND ALGORITHM PROCESSING
# =====================================================================
if st.button("Transmit Payload to credit-card-fraud-detector Endpoint"):
    
    # Recreate the exact structural input payload data frame
    input_df = pd.DataFrame([{
        "Amount": amount,
        "V1": v1,
        "V2": v2
    }])
    
    # Preprocess: Scale the amount feature using the downloaded configuration scaler
    processed_df = input_df.copy()
    processed_df['Amount'] = pipeline['scaler'].transform(input_df[['Amount']])
    
    # Algorithm A: Logistic Regression Binary Classifier Execution
    lr_pred = pipeline['logistic_regression'].predict(processed_df)[0]
    decision_label = "FRAUD" if lr_pred == 1 else "NORMAL"
    
    # Algorithm B: Random Forest Probability Estimator
    fraud_probability = pipeline['random_forest'].predict_proba(processed_df)[0][1] * 100
    
    # Dynamic Risk Assessment Level Matrix mapping
    if fraud_probability >= 85:
        risk_level = "CRITICAL"
    elif fraud_probability >= 50:
        risk_level = "HIGH"
    elif fraud_probability >= 20:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
        
    # Algorithm C: Isolation Forest Anomaly Detection Outlier Profiler
    # Isolation Forest outputs -1 for an anomaly (outlier) and 1 for normal data points
    iso_pred = pipeline['isolation_forest'].predict(processed_df)[0]
    anomaly_status = "ANOMALOUS ACTIVITY" if iso_pred == -1 else "STANDARD BEHAVIOR PROFILE"

    # =====================================================================
    # 4. COMPILING THE REQUESTED RESTRUCTED JSON OUTPUT
    # =====================================================================
    api_gateway_response = {
        "fraud_probability": round(float(fraud_probability), 1),
        "risk_level": risk_level
    }
    
    # Diagnostic Dashboard Display Extensions
    st.success("Analysis complete. Real-world banking AI evaluated metrics safely.")
    
    ui_left, ui_center, ui_right = st.columns(3)
    with ui_left:
        st.metric("Logistic Regression Status", decision_label)
    with ui_center:
        st.metric("Random Forest Risk Scale", f"{round(fraud_probability, 1)}%")
    with ui_right:
        st.metric("Isolation Forest Tag", anomaly_status)
        
    st.subheader("Simulated AWS Endpoint Output Response JSON")
    st.json(api_gateway_response)
