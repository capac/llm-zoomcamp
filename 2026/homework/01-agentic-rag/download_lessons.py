from gitsource import GithubRepositoryDataReader

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
