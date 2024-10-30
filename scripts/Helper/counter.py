import pandas as pd

# Read the CSV, forcing it into a single column by specifying an unusual separator
df = pd.read_csv(r'C:\Users\91745\OneDrive\Desktop\Github_analyser\output\local_repo\final_repo\llamaedge_repopack.csv', sep='\n', header=None)

# Rename the column to 'Content'
df.columns = ['Content']

# Define the word count function
def count_words(text):
    if isinstance(text, str):
        return len(text.split())
    else:
        return 0

# Apply the word count function and add the result as a new column
df['Content_Word_Count'] = df['Content'].apply(count_words)

# Write to a new CSV without headers
df.to_csv('wasmedge_quickjs.csv', index=False, header=False)




'''
import pandas as pd
from transformers import AutoModel

model = AutoModel.from_pretrained("Xenova/gpt-4")

tokenizer = GPT2TokenizerFast.from_pretrained('Xenova/gpt-4')


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