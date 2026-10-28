"""Evaluate the frozen demo classifier on locally supplied, independently labeled CSV.

No user-supplied document text, filenames, or example predictions are stored
in the report. This script never retrains or modifies the model under test.
It cannot independently determine whether a dataset is truly external.
"""
import argparse
import csv
import json
from pathlib import Path

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from src.classification.model import demo_model

MAX_DATASET_BYTES = 6 * 1024 * 1024
MAX_ROWS = 1000
MAX_TEXT_CHARS = 20_000


def evaluate_csv(path: str | Path) -> dict:
    source = Path(path)
    if not source.is_file() or not 0 < source.stat().st_size <= MAX_DATASET_BYTES:
        raise ValueError("The CSV must exist, be nonempty, and be at most 6 MiB.")
    model = demo_model()
    classes = sorted(str(x) for x in model.classes_)
    truth, texts = [], []
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not {"label", "text"}.issubset(reader.fieldnames):
            raise ValueError("The CSV must contain 'label' and 'text' columns.")
        for row in reader:
            if len(texts) >= MAX_ROWS:
                raise ValueError(f"Evaluation exceeds the {MAX_ROWS}-row maximum.")
            label, text = row.get("label", ""), row.get("text", "")
            if label not in classes or not 8 <= len(text.split()) or len(text) > MAX_TEXT_CHARS:
                raise ValueError("Invalid label, insufficient text or overlong text in dataset.")
            truth.append(label)
            texts.append(text)
    if len(truth) < 12 or len(set(truth)) < 2:
        raise ValueError("Provide at least 12 labeled documents across at least two classes.")
    predicted = model.predict(texts).tolist()
    return {
        "evaluation_type": "local user-supplied CSV; independence and label quality unverified",
        "model": "frozen bundled synthetic-trained TF-IDF/logistic regression",
        "example_count": len(truth),
        "class_labels": classes,
        "accuracy": round(float(accuracy_score(truth, predicted)), 6),
        "classification_report": classification_report(truth, predicted, labels=classes, output_dict=True, zero_division=0),
        "confusion_matrix": confusion_matrix(truth, predicted, labels=classes).tolist(),
        "privacy_note": "Contains aggregate metrics only; no source text, filenames, or row-level predictions.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the frozen demo model on a private local CSV.")
    parser.add_argument("csv", help="UTF-8 CSV with label and text columns; do not commit private data.")
    parser.add_argument("--output", default="reports/external_evaluation.json")
    args = parser.parse_args()
    result = evaluate_csv(args.csv)
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"evaluated_rows": result["example_count"], "accuracy": result["accuracy"],
                      "report_path": str(target), "note": result["evaluation_type"]}, indent=2))


if __name__ == "__main__":
    main()
