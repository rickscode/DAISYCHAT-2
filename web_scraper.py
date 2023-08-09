import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key and Custom Search Engine ID from the environment variables
API_KEY = os.getenv('GOOGLE_API_KEY')
CUSTOM_SEARCH_ENGINE_ID = os.getenv('CUSTOM_SEARCH_ENGINE_ID')

def search_google(query):
    url = f'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': API_KEY,
        'cx': CUSTOM_SEARCH_ENGINE_ID,
        'q': query,
        'num': 10,  # Number of search results
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get('items', [])

# Rest of the code remains unchanged...

# def extract_data_from_search_results(search_results):
#     collected_data = []
#     for item in search_results:
#         title = item['title']
#         snippet = item['snippet']
#         url = item['link']
#         collected_data.append({'title': title, 'snippet': snippet, 'url': url})
#     return collected_data
# Modify extract_data_from_search_results to return a list of dictionaries
def extract_data_from_search_results(search_results):
    collected_data = []
    for item in search_results:
        print(item)  # Add this line to print the item dictionary
        title = item['title']
        snippet = item['snippet']
        url = item['link']
        collected_data.append({'title': title, 'snippet': snippet, 'url': url})
    return collected_data


def save_data_to_file(data, filename):
    with open(filename, 'w') as file:
        for item in data:
            file.write(f"Title: {item['title']}\n")
            file.write(f"Snippet: {item['snippet']}\n")
            file.write(f"URL: {item['url']}\n")
            file.write("=" * 50 + "\n\n")

if __name__ == '__main__':
    search_query = "best digital nomad destinations"
    search_results = search_google(search_query)
    collected_data = extract_data_from_search_results(search_results)
    
    # Display and save collected data
    for item in collected_data:
        print(f"Title: {item['title']}")
        print(f"Snippet: {item['snippet']}")
        print(f"URL: {item['url']}")
        print("=" * 50 + "\n")
    
    # Save data to a file
    save_data_to_file(collected_data, 'search_results.txt')
