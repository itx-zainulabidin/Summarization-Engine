import os
import torch
from transformers import pipeline

MODEL_NAME = os.environ.get("SUMMARIZER_MODEL", "facebook/bart-large-cnn")

#loading HuggingFace summarizer
try:
    summarizer = pipeline(
        "summarization",
        model=MODEL_NAME,
        tokenizer=MODEL_NAME,
        device=0 if torch.cuda.is_available() else -1
    )
except Exception as e:
    print(f"[Warning] Failed to load summarizer model: {e}")
    summarizer = None




def summarize_document(text: str, mode: str = "short") -> str:
    """
    Summarize a document using an abstractive model (BART or other Seq2Seq).

    Args:
        text (str): Input document text to summarize.
        mode (str): Summary length style:
            - "tldr": very short (~1–2 sentences)
            - "short": medium length summary
            - "extended": longer summary

    Returns:
        str: Generated summary text (joined across chunks if needed).
    """
    
    # Limit based on mode
    if mode == "tldr":
        max_len = 60
        min_len = 20
    elif mode == "short":
        max_len = 120
        min_len = 40
    else:  # extended
        max_len = 300
        min_len = 100

    # BART has max input length of 1024 tokens → enforce safe chunking
    max_input_length = 1024
    chunks = [text[i:i + 2000] for i in range(0, len(text), 2000)]  # ~2000 chars per chunk

    summaries = []
    for chunk in chunks:
        try:
            result = summarizer(
                chunk,
                max_length=max_len,
                min_length=min_len,
                truncation=True  # avoid index errors
            )
            summaries.append(result[0]['summary_text'])
        except Exception as e:
            summaries.append(f"[Error on chunk: {e}]")

    # Join chunk summaries
    return " ".join(summaries)
