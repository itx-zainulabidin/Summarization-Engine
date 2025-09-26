from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# from src import inference, extractive, provenance, ingest, exporter
# # Local module imports
from src import inference
from src import extractive
from src import provenance
from src import ingest
from src import exporters

app = FastAPI(title="Summarizer Prototype API")


class SummRequest(BaseModel):
     """
    Request body for summarization API.
    - doc_id: filename inside /data folder (txt, pdf, docx, srt)
    - mode: summary length/type (tldr | short | extended)
    - export: optional export format (pdf | docx | txt)
    """
    doc_id: str
    mode: str  # tldr | short | extended
    export: Optional[str] = None  # pdf | docx | txt



# summarize endpoint
@app.post("/api/summarize")
def summarize(req: SummRequest):
    """
    Main summarization pipeline:
    1. Load document text from /data folder
    2. Perform extractive summarization (TextRank)
    3. Run abstractive summarization on extracted text
    4. Map provenance between summary and source sentences
    5. Optionally export summary to PDF/DOCX/TXT
    """
    # Load text by doc_id
    text = ingest.load_text(req.doc_id)
    if text is None:
        raise HTTPException(status_code=404, detail="doc_id not found in data folder")

    # Extractive step
    sentences = ingest.split_into_sentences(text)
    extracted = extractive.textrank_sentences(sentences, top_k=12)

    # Abstractive step
    extracted_texts = [s["text"] for s in extracted]
    summary = inference.summarize_document(" ".join(extracted_texts), mode=req.mode)

    # Provenance mapping
    sources = provenance.map_provenance(summary, extracted)

    response = {
        "doc_id": req.doc_id,
        "mode": req.mode,
        "summary": summary,
        "sources": sources,
    }

    # Handle export if requested
    if req.export:
        try:
            file_path = exporters.export_summary(summary, req.doc_id, req.mode, req.export)
            response["export_path"] = file_path
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    return response
