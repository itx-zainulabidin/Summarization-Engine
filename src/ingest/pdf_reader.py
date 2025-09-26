import os
import re

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")

def load_text(doc_id):
    # Simple loader: expects data/{doc_id}.txt
    path = os.path.join(DATA_DIR, f"{doc_id}.txt")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def split_into_sentences(text):
    # Very simple sentence splitter that keeps metadata for provenance
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    sentences = []
    sid = 0
    for li, line in enumerate(lines):
        parts = re.split(r'(?<=[.!?])\s+', line)
        for p in parts:
            sid += 1
            sentences.append({"id": f"s{sid}", "text": p, "meta": {"line": li+1}})
    return sentences
