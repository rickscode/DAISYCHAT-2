### DAISYCHAT-2


https://github.com/rickscode/DAISYCHAT-2/assets/71875733/b76ee5af-0dcc-4857-acf4-de33c6279fd5



## Using Llama2-Chat-7B as LLM (Can Update this to larger model if running local on more powerful machine)
Check out 'The Bloke' On HuggingFace for other ggmal LLM's
Just for simple tasks Llama 2 is already pre-trained on just chatting with DAISYCHAT-2
For more updated data and precise answer content ask DAISYCHAT-2 to Google or search for a certain topic then produce any type of written content from the data # returned back in JSON form from google (URLS and token count can be edited in the daisy.py file)

### To run it: 
1. Download it and cd into main repo
2. Activate and run 'python -m venv tutorial-env' then 'source /path/DaisyChat-2/venv/bin/activate' 
3. cd into llama.cpp
4. pip install nltk googlesearch-python trafilatura
5. run command 'python3 daisy.py
6. If you get this error "Resource punkt not found", it's because Punkt sentence tokenizer for Natural Language Toolkit is missing. 
7. Uncomment from nltk.tokenize import word_tokenize
8. It will download the necessary English.pickle:
9. Also, uncomment import nltk
10. And nltk.download('punkt')
11. Exit daiy.py with Ctrl+Z
12. Re-run command 'daisy.py
13. You can then re-comment out the above imports they only importing once
14. Enter client chat input 

### These words are intercepted by the model for google searching topics in the "def process_input" function
typing 'search', 'find', 'query', 'google' will trigger the google search return JSON data and DAISYCHAT-2 will interpret and summarize data then ask for more input

### Example User Imput

> Please google coinbase and write my a 500 word review 

> Or Please search best beaches in Thailand, wait for summary from DAISYCHAT-2

When asked for your next chat input you can request for DAISYCHAT-2 to use the return data for an marketing email

Example: Please generate a maketing emailed titled [ ] to promote the destinations you have learnt about, please include hyperlink entries for booking flights to each destination




