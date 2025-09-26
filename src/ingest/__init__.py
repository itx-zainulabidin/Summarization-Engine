import os
import docx
from PyPDF2 import PdfReader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def load_text(doc_id: str) -> str:

    file_path = os.path.join(DATA_DIR, doc_id)
    if not os.path.exists(file_path):
        return f"[Error: file not found: {file_path}]"

    ext = os.path.splitext(doc_id)[1].lower()

    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    elif ext == ".pdf":
        return load_pdf(doc_id)

    elif ext == ".docx":
        return load_docx(doc_id)

    elif ext == ".srt":
        return load_srt(doc_id)

    else:
        return f"[Error: unsupported file type: {ext}]"




def split_into_sentences(text: str):

    import re
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    return [s for s in sentences if s]


def load_pdf(doc_id: str) -> str:
    path = os.path.join(DATA_DIR, doc_id)
    text = []
    try:
        reader = PdfReader(path)
        for page in reader.pages:
            text.append(page.extract_text() or "")
    except Exception as e:
        return f"[Error reading PDF: {e}]"
    return "\n".join(text)


def load_docx(doc_id: str) -> str:
    path = os.path.join(DATA_DIR, doc_id)
    try:
        doc = docx.Document(path)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        return f"[Error reading DOCX: {e}]"




def load_srt(doc_id: str) -> str:
    
    path = os.path.join("data", doc_id)
    lines = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(path, "r", encoding="latin-1", errors="ignore") as f:
            lines = f.readlines()

    # remove numbers and timestamps
    cleaned = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.isdigit():
            continue
        if "-->" in line:  # timestamp line
            continue
        cleaned.append(line)
    return " ".join(cleaned)
