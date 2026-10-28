"""Faithful extractive summary: every output sentence appears in its cited source page."""
from collections import Counter
import re

STOP = set("the and for from that this with into have will were they their about your which when where a an are you its such can not was be of on by in to as is at it or".split())

def _sentences(text: str):
    # Paragraph boundaries and punctuation. Preserve original sentence text.
    for section in re.split(r"(?<=[.!?])\s+|\n+", text):
        sent = section.strip()
        if 25 <= len(sent) <= 750 and len(sent.split()) >= 5:
            yield sent

def summarize(pages: list[dict], limit: int = 4) -> list[dict]:
    candidates = [(p["page"], sent) for p in pages for sent in _sentences(p["text"])]
    if not candidates:
        return []
    tokens = [re.findall(r"[a-zA-Z]{3,}", sentence.lower()) for _, sentence in candidates]
    frequency = Counter(t for row in tokens for t in row if t not in STOP)
    scores = []
    for i, row in enumerate(tokens):
        relevant = [t for t in row if t not in STOP]
        score = sum(frequency[t] for t in set(relevant)) / max(len(relevant), 1)
        scores.append((score, -i, i))
    chosen = sorted([i for _, _, i in sorted(scores, reverse=True)[:limit]])
    return [{"text": candidates[i][1], "page": candidates[i][0]} for i in chosen]
