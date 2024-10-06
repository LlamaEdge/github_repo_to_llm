import requests
import csv
import mimetypes
from io import BytesIO
from PIL import Image
from surya.ocr import run_ocr
from surya.model.detection.model import load_model as load_det_model, load_processor as load_det_processor
from surya.model.recognition.model import load_model as load_rec_model
from surya.model.recognition.processor import load_processor as load_rec_processor

def get_github_contents(repo_url):
    parts = repo_url.rstrip('/').split('/')
    user = parts[-2]
    repo = parts[-1]
    
    api_url = f"https://api.github.com/repos/{user}/{repo}/contents/"
    
    response = requests.get(api_url)
    response.raise_for_status()
    
    return response.json()

def process_contents(contents, paths=[], parent_path=""):
    langs = ["en"]
    det_processor, det_model = load_det_processor(), load_det_model()
    rec_model, rec_processor = load_rec_model(), load_rec_processor()
    
    for item in contents:
        path = parent_path + item['name']
        if item['type'] == 'dir':
            dir_contents = requests.get(item['url']).json()
            process_contents(dir_contents, paths, path + "/")
        else:
            mime_type, _ = mimetypes.guess_type(item['name'])
            if mime_type and mime_type.split('/')[0] == 'image':
                image_content = requests.get(item['download_url']).content
                image = Image.open(BytesIO(image_content))
                predictions = run_ocr([image], [langs], det_model, det_processor, rec_model, rec_processor)
                paths.append({"path": path, "content": ""})
    
    return paths

def write_to_csv(data, output_file):
    if data:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['path', 'content']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    else:
        print("No data to write to CSV.")

if __name__ == "__main__":
    repo_url = input("Enter GitHub repository URL: ")
    contents = get_github_contents(repo_url)
    paths = process_contents(contents)
    write_to_csv(paths, "repo_ocr.csv")
    print(f"CSV file 'repo_ocr.csv' generated successfully with {len(paths)} entries.")
