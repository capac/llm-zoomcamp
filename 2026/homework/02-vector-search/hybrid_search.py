from vector_search import v_search
from text_search import t_search
from ingest import download_documents
from typing import List


def rrf(result_lists: List[List], k=60, num_results=5) -> List:
    scores = {}
    docs = {}

    for results in result_lists:
        for rank, doc in enumerate(results):
            key = (doc["filename"], doc["start"])
            scores[key] = scores.get(key, 0) + 1 / (k + rank)
            docs[key] = doc

    ranked = sorted(scores, key=scores.get, reverse=True)
    return [docs[key] for key in ranked[:num_results]]


if __name__ == "__main__":
    documents = download_documents()
    q1 = "How do I give the model access to tools?"
    text_results = t_search(documents, q1)
    vector_results = v_search(documents, q1)
    hybrid_results = rrf([vector_results, text_results])
    for result in hybrid_results:
        print(f"{result['filename']}")
