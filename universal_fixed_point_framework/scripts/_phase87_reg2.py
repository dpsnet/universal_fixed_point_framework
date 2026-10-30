# -*- coding: utf-8 -*-
"""Phase 87 M87-4/5（主判据，无模型依赖）：
sigma_obs / depth_obs 对 log10B 回归（弱场 vs 中场，同仪器同归一化，仪器项抵消）
线级展宽预言 sigma 增；拓扑禁戒预言 depth 降而 sigma 平。
附：35 颗有 Koester 模型谱者，输出 sigma 比值版本（模型消除 Teff 混杂）。
"""
import io, json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_linelevel.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

def agg(star, need_mod=False):
    """每星聚合：per-line d_pure（纯线深）/fwhm；need_mod 时要求有 sig_mod"""
    s_l, d_l, dp_l, f_l = [], [], [], []
    per = {}
    for ln, rec in star["lines"].items():
        if need_mod and "sig_mod" not in rec:
            continue
        s_l.append(rec["sig_obs"])
        d_l.append(rec["d_meas"])
        dp_l.append(rec["d_pure"])
        f_l.append(rec["fwhm"])
        per[ln] = {"sig": rec["sig_obs"], "dep": rec["d_pure"], "dep_bg": rec["d_meas"],
                   "fwhm": rec["fwhm"],
                   "sig_mod": rec.get("sig_mod"), "dep_mod": rec.get("d_pure_mod"),
                   "fwhm_mod": rec.get("fwhm_mod")}
    if not s_l:
        return None, per
    return {"sig": float(np.median(s_l)), "dep": float(np.median(dp_l)),
            "dep_bg": float(np.median(d_l)),
            "fwhm": float(np.nanmedian(f_l)), "n_lines": len(s_l)}, per

rows = []
rows_mod = []
per_all = {}
for grp in ("weak", "mid"):
    for star in data[grp]:
        a, per = agg(star)
        if a is None:
            continue
        rows.append({"gid": star["gid"], "B_MG": star["B_MG"], "Teff": star["Teff"],
                     "grp": grp, **a})
        per_all[star["gid"]] = per
        am, _ = agg(star, need_mod=True)
        if am is not None:
            rows_mod.append({"gid": star["gid"], "B_MG": star["B_MG"], "Teff": star["Teff"],
                             "grp": grp, "sig": am["sig"], "dep": am["dep"], **am})

lb = np.log10(np.array([r["B_MG"] for r in rows]))
T = np.array([r["Teff"] for r in rows])
S = np.array([r["sig"] for r in rows])
D = np.array([r["dep"] for r in rows])        # 纯线深
D_bg = np.array([r["dep_bg"] for r in rows])  # 含背景（对照）
F = np.array([r["fwhm"] for r in rows])
print("n=%d (weak %d / mid %d)" % (len(rows), sum(1 for r in rows if r["grp"] == "weak"),
                                   sum(1 for r in rows if r["grp"] == "mid")))
print("with-model subset n=%d (weak %d / mid %d)" % (
    len(rows_mod), sum(1 for r in rows_mod if r["grp"] == "weak"),
    sum(1 for r in rows_mod if r["grp"] == "mid")))

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

def boot_ci(x, y, nboot=5000, seed=42):
    rng = np.random.default_rng(seed)
    sl = []
    n = len(x)
    for _ in range(nboot):
        idx = rng.integers(0, n, n)
        b, *_ = ols(np.column_stack([np.ones(n), x[idx] - np.mean(x[idx])]), y[idx])
        sl.append(b[1])
    sl = np.array(sl)
    return np.percentile(sl, 2.5), np.percentile(sl, 97.5)

from scipy import stats
print("\n== 主判据：sig/dep(纯线深)/dep(含背景)/fwhm ~ log10B（单变量）==")
for nm, y in (("sigma", S), ("depth_pure", D), ("depth_bg", D_bg), ("fwhm", F)):
    b, se, t = ols(np.column_stack([np.ones(len(lb)), lb - np.mean(lb)]), y)
    lo, hi = boot_ci(lb, y)
    p = 2 * (1 - stats.t.cdf(abs(t[1]), len(y) - 2))
    print("%-12s beta=%+.4f t=%+.2f p=%.4f CI(%.4f,%.4f)" % (nm, b[1], t[1], p, lo, hi))

print("\n== 主判据：sig/dep ~ log10B + Teff（双变量）==")
X2 = np.column_stack([np.ones(len(lb)), lb - np.mean(lb), T - np.mean(T)])
for nm, y in (("sigma", S), ("depth_pure", D), ("depth_bg", D_bg), ("fwhm", F)):
    b, se, t = ols(X2, y)
    print("%-12s B_beta=%+.4f t=%+.2f | Teff_beta=%+.4f t=%+.2f" % (nm, b[1], t[1], b[2], t[2]))

