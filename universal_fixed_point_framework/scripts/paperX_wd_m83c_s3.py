# -*- coding: utf-8 -*-
"""M83c 步骤3：下载 Koester 光谱 + Balmer EW 计算（后台）
流程：样本 -> 最近网格点 -> fid -> 下载 ascii -> normalize -> measure_ew 五线 -> 理论总 EW
"""
import urllib.request, json, os, sys, time

base = 'E:/workspace/hyper-resolution/universal_fixed_point_framework'
sys.path.insert(0, base + '/src/white_dwarf_analysis')

LOG = base + '/scripts/_m83c_s3_log.txt'

def log(msg):
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')
    print(msg, flush=True)

def get(url, timeout=60):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', errors='replace')

def parse_ascii(text):
    """解析 Koester ascii 光谱 -> (wl[], fl[])"""
    wl, fl = [], []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split()
        if len(parts) >= 2:
            try:
                wl.append(float(parts[0]))
                fl.append(float(parts[1]))
            except ValueError:
                continue
    return wl, fl

# 1) 数据加载
with open(base + '/scripts/paperX_wd_m83c_sample_list.json', encoding='utf-8') as f:
    samples = json.load(f)
with open(base + '/scripts/paperX_wd_m83c_fid_table.json', encoding='utf-8') as f:
    fid_tbl = json.load(f)  # 'teff_logg' -> fid

# 网格键重建
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

# 2) 逐样本处理（网格点缓存）
cache_dir = base + '/scripts/_koester_spec'
os.makedirs(cache_dir, exist_ok=True)
spec_cache = {}

log(f'M83c 步骤3 启动：{len(samples)} 样本')
n_dl = 0
for i, s in enumerate(samples):
    t, g = nearest(s['Teff'], s['logg'])
    fid = grid.get((t, g))
    if fid is None:
        s['koester_EW'] = None
        s['koester_note'] = 'no_grid'
        continue
    key = f'{t}_{g}'
    if key in spec_cache:
        ew, det = spec_cache[key]
        s['koester_EW'] = ew
        s['koester_n_det'] = det
        continue
    # 下载
    url = f'http://svo2.cab.inta-csic.es/theory/newov2/ssap.php?model=koester2&fid={fid}&format=ascii'
    try:
        st, text = get(url)
        if st != 200 or len(text) < 5000:
            s['koester_EW'] = None
            s['koester_note'] = f'dl_fail_{st}'
            continue
        wl, fl = parse_ascii(text)
        if len(wl) < 100:
            s['koester_EW'] = None
            s['koester_note'] = 'parse_fail'
            continue
        # 用 v10 normalize + measure_ew 口径
        import white_dwarf_analysis_v10 as v10
        import numpy as np
        wl_a, fl_a = np.array(wl), np.array(fl)
        nf = v10.normalize(wl_a, fl_a)
        tew = 0.0
        nd = 0
        for ln, lw in v10.BALMER.items():
            ew, d = v10.measure_ew(wl_a, nf, lw)
            if d:
                tew += ew
                nd += 1
        spec_cache[key] = (float(tew), nd)
        s['koester_EW'] = float(tew)
        s['koester_n_det'] = nd
        n_dl += 1
        # 缓存文件（调试/复用）
        with open(f'{cache_dir}/fid{fid}_{key}.dat', 'w', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        s['koester_EW'] = None
        s['koester_note'] = f'err_{type(e).__name__}'
    if (i + 1) % 25 == 0:
        log(f'  进度 {i+1}/{len(samples)}（下载 {n_dl} 光谱）')

log(f'完成：下载 {n_dl} 光谱，缓存 {len(spec_cache)} 网格点')

# 3) 保存
out = {'n_samples': len(samples), 'n_with_koester': sum(1 for s in samples if s.get('koester_EW')),
       'n_downloaded': n_dl, 'samples': samples}
with open(base + '/scripts/paperX_wd_m83c_koester_ew.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
log('DONE -> paperX_wd_m83c_koester_ew.json')
