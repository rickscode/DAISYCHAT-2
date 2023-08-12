# import subprocess
# import os

# def main():
#     with open('/home/rick/code/DaisyPR-Agent/search_results.txt', 'r') as file:
#         content = file.read()

#     sections = content.split("==================================================\n")
#     prompts = []

#     for section in sections:
#         lines = section.strip().split('\n')
#         if len(lines) >= 3:
#             title = lines[0].replace("Title: ", "")
#             snippet = lines[1].replace("Snippet: ", "")
#             prompts.append(snippet)
    
#     extra_prompt = input("Enter the extra prompt: ")

#     model_path = "/home/rick/code/DaisyPR-Agent/llama.cpp/models/llama2_7b_chat/llama-2-7b-chat.ggmlv3.q2_K.bin"
#     output_file = "llama_generated_prompts.txt"

#     with open(output_file, 'w') as f:
#         for prompt in prompts:
#             first_quote = prompt.find('"')
#             modified_prompt = f'{prompt[:first_quote+1]}{extra_prompt}{prompt[first_quote+1:]}\n'
#             command = f'./main -m {model_path} --color -c 4096 --temp 0.7 -p "{modified_prompt}" -n 1700\n'
#             f.write(command)
    
#     print(f"Generated prompts with extra prompt written to {output_file}")

# if __name__ == "__main__":
#     main()


### save llama output to llama_generated_output.txt

import subprocess
import os

def main():
    with open('/home/rick/code/DaisyPR-Agent/search_results.txt', 'r') as file:
        content = file.read()

    sections = content.split("==================================================\n")
    prompts = []

    for section in sections:
        lines = section.strip().split('\n')
        if len(lines) >= 3:
            title = lines[0].replace("Title: ", "")
            snippet = lines[1].replace("Snippet: ", "")
            prompts.append(snippet)
    
    extra_prompt = input("Enter the extra prompt: ")

    model_path = "/home/rick/code/DaisyPR-Agent/llama.cpp/models/llama2_7b_chat/llama-2-7b-chat.ggmlv3.q2_K.bin"
    output_file = "llama_generated_prompts.txt"
    llama_output_file = "llama_generated_output.txt"

    with open(output_file, 'w') as f:
        for prompt in prompts:
            first_quote = prompt.find('"')
            modified_prompt = f'{prompt[:first_quote+1]}{extra_prompt}{prompt[first_quote+1:]}\n'
            command = f'./main -m {model_path} --color -c 4096 --temp 0.7 -p "{modified_prompt}" -n 1700 > {llama_output_file}\n'
            f.write(command)
    
    print(f"Generated prompts with extra prompt written to {output_file}")

if __name__ == "__main__":
    main()
