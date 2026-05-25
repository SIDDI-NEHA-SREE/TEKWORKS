import streamlit as st
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

model = tf.keras.models.load_model("titanic_ann_model.h5")

st.set_page_config(page_title="Titanic Survival Prediction")

st.title("🚢 Titanic Survival Prediction System")
st.subheader("Deep Learning Based Passenger Survival Prediction")

st.write("""
This application predicts passenger survival
using an Artificial Neural Network trained
using TensorFlow.
""")

col1,col2,col3=st.columns(3)

with col1:
    pclass=st.selectbox(
        "Passenger Class",[1,2,3]
    )

with col2:
    age=st.slider(
        "Age",1,80,24
    )

with col3:
    fare=st.number_input(
        "Fare",0.0,600.0,120.0
    )

def normalize(x,minv,maxv):
    return (x-minv)/(maxv-minv)

if st.button("Predict Survival"):

    pclass_n=normalize(pclass,1,3)
    age_n=normalize(age,0,80)
    fare_n=normalize(fare,0,600)

    X=np.array([
        [pclass_n,age_n,fare_n]
    ])

    pred=model.predict(X)[0][0]

    survival=pred
    nonsurvival=1-pred

    result="Survived" if pred>0.5 else "Not Survived"

    st.metric(
        "Prediction",
        result
    )

    st.metric(
        "Probability",
        f"{pred:.2%}"
    )

    st.metric(
        "Confidence",
        f"{max(pred,1-pred):.2%}"
    )

    fig,ax=plt.subplots()

    ax.bar(
        ["No","Yes"],
        [nonsurvival,survival]
    )

    st.pyplot(fig)