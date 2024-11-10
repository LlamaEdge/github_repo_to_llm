import anthropic
import csv
import os
from typing import List, Dict

class ClaudeSummarizer:
    def __init__(self, api_key: str): 
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"
        self.max_tokens = 8000
        self.temperature = 0

    def summarize(self, source_text: str) -> str:
        message = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system="""
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
            system="Respond with a list of 10 questions. The text in the user message must contain specific answers to each question. Each question must be on its own line. Just list the questions without any introductory text or numbers.",
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
            Give a comprehensive and well-reasoned answer to the user question strictly based on the context below 
            and try to give a detailed explanation while answering the questions. Also try to add some bonus tip to 
            each answer and some relevant example outside of the content.

            Context:
            {source_text}
            """,
            messages=[
                {"role": "user", "content": question}
            ]
        )
        return message.content[0].text

def main():
    input_path = r"C:\Users\91745\OneDrive\Desktop\Github_analyser\test_in.csv"
    output_path = r"C:\Users\91745\OneDrive\Desktop\Github_analyser\test_out.csv"
    
    api_key = "sk-ant-"
    
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

        csv_reader = csv.DictReader(csvfile_in)
        fieldnames = ["Content", "Summary and Q&A"]
        writer = csv.DictWriter(csvfile_out, fieldnames=fieldnames)

        if not output_file_exists:
            writer.writeheader()

        for row in csv_reader:
            main_content = row['Content']

            if main_content in processed_contents:
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