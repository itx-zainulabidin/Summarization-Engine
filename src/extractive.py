import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def textrank_sentences(sentences, top_k=12):
    """
    Run TextRank on a list of sentences and return the top-ranked ones.

    Args:
        sentences (list[str]): List of input sentences.
        top_k (int): Number of sentences to keep (default: 12).

    Returns:
        list[dict]: List of top-ranked sentences in the form:
            [{"id": int, "text": str}, ...]
    """
    if not sentences:
        return []

    texts = [s if isinstance(s, str) else str(s) for s in sentences]
    ranked = run_textrank(texts, top_k)

    return [{"id": i, "text": s} for i, s in enumerate(ranked)]


def run_textrank(sentences, top_k=12):
    """
    Core TextRank algorithm implementation for sentence ranking.

    Steps:
    1. Convert sentences into TF-IDF vectors.
    2. Compute cosine similarity matrix between all pairs of sentences.
    3. Build a similarity graph where:
        - Nodes = sentences
        - Edges = similarity scores
    4. Apply PageRank algorithm to compute sentence importance.
    5. Return the top-k ranked sentences.

    Args:
        sentences (list[str]): List of sentences.
        top_k (int): Number of sentences to return.

    Returns:
        list[str]: Top-ranked sentences.
    """
    
    if not sentences:
        return []

    # Convert sentences to TF-IDF vectors
    vectorizer = TfidfVectorizer().fit_transform(sentences)
    sim_matrix = cosine_similarity(vectorizer)

    # Build similarity graph
    nx_graph = nx.from_numpy_array(sim_matrix)
    scores = nx.pagerank(nx_graph)

    # Rank sentences by PageRank score
    ranked = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    return [s for _, s in ranked[:top_k]]
