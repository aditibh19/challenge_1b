import fitz  # PyMuPDF
import json
import sys

def extract_outline_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []
    headings = set()
    max_title = ("", 0)
    first_page = doc[0]
    for block in first_page.get_text("dict")["blocks"]:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            spans = line["spans"]
            text = "".join([span["text"] for span in spans]).strip()
            font_sizes = [span["size"] for span in spans]
            max_size = max(font_sizes) if font_sizes else 0
            if text and max_size > max_title[1]:
                max_title = (text, max_size)
    title = max_title[0]
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
                if text in headings:
                    continue
                font_sizes = [span["size"] for span in spans]
                max_size = max(font_sizes) if font_sizes else 0
                is_bold = any("Bold" in span.get("font", "") for span in spans)
                if max_size > 13 or is_bold:
                    if max_size > 17:
                        level = "H1"
                    elif max_size > 14:
                        level = "H2"
                    else:
                        level = "H3"
                    outline.append({"level": level, "text": text, "page": page_idx + 1})
                    headings.add(text)
    return {"title": title, "outline": outline}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python outline_extractor.py input.pdf [output.json]")
        sys.exit(1)
    pdf_path = sys.argv[1]
    output_json = sys.argv[2] if len(sys.argv) > 2 else "output.json"
    result = extract_outline_from_pdf(pdf_path)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Extracted outline written to {output_json}")