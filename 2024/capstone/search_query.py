from elasticsearch import Elasticsearch
import spacy

# Initialize Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Index name where documents are stored
index_name = "solar_eclipse_chunks"


# Function to extract location and date from the query
def extract_entities(query):
    doc = nlp(query)

    location = None
    date = None

    for ent in doc.ents:
        # "GPE" is the entity label for locations like cities and countries
        if ent.label_ == "GPE":
            location = ent.text
        if ent.label_ == "DATE":
            date = ent.text

    return location, date


# Function to build the Elasticsearch query dynamically
def build_query(query, location, date):
    must_clauses = [
        {
            "multi_match": {
                "query": query,
                "fields": ["text", "table"],
                "type": "best_fields"
            }
        }
    ]

    # If a location was detected, add it as a filter
    if location:
        must_clauses.append({
            "match": {
                "text": location
            }
        })

    # If a date was detected, try to add it as a filter
    if date:
        must_clauses.append({
            "match": {
                "text": date
            }
        })

    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": must_clauses
            }
        }
    }

    return search_query


# Function to search in Elasticsearch with dynamic filtering
def query_solar_eclipse(query):
    # Extract location and date from the user query
    location, date = extract_entities(query)

    # Build the Elasticsearch query dynamically based on the extracted entities
    es_query = build_query(query, location, date)

    # Perform the search in Elasticsearch
    response = es.search(index=index_name, body=es_query)

    # Process and return the results
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
                "table": None
            })
        elif table_data:
            results.append({
                "doc_id": source['doc_id'],
                "chunk_id": source['chunk_id'],
                "text": None,
                "table": table_data
            })

    return results


# Example: Query the index
def main():
    # Example question
    user_query = ("When will the next solar eclipse "
                  "occur in the United States?")

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
