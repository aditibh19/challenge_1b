import os
import json

def summarize_output(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("📄", os.path.basename(path))
    print("Persona:", data["metadata"]["persona"])
    print("Job:", data["metadata"]["job_to_be_done"])
    print("Top Sections:")
    for sec in data["extracted_sections"]:
        print(f"  #{sec['importance_rank']} – {sec['section_title']} ({sec['document']})")

    print("Top Subsections:")
    for sub in data["subsection_analysis"]:
        snippet = sub["refined_text"][:80].replace("\n", " ") + "..."
        print(f"  🔹 {snippet}")
    print("-" * 60)

def main():
    base_dir = os.getcwd()
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file == "challenge1b_output.json":
                summarize_output(os.path.join(root, file))

if __name__ == "__main__":
    main()