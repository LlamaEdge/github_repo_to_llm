import csv
import os

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
                new_content = f"The following is a markdown document located at {path}\n------\n{content}\n------"
            elif extension == '.rs':
                new_content = f"```rust:{path}\n{content}\n```"
            elif extension == '.sh':
                new_content = f"```bash:{path}\n{content}\n```"
            elif extension == '.py':
                new_content = f"```python:{path}\n{content}\n```"
            elif extension == '.js':
                new_content = f"```javascript:{path}\n{content}\n```"
            elif extension == '.json':
                new_content = f"```json:{path}\n{content}\n```"
            elif extension == '.txt':
                new_content = f"The following is a plain text file located at {path}\n------\n{content}\n------"
            elif extension == '.toml':
                new_content = f"```toml:{path}\n{content}\n```"
            elif extension == '.jsx':
                new_content = f"```jsx:{path}\n{content}\n```"
            elif extension == '.css':
                new_content = f"```css:{path}\n{content}\n```"
            else:
                new_content = f"The following document is located at {path}\n------\n{content}\n------"
            writer.writerow([new_content])

if __name__ == "__main__":
    input_file = input("Enter the path of your text file: ")
    final_output_csv = "transformed_repopack_llamaedge.csv"
    parsed_data = parse_text_file(input_file)
    transform_and_write_csv(parsed_data, final_output_csv)
    print(f"Transformed CSV file '{final_output_csv}' generated successfully.")
