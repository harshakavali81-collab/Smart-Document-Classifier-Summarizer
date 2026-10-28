from src.classification.model import load_examples, train
from src.evaluation.metrics import evaluate

def test_synthetic_training():
    examples = load_examples()
    assert len(examples) >= 60
    assert len(set(ex["label"] for ex in examples)) == 6
    classifier = train(examples)
    assert classifier.predict(["A professional resume lists Python skills, experience, and degrees."])[0] in classifier.classes_

def test_evaluation_is_reproducible():
    first = evaluate()
    second = evaluate()
    assert first["confusion_matrix"] == second["confusion_matrix"]
    assert first["test_count"] > 0
