# -*- coding: utf-8 -*-
"""Phase 74 窗口扫描：DESI 116 颗多窗口 EW + Koester 同窗口理论 EW + 回归
W = {80, 160, 320}；每线窗口受 half-gap（到最近 Balmer 线半距）截断
同时输出"无保护"（v0.7 R6 口径，window=80 直用）对照——审计 Hδ/Hε/Hζ/Hη 重叠污染
输出 _m83e_window_scan.json + _m83e_window_scan_regs.json
"""
import io, json, os, glob, sys
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\src\white_dwarf_analysis")
import white_dwarf_analysis_v10 as v10

WINDOWS = [80.0, 160.0, 320.0]

# 最近邻半距（按 Balmer 波长排序计算）
_BW = sorted(v10.BALMER.items(), key=lambda kv: kv[1])
def half_gaps():
    hg = {}
    for i, (nm, c) in enumerate(_BW):
        lo = _BW[i-1][1] if i > 0 else None
        hi = _BW[i+1][1] if i+1 < len(_BW) else None
        cand = [d for d in (None if lo is None else c-lo, None if hi is None else hi-c) if d]
        hg[nm] = min(cand) / 2.0 - 1.0  # 1 Å 余量
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
    """返回 (tew, n_det, per_line)"""
    tew, nd, per = 0.0, 0, {}
    for nm, c in v10.BALMER.items():
        weff = min(window, HG[nm]) if protect else window
        ew, det = measure_ew_w(wl, nf, c, weff)
        per[nm] = {"ew": float(ew), "det": bool(det), "w": float(weff)}
        if det:
            tew += ew; nd += 1
    return tew, nd, per

# ---- 1) 目录 ----
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = json.load(f)["samples"]
with io.open(os.path.join(BASE, "_m83e_desi_ew.json"), "r", encoding="utf-8") as f:
    ew0 = json.load(f)

# ---- 2) Koester fid 网格 ----
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

# ---- 3) 主循环 ----
star_ews = {}   # gid -> {protect: {W: {tew, nd, per}}, noprotect: {80: ...}}
for s in cat:
    gid = str(s["gaia_int"])
    if gid not in ew0 or not ew0[gid].get("ok"):
        continue
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
    star_ews[gid] = {"B_MG": s["B_MG"], "Teff": s["Teff"], "logg": s["logg"]}
    for prot in (True, False):
        star_ews[gid]["p" if prot else "n"] = {}
        for W in WINDOWS:
            tew, nd, per = total_ew(w, nf, W, protect=prot)
            star_ews[gid]["p" if prot else "n"][str(int(W))] = {"tew": tew, "nd": nd, "per": per}

# ---- 4) Koester 理论 EW（同窗口） ----
koester_ews = {}   # (teff, logg) -> {protect: {W: tew}}
kstar = {}
for gid, st in star_ews.items():
    k = load_koester(st["Teff"], st["logg"])
    if k is None:
        continue
    key = (round(st["Teff"]), round(st["logg"]))
    if key in kstar:
        continue
    wl_a, fl_a = k
    nf2 = v10.normalize(wl_a, fl_a)
    kstar[key] = {}
    for prot in (True, False):
        kstar[key]["p" if prot else "n"] = {}
        for W in WINDOWS:
            tew, nd, _ = total_ew(wl_a, nf2, W, protect=prot)
            kstar[key]["p" if prot else "n"][str(int(W))] = {"tew": tew, "nd": nd}

# ---- 5) 组装残差样本 + 回归 ----
from scipy.stats import spearmanr
regs = {}
for prot in (True, False):
    tag = "protect" if prot else "no_protect"
    for W in WINDOWS:
        recs = []
        for gid, st in star_ews.items():
            obs = st["p" if prot else "n"][str(int(W))]["tew"]
            if obs <= 0:
                continue
            kk = kstar.get((round(st["Teff"]), round(st["logg"])))
            if kk is None:
                continue
            theo = kk["p" if prot else "n"][str(int(W))]["tew"]
            if theo <= 0:
                continue
            recs.append({
                "gaia_int": gid, "B_MG": st["B_MG"], "Teff": st["Teff"],
                "obs_EW": obs, "koester_EW": theo,
                "resid": float(np.log10(obs/theo)),
            })
        if len(recs) >= 5:
            X = np.array([[np.log10(r["B_MG"]*100.0), r["Teff"]] for r in recs], dtype=float)
            y = np.array([r["resid"] for r in recs], dtype=float)
            Xc = X - X.mean(axis=0)
            Xd = np.column_stack([np.ones(len(y)), Xc])
            beta = np.linalg.solve(Xd.T @ Xd, Xd.T @ y)
            resid = y - Xd @ beta
            s2 = resid @ resid / (len(y) - 3)
            se = np.sqrt(np.diag(s2 * np.linalg.inv(Xd.T @ Xd)))
            t = beta / se
            rho, p = spearmanr(Xc[:, 0], y)
            regs["%s_W%s" % (tag, int(W))] = {
                "n": len(recs), "log10B": float(beta[1]), "t_log10B": float(t[1]),
                "Teff": float(beta[2]), "rho": float(rho), "p": float(p),
                "B_range_MG": [min(r["B_MG"] for r in recs), max(r["B_MG"] for r in recs)],
            }
        else:
            regs["%s_W%s" % (tag, int(W))] = {"n": len(recs), "note": "too_few"}

with io.open(os.path.join(BASE, "_m83e_window_scan.json"), "w", encoding="utf-8") as f:
    json.dump({"star_ews": star_ews, "koester_ews": {("%d_%d" % (kk[0], kk[1])): v for kk, v in kstar.items()},
               "regs": regs, "windows": WINDOWS, "half_gaps": HG}, f, ensure_ascii=False, indent=1)
with io.open(os.path.join(BASE, "_m83e_window_scan_regs.json"), "w", encoding="utf-8") as f:
    json.dump(regs, f, ensure_ascii=False, indent=1)

print("stars measured:", len(star_ews))
for tag, W in [("protect", 80.0), ("protect", 160.0), ("protect", 320.0)]:
    r = regs["%s_W%d" % (tag, int(W))]
    print("%s W=%d: n=%d log10B=%.3f (t=%.2f) rho=%.3f p=%.3e" % (tag, W, r["n"], r["log10B"], r["t_log10B"], r["rho"], r["p"]))
for tag, W in [("no_protect", 80.0)]:
    r = regs["%s_W%d" % (tag, int(W))]
    print("%s W=%d: n=%d log10B=%.3f (t=%.2f) rho=%.3f p=%.3e" % (tag, W, r["n"], r["log10B"], r["t_log10B"], r["rho"], r["p"]))
