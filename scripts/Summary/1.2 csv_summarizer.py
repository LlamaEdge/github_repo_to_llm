import pandas as pd
import openai
import logging
import time

logging.basicConfig(level=logging.INFO)

API_BASE_URL = "https://llama.us.gaianet.network/v1"
MODEL_NAME = "llama"
API_KEY = "GAIA"

client = openai.OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def summarize_text(content, page_number):
    try:
        start_time = time.time()
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert summarizer. Your task is to analyze the provided content from every row of a csv file and generate a concise, coherent summary that captures the key points, themes, and information from the text."
                },
                {
                    "role": "user",
                    "content": f"Page {page_number} content:\n\n{content}",
                }
            ],
            model=MODEL_NAME,
            stream=False,
        )
        logging.info(f"API call took {time.time() - start_time} seconds.")
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error in summarizing content: {e}")
        return "Error: Could not summarize"

def summarize_csv_content(input_csv_file, output_csv_file):
    try:
        df = pd.read_csv(input_csv_file)
        if 'Content' not in df.columns or 'Path' not in df.columns:
            raise ValueError("'Content' or 'Path' column not found in the input CSV file.")

        logging.info("Starting summarization...")
        df['Summary'] = df.apply(lambda row: summarize_text(row['Content'], row['Path']) if pd.notnull(row['Content']) else "", axis=1)

        df.to_csv(output_csv_file, index=False)
        logging.info(f"Summaries have been generated and saved to {output_csv_file}")
    except Exception as e:
        logging.error(f"Error processing CSV: {e}")

if __name__ == "__main__":
    input_csv_file = '/home/aru/Desktop/Github_analyser/Output/main_repos/llamaedge_all.csv'  
    output_csv_file = '/home/aru/Desktop/Github_analyser/Output/summary/llamaedge_summary.csv' 
    summarize_csv_content(input_csv_file, output_csv_file)
