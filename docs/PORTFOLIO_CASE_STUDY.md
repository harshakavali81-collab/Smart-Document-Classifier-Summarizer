# DocSight AI — Case study

**Problem:** Document summaries and category labels are not always traceable to original PDF evidence.

**Implementation:** Built Python/FastAPI document ingestion and page-preserving extraction, a six-class TF-IDF/scikit-learn classifier, extractive summary ranking with page citations, React upload UI, SQLite operational charts, Docker services and GitHub Actions.

**Key design choice:** Summary content is copied from source pages rather than generated. SQLite records timing and category metadata, not original uploads. File size and page limits are enforced.

**Evidence:** inspect source code, run pytest, execute the synthetic holdout evaluation, and review GitHub Actions status. Results on 72 synthetic examples must not be represented as performance on real documents.

**Roles:** entry-level AI/ML Engineer, Python Developer, Backend Engineer. **Tools:** Python, FastAPI, PyMuPDF, scikit-learn, React, SQLite, Docker, CI.

**Limits:** No OCR, authentication, independently verified model quality or public full-stack deployment.
