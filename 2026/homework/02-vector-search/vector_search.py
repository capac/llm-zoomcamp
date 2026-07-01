from embedder import Embedder
from gitsource import chunk_documents, GithubRepositoryDataReader
from minsearch import VectorSearch
import numpy as np

reader = GithubRepositoryDataReader(
    repo_owner="DataTalksClub",
    repo_name="llm-zoomcamp",
    commit_id="8c1834d",
    allowed_extensions={"md"},
    filename_filter=lambda path: "/lessons/" in path,
)

documents = [file.parse() for file in reader.read()]
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
