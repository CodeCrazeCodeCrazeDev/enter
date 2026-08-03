# -*- coding: utf-8 -*-
"""
verify_corpus_uniqueness.py: Automatically checks paper uniqueness and outputs duplicate-detection
results across papers 1-130 vs 131-230.
"""
import yaml

def get_tokens(text):
    if not text:
        return set()
    return set(text.lower().replace(".", "").replace(",", "").split())

def calculate_jaccard(text1, text2):
    tokens1 = get_tokens(text1)
    tokens2 = get_tokens(text2)
    if not tokens1 or not tokens2:
        return 0.0
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    return len(intersection) / len(union)

def main():
    filepath = "docs/research/papers/AI_EOS_RESEARCH_DB.yaml"
    print(f"Loading research database from: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        db = yaml.safe_load(f)

    papers = db.get("papers", [])
    original_papers = [p for p in papers if p["id"] <= 130]
    new_papers = [p for p in papers if p["id"] >= 131]

    print(f"Total papers: {len(papers)}")
    print(f"Original corpus (1-130): {len(original_papers)} papers")
    print(f"New literature review corpus (131-230): {len(new_papers)} papers")

    duplicates_found = 0
    highest_similarity = 0.0
    most_similar_pair = ()

    # Compare every new paper with all original papers
    for new_p in new_papers:
        new_title = new_p["metadata"]["title"]
        new_prob = new_p["technical_facts"]["problem"]
        new_meth = new_p["technical_facts"]["method"]
        new_notes = new_p["analysis"]["implementation_notes"]

        for orig_p in original_papers:
            orig_title = orig_p["metadata"]["title"]
            orig_prob = orig_p["technical_facts"]["problem"]
            orig_meth = orig_p["technical_facts"]["method"]
            orig_notes = orig_p["analysis"]["implementation_notes"]

            # Exact matching checks
            if new_title.lower() == orig_title.lower():
                print(f"[DUPLICATE] Exact title match: ID {new_p['id']} vs ID {orig_p['id']} - '{new_title}'")
                duplicates_found += 1
            if new_prob.lower() == orig_prob.lower():
                print(f"[DUPLICATE] Exact problem match: ID {new_p['id']} vs ID {orig_p['id']}")
                duplicates_found += 1
            if new_meth.lower() == orig_meth.lower():
                print(f"[DUPLICATE] Exact method match: ID {new_p['id']} vs ID {orig_p['id']}")
                duplicates_found += 1
            if new_notes.lower() == orig_notes.lower():
                print(f"[DUPLICATE] Exact implementation notes match: ID {new_p['id']} vs ID {orig_p['id']}")
                duplicates_found += 1

            # Jaccard similarity score on title
            sim = calculate_jaccard(new_title, orig_title)
            if sim > highest_similarity:
                highest_similarity = sim
                most_similar_pair = (new_p["id"], orig_p["id"], new_title, orig_title)

    print("\n--- Duplicate-Detection Verification Results ---")
    print(f"Exact Duplicates Found: {duplicates_found}")
    print(f"Highest Title Jaccard Similarity: {highest_similarity:.4f}")
    if most_similar_pair:
        new_id, orig_id, t1, t2 = most_similar_pair
        print(f"Most similar title pair: ID {new_id} vs ID {orig_id}")
        print(f"  - New Title:  '{t1}'")
        print(f"  - Orig Title: '{t2}'")

    if duplicates_found == 0:
        print("\n✔ SUCCESS: 100% uniqueness verified! No duplicate papers detected.")
    else:
        print("\n✖ FAILURE: Duplicate papers detected in database.")
        exit(1)

if __name__ == "__main__":
    main()
