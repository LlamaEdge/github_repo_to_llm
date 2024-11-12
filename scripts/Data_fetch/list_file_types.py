import requests
import mimetypes
from collections import defaultdict
import os

GITHUB_TOKEN = "" # Replace with your actual GitHub personal access token

def get_github_contents(repo_url):
    parts = repo_url.rstrip('/').split('/')
    user = parts[-2]
    repo = parts[-1]
    
    api_url = f"https://api.github.com/repos/{user}/{repo}/contents/"
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }
    
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    
    return response.json()

def list_file_extensions(contents, file_extensions=None, parent_path=""):
    if file_extensions is None:
        file_extensions = defaultdict(int)

    for item in contents:
        path = parent_path + item['name']
        
        if item['type'] == 'dir':
            dir_url = item['url']
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}"
            }
            dir_response = requests.get(dir_url, headers=headers)
            
            if dir_response.status_code == 200:
                dir_contents = dir_response.json()
                if isinstance(dir_contents, list):
                    list_file_extensions(dir_contents, file_extensions, path + "/")
                else:
                    print(f"Unexpected directory contents at {path}: {dir_contents}")
            else:
                print(f"Failed to fetch directory contents at {path}. Status code: {dir_response.status_code}")
        else:
            _, file_extension = os.path.splitext(item['name'])
            
            if file_extension:
                file_extensions[file_extension] += 1
            else:
                file_extensions["no_extension"] += 1 

    return file_extensions

def get_file_extensions_in_repo(repo_url):
    contents = get_github_contents(repo_url)
    file_extensions = list_file_extensions(contents)
    return dict(file_extensions)

if __name__ == "__main__":
    repo_url = input("Enter GitHub repository URL: ")
    file_extensions = get_file_extensions_in_repo(repo_url)
    for extension, count in file_extensions.items():
        print(f"{extension}: {count} files")
