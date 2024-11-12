import csv
import os
import sys
import argparse 
csv.field_size_limit(10**9) 

parser = argparse.ArgumentParser(description='Transform CSV content with formatting based on file extensions')
parser.add_argument('input_csv', help='Path to input CSV file')
parser.add_argument('output_csv', help='Path to output CSV file')

args = parser.parse_args()

input_csv = args.input_csv
output_csv = args.output_csv
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
