# Independent validation playbook

The model in this repository is trained using 72 fictional, templated examples. Its bundled synthetic holdout results are **not** production-quality evidence.

## Locally evaluate genuinely independent, consented documents

1. Obtain a legally licensed dataset of real documents with explicit permission for the intended evaluation. Never upload private or confidential source documents to this public GitHub repository.
2. Manually review label definitions for the six classes: Invoice, Resume, Contract, Research, Medical and Report. Establish multi-label policies and adjudication rules.
3. Save a **local only** UTF-8 CSV, with columns named \`label,text\`. Use at least 12 independently labeled documents from two or more classes. Recommended: substantially more per class.
4. Run the frozen classifier, without retraining on evaluation examples:

~~~bash
python -m scripts.evaluate_external private_documents.csv
~~~

5. Inspect **reports/external_evaluation.json** (ignored by Git), including the confusion matrix, class-specific recall, precision and F1. The tool stores only aggregated metrics.
6. Audit confusion examples locally and document dataset provenance, annotator agreement, split boundaries, class prevalence and language/domain coverage. The tool **cannot confirm** dataset independence or licensing.
7. Perform independent tests for prompt-like embedded text, tables, handwritten/scan-only PDFs, encrypted PDFs, mixed-language text, long documents and duplicate templates.
8. Choose an operational abstention threshold only after confidence calibration and human review. Never use a raw model score as a safety assurance.

## Decision checklist

- A real-world benchmark was acquired and is appropriately licensed.
- Duplicate or related company templates do not cross train/test boundaries.
- Medical/legal classification is used only for document-type organization, not professional advice.
- Evaluation includes human-reviewed citation fidelity, completeness and failure cases.
- Privacy, encryption, authentication, malware scanning and isolation are complete before accepting external users.

Until these steps have **actually been performed**, treat DocSight AI as a portfolio prototype rather than a validated service.
