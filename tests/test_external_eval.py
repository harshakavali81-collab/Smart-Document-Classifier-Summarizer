import csv

import pytest

from scripts.evaluate_external import evaluate_csv
from src.classification.model import load_examples


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["label", "text"])
        writer.writeheader()
        writer.writerows(rows)


def test_external_evaluation_does_not_echo_source_text(tmp_path):
    rows = load_examples()[:12] + load_examples()[12:24]
    sample = "LOCAL_ONLY_PRIVATE_SENTINEL_Redacted123"
    rows[0] = dict(rows[0], text=rows[0]["text"] + " " + sample)
    path = tmp_path / "private.csv"
    write_csv(path, rows)
    report = evaluate_csv(path)
    assert report["example_count"] == len(rows)
    assert sample not in str(report) and str(path) not in str(report)
    assert len(report["confusion_matrix"]) == 6


def test_external_evaluation_rejects_unknown_labels(tmp_path):
    path = tmp_path / "bad.csv"
    write_csv(path, [{"label": "NotARealCategory", "text": "This is enough text for a category prediction."}] * 12)
    with pytest.raises(ValueError, match="Invalid label"):
        evaluate_csv(path)


def test_external_evaluation_rejects_short_corpus(tmp_path):
    path = tmp_path / "short.csv"
    write_csv(path, load_examples()[:3])
    with pytest.raises(ValueError, match="at least 12"):
        evaluate_csv(path)
