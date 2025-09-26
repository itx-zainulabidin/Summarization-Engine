import os
import docx
from PyPDF2 import PdfReader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def load_text(doc_id: str) -> str:
    """
    Load text from a file given its doc_id (filename).
    Supports TXT, PDF, DOCX, and SRT formats.

    Args:
        doc_id (str): The filename (with extension) of the document.

    Returns:
        str: Extracted text or an error message if unsupported format or file not found.
    """
    
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
    """
    Split text into sentences using regex rules.
    Handles '.', '!', and '?' as sentence boundaries.

    Args:
        text (str): Input text.

    Returns:
        list[str]: List of sentences.
    """

    import re
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    return [s for s in sentences if s]


def load_pdf(doc_id: str) -> str:
    
    """
    Extract text from a PDF file.

    Args:
        doc_id (str): PDF filename.

    Returns:
        str: Extracted text or error message.
    """
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
    """
    Extract text from a DOCX file.

    Args:
        doc_id (str): DOCX filename.

    Returns:
        str: Extracted text or error message.
    """
    path = os.path.join(DATA_DIR, doc_id)
    try:
        doc = docx.Document(path)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        return f"[Error reading DOCX: {e}]"




def load_srt(doc_id: str) -> str:
    """
    Extract and clean text from an SRT subtitle file.
    Removes sequence numbers and timestamps, keeping only subtitle lines.

    Args:
        doc_id (str): SRT filename.

    Returns:
        str: Cleaned subtitle text.
    """
    
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
