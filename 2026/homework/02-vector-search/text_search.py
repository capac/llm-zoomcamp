from ingest import download_documents
from gitsource import chunk_documents
from minsearch import Index
from typing import List


def t_search(documents: List, question: str) -> List[str]:
    chunks = chunk_documents(documents, size=2000, step=1000)

    text_index = Index(text_fields=["content"])
    text_index.fit(chunks)

    print("Indexing completed\n")

    results = text_index.search(question, num_results=5)
    for result in results:
        print(f"Filename: {result['filename']}")
    print("Done with text results\n")
    return results


if __name__ == "__main__":
    documents = download_documents()
    q1 = "How do I store vectors in PostgreSQL?"
    t_search(documents, q1)
