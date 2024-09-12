import openai
import csv
import sys
import os

API_BASE_URL = "https://llama.us.gaianet.network/v1"
MODEL_NAME = "llama"
API_KEY = "GAIA"

def summarize(source_text):
    client = openai.OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Respond with a comprehensive summary of the text in the user message",
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
                "content": "Respond with a list of 10 questions. The text in the user message must contain specific answers to each question. Each question must be complete without references to unclear context such as 'this team' or 'that lab'. Each question must be on its own line. Just list the questions without any introductory text or numbers.",
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
                "content": "Give a comprehensive and well-reasoned answer to the user question strictly based on the context below.\n" + source_text,
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
    results = []
    input_path = "C:\\Users\\91745\\OneDrive\\Desktop\\Github_analyser\\Output\\repo_Codes.csv"
    output_path = "C:\\Users\\91745\\OneDrive\\Desktop\\Github_analyser\\Output\\repo_Codes_test_merge.csv"

    with open(input_path, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)  # Use DictReader to access columns by name
        for row in csv_reader:
            main_content = row['Content']  # Use 'Content' column

            # Summarize the content
            summary = summarize(main_content)

            # Generate questions based on the content
            qs = qgen(main_content)
            qna_list = []
            for q in qs.splitlines():
                if len(q.strip()) == 0:
                    continue
                answer = agen(main_content, q)
                qna_list.append(f"Q: {q}\nA: {answer}")

            # Combine summary and QnA into one string
            summary_and_qna = f"Summary:\n{summary}\n\nQuestions and Answers:\n" + "\n\n".join(qna_list)

            # Append the result with main content in one column and summary with Q&A in another
            results.append([main_content, summary_and_qna])

    # Write results to the output CSV file
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Main Content", "Summary and Q&A"])  # Header row
        writer.writerows(results)

if __name__ == "__main__":
    main()
