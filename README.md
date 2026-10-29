# DocSight AI — Smart Document Classifier & Summarizer

A full-stack, local-first document intelligence portfolio application: upload a PDF or text file, predict its category, see extractive highlights with source page numbers, and explore request analytics.

[Setup](#local-installation--setup-guide) · [Architecture](#architecture--system-design-diagram) · [Detailed guide](PROJECT_GUIDE.md) · [Repository standard](docs/REPOSITORY_STANDARD.md)

## Visuals

![Dashboard concept](<assets/01-product-preview.svg>)

Existing project visual; diagrams and illustrative graphics are not evidence of a deployed application.

## Live Link / Demo

Existing published preview link: [Open browser preview](https://harshakavali81-collab.github.io/harshavardhan-portfolio/docsight-demo.html). This update does not independently verify its availability or backend deployment.

## Key Features

| Module | Implementation |
|---|---|
| Ingestion | PyMuPDF PDF parser (selectable text), UTF-8 TXT, original page indexing |
| ML | TF-IDF word ngrams + Logistic Regression; six classes and uncertain fallback |
| Summarization | Sentence ranking with citations to source pages |
| API | FastAPI with input checks, Pydantic schema and OpenAPI docs |
| Web | React/Vite upload interface, sample mode, evidence display, JSON export |
| Analytics | SQLite stores request timing, counts and categories — never uploaded content |
| Engineering | Tests, synthetic evaluation, GitHub Actions, Docker Compose |

## Tech Stack

![Python](https://img.shields.io/badge/Python-334155?style=flat-square) ![FastAPI](https://img.shields.io/badge/FastAPI-334155?style=flat-square) ![scikit-learn](https://img.shields.io/badge/scikit--learn-334155?style=flat-square) ![React](https://img.shields.io/badge/React-334155?style=flat-square) ![Docker](https://img.shields.io/badge/Docker-334155?style=flat-square)

Dependency versions and optional packages are defined in the repository manifests.

## Architecture / System Design Diagram

[Architecture documentation / diagram](<docs/ARCHITECTURE.md>)

## Local Installation & Setup Guide

```bash
git clone https://github.com/harshakavali81-collab/Smart-Document-Classifier-Summarizer.git
cd Smart-Document-Classifier-Summarizer
```

**Docker (requires Docker Compose):**

~~~bash
docker compose up --build
~~~

Open http://localhost:8080

**Local development (Python 3.11+ and Node.js 20+):**

~~~bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn backend.app.main:app --reload --port 8000
~~~

In a second terminal:

~~~bash
cd frontend
npm install
npm run dev
~~~

Open http://localhost:5173 . API docs: http://localhost:8000/docs

**Test the sample:**

~~~bash
curl -X POST http://localhost:8000/api/v1/analyze -F "file=@data/samples/example_report.txt"
pytest -q
python -m scripts.evaluate
python -m scripts.make_eval_charts
~~~

The evaluation outputs a synthetic held-out classification report and confusion matrix at reports/model_evaluation.json. The chart generator creates reports/confusion_matrix.svg and reports/per_class_f1.svg from those **actual synthetic test results**. All three are ignored by Git and included in the downloadable CI evaluation artifact; none constitute an independent real-world benchmark. Do not confuse synthetic test performance with real-world accuracy.

## Challenges & Solutions

**Repository organization:** this project uses `src/`, `backend/`, `frontend/`. Keeping those paths stable avoids breaking imports, asset links and deployment commands while the documentation follows a shared format. Project-specific technical limitations and prior release evidence are retained in [Project guide](PROJECT_GUIDE.md).

## Future Improvements

- Capture a reproducible end-to-end demo with runtime versions and sample inputs.
- Expand regression checks for invalid inputs and documented edge cases.
- Record measured results, data provenance and deployment limitations alongside each release.

## Scope and supporting evidence

A full-stack, local-first document intelligence portfolio application: upload a PDF or text file, predict its category, see extractive highlights with source page numbers, and explore request analytics.

**Transparency:** The classifier is trained on 72 authored synthetic samples across 6 categories, not validated real-world documents. Probabilities are not calibrated. The extractive summarizer returns sentences from the input, not LLM-generated prose. Illustrations are original schematics, not screenshots from a deployed production service.

## Repository Structure

| Location | Purpose |
| --- | --- |
| `src/` | Source modules |
| `backend/` | Backend services |
| `frontend/` | Frontend interface |
| `tests/` | Tests |
| `docs/` | Documentation |
| `data/` | Data and samples |
| `assets/` | Visual assets |
| `scripts/` | Automation scripts |
| `.github/` | Issue forms, PR template and automated checks |

[Complete file inventory and workflow](docs/REPOSITORY_STANDARD.md). Runtime entry points retain their existing paths.

## Workflow & Tracking

Use the [bug and feature forms](https://github.com/harshakavali81-collab/Smart-Document-Classifier-Summarizer/issues/new/choose) to define work with acceptance criteria. Keep tasks in Todo → In progress → Review → Done, and link a pull request with `Closes #<number>`. See [the maintenance workflow](docs/REPOSITORY_STANDARD.md#workflow).

## License

See [LICENSE](LICENSE) for the existing terms.
