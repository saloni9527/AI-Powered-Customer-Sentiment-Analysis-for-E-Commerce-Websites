import os
import pickle
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


def train_models(X_train, X_test, y_train, y_test):

    # Create models folder if not exists
    os.makedirs("models", exist_ok=True)

    models = {
        "NaiveBayes": MultinomialNB(),
        "SVM": SVC(),
        "LogisticRegression": LogisticRegression(max_iter=1000),
        "DecisionTree": DecisionTreeClassifier(),
        "KNN": KNeighborsClassifier()
    }

    best_model = None
    best_accuracy = 0

    for name, model in models.items():

        print(f"🔄 Training {name} model...")

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)

        print(f"✅ {name} Accuracy: {accuracy}")

        # Save each model
        with open(f"models/{name}.pkl", "wb") as f:
            pickle.dump(model, f)

        print(f"💾 {name} model saved successfully\n")

        # Check best model
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = model

    # Save best model
    with open("models/saved_model.pkl", "wb") as f:
        pickle.dump(best_model, f)

    print("🏆 Best model saved as saved_model.pkl")
    print("🎉 All ML Models Trained Successfully!")


# 🚀 MAIN PROGRAM
if __name__ == "__main__":

    print("🚀 ML Models script started")

    # Load dataset
    data = pd.read_csv("dataset/clothing_reviews.csv")

    data = data.dropna()

    # Features & labels
    X = data["Review Text"]
    y = data["Rating"]

    # Convert text → numerical
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(X)

    # Save vectorizer (IMPORTANT for prediction)
    os.makedirs("models", exist_ok=True)
    with open("models/vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)

    print("💾 Vectorizer saved successfully")

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train models
    train_models(X_train, X_test, y_train, y_test)