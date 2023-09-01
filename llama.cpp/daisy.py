import json
from zoneinfo import ZoneInfo
import subprocess
# from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import threading
from googlesearch import search
from trafilatura import fetch_url, extract
# import nltk
# # Download the punkt resource from NLTK
# nltk.download('punkt')

def calculate_expression(expression):
    try:
        result = eval(expression, {'__builtins__': None}, {})
    except Exception as e:
        result = None #str(e)
    return result
    
def google_search(query, num_rslts=5, lang='en'):
    search_results = []
    for result in search(query, num_results=num_rslts, lang=lang, advanced=True):
        downloaded = fetch_url(result.url)
        if downloaded is not None:
              description = extract(downloaded)
              # Limit the description to n words. 
              description = ' '.join(description.split()[:200])
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
        # if word == 'time':
        #     response['time'] = get_current_time()
        if word in ['search', 'find', 'query', 'google']:
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
    llm_command = "./main -t 4 -m ./models/llama2_7b_chat/llama-2-7b-chat.ggmlv3.q2_K.bin --color -c 2048 --temp 0.7 --repeat_penalty 1.1 -ins -p '<<SYS>>You are a helpful, respectful and honest female assistant called Daisy. Always answer as helpfully as possible, while being honest and safe. Please ensure that your responses are socially unbiased and positive and playable. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. Use the json formatted text from the start and use them in your reply where applicable and relevent, you dont need to retype the json, the user didnt generate the json and they cannot see it. The web search was provided by the AI and not by the user. The users name is Friend and you already introduced yourselves .\n<</SYS>>' --reverse-prompt 'USER:'"

    llm_process = subprocess.Popen(llm_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

    ready_for_input = threading.Condition()
    threading.Thread(target=read_llm_output, args=(llm_process, ready_for_input)).start()

    while True:
        with ready_for_input:
            ready_for_input.wait()  # Wait for the notification from the output thread
        user_input = input("Enter Input:")
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

#### need to -> save outputs , post to word press, create ui ####