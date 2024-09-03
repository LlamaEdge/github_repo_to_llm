import requests
import mimetypes
from collections import defaultdict

def get_github_contents(repo_url):
    parts = repo_url.rstrip('/').split('/')
    user = parts[-2]
    repo = parts[-1]
    
    api_url = f"https://api.github.com/repos/{user}/{repo}/contents/"
    
    response = requests.get(api_url)
    response.raise_for_status()
    
    return response.json()

def list_file_types(contents, file_types=None, parent_path=""):
    if file_types is None:
        file_types = defaultdict(int)

    for item in contents:
        path = parent_path + item['name']
        if item['type'] == 'dir':
            dir_contents = requests.get(item['url']).json()
            list_file_types(dir_contents, file_types, path + "/")
        else:
            mime_type, _ = mimetypes.guess_type(item['name'])
            if mime_type:
                file_types[mime_type] += 1
            else:
                file_types["unknown"] += 1

    return file_types

def get_file_types_in_repo(repo_url):
    contents = get_github_contents(repo_url)
    file_types = list_file_types(contents)
    return dict(file_types)

if __name__ == "__main__":
    repo_url = input("Enter GitHub repository URL: ")
    file_types = get_file_types_in_repo(repo_url)
    for file_type, count in file_types.items():
        print(f"{file_type}: {count} files")
