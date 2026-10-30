# -*- coding: utf-8 -*-
"""M83d 恢复：60 颗重跑（下载 + obs_EW + Koester EW + 强场端残差回归），增量保存防中断。"""
import urllib.request, json, os, sys, time, random
import numpy as np
import warnings
warnings.filterwarnings('ignore')

base = 'E:/workspace/hyper-resolution/universal_fixed_point_framework'
sys.path.insert(0, base + '/src/white_dwarf_analysis')
import white_dwarf_analysis_v10 as v10

LOG = base + '/scripts/_m83d_recover_log.txt'
PROG = base + '/scripts/_m83d_recover_progress.json'
OUT = base + '/scripts/paperX_wd_m83d_kepler_sample.json'

def log(msg):
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')
    print(msg, flush=True)

def fnum(r, k):
    try:
        return float(str(r.get(k, '')).strip())
    except (TypeError, ValueError):
        return None

# 1) 现有样本去重 + Kepler 采样（同 s2：seed 42）
with open(base + '/scripts/paperX_wd_m83c_sample_list.json', encoding='utf-8') as f:
    existing = json.load(f)
exist_ids = set(s['name'].replace('SDSS ', '').replace('J', '') for s in existing)

with open(base + '/scripts/paperX_wd_m83d_kepler2013.json', encoding='utf-8') as f:
    k2013 = json.load(f)
cand = []
for r in k2013:
    B, Teff, logg = fnum(r, 'BHa'), fnum(r, 'Teff'), fnum(r, 'logg')
    sdss = str(r.get('SDSS', '')).strip().replace('J', '')
    if B is None or Teff is None or logg is None:
        continue
    if not (10 <= B <= 300) or not (8000 <= Teff <= 40000) or sdss in exist_ids:
        continue
    cand.append({'name': 'SDSS J' + sdss, 'B_tesla': B * 100.0, 'Teff': Teff, 'logg': logg,
                 'Sp-ID': "%d-%d-%d" % (int(r['Plate']), int(r['MJD']), int(r['Fiber'])),
                 'src': 'kepler2013', 'B_MG': B})
random.seed(42); random.shuffle(cand)
sel = cand[:60]
log('采样 %d 颗（候选 %d）' % (len(sel), len(cand)))

# 2) Koester fid 网格（复用）
with open(base + '/scripts/paperX_wd_m83c_fid_table.json', encoding='utf-8') as f:
    fid_tbl = json.load(f)
grid = {}
for k, v in fid_tbl.items():
    t, g = k.split('_')
    grid[(float(t), float(g))] = int(v)
teffs = sorted(set(t for t, g in grid)); loggs = sorted(set(g for t, g in grid))
def nearest(teff, logg):
    return min(teffs, key=lambda x: abs(x - teff)), min(loggs, key=lambda x: abs(x - logg))

def get(url, timeout=60):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', errors='replace')

def parse_ascii(text):
    wl, fl = [], []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        p = line.split()
        if len(p) >= 2:
            try:
                wl.append(float(p[0])); fl.append(float(p[1]))
            except ValueError:
                pass
    return wl, fl

# 3) 恢复进度（增量）
done = {}
if os.path.exists(PROG):
    with open(PROG, 'r', encoding='utf-8') as f:
        done = json.load(f)

cache_dir = base + '/scripts/_koester_spec'
os.makedirs(cache_dir, exist_ok=True)

from astroquery.sdss import SDSS
n_obs = 0
for i, s in enumerate(sel):
    nm = s['name']
    if nm in done and done[nm].get('status') in ('ok', 'no_spec', 'err'):
        if done[nm].get('obs_EW') is not None:
            n_obs += 1
        continue
    try:
        parts = s['Sp-ID'].split('-')
        sp = SDSS.get_spectra(plate=int(parts[0]), mjd=int(parts[1]), fiberID=int(parts[2]), timeout=60)
        if not sp or len(sp) == 0:
            done[nm] = {'status': 'no_spec', 'note': 'no_spec'}
        else:
            d = sp[0][1].data
            wl = 10.0 ** d['loglam']
            fl = np.array(d['flux'], dtype=float)
            nf = v10.normalize(wl, fl)
            tew = 0.0; nd = 0; br = {}
            for ln, lw in v10.BALMER.items():
                ew, det = v10.measure_ew(wl, nf, lw)
                br[ln] = {'EW': float(ew), 'detected': bool(det)}
                if det:
                    tew += ew; nd += 1
            done[nm] = {'status': 'ok', 'obs_EW': float(tew), 'n_detected': nd, 'balmer': br}
            n_obs += 1
    except Exception as e:
        done[nm] = {'status': 'err', 'error': str(e)[:100]}
    if (i + 1) % 10 == 0:
        with open(PROG, 'w', encoding='utf-8') as f:
            json.dump(done, f, ensure_ascii=False)
        log('obs 进度 %d/%d（有谱 %d）' % (i + 1, len(sel), n_obs))