print("\n== 分组中位（weak vs mid）==")
for nm, y in (("sigma", S), ("depth_pure", D), ("depth_bg", D_bg), ("fwhm", F)):
    w = y[np.array([r["grp"] == "weak" for r in rows])]
    m = y[np.array([r["grp"] == "mid" for r in rows])]
    print("%-12s weak %.3f±%.3f | mid %.3f±%.3f | diff %+.3f (%.1f%%)" % (
        nm, np.median(w), np.std(w), np.median(m), np.std(m),
        np.median(m) - np.median(w), 100 * (np.median(m) - np.median(w)) / np.median(w)))

print("\n== Teff 分档交叉验证（纯线深 depth_pure，弱 vs 中）==")
for lo, hi in ((8000, 16000), (16000, 25000)):
    sel = np.array([r["Teff"] for r in rows])
    mm = (sel >= lo) & (sel < hi)
    if mm.sum() < 4:
        print("[%d-%d kK] 样本不足 (%d)" % (lo, hi, mm.sum()))
        continue
    w = D[mm & np.array([r["grp"] == "weak" for r in rows])]
    m = D[mm & np.array([r["grp"] == "mid" for r in rows])]
    if len(w) >= 4 and len(m) >= 3:
        from scipy import stats as st
        t, p = st.ttest_ind(m, w, equal_var=False)
        print("[%d-%d kK] weak %.3f±%.3f (n=%d) | mid %.3f±%.3f (n=%d) | diff %+.3f (%.0f%%) t=%.2f p=%.3f" % (
            lo, hi, np.median(w), np.std(w), len(w), np.median(m), np.std(m), len(m),
            np.median(m) - np.median(w), 100 * (np.median(m) - np.median(w)) / np.median(w), t, p))
    else:
        print("[%d-%d kK] weak n=%d mid n=%d 不足" % (lo, hi, len(w), len(m)))

print("\n== 模型谱子集：R_sig=log10(sig_obs/sig_mod) ~ log10B（消除 Teff 混杂）==")
if len(rows_mod) >= 10:
    lbm = np.log10(np.array([r["B_MG"] for r in rows_mod]))
    Tm = np.array([r["Teff"] for r in rows_mod])
    # 每星 sig 比值（sig_mod 来自同星同线）
    rs = []
    for r in rows_mod:
        per = per_all[r["gid"]]
        v = [np.log10(per[ln]["sig"] / per[ln]["sig_mod"]) for ln in per if per[ln].get("sig_mod")]
        rs.append(float(np.median(v)))
    rs = np.array(rs)
    Xm = np.column_stack([np.ones(len(lbm)), lbm - np.mean(lbm), Tm - np.mean(Tm)])
    b, se, t = ols(Xm, rs)
    lo, hi = boot_ci(lbm, rs)
    p = 2 * (1 - stats.t.cdf(abs(t[1]), len(rs) - 3))
    print("R_sig B_beta=%+.4f t=%+.2f p=%.4f CI(%.4f,%.4f)" % (b[1], t[1], p, lo, hi))
    w = rs[np.array([r["grp"] == "weak" for r in rows_mod])]
    m = rs[np.array([r["grp"] == "mid" for r in rows_mod])]
    print("R_sig weak %.3f / mid %.3f (diff %+.3f dex)" % (np.median(w), np.median(m), np.median(m) - np.median(w)))

print("\n== 分线序（mid vs weak：sig/dep 中位差）==")
LN_ORDER = ["Hbeta", "Hgamma", "Hdelta", "Hepsilon", "Hzeta"]
for ln in LN_ORDER:
    w_s, w_d, m_s, m_d = [], [], [], []
    for r in rows:
        per = per_all.get(r["gid"], {}).get(ln)
        if not per:
            continue
        if r["grp"] == "weak":
            w_s.append(per["sig"]); w_d.append(per["dep"])
        else:
            m_s.append(per["sig"]); m_d.append(per["dep"])
    if w_s and m_s:
        print("%-9s sig: weak %.3f / mid %.3f (diff %+.3f) | dep: weak %.3f / mid %.3f (diff %+.3f, %.0f%%)" % (
            ln, np.median(w_s), np.median(m_s), np.median(m_s) - np.median(w_s),
            np.median(w_d), np.median(m_d), np.median(m_d) - np.median(w_d),
            100 * (np.median(m_d) - np.median(w_d)) / np.median(w_d)))
    else:
        print("%-9s 样本不足" % ln)

with io.open(os.path.join(BASE, "_gaia_abs", "paperX_wd_linelevel_reg.json"), "w", encoding="utf-8") as f:
    json.dump({"rows": rows, "rows_mod": rows_mod, "per_line": per_all}, f, ensure_ascii=False, indent=1)
print("\nwritten paperX_wd_linelevel_reg.json")
