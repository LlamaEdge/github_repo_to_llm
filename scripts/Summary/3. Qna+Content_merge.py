import csv

def merge_content_summary_qna(content_csv, summary_qna_csv, output_csv):
    content_rows = []
    with open(content_csv, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            content_rows.append(row['Content'])

    summary_qna_rows = []
    with open(summary_qna_csv, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            summary = row['Summary'].strip()
            qna = row['QnA'].strip()
            combined = f"Summary:\n{summary}\n\nQnA:\n{qna}"
            summary_qna_rows.append(combined)

    if len(content_rows) != len(summary_qna_rows):
        print("Error: The number of rows in content CSV and summary+qna CSV do not match.")
        return

    merged_results = []
    for content, summary_qna in zip(content_rows, summary_qna_rows):
        merged_results.append({
            'Content': content,
            'Summary+QnA': summary_qna
        })

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Content', 'Summary+QnA']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in merged_results:
            writer.writerow(row)

content_csv = ''  # Replace with your content CSV file path
summary_qna_csv = ''  # Replace with your summary+qna CSV file path
output_csv = ''  # Replace with your output CSV file path

merge_content_summary_qna(content_csv, summary_qna_csv, output_csv)
