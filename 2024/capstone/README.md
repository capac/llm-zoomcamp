# Capstone project for LLM Zoomcamp

This project aims to create a text-based chatbot that provides information on solar eclipses, using information from 187 pages on solar eclipses from Wikipedia. Using the technique of retrieval augmented generation (RAG) and storing the information on Elasticsearch, the user can interact with the chatbot by modifiying the text query in the `search_query.py` file.

## Requirements

The scripts make use of:
* [Elasticsearch](https://www.elastic.co/elasticsearch "https://www.elastic.co/elasticsearch")
* [OpenAI](https://openai.com/ "https://openai.com/") API project key (requires an OpenAI account and OpenAI credits)

## Files used

* `save_pages_into_chunks.py`: This script downloads 187 articles from a Wikipedia search on solar eclipses and saves the articles as chunks in JSON format in a local folder.

* `index_chunks.py`: This script indexes the chunks generated in the previous script using [Elasticsearch](https://www.elastic.co/elasticsearch "https://www.elastic.co/elasticsearch"). In order for the script to work, an Elasticsearch Docker container needs to be running. The command used to run Elasticsearch is: `docker run -it --rm --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" elasticsearch:8.4.3`. Once you run the command, if the Elasticsearch Docker container isn't present Docker will download it for you.

* `search_query.py`: This script allow the user to interact with the model and submit queries on solar eclipses. In some cases however, the information retrieved from Wikipedia doesn't return appropriate answers for some queries, possibly due to a lack of information in the Wikipedia articles themselves. However, try tweaking the wording of the query itself, sometimes a bit of prompt engineering is all that is needed!

* `local_search_query.py`: Used just for querying the local Elasticsearch container. In addition to the previous requirements, it also requires `spacy`.
