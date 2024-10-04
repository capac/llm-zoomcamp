from elasticsearch import Elasticsearch
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Initialize Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Index name where documents are stored
index_name = "solar_eclipse_chunks"


# Query function to search for relevant answers
def query_database(query):
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
                            "fields": ["text^2", "table^1"],
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


def build_prompt(query, search_results):
    prompt_template = """
You're an astronomor enthusiast. Answer the QUESTION based on the CONTEXT from
the database. Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT: {context}
""".strip()

    context = ""

    for doc in search_results:
        context = context + f"text: {doc['text']}\ntable: {doc['table']}\n\n"

    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt


def llm(prompt):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def rag(query):
    search_results = query_database(query)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt)
    return answer


# Example: Query the index
def main():
    # Example question
    user_query = "When will the next total solar eclipse occur in Europe?"

    # Query Elasticsearch for the answer
    search_results = rag(user_query)
    print(search_results)


if __name__ == "__main__":
    main()
