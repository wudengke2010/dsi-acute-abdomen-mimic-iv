"""Verify all manuscript references against Crossref API."""
import re
import time
import json
import urllib.request
import urllib.error

md = open('SCI_paper_v8.md', encoding='utf-8').read()
refsec = md[md.index('## References'):]
refs = {}
for line in refsec.split('\n'):
    m = re.match(r'^(\d+)\. (.+)$', line.strip())
    if m:
        refs[int(m.group(1))] = m.group(2)

results = []
for num, text in sorted(refs.items()):
    dm = re.search(r'https://doi\.org/(10\.\S+?)(?:\s|$)', text)
    # claimed title: text after authors, before journal-ish part — take a key phrase from ref text
    if not dm:
        results.append({'ref': num, 'doi': None, 'status': 'NO_DOI', 'text': text[:90]})
        continue
    doi = dm.group(1)
    req = urllib.request.Request(
        f'https://api.crossref.org/works/{doi}',
        headers={'User-Agent': 'ref-verify/1.0 (mailto:wudk2010@csu.edu.cn)'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode())['message']
        cr_title = (data.get('title') or [''])[0].lower()
        cr_year = None
        for k in ('published-print', 'published-online', 'issued'):
            if k in data and data[k].get('date-parts'):
                cr_year = data[k]['date-parts'][0][0]
                break
        cr_journal = (data.get('container-title') or [''])[0]
        # claimed year from ref text
        ym = re.search(r'\b(19|20)\d{2}\b(?=[;.])', text[text.index(doi.split('/')[1][:5]) if False else 40:])
        # simpler: first 4-digit year in text that appears after authors
        years = re.findall(r'\b((?:19|20)\d{2})\b', text)
        claimed_year = None
        for y in years:
            iy = int(y)
            if 1940 <= iy <= 2026:
                claimed_year = iy
                break
        ok_title = bool(cr_title) and len(cr_title) > 10
        year_match = (claimed_year is None) or (cr_year in (claimed_year, claimed_year + 1, claimed_year - 1))
        results.append({'ref': num, 'doi': doi, 'status': 'FOUND',
                        'cr_title': cr_title[:80], 'cr_year': cr_year, 'cr_journal': cr_journal[:40],
                        'claimed_year': claimed_year, 'year_match': year_match})
    except urllib.error.HTTPError as e:
        results.append({'ref': num, 'doi': doi, 'status': f'HTTP_{e.code}', 'text': text[:90]})
    except Exception as e:
        results.append({'ref': num, 'doi': doi, 'status': f'ERR_{type(e).__name__}', 'text': str(e)[:60]})
    time.sleep(0.6)

print(json.dumps(results, ensure_ascii=False, indent=1))
