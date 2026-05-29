this app doesnot use the aws constraints
🚀 Assignment 1 
AI-Powered Employee Attrition Prediction System
Kaggle Dataset
🏆 IBM HR Analytics Employee Attrition & Performance
Kaggle:
 https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset

Real Business Problem
An organization loses employees every month.
HR wants to predict:
Which employees are likely to leave
Why they may leave
Which factors influence attrition
Risk category of employees

Student Deliverables
Phase 1 — EDA
Identify:
Attrition rate
Department-wise attrition
Gender-wise attrition
Salary impact
Experience impact

Phase 2 — Machine Learning
Logistic Regression
Predict:
Attrition = Yes / No

Decision Tree
Generate HR decision rules.
Example:
IF
JobSatisfaction < 2
AND
MonthlyIncome < 4000

THEN
High Attrition Risk

Random Forest
Build production model.

SVM
Compare accuracy.

KNN
Find similar employees.

Naive Bayes
Probability-based prediction.

PCA
Dimensionality reduction.

K-Means
Employee Segmentation:
Cluster 1:
High Performers

Cluster 2:
At Risk

Cluster 3:
New Employees

AWS Requirements
S3
Store:
dataset/
model/
reports/

SageMaker
Train:
logistic_regression.pkl
random_forest.pkl

Endpoint
Deploy:
employee-attrition-predictor

Lambda
Input:
{
 "Age": 35,
 "MonthlyIncome": 4500,
 "JobSatisfaction": 2
}

API Gateway
POST /predict

Output
{
 "attrition_probability": 87.3,
 "risk_level": "HIGH"
}
