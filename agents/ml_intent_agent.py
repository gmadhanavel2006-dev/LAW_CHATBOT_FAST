import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import os


class MLIntentClassifier:
    """
    ML-based legal intent classifier using TF-IDF + Logistic Regression
    """

    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = LogisticRegression(max_iter=1000)
        self.is_trained = False

    def train(self, csv_path="data/intent_data.csv"):
        if not os.path.exists(csv_path):
            print("⚠️ intent_data.csv not found. Skipping training.")
            return

        data = pd.read_csv(csv_path)

        if data.empty or "text" not in data.columns or "label" not in data.columns:
            print("⚠️ intent_data.csv is empty or invalid. Skipping training.")
            return

        X = self.vectorizer.fit_transform(data["text"])
        y = data["label"]

        self.model.fit(X, y)
        self.is_trained = True

    def predict(self, text: str):
        if not self.is_trained:
            return "unknown"

        X = self.vectorizer.transform([text])
        return self.model.predict(X)[0]