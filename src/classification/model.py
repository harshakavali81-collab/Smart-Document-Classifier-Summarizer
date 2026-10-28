"""Synthetic-example TF-IDF + logistic regression document classifier."""
from functools import lru_cache
from pathlib import Path
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

DATASET = Path(__file__).resolve().parents[2] / "data" / "samples" / "training.jsonl"

def load_examples(path=DATASET) -> list[dict]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]

def train(examples: list[dict]) -> Pipeline:
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True, max_features=12000)),
        ("model", LogisticRegression(max_iter=600, class_weight="balanced", random_state=42)),
    ])
    pipeline.fit([item["text"] for item in examples], [item["label"] for item in examples])
    return pipeline

@lru_cache(maxsize=1)
def demo_model() -> Pipeline:
    # Training on synthetic examples is a demonstration, not a production-ready model.
    return train(load_examples())

def classify(text: str) -> dict:
    scores = demo_model().predict_proba([text[:20000]])[0]
    model = demo_model()
    ranked = sorted(zip(model.classes_, scores), key=lambda pair: pair[1], reverse=True)
    label, score = ranked[0]
    return {
        "label": label if float(score) >= 0.25 else "Uncertain",
        "confidence": round(float(score), 4),
        "alternatives": [{"label": name, "confidence": round(float(prob), 4)}
                         for name, prob in ranked[1:3]],
        "model_note": "Demo classifier trained on authored synthetic examples; score is not calibrated.",
    }
