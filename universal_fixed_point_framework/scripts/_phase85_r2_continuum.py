# -*- coding: utf-8 -*-
"""Phase 85 R2：连续谱测量管线
从 DESI 缓存光谱提取三量：Balmer 跳变 D_B、连续谱斜率、归一化基底残差
同口径在 Koester 理论谱重算 -> 残差 log10(obs/theo)
输出 scripts/paperX_wd_continuum.json
"""
import os, sys, json, io
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\src\white_dwarf_analysis")
from white_dwarf_analysis_v10 import normalize, BALMER

# ---- 连续谱带（避开全部 Balmer 线 ±60 Å）----
BAND_BJ_BLUE  = (3600, 3640)   # Balmer 跳变蓝端（3646 前）
BAND_BJ_RED   = (3700, 3750)   # 跳变红端
BAND_SLOPE_A  = (4000, 4060)   # 斜率蓝带（Hδ 4101 前 41-101 Å；Hε 3970 后 30-90 Å）
BAND_SLOPE_B  = (5000, 5800)   # 斜率红带（无 Balmer 线）
BAND_RES      = [(4000, 4060), (4800, 4840), (5000, 5800)]  # 归一化残差带

def band_mean(wl, fl, band):
    m = (wl >= band[0]) & (wl <= band[1])
    if np.sum(m) < 2:
        return None
    return float(np.median(fl[m]))

def band_snr(wl, fl, ivar, band):
    m = (wl >= band[0]) & (wl <= band[1])
    if np.sum(m) < 10:
        return 0.0
    snr = fl[m] * np.sqrt(ivar[m])
    return float(np.median(snr))

def measure_continuum(wl, fl, ivar=None):
    """返回 {D_B, slope, res_bands, snr_blue, snr_red}"""
    out = {}
    fb = band_mean(wl, fl, BAND_BJ_BLUE)
    fr = band_mean(wl, fl, BAND_BJ_RED)
    out["D_B"] = fb / fr if (fb and fr and fr > 0) else None
    fa = band_mean(wl, fl, BAND_SLOPE_A)
    fb2 = band_mean(wl, fl, BAND_SLOPE_B)
    lam_a = np.sqrt(BAND_SLOPE_A[0] * BAND_SLOPE_A[1])
    lam_b = np.sqrt(BAND_SLOPE_B[0] * BAND_SLOPE_B[1])
    out["slope"] = (np.log(fb2) - np.log(fa)) / (np.log(lam_b) - np.log(lam_a)) if (fa and fb2 and fa > 0 and fb2 > 0) else None
    # 归一化基底残差（v10 口径，在归一化谱上测连续谱带均值 - 1）
    nf = normalize(wl, fl)
    res = {}
    for nm, bd in [("b1", BAND_RES[0]), ("b2", BAND_RES[1]), ("b3", BAND_RES[2])]:
        v = band_mean(wl, nf, bd)
        res[nm] = (v - 1.0) if v is not None else None
    out["res"] = res
    if ivar is not None:
        out["snr_blue"] = band_snr(wl, fl, ivar, BAND_BJ_BLUE)
        out["snr_red"] = band_snr(wl, fl, ivar, BAND_BJ_RED)
    return out

# ---- 1) 观测侧：DESI 缓存 ----
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = json.load(f)["samples"]
with io.open(os.path.join(BASE, "_m83e_desi_ew.json"), "r", encoding="utf-8") as f:
    ew0 = json.load(f)

meta = {str(s["gaia_int"]): s for s in cat}
obs = {}
for fn in sorted(os.listdir(os.path.join(BASE, "_desi_spec"))):
    if not fn.endswith(".npz"):
        continue
    gid = fn.split(".")[0]
    if gid not in meta or gid not in ew0 or not ew0[gid].get("ok"):
        continue
    try:
        d = np.load(os.path.join(BASE, "_desi_spec", fn), allow_pickle=True)
        wl, fl, iv = d["wave"], d["flux"], d["ivar"]
        m = measure_continuum(wl, fl, iv)
        m["B_MG"] = meta[gid]["B_MG"]
        m["Teff"] = meta[gid]["Teff"]
        m["logg"] = meta[gid]["logg"]
        obs[gid] = m
    except Exception as e:
        print("obs fail", gid, e)

