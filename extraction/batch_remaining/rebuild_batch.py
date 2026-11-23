from pathlib import Path
import sys,json,re,csv,hashlib,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2];P=R/'papers';B=R/'extraction/batch_remaining'
sys.path.insert(0,str(R/'workflow'));import epmc
sys.path.insert(0,str(R/'workflow/stage4'));import check_one
rawcuration=json.loads((B/'curation.json').read_text())
ids=[r['pmcid'] for r in json.loads((B/'selection.json').read_text())];configs={n:rawcuration[p] for n,p in enumerate(ids,1)};G={r['name'] for r in csv.DictReader(open(R/'reference/ncbi_genera.tsv'),delimiter='\t') if r['domain']=='Bacteria'}
norm=lambda s:re.sub(r'\s+',' ',s.replace('\\','')).strip().lower()
def splitval(s):
 a=s.split(':',1);return a[0],a[1] if len(a)>1 else None

# Resolve the reviewed design values to explicit Markdown locators.
for _n,_cfg in configs.items():
 _ls=(P/ids[_n-1]/'fulltext.md').read_text().splitlines()
 if _cfg.get('exclude'):continue
 _m=_cfg['method']
 _pat={'16S':r'16\s*S|ribosomal', 'shotgun':r'shotgun|metagenom|whole.genome', 'host_seq_mining':r'RNA.seq|RNA.sequenc|TCGA|scRNA|WGS', '2bRAD-M':r'2bRAD', '16S+shotgun':r'metagenom|16\s*S'}.get(_m,r'sequenc|WGS|16\s*S')
 _sec='';_hits=[]
 for _k,_l in enumerate(_ls,1):
  if _l.startswith('#'):_sec=_l;continue
  if any(t in _sec.lower() for t in ['introduction','discussion','reference','background']):continue
  if re.search(_pat,_l,re.I):_hits.append(_k)
 _mk=_cfg.get('method_line') or (_cfg.get('public') if _m=='host_seq_mining' else None) or (_hits[0] if _hits else None)
 if _mk is None:raise ValueError(f'No method locator {_n}')
 _cfg['method']=f'{_m}:{_mk}'
 for _field,_line in [('controls','control_line'),('decon','decon_line'),('qpcr','qpcr_line')]:
  if _cfg.get(_line):_cfg[_field]+=':'+str(_cfg[_line])
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
 x=dict(pmcid=pm,tissue_category=cfg['tissue'],sub_site=cfg['site'],year=int(years[0]) if years else None,country='',eligible_fulltext=not bool(cfg.get('exclude')),exclusion_reason=cfg.get('exclude',''),extractor='Codex single-agent Markdown remaining corpus; provisional AI first pass',date='2026-11-23',source_markdown_sha256=hashlib.sha256((P/pm/'fulltext.md').read_bytes()).hexdigest())
 try:
  if cfg.get('exclude'):
   x['notes']=cfg.get('notes','')
   x['review_flags']=[cfg['review_taxonomy']] if cfg.get('review_taxonomy') else []
   if cfg.get('overlap_with'):x.update(eligible_fulltext_before_cohort_exclusion=True,overlap_with=cfg['overlap_with'],cohort_exclusion_evidence=evidence(cfg['scope_line'],'previous|studied herein'))
  if not cfg.get('exclude'):
   m,mk=splitval(cfg['method']);c,ck=splitval(cfg['controls']);d,dk=splitval(cfg['decon']);q,qk=splitval(cfg['qpcr'])
   x.update(data_source=dict(value='public_reuse' if cfg.get('public') else 'own_samples',dataset=cfg.get('dataset',''),evidence=evidence(cfg['public'],'TCGA|download|cohort|sequenc') if cfg.get('public') else []),
    method=dict(value=m,region='',evidence=evidence(mk,{'16S':r'16\s?S|ribosomal','2bRAD-M':'2bRAD','host_seq_mining':'RNA.sequenc|RNA.seq|TCGA|non.human|unmapped|WGS|microbial abundance','shotgun':'metagenom|sequencing','metatranscriptomic':'metatranscript','16S+shotgun':r'16\s?S|shotgun'}.get(m,'16S|RNA'))),
    controls=dict(value=c,types='negative controls as cited' if ck else '',n_sequenced=None,evidence=evidence(ck,'negative|blank|control') if ck else []),
    decontamination=dict(value=d,tool=cfg.get('decon_tool',''),evidence=evidence(dk,r'decontam|SCRuB|SourceTracker|remov[^.]{0,100}(?:control|contamina)|exclud[^.]{0,100}(?:control|contamina)|contamina[^.]{0,100}(?:remov|exclud)|threshold|filter') if dk else []),
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

# Source-author-defined per-cancer strata only; excludes mucosal primary cancers.
allowed={'ACC','BRCA','CHOL','DLBC','GBM','KICH','KIRC','KIRP','LGG','LIHC','LUAD','LUSC','MESO','OV','PAAD','PCPG','PRAD','SARC','SKCM','TGCT','THCA','THYM','UCEC','UCS','UVM'}
cells=lambda l:[c.strip().replace('\\','') for c in l.split('|')[1:-1]]
for n,fn in [(54,'S960.md'),(70,'S910.md'),(75,'S3.md'),(96,'S2.md')]:
 pm=ids[n-1];f=B/'records'/f'{pm}.json';x=json.loads(f.read_text());ls=(P/pm/'supp_md'/fn).read_text().splitlines();adds=[];support=[]
 if n==54:
  for k,l in enumerate(ls,1):
   a=cells(l)
   if k>3 and len(a)>5:
    g=a[4]
    if g in G:adds.append((g,f'{fn[:-3]}:L{k}'))
 if n==70:
  for k,l in enumerate(ls,1):
   if not l.startswith('|'):continue
   for g in re.findall(r'g__([A-Z][a-z]+)',l.replace('\\','')):
    if g in G:adds.append((g,f'{fn[:-3]}:L{k}'))
 if n==75:
  for k,l in enumerate(ls,1):
   a=cells(l)
   if k>4 and len(a)>=3 and a[2] in allowed:
    g=a[0].removeprefix('Candidatus ')
    if g in G:adds.append((g,f'{fn[:-3]}:L{k}'));support.append(dict(line=k,cancer=a[2],label=a[0]))
 if n==96:
  # S01 provides patient-to-cancer mappings; S03/S04 contain species abundance columns.
  meta={}
  for k in range(35,2363):
   a=cells(ls[k-1])
   if len(a)>=3 and a[2].removeprefix('TCGA-') in allowed:meta[a[1]]=(a[2],k)
  for hk,start,end in [(2721,2723,4558),(4560,4562,6862)]:
   header=cells(ls[hk-1]);positive={}
   for k in range(start,end+1):
    a=cells(ls[k-1])
    if not a or a[0] not in meta:continue
    for c,v in enumerate(a[1:],1):
     try:val=float(v)
     except ValueError:continue
     if val>0 and c not in positive:positive[c]=(k,a[0],meta[a[0]])
   for c,(k,sample,(cancer,mk)) in positive.items():
    if c>=len(header):continue
    label=header[c];g=re.split('[_ ]',label)[0]
    if g in G:
     adds.append((g,f'{fn[:-3]}:L{hk}'));support.append(dict(label=label,header_line=hk,positive_abundance_line=k,sample=sample,cancer=cancer,metadata_line=mk))
 keys={re.split(r'[-_ ‐–—/]',g['name'])[0].casefold() for g in x['genera']}
 for g,eid in adds:
  if g.casefold() not in keys:x['genera'].append(dict(name=g,evidence_id=eid,flagged_contaminant=False));keys.add(g.casefold())
 x['supplement_use']='Fewer than 3 securely attributable target-site genera in main text; supplementary table restricted to target samples or eligible cancer strata.'
 if n==96:x['notes']+=' Supplement abundance rows matched to eligible cancer types via the same supplement patient metadata; only positive entries used, with row links retained in the support manifest.'
 f.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
 (B/f'{pm}_supplement_support.json').write_text(json.dumps(support,ensure_ascii=False,indent=2)+'\n')
 print(n,pm,'genera',len(x['genera']))
(B/'curation.json').write_text(json.dumps({ids[n-1]:c for n,c in configs.items()},ensure_ascii=False,indent=2)+'\n')
# The supplementary PDF has graphical labels not preserved by MarkItDown.
import shutil
n=4;pm=ids[n-1];pdf=P/pm/'supp/microorganisms-08-00794-s001.pdf';img=P/pm/'figure_review_S3_page2.png'
assert img.exists(), 'Retained verified Figure S3 rendering is required'
trans=P/pm/'supp_md/S990.md'
head=['# Verified figure transcription (derived, not original PDF text)',f'Source {pdf.name}; PDF SHA256 {hashlib.sha256(pdf.read_bytes()).hexdigest()}',f'PDF page 2, supplementary Figure S3; light-grey bar indicates lung tissue. Render SHA256 {hashlib.sha256(img.read_bytes()).hexdigest()}','Genus labels with visible positive readcount in lung tissue. Dark-grey airway-only Cloacibacterium and family/unclassified labels excluded.','Visual reading by Codex 2026-11-23; independent human verification pending.']
trans.write_text('\n'.join(head+[g+' — Figure S3, positive lung-tissue heatmap signal' for g in configs[n]['visual_genera']])+'\n')
f=B/'records'/f'{pm}.json';x=json.loads(f.read_text());x['genera']=[dict(name=g,evidence_id=f'S990:L{k}',flagged_contaminant=False) for k,g in enumerate(configs[n]['visual_genera'],6)];x['supplement_use']='Main text had fewer than three attributable lung-tissue genera; visually verified supplementary Figure S3 used.';x['review_flags'].append('Manual figure transcription requires independent human verification; source PDF and rendering retained.');f.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
(B/f'{pm}_figure_manifest.json').write_text(json.dumps(dict(pdf=str(pdf),pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),render=str(img),render_sha256=hashlib.sha256(img.read_bytes()).hexdigest(),transcription=str(trans),transcription_sha256=hashlib.sha256(trans.read_bytes()).hexdigest(),figure='S3',page=2,human_checked=False),indent=2)+'\n')
(B/'curation.json').write_text(json.dumps({ids[n-1]:c for n,c in configs.items()},ensure_ascii=False,indent=2)+'\n')
