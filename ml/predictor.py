"""
predictor.py
------------
Loads the saved model and exposes predict().
"""

import os
import pickle
import re

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

_pipeline = None  # module-level cache


def _load_model():
    global _pipeline
    if _pipeline is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                "Model file not found. Please run:  python ml/train_model.py"
            )
        with open(MODEL_PATH, "rb") as f:
            _pipeline = pickle.load(f)
    return _pipeline


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def predict(title: str, text: str) -> dict:
    """
    Returns:
        {
            "prediction": "FAKE" | "REAL",
            "confidence": float (0–1),
            "fake_probability": float (0–1),
            "real_probability": float (0–1),
        }
    """
    pipe = _load_model()
    combined = clean_text(f"{title} {text}")
    proba = pipe.predict_proba([combined])[0]   # [P(real), P(fake)]
    # label 0 = REAL, label 1 = FAKE
    classes = list(pipe.classes_)
    fake_idx = classes.index(1)
    real_idx = classes.index(0)

    fake_prob = float(proba[fake_idx])
    real_prob = float(proba[real_idx])
    prediction = "FAKE" if fake_prob >= 0.5 else "REAL"
    confidence = fake_prob if prediction == "FAKE" else real_prob

    return {
        "prediction":       prediction,
        "confidence":       confidence,
        "fake_probability": fake_prob,
        "real_probability": real_prob,
    }
