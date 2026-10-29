# Repository standard

## Layout

This repository keeps its working source paths. A shared portfolio structure does not require moving a React application, Python package, BI workbook or Verilog project into identical runtime directories.

| Area | Convention |
| --- | --- |
| Landing page | `README.md`: purpose, visuals, demo, features, stack, architecture, setup, tradeoffs and roadmap |
| Detailed reference | `PROJECT_GUIDE.md`: retained project-specific explanation and historical release notes |
| Documentation | `docs/`: design, inventory, reproduction and evidence |
| Work intake | `.github/ISSUE_TEMPLATE/`: bug and feature forms |
| Review | `.github/PULL_REQUEST_TEMPLATE.md`: linked issue, behavior and validation |
| Automation | `.github/workflows/portfolio-docs.yml`: README section and local-link checks |
| Source and tests | Existing project-specific paths listed below; no empty source/test placeholders |

## Workflow

1. Open an issue describing the user problem and measurable acceptance criteria.
2. Add it to a GitHub Project with Todo, In progress, Review and Done states when a board is configured.
3. Use a focused branch and meaningful commits, such as `docs: correct local setup paths` or `fix(api): reject malformed input`.
4. Run the project's documented checks and `python scripts/check_portfolio_docs.py`.
5. Open a pull request with actual validation results and `Closes #<issue-number>`.
6. Merge after review; record release evidence and update the issue/board.

Board creation, profile pins, repository social previews and milestone settings require account-level configuration. This file does not claim those settings have been applied.

## Validation scope

The documentation check validates the landing-page headings and local link targets only. It does not execute models, certify test coverage, inspect Git history for secrets, verify external websites, or prove production readiness. Existing application workflows remain the source of runtime CI evidence.

Keep credentials in local environment variables. A gitignore rule does not remove secrets already tracked or committed. Use only permitted sample data in public demos.

## Inventory at standardization

The following are the pre-existing public project files. New standardization files are described above. Historical guides may mention external bundles that are not part of this list.

