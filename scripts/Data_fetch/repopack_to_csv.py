import csv

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

def write_to_csv(data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Path', 'Content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    input_file = input("Enter the path of your text file: ")
    output_file = "repopack_llamaedge.csv"
    parsed_data = parse_text_file(input_file)
    write_to_csv(parsed_data, output_file)
    print(f"CSV file '{output_file}' generated successfully.")


'''
The above script do not consider header files that contain file structure etc.
to_do function for headers
for line in lines:
        # Check for delimiter to separate file blocks
        if line.strip() == '================================================================':
            if inside_file_block and current_path and current_content:
                # Save the current file block
                data.append({
                    "Path": current_path.strip(),
                    "Content": ''.join(current_content).strip()
                })
                current_path = None
                current_content = []
                inside_file_block = False
        else:
            # Treat any text between two delimiters as the file path
            if not inside_file_block and not current_path:
                current_path = line.strip()  # Capture the path
                inside_file_block = True
            elif inside_file_block:
                current_content.append(line)
'''