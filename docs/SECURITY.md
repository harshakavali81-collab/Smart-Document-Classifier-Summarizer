# Privacy and security

**Present:** upload type checks and PDF header validation, 6 MiB maximum, 50-page maximum, 150,000 extracted characters, no external AI requests, metadata-only SQLite storage, CORS allowlist, non-root Python Docker backend. The app does not intentionally persist document content.

**Not present:** authentication/authorization, per-tenant isolation, rate limits, malware scanning, PDF parser isolation, data encryption, retention automation, formal security review, production monitoring or public hosting. The SQLite volume retains operational metadata. Small traffic cohorts may be inferred from public category counts.

**Requirements before production:** HTTPS, identity/permissions, per-user quotas, scanned-PDF sandboxing/malware scanning, PDF fuzz testing, encryption, retention/deletion policy, privacy notices, backups, secrets management, safe dependency pinning and independent model validation. Do not process private or sensitive real documents on an untrusted deployed copy.