- [`Dockerfile`](<../Dockerfile>)
- [`LICENSE`](<../LICENSE>)
- [`README.md`](<../README.md>)
- [`SECURITY.md`](<../SECURITY.md>)
- [`START_WINDOWS.ps1`](<../START_WINDOWS.ps1>)
- [`assets`](<../assets>)
- [`assets/01-product-preview.svg`](<../assets/01-product-preview.svg>)
- [`assets/02-end-to-end-workflow.svg`](<../assets/02-end-to-end-workflow.svg>)
- [`assets/03-system-architecture.svg`](<../assets/03-system-architecture.svg>)
- [`assets/04-ingestion-pipeline.svg`](<../assets/04-ingestion-pipeline.svg>)
- [`assets/05-classification-graph.svg`](<../assets/05-classification-graph.svg>)
- [`assets/06-summarization-logic.svg`](<../assets/06-summarization-logic.svg>)
- [`assets/07-page-citation-map.svg`](<../assets/07-page-citation-map.svg>)
- [`assets/08-analytics-graphs.svg`](<../assets/08-analytics-graphs.svg>)
- [`assets/09-security-safeguards.svg`](<../assets/09-security-safeguards.svg>)
- [`assets/10-ci-deployment.svg`](<../assets/10-ci-deployment.svg>)
- [`backend`](<../backend>)
- [`backend/__init__.py`](<../backend/__init__.py>)
- [`backend/app`](<../backend/app>)
- [`backend/app/__init__.py`](<../backend/app/__init__.py>)
- [`backend/app/db`](<../backend/app/db>)
- [`backend/app/db/__init__.py`](<../backend/app/db/__init__.py>)
- [`backend/app/db/store.py`](<../backend/app/db/store.py>)
- [`backend/app/main.py`](<../backend/app/main.py>)
- [`backend/app/routes`](<../backend/app/routes>)
- [`backend/app/routes/__init__.py`](<../backend/app/routes/__init__.py>)
- [`backend/app/routes/documents.py`](<../backend/app/routes/documents.py>)
- [`backend/app/schemas`](<../backend/app/schemas>)
- [`backend/app/schemas/__init__.py`](<../backend/app/schemas/__init__.py>)
- [`backend/app/schemas/models.py`](<../backend/app/schemas/models.py>)
- [`backend/app/services`](<../backend/app/services>)
- [`backend/app/services/__init__.py`](<../backend/app/services/__init__.py>)
- [`backend/app/services/analyze.py`](<../backend/app/services/analyze.py>)
- [`data`](<../data>)
- [`data/samples`](<../data/samples>)
- [`data/samples/README.md`](<../data/samples/README.md>)
- [`data/samples/example_report.txt`](<../data/samples/example_report.txt>)
- [`data/samples/training.jsonl`](<../data/samples/training.jsonl>)
- [`docker-compose.yml`](<../docker-compose.yml>)
- [`docs`](<../docs>)
- [`docs/API.md`](<../docs/API.md>)
- [`docs/ARCHITECTURE.md`](<../docs/ARCHITECTURE.md>)
- [`docs/DEPLOYMENT.md`](<../docs/DEPLOYMENT.md>)
- [`docs/MODEL_CARD.md`](<../docs/MODEL_CARD.md>)
- [`docs/OPERATIONS.md`](<../docs/OPERATIONS.md>)
- [`docs/PORTFOLIO_CASE_STUDY.md`](<../docs/PORTFOLIO_CASE_STUDY.md>)
- [`docs/PROJECT_TREE.txt`](<../docs/PROJECT_TREE.txt>)
- [`docs/REAL_WORLD_VALIDATION.md`](<../docs/REAL_WORLD_VALIDATION.md>)
- [`docs/RELEASE_CHECKLIST.md`](<../docs/RELEASE_CHECKLIST.md>)
- [`docs/SECURITY.md`](<../docs/SECURITY.md>)
- [`frontend`](<../frontend>)
- [`frontend/Dockerfile`](<../frontend/Dockerfile>)
- [`frontend/index.html`](<../frontend/index.html>)
- [`frontend/nginx.conf`](<../frontend/nginx.conf>)
- [`frontend/package.json`](<../frontend/package.json>)
- [`frontend/src`](<../frontend/src>)
- [`frontend/src/App.jsx`](<../frontend/src/App.jsx>)
- [`frontend/src/main.jsx`](<../frontend/src/main.jsx>)
- [`frontend/src/styles.css`](<../frontend/src/styles.css>)
- [`frontend/vite.config.js`](<../frontend/vite.config.js>)
- [`portfolio`](<../portfolio>)
- [`portfolio/PORTFOLIO_CARD.md`](<../portfolio/PORTFOLIO_CARD.md>)
- [`pyproject.toml`](<../pyproject.toml>)
- [`requirements-dev.txt`](<../requirements-dev.txt>)
- [`requirements.txt`](<../requirements.txt>)
- [`scripts`](<../scripts>)
- [`scripts/__init__.py`](<../scripts/__init__.py>)
- [`scripts/evaluate.py`](<../scripts/evaluate.py>)
- [`scripts/evaluate_external.py`](<../scripts/evaluate_external.py>)
- [`scripts/make_eval_charts.py`](<../scripts/make_eval_charts.py>)
- [`scripts/smoke_api.py`](<../scripts/smoke_api.py>)
- [`scripts/train_classifier.py`](<../scripts/train_classifier.py>)
- [`src`](<../src>)
- [`src/__init__.py`](<../src/__init__.py>)
- [`src/classification`](<../src/classification>)
- [`src/classification/__init__.py`](<../src/classification/__init__.py>)
- [`src/classification/model.py`](<../src/classification/model.py>)
- [`src/evaluation`](<../src/evaluation>)
- [`src/evaluation/__init__.py`](<../src/evaluation/__init__.py>)
- [`src/evaluation/metrics.py`](<../src/evaluation/metrics.py>)
- [`src/ingestion`](<../src/ingestion>)
- [`src/ingestion/__init__.py`](<../src/ingestion/__init__.py>)
- [`src/ingestion/pdf.py`](<../src/ingestion/pdf.py>)
- [`src/preprocessing`](<../src/preprocessing>)
- [`src/preprocessing/__init__.py`](<../src/preprocessing/__init__.py>)
- [`src/preprocessing/text.py`](<../src/preprocessing/text.py>)
- [`src/security`](<../src/security>)
- [`src/security/__init__.py`](<../src/security/__init__.py>)
- [`src/security/validation.py`](<../src/security/validation.py>)
- [`src/summarization`](<../src/summarization>)
- [`src/summarization/__init__.py`](<../src/summarization/__init__.py>)
- [`src/summarization/extractive.py`](<../src/summarization/extractive.py>)
- [`tests`](<../tests>)
- [`tests/test_analysis.py`](<../tests/test_analysis.py>)
- [`tests/test_api.py`](<../tests/test_api.py>)
- [`tests/test_charts.py`](<../tests/test_charts.py>)
- [`tests/test_error_paths.py`](<../tests/test_error_paths.py>)
- [`tests/test_external_eval.py`](<../tests/test_external_eval.py>)
- [`tests/test_limits.py`](<../tests/test_limits.py>)
- [`tests/test_model.py`](<../tests/test_model.py>)
