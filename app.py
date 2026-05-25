import streamlit as nn_st
import tensorflow as tf
import numpy as np
import plotly.graph_objects as go

# --- TASK 5: LOAD TRAINED MODEL ---
@nn_st.cache_resource
def load_titanic_model():
    # Loads the compiled TensorFlow H5 model file
    return tf.keras.models.load_model('titanic_model.h5')

try:
    model = load_titanic_model()
except Exception as e:
    nn_st.error("Error: 'titanic_model.h5' not found. Please place the model file in the same directory.")
    model = None

# --- TASK 7: UI STYLING & CONFIGURATION ---
nn_st.set_page_config(page_title="Titanic Survival Predictor", page_icon="🚢", layout="centered")

# Custom CSS styling for a professional interface appearance
nn_st.markdown("""
    <style>
    .main-header { font-size: 2.3rem; font-weight: bold; color: #1E3A8A; margin-bottom: 0px; }
    .sub-header { font-size: 1.2rem; color: #4B5563; margin-bottom: 20px; }
    .card-container { background-color: #F3F4F6; padding: 20px; border-radius: 10px; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

# --- TASK 3: SECTION 1 — HEADER AREA ---
nn_st.markdown('<p class="main-header">🚢 Titanic Survival Prediction System</p>', unsafe_allow_html=True)
nn_st.markdown('<p class="sub-header">Deep Learning Based Passenger Survival Prediction</p>', unsafe_allow_html=True)

# --- TASK 3: SECTION 2 — PROJECT DESCRIPTION ---
with nn_st.container():
    nn_st.markdown("""
    ### Project Overview
    This interactive data product utilizes a custom **Artificial Neural Network (ANN)** built with **TensorFlow** 
    to analyze and calculate survival likelihood profiles during maritime emergencies. By evaluating crucial social and biological parameters, the underlying architecture maps feature relationships to compute production probabilities.
    """)

nn_st.divider()

# --- TASK 3: SECTION 3 — PASSENGER INPUT FORM ---
nn_st.markdown("### 📋 Enter Passenger Demographics")

with nn_st.form(key='passenger_form'):
    col1, col2, col3 = nn_st.columns(3)
    
    with col1:
        pclass = nn_st.selectbox("Passenger Class (Pclass)", options=[1, 2, 3], help="1 = Upper class, 2 = Middle class, 3 = Lower class")
    
    with col2:
        age = nn_st.slider("Passenger Age (Years)", min_value=1, max_value=100, value=24, step=1)
        
    with col3:
        fare = nn_st.number_input("Ticket Fare ($)", min_value=0.0, max_value=600.0, value=120.0, step=5.0)

    # --- TASK 3: SECTION 4 — PREDICTION BUTTON ---
    submit_button = nn_st.form_submit_button(label="🔮 Predict Survival")

# Execution sequence on form submission
if submit_button and model is not None:
    
    # --- TASK 4: DATA PREPROCESSING (MIN-MAX SCALING MATCHING TRAINING OBJECTIVES) ---
    # Normalization mappings manually configured to mirror training records:
    # Pclass: [1, 3] -> 1 maps to 0.2
    # Age: [0, 100] -> 24 maps to 0.24
    # Fare: [0, 150] -> 120 maps to 0.80
    norm_pclass = 0.2 if pclass == 1 else (0.5 if pclass == 2 else 0.8)
    norm_age = age / 100.0
    norm_fare = fare / 150.0
    
    # Constructing input tensor arrays
    input_data = np.array([[norm_pclass, norm_age, norm_fare]], dtype=np.float32)
    
    # Executing prediction pipeline
    prediction_raw = model.predict(input_data)
    survival_prob = float(prediction_raw[0][0])
    non_survival_prob = 1.0 - survival_prob

    # --- TASK 6: PREDICTION LOGIC ---
    if survival_prob >= 0.5:
        result_status = "Survived"
        alert_style = nn_st.success
        metric_color = "green"
    else:
        result_status = "Did Not Survive"
        alert_style = nn_st.error
        metric_color = "red"

    nn_st.divider()

    # --- TASK 3: SECTION 5 — PREDICTION OUTPUT AREA ---
    nn_st.markdown("### 🎯 Classification Results")
    
    alert_style(f"### Outcome: Passenger is predicted to have: **{result_status}**")
    
    # Highlight values using Streamlit native components
    m_col1, m_col2, m_col3 = nn_st.columns(3)
    m_col1.metric(label="Prediction Outcome", value=result_status)
    m_col2.metric(label="Survival Probability", value=f"{survival_prob * 100:.2f}%")
    m_col3.metric(label="Model Confidence Score", value=f"{abs(survival_prob - 0.5) * 2 * 100:.2f}%")

    # --- TASK 3: SECTION 6 — VISUALIZATION AREA ---
    nn_st.markdown("### 📊 Distribution Profile Matrix")
    
    # Plotly donut chart composition mapping target metrics
    fig = go.Figure(data=[go.Pie(
        labels=['Survived', 'Not Survived'], 
        values=[survival_prob, non_survival_prob],
        hole=.4,
        marker_colors=['#10B981', '#EF4444'],
        textinfo='percent+label'
    )])
    
    fig.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        height=300,
        showlegend=False
    )
    
    nn_st.plotly_chart(fig, use_container_width=True)
