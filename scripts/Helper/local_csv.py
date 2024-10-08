import csv
import os
import sys

csv.field_size_limit(10**9) 

input_csv = r''
output_csv = r''

with open(input_csv, mode='r', newline='', encoding='utf-8') as infile, \
     open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    
    for row in reader:
        path = row['Path']
        content = row['Content']
        extension = os.path.splitext(path)[1]
        if extension == '.md':
            new_content = f"The following is a markdown document located at {path}\n------\n{content}\n------"
        elif extension == '.rs':
            new_content = f"```rust:{path}\n{content}\n```"
        elif extension == '.sh':
            new_content = f"```bash:{path}\n{content}\n```"
        elif extension == '.py':
            new_content = f"```python:{path}\n{content}\n```"
        else:
            new_content = new_content = f"The following document is located at {path}\n------\n{content}\n------"
        writer.writerow([new_content])
print(f"Transformed CSV has been written to {output_csv}")
