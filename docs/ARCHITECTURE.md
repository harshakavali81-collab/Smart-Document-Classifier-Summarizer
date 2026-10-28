# Architecture

![Architecture schematic](../assets/03-system-architecture.svg)

React (Vite) uploads PDF/TXT documents through FastAPI. Validation enforces 6 MiB upload size, max 50 PDF pages and max 150,000 extracted text characters. PyMuPDF preserves original 1-based PDF page positions. The TF-IDF + Logistic Regression model predicts one of six document labels. An independent extractive summarizer ranks verbatim sentences and retains source page numbers.

SQLite stores metadata only: timestamp, predicted class, pages, words and elapsed request milliseconds. No filename, source text, embeddings or upload bytes are written to the database. A React dashboard reads category distributions and daily counts from a separate API endpoint.

~~~mermaid
sequenceDiagram
    participant U as User
    participant F as React
    participant B as FastAPI
    participant P as Parser
    participant M as Classifier
    participant D as SQLite
    U->>F: Upload
    F->>B: POST analyze
    B->>P: Parse indexed pages
    P-->>B: Text and pages
    B->>M: Classify normalized text
    M-->>B: Label and raw score
    B->>B: Select verbatim excerpts and cited pages
    B->>D: Record operational metadata
    B-->>F: Analysis response
~~~

Docker Compose runs a non-root Python backend with a writable SQLite volume and a frontend Nginx reverse proxy. This prototype must not be considered a public production service.
