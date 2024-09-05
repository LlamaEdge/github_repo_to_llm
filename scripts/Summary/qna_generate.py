import pandas as pd
import openai
import logging
import time

logging.basicConfig(level=logging.ERROR)

API_BASE_URL = "https://llama.us.gaianet.network/v1"
MODEL_NAME = "llama"
API_KEY = "GAIA"

client = openai.OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def generate_qna(text, summary):
    try:
        start_time = time.time()
        combined_text = f"Content: {text}\n\nSummary: {summary}"
        
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in analyzing complex information. Based on the provided content and summary, generate 3-5 insightful questions and provide brief, informative answers. Format the output as: Question: [question text] Answer: [answer text]."
                },
                {
                    "role": "user",
                    "content": combined_text,
                }
            ],
            model=MODEL_NAME,
            stream=False,
        )
        
        raw_content = response.choices[0].message.content.strip()

        # Capture QnA pairs
        return raw_content
    except Exception as e:
        logging.error(f"Error in generating Q&A: {e}")
        return "Error: Could not generate Q&A"

def generate_qna_csv(input_csv_file, output_csv_file):
    try:
        df = pd.read_csv(input_csv_file)
        
        if 'Content' not in df.columns or 'Summary' not in df.columns:
            raise ValueError("'Content' or 'Summary' column not found in the input CSV file.")
        
        df['QnA'] = df.apply(lambda row: generate_qna(row['Content'], row['Summary']) if pd.notnull(row['Content']) else "", axis=1)

        # Save the new DataFrame with the QnA column
        df.to_csv(output_csv_file, index=False)
    except Exception as e:
        logging.error(f"Error processing CSV: {e}")

if __name__ == "__main__":
    input_csv_file = r"C:\Users\91745\OneDrive\Desktop\Github_analyser\Output\repo_Codes_summary_gemma.csv"  
    output_csv_file = r"C:\Users\91745\OneDrive\Desktop\Github_analyser\Output\repo_Codes_summary_gemma_qna.csv"  
    generate_qna_csv(input_csv_file, output_csv_file)
