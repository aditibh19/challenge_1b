# 🧠 Approach Overview

## 📂 Section Extraction
- Each PDF is parsed using **PyMuPDF** for layout-aware text extraction.
- Headings are detected based on:
  - Font size and weight (bold)
  - Alignment (centered or left-aligned)
  - Spacing and layout features
- If headings are not detected, each page is treated as a fallback section.
- Output includes: `filename`, `section_title`, `page_number`, and `full_text`.

## 🤖 Semantic Relevance Ranking
- Each extracted section is encoded using `sentence-transformers` (MiniLM-L6-v2, ~80MB RAM).
- The persona and job are combined into a semantic query.
- **Cosine similarity** is used to rank sections against the query embedding.

## 🔍 Granular Subsection Highlighting
- For each top section, we extract a **600-character context window**.
- This can be further extended to sentence-level or keyword-highlighting in future work.

## 📤 Structured Output
- JSON output follows the challenge schema:
  - `metadata`: persona, job, timestamp
  - `extracted_sections`: top-ranked sections
  - `subsection_analysis`: highlighted refined snippets
- Modular design enables adaptation to new personas and PDF layouts.

---

# ✅ Challenge Constraints Met

| Requirement                             | Status       |
|----------------------------------------|--------------|
| CPU-only                                | ✅ Yes        |
| Model size ≤ 1 GB                       | ✅ ~80MB      |
| No internet access                      | ✅ Fully local|
| ≤ 60 seconds for 3–5 documents          | ✅ Optimized  |
| Strict JSON schema compliance           | ✅ Confirmed  |
| Handles multiple folders independently  | ✅ Supported  |

