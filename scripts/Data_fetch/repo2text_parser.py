import csv
import os

def parse_text_file(input_file):
    data = []
    current_path = None
    current_content = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for file start marker
        if line == '---' and i + 1 < len(lines) and 'File:' in lines[i + 1]:
            # If we have existing content, save it
            if current_path and current_content:
                data.append({
                    "Path": current_path,
                    "Content": ''.join(current_content)
                })
                current_content = []
            
            # Extract the new file path
            current_path = lines[i + 1].split('File:')[1].strip()
            i += 2  # Skip the File: line
            
            # Skip the closing '---' of the file header if it exists
            if i < len(lines) and lines[i].strip() == '---':
                i += 1
                
            continue
        
        # If we have a current path, collect all content including front matter
        if current_path:
            current_content.append(lines[i] + '\n')
        
        i += 1
    
    # Don't forget to add the last file
    if current_path and current_content:
        data.append({
            "Path": current_path,
            "Content": ''.join(current_content)
        })
    
    return data

def transform_and_write_csv(data, output_csv):
    with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        for row in data:
            path = row.get('Path')
            if not path:
                continue
                
            content = row.get('Content', '')
            extension = os.path.splitext(path)[1].lower()

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
            elif extension == '.java':
                new_content = f"```java:{path}\n{content}\n```"
            elif extension == '.hpp':
                new_content = f"```hpp:{path}\n{content}\n```"
            elif extension == '.c':
                new_content = f"```c:{path}\n{content}\n```"
            elif extension == '.yml':
                new_content = f"```yml:{path}\n{content}\n```"
            elif extension == '.xml':
                new_content = f"```xml:{path}\n{content}\n```"
            else:
                new_content = f"The following document is located at {path}\n------\n{content}\n------"
            writer.writerow([new_content])

if __name__ == "__main__":
    input_file = input("Enter the path of your text file: ")
    final_output_csv = "wasmedge.csv"
    parsed_data = parse_text_file(input_file)
    transform_and_write_csv(parsed_data, final_output_csv)
    print(f"Transformed CSV file '{final_output_csv}' generated successfully.")