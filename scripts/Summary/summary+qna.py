import openai
import csv
import sys

API_BASE_URL = "https://phi.us.gaianet.network/v1"
MODEL_NAME = "phi"
API_KEY = "GAIA"

client = openai.OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def summarize(source_text):
    """Generate a summary for the provided code/content."""
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an expert software engineer. Summarize the following code or content in a concise manner, highlighting its purpose, key components, and any potential issues or improvements.",
            },
            {
                "role": "user",
                "content": source_text,
            }
        ],
        model=MODEL_NAME,
        stream=False,
    )
    return response.choices[0].message['content'].strip()

def qgen(source_text):
    """Generate 5 to 10 questions based on the code/content."""
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an expert software engineer. Generate a list of 5 to 10 insightful questions based on the following code or content. Each question must be self-contained and specific to the provided content. Just list the questions without any introductory text or numbers.",
            },
            {
                "role": "user",
                "content": source_text,
            }
        ],
        model=MODEL_NAME,
        stream=False,
    )
    return response.choices[0].message['content'].strip()

def agen(source_text, question):
    """Generate answers for each question based on the provided code/content."""
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"Provide a comprehensive answer to the following question based on the code or content provided:\n{source_text}",
            },
            {
                "role": "user",
                "content": question,
            }
        ],
        model=MODEL_NAME,
        stream=False,
    )
    return response.choices[0].message['content'].strip()

def main():
    results = []
    arguments = sys.argv[1:]

    with open(arguments[0], 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        
        for row in csv_reader:
            print(f"Processing {row['Path']}")

            # Get the summary
            summary = summarize(row['Content'])
            
            # Get the questions
            questions = qgen(row['Content']).splitlines()

            # Generate QnA
            qna_list = []
            for q in questions:
                if q.strip():
                    answer = agen(row['Content'], q)
                    qna_list.append(f"Q: {q}\nA: {answer}")

            # Combine summary and QnA
            qna_combined = f"Summary:\n{summary}\n\nQnA:\n" + "\n\n".join(qna_list)

            # Append to results
            results.append({
                "Content": row['Content'],
                "Summary and QnA": qna_combined
            })

    with open(arguments[1], 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Content', 'Summary and QnA']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in results:
            writer.writerow(row)

if __name__ == "__main__":
    main()
