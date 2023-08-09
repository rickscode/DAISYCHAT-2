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
    
    model_path = "/home/rick/code/DaisyPR-Agent/llama.cpp/models/llama2_7b_chat/llama-2-7b-chat.ggmlv3.q2_K.bin"
    output_file = "llama_generated_prompts.txt"

    with open(output_file, 'w') as f:
        for prompt in prompts:
            command = f'./main -m {model_path} -p "{prompt}" -n 100\n'
            f.write(command)
    
    print(f"Generated prompts written to {output_file}")

if __name__ == "__main__":
    main()

# Define the extra prompt
extra_prompt = """
As a subject expert in digital nomad lifestyles and travel, I am excited to delve into the captivating allure of some of the world's most sought-after destinations for remote work and adventure. In this comprehensive article, I will explore the unique appeal and practical aspects of nomadic living in Lisbon, Canggu, Bangkok, Zagreb, Timisoara, Chiang Mai, Berlin, and Bengaluru. Join me as we uncover the distinctive advantages and cultural experiences that await digital nomads in these vibrant cities. From coworking spaces to local cuisine, we will take a closer look at what makes these destinations top choices for the nomadic lifestyle. Discover the blend of modernity and tradition, the bustling streets and serene retreats, and the opportunities that each city presents for personal and professional growth. Whether you're a seasoned nomad or embarking on your first journey, this article will provide you with insights and inspiration to make the most of your remote work experience.
"""

# Path to the generated prompts file
generated_prompts_path = "/home/rick/code/DaisyPR-Agent/llama_generated_prompts.txt"

# Read the existing prompts from the file
with open(generated_prompts_path, "r") as file:
    prompts = file.readlines()

# Add the extra prompt to each generated prompt
prompts_with_extra = [prompt.strip() + extra_prompt for prompt in prompts]

# Write the prompts with the extra prompt back to the file
with open(generated_prompts_path, "w") as file:
    for prompt in prompts_with_extra:
        file.write(prompt + "\n")

# Run the LLAMA command for each prompt
for prompt in prompts_with_extra:
    cmd = f"./main -m /home/rick/code/DaisyPR-Agent/llama.cpp/models/llama2_7b_chat/llama-2-7b-chat.ggmlv3.q2_K.bin -p \"{prompt}\" -n 1"
    os.system(cmd)
