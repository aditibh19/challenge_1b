## Approach Overview

### Section Extraction

* Each PDF is parsed using **PyMuPDF** for layout-aware text extraction.
* Headings are detected based on:

  * Font size and weight (bold)
  * Alignment (centered or left-aligned)
  * Spacing and layout features
* If headings are not detected, each page is treated as a fallback section.
* Output includes: `filename`, `section_title`, `page_number`, and `full_text`.

### Semantic Relevance Ranking

* Each extracted section is embedded using a compact, open-source sentence embedding model.
* The persona and job description are combined into a semantic query.
* Cosine similarity is used to rank all sections for their relevance to the query.

### Granular Subsection Highlighting

* For each top-ranked section, a 600-character context window is extracted as the most relevant snippet.
* The approach can be extended to sentence-level or keyword-level highlights.

### Structured Output

* JSON output follows the challenge schema:

  * `metadata`: persona, job, timestamp
  * `extracted_sections`: top-ranked sections
  * `subsection_analysis`: highlighted, refined snippets
* The modular design allows for easy adaptation to new personas and PDF layouts.

---

## Challenge Constraints Met

| Requirement                            | Status      |
| -------------------------------------- | ----------- |
| CPU-only                               | Yes         |
| Model size ≤ 1 GB                      | Yes         |
| No internet access                     | Fully local |
| ≤ 60 seconds for 3–5 documents         | Optimized   |
| Strict JSON schema compliance          | Confirmed   |
| Handles multiple folders independently | Supported   |

---
