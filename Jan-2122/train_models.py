import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC

# -------------------------------
# Load dataset
# -------------------------------
df = pd.read_csv("train.csv")

# -------------------------------
# Preprocessing
# -------------------------------
df['LoanAmount'].fillna(df['LoanAmount'].median(), inplace=True)
df['Credit_History'].fillna(0, inplace=True)
df.fillna(method='ffill', inplace=True)

le = LabelEncoder()
cols = ['Gender','Married','Education','Self_Employed',
        'Property_Area','Loan_Status']

for col in cols:
    df[col] = le.fit_transform(df[col])

# -------------------------------
# Features & Target
# -------------------------------
X = df[['ApplicantIncome','LoanAmount',
        'Credit_History','Self_Employed','Property_Area']]
y = df['Loan_Status']

# -------------------------------
# Train-Test Split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# -------------------------------
# Scaling
# -------------------------------
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)

# -------------------------------
# Train Models
# -------------------------------
svm_linear = SVC(kernel='linear', probability=True)
svm_poly = SVC(kernel='poly', degree=3, probability=True)
svm_rbf = SVC(kernel='rbf', probability=True)

svm_linear.fit(X_train, y_train)
svm_poly.fit(X_train, y_train)
svm_rbf.fit(X_train, y_train)

# -------------------------------
# SAVE MODELS (CRITICAL)
# -------------------------------
pickle.dump(svm_linear, open("svm_linear.pkl", "wb"))
pickle.dump(svm_poly, open("svm_poly.pkl", "wb"))
pickle.dump(svm_rbf, open("svm_rbf.pkl", "wb"))
pickle.dump(scaler, open("scaler.pkl", "wb"))

print("✅ Models & scaler saved successfully")
