from gitsource import chunk_documents
from ingest import download_documents
from embedder import Embedder
import numpy as np


documents = download_documents()
chunks = chunk_documents(documents, size=2000, step=1000)

texts = [chunk["content"] for chunk in chunks]
model = Embedder()
X = model.encode_batch(texts)

q1 = "How does approximate nearest neighbor search work?"
v1 = model.encode(q1)

scores = X.dot(v1)

top5_idx = np.argsort(-scores)[:5]
print("Scores of top 5 most similar chunks to q1:")
for idx in top5_idx:
    print(f"{np.round(scores[idx], 5)}")
print(end="\n")
print("Filenames for top 5 most similar chunks to q1:")
for idx in top5_idx:
    print(f"{chunks[idx]['filename']}")
