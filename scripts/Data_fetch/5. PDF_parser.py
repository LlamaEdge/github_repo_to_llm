import requests
import csv
import mimetypes

def get_github_contents(repo_url):
    parts = repo_url.rstrip('/').split('/')
    user = parts[-2]
    repo = parts[-1]
    
    api_url = f"https://api.github.com/repos/{user}/{repo}/contents/"
    
    response = requests.get(api_url)
    response.raise_for_status()
    
    return response.json()

def process_contents(contents, paths=[], parent_path=""):
    for item in contents:
        path = parent_path + item['name']
        if item['type'] == 'dir':
            dir_contents = requests.get(item['url']).json()
            process_contents(dir_contents, paths, path + "/")
        else:
            extension = '.' + item['name'].split('.')[-1] if '.' in item['name'] else ''
            if extension == '.pdf':
                file_response = requests.get(item['download_url'])
                paths.append({"path": path, "content": file_response.content})
    return paths

def write_to_csv(data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['path', 'content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in data:
            writer.writerow({"path": row["path"], "content": ""})

if __name__ == "__main__":
    repo_url = input("Enter GitHub repository URL: ")
    contents = get_github_contents(repo_url)
    paths = process_contents(contents)
    write_to_csv(paths, "Output// repo_pdf.csv")
    print("CSV file 'repo_pdf.csv' generated successfully, containing only paths to PDF files.")