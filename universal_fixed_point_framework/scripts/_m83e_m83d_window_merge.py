# -*- coding: utf-8 -*-
"""Phase 74 合并：DESI + Kepler 窗口扫描统一回归（protect 口径）
- 理论 EW：每星最近网格点 Koester 谱 + 同窗口 total_ew（统一口径）
- 每窗口：合并 OLS（目录固定效应 + 目录×log10B 交互）+ Spearman
- 输出 _m83e_m83d_window_merge.json
"""
import io, json, os, sys
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\src\white_dwarf_analysis")
import white_dwarf_analysis_v10 as v10

WINDOWS = [80.0, 160.0, 320.0]
from scipy.stats import spearmanr

with io.open(os.path.join(BASE, "_m83e_window_scan.json"), "r", encoding="utf-8") as f:
    d1 = json.load(f)
with io.open(os.path.join(BASE, "_m83d_window_scan.json"), "r", encoding="utf-8") as f:
    d2 = json.load(f)

# Koester 网格
with io.open(os.path.join(BASE, "paperX_wd_m83c_fid_table.json"), "r", encoding="utf-8") as f:
    fid_tbl = json.load(f)
grid = {}
for k, v in fid_tbl.items():
    t, g = k.split("_")
    grid[(float(t), float(g))] = int(v)
teffs = sorted(set(t for t, g in grid)); loggs = sorted(set(g for t, g in grid))
def nearest(teff, logg):
    return min(teffs, key=lambda x: abs(x-teff)), min(loggs, key=lambda x: abs(x-logg))

cache_dir = os.path.join(BASE, "_koester_spec")
_spec = {}
def load_koester(teff, logg):
    t, g = nearest(teff, logg)
    key = (t, g)
    if key in _spec:
        return _spec[key]
    fid = grid.get(key)
    if fid is None:
        return None
    fp = os.path.join(cache_dir, "fid%s_%s_%s.dat" % (fid, t, g))
    if not os.path.exists(fp):
        return None
    wl2, fl2 = [], []
    with io.open(fp, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            p = line.split()
            if len(p) >= 2:
                try:
                    wl2.append(float(p[0])); fl2.append(float(p[1]))
                except ValueError:
                    pass
    if len(wl2) < 100:
        return None
    wl_a, fl_a = np.array(wl2), np.array(fl2)
    nf2 = v10.normalize(wl_a, fl_a)
    _spec[key] = (wl_a, nf2)
    return _spec[key]

_BW = sorted(v10.BALMER.items(), key=lambda kv: kv[1])
def half_gaps():
    hg = {}
    for i, (nm, c) in enumerate(_BW):
        lo = _BW[i-1][1] if i > 0 else None
        hi = _BW[i+1][1] if i+1 < len(_BW) else None
        cand = [d for d in (None if lo is None else c-lo, None if hi is None else hi-c) if d]
        hg[nm] = min(cand) / 2.0 - 1.0
    return hg
HG = half_gaps()

def measure_ew_w(wl, fl, center, window):
    m = (wl >= center-window) & (wl <= center+window)
    if np.sum(m) < 5:
        return 0.0, False
    w, f = wl[m], fl[m]
    ew = float(np.trapezoid(1.0 - f, w))
    cm = np.abs(w-center) < 5
    depth = 1.0 - np.median(f[cm]) if np.sum(cm) > 0 else 0
    return ew, (ew > 0.5 and depth > 0.03)

def total_ew(wl, nf, window, protect=True):
    tew, nd = 0.0, 0
    for nm, c in v10.BALMER.items():
        weff = min(window, HG[nm]) if protect else window
        ew, det = measure_ew_w(wl, nf, c, weff)
        if det:
            tew += ew; nd += 1
    return tew, nd

_theo_cache = {}
def theo_ew(teff, logg, window):
    key = ("%s_%s" % (teff, logg), int(window))
    if key in _theo_cache:
        return _theo_cache[key]
    k = load_koester(teff, logg)
    if k is None:
        _theo_cache[key] = None
        return None
    wl_a, nf2 = k
    tew, nd = total_ew(wl_a, nf2, window, protect=True)
    _theo_cache[key] = (float(tew), nd)
    return _theo_cache[key]

def build(star_ews, window, cat):
    recs = []
    for gid, st in star_ews.items():
        obs = st["p"][str(int(window))]["tew"]
        if obs <= 0:
            continue
        th = theo_ew(st["Teff"], st["logg"], window)
        if th is None or th[0] <= 0:
            continue
        recs.append({"id": gid, "B_MG": st["B_MG"], "Teff": st["Teff"], "cat": cat,
                     "obs_EW": obs, "koester_EW": th[0],
                     "resid": float(np.log10(obs/th[0]))})
    return recs

out = {}
for W in WINDOWS:
    r1 = build(d1["star_ews"], W, "DESI")
    r2 = build(d2["star_ews"], W, "Kepler")
    recs = r1 + r2
    if len(recs) < 5:
        out[str(int(W))] = {"n": len(recs), "note": "too_few"}
        continue
    X = np.array([[np.log10(r["B_MG"]*100.0), r["Teff"],
                   1.0 if r["cat"] == "Kepler" else 0.0,
                   np.log10(r["B_MG"]*100.0) * (1.0 if r["cat"] == "Kepler" else 0.0)] for r in recs], dtype=float)
    y = np.array([r["resid"] for r in recs], dtype=float)
    Xc = X - X.mean(axis=0)
    Xc[:, 2] = X[:, 2]
    Xc[:, 3] = X[:, 3] - X[:, 3].mean()
    Xd = np.column_stack([np.ones(len(y)), Xc])
    rank = np.linalg.matrix_rank(Xd)
    beta, _, rank2, _ = np.linalg.lstsq(Xd, y, rcond=None)
    resid = y - Xd @ beta
    dof = len(y) - rank
    s2 = resid @ resid / dof if dof > 0 else 0.0
    try:
        se = np.sqrt(np.diag(s2 * np.linalg.inv(Xd.T @ Xd)))
        t = beta / se
    except Exception:
        t = np.full(len(beta), np.nan)
    rho, p = spearmanr(np.log10([r["B_MG"]*100.0 for r in recs]), y)
    out[str(int(W))] = {
        "n": len(recs), "n_desi": len(r1), "n_kepler": len(r2),
        "log10B": float(beta[1]), "t_log10B": float(t[1]),
        "kepler_dummy": float(beta[3]), "t_kepler_dummy": float(t[3]),
        "kepler_x_B": float(beta[4]), "t_kepler_x_B": float(t[4]),
        "rho": float(rho), "p": float(p),
        "B_range_MG": [min(r["B_MG"] for r in recs), max(r["B_MG"] for r in recs)],
    }
    print("W=%d: n=%d (D%d+K%d) log10B=%.3f t=%.2f rho=%.3f p=%.3e | kepler_xB=%.3f t=%.2f" % (
        W, len(recs), len(r1), len(r2), beta[1], t[1], rho, p, beta[4], t[4]))

with io.open(os.path.join(BASE, "_m83e_m83d_window_merge.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("saved merge")
