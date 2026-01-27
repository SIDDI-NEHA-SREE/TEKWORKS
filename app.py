import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

st.set_page_config(
    page_title="Customer Risk Prediction System (KNN)",
    layout="wide"
)

st.markdown("""
<style>
.main {background-color:#0e1117;}
h1,h2,h3 {color:#ffffff;}
div[data-testid="stSidebar"] {background-color:#161b22;}
.stButton>button {background-color:#2563eb;color:white;border-radius:8px;}
.stDataFrame {background-color:#ffffff;}
.result-high {background-color:#7f1d1d;padding:20px;border-radius:12px;color:white;text-align:center;}
.result-low {background-color:#14532d;padding:20px;border-radius:12px;color:white;text-align:center;}
.metric-box {background-color:#1f2937;padding:15px;border-radius:10px;color:white;}
</style>
""", unsafe_allow_html=True)

df = pd.read_csv("credit_risk_dataset.csv")
df = df.dropna()

df["cb_person_default_on_file"] = df["cb_person_default_on_file"].map({"Y":1,"N":0})

X = df[[
    "person_age",
    "person_income",
    "loan_amnt",
    "cb_person_cred_hist_length",
    "cb_person_default_on_file"
]]

y = df["loan_status"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

st.title("Customer Risk Prediction System (KNN)")
st.write("This system predicts customer risk by comparing them with similar customers.")

st.sidebar.header("Customer Details")

age = st.sidebar.slider("Age",18,70,30)
income = st.sidebar.number_input("Annual Income",20000,2000000,500000)
loan = st.sidebar.number_input("Loan Amount",1000,1000000,100000)
history = st.sidebar.slider("Credit History (Years)",0,30,5)
default = st.sidebar.selectbox("Credit History Default",["No","Yes"])
k = st.sidebar.slider("K Value",1,15,5)

default_val = 1 if default=="Yes" else 0

input_data = np.array([[age,income,loan,history,default_val]])
input_scaled = scaler.transform(input_data)

col1, col2 = st.columns([2,1])

with col1:
    if st.button("Predict Customer Risk"):
        model = KNeighborsClassifier(n_neighbors=k)
        model.fit(X_train,y_train)
        
        prediction = model.predict(input_scaled)[0]
        neighbors = model.kneighbors(input_scaled,return_distance=False)[0]
        neighbor_classes = y_train.iloc[neighbors]
        majority = neighbor_classes.mode()[0]
        
        if prediction==1:
            st.markdown('<div class="result-high"><h2>🔴 High Risk Customer</h2></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-low"><h2>🟢 Low Risk Customer</h2></div>', unsafe_allow_html=True)
        
        st.subheader("Nearest Neighbors Explanation")
        st.markdown(f"""
        <div class="metric-box">
        Neighbors considered: <b>{k}</b><br>
        Majority class: <b>{"High Risk" if majority==1 else "Low Risk"}</b>
        </div>
        """, unsafe_allow_html=True)
        
        neighbor_df = df.iloc[neighbors][[
            "person_age","person_income","loan_amnt","loan_status"
        ]]
        neighbor_df["loan_status"] = neighbor_df["loan_status"].map({1:"High Risk",0:"Low Risk"})
        st.dataframe(neighbor_df,use_container_width=True)
        
        st.subheader("Business Insight")
        st.info("This decision is based on similarity with nearby customers in feature space.")

with col2:
    model_eval = KNeighborsClassifier(n_neighbors=5)
    model_eval.fit(X_train,y_train)
    y_pred = model_eval.predict(X_test)
    
    acc = accuracy_score(y_test,y_pred)
    cm = confusion_matrix(y_test,y_pred)
    
    st.subheader("Model Evaluation (K=5)")
    st.markdown(f"""
    <div class="metric-box">
    Accuracy: <b>{round(acc,3)}</b>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("Confusion Matrix")
    st.dataframe(pd.DataFrame(
        cm,
        columns=["Predicted Low","Predicted High"],
        index=["Actual Low","Actual High"]
    ))
