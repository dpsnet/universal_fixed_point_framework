# -*- coding: utf-8 -*-
"""Phase 94 M94-2：Amorim 目录中场档（10-100 MG = 1e3-1e4 T）全量 SDSS 光谱 + 线级
复用 _phase89b 管线（load_cat → get_spec → fit_line）
"""
import io, json, os, sys, time
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
                    'd_meas': d_meas, 'd_pure': d_pure,
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
                    'd_meas': d_meas, 'd_pure': d_pure,
                    'chi2': float(np.sum(resid ** 2)), 'ok': True, 'ndata': int(len(x))}
    except Exception:
        return None

print("载入 VizieR J/ApJ/944/56 ...", flush=True)
data, inter, weak = v10.load_cat()
mid = [d for d in data if 1e3 <= d['B_tesla'] < 1e4]
print("全目录 %d, 中场(10-100 MG) %d 颗" % (len(data), len(mid)), flush=True)

spec_dir = os.path.join(BASE, "_desi_spec")
os.makedirs(spec_dir, exist_ok=True)
out = {"mid_full": []}
n_ok = n_fail = 0
for s in mid:
    gid = str(s["name"]).replace("SDSS ", "").replace("/", "")
    print(">> %s B=%.1f MG Teff=%s Sp-ID=%s" % (s["name"], s["B_tesla"] / 100.0, s["Teff"], s.get("Sp-ID")), flush=True)
    try:
        spec = v10.get_spec(s)
    except Exception as e:
        print("   get_spec 异常: %s" % str(e)[:100], flush=True)
        spec = None
    if spec is None:
        n_fail += 1
        print("   光谱失败", flush=True)
        time.sleep(0.5)
        continue
    wl_a, fl_a = spec
    wl_a = np.asarray(wl_a, dtype=float); fl_a = np.asarray(fl_a, dtype=float)
    good = np.isfinite(fl_a) & (fl_a > 0)
    if good.sum() < 500:
        n_fail += 1
        print("   光谱无效", flush=True)
        continue
    np.savez(os.path.join(spec_dir, gid + ".npz"), wave=wl_a, flux=fl_a)
    n_ok += 1
    w, f = wl_a[good], fl_a[good]
    nf = v10.normalize(w, f)
    star = {"name": s["name"], "gid": gid, "B_MG": s["B_tesla"] / 100.0,
            "Teff": s["Teff"], "logg": None, "Sp-ID": s.get("Sp-ID"), "lines": {}}
    for ln in LINES:
        c = LINE_C[ln]
        hw = min(60.0, HG.get(ln, 60.0))
        rA = fit_line(w, nf, c, hw)
        rB = fit_line(w, nf, c, hw, use_zeeman=True, B_G=s["B_tesla"] * 1e6 / 100.0)
        if rA is None or rA["d_meas"] < 0.03:
            continue
        rec = {"d_obs": rA["d"], "sig_obs": rA["sig"],
               "d_meas": rA["d_meas"], "d_pure": rA["d_pure"],
               "chi2_A": rA["chi2"], "chi2_B": rB["chi2"] if rB else None,
               "wpi": rB["wpi"] if rB else None}
        star["lines"][ln] = rec
    out["mid_full"].append(star)
    dp = [r["d_pure"] for r in star["lines"].values()]
    print("   B=%.1f MG Teff=%s 线数=%d d_pure 中位=%s" % (
        s["B_tesla"] / 100.0, s["Teff"], len(star["lines"]),
        "%.3f" % float(np.median(dp)) if dp else "—"), flush=True)
    time.sleep(0.3)

with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_linelevel_mid_full.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("完成: 成功 %d / 失败 %d; written paperX_wd_linelevel_mid_full.json" % (n_ok, n_fail), flush=True)
