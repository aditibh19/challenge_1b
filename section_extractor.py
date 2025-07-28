import fitz  # PyMuPDF

def extract_sections_from_pdf(pdf_path, doc_name):
    doc = fitz.open(pdf_path)
    results = []
    section_starts = []

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                spans = line["spans"]
                text = "".join([span["text"] for span in spans]).strip()
                if not text or len(text) > 120:
                    continue
                font_sizes = [span["size"] for span in spans]
                max_size = max(font_sizes) if font_sizes else 0
                is_bold = any("Bold" in span.get("font", "") for span in spans)
                if max_size > 13 or is_bold:
                    section_starts.append((page_idx, text))

    if section_starts:
        for idx, (page_idx, heading_text) in enumerate(section_starts):
            start_page = page_idx
            end_page = section_starts[idx + 1][0] if idx + 1 < len(section_starts) else len(doc)
            section_text = ""
            for p in range(start_page, end_page):
                section_text += doc[p].get_text()
            if len(section_text.strip()) > 80:
                results.append({
                    "document": doc_name,
                    "section_title": heading_text,
                    "page_number": start_page + 1,
                    "section_text": section_text.strip()
                })
    else:
        for page_idx in range(len(doc)):
            text = doc[page_idx].get_text()
            if len(text.strip()) > 80:
                results.append({
                    "document": doc_name,
                    "section_title": f"Page {page_idx+1}",
                    "page_number": page_idx + 1,
                    "section_text": text.strip()
                })
    doc.close()
    return results