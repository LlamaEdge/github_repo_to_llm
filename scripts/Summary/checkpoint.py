import openai
import csv
import os
import json
import time
from datetime import datetime

API_BASE_URL = "https://llama.us.gaianet.network/v1"
MODEL_NAME = "llama"
API_KEY = "GAIA"

def save_checkpoint(checkpoint_file, processed_row, processed_contents):
    checkpoint_data = {
        'last_processed_row': processed_row,
        'processed_contents': list(processed_contents)
    }
    with open(checkpoint_file, 'w') as f:
        json.dump(checkpoint_data, f)

def load_checkpoint(checkpoint_file):
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            checkpoint_data = json.load(f)
            return (
                checkpoint_data['last_processed_row'],
                set(checkpoint_data['processed_contents'])
            )
    return 0, set()

def create_backup(file_path):
    """Create a backup of the output file with timestamp"""
    if os.path.exists(file_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{file_path}.{timestamp}.bak"
        os.rename(file_path, backup_path)
        print(f"Created backup at: {backup_path}")

def summarize(source_text, max_retries=3):
    for attempt in range(max_retries):
        try:
            client = openai.OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": """
                        You are an AI assistant designed to review pull requests (PRs) in GitHub repositories. Your task is to:

                        1. Summarize Code-related Files:
                        - Focus on key changes in the code, including additions, deletions, and modifications.
                        - Capture essential details such as the purpose of the code, any new functions, classes, or methods, and the overall impact of these changes on the project.
                        - Highlight any dependencies, error handling, or performance implications.

                        2. Summarize Markdown Files:
                        - Extract key points from documentation, readme files, and other markdown content.
                        - Identify sections related to project setup, usage instructions, change logs, or contributor guidelines.
                        - Note updates in the documentation and the implications for users or developers.
                        """,
                    },
                    {
                        "role": "user",
                        "content": source_text,
                    }
                ],
                model=MODEL_NAME,
                stream=False,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Attempt {attempt + 1} failed: {str(e)}. Retrying...")
            time.sleep(2 ** attempt)  

def qgen(source_text, max_retries=3):
    for attempt in range(max_retries):
        try:
            client = openai.OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Respond with a list of 10 questions. The text in the user message must contain specific answers to each question. Each question must be on its own line. Just list the questions without any introductory text or numbers.",
                    },
                    {
                        "role": "user",
                        "content": source_text,
                    }
                ],
                model=MODEL_NAME,
                stream=False,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Attempt {attempt + 1} failed: {str(e)}. Retrying...")
            time.sleep(2 ** attempt)

def agen(source_text, question, max_retries=3):
    for attempt in range(max_retries):
        try:
            client = openai.OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Give a comprehensive and well-reasoned answer to the user question strictly based on the context below and try to give a detailed explanation while answering the questions. Also try to add some bonus tip to in each answer and some relevant example outside of the content.\n" + source_text
                    },
                    {
                        "role": "user",
                        "content": question,
                    }
                ],
                model=MODEL_NAME,
                stream=False,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Attempt {attempt + 1} failed: {str(e)}. Retrying...")
            time.sleep(2 ** attempt)

def main():
    input_path = r"C:\Users\91745\OneDrive\Desktop\Github_analyser\output\local_repo\docs\quick_js_js.csv"
    output_path = r"C:\Users\91745\OneDrive\Desktop\Github_analyser\output\local_repo\summary\quick_js_js.csv"
    checkpoint_file = output_path + '.checkpoint'
    
    last_processed_row, processed_contents = load_checkpoint(checkpoint_file)
    
    if last_processed_row == 0 and os.path.exists(output_path):
        create_backup(output_path)

    row_count = last_processed_row

    try:
        with open(input_path, 'r', newline='', encoding='utf-8') as infile, \
             open(output_path, 'a', newline='', encoding='utf-8') as outfile:

            csv_reader = csv.reader(infile)
            csv_writer = csv.writer(outfile)
            
            for _ in range(last_processed_row):
                next(csv_reader)

            for row in csv_reader:
                try:
                    main_content = row[0]

                    if main_content in processed_contents:
                        continue

                    print(f"Processing row {row_count + 1}...")
                    
                    summary = summarize(main_content)
                    qs = qgen(main_content)
                    qna_list = []
                    
                    for q in qs.splitlines():
                        if len(q.strip()) == 0:
                            continue
                        answer = agen(main_content, q)
                        qna_list.append(f"Q: {q}\nA: {answer}")

                    csv_writer.writerow([main_content, f"Summary:\n{summary}"])
                    for qna in qna_list:
                        csv_writer.writerow([main_content, qna])
                    
                    processed_contents.add(main_content)
                    row_count += 1

                    save_checkpoint(checkpoint_file, row_count, processed_contents)
                    
                    print(f"Successfully processed row {row_count}")

                except Exception as e:
                    print(f"Error processing row {row_count + 1}: {str(e)}")
                    # Save checkpoint before raising the error
                    save_checkpoint(checkpoint_file, row_count, processed_contents)
                    raise

        print(f"Processing completed. Modified data has been written to {output_path}")
        print(f"Total rows processed: {row_count}")
        
        if os.path.exists(checkpoint_file):
            os.remove(checkpoint_file)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(f"Progress has been saved. You can resume from row {row_count + 1}")
        raise

if __name__ == "__main__":
    main()