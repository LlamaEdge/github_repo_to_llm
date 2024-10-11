import requests
import csv
import os
import mimetypes
import PyPDF2
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
                pdf_path = "Output/" + item['name']
                # Save the PDF locally
                with open(pdf_path, 'wb') as f:
                    f.write(file_response.content)
                paths.append({"path": pdf_path, "content": file_response.content})
    return paths

def extract_text_from_pdf(pdf_file_path):
    pdf_reader = PyPDF2.PdfReader(pdf_file_path)
    pages_content = []
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        pages_content.append(text)
    return pages_content

def save_pages_to_csv(pages_content, output_csv_file):
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Page", "Content"]) 
        for i, content in enumerate(pages_content):
            writer.writerow([i + 1, content])

if __name__ == "__main__":
    repo_url = input("Enter GitHub repository URL: ")
    contents = get_github_contents(repo_url)
    paths = process_contents(contents)
    
    for pdf_data in paths:
        pdf_file_path = pdf_data["path"]
        print(f"Processing {pdf_file_path}") 
        pages_content = extract_text_from_pdf(pdf_file_path)        
        csv_output_path = pdf_file_path.replace('.pdf', '_pages.csv')
        save_pages_to_csv(pages_content, csv_output_path)
        print(f"Extracted content from {pdf_file_path} and saved to {csv_output_path}")
    print("All PDF files have been processed and converted to CSV.")