log('obs 下载完成：%d/%d 有光谱' % (n_obs, len(sel)))

# 4) Koester EW（对有 obs_EW>0 的）
spec_cache = {}
n_k = 0
for s in sel:
    nm = s['name']
    if done[nm].get('status') != 'ok' or not done[nm].get('obs_EW', 0) or done[nm].get('koester_EW') is not None:
        continue
    t, g = nearest(s['Teff'], s['logg'])
    key = '%s_%s' % (t, g)
    if key in spec_cache:
        done[nm]['koester_EW'], done[nm]['koester_n_det'] = spec_cache[key]
        continue
    fid = grid.get((t, g))
    if fid is None:
        done[nm]['koester_note'] = 'no_grid'; continue
    url = 'http://svo2.cab.inta-csic.es/theory/newov2/ssap.php?model=koester2&fid=%s&format=ascii' % fid
    try:
        st, text = get(url)
        if st != 200 or len(text) < 5000:
            done[nm]['koester_note'] = 'dl_fail_%s' % st; continue
        wl, fl = parse_ascii(text)
        if len(wl) < 100:
            done[nm]['koester_note'] = 'parse_fail'; continue
        wl_a, fl_a = np.array(wl), np.array(fl)
        nf = v10.normalize(wl_a, fl_a)
        tew = 0.0; nd = 0
        for ln, lw in v10.BALMER.items():
            ew, det = v10.measure_ew(wl_a, nf, lw)
            if det:
                tew += ew; nd += 1
        spec_cache[key] = (float(tew), nd)
        done[nm]['koester_EW'], done[nm]['koester_n_det'] = float(tew), nd
        n_k += 1
        with open('%s/fid%s_%s.dat' % (cache_dir, fid, key), 'w', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        done[nm]['koester_note'] = 'err_%s' % type(e).__name__
    with open(PROG, 'w', encoding='utf-8') as f:
        json.dump(done, f, ensure_ascii=False)

log('Koester EW：%d 颗完成' % n_k)

# 5) 合并输出 + 回归
out = []
for s in sel:
    nm = s['name']
    r = dict(s)
    d = done.get(nm, {})
    r['status'] = d.get('status')
    if d.get('obs_EW') is not None:
        r['obs_EW'] = d['obs_EW']; r['n_detected'] = d['n_detected']; r['balmer'] = d['balmer']
        if d.get('koester_EW') is not None:
            r['koester_EW'] = d['koester_EW']; r['koester_n_det'] = d['koester_n_det']
            r['resid'] = float(np.log10(d['obs_EW'] / d['koester_EW']))
    else:
        r['note'] = d.get('note') or d.get('error')
    out.append(r)

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
log('DONE -> paperX_wd_m83d_kepler_sample.json（%d 颗，obs>0 %d，koester %d）' % (len(out), n_obs, n_k))

# 6) 强场端回归（obs_EW>0 且有 koester_EW）
recs = [r for r in out if r.get('obs_EW') and r.get('koester_EW')]
print('强场有效残差 n =', len(recs))
if len(recs) >= 5:
    X = np.array([[np.log10(r['B_tesla']), r['Teff'], r['logg']] for r in recs], dtype=float)
    y = np.array([r['resid'] for r in recs], dtype=float)
    Xc = X - X.mean(axis=0)
    Xd = np.column_stack([np.ones(len(y)), Xc])
    beta = np.linalg.solve(Xd.T @ Xd, Xd.T @ y)
    resid = y - Xd @ beta
    s2 = resid @ resid / (len(y) - 4)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(Xd.T @ Xd)))
    t = beta / se
    from scipy.stats import spearmanr
    rho, p = spearmanr(Xc[:, 0], y)
    print('强场 OLS: log10B %.3f (t=%.2f) Teff %.2e logg %.3f ; Spearman rho=%.3f p=%.3e' % (beta[1], t[1], beta[2], beta[3], rho, p))
    with open(base + '/scripts/_m83d_regression.json', 'w', encoding='utf-8') as f:
        json.dump({'n': int(len(recs)), 'log10B': float(beta[1]), 't': float(t[1]), 'Teff': float(beta[2]), 'logg': float(beta[3]), 'rho': float(rho), 'p': float(p)}, f, indent=1)
