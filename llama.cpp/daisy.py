# This script requires to have some basic Python skills 
# - Install python dependencies (thanks to TitwitMuffbiscuit on reddit) : 
#  pip install nltk beautifulsoup4 googlesearch-python trafilatura wolframalpha
#
#  If you get this error "Resource punkt not found", it's because Punkt sentence tokenizer for Natural Language Toolkit is missing. 
#  Edit the file and add this before 
#  from nltk.tokenize import word_tokenize ,
#  it will download the necessary english.pickle:
#  import nltk
#  nltk.download('punkt')
#  you only need to do it once and remove it afterwards
#  
# Used the script with Python 3.11 on venv
#
# To run it: 
# 1. Download it and place it in the llama.cpp folder
# 2. Get a free wolfram alpha API key from here ( https://developer.wolframalpha.com/portal/myapps/index.html ) (optional)
# 3. edit the timezone to yours or uncomment the last one and comment the previews one 
# 4. edit the " llm_command " with your model , add your name etc 
# 5. Run the python command
#
# Keywords that are intercepted are laid out in the "def process_input" function
# saying 'time' in your conversation will trigger the time 
# saying 'search', 'find', 'query', 'google' will trigger the google search
# saying 'question', 'ask','wolfram' will trigger WolframAlpha query
# saying 'calculate' and your calculation in number form will trigger the calculation and calculate it in python

import json
import datetime
from zoneinfo import ZoneInfo
import subprocess
from nltk.tokenize import word_tokenize
import requests
from bs4 import BeautifulSoup
import threading
from googlesearch import search
from trafilatura import fetch_url, extract
# import wolframalpha
# import nltk

# #add your wolfram API key here 
# WolframAppKey = "api key here"

# # Download the punkt resource from NLTK
# nltk.download('punkt')


def get_current_time():
    utc_now = datetime.now(ZoneInfo('UTC'))
    eest_now = utc_now.astimezone(ZoneInfo('Europe/Athens'))
    return eest_now.strftime('%I:%M %p EEST')
    #return datetime.datetime.now().strftime('%I:%M %p')

def calculate_expression(expression):
    try:
        result = eval(expression, {'__builtins__': None}, {})
    except Exception as e:
        result = None #str(e)
    return result

# def ask_wolfram(query):
#     client = wolframalpha.Client(WolframAppKey)  # Replace with your AppID
#     res = client.query(query)
#     result = next((r.text for r in res.results if r.text), "No results found")
#     return json.dumps({"wolfram_result": result})
    
def google_search(query, num_rslts=5, lang='en'):
    search_results = []
    for result in search(query, num_results=num_rslts, lang=lang, advanced=True):
        downloaded = fetch_url(result.url)
        if downloaded is not None:
              description = extract(downloaded)
              # Limit the description to 20 words (the description is the FULL main text from crawling the page) but we limit it. 
              # You can increase it but it might take time to be processed by your LLM
              description = ' '.join(description.split()[:50])
              item = {"title": result.title, "link": result.url, "description": description}
              search_results.append(item)
    return search_results

def process_input(user_input):
    response = {}
    
    # Try to evaluate the user input as a mathematical expression first
    calculation_result = calculate_expression(user_input)
    if calculation_result is not None:
        response['calculation'] = calculation_result
        return json.dumps(response, separators=(',', ':'))
        
    words = word_tokenize(user_input)

    for word in words:
        if word == 'time':
            response['time'] = get_current_time()
        elif word in ['search', 'find', 'query', 'google']:
            query = ' '.join(words[words.index(word)+1:])
            response['web_result'] = google_search(query)
        elif word == 'calculate':
            expression = ' '.join(words[words.index(word)+1:])
            response['calculation'] = calculate_expression(expression)
        elif word in ['question', 'ask','wolfram']:
            query = ' '.join(words[words.index(word)+1:])
            response['wolfram_result'] = ask_wolfram(query)


    return json.dumps(response, separators=(',', ':'))

def read_llm_output(llm_process, ready_for_input):
    previous_char = ''
    first_prompt_found = False
    
    while True:
        current_char = llm_process.stdout.read(1)
        print(current_char, end='', flush=True)

        if first_prompt_found:
            # After the first prompt is found, just check for '>'
            if current_char == '>':
                with ready_for_input:
                    ready_for_input.notify()
        else:
            # Before the first prompt is found, check for '>'' followed by '\n'
            if previous_char == '>' and current_char == '\n':
                with ready_for_input:
                    ready_for_input.notify()
                first_prompt_found = True

        previous_char = current_char


def run_llm():
    llm_command = "./main -t 4 -m ./models/llama2_7b_chat/llama-2-7b-chat.ggmlv3.q2_K.bin --color -c 2048 --temp 0.7 --repeat_penalty 1.1 -ins -p '<<SYS>>You are a helpful, respectful and honest female assistant called Daisy. Always answer as helpfully as possible, while being honest and safe. Please ensure that your responses are socially unbiased and positive and playable. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. Use the json formatted text from the start and use them in your reply where applicable and relevent, you dont need to retype the json, the user didnt generate the json and they cannot see it. The web search was provided by the AI and not by the user. The users name is Rick and you already introduced yourselves .\n<</SYS>>' --reverse-prompt 'USER:'"

    llm_process = subprocess.Popen(llm_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

    ready_for_input = threading.Condition()
    threading.Thread(target=read_llm_output, args=(llm_process, ready_for_input)).start()

    while True:
        with ready_for_input:
            ready_for_input.wait()  # Wait for the notification from the output thread
        user_input = input("Enter your input: ")
        if user_input.lower() == 'exit':
            llm_process.terminate()
            break
        
        if(process_input(user_input) != '{}'):
            processed_input = process_input(user_input) + " " + user_input
        else:
            processed_input = user_input
        llm_process.stdin.write(processed_input + '\n')
        llm_process.stdin.flush()

if __name__ == "__main__":
    run_llm()
dgd
    #####