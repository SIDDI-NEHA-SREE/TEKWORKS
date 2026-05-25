import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# -----------------------------
# Streamlit Config
# -----------------------------
st.set_page_config(
    page_title="Titanic Survival Predictor",
    page_icon="🚢",
    layout="wide"
)

# -----------------------------
# Base directory (works locally + Streamlit Cloud)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------------------
# Load scaler safely
# -----------------------------
try:
    scaler = joblib.load(
        os.path.join(BASE_DIR, "scaler.pkl")
    )
except Exception as e:
    st.error(f"Scaler loading failed: {e}")
    st.stop()

# -----------------------------
# Load dataset safely
# -----------------------------
try:
    data = pd.read_csv(
        os.path.join(BASE_DIR, "Titanic-Dataset.csv")
    )
except Exception as e:
    st.error(f"Dataset loading failed: {e}")
    st.stop()


# -----------------------------
# Manual ANN weights
# Keep YOUR original weights here
# -----------------------------

w_input_hidden = np.array([
    # paste your weights exactly
])

b_hidden = np.array([
    # paste hidden bias
])

w_hidden_output = np.array([
    # paste output weights
])

b_output = np.array([
    # paste output bias
])


# -----------------------------
# Activation
# -----------------------------
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# -----------------------------
# Prediction
# -----------------------------
def predict_survival(features):

    scaled = scaler.transform([features])

    hidden = sigmoid(
        np.dot(scaled, w_input_hidden) + b_hidden
    )

    output = sigmoid(
        np.dot(hidden, w_hidden_output) + b_output
    )

    probability = output[0][0]

    return probability


# -----------------------------
# UI
# -----------------------------

st.title("🚢 Titanic Survival Predictor")

st.write(
    "Predict whether a passenger would survive "
    "the Titanic disaster."
)

col1, col2 = st.columns(2)

with col1:

    pclass = st.selectbox(
        "Passenger Class",
        [1, 2, 3]
    )

    sex = st.selectbox(
        "Sex",
        ["Male", "Female"]
    )

    age = st.slider(
        "Age",
        0,
        80,
        25
    )

    sibsp = st.number_input(
        "Siblings / Spouses",
        0,
        10,
        0
    )

with col2:

    parch = st.number_input(
        "Parents / Children",
        0,
        10,
        0
    )

    fare = st.slider(
        "Fare",
        0.0,
        600.0,
        32.0
    )

    embarked = st.selectbox(
        "Embarked",
        ["S", "C", "Q"]
    )


# -----------------------------
# Encoding
# -----------------------------

sex = 1 if sex == "Male" else 0

embarked_s = 1 if embarked == "S" else 0
embarked_c = 1 if embarked == "C" else 0
embarked_q = 1 if embarked == "Q" else 0


features = [
    pclass,
    sex,
    age,
    sibsp,
    parch,
    fare,
    embarked_c,
    embarked_q,
    embarked_s
]


# -----------------------------
# Predict button
# -----------------------------

if st.button("Predict"):

    prob = predict_survival(features)

    if prob >= 0.5:

        st.success(
            f"Survived ✅ "
            f"({prob*100:.2f}% confidence)"
        )

    else:

        st.error(
            f"Did Not Survive ❌ "
            f"({(1-prob)*100:.2f}% confidence)"
        )


# -----------------------------
# Dataset Preview
# -----------------------------

with st.expander("Dataset Preview"):

    st.dataframe(data.head())
