import openai
import csv
import sys
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_BASE_URL = "https://llama.us.gaianet.network/v1"
MODEL_NAME = "llama"
API_KEY = "GAIA"

client = openai.OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def qgen(source_text):
    try:
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
    except Exception as e:
        logging.error(f"Error in generating questions: {e}")
        return None

def agen(source_text, question):
    try:
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
    except Exception as e:
        logging.error(f"Error in generating answer: {e}")
        return None

def process_csv(input_csv, output_csv):
    results = []
    processed_contents = set()

    if os.path.exists(output_csv):
        with open(output_csv, 'r', newline='', encoding='utf-8') as outfile:
            reader = csv.reader(outfile)
            for row in reader:
                processed_contents.add(row[0]) 

    try:
        with open(input_csv, 'r', newline='', encoding='utf-8') as csvfile_in, \
             open(output_csv, 'a', newline='', encoding='utf-8') as csvfile_out:

            csv_reader = csv.DictReader(csvfile_in)
            fieldnames = ['Content', 'Summary and Q&A']
            writer = csv.DictWriter(csvfile_out, fieldnames=fieldnames)

            if not os.path.exists(output_csv) or os.stat(output_csv).st_size == 0:
                writer.writeheader()  

            for row in csv_reader:
                main_content = row['Content']
                summary = row['Summary']

                if main_content in processed_contents:
                    logging.info(f"Skipping already processed content: {main_content}")
                    continue

                questions = qgen(main_content)
                if questions is None:
                    logging.error(f"Skipping content due to question generation failure: {main_content}")
                    continue

                question_list = questions.splitlines()
                result = [{"Content": main_content, "Summary and Q&A": f"Summary:\n{summary}"}]
                
                for question in question_list:
                    if len(question.strip()) == 0:
                        continue
                    answer = agen(main_content, question)
                    if answer is None:
                        logging.error(f"Skipping question due to answer generation failure: {question}")
                        continue
                    result.append({"Content": main_content, "Summary and Q&A": f"Q: {question}\nA: {answer}"})

                for res in result:
                    writer.writerow(res)
                    csvfile_out.flush() 

                logging.info(f"Processed and saved content: {main_content}")

    except Exception as e:
        logging.error(f"Error processing CSV: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        logging.error("Usage: python script.py <input_csv> <output_csv>")
        sys.exit(1)

    input_csv_file = sys.argv[1]
    output_csv_file = sys.argv[2]

    process_csv(input_csv_file, output_csv_file)
