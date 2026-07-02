from ingest import download_documents
from embedder import Embedder
from gitsource import chunk_documents
from minsearch import VectorSearch
from typing import List
import numpy as np


def v_search(documents: List, question: str) -> List[str]:
    chunks = chunk_documents(documents, size=2000, step=1000)

    model = Embedder()
    chunks_embeddings = []
    for chunk in chunks:
        embedding = model.encode(chunk["content"])
        chunks_embeddings.append(embedding)

    X = np.array(chunks_embeddings)

    vector_index = VectorSearch(keyword_fields=["content"])
    vector_index.fit(X, chunks)

    v1 = model.encode(question)

    results = vector_index.search(v1, num_results=5)
    for result in results:
        print(f"Filename: {result['filename']}")
    print("Done with vector results\n")
    return results


if __name__ == "__main__":
    documents = download_documents()
    # q1 = "What metric do we use to evaluate a search engine?"
    q1 = "How do I store vectors in PostgreSQL?"
    v_search(documents, q1)
