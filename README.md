# Persona-Driven Document Intelligence — Challenge 1B

This repository contains our submission for Round 1B of the **Persona-Driven Document Intelligence Hackathon**.

Our system is a **generic, fast, CPU-only pipeline** for extracting the most relevant sections and granular content from diverse PDF collections, based on a user’s **persona** and **job-to-be-done**. The solution meets all challenge constraints and works fully offline.

---

## Quick Start for Judges

**1. Build the Docker image (from project root):**

```bash
docker build -t adobe1b .
```

**2. Prepare your collections:**

* Place all your `Collection 1/`, `Collection 2/`, ... folders in the root directory.
* Each `Collection X` folder must have a `pdf/` subdirectory with input PDFs, and a `challenge1b_input.json` file.

**3. Run the container (Universal Command):**

```bash
docker run --rm -v "$(Get-Location):/app" -w /app adobe1b
```

* On Windows, use an absolute path or `%cd%` instead of `$PWD`.
* Output files (`challenge1b_output.json`) will be written into each `Collection X` folder.

---

## Approach Overview

### Section Extraction

* Uses **PyMuPDF** for layout-aware PDF parsing.
* Detects headings using font size, boldness, and spacing/layout features.
* If headings aren’t found, treats each page as a fallback section.
* Captures: `filename`, `section_title`, `page_number`, and full section text.

### Semantic Relevance Ranking

* Each section is semantically ranked using sentence-transformers.
* Persona and job are combined as a query; relevance is scored using cosine similarity.

### Granular Subsection Highlighting

* For each top section, extracts the **most relevant 600-character context window**.
* Fully extendable to sentence/keyword level.

### Structured Output

* JSON output strictly matches the challenge schema:

  * `metadata`: persona, job, timestamp, input documents.
  * `extracted_sections`: top-ranked sections.
  * `subsection_analysis`: refined, relevant content per section.

---

## Challenge Constraints Met

| Requirement                    | Status      |
| ------------------------------ | ----------- |
| CPU-only                       | Yes         |
| Model size ≤ 1 GB              | Yes         |
| No internet access             | Fully local |
| ≤ 60 seconds for 3–5 documents | Optimized   |
| Strict JSON schema compliance  | Confirmed   |
| Handles multiple collections   | Supported   |

---

## Tech Stack

* Python 3.10
* PyMuPDF for PDF parsing
* Sentence-Transformers for semantic ranking
* Docker (CPU-only)
* JSON for I/O

---

## Project Structure

```
CHALLENGE_1B-MAIN/
├── Collection 1/
│   └── pdf/
│       └── *.pdf
│   └── challenge1b_input.json
│   └── challenge1b_output.json
├── Collection 2/
│   └── pdf/
│   └── challenge1b_input.json
│   └── challenge1b_output.json
├── Collection 3/
│   └── ...
├
├── persona_extract.py          # Main runner (universal, no hardcoded paths)
├── section_extractor.py        # PDF section extraction logic
├── semantic_ranker.py          # Embedding + scoring
├── outline_extractor.py        # Heuristic heading extractor (optional)
├── outputsummary.py            # CLI output summary/validator
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## Example Output Format

```json
{
  "metadata": {
    "input_documents": ["file1.pdf", "file2.pdf"],
    "persona": "Marketing Manager",
    "job_to_be_done": "Plan a launch campaign",
    "processing_timestamp": "2025-07-24T13:05:32.123Z"
  },
  "extracted_sections": [
    {
      "document": "file1.pdf",
      "section_title": "Campaign Strategy Overview",
      "page_number": 3,
      "importance_rank": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "file1.pdf",
      "refined_text": "...most relevant 600 characters...",
      "page_number": 3
    }
  ]
}
```

---

## Credits

Team: **C0d3Hers**

Developed by: **Aditi Bhalla and Kashvi Rathore**

GitHub: https://github.com/aditibh19/challenge_1b.git

---

