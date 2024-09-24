import requests
from elasticsearch import Elasticsearch
import tiktoken
from pprint import pprint

docs_url = 'https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/documents.json?raw=1'
docs_response = requests.get(docs_url)
documents_raw = docs_response.json()

documents = []

for course in documents_raw:
    course_name = course['course']

    for doc in course['documents']:
        doc['course'] = course_name
        documents.append(doc)

es_client = Elasticsearch('http://localhost:9200')

index_settings = {
    'settings': {
        'number_of_shards': 1,
        'number_of_replicas': 0,
    },
    'mappings': {
        'properties': {
            'text': {'type': 'text'},
            'selection': {'type': 'text'},
            'question': {'type': 'text'},
            'course': {'type': 'keyword'},
        },
    },
}

index_name = 'course-questions'
query = 'How do I execute a command in a running docker container?'

# check if the index exists
if not es_client.indices.exists(index=index_name):
    # create the index if it does not exist
    try:
        es_client.indices.create(index=index_name, body=index_settings)
        print(f"Index '{index_name}' created successfully.")
    except ElasticsearchException as e:
        print(f"Error creating index: {e}")

for doc in documents:
    es_client.index(index=index_name, document=doc)

search_query = {
    'size': 5,
    'query': {
        'bool': {
            'must': {
                'multi_match': {
                    'query': query,
                    'fields': ['question^4', 'text'],
                    'type': 'best_fields',
                },
            },
            'filter': {
                'term': {
                    'course': 'machine-learning-zoomcamp',
                },
            },
        },
    },
}

response = es_client.search(index=index_name, body=search_query)

results_docs = []
for hit in response['hits']['hits']:
    results_docs.append(hit['_source'])

context = ""
for doc in results_docs:
    context = context + f"question: {doc['question']}\nanswer: {doc['text']}\n\n"

context_template = """
You're a course teaching assistant
Q: {question}
A: {context}
""".strip()

prompt = context_template.format(question=query, context=context).strip()
print(f'Length of prompt: {len(prompt)}')
encoding = tiktoken.encoding_for_model("gpt-4o")


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

print(f"Number of tokens in prompt: {num_tokens_from_string(prompt, 'cl100k_base')}")
