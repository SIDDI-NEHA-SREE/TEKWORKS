import streamlit as st
import numpy as np
import joblib
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Titanic Survival Prediction",
    layout="wide"
)

scaler = joblib.load("scaler.pkl")

# Trained weights
w_input_hidden = np.array([
    [0.11,0.21],
    [0.14,0.24],
    [0.17,0.27]
])

b_hidden = np.array([0.1,0.1])

w_hidden_output = np.array([
    [0.31],
    [0.34]
])

b_output = 0.1

def sigmoid(x):
    return 1/(1+np.exp(-x))

st.title("🚢 Titanic Survival Prediction System")

st.subheader(
    "Deep Learning Based Passenger Survival Prediction"
)

st.write(
"""
Predict passenger survival using
an Artificial Neural Network.
"""
)

col1,col2,col3 = st.columns(3)

with col1:
    pclass = st.selectbox(
        "Passenger Class",
        [1,2,3]
    )

with col2:
    age = st.slider(
        "Age",
        1,
        80,
        24
    )

with col3:
    fare = st.number_input(
        "Fare",
        0.0,
        600.0,
        120.0
    )

if st.button("Predict Survival"):

    X = scaler.transform(
        [[pclass,age,fare]]
    )

    hidden_net = (
        np.dot(X,w_input_hidden)
        + b_hidden
    )

    hidden = sigmoid(hidden_net)

    output_net = (
        np.dot(
            hidden,
            w_hidden_output
        )
        + b_output
    )

    prediction = sigmoid(output_net)[0][0]

    result = (
        "Survived"
        if prediction>0.5
        else "Not Survived"
    )

    st.metric(
        "Prediction",
        result
    )

    st.metric(
        "Survival Probability",
        f"{prediction*100:.2f}%"
    )

    st.metric(
        "Confidence",
        f"{max(prediction,1-prediction)*100:.2f}%"
    )

    fig,ax=plt.subplots()

    ax.bar(
        ["No","Yes"],
        [1-prediction,prediction]
    )

    st.pyplot(fig)
