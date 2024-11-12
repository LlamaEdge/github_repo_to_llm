import requests
import csv


GITHUB_TOKEN = "" # Replace with your actual GitHub token

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

def process_contents(contents, paths=[], parent_path=""):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }

    for item in contents:
        path = parent_path + item['name']
        if item['type'] == 'dir':
            dir_response = requests.get(item['url'], headers=headers)
            dir_response.raise_for_status()
            dir_contents = dir_response.json()
            process_contents(dir_contents, paths, path + "/")
        else:
            file_response = requests.get(item['download_url'], headers=headers)
            file_response.raise_for_status()
            file_content = file_response.text
            paths.append({"Path": path, "Content": file_content})

    return paths

def write_to_csv(data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Path', 'Content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    repo_url = input("Enter GitHub repository URL: ")
    output_path = input("Enter output CSV file path: ")
    contents = get_github_contents(repo_url)
    paths = process_contents(contents)
    write_to_csv(paths, output_path)
    print(f"CSV file '{output_path}' generated successfully.")
