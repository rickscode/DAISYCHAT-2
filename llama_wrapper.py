def read_search_results(file_path):
    collected_data = []
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()
        for i in range(0, len(lines), 4):
            title = lines[i].replace("Title: ", "")
            snippet = lines[i + 1].replace("Snippet: ", "")
            collected_data.append({'title': title, 'snippet': snippet})
    return collected_data

def create_input_data_file(data, file_path):
    with open(file_path, 'w') as file:
        for item in data:
            file.write(f"Title: {item['title']}\n")
            file.write(f"Snippet: {item['snippet']}\n")
            file.write("=" * 50 + "\n\n")
