import pandas as pd

df = pd.read_csv('Output/summary/eth_md_summary.csv')
def truncate_content(content, max_tokens=7000):
    words = content.split()
    return ' '.join(words[:max_tokens])

df['Content'] = df['Content'].apply(lambda x: truncate_content(x))
df['Summary and Q&A'] = df['Summary and Q&A'].apply(lambda x: truncate_content(x))

df.to_csv('Output/summary/eth_md_summary_trun.csv', index=False)

'''
import pandas as pd

df = pd.read_csv('input_file.csv')

def split_content(row, max_words=5000):
    content = row['Content']
    words = content.split()
    chunks = [words[i:i + max_words] for i in range(0, len(words), max_words)]
    return [{'Path': row['Path'], 'Content': ' '.join(chunk)} for chunk in chunks]

new_rows = []

for index, row in df.iterrows():
    new_rows.extend(split_content(row))

new_df = pd.DataFrame(new_rows)

new_df.to_csv('output_file.csv', index=False)
'''