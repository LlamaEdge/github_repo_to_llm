import csv
import os
import sys

csv.field_size_limit(10**9)

def parse_text_file(input_file):
    data = []
    current_path = None
    current_content = []

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    inside_file_block = False

    for line in lines:
        if line.strip() == '================':
            if inside_file_block and current_path and current_content:
                data.append({
                    "Path": current_path.strip(),
                    "Content": ''.join(current_content).strip()
                })
                current_path = None
                current_content = []
                inside_file_block = False
        elif line.startswith('File:'):
            current_path = line.split('File: ')[1].strip()
            inside_file_block = True
        else:
            if inside_file_block:
                current_content.append(line)

    if current_path and current_content:
        data.append({
            "Path": current_path.strip(),
            "Content": ''.join(current_content).strip()
        })
    return data

def transform_and_write_csv(data, output_csv):
    with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        for row in data:
            path = row['Path']
            content = row['Content']
            extension = os.path.splitext(path)[1]

            if extension == '.md':
                formatted_content = f"The following is a markdown document located at {path}\n------\n{content}\n------"
            elif extension == '.rs':
                formatted_content = f"```rust:{path}\n{content}\n```"
            elif extension == '.sh':
                formatted_content = f"```bash:{path}\n{content}\n```"
            elif extension == '.py':
                formatted_content = f"```python:{path}\n{content}\n```"
            elif extension == '.js':
                formatted_content = f"```javascript:{path}\n{content}\n```"
            elif extension == '.json':
                formatted_content = f"```json:{path}\n{content}\n```"
            elif extension == '.txt':
                formatted_content = f"The following is a plain text file located at {path}\n------\n{content}\n------"
            elif extension == '.toml':
                formatted_content = f"```toml:{path}\n{content}\n```"
            elif extension == '.jsx':
                formatted_content = f"```jsx:{path}\n{content}\n```"
            elif extension == '.css':
                formatted_content = f"```css:{path}\n{content}\n```"
            elif extension == '.java':
                formatted_content = f"```java:{path}\n{content}\n```"
            elif extension == '.hpp':
                formatted_content = f"```hpp:{path}\n{content}\n```"
            elif extension == '.c':
                formatted_content = f"```c:{path}\n{content}\n```"
            elif extension == '.yml':
                formatted_content = f"```yml:{path}\n{content}\n```"
            elif extension == '.xml':
                formatted_content = f"```xml:{path}\n{content}\n```"
            else:
                formatted_content = f"The following document is located at {path}\n------\n{content}\n------"
            writer.writerow([formatted_content])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_text_file> <output_csv_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    parsed_data = parse_text_file(input_file)
    transform_and_write_csv(parsed_data, output_file)
    print(f"Transformed CSV file '{output_file}' generated successfully.")
