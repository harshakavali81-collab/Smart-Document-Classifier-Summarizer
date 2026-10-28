import xml.etree.ElementTree as ET
from src.evaluation.metrics import evaluate
from scripts.make_eval_charts import create_charts

def test_real_synthetic_graphs_are_well_formed(tmp_path):
    report = evaluate()
    create_charts(report, tmp_path)
    for file in ["confusion_matrix.svg", "per_class_f1.svg"]:
        root = ET.parse(tmp_path / file).getroot()
        assert root.tag.endswith("svg")
        assert (tmp_path / file).stat().st_size > 500
