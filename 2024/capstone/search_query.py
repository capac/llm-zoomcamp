from elasticsearch import Elasticsearch

# Initialize Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Index name where documents are stored
index_name = "solar_eclipse_chunks"


# Query function to search for relevant answers
def query_solar_eclipse(query):
    # Construct the search query
    search_query = {
        "size": 5,  # Return the top 5 matches
        "query": {
            "bool": {
                "should": [
                    {
                        "multi_match": {
                            "query": query,
                            # Prioritize text (boosted by ^3) over tables
                            "fields": ["text^3", "table^1"],
                            "type": "best_fields"
                        }
                    }
                ],
                "minimum_should_match": 1  # At least one match required
            }
        }
    }

    # Perform the search
    response = es.search(index=index_name, body=search_query)

    # Process the results
    results = []
    for hit in response['hits']['hits']:
        source = hit['_source']
        chunk_text = source.get("text", "")
        table_data = source.get("table", [])

        # Privilege text results, only include table if no sufficient text
        if chunk_text:
            results.append({
                "doc_id": source['doc_id'],
                "chunk_id": source['chunk_id'],
                "text": chunk_text,
                "table": None  # No table, prioritize text
            })
        elif table_data:
            results.append({
                "doc_id": source['doc_id'],
                "chunk_id": source['chunk_id'],
                "text": None,  # No text
                "table": table_data
            })

    return results


# Example: Query the index
def main():
    # Example question
    user_query = "When will the next total solar eclipse occur in Europe?"

    # Query Elasticsearch for the answer
    search_results = query_solar_eclipse(user_query)

    # Print results
    for result in search_results:
        if result['text']:
            print(f"Document ID: {result['doc_id']}")
            print(f"Chunk ID: {result['chunk_id']}")
            print(f"Text: {result['text']}")
        elif result['table']:
            print(f"Document ID: {result['doc_id']}")
            print(f"Chunk ID: {result['chunk_id']}")
            print("Table Data:")
            for row in result['table']:
                print(row)


if __name__ == "__main__":
    main()
