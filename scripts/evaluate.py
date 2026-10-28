"""Create a held-out synthetic benchmark report; no real-world accuracy claim."""
import json
from pathlib import Path
from src.evaluation.metrics import evaluate

if __name__ == "__main__":
    report = evaluate()
    destination = Path("reports/model_evaluation.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"train_count": report["train_count"], "test_count": report["test_count"],
                      "macro_f1": report["classification_report"]["macro avg"]["f1-score"],
                      "artifact": str(destination)}, indent=2))
