# CSV Summarizer and Q&A Generator

This folder contains Python scripts that process CSV files to generate summaries and Q&A pairs based on the provided content. Each script uses a different API for processing, offering flexibility and compatibility with various platforms.

---

## 1. **`summarizer_gaia.py`**

### Description:
- This script utilizes the **GaiaNet API** (based on public endpoints from gaianet) to process CSV rows. 
- It generates:
  - Summaries for the content.
  - Questions based on the content.
  - Comprehensive answers to the generated questions.
  
### Key Features:
- Built-in retry mechanism for handling API timeouts or errors.
- Skips rows that exceed size limits or have already been processed.

### Usage:
```bash
python summarizer_gaia.py <input_csv> <output_csv>
```

### Parameters:
- `<input_csv>`: Path to the input CSV file containing the content to process.
- `<output_csv>`: Path to the output CSV file where the results will be saved.

---

## 2. **`summarizer_openai.py`**

### Description:
- This script leverages the **OpenAI API** (e.g., GPT-3.5, GPT-4) for processing.
- Similar functionality to `summarizer_gaia.py`, including:
  - Summaries.
  - Question generation.
  - Answer generation.

### Usage:
```bash
python summarizer_openai.py <input_csv> <output_csv>
```

### Parameters:
- `<input_csv>`: Path to the input CSV file containing the content to process.
- `<output_csv>`: Path to the output CSV file where the results will be saved.

---

## 3. **`summarizer_claude.py`**

### Description:
- This script uses the **Claude API** for processing content.
- Features:
  - Generates concise summaries.
  - Creates relevant questions and answers.
  - Ideal for workflows requiring Claude's specific strengths.

### Usage:
```bash
python summarizer_claude.py <input_csv> <output_csv>
```

### Parameters:
- `<input_csv>`: Path to the input CSV file containing the content to process.
- `<output_csv>`: Path to the output CSV file where the results will be saved.

---

## Common Notes

1. **Requirements**:
   - Python 3.7 or above.
   - Required Python libraries:
     - `openai`, `csv`, `tenacity`, `os`, `sys`, `logging`, `time`.

2. **General Execution**:
   - Each script automatically skips rows that:
     - Exceed the character limit (e.g., 32,000 characters).
     - Have already been processed (to avoid duplicates).

3. **API Configuration**:
   - Ensure your API keys are correctly set up in the script for each corresponding API:
     - GaiaNet: Set `API_BASE_URL`, `MODEL_NAME`, and `API_KEY`.
     - OpenAI: Replace with your OpenAI API key.
     - Claude: Configure your API access.

4. **Interrupt Handling**:
   - The scripts save progress in real-time to avoid data loss in case of interruptions.

5. **Individual Operation Scripts**:  
   - Separate scripts are available to run a single operation, such as generating only summaries or only Q&A pairs.

---

Feel free to use these scripts based on your API preferences and processing requirements. 
Try generating summaries and qna pairs by using different prompts for various use cases. If you encounter any issues or need assistance, open an issue.

---