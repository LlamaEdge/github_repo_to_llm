import os
import csv
import sys

csv.field_size_limit(10**9)

def process_local_repo(repo_path, paths=[]):
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                file_content = f.read()
            relative_path = os.path.relpath(file_path, repo_path)
            
            # Formatting content based on file extension
            extension = os.path.splitext(relative_path)[1]
            if extension == '.md':
                formatted_content = f"The following is a markdown document located at {relative_path}\n------\n{file_content}\n------"
            elif extension == '.rs':
                formatted_content = f"```rust:{relative_path}\n{file_content}\n```"
            elif extension == '.sh':
                formatted_content = f"```bash:{relative_path}\n{file_content}\n```"
            elif extension == '.py':
                formatted_content = f"```python:{relative_path}\n{file_content}\n```"
            elif extension =='.js':
                formatted_content = f"```javascript:{relative_path}\n{file_content}\n```"
            else:
                formatted_content = f"The following document is located at {relative_path}\n------\n{file_content}\n------"
            
            paths.append({"FormattedContent": formatted_content})

    return paths

def write_to_csv(data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        for row in data:
            writer.writerow([row['FormattedContent']])

if __name__ == "__main__":
    repo_path = input("Enter the local repository path: ")
    paths = process_local_repo(repo_path)
    output_csv = "local_repo_formatted.csv"
    write_to_csv(paths, output_csv)
    print(f"CSV file '{output_csv}' generated successfully.")
