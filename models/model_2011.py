import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize the TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Load the dataset
csv_file = "../compute/" + str(PORT) + "/2011.csv"
data = pd.read_csv(csv_file)

# Handling missing values
data.dropna(
    subset=[
        "Application Date",
        "Status",
        "Publication Number",
        "Publication Date(U/S 11A)",
        "Publication Type",
        "Application Filing Date",
        "Classification (IPC)",
        "Inventor Name",
        "Inventor Address",
        "Inventor Country",
        "Inventor Nationality",
        "Applicant Name",
        "Applicant Address",
        "Applicant Country",
        "Applicant Nationality",
        "Application Type",
        "REQUEST FOR EXAMINATION DATE",
        "Application Status",
    ],
    inplace=True,
)

# Fill remaining missing values
data["Priority Number"].fillna("Unknown", inplace=True)
data["Priority Country"].fillna("Unknown", inplace=True)
data["Priority Date"].fillna("Unknown", inplace=True)
data["Field Of Invention"].fillna("Unknown", inplace=True)
data["PARENT APPLICATION NUMBER"].fillna("Unknown", inplace=True)
data["PARENT APPLICATION FILING DATE"].fillna("Unknown", inplace=True)
data["FIRST EXAMINATION REPORT DATE"].fillna("Unknown", inplace=True)
data["Date Of Certificate Issue"].fillna("Unknown", inplace=True)
data["POST GRANT JOURNAL DATE"].fillna("Unknown", inplace=True)
data["REPLY TO FER DATE"].fillna("Unknown", inplace=True)
data["PCT INTERNATIONAL APPLICATION NUMBER"].fillna("Unknown", inplace=True)
data["PCT INTERNATIONAL FILING DATE"].fillna("Unknown", inplace=True)
data["E-MAIL (As Per Record)"].fillna("Unknown", inplace=True)
data["ADDITIONAL-EMAIL (As Per Record)"].fillna("Unknown", inplace=True)
data["E-MAIL (UPDATED Online)"].fillna("Unknown", inplace=True)

# Splitting the data into features (X) and target variable (y)
X = tfidf_vectorizer.fit_transform(data["Title"])
y = data["Application Status"]

# Load the initial KNN model
initial_model_file = "../compute/" + str(PORT) + "/initial_knn_model_2011.joblib"
knn_model = joblib.load(initial_model_file)
knn_model.fit(X, y)

# Save the trained model to a file
joblib.dump(knn_model, "../compute/" + str(PORT) + "/weights.joblib")
