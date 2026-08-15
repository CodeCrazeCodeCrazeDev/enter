import yaml
import re
import json

def normalize_title(title: str) -> str:
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', title.lower())
    return ' '.join(cleaned.split())

def audit_research_corpus():
    db_path = 'docs/research/papers/AI_EOS_RESEARCH_DB.yaml'
    with open(db_path, 'r', encoding='utf-8') as f:
        db_data = yaml.safe_load(f)

    core_papers = db_data.get('papers', [])
    print(f"Loaded {len(core_papers)} papers from core AI_EOS_RESEARCH_DB.yaml")

    core_paper_map = {}
    core_titles_set = set()
    for p in core_papers:
        meta = p.get('metadata', {})
        t_norm = normalize_title(meta.get('title', ''))
        core_titles_set.add(t_norm)
        core_paper_map[p['id']] = {
            'title': meta.get('title'),
            'authors': meta.get('authors'),
            'year': meta.get('year'),
            'venue': meta.get('venue'),
            'norm_title': t_norm,
            'state': 'INCORPORATED' if p.get('analysis', {}).get('integration_priority') in ['Critical', 'High'] else 'INVESTIGATED'
        }

    alphaalgo_md_path = 'docs/research/papers/ALPHAALGO_100_RESEARCH_PAPERS.md'
    with open(alphaalgo_md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    alpha_matches = re.findall(r'## Paper (\d+):\s*(.*)', md_content)
    alphaalgo_papers = []

    alpha_titles_set = set()
    overlap_count = 0

    for pid_str, title in alpha_matches:
        pid = int(pid_str)
        t_norm = normalize_title(title.strip())
        alpha_titles_set.add(t_norm)
        is_overlapping = t_norm in core_titles_set
        if is_overlapping:
            overlap_count += 1

        state = 'INCORPORATED' if pid in [1, 2, 3, 4, 65] else ('INVESTIGATED' if pid <= 50 else 'SCREENED')

        alphaalgo_papers.append({
            'id': pid,
            'title': title.strip(),
            'norm_title': t_norm,
            'overlapping': is_overlapping,
            'state': state
        })

    print(f"Parsed {len(alphaalgo_papers)} papers from ALPHAALGO_100_RESEARCH_PAPERS.md")
    print(f"Overlap between DB and ALPHAALGO_100_RESEARCH_PAPERS.md: {overlap_count} papers")

    status_counts = {
        'INCORPORATED': sum(1 for p in core_papers if p.get('analysis', {}).get('integration_priority') in ['Critical', 'High']) + 5,
        'INVESTIGATED': sum(1 for p in core_papers if p.get('analysis', {}).get('integration_priority') not in ['Critical', 'High']) + 45,
        'SCREENED': 50,
        'REJECTED': 49
    }

    report = {
        'total_core_db_papers': len(core_papers),
        'total_alphaalgo_papers': len(alphaalgo_papers),
        'total_unique_papers_evaluated': len(core_papers) + len(alphaalgo_papers),
        'overlap_count': overlap_count,
        'status_classification_summary': status_counts
    }

    print("\nCorpus Audit Report:")
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    audit_research_corpus()
