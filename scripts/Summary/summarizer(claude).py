import anthropic
import csv
import os
import sys
import logging
from typing import List, Dict
import csv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import time

csv.field_size_limit(10**9)

class ClaudeSummarizer:
    def __init__(self, api_key: str): 
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"
        self.max_tokens = 8192
        self.temperature = 0

    def summarize(self, source_text: str) -> str:
        message = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system="""
            You are an expert coding assistant. Analyze the files in a repository and provide a precise, concise summary of each code or markdown file. Focus on:

            Core Functionality: Explain the purpose of the file and its key features.
            Libraries Used: Highlight the libraries, frameworks, or dependencies used and their role.
            Functions, Classes, and Methods: Describe important functions, classes, or methods, including their parameters and usage.
            Applications: Suggest potential use cases or scenarios where the code can be applied.
            Code Suggestions: Provide a simple example or recommendation for integrating or extending the script in a real-world application.
            Ensure the summary is clear, structured, and actionable for developers.
            """,
            messages=[
                {"role": "user", "content": source_text}
            ]
        )
        return message.content[0].text

    def generate_questions(self, source_text: str) -> List[str]:
        message = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=
            """
            List 10 concise, insightful questions to improve the usability of the code for developers. 
            Each question should focus on clarity, functionality, and real-world application, with each question on its own line. 
            Do not include introductory text, numbers, or extra formatting.
            """,
            messages=[
                {"role": "user", "content": source_text}
            ]
        )
        return message.content[0].text.strip().split('\n')

    def generate_answer(self, source_text: str, question: str) -> str:
        message = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=f"""
            Provide a detailed and well-reasoned answer to the user’s question based strictly on the given context.
            Ensure the explanation is comprehensive, clear, and informative.
            Include a bonus tip for added value and provide a relevant example beyond the context to enhance understanding.
            Context:
            {source_text}
            """,
            messages=[
                {"role": "user", "content": question}
            ]
        )
        return message.content[0].text


def main():
    if len(sys.argv) != 3:
        logging.error("Usage: python summarizer(claude).py <input_csv> <output_csv>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    api_key = "sk-"  # Replace with your actual API key
    summarizer = ClaudeSummarizer(api_key)
    
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

        csv_reader = csv.reader(csvfile_in) 
        fieldnames = ["Content", "Summary and Q&A"]
        writer = csv.DictWriter(csvfile_out, fieldnames=fieldnames)

        if not output_file_exists:
            writer.writeheader()

        for row in csv_reader:
            if not row: 
                continue

            main_content = row[0] 
            if len(main_content) > 32000:
                print(f"Skipping row {row_count + 1} due to content length exceeding 32000 characters.")
                continue

            if main_content in processed_contents:
                print(f"Skipping row as content has already been processed.")
                continue

            try:
                summary = summarizer.summarize(main_content)
                if summary.strip():
                    writer.writerow({
                        "Content": main_content,
                        "Summary and Q&A": f"Summary:\n{summary}"
                    })

                questions = summarizer.generate_questions(main_content)
                for question in questions:
                    if question.strip():
                        answer = summarizer.generate_answer(main_content, question)
                        if answer.strip():
                            writer.writerow({
                                "Content": main_content,
                                "Summary and Q&A": f"Q: {question}\nA: {answer}"
                            })

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
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

