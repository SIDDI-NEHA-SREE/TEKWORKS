import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="House Price Prediction – Stacking Model", layout="wide")
st.title("🎯 House Price Prediction System – Stacking Model")
st.write("This system uses a **Stacking Ensemble Machine Learning model** to predict house prices by combining multiple ML models for better decision making.")

st.sidebar.header("🏠 Enter House Details")

def user_input_features():
    bedrooms = st.sidebar.number_input("Bedrooms", 0, 10, 3)
    bathrooms = st.sidebar.number_input("Bathrooms", 0.0, 10.0, 2.0)
    sqft_living = st.sidebar.number_input("Living Area (sqft)", 300, 10000, 1500)
    sqft_lot = st.sidebar.number_input("Lot Size (sqft)", 300, 50000, 5000)
    floors = st.sidebar.number_input("Floors", 1.0, 5.0, 1.0)
    waterfront = st.sidebar.selectbox("Waterfront", [0, 1])
    view = st.sidebar.slider("View (0-4)", 0, 4, 0)
    condition = st.sidebar.slider("Condition (1-5)", 1, 5, 3)
    grade = st.sidebar.slider("Grade (1-13)", 1, 13, 7)
    sqft_above = st.sidebar.number_input("Sqft Above", 300, 8000, 1000)
    sqft_basement = st.sidebar.number_input("Sqft Basement", 0, 3000, 500)
    zipcode = st.sidebar.number_input("Zipcode", 10000, 99999, 98103)
    lat = st.sidebar.number_input("Latitude", value=47.6)
    long = st.sidebar.number_input("Longitude", value=-122.3)
    sqft_living15 = st.sidebar.number_input("Living 15 Nearby (sqft)", 300, 10000, 1500)
    sqft_lot15 = st.sidebar.number_input("Lot 15 Nearby (sqft)", 300, 50000, 5000)

    data = {
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'sqft_living': sqft_living,
        'sqft_lot': sqft_lot,
        'floors': floors,
        'waterfront': waterfront,
        'view': view,
        'condition': condition,
        'grade': grade,
        'sqft_above': sqft_above,
        'sqft_basement': sqft_basement,
        'zipcode': zipcode,
        'lat': lat,
        'long': long,
        'sqft_living15': sqft_living15,
        'sqft_lot15': sqft_lot15
    }
    return pd.DataFrame(data, index=[0])

input_df = user_input_features()

st.subheader("🧩 Stacking Model Architecture")
st.info("""
**Base Models:**
- Linear Regression
- Decision Tree
- Random Forest

**Meta Model:**
- Linear Regression
""")

data = pd.read_csv("kc_house_data.csv")

# Drop date and id columns
columns_to_drop = ['id', 'date', 'yr_built', 'yr_renovated']
for col in columns_to_drop:
    if col in data.columns:
        data = data.drop(col, axis=1)

X = data.drop(['price'], axis=1)
y = data['price']

X = X.apply(pd.to_numeric, errors='coerce').fillna(0)
input_df = input_df.apply(pd.to_numeric, errors='coerce').fillna(0)

# Ensure input_df has the same columns as X
input_df = input_df[X.columns]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
input_scaled = scaler.transform(input_df)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

lr = LinearRegression()
dt = DecisionTreeRegressor(random_state=42)
rf = RandomForestRegressor(random_state=42, n_estimators=100)

stacking_model = StackingRegressor(
    estimators=[('lr', lr), ('dt', dt), ('rf', rf)],
    final_estimator=LinearRegression()
)

stacking_model.fit(X_train, y_train)

if st.button("🔘 Predict Price (Stacking Model)"):
    lr_pred = lr.fit(X_train, y_train).predict(input_scaled)[0]
    dt_pred = dt.fit(X_train, y_train).predict(input_scaled)[0]
    rf_pred = rf.fit(X_train, y_train).predict(input_scaled)[0]
    final_pred = stacking_model.predict(input_scaled)[0]

    st.subheader("🏷 Prediction Result")
    st.success(f"💰 Predicted House Price: ${final_pred:,.2f}")

    st.subheader("📊 Base Model Predictions")
    st.write(f"Linear Regression → ${lr_pred:,.2f}")
    st.write(f"Decision Tree → ${dt_pred:,.2f}")
    st.write(f"Random Forest → ${rf_pred:,.2f}")

    st.subheader("🧠 Final Stacking Decision")
    st.write(f"Predicted Price → ${final_pred:,.2f}")

st.subheader("💡 Business Explanation")
st.info(
    "Based on the house features and combined predictions from multiple models, "
    "the price of the house may vary. The stacking model intelligently combines "
    "base model predictions to provide a more accurate estimate."
)
