import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import json

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
        'num': 1,  # Number of search results
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get('items', [])

def scrape_article_content(url, chromedriver_path):
    service = Service(chromedriver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        page_source = driver.page_source
        return page_source

    finally:
        driver.quit()

if __name__ == '__main__':
    search_query = "best digital nomad destinations"
    search_results = search_google(search_query)

    collected_data = []
    chromedriver_path = '/usr/local/bin/chromedriver'  # Replace with the actual path

    for item in search_results:
        title = item['title']
        snippet = item['snippet']
        url = item['link']

        try:
            article_content = scrape_article_content(url, chromedriver_path)
            collected_data.append({'title': title, 'snippet': snippet, 'url': url, 'article': article_content})
        except Exception as e:
            print(f"Error extracting content from {url}: {e}")

    # Save collected data to a JSON file
    with open('collected_data.json', 'w') as file:
        json.dump(collected_data, file, indent=4)

    for item in collected_data:
        print(f"Title: {item['title']}")
        print(f"Snippet: {item['snippet']}")
        print(f"URL: {item['url']}")
        print(f"Article Content:", item['article'][:300])  # Print the first 300 characters of the article content
        print("=" * 50 + "\n")
