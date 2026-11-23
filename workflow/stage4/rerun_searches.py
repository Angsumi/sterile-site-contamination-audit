"""Stage 4: re-run the v1 and v2 searches unchanged (protocol section 4: 'will be re-run at the
start of full screening'). Same queries; only the output folder differs and the PubMed end date
is moved to the run date. Writes search/rerun_<date>/{v1,v2}/."""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import epmc, run_search, run_search_v2

day = time.strftime('%Y-%m-%d')
base = epmc.ROOT / 'search' / f'rerun_{day}'
for mod, sub in ((run_search, 'v1'), (run_search_v2, 'v2')):
    out = base / sub
    out.mkdir(parents=True, exist_ok=True)
    mod.OUT = out
    if hasattr(mod, 'YEARS_PM'):
        mod.YEARS_PM = mod.YEARS_PM.replace('2026/11/22', day.replace('-', '/'))
    print('==', sub, flush=True)
    mod.main()
