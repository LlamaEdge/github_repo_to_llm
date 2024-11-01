import openai
import csv
import os
import time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
csv.field_size_limit(10**9)

API_BASE_URL = "https://llama.us.gaianet.network/v1"
MODEL_NAME = "llama"
API_KEY = "GAIA"

def create_retry_decorator():
    return retry(
        retry=retry_if_exception_type((openai.APIError, openai.APITimeoutError)),
        stop=stop_after_attempt(3), 
        wait=wait_exponential(multiplier=1, min=4, max=10),
        before_sleep=lambda retry_state: print(f"Retry attempt {retry_state.attempt_number} after {retry_state.outcome.exception()}")
    )

@create_retry_decorator()
def make_api_call(client, messages, model):
    return client.chat.completions.create(
        messages=messages,
        model=model,
        stream=False,
    )

def summarize(source_text):
    client = openai.OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    messages = [
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
    ]
    chat_completion = make_api_call(client, messages, MODEL_NAME)
    return chat_completion.choices[0].message.content

def qgen(source_text):
    client = openai.OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    messages = [
        {
            "role": "system",
            "content": "Respond with a list of 10 questions. The text in the user message must contain specific answers to each question. Each question must be on its own line. Just list the questions without any introductory text or numbers.",
        },
        {
            "role": "user",
            "content": source_text,
        }
    ]
    chat_completion = make_api_call(client, messages, MODEL_NAME)
    return chat_completion.choices[0].message.content

def agen(source_text, question):
    client = openai.OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    messages = [
        {
            "role": "system",
            "content": "Give a comprehensive and well-reasoned answer to the user question strictly based on the context below and try to give a detailed explanation while answering the questions. Also try to add some bonus tip to in each answer and some relevant example outside of the content.\n" + source_text
        },
        {
            "role": "user",
            "content": question,
        }
    ]
    chat_completion = make_api_call(client, messages, MODEL_NAME)
    return chat_completion.choices[0].message.content

def main():
    input_path = r"C:\Users\91745\OneDrive\Desktop\Github_analyser\output\local_repo\docs\wasmedge_docs.csv"
    output_path = r"C:\Users\91745\OneDrive\Desktop\Github_analyser\output\local_repo\summary\wasmedge_docs_2.csv"
    processed_contents = set()
    output_file_exists = os.path.exists(output_path)

    row_count = 0

    with open(input_path, 'r', newline='', encoding='utf-8') as infile, \
         open(output_path, 'a', newline='', encoding='utf-8') as outfile:

        csv_reader = csv.reader(infile)
        csv_writer = csv.writer(outfile)

        if not output_file_exists:
            pass 

        for row in csv_reader:
            try:
                main_content = row[0]

                if main_content in processed_contents:
                    continue  

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
                print(f"Processed row {row_count}")

            except Exception as e:
                print(f"Error processing row {row_count + 1}: {str(e)}")
                continue

    print(f"Modified data has been written to {output_path}")
    print(f"Total rows summarized: {row_count}")

if __name__ == "__main__":
    main()