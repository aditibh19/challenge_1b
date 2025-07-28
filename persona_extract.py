import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import os
import json
import datetime
from section_extractor import extract_sections_from_pdf
from semantic_ranker import rank_sections_semantically

def process_collection(collection_path):
    input_json_path = os.path.join(collection_path, "challenge1b_input.json")
    pdf_dir = os.path.join(collection_path, "pdf")
    output_json_path = os.path.join(collection_path, "challenge1b_output.json")

    if not os.path.exists(input_json_path):
        print(f"❌ Missing input file in {collection_path}")
        return

    with open(input_json_path, "r", encoding="utf-8") as f:
        input_data = json.load(f)

    persona = input_data["persona"]["role"]
    job = input_data["job_to_be_done"]["task"]
    doc_list = input_data["documents"]
    all_sections = []

    for doc in doc_list:
        pdf_path = os.path.join(pdf_dir, doc["filename"])
        if not os.path.isfile(pdf_path):
            print(f"⚠️ Missing file: {pdf_path}")
            continue
        sections = extract_sections_from_pdf(pdf_path, doc["filename"])
        all_sections.extend(sections)

    extracted_sections, subsection_analysis = rank_sections_semantically(
        all_sections, persona, job
    )

    output = {
        "metadata": {
            "input_documents": [d["filename"] for d in doc_list],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.datetime.now().isoformat()
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✅ Processed {collection_path}")

def main():
    base_dir = os.getcwd()
    for folder in os.listdir(base_dir):
        # Skip hidden/system folders and the 'models' directory
        if folder.startswith(".") or folder.startswith("__") or folder == "models":
            continue
        path = os.path.join(base_dir, folder)
        if os.path.isdir(path):
            process_collection(path)
    print("🎉 Done processing all collections!")

if __name__ == "__main__":
    main()
