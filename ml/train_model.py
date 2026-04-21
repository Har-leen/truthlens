"""
train_model.py
--------------
Run this script ONCE to train the fake-news classifier and save the model.

Usage:
    python ml/train_model.py

The script reads fake_news_dataset.csv (placed at project root),
trains a Logistic Regression pipeline with TF-IDF features,
and saves model.pkl to the ml/ directory.
"""

import os
import pickle
import re

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
DATA_PATH  = os.path.join(os.path.dirname(__file__), "..", "fake_news_dataset.csv")


def clean_text(text: str) -> str:
    """Basic text cleaning."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " ", text)      # remove URLs
    text = re.sub(r"[^a-z\s]", " ", text)             # keep only letters
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.dropna(subset=["text", "label"])
    df["combined"] = (
        df["title"].fillna("").astype(str) + " " + df["text"].astype(str)
    )
    df["combined"] = df["combined"].apply(clean_text)
    return df


def train():
    print("Loading dataset …")
    df = load_data(DATA_PATH)
    print(f"  Rows: {len(df)}  |  Label distribution:\n{df['label'].value_counts()}")

    X = df["combined"]
    y = df["label"]          # 1 = fake, 0 = real

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            max_features=60_000,
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=2,
        )),
        ("clf", LogisticRegression(
            max_iter=1000,
            C=5.0,
            solver="lbfgs",
            n_jobs=-1,
        )),
    ])

    print("Training …")
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nTest Accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred, target_names=["REAL", "FAKE"]))

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(pipeline, f)
    print(f"Model saved → {MODEL_PATH}")


if __name__ == "__main__":
    train()
