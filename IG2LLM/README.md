# IG Core Component Extraction and Evaluation

This project provides a test suite to extract components from regulative and constitutive statements at the IG Core level (Institutional Grammar 2.0) using Large Language Models (LLMs). It supports running extraction experiments, aggregating multiple runs, and computing detailed evaluation metrics.

## Features
- Prompt templates for both regulative and constitutive statements, with optional examples
- CSV to JSON conversion for labeled data
- LLM interface supporting OpenAI, DeepSeek, Gemini, and Claude
- Aggregation of multiple LLM runs to consolidate component extraction
- Component-level and aggregate metrics computation with bootstrap confidence intervals
- Command-line interface for end-to-end experiments

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```
2. Install Python 3.8+ dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Create a `.env` file in the project root to store your API keys:
   ```bash
   OPENAI_API_KEY=your_openai_key
   DEEPSEEK_API_KEY=your_deepseek_key
   GEMINI_API_KEY=your_gemini_key
   ANTHROPIC_API_KEY=your_anthropic_key
   ```

## Data Preparation
1. Create a `data/` directory at the project root.
2. Place your CSV files named in the format:
   ```text
   {difficulty}_{statement_type}_statements.csv
   ```
   - `difficulty`: `easy`, `medium`, or `hard`
   - `statement_type`: `regulative` or `constitutive`
3. Each CSV must have headers:
   ```text
   "Input","Output",
   "Raw text","Coded text",
   ```
   where `Output` contains ground-truth component annotations, e.g., `A(commission) D(shall) I(optimize) ...`.

## Usage
Run the main evaluation script:
```bash
python evaluate.py \
  --runs <N> \
  --type [r|c] \
  --level [1|2|3] \
  [--examples] \
  [--provider openai|deepseek|gemini|claude]
```

Arguments:
- `--runs`: Number of LLM runs per statement (default: 1)
- `--type`: `r` for regulative, `c` for constitutive
- `--level`: `1` (easy), `2` (medium), `3` (hard)
- `--examples`: Include in-context examples in the prompt
- `--provider`: LLM provider (default: `openai`)

Results:
- Output JSON files are saved in the `results/` directory, named as:
  ```text
  <provider>_<difficulty>_<statement_type>_statements[_with_examples]_results.json
  ```
- Evaluation metrics (precision, recall, F1, confidence intervals) are printed to the console.

## Utilities
- **CSV to JSON Conversion**: `util/convert_to_json.py` for standalone conversion:
  ```bash
  python util/convert_to_json.py <input.csv> <regulative|constitutive> [--classification]
  ```
- **Result Aggregation**: `util/aggregation.aggregate_results` to merge multiple runs into consolidated predictions.

## Project Structure
```
.  
├── evaluate.py               
├── prompt_templates/         
├── prompts/                  
├── model/                    
├── util/                     
├── metrics/                 
├── services/                 
├── tests/                    
└── requirements.txt
```