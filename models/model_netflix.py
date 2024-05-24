import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib

csv_file = "../compute/" + str(PORT) + "/netflix.csv"
data = pd.read_csv(csv_file, encoding="latin1")

data.drop(
    columns=[
        "Unnamed: 12",
        "Unnamed: 13",
        "Unnamed: 14",
        "Unnamed: 15",
        "Unnamed: 16",
        "Unnamed: 17",
        "Unnamed: 18",
        "Unnamed: 19",
        "Unnamed: 20",
        "Unnamed: 21",
        "Unnamed: 22",
        "Unnamed: 23",
        "Unnamed: 24",
        "Unnamed: 25",
    ],
    inplace=True,
)

# Handling missing values
data.dropna(subset=["date_added", "rating", "duration"], inplace=True)
data["director"].fillna("Unknown", inplace=True)
data["cast"].fillna("Unknown", inplace=True)
data["country"].fillna("Unknown", inplace=True)

# Splitting the data into features (X) and target variable (y)
X = data.drop(columns=["show_id", "title", "type", "description"])
y = data["type"]

# Load the initial KNN model
initial_model_file = "../compute/" + str(PORT) + "/initial_knn_model_netflix.joblib"
knn_model = joblib.load(initial_model_file)
knn_model.fit(X, y)

# Save the trained model to a file
joblib.dump(knn_model, "../compute/" + str(PORT) + "/weights.joblib")
