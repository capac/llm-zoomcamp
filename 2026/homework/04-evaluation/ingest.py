from gitsource import GithubRepositoryDataReader


def download_documents(
        repo_owner="DataTalksClub",
        repo_name="llm-zoomcamp",
        commit_id="8c1834d",
        allowed_extensions={"md"}
        ):

    reader = GithubRepositoryDataReader(
        repo_owner=repo_owner,
        repo_name=repo_name,
        commit_id=commit_id,
        allowed_extensions=allowed_extensions,
        filename_filter=lambda path: "/lessons/" in path,
    )

    print("Downloading lessons...")
    files = reader.read()

    documents = []

    for file in files:
        doc = file.parse()
        documents.append(doc)

    return documents
