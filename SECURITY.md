# Security policy

This is a **portfolio demonstration**, not a hosted secure document-processing service. Do not upload sensitive documents to an untrusted instance.

Report vulnerabilities privately to the repository maintainer using GitHub private vulnerability reporting when enabled, or an established private channel. Avoid posting exploit details or private records in public issues.

Supported: latest main branch. Public API has no authentication or per-user data isolation. Before deploying to external users, implement identity, authorization, rate limiting, independent malware/parser sandboxing, HTTPS, retention/deletion policy, threat review, monitoring, and model governance. See [detailed controls](docs/SECURITY.md).
