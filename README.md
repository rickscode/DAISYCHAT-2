### DAISYCHAT-2


![DaisyPR](https://github.com/rickscode/DAISYCHAT-2/assets/71875733/e2db7f69-15eb-4829-99c5-8fdfbeb47acc)


## Using Llama2-Chat-7B as LLM (Can Update this to larger model if running local on more powerful machine)
# Check out 'The Bloke' On HuggingFace for other ggmal LLM's
# Just for simple tasks Llama 2 is already pre-trained on just chat with DAISYCHAT-2
# For more update date and precise answer content ask DAISYCHAT-2 to google or search a certain topic then produce any type of written content from the data # returned back in JSON form from google (URLS AND TOKENS RETURNED FROM EACH ONE CAN BE EDITIED IN daisy.py file)

### To run it: 
1. Download it and cd into main repo
# 2. activate and run 'python -m venv tutorial-env' then 'source /path/DaisyChat-2/venv/bin/activate' 
# 3. cd into llama.cpp
# 4. pip install nltk googlesearch-python trafilatura
# 4. run command 'python3 daisy.py
# 5. If you get this error "Resource punkt not found", it's because Punkt sentence tokenizer for Natural Language Toolkit is missing. 
# 6. Uncomment from nltk.tokenize import word_tokenize
# 7. it will download the necessary english.pickle:
# 8. Also uncomment import nltk
# 9. And nltk.download('punkt')
# 10. Exit daiy.py with Ctrl+Z
# 11. Re-run command 'daisy.py
# 12. You can then re-comment out the above imports they only importing once
# 5. Enter client chat input 

### These words are intercepted are laid out in the "def process_input" function
# typing 'search', 'find', 'query', 'google' will trigger the google search return JSON data and DAISYCHAT-2 will interpret and summarize data then ask for 
# more input

### Example 
# Please google coinbase and write my a 500 word review 

# Or Please search best beaches in Thailand, wait for summary from DAISYCHAT-2
# When asked for your next chat input you can request for DAISYCHAT-2 to use the return data for an marketing email
# Example: Please generate a maketing emailed titled [ ] to promote the destinations you have learnt about, please include hyperlink entries for booking 
# flights to each destination




