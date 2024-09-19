import requests
from bs4 import BeautifulSoup
import hashlib
import json
import nltk
from helper_functions import retrieve_page_titles

# Download the necessary resources for sentence tokenization
nltk.download('punkt')

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

        return content
    else:
        print(f"Failed to fetch {page_title}")
        return None


# Function to create unique IDs using a hash function
def generate_hash_id(text, prefix="doc"):
    """
    Generate a unique hash ID for a given text. This is
    useful for creating unique IDs for documents and chunks.
    """
    hash_object = hashlib.sha256(text.encode('utf-8'))
    return f"{prefix}_{hash_object.hexdigest()}"


# Function to split content into sentences
def split_into_sentences(content):
    """
    Use NLTK to split content into a list of sentences.
    """
    sentences = nltk.sent_tokenize(content)
    return sentences


# Function to chunk sentences into blocks of approximately 1024 tokens
def chunk_sentences(sentences, max_tokens=1024):
    """
    Chunk sentences into blocks, where each block has a maximum token
    count (approx. 1024 tokens). This function ensures that chunks contain
    complete sentences.
    """
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        # Estimate the token length of the sentence
        # (tokens are approximated by splitting by spaces)
        sentence_length = len(sentence.split())

        # If adding the sentence exceeds max_tokens, finalize the current chunk
        if current_length + sentence_length > max_tokens and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length
        else:
            current_chunk.append(sentence)
            current_length += sentence_length

    # Add any remaining sentences as the last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


# Function to process and chunk Wikipedia content
def process_wikipedia_page(page_title, max_tokens=1024):
    """
    Process a Wikipedia page by fetching its content, chunking
    it into sentences, and returning JSON-like chunks with unique
    document and chunk IDs.
    """
    content = fetch_wikipedia_content(page_title)

    if content:
        # Generate a unique document ID for the page
        doc_id = generate_hash_id(page_title, prefix="doc")

        # Split the content into sentences
        sentences = split_into_sentences(content)

        # Chunk the sentences into blocks of approximately max_tokens
        chunks = chunk_sentences(sentences, max_tokens)

        # Create a list of chunk dictionaries
        chunked_content = []
        for i, chunk in enumerate(chunks):
            chunk_id = generate_hash_id(chunk, prefix="chunk")
            chunked_content.append({
                "doc_id": doc_id,
                "chunk_id": chunk_id,
                "text": chunk
            })

        return chunked_content
    return None


# Function to save chunks in JSON format
def save_chunks_as_json(chunks, file_name):
    """
    Save the list of chunk dictionaries into a JSON file.
    """
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=4)


# Main script to process multiple Wikipedia articles
def process_multiple_pages(page_titles, max_tokens=1024):
    """
    Process multiple Wikipedia pages by fetching their content
    and chunking them. Each page is saved as a separate JSON file.
    """
    for page_title in page_titles:
        # Process the Wikipedia page and get chunked content
        chunked_content = process_wikipedia_page(page_title, max_tokens)

        # Save each chunked content to a unique JSON file
        if chunked_content:
            file_name = f"{page_title}_chunks.json"
            save_chunks_as_json(chunked_content, file_name)
            print(f"Chunks saved in {file_name}")
        else:
            print(f"Failed to process page: {page_title}")


# Process the pages and chunk their content into JSON files
page_titles = retrieve_page_titles(query, limit)
process_multiple_pages(page_titles, max_tokens=1024)
