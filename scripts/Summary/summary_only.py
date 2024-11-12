import pandas as pd
import openai
import logging
import time
import sys

logging.basicConfig(level=logging.INFO)

API_BASE_URL = "https://llama.us.gaianet.network/v1"
MODEL_NAME = "llama"
API_KEY = "GAIA"

client = openai.OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def summarize_code(code, path):
    try:
        start_time = time.time()
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert software engineer. Your task is to analyze the provided code and generate a concise, coherent summary that captures the purpose, functionality, and key components of the code. Additionally, highlight any potential issues or areas for improvement."
                },
                {
                    "role": "user",
                    "content": f"Code from {path}:\n\n{code}",
                }
            ],
            model=MODEL_NAME,
            stream=False,
        )
        logging.info(f"API call took {time.time() - start_time} seconds.")
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error in summarizing code: {e}")
        return "Error: Could not summarize"
    

def summarize_csv_content(input_csv_file, output_csv_file):
    try:
        df = pd.read_csv(input_csv_file)
        if 'Content' not in df.columns or 'Path' not in df.columns:
            raise ValueError("'Content' or 'Path' column not found in the input CSV file.")

        logging.info("Starting summarization...")
        df['Summary'] = df.apply(lambda row: summarize_code(row['Content'], row['Path']) if pd.notnull(row['Content']) else "", axis=1)

        df.to_csv(output_csv_file, index=False)
        logging.info(f"Summaries have been generated and saved to {output_csv_file}")
    except Exception as e:
        logging.error(f"Error processing CSV: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        logging.error("Usage: python script.py <input_csv> <output_csv>")
        sys.exit(1)
    
    input_csv_file = sys.argv[1]
    output_csv_file = sys.argv[2]
    
    summarize_csv_content(input_csv_file, output_csv_file)