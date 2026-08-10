# Programmatic uniqueness validation script for AlphaAlgo Research Bibliography.
# This script asserts that the 100 new papers do not overlap with the existing 130 papers.

import yaml

existing_db_path = "docs/research/papers/AI_EOS_RESEARCH_DB.yaml"
new_md_path = "docs/research/papers/ALPHAALGO_100_RESEARCH_PAPERS.md"

def verify_uniqueness():
    # Load existing titles
    with open(existing_db_path, "r") as f:
        db = yaml.safe_load(f)
    existing_titles = set(p["metadata"]["title"].strip().lower() for p in db["papers"])
    print(f"[Verification] Loaded {len(existing_titles)} existing paper titles from {existing_db_path}.")

    # Read the 100 new papers and parse their titles
    with open(new_md_path, "r") as f:
        md_text = f.read()

    # Match titles of the form "## ID. Title"
    new_titles = [line.split(".", 1)[1].strip() for line in md_text.splitlines() if line.startswith("## ")]
    print(f"[Verification] Loaded {len(new_titles)} new paper titles from {new_md_path}.")

    assert len(new_titles) == 100, f"Expected exactly 100 new papers, found {len(new_titles)}."

    # Verify zero overlap
    overlaps = []
    for t in new_titles:
        if t.lower() in existing_titles:
            overlaps.append(t)

    if overlaps:
        print(f"[Verification] FAILURE: Found {len(overlaps)} overlapping paper titles!")
        for o in overlaps:
            print(f"  - {o}")
        raise AssertionError("Validation failed: Overlapping papers found.")
    else:
        print("[Verification] SUCCESS: 100% unique papers! Zero overlaps detected.")

if __name__ == "__main__":
    verify_uniqueness()
