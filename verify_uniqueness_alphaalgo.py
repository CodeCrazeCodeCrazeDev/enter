import yaml
import re

# Load AI_EOS_RESEARCH_DB.yaml
db_path = 'docs/research/papers/AI_EOS_RESEARCH_DB.yaml'
with open(db_path, 'r') as f:
    db_data = yaml.safe_load(f)
db_titles = {p['metadata']['title'].lower().strip() for p in db_data['papers']}

# Load docs/research/papers/ALPHAALGO_100_RESEARCH_PAPERS.md and parse titles
papers_md_path = 'docs/research/papers/ALPHAALGO_100_RESEARCH_PAPERS.md'
with open(papers_md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

# Regular expression to extract paper titles
# Format in markdown: "## Paper X: Title of the Paper"
found_titles = re.findall(r'## Paper \d+:\s*(.*)', md_content)
parsed_titles = {t.strip().lower() for t in found_titles}

print(f"Total parsed titles from MD: {len(parsed_titles)}")
print(f"Total unique titles from DB: {len(db_titles)}")

# Find intersection
overlap = parsed_titles.intersection(db_titles)
if overlap:
    raise ValueError(f"CRITICAL ERROR: Overlap of {len(overlap)} titles found between DB and AlphaAlgo 100 papers! Overlapped titles: {overlap}")
else:
    print("SUCCESS: 100% uniqueness verified! Zero title overlap found between the research corpuses.")
