from ingest import download_documents
from gitsource import chunk_documents
from minsearch import Index

documents = download_documents()
chunks = chunk_documents(documents, size=2000, step=1000)

text_index = Index(text_fields=["content"])
text_index.fit(chunks)

print("Indexing completed.")

q1 = "How do I store vectors in PostgreSQL?"
search_results = text_index.search(q1, num_results=5)
for result in search_results:
    print(f"Filename: {result['filename']}")
