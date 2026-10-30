# -*- coding: utf-8 -*-
"""R6：DESI 第三目录独立回归（Koester 缓存理论 EW + 中心化 OLS + Spearman）"""
import io, json, os, sys
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
sys.path.insert(0, BASE)
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\src\white_dwarf_analysis")
import white_dwarf_analysis_v10 as v10

# 1) 目录与 EW
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = json.load(f)["samples"]
with io.open(os.path.join(BASE, "_m83e_desi_ew.json"), "r", encoding="utf-8") as f:
    ew = json.load(f)
# 2) Koester fid 网格 + 缓存
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
    wl_a, fl_a = np.array(wl2), np.array(fl2)
    nf2 = v10.normalize(wl_a, fl_a)
    tew2 = 0.0; nd2 = 0
    for ln, lw in v10.BALMER.items():
        ew2, det2 = v10.measure_ew(wl_a, nf2, lw)
        if det2:
            tew2 += ew2; nd2 += 1
    spec_cache[key] = (float(tew2), nd2)
    return spec_cache[key]

# 3) 组装残差样本
recs = []
for s in cat:
    gid = str(s["gaia_int"])
    if gid not in ew or not ew[gid].get("ok"):
        continue
    obs_EW = sum(v for v in ew[gid]["ews"].values() if v is not None)
    if obs_EW <= 0:
        continue
    k = koester_ew(s["Teff"], 8.0)
    if k is None:
        continue
    koester_EW, nk = k
    if koester_EW <= 0:
        continue
    recs.append({
        "gaia_int": s["gaia_int"], "desi_name": s["desi_name"],
        "B_MG": s["B_MG"], "B_tesla": s["B_MG"] * 100.0,
        "Teff": s["Teff"], "Mass": s["Mass"], "logg": 8.0,
        "obs_EW": obs_EW, "koester_EW": float(koester_EW),
        "resid": float(np.log10(obs_EW / koester_EW)),
        "n_det": ew[gid]["n_det"],
    })
print("DESI 有效残差样本 n =", len(recs))
# B 分档
bs = [r["B_MG"] for r in recs]
print("B<10:", sum(1 for x in bs if x < 10), "10-100:", sum(1 for x in bs if 10 <= x < 100), ">=100:", sum(1 for x in bs if x >= 100))

# 4) 回归
if len(recs) >= 5:
    X = np.array([[np.log10(r["B_tesla"]), r["Teff"]] for r in recs], dtype=float)
    y = np.array([r["resid"] for r in recs], dtype=float)
    Xc = X - X.mean(axis=0)
    Xd = np.column_stack([np.ones(len(y)), Xc])
    beta = np.linalg.solve(Xd.T @ Xd, Xd.T @ y)
    resid = y - Xd @ beta
    s2 = resid @ resid / (len(y) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(Xd.T @ Xd)))
    t = beta / se
    from scipy.stats import spearmanr
    rho, p = spearmanr(Xc[:, 0], y)
    print("DESI OLS: log10B %.3f (t=%.2f) Teff %.2e ; Spearman rho=%.3f p=%.3e" % (beta[1], t[1], beta[2], rho, p))
    out = {"n": len(recs), "log10B": float(beta[1]), "t_log10B": float(t[1]),
           "Teff": float(beta[2]), "rho": float(rho), "p": float(p),
           "B_MG_range": [min(bs), max(bs)],
           "n_by_B": {"lt10": sum(1 for x in bs if x < 10), "10_100": sum(1 for x in bs if 10 <= x < 100), "ge100": sum(1 for x in bs if x >= 100)}}
    with io.open(os.path.join(BASE, "_m83e_desi_regression.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("saved _m83e_desi_regression.json")
# 5) 保存样本
with io.open(os.path.join(BASE, "_m83e_desi_resid_samples.json"), "w", encoding="utf-8") as f:
    json.dump(recs, f, ensure_ascii=False, indent=1)
print("saved resid samples")