# ---- 2) 理论侧：Koester 谱同带重算 ----
def load_koester(teff, logg):
    """最近网格点理论谱（与 _m83e_window_scan.py 同口径）"""
    import re
    best = None
    for fn in os.listdir(os.path.join(BASE, "_koester_spec")):
        mm = re.match(r"fid\d+_([\d.]+)_([\d.]+)\.dat", fn)
        if not mm:
            continue
        t, g = float(mm.group(1)), float(mm.group(2))
        score = (t - teff) ** 2 + (g - logg) ** 2
        if best is None or score < best[0]:
            best = (score, os.path.join(BASE, "_koester_spec", fn))
    if best is None:
        return None
    arr = np.loadtxt(best[1])
    return arr[:, 0], arr[:, 1]

theo = {}
for gid, m in obs.items():
    k = load_koester(m["Teff"], m["logg"])
    if k is None:
        continue
    wl_k, fl_k = k
    tm = measure_continuum(wl_k, fl_k)
    theo[gid] = tm

# ---- 3) 残差 ----
rows = []
for gid in obs:
    if gid not in theo:
        continue
    o, t = obs[gid], theo[gid]
    row = {"gaia_int": int(gid), "B_MG": o["B_MG"], "Teff": o["Teff"], "logg": o["logg"],
           "snr_blue": o.get("snr_blue"), "snr_red": o.get("snr_red")}
    for k in ["D_B", "slope"]:
        # D_B 恒正；slope 观测/理论均为负（连续谱红端下降）——要求同号且非零
        ok = o[k] is not None and t[k] is not None
        if k == "slope":
            ok = ok and abs(o[k]) > 0 and abs(t[k]) > 0 and (o[k] * t[k] > 0)
        else:
            ok = ok and o[k] > 0 and t[k] > 0
        if ok:
            row[k + "_obs"] = o[k]
            row[k + "_theo"] = t[k]
            row[k + "_res"] = float(np.log10(o[k] / t[k]))
        else:
            row[k + "_res"] = None
    for nm in ["b1", "b2", "b3"]:
        if o["res"][nm] is not None and t["res"][nm] is not None:
            row["res_" + nm + "_obs"] = o["res"][nm]
            row["res_" + nm + "_theo"] = t["res"][nm]
            row["res_" + nm + "_diff"] = o["res"][nm] - t["res"][nm]
        else:
            row["res_" + nm + "_diff"] = None
    rows.append(row)

out = {"n_obs": len(obs), "n_theo": len(theo), "n_rows": len(rows), "rows": rows}
with io.open(os.path.join(BASE, "paperX_wd_continuum.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

# ---- 汇总 ----
import numpy as np
def grp(rows, cond, key):
    vs = [r[key] for r in rows if cond(r) and r[key] is not None]
    return (len(vs), float(np.mean(vs)), float(np.std(vs))) if vs else (0, None, None)

print("n_obs=%d n_theo=%d n_rows=%d" % (len(obs), len(theo), len(rows)))
for key in ["D_B_res", "slope_res", "res_b1_diff", "res_b3_diff"]:
    for nm, cond in [("弱场(<10MG)", lambda r: r["B_MG"] < 10),
                     ("中场(10-100MG)", lambda r: 10 <= r["B_MG"] < 100),
                     ("强场(>100MG)", lambda r: r["B_MG"] >= 100)]:
        n, mu, sd = grp(rows, cond, key)
        if n:
            print("%-14s %-14s n=%3d mean=%+.4f sd=%.4f" % (key, nm, n, mu, sd))
