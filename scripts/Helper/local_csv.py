import csv
import os
import sys


csv.field_size_limit(10**9) 

# Input and output file paths
input_csv = r'C:\Users\91745\OneDrive\Desktop\Github_analyser\output\local_repo\llamaedge.csv'
output_csv = r'C:\Users\91745\OneDrive\Desktop\Github_analyser\output\local_repo\llamaedge_merge.csv'


with open(input_csv, mode='r', newline='', encoding='utf-8') as infile, \
     open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    
    for row in reader:
        path = row['Path']
        content = row['Content']
        

        extension = os.path.splitext(path)[1]
        
        if extension == '.md':
            # Format for markdown files
            new_content = f"The following is a markdown document located at {path}\n------\n{content}\n------"
        elif extension == '.rs':
            # Format for Rust code files
            new_content = f"```rust:{path}\n{content}\n```"
        elif extension == '.sh':
            # Format for shell script files
            new_content = f"```bash:{path}\n{content}\n```"
        elif extension == '.py':
            # Format for Python files
            new_content = f"```python:{path}\n{content}\n```"
        else:
            new_content = f"language: {path}\n{content}"
        
        writer.writerow([new_content])

print(f"Transformed CSV has been written to {output_csv}")