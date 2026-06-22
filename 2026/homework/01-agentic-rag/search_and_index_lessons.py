from gitsource import GithubRepositoryDataReader
from minsearch import Index

reader = GithubRepositoryDataReader(
    repo_owner="DataTalksClub",
    repo_name="llm-zoomcamp",
    commit_id="8c1834d",
    allowed_extensions={"md"},
    filename_filter=lambda path: "/lessons/" in path,
)

print("Downloading lessons...")
files = reader.read()

documents = []

for file in files:
    doc = file.parse()
    documents.append(doc)

print(f"Number of documents downloaded: {len(documents)}")

index = Index(
    text_fields=["content"],
    keyword_fields=["filename"]
)

index.fit(documents)
print("Indexing completed.")

question = "How does the agentic loop keep calling the model until it stops?"

search_results = index.search(
    question,
    boost_dict={"question": 2.0, "section": 0.5},
    # filter_dict={"course": "llm-zoomcamp"},
    num_results=5
)

print(f"Search results for first filename: {search_results[0]['filename']}")
