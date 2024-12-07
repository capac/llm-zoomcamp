# Capstone project for LLM Zoomcamp

This project aims to create a chatbot that provides information on solar eclipses using information from 200 pages on solar eclipese on Wikipedia. Using the technique of retrieval augmented generation (RAG) and storing the information on Elasticsearch, the user can interact with the chatbot through a Streamlit interface.

## Files used

* `save_pages_into_chunks.py`: This script downloads the first 200 articles from a search on Wikipedia on solar eclipses and saves the articles as chunks in JSON format.

* `index_chunks.py`: This script indexes the chunks from the previous script in Elasticsearch. In order to work, the script requires an Elasticsearch Docker container to be running. The command used to run Elasticsearch is: `docker run -it --rm --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" elasticsearch:8.4.3`.

* `search_query.py`: This script allow the user to interact with the model and submit queries on solar eclipses. The information retrieved from Wikipedia however doesn't return appropriate answers for some queries, possibly due to a lack of information in the Wikipedia articles themselves.
