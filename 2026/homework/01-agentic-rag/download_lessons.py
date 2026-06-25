from ingest import download_documents

documents = download_documents()
print(f"Number of documents downloaded: {len(documents)}")
