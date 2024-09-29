1. code_summarizer.py takes input from output folder a csv that has path and content as summarizes it and create a new csv containing content and summary as headers.

2. qna.py generates a new summary file from the above summary file that can be used to generate multiple vector embeddings from 1 file only.

3. openai_summary.py combines the above 2 step and directly generates the summary file from the raw CSV file but it uses openai api.

4. final_split_summary.py also does the similar function but it uses gaianet endpoints instead of openai api.

The key difference between the above 2 files is the use of APIs from open source models and proprietary models