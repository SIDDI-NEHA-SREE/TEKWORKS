import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Telco Churn Prediction", layout="wide")

# ------------------ LOAD CSS ------------------
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# ------------------ TITLE ------------------
st.markdown("<h1 class='title'>Telco Customer Churn Analysis</h1>", unsafe_allow_html=True)

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    return pd.read_csv("Telco-Customer-Churn.csv")

df = load_data()

# ------------------ DATA PREPROCESSING ------------------
df = df.drop("customerID", axis=1)

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna()

df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

df = pd.get_dummies(df, drop_first=True)

X = df.drop("Churn", axis=1)
y = df["Churn"]

# ------------------ TRAIN TEST SPLIT ------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ------------------ SCALING ------------------
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# ------------------ MODEL ------------------
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# ------------------ PREDICTION ------------------
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

# ------------------ RESULTS ------------------
st.markdown("## Model Performance")

st.metric(label="Accuracy", value=f"{accuracy * 100:.2f}%")

stay_count = (y == 0).sum()
leave_count = (y == 1).sum()

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Customers Staying")
    st.write(stay_count)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Customers Leaving")
    st.write(leave_count)
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------ CONFUSION MATRIX ------------------
st.markdown("## Confusion Matrix")
st.write(pd.DataFrame(
    cm,
    columns=["Predicted Stay", "Predicted Leave"],
    index=["Actual Stay", "Actual Leave"]
))
