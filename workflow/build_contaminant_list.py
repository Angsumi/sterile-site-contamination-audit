"""Build the pre-specified C6 contaminant genus list from open-access source tables.

Sources are parsed from their full-text XML (Europe PMC / PMC OA), so every genus
traces to an evidence ID. Run before any study results are extracted.

Output: reference/contaminant_genera.csv (one row per genus, with source flags and list membership)
"""
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import epmc

SOURCES = {
    'salter2014': ('PMC4228153', 'Salter et al. 2014 BMC Biol 12:87, Table 1 (genera in sequenced blank controls, 4 years, 3 labs)'),
    'glassing2016': ('PMC4882852', 'Glassing et al. 2016 Gut Pathog 8:24, Tables 1-2 (genera in blood and MoBio extraction kits)'),
    'weyrich2019': ('PMC6850301', 'Weyrich et al. 2019 Mol Ecol Resour 19:982, Table 1 (69 dominant genera in extraction blanks and NTCs)'),
}

# Pre-specified (22 Nov 2026, before any study extraction): genera excluded from the PRIMARY
# "environmental" list because they are dominant members of human gut, oral, skin or vaginal
# communities, or major human pathogens, so a hit is not good evidence of contamination.
HUMAN_ASSOCIATED = {
    'Abiotrophia', 'Acinetobacter', 'Actinomyces', 'Alistipes', 'Anaerococcus', 'Atopobium', 'Bacteroides',
    'Bifidobacterium', 'Blautia', 'Brevibacterium', 'Capnocytophaga', 'Cardiobacterium', 'Catenibacterium',
    'Christensenella', 'Clostridium', 'Collinsella', 'Coprococcus', 'Corynebacterium', 'Dialister', 'Dorea',
    'Eggerthella', 'Enterobacter', 'Enterococcus', 'Erysipelatoclostridium', 'Escherichia', 'Escherichia_Shigella',
    'Eubacterium', 'Facklamia', 'Flavonifractor', 'Fusobacterium', 'Gemella', 'Granulicatella', 'Haemophilus',
    'Intestinibacter', 'Johnsonella', 'Kingella', 'Klebsiella', 'Kocuria', 'Lachnoanaerobaculum', 'Lachnoclostridium',
    'Lachnospira', 'Lactobacillus', 'Leptotrichia', 'Micrococcus', 'Moryella', 'Neisseria', 'Parabacteroides',
    'Parvimonas', 'Peptococcus', 'Peptoniphilus', 'Porphyromonas', 'Prevotella', 'Propionibacterium', 'Cutibacterium',
    'Pseudobutyrivibrio', 'Pseudoflavonifractor', 'Pseudomonas', 'Quinella', 'Roseburia', 'Rothia', 'Serratia',
    'Slackia', 'Solobacterium', 'Staphylococcus', 'Stenotrophomonas', 'Streptococcus', 'Turicibacter', 'Tyzzerella',
    'Veillonella', 'Xylanibacter',
}
# Synonyms: reported names mapped onto the list name (renamed genera)
SYNONYMS = {'Cutibacterium': 'Propionibacterium', 'Roseateles': 'Pelomonas', 'Escherichia_Shigella': 'Escherichia',
            'Escherichia-Shigella': 'Escherichia', 'Shigella': 'Escherichia'}


def salter():
    e = epmc.elements(epmc.PAPERS / 'PMC4228153' / 'fulltext.xml')
    for x in e:
        t = x['text']
        if 'Table 1 List of contaminant genera' in t:
            body = t[t.find('Table 1 List'):t.find('The listed genera were all detected')]
            names = set(re.findall(r'\b([A-Z][a-z]{3,})\b', body))
            drop = {'Table', 'List', 'Phylum', 'Proteobacteria', 'Alpha', 'Beta', 'Gamma', 'Actinobacteria', 'Firmicutes',
                    'Bacteroidetes', 'Deinococcus', 'Thermus', 'Acidobacteria', 'Predominantly'}
            g = sorted(names - drop) + ['Deinococcus']
            return {n: x['evidence_id'] for n in g}
    raise ValueError('Salter Table 1 not found')


def glassing():
    out = {}
    for x in epmc.elements(epmc.PAPERS / 'PMC4882852' / 'fulltext.xml'):
        t = x['text']
        if re.match(r'\[Table [12] row\]', t):
            cells = [c.strip() for c in t.split(']', 1)[1].split('|')]
            if cells[0] in ('Family',):
                continue
            name = cells[-2] if len(cells) >= 2 else ''
            m = re.match(r'([A-Z][a-z]+(?:_[A-Za-z]+)?)', name)
            if m and m.group(1) not in ('Genus', 'Genera', 'Candidatus'):
                out.setdefault(m.group(1), x['evidence_id'])
    return out


def weyrich():
    out = {}
    for x in epmc.elements(epmc.PAPERS / 'PMC6850301' / 'fulltext.xml'):
        t = x['text']
        if t.startswith('[Table 1 row]'):
            m = re.search(r'g__([A-Z][a-z]+)', t)
            if m:
                out.setdefault(m.group(1), x['evidence_id'])
    return out


def main():
    src = {'salter2014': salter(), 'glassing2016': glassing(), 'weyrich2019': weyrich()}
    genera = sorted({SYNONYMS.get(g, g) for s in src.values() for g in s})
    rows = []
    for g in genera:
        flags = {k: next((v[n] for n in v if SYNONYMS.get(n, n) == g), '') for k, v in src.items()}
        n_src = sum(bool(v) for v in flags.values())
        human = g in HUMAN_ASSOCIATED
        rows.append({'genus': g, **{f'{k}_evidence': flags[k] for k in src}, 'n_sources': n_src,
                     'human_associated': int(human),
                     # PRIMARY: Salter 2014 genera that are not human-associated
                     'list_primary_environmental': int(bool(flags['salter2014']) and not human),
                     # STRICT: primary AND confirmed in >=1 other source
                     'list_strict': int(bool(flags['salter2014']) and not human and n_src >= 2),
                     # BROAD: any genus in any source (incl. human-associated)
                     'list_broad': 1})
    out = epmc.ROOT / 'reference' / 'contaminant_genera.csv'
    with open(out, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print({k: len(v) for k, v in src.items()}, 'union', len(rows),
          'primary', sum(r['list_primary_environmental'] for r in rows), 'strict', sum(r['list_strict'] for r in rows))
    print('strict:', ', '.join(r['genus'] for r in rows if r['list_strict']))


if __name__ == '__main__':
    main()
