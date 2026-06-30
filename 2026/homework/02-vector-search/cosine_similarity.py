from sentence_transformers import SentenceTransformer
from gitsource import GithubRepositoryDataReader
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")
q1 = "How does approximate nearest neighbor search work?"

v1 = model.encode(q1)

reader = GithubRepositoryDataReader(
    repo_owner="DataTalksClub",
    repo_name="llm-zoomcamp",
    commit_id="8c1834d",
    allowed_extensions={"md"},
    filename_filter=lambda path: "/lessons/" in path,
)

documents = [file.parse() for file in reader.read()]

for index, document in enumerate(documents):
    if document["filename"] == (
        "02-vector-search/lessons/07-sqlitesearch-vector.md"
    ):
        print(
            f"Index: {index}, Filename: {document['filename']},"
            f"Content: {document['content']}"
        )

q2 = documents[22]["content"]
v2 = model.encode(q2)

norm = (np.linalg.norm(v1) * np.linalg.norm(v2))
print(f"Cosine similarity: {v1.dot(v2) / norm}")
