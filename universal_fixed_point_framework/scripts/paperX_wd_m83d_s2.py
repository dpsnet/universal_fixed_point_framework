# -*- coding: utf-8 -*-
"""M83d：Kepler 2013 强场补充样本——采样 + 下载 + Koester EW + 强场端残差"""
import urllib.request, json, os, sys, time, random
import numpy as np

base = 'E:/workspace/hyper-resolution/universal_fixed_point_framework'
sys.path.insert(0, base + '/src/white_dwarf_analysis')

LOG = base + '/scripts/_m83d_log.txt'
def log(msg):
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')
    print(msg, flush=True)

def fnum(r, k):
    try:
        return float(str(r.get(k, '')).strip())
    except (TypeError, ValueError):
        return None

# 1) 现有样本（去重）
with open(base + '/scripts/paperX_wd_m83c_sample_list.json', encoding='utf-8') as f:
    existing = json.load(f)
exist_ids = set()
for s in existing:
    nm = s['name'].replace('SDSS ', '').replace('J', '')
    exist_ids.add(nm)
log(f'现有样本: {len(existing)}')

# 2) Kepler 2013 采样
with open(base + '/scripts/paperX_wd_m83d_kepler2013.json', encoding='utf-8') as f:
    k2013 = json.load(f)
cand = []
for r in k2013:
    B = fnum(r, 'BHa')
    Teff = fnum(r, 'Teff')
    logg = fnum(r, 'logg')
    sdss = str(r.get('SDSS', '')).strip().replace('J', '')
    if B is None or Teff is None or logg is None:
        continue
    if not (10 <= B <= 300):      # 10-300 MG（补充强场档）
        continue
    if not (8000 <= Teff <= 40000):
        continue
    if sdss in exist_ids:
        continue
    cand.append({'name': 'SDSS J' + sdss, 'B_tesla': B * 100.0,  # MG -> T
                 'Teff': Teff, 'logg': logg,
                 'Sp-ID': f"{r['Plate']}-{r['MJD']}-{r['Fiber']}",
                 'src': 'kepler2013', 'B_MG': B})
log(f'Kepler 候选（10-300MG、温度域重叠、不重叠现有）: {len(cand)}')

random.seed(42)
random.shuffle(cand)
sel = cand[:60]
log(f'采样: {len(sel)} 颗')

# 3) 下载 + EW
def get_spec(star, max_retries=2):
    import warnings
    try:
        import astropy
    except ImportError:
        pass
    parts = star['Sp-ID'].split('-')
    if len(parts) != 3:
        return None
    try:
        from astropy.io import fits
        # SDSS 光谱接口（同 v10 方式）
        import sdss as sdss_mod
    except ImportError:
        return None
    # 直接用 v10 的 get_spec
    import white_dwarf_analysis_v10 as v10
    return v10.get_spec(star)

spec_cache = {}
n_dl = 0
for i, s in enumerate(sel):
    try:
        import white_dwarf_analysis_v10 as v10
        spec = v10.get_spec(s)
        if spec is None:
            s['koester_EW'] = None; s['note'] = 'no_spec'
            log(f'  [{i+1}/{len(sel)}] {s["name"]}: 无光谱')
            continue
        wl, fl = spec
        wl_a, fl_a = np.array(wl), np.array(fl)
        nf = v10.normalize(wl_a, fl_a)
        tew = 0.0; nd = 0; br = {}
        for ln, lw in v10.BALMER.items():
            ew, d = v10.measure_ew(wl_a, nf, lw)
            br[ln] = {'EW': ew, 'detected': d}
            if d: tew += ew; nd += 1
        s['obs_EW'] = float(tew); s['n_detected'] = nd; s['balmer'] = br
        # Koester 理论 EW（最近网格点——用缓存 fid 表）
        s['koester_EW'] = None
        n_dl += 1
    except Exception as e:
        s['obs_EW'] = None; s['note'] = f'err_{type(e).__name__}'
    if (i + 1) % 10 == 0:
        log(f'  进度 {i+1}/{len(sel)}（成功 {n_dl}）')

log(f'下载完成：{n_dl}/{len(sel)} 有光谱')

# 4) 保存
with open(base + '/scripts/paperX_wd_m83d_kepler_sample.json', 'w', encoding='utf-8') as f:
    json.dump(sel, f, ensure_ascii=False, indent=1)
log('DONE -> paperX_wd_m83d_kepler_sample.json')
