# -*- coding: utf-8 -*-
"""Phase 88 M88-1/2：Kepler 32 有效中场 SDSS 光谱下载 + 线级测量（Phase 87 管线适配）
输出：paperX_wd_kepler_linelevel.json（含 Koester R_sig/R_dep）
"""
import io, json, os, sys, time
import numpy as np
from scipy.optimize import curve_fit

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\src\white_dwarf_analysis")
import white_dwarf_analysis_v10 as v10

BALMER = v10.BALMER
LINE_C = {'Hbeta': 4861.3, 'Hgamma': 4340.5, 'Hdelta': 4101.7, 'Hepsilon': 3970.1, 'Hzeta': 3889.1}
_BW = sorted(BALMER.items(), key=lambda kv: kv[1])
HG = {}
for i, (nm, c) in enumerate(_BW):
    lo = _BW[i-1][1] if i > 0 else None
    hi = _BW[i+1][1] if i+1 < len(_BW) else None
    cand = [d for d in (None if lo is None else c-lo, None if hi is None else hi-c) if d]
    HG[nm] = min(cand) / 2.0 - 1.0

def gauss(x, d, x0, s):
    return d * np.exp(-(x - x0) ** 2 / (2 * s ** 2))

def fit_line(wl, nf, center, half_w, B_G=0.0):
    """Phase 87 同款：二次基线 + d_pure + 拟合 σ（SDSS 上限放宽 4 Å）"""
    m = (wl >= center - half_w) & (wl <= center + half_w)
    if np.sum(m) < 8:
        return None
    x, y = wl[m], 1.0 - nf[m]
    core = np.abs(x - center) < 12.0
    wing = ~core
    if wing.sum() >= 8:
        bb = np.polyfit(x[wing], y[wing], 2)
        yb = y - np.polyval(bb, x)
    else:
        yb = y - np.median(y)
    cm = np.abs(x - center) < 5.0
    d_meas = float(np.median(y[cm])) if np.sum(cm) > 0 else 0.0
    d_pure = float(np.median(yb[cm])) if np.sum(cm) > 0 else 0.0
    d0 = max(d_pure, 0.02)
    try:
        p, _ = curve_fit(gauss, x, yb, p0=[d0, center, 1.5],
                         bounds=([0.0, center - 4.0, 0.05], [2.0, center + 4.0, 4.0]),
                         maxfev=4000)
        d, x0, s = p
        resid = yb - gauss(x, d, x0, s)
        return {'d': float(d), 'sig': float(s), 'x0': float(x0),
                'd_meas': d_meas, 'd_pure': d_pure,
                'chi2': float(np.sum(resid ** 2)), 'ok': True, 'ndata': int(len(x))}
    except Exception:
        return None

# ---- Kepler 样本 ----
with io.open(os.path.join(BASE, "paperX_wd_m83d_kepler_sample.json"), "r", encoding="utf-8") as f:
    ksamp = json.load(f)
# 32 颗有效（obs_EW 有值且 >0）
valid = [s for s in ksamp if s.get("obs_EW")]
print("Kepler 采样 %d 颗，有效 %d 颗" % (len(ksamp), len(valid)))
mid = [s for s in valid if 10 <= s.get("B_MG", 0) < 100]
weak = [s for s in valid if s.get("B_MG", 0) < 10]
print("中场(10-100 MG): %d | 弱场(<10 MG): %d" % (len(mid), len(weak)))

# ---- Koester fid ----
with io.open(os.path.join(BASE, "paperX_wd_m83c_fid_table.json"), "r", encoding="utf-8") as f:
    fid_tbl = json.load(f)
grid = {}
for k, v in fid_tbl.items():
    t, g = k.split("_")
    grid[(float(t), float(g))] = int(v)
teffs = sorted(set(t for t, g in grid)); loggs = sorted(set(g for t, g in grid))
def nearest(teff, logg):
    return min(teffs, key=lambda x: abs(x - teff)), min(loggs, key=lambda x: abs(x - logg))
cache_dir = os.path.join(BASE, "_koester_spec")
def load_koester(teff, logg):
    t, g = nearest(teff, logg)
    fid = grid.get((t, g))
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
    return np.array(wl2), np.array(fl2)

# ---- 逐星逐线（SDSS 下载 + 测量）----
out = {"weak": [], "mid": []}
n_no = 0
for s in valid:
    gid = s.get("name", "?").replace("SDSS J", "")
    grp = "mid" if 10 <= s.get("B_MG", 0) < 100 else "weak"
    spec = v10.get_spec(s)
    if spec is None:
        n_no += 1
        continue
    wl_a, fl_a = spec
    wl_a = np.asarray(wl_a, dtype=float); fl_a = np.asarray(fl_a, dtype=float)
    good = np.isfinite(fl_a) & (fl_a > 0)
    if good.sum() < 500:
        n_no += 1
        continue
    w, f = wl_a[good], fl_a[good]
    nf = v10.normalize(w, f)
    km = load_koester(s["Teff"], s["logg"])
    nm = None
    if km is not None:
        nm = v10.normalize(km[0], km[1])
    star = {"gid": gid, "B_MG": s["B_MG"], "Teff": s["Teff"], "logg": s["logg"],
            "Sp-ID": s.get("Sp-ID"), "src": "kepler2013", "lines": {}}
    for ln in ("Hbeta", "Hgamma", "Hdelta", "Hepsilon"):
        c = LINE_C[ln]
        hw = min(60.0, HG.get(ln, 60.0))
        rA = fit_line(w, nf, c, hw)
        rM = fit_line(km[0], nm, c, hw) if nm is not None else None
        if rA is None or rA["d_pure"] < 0.03:
            continue
        rec = {"d_obs": rA["d"], "sig_obs": rA["sig"],
               "d_meas": rA["d_meas"], "d_pure": rA["d_pure"],
               "chi2_A": rA["chi2"]}
        if rM is not None and rM["d_pure"] > 0.03:
            rec["d_mod"] = rM["d"]; rec["sig_mod"] = rM["sig"]
            rec["d_pure_mod"] = rM["d_pure"]
        star["lines"][ln] = rec
    if star["lines"]:
        out[grp].append(star)
    time.sleep(0.3)
print("无光谱/无效: %d" % n_no)
print("弱场有效星: %d | 中场有效星: %d" % (len(out["weak"]), len(out["mid"])))

with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_kepler_linelevel.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written paperX_wd_kepler_linelevel.json")
