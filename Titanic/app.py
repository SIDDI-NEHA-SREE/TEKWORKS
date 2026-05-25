import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

st.set_page_config(
    page_title="Titanic Survival Prediction",
    page_icon="🚢",
    layout="wide"
)

@st.cache_resource
def train_model():

    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

    df = pd.read_csv(url)

    df = df[['Pclass','Sex','Age','SibSp','Parch','Fare','Embarked','Survived']]

    df['Age'] = df['Age'].fillna(df['Age'].median())
    df['Fare'] = df['Fare'].fillna(df['Fare'].median())
    df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])

    df['Sex'] = df['Sex'].map({
        'male':0,
        'female':1
    })

    df['Embarked'] = df['Embarked'].map({
        'S':0,
        'C':1,
        'Q':2
    })

    X = df.drop('Survived',axis=1)
    y = df['Survived']

    X_train,X_test,y_train,y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train,y_train)

    accuracy = model.score(X_test,y_test)

    return model,accuracy


model,accuracy = train_model()

st.title("🚢 Titanic Survival Prediction System")

st.markdown(
"""
Predict whether a passenger would survive the Titanic disaster.
"""
)

st.sidebar.header("Passenger Details")

pclass = st.sidebar.selectbox(
    "Passenger Class",
    [1,2,3]
)

sex = st.sidebar.selectbox(
    "Gender",
    ["Male","Female"]
)

age = st.sidebar.slider(
    "Age",
    0,
    80,
    25
)

sibsp = st.sidebar.slider(
    "Siblings / Spouses",
    0,
    8,
    0
)

parch = st.sidebar.slider(
    "Parents / Children",
    0,
    6,
    0
)

fare = st.sidebar.slider(
    "Fare",
    0,
    550,
    50
)

embarked = st.sidebar.selectbox(
    "Embarked Port",
    ["Southampton","Cherbourg","Queenstown"]
)

sex_map = {
    "Male":0,
    "Female":1
}

embark_map = {
    "Southampton":0,
    "Cherbourg":1,
    "Queenstown":2
}

features = pd.DataFrame(
    [[
        pclass,
        sex_map[sex],
        age,
        sibsp,
        parch,
        fare,
        embark_map[embarked]
    ]],
    columns=[
        'Pclass',
        'Sex',
        'Age',
        'SibSp',
        'Parch',
        'Fare',
        'Embarked'
    ]
)

if st.button("Predict Survival"):

    prediction = model.predict(features)[0]

    probability = model.predict_proba(features)[0][1]

    st.subheader("Prediction Result")

    if prediction == 1:

        st.success(
            f"Passenger likely SURVIVES ✅\n\nConfidence: {probability:.2%}"
        )

    else:

        st.error(
            f"Passenger likely DOES NOT SURVIVE ❌\n\nConfidence: {(1-probability):.2%}"
        )

st.divider()

st.metric(
    "Model Accuracy",
    f"{accuracy:.2%}"
)

st.caption(
    "Built with Streamlit + Scikit-Learn"
)
