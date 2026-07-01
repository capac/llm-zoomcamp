from gitsource import chunk_documents, GithubRepositoryDataReader
from embedder import Embedder
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

chunk_dict = {}
for chunk in chunks:
    chunk_dict[chunk["filename"]] = model.encode(chunk["content"])

X = np.array(list(chunk_dict.values()))
y = np.array(list(chunk_dict.keys()))

q1 = "How does approximate nearest neighbor search work?"
v1 = model.encode(q1)

scores = X.dot(v1)

top5_indexes = np.argsort(-scores)[:5]
print(f"Scores of top 5 most similar chunks to q1:\n{scores[top5_indexes]}")
print(f"Filenames for top 5 most similar chunks to q1:\n{y[top5_indexes]}")
