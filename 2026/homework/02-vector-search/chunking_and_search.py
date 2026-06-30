from gitsource import chunk_documents, GithubRepositoryDataReader
from sentence_transformers import SentenceTransformer
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

model = SentenceTransformer("all-MiniLM-L6-v2")

embed = Embedder()
chunk_dict = {}
for chunk in chunks:
    chunk_dict[chunk["filename"]] = embed.encode(chunk["content"])

X = np.array(list(chunk_dict.values()))
y = np.array(list(chunk_dict.keys()))

q1 = "How does approximate nearest neighbor search work?"
v1 = model.encode(q1)

scores = X.dot(v1)

content_top5 = np.argsort(scores)[::-1][:5]
print(f"Scores of top 5 most similar chunks to q1:\n{scores[content_top5]}")
print(f"Filenames for top 5 most similar chunks to q1:\n{y[content_top5]}")
