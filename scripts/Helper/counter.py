import pandas as pd
df = pd.read_csv(r'C:\Users\91745\OneDrive\Desktop\Github_analyser\local_repo_formatted.csv', header=None)
df.columns = ['Content']
def count_words(text):
    if isinstance(text, str):
        return len(text.split())
    else:
        return 0   
df['Content_Word_Count'] = df['Content'].apply(count_words)
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