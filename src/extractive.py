import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def textrank_sentences(sentences, top_k=12):
    if not sentences:
        return []

    texts = [s if isinstance(s, str) else str(s) for s in sentences]
    ranked = run_textrank(texts, top_k)

    return [{"id": i, "text": s} for i, s in enumerate(ranked)]


def run_textrank(sentences, top_k=12):
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
