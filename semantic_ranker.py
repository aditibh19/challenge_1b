from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer

# Load any public model by name
model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/paraphrase-MiniLM-L6-v2")

def truncate_text(text, max_tokens=512):
    input_ids = tokenizer.encode(text, truncation=True, max_length=max_tokens)
    return tokenizer.decode(input_ids, skip_special_tokens=True)

def rank_sections_semantically(sections, persona, job, topk_sections=5, topk_subsections=5):
    query = f"{persona}: {job}"
    query_embedding = model.encode(query, convert_to_tensor=True)

    section_scores = []
    for sec in sections:
        formatted = f"{sec.get('section_title','')}\n\n{sec.get('section_text','')}"
        truncated = truncate_text(formatted)
        embedding = model.encode(truncated, convert_to_tensor=True)
        score = util.cos_sim(query_embedding, embedding).item()
        section_scores.append((score, sec))

    # 1. For each document, keep only the *best scoring* section
    best_per_doc = {}
    for score, sec in section_scores:
        doc = sec["document"]
        if doc not in best_per_doc or score > best_per_doc[doc][0]:
            best_per_doc[doc] = (score, sec)

    # 2. Create a list with the top section from each doc (sorted by score)
    diverse_sections = sorted(best_per_doc.values(), key=lambda x: x[0], reverse=True)

    # 3. If topk_sections > num_docs, fill up from remaining best sections
    used_docs = set(sec["document"] for _, sec in diverse_sections)
    rest = [
        (score, sec) for score, sec in sorted(section_scores, key=lambda x: x[0], reverse=True)
        if sec["document"] not in used_docs
    ]
    top_sections = diverse_sections[:topk_sections]
    while len(top_sections) < topk_sections and rest:
        top_sections.append(rest.pop(0))

    # 4. Build output in your preferred format
    extracted_sections = []
    for rank, (score, sec) in enumerate(top_sections, 1):
        extracted_sections.append({
            "document": sec["document"],
            "section_title": sec["section_title"],
            "importance_rank": rank,
            "page_number": sec["page_number"]
        })

    # 5. Paragraph ranking for granular analysis (same as before)
    paragraph_scores = []
    for _, sec in top_sections:
        text = sec.get('section_text', '')
        paragraphs = [p.strip() for p in text.split("\n") if len(p.strip()) > 30]
        if not paragraphs:
            paragraphs = [text.strip()]
        for para in paragraphs:
            para_trunc = truncate_text(para)
            para_embedding = model.encode(para_trunc, convert_to_tensor=True)
            score = util.cos_sim(query_embedding, para_embedding).item()
            paragraph_scores.append((score, {
                "document": sec["document"],
                "refined_text": para[:600],
                "page_number": sec["page_number"]
            }))

    paragraph_scores.sort(key=lambda x: x[0], reverse=True)
    subsection_analysis = [x[1] for x in paragraph_scores[:topk_subsections]]

    return extracted_sections, subsection_analysis
