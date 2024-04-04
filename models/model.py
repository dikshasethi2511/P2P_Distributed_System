import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib

csv_file = "../compute/8080/Iris_shard_1.csv"
iris_data = pd.read_csv(csv_file)

# Separate features and target variable
X = iris_data.drop(columns=["Id", "Species"])
y = iris_data["Species"]

# Train the KNN model
k = 3  # You can adjust the value of k as per your requirement
knn_model = KNeighborsClassifier(n_neighbors=k)
knn_model.fit(X, y)

# Save the trained model to a file
joblib.dump(knn_model, "knn_model.joblib")
