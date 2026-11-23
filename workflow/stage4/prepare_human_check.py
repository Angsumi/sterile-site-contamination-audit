"""Prepare seed-6 human review forms; never populate human judgments or run models."""
from pathlib import Path
import csv,hashlib,json,math,random,sys
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'human_check'
sys.path.insert(0,str(ROOT/'workflow'));import epmc
sys.path.insert(0,str(Path(__file__).resolve().parent));import check_one
form=OUT/'review_form.tsv'
if form.exists():
    old=list(csv.DictReader(open(form),delimiter='\t'))
    if any(any(v for k,v in r.items() if k.startswith('human_') or k in ('reviewer','checked_on')) for r in old):
        raise SystemExit('Existing human judgments found; preserve them and reconcile manually.')
screen_form=OUT/'screening_review.json'
if screen_form.exists():
    old_screen=json.loads(screen_form.read_text())
    if any(any(r.get(k) not in (None,'') for k in ('human_decision','reviewer','checked_on','comments')) for r in old_screen):
        raise SystemExit('Existing human screening judgments found; preserve them and reconcile manually.')
OUT.mkdir(exist_ok=True);(OUT/'packets').mkdir(exist_ok=True)
records={f.stem:json.loads(f.read_text()) for f in (ROOT/'extraction/json').glob('PMC*.json')}
studies={r['pmcid']:r for r in csv.DictReader(open(ROOT/'data/studies.csv'))}
pilot=sorted(f.stem for f in (ROOT/'pilot/extractions').glob('PMC*.json'))
assert len(pilot)==21 and all(p in records for p in pilot)
pool=sorted(p for p,x in records.items() if x['eligible_fulltext'] and p not in pilot)
rng=random.Random(6);random_ids=sorted(rng.sample(pool,math.ceil(len(pool)*.10)))
priorities={
'PMC7355471':'Manual supplement figure transcription; independently inspect Figure S3 tissue-column selection.',
'PMC6109274':'Manual supplement figure transcription; independently inspect Figure S6A AF labels.',
'PMC12922273':'Provisional exclusion: qualifying sequencing source cannot be verified.',
'PMC9130323':'Explicit retraction; determine reporting-audit and sensitivity handling before analysis.',
'PMC6586825':'Confirmed whole-cohort duplicate of PMC6345098; verify retained longer list.',
'PMC13243561':'Partial reuse of PMC8052771; verify independent Cohort-B-only extraction.',
'PMC9609265':'New cohort plus old validation; confirm discovery-only genus assignment.',
'PMC12649041':'Mixed reused cohorts and own validation; control provenance and possible CAMS overlap.',
'PMC12269162':'Possible blood MI cohort overlap with PMC12008866.',
'PMC12029928':'Check donor overlap with prior UAMS brain studies.',
'PMC11309925':'Possible serum-EV renal cohort overlap with PMC11786307.',
'PMC11786307':'Possible serum-EV renal cohort overlap with PMC11309925.',
'PMC10031003':'Pooled TCGA taxa lack eligible-site assignment; figure/metadata adjudication needed.',
'PMC13720141':'Pooled genome catalog lacks per-genus eligible-site assignment.',
'PMC13185545':'Verify supplement sample-to-cancer mapping and positive-abundance rule.',
'PMC5610236':'Diagnostic amniotic-fluid infection exclusion scope.',
'PMC3577789':'Diagnostic intra-amniotic infection/neonatal-sepsis exclusion scope.',
'PMC11811456':'GIST sequencing limited to ulcerated mucosa-exposed lesions; verify scope.',
'PMC9357631':'GIST closed-site eligibility and ulceration require confirmation.',
'PMC3587628':'Induced transient dental bacteremia: verify protocol scope and sensitivity flag.'}
selected=sorted(set(pilot+random_ids+list(priorities)))
manifest={'seed':6,'eligible_count':sum(x['eligible_fulltext'] for x in records.values()),'eligible_nonpilot_pool':len(pool),'random_fraction':.10,'random_rounding':'ceil','random_eligible_ids':random_ids,'all_pilot_ids':pilot,'protocol_extraction_ids':sorted(set(random_ids+pilot)),'additional_priority_reviews':priorities,'all_packet_ids':selected,'human_reviews_completed':0,'agreement':None}
rows=[]
for p in selected:
    x=records[p];s=studies[p];reasons=(['pilot'] if p in pilot else [])+(['seed6_random'] if p in random_ids else [])+(['additional_priority'] if p in priorities else [])
    rows.append({'pmcid':p,'selection':';'.join(reasons),'AI_eligible':x['eligible_fulltext'],'AI_tissue':x['tissue_category'],'AI_method':(x.get('method') or {}).get('value',''),'AI_controls':(x.get('controls') or {}).get('value',''),'AI_decontamination':(x.get('decontamination') or {}).get('value',''),'AI_counted_genera':s['n_genera'],**{k:'' for k in ['human_eligible','human_exclusion_reason','human_tissue','human_method','human_controls','human_decontamination','human_biomass_qpcr','human_genera','reviewer','checked_on','comments']}})
    els={e['evidence_id']:e for e in epmc.elements(epmc.PAPERS/p/'fulltext.xml')}
    packet=[f'# {p} — human review pending','',f"Selection: {', '.join(reasons)}.",f"Priority: {priorities.get(p,'Protocol sample.')}",'',f"[Full-text Markdown]({epmc.PAPERS/p/'fulltext.md'}) · [Source XML]({epmc.PAPERS/p/'fulltext.xml'})",'', '## AI extraction (provisional)','', '```json',json.dumps(x,ensure_ascii=False,indent=2),'```','','## Genus evidence windows','']
    for g in x.get('genera',[]):
        t=check_one.element_text(p,els,g['evidence_id']) or '';j=t.casefold().find(g['name'].casefold());start=max(0,j-80);window=t[start:start+260].replace('\n',' ')
        packet += [f"- **{g['name']}**, `{g['evidence_id']}`, flagged={g.get('flagged_contaminant',False)}: {window}"]
    packet+=['','Complete the blank human fields in `review_form.tsv`; do not treat automated matching or this AI packet as independent validation.']
    (OUT/'packets'/f'{p}.md').write_text('\n'.join(packet)+'\n')
