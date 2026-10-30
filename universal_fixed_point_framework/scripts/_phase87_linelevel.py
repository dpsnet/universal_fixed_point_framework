# -*- coding: utf-8 -*-
"""Phase 87 M87-2/3/4：线级建模——σ/depth 提取 + Zeeman 三分量拟合 + Koester 零场对比 + 回归
判据：R_sigma = log10(sig_obs/sig_mod) ~ log10B；R_depth 同。
B 预言 R_sigma~0 且 R_depth<0；线级展宽预言 R_sigma>0 且 R_depth~0
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
# half-gap 保护窗口（复用 Phase 74 逻辑）
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
    """测量量：线心深度 depth（±5 Å 中位）+ FWHM（半高直测）；拟合高斯/Zeeman 作辅助（x0 钉在理论线心）"""
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
    # 测量量（不依赖拟合）
    cm = np.abs(x - center) < 5.0
    d_meas = float(np.median(y[cm])) if np.sum(cm) > 0 else 0.0   # 含背景
    d_pure = float(np.median(yb[cm])) if np.sum(cm) > 0 else 0.0  # 纯线深（基线校正后）
    # FWHM：纯线深半高直测（yb 口径，hm=d_pure/2）
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
    # 拟合（x0 钉理论线心；σ 物理上限 3 Å——超过即非物理吸收翼，标记 censored）
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
            # Zeeman 三分量：pi 中心 + 2 sigma 分量 ±dL，权重自由
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
with io.open(os.path.join(BASE, "_m83e_desi_ew.json"), "r", encoding="utf-8") as f:
    ew0 = json.load(f)
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

# ---- 主档筛选（8-25 kK 扩容版，含强中场）----
rows = []
for s in cat:
    gid = str(s["gaia_int"])
    if gid not in ew0 or not ew0[gid].get("ok"):
        continue
    if not (8000 <= s["Teff"] <= 25000):
        continue
    rows.append(s)
weak = [s for s in rows if s["B_MG"] < 10.0]
mid = [s for s in rows if 10.0 <= s["B_MG"] < 100.0]
print("main bin: weak n=%d  mid n=%d" % (len(weak), len(mid)))

# ---- 逐星逐线拟合 ----
out = {"weak": [], "mid": []}
for grp_name, grp in (("weak", weak), ("mid", mid)):
    for s in grp:
        gid = str(s["gaia_int"])
        fp = os.path.join(BASE, "_desi_spec", gid + ".npz")
        if not os.path.exists(fp):
            continue
        d = np.load(fp)
        wave, flux = d["wave"], d["flux"]
        good = np.isfinite(flux) & (flux > 0)
        if good.sum() < 500:
            continue
        w, f = wave[good], flux[good]
        nf = v10.normalize(w, f)
        # Koester 零场模型谱
        km = load_koester(s["Teff"], s["logg"])
        nm = None
        if km is not None:
            wl_a, fl_a = km
            nm = v10.normalize(wl_a, fl_a)
        star = {"gid": gid, "B_MG": s["B_MG"], "Teff": s["Teff"], "logg": s["logg"], "lines": {}}
        for ln in LINES:
            c = LINE_C[ln]
            hw = min(60.0, HG.get(ln, 60.0))
            rA = fit_line(w, nf, c, hw)
            rB = fit_line(w, nf, c, hw, use_zeeman=True, B_G=s["B_MG"] * 1e6)
            rM = fit_line(wl_a, nm, c, hw) if nm is not None else None
            if rA is None or rA["d_meas"] < 0.03:
                continue
            rec = {"d_obs": rA["d"], "sig_obs": rA["sig"],
                   "d_meas": rA["d_meas"], "d_pure": rA["d_pure"], "fwhm": rA["fwhm"],
                   "chi2_A": rA["chi2"], "chi2_B": rB["chi2"] if rB else None,
                   "wpi": rB["wpi"] if rB else None}
            if rM is not None and rM["d_meas"] > 0.03:
                rec["d_mod"] = rM["d"]
                rec["sig_mod"] = rM["sig"]
                rec["d_meas_mod"] = rM["d_meas"]
                rec["d_pure_mod"] = rM["d_pure"]
                rec["fwhm_mod"] = rM["fwhm"]
            star["lines"][ln] = rec
        out[grp_name].append(star)
    print("%s: %d stars" % (grp_name, len(out[grp_name])))

with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_linelevel.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written paperX_wd_linelevel.json")
