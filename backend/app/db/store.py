"""Minimal aggregate analytics; never stores filenames, text, embeddings or file bytes."""
import os
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

def _dbpath():
    return Path(os.getenv("ANALYTICS_DB", "runtime/usage.db"))

def connect():
    path = _dbpath()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), timeout=10)
    conn.execute("""CREATE TABLE IF NOT EXISTS analyses (
       id INTEGER PRIMARY KEY, at TEXT NOT NULL, category TEXT NOT NULL,
       page_count INTEGER NOT NULL, word_count INTEGER NOT NULL, latency_ms REAL NOT NULL
    )""")
    return conn

def record(result: dict):
    with connect() as conn:
        conn.execute("INSERT INTO analyses(at,category,page_count,word_count,latency_ms) VALUES(?,?,?,?,?)",
                     (datetime.now(timezone.utc).isoformat(), result["category"],result["page_count"],
                      result["word_count"],result["latency_ms"]))

def dashboard():
    with connect() as conn:
        total, avg_latency, pages = conn.execute("SELECT COUNT(*),COALESCE(AVG(latency_ms),0),COALESCE(SUM(page_count),0) FROM analyses").fetchone()
        categories = [{"label": name, "count": count} for name,count in
                      conn.execute("SELECT category,COUNT(*) FROM analyses GROUP BY category ORDER BY COUNT(*) DESC")]
        days = [{"day": day, "count": count} for day,count in
                conn.execute("SELECT substr(at,1,10),COUNT(*) FROM analyses GROUP BY substr(at,1,10) ORDER BY 1 DESC LIMIT 14")]
    return {"total_analyses": total, "average_latency_ms": round(avg_latency,2),
            "pages_processed": pages, "categories": categories, "days": list(reversed(days)),
            "data_note": "Only operational metadata is stored; aggregate counts are not anonymized for very low traffic."}
