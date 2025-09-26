def map_provenance(summary: str, extracted_sentences: list):
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
