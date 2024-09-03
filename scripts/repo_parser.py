import requests
import csv
import mimetypes

def get_github_contents(repo_url):
    # Extract the user and repo name from the URL
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
            mime_type, _ = mimetypes.guess_type(item['name'])
            if mime_type and mime_type.split('/')[0] in ['image', 'video']:
                paths.append({"path": path, "content": ""})
            else:
                file_response = requests.get(item['download_url'])
                file_content = file_response.text
                paths.append({"path": path, "content": file_content})
    return paths

def write_to_csv(data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['path', 'content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    repo_url = input("Enter GitHub repository URL: ")
    contents = get_github_contents(repo_url)
    paths = process_contents(contents)
    write_to_csv(paths, "repo_contents.csv")
    print("CSV file 'repo_contents.csv' generated successfully.")
