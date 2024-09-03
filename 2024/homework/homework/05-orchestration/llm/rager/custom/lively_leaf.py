from elasticsearch import Elasticsearch

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(*args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here
    
    es_client = Elasticsearch('http://elasticsearch:9200') 

    # print(f'Elastic Search client info: {es_client.info()}')

    def elastic_search(query):
        search_query = {
            "size": 5,
            "query": {
                "bool": {
                    "must": {
                        "multi_match": {
                            "query": query,
                            "fields": ["question^3", "text", "section"],
                            "type": "best_fields"
                        }
                    }
                }
            }
        }

        response = es_client.search(
            index='documents_20240821_0928_20240821_1602',
            body=search_query
        )
        
        result_docs = []
        
        for hit in response['hits']['hits']:
            result_docs.append(hit['_source'])
        
        print(result_docs)

    elastic_search("When is the next cohort?")


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
