# -*- coding: utf-8 -*-
"""Phase 89b M89b-1：DESI 强场样本（B>=100 MG，4 颗有缓存）线级测量 + 理论对照
复用 Phase 87 管线（fit_line/二次基线/d_pure/Zeeman 三分量/模型谱）
输出：paperX_wd_linelevel_strong.json + 对照表
"""
import io, json, os, sys
import numpy as np
from scipy.optimize import curve_fit

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\src\white_dwarf_analysis")
import white_dwarf_analysis_v10 as v10

BALMER = v10.BALMER
LINES = ['Hbeta', 'Hgamma', 'Hdelta', 'Hepsilon', 'Hzeta']
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

def fit_line(wl, nf, center, half_w, use_zeeman=False, B_G=0.0):
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
    fwhm = float('nan')
    if d_pure > 0.04:
        hm = d_pure / 2.0
        cent = int(np.argmin(np.abs(x - center)))
        j = cent
        while j > 0 and yb[j] >= hm:
            j -= 1
        lh = None
        if j < cent and j + 1 < len(x):
            if yb[j + 1] > yb[j]:
                lh = x[j] + (hm - yb[j]) * (x[j + 1] - x[j]) / (yb[j + 1] - yb[j])
            else:
                lh = x[j]
        j = cent
        while j < len(x) - 1 and yb[j] >= hm:
            j += 1
        rh = None
        if j > cent and j - 1 >= 0:
            if yb[j - 1] > yb[j]:
                rh = x[j] - (hm - yb[j]) * (x[j] - x[j - 1]) / (yb[j - 1] - yb[j])
            else:
                rh = x[j]
        if lh is not None and rh is not None and rh > lh:
            fwhm = float(rh - lh)
    d0 = max(d_meas, 0.02)
    s0 = 1.0
    try:
        if not use_zeeman:
            p, _ = curve_fit(gauss, x, yb, p0=[d0, center, s0],
                             bounds=([0.0, center - 3.0, 0.05], [2.0, center + 3.0, 3.0]),
                             maxfev=4000)
            d, x0, s = p
            resid = yb - gauss(x, d, x0, s)
            return {'d': float(d), 'sig': float(s), 'x0': float(x0),
                    'd_meas': d_meas, 'd_pure': d_pure, 'fwhm': fwhm,
                    'chi2': float(np.sum(resid ** 2)), 'ok': True, 'ndata': int(len(x))}
        else:
            dL = 4.67e-13 * center ** 2 * B_G
            def zfun(x, d, x0, s, wpi):
                g0 = gauss(x, d * wpi, x0, s)
                gs = gauss(x, d * (1 - wpi) / 2, x0 - dL, s) + gauss(x, d * (1 - wpi) / 2, x0 + dL, s)
                return g0 + gs
            p, _ = curve_fit(zfun, x, yb, p0=[d0, center, s0, 0.33],
                             bounds=([0.0, center - 3.0, 0.05, 0.0], [2.0, center + 3.0, 3.0, 1.0]),
                             maxfev=4000)
            d, x0, s, wpi = p
            resid = yb - zfun(x, d, x0, s, wpi)
            return {'d': float(d), 'sig': float(s), 'x0': float(x0), 'wpi': float(wpi),
                    'd_meas': d_meas, 'd_pure': d_pure, 'fwhm': fwhm,
                    'chi2': float(np.sum(resid ** 2)), 'ok': True, 'ndata': int(len(x))}
    except Exception:
        return None

# ---- 载入 ----
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = json.load(f)["samples"]
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

# ---- 强场样本（B>=100 MG 且有缓存）----
spec_dir = os.path.join(BASE, "_desi_spec")
have = set(fn[:-4] for fn in os.listdir(spec_dir) if fn.endswith(".npz"))
strong = [s for s in cat if (s.get("B_MG") or 0) >= 100 and str(s.get("gaia_int")) in have]
print("强场有缓存:", len(strong))

# 理论 η_sc（束缚态衰减口径插值——用论文表态数锚 303@0.001，1 a.u.=2350 MG）
B_p = np.array([0.001, 0.01, 0.05, 0.1, 0.2]); N_p = np.array([303.0, 300.0, 152.0, 69.0, 33.0])
def eta_at_b_mg(b):
    b = b / 2350.0
    if b <= 0.001: return 0.0
    if b >= 0.2: n = 33.0
    else: n = float(np.interp(np.log10(b), np.log10(B_p), N_p))
    return max(0.0, min(1.0, 1.0 - n / 303.0))

out = {"strong": []}
for s in strong:
    gid = str(s["gaia_int"])
    fp = os.path.join(spec_dir, gid + ".npz")
    d = np.load(fp)
    wave, flux = d["wave"], d["flux"]
    good = np.isfinite(flux) & (flux > 0)
    if good.sum() < 500:
        continue
    w, f = wave[good], flux[good]
    nf = v10.normalize(w, f)
    km = load_koester(s["Teff"], s["logg"])
    nm = None
    if km is not None:
        nm = v10.normalize(km[0], km[1])
    star = {"gid": gid, "B_MG": s["B_MG"], "Teff": s["Teff"], "logg": s["logg"],
            "eta_sc": eta_at_b_mg(s["B_MG"]), "lines": {}}
    for ln in LINES:
        c = LINE_C[ln]
        hw = min(60.0, HG.get(ln, 60.0))
        rA = fit_line(w, nf, c, hw)
        rB = fit_line(w, nf, c, hw, use_zeeman=True, B_G=s["B_MG"] * 1e6)
        rM = fit_line(km[0], nm, c, hw) if nm is not None else None
        if rA is None or rA["d_meas"] < 0.03:
            continue
        rec = {"d_obs": rA["d"], "sig_obs": rA["sig"],
               "d_meas": rA["d_meas"], "d_pure": rA["d_pure"], "fwhm": rA["fwhm"],
               "chi2_A": rA["chi2"], "chi2_B": rB["chi2"] if rB else None,
               "wpi": rB["wpi"] if rB else None}
        if rM is not None and rM["d_meas"] > 0.03:
            rec["d_mod"] = rM["d"]; rec["sig_mod"] = rM["sig"]
            rec["d_meas_mod"] = rM["d_meas"]; rec["d_pure_mod"] = rM["d_pure"]
        star["lines"][ln] = rec
    out["strong"].append(star)
    dp = [r["d_pure"] for r in star["lines"].values()]
    print("B=%.1f MG Teff=%d η_sc=%.2f 线数=%d d_pure 中位=%.3f" % (
        s["B_MG"], s["Teff"], star["eta_sc"], len(star["lines"]),
        float(np.median(dp)) if dp else float('nan')), flush=True)

with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_linelevel_strong.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written paperX_wd_linelevel_strong.json")
