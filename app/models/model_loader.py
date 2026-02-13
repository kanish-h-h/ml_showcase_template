import os
import pickle
import joblib
from pathlib import Path


class ModelManager:
    """Centralized model loading and caching"""

    _models = {}

    @classmethod
    def get_model(cls, model_name):
        """Get or load model (cached)"""
        if model_name not in cls._models:
            model_path = Path(__file__).parent / f"{model_name}.pkl"

            # If model doesn't exist, return a mock model for demo
            if not model_path.exists():
                print(f"⚠️ Model '{model_name}' not found. Using mock model.")
                return MockModel()

            print(f"Loading model: {model_name}")

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


# Mock model for demo purposes (when real models don't exist yet)
class MockModel:
    def predict(self, X):
        import numpy as np

        # Return random predictions for demo
        return np.random.randint(0, 2, size=len(X) if hasattr(X, "__len__") else 1)

    def predict_proba(self, X):
        import numpy as np

        # Return random probabilities
        probs = np.random.rand(len(X) if hasattr(X, "__len__") else 1, 2)
        return probs / probs.sum(axis=1, keepdims=True)


# Example: Your custom model wrapper
class SentimentClassifier:
    def __init__(self):
        try:
            self.model = ModelManager.get_model("sentiment_model")
            self.vectorizer = ModelManager.get_model("tfidf_vectorizer")
        except:
            # Use mock if models don't exist
            self.model = MockModel()
            self.vectorizer = MockVectorizer()

    def predict(self, text):
        """Predict sentiment with confidence"""
        import numpy as np

        # Preprocess
        X = self.vectorizer.transform([text])

        # Predict
        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]

        return {
            "sentiment": "positive" if prediction == 1 else "negative",
            "confidence": float(max(probabilities)),
            "probabilities": {
                "negative": float(probabilities[0]),
                "positive": float(probabilities[1]),
            },
        }


class MockVectorizer:
    def transform(self, texts):
        import numpy as np

        # Return random features for demo
        return np.random.rand(len(texts), 100)
