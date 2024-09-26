import pandas as pd

file_path = '/home/aru/Desktop/Github_analyser/Output/split_summary/wasmedge_split.csv' 
df = pd.read_csv(file_path)

df_cleaned = df.dropna(subset=['Content'])

output_file_path = '/home/aru/Desktop/Github_analyser/Output/split_summary/wasmedge_split_cleam.csv'  
df_cleaned.to_csv(output_file_path, index=False)

print("Rows with empty 'Content' have been removed.")
