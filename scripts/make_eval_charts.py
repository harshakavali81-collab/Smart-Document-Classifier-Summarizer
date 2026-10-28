"""Generate evaluation SVGs from measured held-out synthetic test results.

No chart contains invented numbers. These are still synthetic benchmark outputs,
not independent real-document classification accuracy.
"""
import json
from pathlib import Path
from xml.sax.saxutils import escape

SOURCE = Path("reports/model_evaluation.json")
OUT = Path("reports")

def header(title: str, subtitle: str) -> list[str]:
    return [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 660" role="img">',
        '<rect width="1000" height="660" fill="#081a2c"/>',
        '<text x="60" y="67" font-family="Arial" font-size="32" font-weight="bold" fill="#e8f7ff">' + escape(title) + '</text>',
        '<text x="60" y="100" font-family="Arial" font-size="16" fill="#93b7ca">' + escape(subtitle) + '</text>',
    ]

def finish(parts: list[str], target: Path):
    parts.append('<text x="60" y="620" font-family="Arial" font-size="14" fill="#96b4c3">Synthetic held-out test set only - not real-world model performance.</text>')
    parts.append('</svg>')
    target.write_text("\n".join(parts), encoding="utf-8")

def create_charts(report: dict, target_dir: Path = OUT):
    target_dir.mkdir(parents=True, exist_ok=True)
    labels = report["labels"]
    matrix = report["confusion_matrix"]
    maximum = max((max(row) for row in matrix), default=1) or 1
    parts = header("Classification confusion matrix", "Measured from held-out, templated synthetic examples")
    start_x, start_y, cell = 268, 176, 62
    for i, label in enumerate(labels):
        parts.append(f'<text x="250" y="{start_y+i*cell+38}" text-anchor="end" fill="#d0e4ee" font-family="Arial" font-size="17">{escape(label)}</text>')
        parts.append(f'<text x="{start_x+i*cell+30}" y="150" text-anchor="middle" fill="#d0e4ee" font-family="Arial" font-size="16">{escape(label)}</text>')
        for j, value in enumerate(matrix[i]):
            intensity = int(24 + 150 * value / maximum)
            color = f'rgb(23,{intensity+35},125)'
            x, y = start_x+j*cell, start_y+i*cell
            parts.append(f'<rect x="{x}" y="{y}" width="58" height="58" rx="7" fill="{color}" stroke="#35526a"/>')
            parts.append(f'<text x="{x+29}" y="{y+35}" text-anchor="middle" fill="#f0fbff" font-family="Arial" font-size="21" font-weight="bold">{value}</text>')
    finish(parts, target_dir / "confusion_matrix.svg")
    parts = header("Per-class F1 score", "Measured synthetic holdout - 1.0 represents perfect score on these test examples")
    for i, label in enumerate(labels):
        y = 165 + i*65
        value = float(report["classification_report"][label]["f1-score"])
        parts.append(f'<text x="74" y="{y+23}" fill="#d9edf3" font-family="Arial" font-size="19">{escape(label)}</text>')
        parts.append(f'<rect x="245" y="{y}" width="600" height="29" rx="7" fill="#1b3b51"/>')
        parts.append(f'<rect x="245" y="{y}" width="{value*600:.1f}" height="29" rx="7" fill="#70e0c3"/>')
        parts.append(f'<text x="875" y="{y+22}" fill="#b2f5df" font-family="Arial" font-size="19">{value:.3f}</text>')
    finish(parts, target_dir / "per_class_f1.svg")

if __name__ == "__main__":
    create_charts(json.loads(SOURCE.read_text(encoding="utf-8")))
    print("Saved synthetic evaluation charts in reports/")
