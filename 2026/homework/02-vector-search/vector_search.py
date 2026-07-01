from embedder import Embedder
from gitsource import GithubRepositoryDataReader
from minsearch import VectorSearch
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

reader = GithubRepositoryDataReader(
    repo_owner="DataTalksClub",
    repo_name="llm-zoomcamp",
    commit_id="8c1834d",
    allowed_extensions={"md"},
    filename_filter=lambda path: "/lessons/" in path,
)

documents = [file.parse() for file in reader.read()]

embed = Embedder()
docs_dict = {}
for document in documents:
    docs_dict[document["filename"]] = embed.encode(document["content"])

X = np.array(list(docs_dict.values()))
y = np.array(list(docs_dict.keys()))

vector_index = VectorSearch(keyword_fields=["content"])
vector_index.fit(X, documents)

# q1 = "What metric do we use to evaluate a search engine?"
q1 = "How do I store vectors in PostgreSQL?"
v1 = model.encode(q1)

results = vector_index.search(v1, num_results=5)
for result in results:
    print(f"Filename: {result['filename']}")
