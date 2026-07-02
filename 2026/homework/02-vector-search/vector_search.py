from ingest import download_documents
from embedder import Embedder
from gitsource import chunk_documents
from minsearch import VectorSearch
import numpy as np

documents = download_documents()
chunks = chunk_documents(documents, size=2000, step=1000)

model = Embedder()
chunks_embeddings = []
for chunk in chunks:
    embedding = model.encode(chunk["content"])
    chunks_embeddings.append(embedding)

X = np.array(chunks_embeddings)

vector_index = VectorSearch(keyword_fields=["content"])
vector_index.fit(X, chunks)

# q1 = "What metric do we use to evaluate a search engine?"
q1 = "How do I store vectors in PostgreSQL?"
v1 = model.encode(q1)

results = vector_index.search(v1, num_results=5)
for result in results:
    print(f"Filename: {result['filename']}")
