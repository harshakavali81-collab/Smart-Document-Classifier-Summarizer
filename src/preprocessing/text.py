"""Conservative normalization that preserves sentence evidence."""
import re

def normalize(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[\t ]+", " ", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()

def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))
