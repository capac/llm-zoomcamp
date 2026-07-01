from gitsource import chunk_documents, GithubRepositoryDataReader
from minsearch import Index

reader = GithubRepositoryDataReader(
    repo_owner="DataTalksClub",
    repo_name="llm-zoomcamp",
    commit_id="8c1834d",
    allowed_extensions={"md"},
    filename_filter=lambda path: "/lessons/" in path,
)

documents = [file.parse() for file in reader.read()]
chunks = chunk_documents(documents, size=2000, step=1000)

text_index = Index(text_fields=["content"])
text_index.fit(chunks)

print("Indexing completed.")

q1 = "How do I store vectors in PostgreSQL?"
search_results = text_index.search(q1, num_results=5)
for result in search_results:
    print(f"Filename: {result['filename']}")
