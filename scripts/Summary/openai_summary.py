import csv
import os
import openai
from openai import OpenAI
client = OpenAI(api_key='')
MODEL_NAME = "gpt-4o"

def summarize(source_text):
    chat_completion = client.chat.completions.create(model=MODEL_NAME,
    messages=[
        {
            "role": "system",
            "content": "Respond with a comprehensive summary of the text or the code provided in the user message",
        },
        {
            "role": "user",
            "content": source_text,
        }
    ])
    return chat_completion.choices[0].message.content

def qgen(source_text):
    chat_completion = client.chat.completions.create(model=MODEL_NAME,
    messages=[
        {
            "role": "system",
            "content": "Respond with a list of 10 questions. The text in the user message must contain specific answers to each question. Each question must be on its own line. Just list the questions without any introductory text or numbers.",
        },
        {
            "role": "user",
            "content": source_text,
        }
    ])
    return chat_completion.choices[0].message.content

def agen(source_text, question):
    chat_completion = client.chat.completions.create(model=MODEL_NAME,
    messages=[
        {
            "role": "system",
            "content": (
                "Give a comprehensive and well-reasoned answer to the user question strictly based on the context below "
                "and try to give a detailed explanation while answering the questions. Also try to add some bonus tip to "
                "each answer and some relevant example outside of the content.\n\nContext:\n" + source_text
            ),
        },
        {
            "role": "user",
            "content": question,
        }
    ])
    return chat_completion.choices[0].message.content

def main():
    input_path = r"C:\Users\91745\OneDrive\Desktop\Github_analyser\Output\main_repos\gaianet_md_2.csv"
    output_path = r"C:\Users\91745\OneDrive\Desktop\Github_analyser\Output\split_summary\gaianet_split.csv"
    processed_contents = set()
    output_file_exists = os.path.exists(output_path)

    if output_file_exists:
        with open(output_path, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                processed_contents.add(row['Content'])

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

            if summary.strip():
                writer.writerow({"Content": main_content, "Summary and Q&A": f"Summary:\n{summary}"})

            for q in qs.strip().split('\n'):
                if q.strip():
                    answer = agen(main_content, q)
                    if answer.strip():
                        writer.writerow({"Content": main_content, "Summary and Q&A": f"Q: {q}\nA: {answer}"})

            processed_contents.add(main_content)
            row_count += 1
            print(f"Processed row {row_count}")

    print(f"Modified data has been written to {output_path}")
    print(f"Total rows summarized: {row_count}")

if __name__ == "__main__":
    main()
