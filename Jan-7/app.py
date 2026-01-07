import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Page Config
st.set_page_config(page_title="Telco Churn - Logistic Regression", layout="centered")

# Load CSS
import os

def load_css(file):
    if os.path.exists(file):
        with open(file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css("style.css")
# Title
st.markdown("""
<div class="card">
    <h1>Logistic Regression</h1>
    <p>Predict <b>Customer Churn</b> using Telco Customer Data</p>
</div>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("Telco-Customer-Churn.csv")
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df.dropna(inplace=True)
    return df

df = load_data()

# Dataset Preview
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Dataset Preview")
st.dataframe(df.head())
st.markdown('</div>', unsafe_allow_html=True)

# Encode Categorical Data
le = LabelEncoder()
for col in df.select_dtypes(include='object').columns:
    df[col] = le.fit_transform(df[col])

# Features & Target
X = df.drop('Churn', axis=1)
y = df['Churn']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Logistic Model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)

# Predictions
y_pred = model.predict(X_test_scaled)

# Metrics
accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

# Visualization: Churn Distribution
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Churn Distribution")

fig1, ax1 = plt.subplots()
sns.countplot(x=y, ax=ax1)
ax1.set_xlabel("Churn (0 = Stay, 1 = Leave)")
ax1.set_ylabel("Count")
st.pyplot(fig1)
st.markdown('</div>', unsafe_allow_html=True)

# Confusion Matrix
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Confusion Matrix")

fig2, ax2 = plt.subplots()
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax2)
ax2.set_xlabel("Predicted")
ax2.set_ylabel("Actual")
st.pyplot(fig2)
st.markdown('</div>', unsafe_allow_html=True)

# Performance Metrics
st.subheader("Model Performance")

c1, c2, c3 = st.columns(3)
c1.metric("Accuracy", f"{accuracy*100:.2f}%")
c2.metric("Correct Churn Identified", cm[1,1])
c3.metric("Non-Churn Misclassified", cm[0,1])

# Model Details
st.markdown(f"""
<div class="card">
    <h3>Model Details</h3>
    <p>
        <b>Algorithm:</b> Logistic Regression<br>
        <b>Total Features:</b> {X.shape[1]}<br>
        <b>Dataset Size:</b> {len(df)}
    </p>
</div>
""", unsafe_allow_html=True)

# Prediction Section
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Predict Customer Churn")

tenure = st.slider("Tenure (Months)", 0, 72, 12)
monthly = st.slider("Monthly Charges", 0.0, 200.0, 70.0)
total = st.slider("Total Charges", 0.0, 10000.0, 1000.0)

sample = np.zeros(X.shape[1])
sample[X.columns.get_loc("tenure")] = tenure
sample[X.columns.get_loc("MonthlyCharges")] = monthly
sample[X.columns.get_loc("TotalCharges")] = total

sample_scaled = scaler.transform(sample.reshape(1, -1))
prediction = model.predict(sample_scaled)[0]

if prediction == 1:
    st.error("⚠️ Customer is Likely to LEAVE")
else:
    st.success("✅ Customer is Likely to STAY")

st.markdown('</div>', unsafe_allow_html=True)

