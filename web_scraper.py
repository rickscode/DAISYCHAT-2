# import os
# import requests
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Get the API key and Custom Search Engine ID from the environment variables
# API_KEY = os.getenv('GOOGLE_API_KEY')
# CUSTOM_SEARCH_ENGINE_ID = os.getenv('CUSTOM_SEARCH_ENGINE_ID')

# def search_google(query):
#     url = f'https://www.googleapis.com/customsearch/v1'
#     params = {
#         'key': API_KEY,
#         'cx': CUSTOM_SEARCH_ENGINE_ID,
#         'q': query,
#         'num': 10,  # Number of search results
#     }
#     response = requests.get(url, params=params)
#     data = response.json()
#     return data.get('items', [])

# def extract_data_from_search_results(search_results):
#     collected_data = []
#     for item in search_results:
#         print(item)  # Add this line to print the item dictionary
#         title = item['title']
#         snippet = item['snippet']
#         url = item['link']
#         collected_data.append({'title': title, 'snippet': snippet, 'url': url})
#     return collected_data


# def save_data_to_file(data, filename):
#     with open(filename, 'w') as file:
#         for item in data:
#             file.write(f"Title: {item['title']}\n")
#             file.write(f"Snippet: {item['snippet']}\n")
#             file.write(f"URL: {item['url']}\n")
#             file.write("=" * 50 + "\n\n")

# if __name__ == '__main__':
#     search_query = input("Enter the search query: ")
#     search_results = search_google(search_query)
#     collected_data = extract_data_from_search_results(search_results)
    
#     # Display and save collected data
#     for item in collected_data:
#         print(f"Title: {item['title']}")
#         print(f"Snippet: {item['snippet']}")
#         print(f"URL: {item['url']}")
#         print("=" * 50 + "\n")
    
#     # Save data to a file
#     save_data_to_file(collected_data, 'search_results.txt')

import os
import requests
from bs4 import BeautifulSoup
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
        'num': 3,  # Number of search results
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get('items', [])

def get_shortened_snippet(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    article_text = extract_and_shorten_article_text(soup)  # Call the function to extract and shorten article text
    return article_text

def extract_and_shorten_article_text(soup, max_words=2000):  # Change max_words to the desired word count
    # Example: Extract the text from all <p> elements and concatenate them
    paragraphs = soup.find_all('p')
    article_text = ' '.join([p.get_text() for p in paragraphs])
    
    # Split the text into words and limit the snippet to the specified word count
    words = article_text.split()
    shortened_text = ' '.join(words[:max_words])
    
    return shortened_text

def extract_data_from_search_results(search_results):
    collected_data = []
    for item in search_results:
        title = item['title']
        url = item['link']
        snippet = get_shortened_snippet(url)
        collected_data.append({'title': title, 'snippet': snippet, 'url': url})
    return collected_data

def save_data_to_file(data, filename):
    with open(filename, 'w') as file:
        for item in data:
            file.write("=" * 50 + "\n\n")
            file.write(f"Title: {item['title']}\n")
            file.write(f"Snippet: {item['snippet']}\n")
            file.write(f"URL: {item['url']}\n")
            file.write("=" * 50 + "\n\n")

if __name__ == '__main__':
    search_query = input("Enter the search query: ")
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

