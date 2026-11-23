from pathlib import Path
import sys,json,re,csv,hashlib,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2];P=R/'papers';B=R/'extraction/batch_next100'
sys.path.insert(0,str(R/'workflow'));import epmc
sys.path.insert(0,str(R/'workflow/stage4'));import check_one
ids=[r['pmcid'] for r in json.loads((B/'selection.json').read_text())];curation=json.loads((B/'curation.json').read_text());configs={n:curation[pm] for n,pm in enumerate(ids,1)}
G={r['name'] for r in csv.DictReader(open(R/'reference/ncbi_genera.tsv'),delimiter='\t') if r['domain']=='Bacteria'}
norm=lambda s:re.sub(r'\s+',' ',s.replace('\\','')).strip().lower()
def splitval(s):
 a=s.split(':',1);return a[0],a[1] if len(a)>1 else None
errors=[]
for n,pm in enumerate(ids,1):
 cfg=configs[n];ls=(P/pm/'fulltext.md').read_text().splitlines();els=epmc.elements(P/pm/'fulltext.xml')
 def el(k,term=''):
  if isinstance(k,str) and k.startswith('S'):
   a,b=k.split(':');t=(P/pm/'supp_md'/f'{a}.md').read_text().splitlines()[int(b[1:])-1];return k,t
  k=int(k);body=re.sub(r'^\[[^]]+\]\s*','',ls[k-1]);ln=norm(body)
  matches=[e for e in els if norm(e['text']) in ln or ln in norm(e['text'])]
  good=[e for e in matches if term.casefold() in e['text'].casefold()] if term else matches
  if not good:
   good=[e for e in els if (not term or term.casefold() in e['text'].casefold()) and (ln[:100] in norm(e['text']) or norm(e['text'])[:100] in ln)]
  if not good:raise ValueError(f'No source match {pm} line{k} {term}')
  e=good[0];return e['evidence_id'],e['text']
 def evidence(k,terms=''):
  eid,t=el(k)
  if terms and not (isinstance(k,str) and k.startswith('S')):
   ln=norm(re.sub(r'^\[[^]]+\]\s*','',ls[int(k)-1]))
   candidates=[e for e in els if (norm(e['text']) in ln or ln in norm(e['text'])) and re.search(terms,e['text'],re.I)]
   if candidates:eid,t=candidates[0]['evidence_id'],candidates[0]['text']
  m=re.search(terms,t,re.I) if terms else None;pos=max(0,m.start()-35) if m else 0
  return [{'id':eid,'quote':t[pos:pos+240]}]
 root=ET.parse(P/pm/'fulltext.xml').getroot();years=[e.text for e in root.findall('.//article-meta/pub-date/year') if e.text]
 x=dict(pmcid=pm,tissue_category=cfg['tissue'],sub_site=cfg['site'],year=int(years[0]) if years else None,country='',eligible_fulltext=not bool(cfg.get('exclude')),exclusion_reason=cfg.get('exclude',''),extractor='Codex single-agent Markdown batch next100; provisional AI first pass',date='2026-11-23',source_markdown_sha256=hashlib.sha256((P/pm/'fulltext.md').read_bytes()).hexdigest())
 try:
  if not cfg.get('exclude'):
   m,mk=splitval(cfg['method']);c,ck=splitval(cfg['controls']);d,dk=splitval(cfg['decon']);q,qk=splitval(cfg['qpcr'])
   x.update(data_source=dict(value='public_reuse' if cfg.get('public') else 'own_samples',dataset=cfg.get('dataset',''),evidence=evidence(cfg['public'],'TCGA|download|cohort|sequenc') if cfg.get('public') else []),
    method=dict(value=m,region='',evidence=evidence(mk,{'16S':r'16\s?S|ribosomal','2bRAD-M':'2bRAD','host_seq_mining':'RNA.sequenc|RNA.seq|TCGA|non.human|unmapped|WGS|microbial abundance','shotgun':'metagenom|sequencing','metatranscriptomic':'metatranscript','16S+shotgun':r'16\s?S|shotgun'}.get(m,'16S|RNA'))),
    controls=dict(value=c,types='negative controls as cited' if ck else '',n_sequenced=None,evidence=evidence(ck,'negative|blank|control') if ck else []),
    decontamination=dict(value=d,tool='SourceTracker' if n==9 else 'decontam' if n in [10,74,87] else 'SCRuB' if n==55 else 'statistical / batch filtering' if d=='tool' else '',evidence=evidence(dk,r'decontam|SCRuB|SourceTracker|remov[^.]{0,100}(?:control|contamina)|exclud[^.]{0,100}(?:control|contamina)|contamina[^.]{0,100}(?:remov|exclud)|threshold|filter') if dk else []),
    biomass_qpcr=dict(value=q,evidence=evidence(qk,'qPCR|quantitative PCR|copy number|bacterial load') if qk else []),n_target_samples=cfg.get('n'),list_type=cfg.get('list_type','mixed'),genera=[],top5=cfg.get('top5',[]),figures_only='partial',authors_conclusion=cfg.get('conclusion','claimed'),notes=cfg.get('notes',''),review_flags=['Provisional AI extraction; human checking and cohort linkage remain outstanding.'])
   if cfg.get('extra_method_line'):x['method']['evidence']+=evidence(cfg['extra_method_line'],'16S|shotgun|sequenc')
   gs={}
   for k in cfg['lines']:
    text=ls[k-1].replace('\\','');manual=cfg.get('overrides',{}).get(str(k));names=set(manual) if manual is not None else set(re.findall(r'(?:g__|g_|\b)([A-Z][a-z]+)',text))&G
    if manual is None:
     # SILVA composite labels count once, preserving source typography.
     for ma in re.finditer(r'[A-Z][a-z]+(?:\s*[-‐‑–—/]\s*[A-Z][a-z]+)+',text):
      parts=re.findall('[A-Z][a-z]+',ma.group())
      if len(set(parts)&G)>=2:
       names-=set(parts);names.add(parts[0] if '/' in ma.group() else ma.group())
    for g in sorted(names):
     eid,t=el(k,g)
     flag=cfg.get('flag_all',False) or any(g.startswith(f) for f in cfg.get('flagged',[]))
     if n==39 and k in range(95,192,4):
      cols=text.split('|');flag=bool(cols[-1].strip().strip('*').strip()) if False else bool(cols[-1].strip())
     key=re.split(r'[-_ ‐–—/]',g)[0].casefold()
     entry=dict(name=g,evidence_id=eid,flagged_contaminant=bool(flag))
     if key not in gs:gs[key]=entry
     elif flag:gs[key]['flagged_contaminant']=True
   x['genera']=list(gs.values())
   if n in [48,60]:x['figures_only']='yes'
   if cfg.get('hold'):x['review_flags'].append(cfg['hold'])
   if cfg.get('review_taxonomy'):x['review_flags'].append(cfg['review_taxonomy'])
   if cfg.get('scope_line'):x['eligibility_evidence']=evidence(cfg['scope_line'],'unable to capture|sepsis')
  dest=B/'held' if cfg.get('hold') else B/'records';dest.mkdir(exist_ok=True);other=B/('records' if cfg.get('hold') else 'held')/f'{pm}.json';other.unlink(missing_ok=True);(dest/f'{pm}.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
 except Exception as exc:errors.append((n,pm,str(exc)))
print('AUTHOR ERRORS',errors)

def positive_table(n,fn,header,start,end,skip):
 ls=(P/ids[n-1]/'supp_md'/fn).read_text().splitlines();cells=lambda l:[c.strip().replace('\\','') for c in l.split('|')[1:-1]]
 h=cells(ls[header-1]);keep=[]
 for col,label in enumerate(h):
  if col<skip:continue
  if label.startswith(('Unknown','Unkonwn','Unkown','Other ')):continue
  has=False
  for row in ls[start-1:end]:
   a=cells(row)
   try:has|=float(a[col])>0
   except (ValueError,IndexError):pass
  if has:
   names=set(re.findall(r'\b[A-Z][a-z]+',label))&G
   if label in ['Sporocarcinia','Granilucatella','Catonella','Veillonela']:names.add(label)
   keep.extend((g,f'{fn[:-3]}:L{header}') for g in names)
 return keep
for n in [49,65,89]:
 pm=ids[n-1];f=B/'records'/f'{pm}.json';x=json.loads(f.read_text());adds=[]
 if n==49:
  ls=(P/pm/'supp_md/S910.md').read_text().splitlines()
  for k in range(114,138):
   adds += [(g,f'S910:L{k}') for g in re.findall(r'\b[A-Z][a-z]+',ls[k-1]) if g in G or g=='Bosea']
  adds+=positive_table(n,'S910.md',60196,60197,60220,1)
  x['notes']=x['notes'].replace('Table 5 explicitly shotgun-only genera','Table 6 nonzero shotgun-only abundance columns')
 if n==65:adds+=positive_table(n,'S1000.md',6,7,69,3)
 if n==89:
  for fn in ['S960.md','S970.md']:
   ls=(P/pm/'supp_md'/fn).read_text().splitlines()
   for k,l in enumerate(ls,1):
    if k<5 or not l.startswith('|'):continue
    a=[c.strip().replace('\\','') for c in l.split('|')[1:-1]]
    try:has=any(float(v)>0 for v in a[1:])
    except ValueError:continue
    if has:
     adds += [(g,f'{fn[:-3]}:L{k}') for g in re.findall(r'\b[A-Z][a-z]+',re.split(r'[-‐–/]',a[0])[0]) if g in G]
 keys={re.split(r'[-_ ‐–—/]',g['name'])[0].casefold() for g in x['genera']}
 for g,eid in adds:
  key=g.casefold()
  if key not in keys:x['genera'].append(dict(name=g,evidence_id=eid,flagged_contaminant=False));keys.add(key)
 x['supplement_use']='Main text contained fewer than 3 target-site genera; added target-compartment supplemental detections only.'
 f.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');print(pm,'genera',len(x['genera']))
# Keep paper-specific values and support cues together in the reviewable curation manifest.
(B/'curation.json').write_text(json.dumps({ids[n-1]:c for n,c in configs.items()},ensure_ascii=False,indent=2)+'\n')
# Figure labels omitted by MarkItDown: verified manually against rendered source PDF.
import shutil
n=57;pm=ids[n-1];pdf=P/pm/'supp/gutjnl-2018-315988supp001.pdf';img=P/pm/'figure_review_S6_page9.png'
assert img.exists(), 'Retained verified Figure S6 rendering is required'
trans=P/pm/'supp_md/S990.md'
head=['# Verified figure transcription (derived, not original PDF text)',f'Source: {pdf.name}; PDF SHA256: {hashlib.sha256(pdf.read_bytes()).hexdigest()}',f'PDF page 9, supplementary Figure S6 panel A, explicitly labelled Amniotic fluid. Render SHA256: {hashlib.sha256(img.read_bytes()).hexdigest()}','Labels read visually by Codex on 2026-11-23. Original PDF and rendered page retained. Human verification pending.','']
trans.write_text('\n'.join(head+[g+' — Figure S6 A, amniotic-fluid row label' for g in configs[n]['visual_genera']])+'\n')
f=B/'records'/f'{pm}.json';x=json.loads(f.read_text());x['genera']=[dict(name=g,evidence_id=f'S990:L{i}',flagged_contaminant=False) for i,g in enumerate(configs[n]['visual_genera'],6)];x['figures_only']='yes';x['review_flags'].append('Genus evidence is an explicitly labelled manual figure transcription; original PDF page must be reviewed during human check.');x['supplement_use']='No securely attributable main-text AF genus list; used visually verified supplementary Figure S6 A.';f.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
(B/'PMC6109274_figure_manifest.json').write_text(json.dumps(dict(pdf=str(pdf),pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),render=str(img),render_sha256=hashlib.sha256(img.read_bytes()).hexdigest(),transcription=str(trans),transcription_sha256=hashlib.sha256(trans.read_bytes()).hexdigest(),page=9,figure='S6A',human_checked=False),indent=2)+'\n')
(B/'curation.json').write_text(json.dumps({ids[n-1]:c for n,c in configs.items()},ensure_ascii=False,indent=2)+'\n')
