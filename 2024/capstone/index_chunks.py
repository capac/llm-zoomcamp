from elasticsearch import Elasticsearch, helpers
from pathlib import Path
import json

# Initialize Elasticsearch client
es = Elasticsearch("http://localhost:9200")

# Index name where documents will be stored
index_name = "solar_eclipse_chunks"
directory_path = Path('wikipedia_pages')


# Create the index in Elasticsearch (optional,
# you can adjust mappings as needed)
def create_index():
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
        print(f"Index '{index_name}' created.")
    else:
        print(f"Index '{index_name}' already exists.")


def store_table_as_string(table):
    return json.dumps(table)


# Function to bulk index chunks to Elasticsearch
def index_chunks(chunks, file):
    actions = []

    for chunk in chunks:
        # Prepare action for bulk indexing
        action = {
            "_index": index_name,
            "_id": chunk['chunk_id'],
            "_source": {
                "doc_id": chunk['doc_id'],
                "chunk_id": chunk['chunk_id'],
                "text": chunk.get('text', ""),
                "table": store_table_as_string(chunk.get('table', None))
            }
        }
        actions.append(action)

    try:
        # Bulk index the data to Elasticsearch
        helpers.bulk(es, actions)
        print(f"Indexed {len(actions)} chunks to "
              f"Elasticsearch from {file.name}.")
    except helpers.BulkIndexError as e:
        # Log errors and failed documents
        print(f"Bulk indexing failed for {file.name}: {e}")
        for err in e.errors:
            print("Error document:", err, '\n')


# Load the chunked data from the JSON file
def load_chunks_from_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return json.load(f)


# Create Elasticsearch index if it doesn't exist
create_index()


# Main script
def main():
    # Load chunks from JSON file
    for json_file in directory_path.glob('*.json'):
        chunks = load_chunks_from_json(json_file)

        # Index chunks to Elasticsearch
        index_chunks(chunks, json_file)


if __name__ == "__main__":
    main()
