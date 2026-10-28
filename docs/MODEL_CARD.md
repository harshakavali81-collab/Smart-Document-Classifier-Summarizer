# Model card

**Classifier:** scikit-learn TF-IDF 1-2 word ngrams and balanced logistic regression. Six labels: Invoice, Resume, Contract, Research, Medical, Report. Trained at runtime from 72 authored synthetic and partly templated examples, 12 per category. Scores are not calibrated. Threshold 0.25 returns an Uncertain label; effectiveness of the threshold is not validated.

**Evaluation:** python scripts/evaluate.py creates a stratified 70/30 held-out report with seed 42 and actual accuracy, class precision, recall, F1 and confusion matrix. Training/test splits share templates, so the held-out score may be much higher than performance on real documents. No production or independent external benchmark is claimed.

**Risks:** OCR scans, multilingual PDFs, complex tables, short fragments, legal/medical implications, mixed-label files, domain changes and hallucinated interpretations by readers. Medical and legal category labels do not constitute advice.

**Summarization:** selects verbatim source sentences from individual page text. This provides page traceability but cannot verify the truth or completeness of the source.

The GitHub Actions workflow also exports an SVG confusion-matrix heat map and per-class F1 bar plot from the evaluation JSON. These graphs contain computed synthetic test metrics, not invented figures or real-world accuracy claims.
