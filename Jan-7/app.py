import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

# Page config
st.set_page_config(page_title="Telco Churn Predictor", layout="centered")

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Telco-Customer-Churn.csv")
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df.dropna(inplace=True)
    return df

tcc = load_data()

st.title("📊 Telco Customer Churn Prediction")

# Encode categorical features
le = LabelEncoder()
for col in tcc.select_dtypes(include='object').columns:
    tcc[col] = le.fit_transform(tcc[col])

X = tcc.drop('Churn', axis=1)
y = tcc['Churn']

# Train model
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Model evaluation
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

st.subheader("📈 Model Performance")
st.write("Accuracy:", round(acc * 100, 2), "%")
st.write("Confusion Matrix:")
st.write(cm)

# Churn analysis
st.subheader("📌 Customer Churn Analysis")
stay = (y == 0).sum()
leave = (y == 1).sum()

st.write(f"Customers likely to **stay**: {stay}")
st.write(f"Customers likely to **leave**: {leave}")

# Prediction UI
st.subheader("🔍 Predict New Customer Churn")

tenure = st.number_input("Tenure (months)", 0, 72, 12)
monthly = st.number_input("Monthly Charges", 0.0, 200.0, 70.0)
total = st.number_input("Total Charges", 0.0, 10000.0, 1000.0)

if st.button("Predict"):
    sample = np.array([[tenure, monthly, total]])
    prediction = model.predict(sample)[0]

    if prediction == 1:
        st.error("⚠️ Customer is likely to LEAVE")
    else:
        st.success("✅ Customer is likely to STAY")
