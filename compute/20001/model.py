import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib

csv_file = "../compute/PORT/Iris.csv"
iris_data = pd.read_csv(csv_file)

# Separate features and target variable
X = iris_data.drop(columns=["Id", "Species"])
y = iris_data["Species"]

# Load the initial KNN model
initial_model_file = "../compute/PORT/initial_knn_model.joblib"
knn_model = joblib.load(initial_model_file)
knn_model.fit(X, y)

# Save the trained model to a file
joblib.dump(knn_model, "../compute/PORT/weights.joblib")
