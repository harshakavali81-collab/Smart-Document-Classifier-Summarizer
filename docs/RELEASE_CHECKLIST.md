# DocSight AI engineering release checklist

## Automated verification
- [ ] GitHub main CI passes Python unit/integration tests, React build and Docker Compose end-to-end smoke checks.
- [ ] Synthetic evaluation metrics and both reproducible SVG charts are included in the build artifact.
- [ ] Python XML coverage report is generated and confirms the enforced 95% minimum for backend/ and src/ (the recorded 2026-10-28 run measured 100% across 215 statements).
- [ ] Dependency updates are reviewed with tests, not blindly merged.

## Functional verification
- [ ] Multi-page selectable-text PDF summary excerpts match the original cited pages.
- [ ] TXT classification, summary display, error responses, and JSON export work end to end.
- [ ] Reject unsupported, corrupt, encrypted, oversized and image-only documents.
- [ ] Confirm no uploaded text, file bytes or filenames are stored in SQLite metadata.
- [ ] Check keyboard navigation, desktop and mobile layout, and source-page browser links.

## Independent real-world validation: not completed
- [ ] Obtain legally licensed, consented, independently labeled documents.
- [ ] Evaluate per-class precision, recall, macro F1, calibration and robustness on non-templated data.
- [ ] Evaluate table extraction, non-English content, ambiguous and mixed-class documents.
- [ ] Conduct human citation-fidelity review for sentence and page references.

## Production security and hosting: not completed
- [ ] Deploy HTTPS with robust authentication, authorization and tenant isolation.
- [ ] Add malware scanning, isolated PDF parsing, per-user rate limits and quotas.
- [ ] Encrypt persistent data; define retention, deletion, backups and audit logging.
- [ ] Conduct independent security review, load testing, monitoring and rollback exercise.

**Status:** a tested portfolio prototype, not a validated legal, clinical, or production document-processing service.
