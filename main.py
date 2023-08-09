from llama_wrapper import generate_article
from web_scraper import read_search_results

if __name__ == '__main__':
    search_results_file = 'search_results.txt'
    search_results = read_search_results(search_results_file)
    input_data_file = 'input_data.txt'
    
    # Generate input_data.txt for Llama model
    # create_input_data_file(search_results, input_data_file)
    
    # Generate a new article using Llama model
    generated_article = generate_article(input_data_file)
    
    print("Generated Article:")
    print(generated_article)
