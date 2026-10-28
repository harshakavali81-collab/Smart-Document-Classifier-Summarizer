"""Reproducible held-out report. Synthetic corpus may overstate real-world performance."""
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from src.classification.model import load_examples, train

def evaluate() -> dict:
    examples = load_examples()
    labels = sorted(set(x["label"] for x in examples))
    train_rows, test_rows = train_test_split(examples, test_size=0.30, stratify=[x["label"] for x in examples], random_state=42)
    model = train(train_rows)
    truth = [x["label"] for x in test_rows]
    predicted = model.predict([x["text"] for x in test_rows]).tolist()
    return {
        "dataset": "authored synthetic examples",
        "train_count": len(train_rows),
        "test_count": len(test_rows),
        "note": "Synthetic test split is not a real-world generalization estimate.",
        "labels": labels,
        "confusion_matrix": confusion_matrix(truth, predicted, labels=labels).tolist(),
        "classification_report": classification_report(truth, predicted, output_dict=True, zero_division=0),
    }