with open(form,'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
screen=list(csv.DictReader(open(ROOT/'screening/screening_log_full.csv')));groups={}
for r in screen:groups.setdefault(r['decision'],[]).append(r)
rng=random.Random(6);screen_sample=[]
for decision,group in sorted(groups.items()):
    group.sort(key=lambda r:r.get('pmcid',''));sample=rng.sample(group,math.ceil(.05*len(group)))
    screen_sample.extend([{**r,'human_decision':None,'reviewer':None,'checked_on':None,'comments':None} for r in sample])
(OUT/'screening_review.json').write_text(json.dumps(screen_sample,ensure_ascii=False,indent=2)+'\n')
manifest['screening_total']=len(screen);manifest['screening_sample_size']=len(screen_sample);manifest['screening_stratified_counts']={k:math.ceil(.05*len(v)) for k,v in groups.items()}
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'data/studies.csv',ROOT/'data/genera.csv',ROOT/'data/check_summary.json',ROOT/'analysis/run_models.py']}
(OUT/'baseline_hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
readme=f'''# C6 independent human checks — pending

First-pass extraction is complete for all 523 downloaded full articles. An additional conference abstract is excluded in the 524-candidate disposition ledger. Current provisional totals: 475 eligible and 398 usable papers.

The seed-6 protocol extraction sample contains **{len(random_ids)} randomly selected eligible nonpilot papers plus all 21 pilot papers**, {len(set(random_ids+pilot))} unique papers. There are **{len(selected)} packet files** after adding explicit uncertainty priorities. Extra priorities are separate from the random sample and must not be used to claim unbiased agreement estimates.

The screening sample contains **{len(screen_sample)} decisions**, selected with seed 6 and 5% rounded up within each decision stratum. Exact IDs, denominators and selection methods are in `manifest.json`.

Review source full texts and supplements independently; record corrections and reviewer/date in the blank human columns of `review_form.tsv` and `screening_review.json`. For each genus, verify detection in the target compartment, source spelling, contaminant flag and sample-cohort attribution. Complete missing sample units, country and assay-region metadata where stated. For excluded records, verify the exclusion against the source.

Both manual figure transcriptions (PMC7355471 and PMC6109274) require visual comparison to the retained source PDF/rendering. The automatic checker can match the derived text, but cannot independently validate the figure reading. Review the retracted reporting record, unverifiable sequencing provenance and cohort links before analysis.

**No human reviews or agreement measurements have been completed. No models have been run.** After review, reconcile corrections, resolve cohort/taxonomy issues, rebuild the dataset, reassess the gate, and only then use the frozen model code. Baseline dataset and model hashes are recorded without executing the models.
'''
(OUT/'README.md').write_text(readme)
print(json.dumps({'protocol_extraction_papers':len(set(random_ids+pilot)),'random':len(random_ids),'pilot':len(pilot),'all_packets':len(selected),'screening_decisions':len(screen_sample),'human_reviews_completed':0}))
