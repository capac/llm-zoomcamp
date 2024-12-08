import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
from pathlib import Path


def retrieve_data_from_wikipedia_table(url):
    # Sending a GET request to the URL
    response = requests.get(url)

    # Parsing the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Finding the table in the page (assuming it's the first table on the page)
    table = soup.find("table", {"class": "wikitable"})

    # Reading the HTML table into a pandas DataFrame and returning the result
    return pd.read_html(StringIO(str(table)))[0]


# Specify the path of the directory you want to create
current_dir = Path.cwd()
data_dir = current_dir / 'data'

# Create the directory if it doesn't exist
data_dir.mkdir(parents=True, exist_ok=True)

# URL of the Wikipedia pages
url_list = [
    'https://en.wikipedia.org/wiki/List_of_solar_eclipses_in_the_20th_century',
    'https://en.wikipedia.org/wiki/List_of_solar_eclipses_in_the_21st_century'
]

# Create an empty pandas DataFrame
df = pd.DataFrame()

# Loop through the URLs in the list and append the result to the DataFrame
for url in url_list:
    table_df = retrieve_data_from_wikipedia_table(url)
    df = pd.concat([df, table_df])

# Saving the DataFrame to a CSV file
csv_file_path = 'data/solar_eclipses.csv'
df.to_csv(csv_file_path, index=False)

print('Done!')
