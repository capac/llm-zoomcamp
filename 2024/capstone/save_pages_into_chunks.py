import requests
from bs4 import BeautifulSoup
import hashlib
import json
import re
from io import StringIO
import pandas as pd
import numpy as np
from pathlib import Path
from helper_functions import retrieve_page_titles

# Specify the path of the directory to create
# and if it doesn't exist create it
directory_path = Path('wikipedia_pages')
directory_path.mkdir(parents=True, exist_ok=True)

# Main code to search for solar eclipse related pages and extract their titles
query = "solar eclipse"
limit = 200  # Number of pages to retrieve


# Function to fetch content from a Wikipedia page
def fetch_wikipedia_content(page_title):
    """
    Fetch the HTML content of a Wikipedia page given its title.
    """
    base_url = f"https://en.wikipedia.org/wiki/{page_title}"
    response = requests.get(base_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract the main content (all paragraphs in the main content area)
        content_paragraphs = soup.find_all('p')
        content = "\n".join([para.get_text() for para in content_paragraphs
                             if para.get_text().strip()])
        # Extracting tables
        tables = soup.find_all('table', {'class': 'wikitable'})
        table_data = []
        for table in tables:
            table_data.append(parse_html_table(table))

        return content, table_data
    else:
        print(f"Failed to fetch {page_title}")
        return None, None


# Function to parse an HTML table using pandas
def parse_html_table(table):
    # Use pandas to read the HTML table into a DataFrame
    try:
        # Read the first table as DataFrame
        tables_df = pd.read_html(StringIO(str(table)), index_col=0,
                                 flavor=["lxml", "bs4"])
        # Initialize a list to store all parsed tables
        parsed_tables = []

        for table_df in tables_df:  # Loop through each DataFrame returned
            # Convert tuple keys (if any) to strings in the table DataFrame
            table_df.columns = [str(col) if isinstance(col, tuple)
                                else col for col in table_df.columns]

            # Replace NaN values with None (JSON-compatible)
            table_df = table_df.replace({np.nan: None})

            # Convert DataFrame to list of dictionaries
            # (JSON-like format) and append to parsed_tables
            parsed_tables.append(table_df.to_dict(orient='records'))

        # Return the list of parsed tables
        # (each table is a list of dictionaries)
        return parsed_tables

    except ValueError:
        print("Failed to parse table")
        return []


# Function to clean the text (remove newlines and citation references)
def clean_text(text):
    # Remove newline characters
    text = text.replace('\n', ' ').replace('\r', '')
    # Remove citation references, e.g. [1], [2], [3]
    text = re.sub(r'\[\d+\]', '', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# Function to chunk text into logical blocks
# (complete sentences and reasonable size)
def chunk_text(text, max_tokens):
    # Split the text by sentence boundaries using regular expression
    sentences = re.split(r'(?<=\.) ', text)

    chunks = []
    current_chunk = []
    current_chunk_len = 0

    # Iterate through sentences and create chunks
    for sentence in sentences:
        # Token count approximation based on word count
        sentence_len = len(sentence.split())

        if current_chunk_len + sentence_len > max_tokens:
            # If adding this sentence exceeds the limit, save the current chunk
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            # Start a new chunk with the current sentence
            current_chunk_len = sentence_len
        else:
            # Add sentence to the current chunk
            current_chunk.append(sentence)
            current_chunk_len += sentence_len
    # Don't forget the last chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks


# Function to generate unique IDs using a shorter hash function (SHA-1)
def generate_unique_id(text):
    return hashlib.sha1(text.encode('utf-8')).hexdigest()


# Function to process the article and save chunks in JSON format
def process_wikipedia_article(page_title, max_tokens):
    content, tables = fetch_wikipedia_content(page_title)

    if content:
        clean_content = clean_text(content)
        chunks = chunk_text(clean_content, max_tokens)
        # Generate document ID from the page title
        doc_id = generate_unique_id(page_title)

        # Prepare JSON structure with chunks and unique IDs
        chunked_data = []
        for i, chunk in enumerate(chunks):
            chunk_id = generate_unique_id(f"{doc_id}_{i}")
            chunked_data.append({
                "doc_id": doc_id,
                "chunk_id": chunk_id,
                "text": chunk
            })

        # Add tables to the JSON structure
        if tables:
            for i, table in enumerate(tables):
                table_id = generate_unique_id(f"{doc_id}_table_{i}")
                chunked_data.append({
                    "doc_id": doc_id,
                    "chunk_id": table_id,
                    "table": table
                })

        return chunked_data
    else:
        return []


# Function to save chunks in JSON format
def save_chunks_as_json(chunks, file_name):
    # Save the list of chunk dictionaries into a JSON file.
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=4)


# Main script to process multiple Wikipedia articles
def process_multiple_pages(page_titles, max_tokens):
    """
    Process multiple Wikipedia pages by fetching their content
    and chunking them. Each page is saved as a separate JSON file.
    """
    for page_title in page_titles:
        # Process the Wikipedia page and get chunked content
        chunked_content = process_wikipedia_article(page_title,
                                                    max_tokens)

        # Save each chunked content to a unique JSON file
        if chunked_content:
            new_title = page_title.replace(' ', '_').replace(',', '').lower()
            file_name = f"{new_title}_chunks.json"
            save_chunks_as_json(chunked_content, directory_path / file_name)
            print(f"Chunks saved in {file_name}")
        else:
            print(f"Failed to process page: {page_title}")


# Main script
def main():
    # Process the pages and chunk their content into JSON files
    page_titles = retrieve_page_titles(query, limit)
    process_multiple_pages(page_titles, max_tokens=64)


if __name__ == "__main__":
    main()
