# -*- coding: utf-8 -*-
"""M83d 补全：将采样从 60 颗扩展至全部候选（10-300 MG、Teff 8000-40000、不重叠现有），
消除"60 采样"选择性口实。复用恢复脚本逻辑（增量保存）。"""
import urllib.request, json, os, sys, time, random
import numpy as np
import warnings
warnings.filterwarnings('ignore')

base = 'E:/workspace/hyper-resolution/universal_fixed_point_framework'
sys.path.insert(0, base + '/src/white_dwarf_analysis')
import white_dwarf_analysis_v10 as v10

LOG = base + '/scripts/_m83d_fill_log.txt'
PROG = base + '/scripts/_m83d_fill_progress.json'
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

# 1) 已有结果（60 颗）——避免重下
done_prev = {}
if os.path.exists(OUT):
    with open(OUT, 'r', encoding='utf-8') as f:
        prev = json.load(f)
    done_prev = {r['name']: r for r in prev}
log('已有结果 %d 颗' % len(done_prev))

# 2) 重建全部候选（同 s2 筛选：10-300MG、8000-40000K、去重现有 Amorim）
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
todo = [c for c in cand if c['name'] not in done_prev]
log('全候选 %d 颗，待补 %d 颗' % (len(cand), len(todo)))

# 3) Koester fid 网格
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

cache_dir = base + '/scripts/_koester_spec'
os.makedirs(cache_dir, exist_ok=True)
spec_cache = {}
from astroquery.sdss import SDSS

n_obs = 0
for i, s in enumerate(todo):
    nm = s['name']
    try:
        parts = s['Sp-ID'].split('-')
        sp = SDSS.get_spectra(plate=int(parts[0]), mjd=int(parts[1]), fiberID=int(parts[2]), timeout=60)
        if not sp or len(sp) == 0:
            s['status'] = 'no_spec'; s['note'] = 'no_spec'
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
            s['status'] = 'ok'; s['obs_EW'] = float(tew); s['n_detected'] = nd; s['balmer'] = br
            n_obs += 1
    except Exception as e:
        s['status'] = 'err'; s['error'] = str(e)[:100]
    # Koester EW（obs>0）
    if s.get('obs_EW', 0) > 0:
        t, g = nearest(s['Teff'], s['logg'])
        key = '%s_%s' % (t, g)
        if key in spec_cache:
            s['koester_EW'], s['koester_n_det'] = spec_cache[key]
        else:
            fid = grid.get((t, g))
            if fid is None:
                s['koester_note'] = 'no_grid'
            else:
                try:
                    st, text = get('http://svo2.cab.inta-csic.es/theory/newov2/ssap.php?model=koester2&fid=%s&format=ascii' % fid)
                    if st != 200 or len(text) < 5000:
                        s['koester_note'] = 'dl_fail_%s' % st
                    else:
                        wl2, fl2 = parse_ascii(text)
                        if len(wl2) < 100:
                            s['koester_note'] = 'parse_fail'
                        else:
                            wl_a, fl_a = np.array(wl2), np.array(fl2)
                            nf2 = v10.normalize(wl_a, fl_a)
                            tew2 = 0.0; nd2 = 0
                            for ln, lw in v10.BALMER.items():
                                ew2, det2 = v10.measure_ew(wl_a, nf2, lw)
                                if det2:
                                    tew2 += ew2; nd2 += 1
                            spec_cache[key] = (float(tew2), nd2)
                            s['koester_EW'], s['koester_n_det'] = float(tew2), nd2
                            with open('%s/fid%s_%s.dat' % (cache_dir, fid, key), 'w', encoding='utf-8') as f:
                                f.write(text)
                except Exception as e2:
                    s['koester_note'] = 'err_%s' % type(e2).__name__
    if s.get('obs_EW', 0) > 0 and s.get('koester_EW'):
        s['resid'] = float(np.log10(s['obs_EW'] / s['koester_EW']))
    with open(PROG, 'w', encoding='utf-8') as f:
        json.dump({c['name']: {k: c[k] for k in ('status','obs_EW','n_detected','koester_EW','resid','note','error') if k in c} for c in todo[:i+1]}, f, ensure_ascii=False)
    if (i + 1) % 10 == 0:
        log('进度 %d/%d（有谱 %d）' % (i + 1, len(todo), n_obs))

log('补全下载完成：%d/%d 有光谱' % (n_obs, len(todo)))

# 4) 合并全部（已有 60 + 新增）+ 回归
merged = []
for c in cand:
    if c['name'] in done_prev:
        merged.append(done_prev[c['name']])
    else:
        c2 = dict(c)
        for k in ('status','obs_EW','n_detected','balmer','koester_EW','koester_n_det','resid','note','error'):
            if k in c:
                c2[k] = c[k]
        merged.append(c2)
merged.sort(key=lambda r: r['B_MG'])
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(merged, f, ensure_ascii=False, indent=1)

recs = [r for r in merged if r.get('obs_EW') and r.get('koester_EW')]
log('合并：总 %d，obs>0 %d，koester+resid %d' % (len(merged), sum(1 for r in merged if r.get('obs_EW',0)>0), len(recs)))
print('全候选有效残差 n =', len(recs))
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
    print('全候选 OLS: log10B %.3f (t=%.2f) Teff %.2e logg %.3f ; Spearman rho=%.3f p=%.3e' % (beta[1], t[1], beta[2], beta[3], rho, p))
    with open(base + '/scripts/_m83d_regression.json', 'w', encoding='utf-8') as f:
        json.dump({'n': int(len(recs)), 'log10B': float(beta[1]), 't': float(t[1]), 'Teff': float(beta[2]), 'logg': float(beta[3]), 'rho': float(rho), 'p': float(p), 'B_MG_range': [min(r['B_MG'] for r in recs), max(r['B_MG'] for r in recs)]}, f, indent=1)
log('DONE 全候选')
