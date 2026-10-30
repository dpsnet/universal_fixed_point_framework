# -*- coding: utf-8 -*-
"""M83c-TMAP：热端样本复核（>20000K——49 颗）——下载 tmap2 + EW + 回归"""
import urllib.request, json, os, sys
import numpy as np

base = 'E:/workspace/hyper-resolution/universal_fixed_point_framework'
sys.path.insert(0, base + '/src/white_dwarf_analysis')

LOG = base + '/scripts/_tmap_s3_log.txt'
def log(msg):
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')
    print(msg, flush=True)

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
        parts = line.split()
        if len(parts) >= 2:
            try:
                wl.append(float(parts[0])); fl.append(float(parts[1]))
            except ValueError:
                continue
    return wl, fl

# 数据
with open(base + '/scripts/paperX_wd_m83c_sample_list.json', encoding='utf-8') as f:
    samples = json.load(f)
with open(base + '/scripts/paperX_wd_m83c_tmap_fid.json', encoding='utf-8') as f:
    fid_tbl = json.load(f)
grid = {}
for k, v in fid_tbl.items():
    t, g = k.split('_')
    grid[(float(t), float(g))] = int(v)
teffs = sorted(set(t for t, g in grid))
loggs = sorted(set(g for t, g in grid))

def nearest(teff, logg):
    t = min(teffs, key=lambda x: abs(x - teff))
    g = min(loggs, key=lambda x: abs(x - logg))
    return t, g

import white_dwarf_analysis_v10 as v10
import numpy as np

cache_dir = base + '/scripts/_tmap_spec'
os.makedirs(cache_dir, exist_ok=True)
spec_cache = {}

hot = [s for s in samples if s['Teff'] > 20000]
log(f'热端样本: {len(hot)}')
n_dl = 0
for i, s in enumerate(hot):
    t, g = nearest(s['Teff'], s['logg'])
    fid = grid.get((t, g))
    if fid is None:
        s['tmap_EW'] = None; s['tmap_note'] = 'no_grid'; continue
    key = f'{t}_{g}'
    if key in spec_cache:
        s['tmap_EW'], s['tmap_n_det'] = spec_cache[key]; continue
    url = f'http://svo2.cab.inta-csic.es/theory/newov2/ssap.php?model=tmap2&fid={fid}&format=ascii'
    try:
        st, text = get(url)
        if st != 200 or len(text) < 5000:
            s['tmap_EW'] = None; s['tmap_note'] = f'dl_fail_{st}'; continue
        wl, fl = parse_ascii(text)
        if len(wl) < 100:
            s['tmap_EW'] = None; s['tmap_note'] = 'parse_fail'; continue
        wl_a, fl_a = np.array(wl), np.array(fl)
        nf = v10.normalize(wl_a, fl_a)
        tew = 0.0; nd = 0
        for ln, lw in v10.BALMER.items():
            ew, d = v10.measure_ew(wl_a, nf, lw)
            if d: tew += ew; nd += 1
        spec_cache[key] = (float(tew), nd)
        s['tmap_EW'] = float(tew); s['tmap_n_det'] = nd
        n_dl += 1
        with open(f'{cache_dir}/fid{fid}_{key}.dat', 'w', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        s['tmap_EW'] = None; s['tmap_note'] = f'err_{type(e).__name__}'
    if (i + 1) % 10 == 0:
        log(f'  进度 {i+1}/{len(hot)}（下载 {n_dl}）')

log(f'完成：下载 {n_dl} 光谱')

# 回归（热端 TMAP）
S = [s for s in hot if s.get('tmap_EW')]
S2 = []
for s in S:
    if s['obs_EW'] > 0 and s['tmap_EW'] > 0:
        s['resid_tmap'] = np.log10(s['obs_EW'] / s['tmap_EW'])
        s['log10B'] = np.log10(s['B_tesla'])
        S2.append(s)
log(f'残差有效: {len(S2)}（/ 热端 {len(hot)}）')

if len(S2) >= 20:
    from scipy import stats
    log10B = np.array([s['log10B'] for s in S2])
    resid = np.array([s['resid_tmap'] for s in S2])
    Teff = np.array([s['Teff'] for s in S2])
    logg = np.array([s['logg'] for s in S2])
    rho, p = stats.spearmanr(log10B, resid)
    log(f'\n=== TMAP NLTE 热端复核（>20kK，n={len(S2)}）===')
    log(f'Spearman rho = {rho:.3f}, p = {p:.2e}')
    X = np.column_stack([np.ones(len(S2)), log10B, Teff, logg])
    beta, res, rank, sv = np.linalg.lstsq(X, resid, rcond=None)
    n = len(S2); k = X.shape[1]; dof = n - k
    sse = float(np.sum((resid - X @ beta) ** 2))
    se = np.sqrt(sse / dof)
    se_beta = np.sqrt(np.diag(np.linalg.inv(X.T @ X))) * se
    t_vals = beta / se_beta
    p_vals = 2 * (1 - stats.t.cdf(np.abs(t_vals), dof))
    for nm, b, sb, t, pv in zip(['const', 'log10B', 'Teff', 'logg'], beta, se_beta, t_vals, p_vals):
        log(f'  {nm}: beta={b:.4f}±{sb:.4f}, t={t:.2f}, p={pv:.2e}')
    out = {'n': len(S2), 'rho': float(rho), 'p': float(p),
           'beta': {nm: float(b) for nm, b in zip(['const', 'log10B', 'Teff', 'logg'], beta)},
           'pvals': {nm: float(pv) for nm, pv in zip(['const', 'log10B', 'Teff', 'logg'], p_vals)}}
    with open(base + '/scripts/paperX_wd_m83c_tmap_reg.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    log('DONE -> paperX_wd_m83c_tmap_reg.json')
else:
    log(f'样本不足（{len(S2)}）——跳过回归')
