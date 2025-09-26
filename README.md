# Summarization (Local, runnable scaffold)
This repository is a **local prototype scaffold** for the multi-stage summarization engine you requested.
It contains:
- extractive stage (TextRank mock)
- abstractive stage (calls to Hugging Face Transformers are optional; stubbed if not available)
- provenance mapping (basic alignment)
- FastAPI server endpoint `/api/summarize`
- exporters (TXT/DOCX/PDF stub)
- training script template for fine-tuning
- sample input text and example curl call

IMPORTANT:
- This scaffold is intended to run **locally on your machine**.
- To use a real summarization model you must install dependencies and download/point to a local HF model (see below).
- If you don't have GPUs, use small models (e.g., `sshleifer/distilbart-cnn-12-6`) or use 8-bit / quantized weights.

Quick start (development / test):
1. Create a Python venv and activate it:
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate    # Windows (PowerShell)

2. Install requirements:
   pip install -r requirements.txt

3. Run the FastAPI app:
   uvicorn src.api.main:app --reload --port 8000

4. Test (example):
   curl -X POST "http://127.0.0.1:8000/api/summarize" -H "Content-Type: application/json" -d \
   '{"doc_id":"sample_text","mode":"tldr"}'

Files of interest:
- src/extractive.py      : TextRank-like extractive selection
- src/inference.py       : Abstractive wrapper (uses HF if available, otherwise returns extractive join)
- src/provenance.py      : Maps output back to source sentences
- src/api/main.py        : FastAPI app and endpoint
- src/abstractive_train.py : Training script template (HF Trainer)
- data/sample_text.txt   : Example text to summarize
