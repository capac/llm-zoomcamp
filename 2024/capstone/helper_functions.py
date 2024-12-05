import requests

# Base URL for Wikipedia's search API
BASE_URL = "https://en.wikipedia.org/w/api.php"


# Function to search Wikipedia for solar eclipse-related articles
def retrieve_page_titles(query, category_titles="Solar eclipses", limit=10):
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "srlimit": limit,  # Limit number of search results
        "srprop": "",  # Only return the titles
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        search_results = response.json().get("query", {}).get("search", [])

        if search_results:
            relevant_pages = []

            # Filter results based on the "Solar_eclipses" category
            for result in search_results:
                page_title = result["title"]
                # Check if the page belongs to the Solar_eclipses category
                if check_page_in_category(page_title, category_titles):
                    relevant_pages.append(page_title)

            return relevant_pages

        else:
            print("No search results found.")
            return []

    else:
        print("Failed to retrieve data from Wikipedia API")
        return []


# Function to check if a page belongs to a specific category
def check_page_in_category(page_title, category_titles):
    params = {
        "action": "query",
        "titles": page_title,
        "prop": "categories",
        "format": "json"
    }

    response = requests.get(BASE_URL, params=params)
    pages = response.json().get("query", {}).get("pages", {})

    for _, page_data in pages.items():
        if "categories" in page_data:
            categories = [cat["title"].replace("Category:", "") for cat
                          in page_data["categories"]]

            for category in category_titles:
                if category in categories:
                    return True

    return False


if __name__ == "__main__":
    # Example: Search for solar eclipse
    query = "solar eclipse"
    category_names = ["20th-century solar eclipses",
                      "21st-century solar eclipses"]
    solar_eclipse_article_titles = retrieve_page_titles(
        query, limit=30,
        category_titles=category_names
        )

    # Output the relevant page titles
    print(solar_eclipse_article_titles)
