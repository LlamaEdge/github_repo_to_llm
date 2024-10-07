import csv

input_csv = r''
output_csv = r''


with open(input_csv, mode='r', newline='', encoding='utf-8') as infile, \
     open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    
    for row in reader:
        path = row['Path']
        content = row['Content']
        
        new_content = f"language: {path}\n{content}"
        writer.writerow([new_content])

print(f"Transformed CSV has been written to {output_csv}")
