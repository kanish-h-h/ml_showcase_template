from operator import mod
import os
import pickle
import joblib
from pathlib import Path


class ModelManager:
    """Centralized model loading and caching"""

    _models = {}  # singleton pattern - load once, use everywhere

    @classmethod
    def get_model(cls, model_name):
        """Get or load model (cached)"""
        if model_name not in cls._models:
            model_path = Path(__file__).parent / f"{model_name}.pkl"
            print(f"Loading model: {model_name}")

            # Support mulitple formats
            if model_path.suffix == ".pkl":
                with open(model_path, "rb") as f:
                    cls._models[model_name] = pickle.load(f)
            elif model_path.suffix == ".joblib":
                cls._models[model_name] = joblib.load(model_path)
            else:
                raise ValueError(f"Unsupported model format: {model_path.suffix}")

        return cls._models[model_name]

    @classmethod
    def list_available_models(cls):
        """List all models in models/ directory"""
        model_dir = Path(__file__).parent
        return [f.stem for f in model_dir.glob("*.pkl")] + [
            f.stem for f in model_dir.glob("*.joblib")
        ]


# Example: Your custom model wrapper
class SentimentClassifier:
    def __init__(self) -> None:
        self.model = ModelManager.get_model("sentiment_model")
        self.vectorizer = ModelManager.get_model("tfidf_vectorizer")

    def predict(self, text):
        """Predict sentiment with confidence"""
        import numpy as np

        # Preprocess
        X = self.vectorizer.transform([text])

        # Predict
        prediciton = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]

        return {
            "sentiment": "positive" if prediciton == 1 else "negative",
            "confidence": float(max(probabilities)),
            "probabilities": {
                "negative": float(probabilities[0]),
                "positive": float(probabilities[1]),
            },
        }
