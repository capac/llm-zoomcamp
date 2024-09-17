import requests

# Function to search Wikipedia for pages related to solar eclipses
def retrieve_wikipedia_page_titles(query, limit=100):
    base_url = "https://en.wikipedia.org/w/api.php"
    
    # Parameters for Wikipedia API search
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "srlimit": limit  # Limit the number of results
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        search_results = data['query']['search']
        if search_results:
            print("Wikipedia Page Titles Related to Solar Eclipses:")
            titles = [result['title'] for result in search_results]
            return titles
        else:
            print("No search results found.")
            return []
    else:
        print("Failed to retrieve data from Wikipedia API")
        return []
