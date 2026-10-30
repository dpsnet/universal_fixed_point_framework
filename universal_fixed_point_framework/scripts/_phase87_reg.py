# -*- coding: utf-8 -*-
"""Phase 87 M87-4/5：σ/depth/EW 比值回归 + 分线序检验 + bootstrap"""
import io, json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_linelevel.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

def per_star_ratios(star):
    """返回该星各线 R_sigma/R_depth/R_ew（有 mod 的线），及每线记录"""
    rs, rd, re = [], [], []
    per = {}
    for ln, rec in star["lines"].items():
        if "sig_mod" not in rec or rec["sig_mod"] <= 0 or rec["sig_obs"] <= 0:
            continue
        r_s = np.log10(rec["sig_obs"] / rec["sig_mod"])
        r_d = np.log10(rec["d_obs"] / rec["d_mod"])
        ew_o = rec["d_obs"] * rec["sig_obs"]
        ew_m = rec["d_mod"] * rec["sig_mod"]
        r_e = np.log10(ew_o / ew_m)
        rs.append(r_s); rd.append(r_d); re.append(r_e)
        per[ln] = {"R_sigma": r_s, "R_depth": r_d, "R_ew": r_e}
    if not rs:
        return None, per
    return {"R_sigma": float(np.median(rs)), "R_depth": float(np.median(rd)),
            "R_ew": float(np.median(re)), "n_lines": len(rs)}, per

rows = []
per_all = {}
for grp in ("weak", "mid"):
    for star in data[grp]:
        agg, per = per_star_ratios(star)
        if agg is None:
            continue
        rows.append({"gid": star["gid"], "B_MG": star["B_MG"], "Teff": star["Teff"],
                     "grp": grp, **agg})
        per_all[star["gid"]] = per

B = np.array([r["B_MG"] for r in rows])
lb = np.log10(B)
T = np.array([r["Teff"] for r in rows])
RS = np.array([r["R_sigma"] for r in rows])
RD = np.array([r["R_depth"] for r in rows])
RE = np.array([r["R_ew"] for r in rows])
print("n=%d (weak %d / mid %d)" % (len(rows), sum(1 for r in rows if r["grp"] == "weak"),
                                   sum(1 for r in rows if r["grp"] == "mid")))

def ols(x, y):
    X = np.column_stack([np.ones(len(x)), x - np.mean(x)])
    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ beta
    resid = y - yhat
    n, p = len(y), 2
    s2 = np.sum(resid ** 2) / (n - p)
    cov = s2 * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    t = beta / se
    return beta, se, t, resid

def boot_ci(x, y, nboot=5000, seed=42):
    rng = np.random.default_rng(seed)
    sl = []
    n = len(x)
    for _ in range(nboot):
        idx = rng.integers(0, n, n)
        b, *_ = ols(x[idx], y[idx])
        sl.append(b[1])
    sl = np.array(sl)
    return np.percentile(sl, 2.5), np.percentile(sl, 97.5)

print("\n== 单变量: R ~ log10B ==")
for nm, y in (("R_sigma", RS), ("R_depth", RD), ("R_ew", RE)):
    b, se, t, _ = ols(lb, y)
    lo, hi = boot_ci(lb, y)
    print("%-9s beta=%+.4f  t=%+.2f  p~%.4f  CI(%.4f, %.4f)" % (nm, b[1], t[1],
          2 * (1 - __import__("scipy").stats.t.cdf(abs(t[1]), len(y) - 2)), lo, hi))

print("\n== 双变量: R ~ log10B + Teff ==")
X2 = np.column_stack([np.ones(len(lb)), lb - np.mean(lb), T - np.mean(T)])
for nm, y in (("R_sigma", RS), ("R_depth", RD), ("R_ew", RE)):
    beta, _, _, _ = np.linalg.lstsq(X2, y, rcond=None)
    yhat = X2 @ beta
    resid = y - yhat
    n, p = len(y), 3
    s2 = np.sum(resid ** 2) / (n - p)
    cov = s2 * np.linalg.inv(X2.T @ X2)
    se = np.sqrt(np.diag(cov))
    t = beta / se
    print("%-9s B_beta=%+.4f t=%+.2f | Teff_beta=%+.4f t=%+.2f" % (nm, beta[1], t[1], beta[2], t[2]))

print("\n== 分组均值（weak vs mid）==")
for nm, y in (("R_sigma", RS), ("R_depth", RD), ("R_ew", RE)):
    w = y[np.array([r["grp"] == "weak" for r in rows])]
    m = y[np.array([r["grp"] == "mid" for r in rows])]
    print("%-9s weak %+.3f (sd %.3f) | mid %+.3f (sd %.3f) | diff %+.3f" % (
        nm, np.mean(w), np.std(w), np.mean(m), np.std(m), np.mean(m) - np.mean(w)))

print("\n== 分线序（mid vs weak 每线 R_sigma/R_depth 中位）==")
LN_ORDER = ["Hbeta", "Hgamma", "Hdelta", "Hepsilon", "Hzeta"]
for ln in LN_ORDER:
    w_rs, w_rd, m_rs, m_rd = [], [], [], []
    for r in rows:
        per = per_all.get(r["gid"], {}).get(ln)
        if not per:
            continue
        if r["grp"] == "weak":
            w_rs.append(per["R_sigma"]); w_rd.append(per["R_depth"])
        else:
            m_rs.append(per["R_sigma"]); m_rd.append(per["R_depth"])
    if w_rs and m_rs:
        print("%-9s R_sig: weak %+.3f / mid %+.3f (diff %+.3f) | R_dep: weak %+.3f / mid %+.3f (diff %+.3f)" % (
            ln, np.median(w_rs), np.median(m_rs), np.median(m_rs) - np.median(w_rs),
            np.median(w_rd), np.median(m_rd), np.median(m_rd) - np.median(w_rd)))
    else:
        print("%-9s 样本不足" % ln)

# 落盘
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_linelevel_reg.json"), "w", encoding="utf-8") as f:
    json.dump({"rows": rows, "per_line": per_all}, f, ensure_ascii=False, indent=1)
print("\nwritten paperX_wd_linelevel_reg.json")
