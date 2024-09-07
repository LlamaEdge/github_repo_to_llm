import openai
import csv
import sys

API_BASE_URL = "https://llama.us.gaianet.network/v1"
MODEL_NAME = "llama"
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
    return response.choices[0].message.content

def qgen(source_text):
    """Generate 5 to 10 questions based on the code/content."""
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an expert software engineer. Generate a list of 5 to 10 insightful questions based on the following code or content. Each question must be self-contained and specific to the provided content.Just list the questions without any introductory text or numbers",
            },
            {
                "role": "user",
                "content": source_text,
            }
        ],
        model=MODEL_NAME,
        stream=False,
    )
    return response.choices[0].message.content

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
    return response.choices[0].message.content

def main():
    results = []
    arguments = sys.argv[1:]

    # Open the input CSV file (containing Path and Content)
    with open(arguments[0], 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        
        for row in csv_reader:
            print(f"Processing {row['Path']}")

            # Generate Summary for the code/content
            summary = summarize(row['Content'])
            questions = qgen(row['Content']).splitlines()

            # Generate Q&A pairs
            for q in questions:
                if len(q.strip()) == 0:
                    continue
                answer = agen(row['Content'], q)

                # Append the Summary, Question, and Answer to the result
                results.append({
                    "Summary": summary,
                    "Question": q,
                    "Answer": answer
                })

    # Write the results to the output CSV file (with Summary, Question, and Answer columns)
    with open(arguments[1], 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Summary', 'Question', 'Answer']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in results:
            writer.writerow(row)

if __name__ == "__main__":
    main()
