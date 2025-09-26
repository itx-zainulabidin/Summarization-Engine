def map_provenance(summary: str, extracted_sentences: list):
    """
    Map each summary sentence back to its most similar source sentence
    from the extracted sentences, using simple word-overlap scoring.

    Args:
        summary (str): The generated summary text.
        extracted_sentences (list): List of extracted sentences, 
            each a dict with:
                - "id": unique sentence index
                - "text": sentence text
                - "meta": optional metadata

    Returns:
        list[dict]: Provenance mapping for each summary sentence with:
            - "sentence_id": ID of the most similar extracted sentence
            - "meta": metadata of the source sentence
            - "score": word-overlap score
    """
    summary_sents = [s.strip() for s in summary.split(". ") if s.strip()]
    sources = []

    for ss in summary_sents:
        best = None
        best_score = -1
        for s in extracted_sentences:
            a = ss.lower().split()
            b = s["text"].lower().split()
            score = len(set(a) & set(b))  # simple word overlap
            if score > best_score:
                best_score = score
                best = s
        if best:
            sources.append({
                "sentence_id": best["id"],
                "meta": best.get("meta", {}),
                "score": best_score
            })

    return sources
