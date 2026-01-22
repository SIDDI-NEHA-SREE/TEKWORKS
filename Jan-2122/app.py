import streamlit as st
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt

# -------------------------------
# App Title & Description
# -------------------------------
st.set_page_config(page_title="Smart Loan Approval System", layout="centered")

st.title("💰 Smart Loan Approval System")
st.write(
    "This application uses **Support Vector Machines (SVM)** to help predict "
    "whether a loan application should be **approved or rejected**."
)

st.divider()

# -------------------------------
# Sidebar – Input Section
# -------------------------------
st.sidebar.header("📋 Applicant Details")

income = st.sidebar.number_input("Applicant Income", min_value=0, value=5000)
loan_amount = st.sidebar.number_input("Loan Amount", min_value=0, value=2000)

credit_history = st.sidebar.selectbox("Credit History", ["Yes", "No"])

employment_status = st.sidebar.selectbox(
    "Employment Status",
    ["Employed", "Self-Employed", "Unemployed"]
)

property_area = st.sidebar.selectbox(
    "Property Area",
    ["Urban", "Semiurban", "Rural"]
)

# -------------------------------
# Encode Inputs
# -------------------------------
credit_history_val = 1 if credit_history == "Yes" else 0

employment_map = {
    "Employed": 2,
    "Self-Employed": 1,
    "Unemployed": 0
}
employment_val = employment_map[employment_status]

property_map = {
    "Urban": 2,
    "Semiurban": 1,
    "Rural": 0
}
property_val = property_map[property_area]

X_user = np.array([
    income,
    loan_amount,
    credit_history_val,
    employment_val,
    property_val
]).reshape(1, -1)

# -------------------------------
# Model Selection
# -------------------------------
st.subheader("🔍 Select Prediction Model")

kernel_choice = st.radio(
    "Choose the SVM model",
    ["Linear SVM", "Polynomial SVM", "RBF SVM"]
)

# -------------------------------
# Sample Training Data
# (Academic demonstration only)
# -------------------------------
X_train = np.array([
    [3000, 1500, 1, 2, 2],
    [2000, 1800, 0, 0, 0],
    [5000, 2000, 1, 2, 1],
    [1500, 3000, 0, 1, 0],
    [6000, 2500, 1, 2, 2],
    [2500, 2800, 0, 1, 1],
])

y_train = np.array([1, 0, 1, 0, 1, 0])

# -------------------------------
# Build Model
# -------------------------------
if kernel_choice == "Linear SVM":
    model = SVC(kernel="linear", probability=True)
elif kernel_choice == "Polynomial SVM":
    model = SVC(kernel="poly", degree=3, probability=True)
else:
    model = SVC(kernel="rbf", probability=True)

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", model)
])

pipeline.fit(X_train, y_train)

# -------------------------------
# Prediction Button
# -------------------------------
st.divider()

if st.button("✅ Check Loan Eligibility"):
    prediction = pipeline.predict(X_user)[0]
    confidence = pipeline.predict_proba(X_user)[0].max()

    if prediction == 1:
        st.success("✅ Loan Approved")
        st.write("The applicant meets the basic financial requirements.")
    else:
        st.error("❌ Loan Rejected")
        st.write("The application shows higher financial risk.")

    st.write(f"**Model Used:** {kernel_choice}")
    st.write(f"**Confidence Level:** {confidence * 100:.2f}%")

    # -------------------------------
    # Business Explanation
    # -------------------------------
    st.subheader("📊 Decision Explanation")

    if prediction == 1:
        st.info(
            "The decision is mainly influenced by a **stable income**, "
            "**good credit history**, and a **balanced loan amount**."
        )
    else:
        st.warning(
            "The decision is influenced by **lower credit reliability** "
            "or an **unfavorable income-to-loan ratio**."
        )

# -------------------------------
# Visual Insights
# -------------------------------
st.divider()
st.subheader("📊 Visual Insights")

approved = X_train[y_train == 1]
rejected = X_train[y_train == 0]

# Plot 1: Income vs Loan Amount
st.write("### Income vs Loan Amount")

fig, ax = plt.subplots()
ax.scatter(approved[:, 0], approved[:, 1], label="Approved")
ax.scatter(rejected[:, 0], rejected[:, 1], label="Rejected")
ax.set_xlabel("Applicant Income")
ax.set_ylabel("Loan Amount")
ax.legend()
st.pyplot(fig)

# Plot 2: Loan Approval Distribution
st.write("### Loan Approval Summary")

fig, ax = plt.subplots()
ax.bar(["Rejected", "Approved"], [sum(y_train == 0), sum(y_train == 1)])
ax.set_ylabel("Number of Applications")
st.pyplot(fig)
