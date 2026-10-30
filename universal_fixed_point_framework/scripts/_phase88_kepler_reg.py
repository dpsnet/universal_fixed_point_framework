# -*- coding: utf-8 -*-
"""Phase 88 M88-3：Kepler 26 中场场内 B 梯度回归 + DESI 跨目录对比"""
import io, json, os
import numpy as np
from scipy import stats

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_kepler_linelevel.json"), "r", encoding="utf-8") as f:
    kdata = json.load(f)
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_linelevel.json"), "r", encoding="utf-8") as f:
    ddata = json.load(f)

def agg(star):
    s_l, dp_l, r_l = [], [], []
    for ln, rec in star["lines"].items():
        s_l.append(rec["sig_obs"])
        dp_l.append(rec["d_pure"])
        if "sig_mod" in rec and rec["sig_mod"]:
            r_l.append(np.log10(rec["sig_obs"] / rec["sig_mod"]))
    if not dp_l:
        return None
    return {"sig": float(np.median(s_l)), "dep": float(np.median(dp_l)),
            "rsig": float(np.median(r_l)) if r_l else None,
            "n_lines": len(dp_l), "n_mod": len(r_l)}

krows = []
for grp in ("weak", "mid"):
    for star in kdata[grp]:
        a = agg(star)
        if a is None:
            continue
        krows.append({"gid": star["gid"], "B_MG": star["B_MG"], "Teff": star["Teff"],
                      "grp": grp, **a})
print("Kepler 线级有效: %d（weak %d / mid %d）" % (len(krows),
      sum(1 for r in krows if r["grp"] == "weak"), sum(1 for r in krows if r["grp"] == "mid")))

def ols(X, y):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ beta
    resid = y - yhat
    n, p = len(y), X.shape[1]
    s2 = np.sum(resid ** 2) / (n - p)
    cov = s2 * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    t = beta / se
    return beta, se, t

km = [r for r in krows if r["grp"] == "mid"]
print("\n== Kepler 中场场内 B 梯度（n=%d，B %.1f–%.1f MG）==" % (len(km), min(r["B_MG"] for r in km), max(r["B_MG"] for r in km)))
lb = np.log10(np.array([r["B_MG"] for r in km]))
T = np.array([r["Teff"] for r in km])
for nm, y in (("depth_pure", np.array([r["dep"] for r in km])),
              ("sigma", np.array([r["sig"] for r in km]))):
    b, se, t = ols(np.column_stack([np.ones(len(lb)), lb - np.mean(lb), T - np.mean(T)]), y)
    rho, p = stats.spearmanr(lb, y)
    print("%-10s B_beta=%+.4f t=%+.2f | Teff_beta=%+.4f t=%+.2f | spearman rho=%+.3f p=%.4f" % (nm, b[1], t[1], b[2], t[2], rho, p))
rs = np.array([r["rsig"] for r in km if r["rsig"] is not None])
km2 = [r for r in km if r["rsig"] is not None]
if len(rs) >= 8:
    lb2 = np.log10(np.array([r["B_MG"] for r in km2]))
    T2 = np.array([r["Teff"] for r in km2])
    b, se, t = ols(np.column_stack([np.ones(len(lb2)), lb2 - np.mean(lb2), T2 - np.mean(T2)]), rs)
    rho, p = stats.spearmanr(lb2, rs)
    print("R_sig(模型比值) B_beta=%+.4f t=%+.2f | spearman rho=%+.3f p=%.4f (n=%d)" % (b[1], t[1], rho, p, len(rs)))
else:
    print("R_sig 有效样本不足: %d" % len(rs))

# 分档（中场内部低/高 B）
print("\n== Kepler 中场分档（B<30 vs B>=30 MG）==")
lo = [r for r in km if r["B_MG"] < 30]
hi = [r for r in km if r["B_MG"] >= 30]
for nm, getf in (("depth_pure", lambda r: r["dep"]), ("sigma", lambda r: r["sig"])):
    if len(lo) >= 3 and len(hi) >= 3:
        a = [getf(r) for r in lo]; b2 = [getf(r) for r in hi]
        t, p = stats.ttest_ind(b2, a, equal_var=False)
        print("%-10s B<30: %.3f±%.3f (n=%d) | B>=30: %.3f±%.3f (n=%d) | diff %+.3f (%.0f%%) t=%.2f p=%.3f" % (
            nm, np.median(a), np.std(a), len(a), np.median(b2), np.std(b2), len(b2),
            np.median(b2) - np.median(a), 100 * (np.median(b2) - np.median(a)) / np.median(a), t, p))

# 跨目录对比：Kepler mid vs DESI mid/weak（纯线深物理量，同口径）
print("\n== 跨目录对比（纯线深 d_pure，同口径物理量）==")
def agg2(star):
    dp = [rec["d_pure"] for rec in star["lines"].values()]
    if not dp:
        return None
    return float(np.median(dp))
dw = [agg2(s) for s in ddata["weak"]]
dw = [v for v in dw if v is not None]
ddm = [agg2(s) for s in ddata["mid"]]
ddm = [v for v in ddm if v is not None]
dm = [r["dep"] for r in km]
print("DESI weak  : %.3f±%.3f (n=%d)" % (np.median(dw), np.std(dw), len(dw)))
print("DESI mid   : %.3f±%.3f (n=%d)" % (np.median(ddm), np.std(ddm), len(ddm)))
print("Kepler mid : %.3f±%.3f (n=%d)" % (np.median(dm), np.std(dm), len(dm)))
t, p = stats.ttest_ind(dm, ddm, equal_var=False)
print("Kepler mid vs DESI mid: t=%.2f p=%.3f（一致→跨仪器物理量可复现）" % (t, p))
t2, p2 = stats.ttest_ind(dm, dw, equal_var=False)
print("Kepler mid vs DESI weak: t=%.2f p=%.3f（显著低→跨仪器复现 B 效应）" % (t2, p2))
# Kepler mid 相对 DESI weak 的缺失幅度
print("Kepler mid 相对 DESI weak 深度缺失: %.0f%%" % (100 * (1 - np.median(dm) / np.median(dw))))

with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_kepler_reg.json"), "w", encoding="utf-8") as f:
    json.dump({"rows": krows}, f, ensure_ascii=False, indent=1)
print("\nwritten paperX_wd_kepler_reg.json")
