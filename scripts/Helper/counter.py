import pandas as pd
import argparse

def count_words(text):
    if isinstance(text, str):
        return len(text.split())
    else:
        return 0

def main():
    parser = argparse.ArgumentParser(description='Count words in a CSV file')
    parser.add_argument('input_path', help='Path to input CSV file')
    parser.add_argument('output_path', help='Path to output CSV file')
    
    args = parser.parse_args()

    df = pd.read_csv(args.input_path, sep='\n', header=None)
    df.columns = ['Content']
   
    df['Content_Word_Count'] = df['Content'].apply(count_words)

    df.to_csv(args.output_path, index=False, header=False)

if __name__ == '__main__':
    main()



'''
import pandas as pd
from transformers import AutoModel

model = AutoModel.from_pretrained("Xenova/gpt-3.5")

tokenizer = GPT2TokenizerFast.from_pretrained('Xenova/gpt-3.5')


df = pd.read_csv('/home/aru/Desktop/Github_analyser/Output/summary/eth_md_summary.csv')

def count_words(text):
    return len(text.split())

def count_tokens(text):
    tokens = tokenizer.encode(text)
    return len(tokens)

df['Content_Word_Count'] = df['Content'].apply(count_words)
df['Summary_QnA_Word_Count'] = df['Summary and Q&A'].apply(count_words)

df['Content_Token_Count'] = df['Content'].apply(count_tokens)
df['Summary_QnA_Token_Count'] = df['Summary and Q&A'].apply(count_tokens)

df.to_csv('output_file.csv', index=False)
'''