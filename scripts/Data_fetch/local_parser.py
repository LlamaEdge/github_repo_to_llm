import os
import csv

def process_local_repo(repo_path, paths=[]):
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                file_content = f.read()
            relative_path = os.path.relpath(file_path, repo_path)
            paths.append({"Path": relative_path, "Content": file_content})

    return paths

def write_to_csv(data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Path', 'Content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    repo_path = input("Enter the local repository path: ")
    paths = process_local_repo(repo_path)
    write_to_csv(paths, "local_repo.csv")
    print("CSV file 'local_repo.csv' generated successfully.")
