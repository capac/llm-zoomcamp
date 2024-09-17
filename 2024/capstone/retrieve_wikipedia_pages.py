import requests
import json
from pathlib import Path
from helper_functions import retrieve_wikipedia_page_titles

# Main code to search for solar eclipse related pages and extract their titles
query = "solar eclipse"
limit = 500  # Number of pages to retrieve
page_titles = retrieve_wikipedia_page_titles(query, limit)

# Directory to save JSON files
output_dir = Path("wikipedia_pages")
output_dir.mkdir(parents=True, exist_ok=True)

# Base URL for the Wikipedia API (action=parse to get the full content)
base_url = "https://en.wikipedia.org/w/api.php"

# Function to fetch and save Wikipedia page as JSON
def fetch_and_save_wikipedia_page(page_title):
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "explaintext": True,  # Extracts plain text with no markup
        "titles": page_title,
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        page_id = next(iter(data['query']['pages']))  # Get the page ID
        content = data['query']['pages'][page_id]['extract']
        file_path = output_dir / f"{page_title}.json"
        with file_path.open("w", encoding="utf-8") as file:
            json.dump({"title": page_title, "content": content}, file, indent=4, ensure_ascii=False)
        print(f"Saved: {file_path}")
    else:
        print(f"Failed to retrieve: {page_title}")

# Retrieve and save each Wikipedia page
for title in page_titles:
    fetch_and_save_wikipedia_page(title)
