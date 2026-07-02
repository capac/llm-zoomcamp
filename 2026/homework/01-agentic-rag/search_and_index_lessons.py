from ingest import download_documents, index_documents

documents = download_documents()

index = index_documents(documents)
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
