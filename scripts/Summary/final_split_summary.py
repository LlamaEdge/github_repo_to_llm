import openai
import csv
import os

API_BASE_URL = "https://llama.us.gaianet.network/v1"
MODEL_NAME = "llama"
API_KEY = "not_now"

def summarize(source_text):
    client = openai.OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Respond with a comprehensive summary of the text or the code provided in the user message",
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

def qgen(source_text):
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

def agen(source_text, question):
    client = openai.OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Give a comprehensive and well-reasoned answer to the user question strictly based on the context below and try to give a detailed explanation while answering the questions. Also try to add some bonus tip to in each answer and some relevant example outside of the content.\n" + source_text,
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

def main():
    input_path = "/home/aru/Desktop/Github_analyser/Output/main_repos/wasmedge_all.csv"
    output_path = "/home/aru/Desktop/Github_analyser/Output/main_repos/wasmedge_all_split.csv"

    processed_contents = set()
    output_file_exists = os.path.exists(output_path)
    if output_file_exists:
        with open(output_path, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                processed_contents.add(row['Content'])
    else:
        pass

    row_count = 0

    with open(input_path, 'r', newline='', encoding='utf-8') as csvfile_in, \
         open(output_path, 'a', newline='', encoding='utf-8') as csvfile_out:

        csv_reader = csv.DictReader(csvfile_in)
        fieldnames = ["Content", "Summary and Q&A"]
        writer = csv.DictWriter(csvfile_out, fieldnames=fieldnames)

        if not output_file_exists:
            writer.writeheader()

        for row in csv_reader:
            main_content = row['Content']

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

            writer.writerow({"Content": main_content, "Summary and Q&A": f"Summary:\n{summary}"})
            for qna in qna_list:
                writer.writerow({"Content": main_content, "Summary and Q&A": qna})
            processed_contents.add(main_content)

            row_count += 1
            print(f"Processed row {row_count}")

    print(f"Modified data has been written to {output_path}")
    print(f"Total rows summarized: {row_count}")

if __name__ == "__main__":
    main()
