# -*- coding: utf-8 -*-
"""R6b：三目录统一合并回归（Amorim 518 + Kepler 60 + DESI 137）
统一 Koester 缓存理论 EW → resid → OLS(含目录固定效应 + 目录×log10B 交互)"""
import io, json, os, sys
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\src\white_dwarf_analysis")
import white_dwarf_analysis_v10 as v10

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
spec_cache = {}
def koester_ew(teff, logg):
    t, g = nearest(teff, logg)
    key = (t, g)
    if key in spec_cache:
        return spec_cache[key]
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
    nf2 = v10.normalize(np.array(wl2), np.array(fl2))
    tew2 = 0.0; nd2 = 0
    for ln, lw in v10.BALMER.items():
        ew2, det2 = v10.measure_ew(np.array(wl2), nf2, lw)
        if det2:
            tew2 += ew2; nd2 += 1
    spec_cache[key] = (float(tew2), nd2)
    return spec_cache[key]

def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

# 1) M83c Amorim 518
with io.open(os.path.join(BASE, "paperX_wd_m83c_sample_list.json"), "r", encoding="utf-8") as f:
    c518 = json.load(f)
# 2) M83d Kepler 60（取 status=ok 且有 obs_EW）
with io.open(os.path.join(BASE, "paperX_wd_m83d_kepler_sample.json"), "r", encoding="utf-8") as f:
    d60 = json.load(f)
# 3) M83e DESI 91（_m83e_desi_ew.json）
with io.open(os.path.join(BASE, "_m83e_desi_ew.json"), "r", encoding="utf-8") as f:
    e91 = json.load(f)
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    e137 = json.load(f)["samples"]

recs = []
# M83c
for s in c518:
    B, Teff, logg, obs = fnum(s["B_tesla"]), fnum(s["Teff"]), fnum(s["logg"]), fnum(s["obs_EW"])
    if None in (B, Teff, logg, obs) or obs <= 0:
        continue
    k = koester_ew(Teff, logg)
    if k is None or k[0] <= 0:
        continue
    recs.append({"cat": "amorim", "B_tesla": B, "Teff": Teff, "logg": logg,
                 "obs_EW": obs, "koester_EW": k[0], "resid": float(np.log10(obs / k[0]))})
# M83d
for s in d60:
    if s.get("status") != "ok" or not s.get("obs_EW") or not s.get("koester_EW"):
        continue
    B, Teff, logg = fnum(s["B_tesla"]), fnum(s["Teff"]), fnum(s["logg"])
    recs.append({"cat": "kepler", "B_tesla": B, "Teff": Teff, "logg": logg,
                 "obs_EW": fnum(s["obs_EW"]), "koester_EW": fnum(s["koester_EW"]),
                 "resid": float(s["resid"]) if s.get("resid") is not None else None})
recs = [r for r in recs if r["resid"] is not None]
# M83e
for s in e137:
    gid = str(s["gaia_int"])
    if gid not in e91 or not e91[gid].get("ok"):
        continue
    obs = sum(v for v in e91[gid]["ews"].values() if v is not None)
    if obs <= 0:
        continue
    k = koester_ew(s["Teff"], 8.0)
    if k is None or k[0] <= 0:
        continue
    recs.append({"cat": "desi", "B_tesla": s["B_MG"] * 100.0, "Teff": s["Teff"], "logg": 8.0,
                 "obs_EW": obs, "koester_EW": k[0], "resid": float(np.log10(obs / k[0]))})

print("合并样本: amorim=%d kepler=%d desi=%d total=%d" % (
    sum(1 for r in recs if r["cat"] == "amorim"),
    sum(1 for r in recs if r["cat"] == "kepler"),
    sum(1 for r in recs if r["cat"] == "desi"), len(recs)))

# 合并 OLS：resid ~ log10B + Teff + logg + cat_kepler + cat_desi + cat×log10B
X = []
for r in recs:
    X.append([np.log10(r["B_tesla"]), r["Teff"], r["logg"],
              1.0 if r["cat"] == "kepler" else 0.0,
              1.0 if r["cat"] == "desi" else 0.0,
              (1.0 if r["cat"] == "kepler" else 0.0) * np.log10(r["B_tesla"]),
              (1.0 if r["cat"] == "desi" else 0.0) * np.log10(r["B_tesla"])])
X = np.array(X, dtype=float)
y = np.array([r["resid"] for r in recs], dtype=float)
Xc = X - X.mean(axis=0)
Xd = np.column_stack([np.ones(len(y)), Xc])
beta = np.linalg.solve(Xd.T @ Xd, Xd.T @ y)
resid = y - Xd @ beta
s2 = resid @ resid / (len(y) - Xd.shape[1])
se = np.sqrt(np.diag(s2 * np.linalg.inv(Xd.T @ Xd)))
t = beta / se
names = ["intercept", "log10B", "Teff", "logg", "cat_kepler", "cat_desi", "kepler_x_B", "desi_x_B"]
print("=== 合并 OLS（含交互）===")
for n_, b_, t_ in zip(names, beta, t):
    print("%-10s %.4f (t=%.2f)" % (n_, b_, t_))
# 简化：不含交互的主回归
X2 = np.array([[np.log10(r["B_tesla"]), r["Teff"], r["logg"]] for r in recs], dtype=float)
Xc2 = X2 - X2.mean(axis=0)
Xd2 = np.column_stack([np.ones(len(y)), Xc2])
beta2 = np.linalg.solve(Xd2.T @ Xd2, Xd2.T @ y)
resid2 = y - Xd2 @ beta2
s22 = resid2 @ resid2 / (len(y) - 4)
se2 = np.sqrt(np.diag(s22 * np.linalg.inv(Xd2.T @ Xd2)))
t2 = beta2 / se2
from scipy.stats import spearmanr
rho, p = spearmanr(Xc2[:, 0], y)
print("=== 合并主回归：log10B %.3f (t=%.2f) Teff %.2e logg %.3f ; Spearman rho=%.3f p=%.3e ===" % (beta2[1], t2[1], beta2[2], beta2[3], rho, p))

out = {"n": len(recs),
       "n_by_cat": {"amorim": sum(1 for r in recs if r["cat"] == "amorim"),
                    "kepler": sum(1 for r in recs if r["cat"] == "kepler"),
                    "desi": sum(1 for r in recs if r["cat"] == "desi")},
       "main_log10B": float(beta2[1]), "main_t": float(t2[1]),
       "main_Teff": float(beta2[2]), "main_logg": float(beta2[3]),
       "rho": float(rho), "p": float(p),
       "interact": {n_: float(b_) for n_, b_ in zip(names, beta)},
       "interact_t": {n_: float(t_) for n_, t_ in zip(names, t)}}
with io.open(os.path.join(BASE, "_m83e_merged_regression.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
with io.open(os.path.join(BASE, "_m83e_merged_resid_samples.json"), "w", encoding="utf-8") as f:
    json.dump(recs, f, ensure_ascii=False, indent=1)
print("saved merged regression + samples")
