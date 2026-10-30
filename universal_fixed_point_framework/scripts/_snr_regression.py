# -*- coding: utf-8 -*-
"""SNR 控制回归：复现 M83c（无 SNR）+ 加 log10(SNR) 项对比 beta(log10B)。
输入：_snr_results.json（SNR 下载结果）+ koester_ew.json + sample_list。"""
import io, json, os, math
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def rdj(name):
    with io.open(os.path.join(BASE, name), "r", encoding="utf-8") as f:
        return json.load(f)

snr = rdj("_snr_results.json")
lst = rdj("paperX_wd_m83c_sample_list.json")
ko = rdj("paperX_wd_m83c_koester_ew.json")

# koester_EW 按 name 索引
ko_by = {}
for s in ko.get("samples", []):
    nm = s.get("name") or s.get("sdss")
    if nm:
        ew = s.get("koester_EW")
        if ew is None:
            # 尝试其他键
            for k in ("koester_ew", "theo_EW", "ew"):
                if k in s and s[k] is not None:
                    ew = s[k]; break
        ko_by[nm] = ew

recs = []
for r in lst:
    nm = r["name"]
    if nm not in snr or nm not in ko_by:
        continue
    s = snr[nm]
    if "error" in s or "SN_MEDIAN" not in s and "SNR_est" not in s:
        continue
    kew = ko_by[nm]
    oew = r.get("obs_EW", 0)
    if not kew or not oew or kew <= 0 or oew <= 0:
        continue
    snr_v = s.get("SN_MEDIAN")
    if snr_v is None:
        snr_v = s.get("SNR_est")
    try:
        snr_f = float(snr_v)
    except Exception:
        continue
    if not np.isfinite(snr_f) or snr_f <= 0:
        continue
    recs.append({
        "name": nm, "log10B": math.log10(r["B_tesla"]), "Teff": r["Teff"], "logg": r["logg"],
        "resid": math.log10(oew / kew), "logSNR": math.log10(snr_f), "SNR": snr_f,
    })
print("n_records =", len(recs))

def ols(X, y):
    XtX = X.T @ X
    beta = np.linalg.solve(XtX, X.T @ y)
    resid = y - X @ beta
    n, p = X.shape
    s2 = resid @ resid / (n - p)
    cov = s2 * np.linalg.inv(XtX)
    se = np.sqrt(np.diag(cov))
    t = beta / se
    # p 值（正态近似）
    from scipy.special import erf
    from math import sqrt
    pv = 2 * (1 - 0.5 * (1 + erf(np.abs(t) / sqrt(2))))
    return beta, se, t, pv

recs = np.array([(r["log10B"], r["Teff"], r["logg"], r["resid"], r["logSNR"]) for r in recs], dtype=float)
Xb = recs[:, :3]; y = recs[:, 3]; ls = recs[:, 4]

# 中心化（与 M83c 口径一致：中心化 OLS）
def center(X):
    return X - X.mean(axis=0)
Xb_c = center(Xb)
ls_c = ls - ls.mean()

# 回归1：复现（无 SNR）
X1 = np.column_stack([np.ones(len(y)), Xb_c])
b1, se1, t1, p1 = ols(X1, y)
print("\n[R1 无SNR] n=%d beta=const %.4f log10B %.4f (t=%.2f p=%.2e) Teff %.2e (p=%.2e) logg %.4f (p=%.2e)"
      % (len(y), b1[0], b1[1], t1[1], p1[1], b1[2], p1[2], b1[3], p1[3]))

# 回归2：加 log10(SNR)
X2 = np.column_stack([np.ones(len(y)), Xb_c, ls_c])
b2, se2, t2, p2 = ols(X2, y)
print("[R2 含SNR] n=%d beta=const %.4f log10B %.4f (t=%.2f p=%.2e) Teff %.2e (p=%.2e) logg %.4f (p=%.2e) logSNR %.4f (t=%.2f p=%.2e)"
      % (len(y), b2[0], b2[1], t2[1], p2[1], b2[2], p2[2], b2[3], p2[3], b2[4], t2[4], p2[4]))

# Spearman 残差 vs log10B（含/不含 SNR 偏回归）
def spearman(x, yv):
    from scipy.stats import spearmanr
    return spearmanr(x, yv)

from scipy.stats import spearmanr
r1, p_s1 = spearmanr(Xb_c[:, 0], y)
# 偏相关：残差在去掉 logSNR 影响后的 log10B 与 resid 相关
def partial(x, z, yv):
    # x ~ z 残差, yv ~ z 残差, 相关
    def res(a, zz):
        Xz = np.column_stack([np.ones(len(zz)), zz])
        beta = np.linalg.lstsq(Xz, a, rcond=None)[0]
        return a - Xz @ beta
    rx = res(x, z); ry = res(yv, z)
    return spearmanr(rx, ry)

rp, p_rp = partial(Xb_c[:, 0], ls_c, y)
print("Spearman resid~log10B: rho=%.3f p=%.2e ; 偏相关(控制logSNR): rho=%.3f p=%.2e" % (r1, p_s1, rp, p_rp))

out = {"n": int(len(y)), "R1": {"log10B": float(b1[1]), "t": float(t1[1]), "p": float(p1[1])},
       "R2": {"log10B": float(b2[1]), "t": float(t2[1]), "p": float(p2[1]), "logSNR": float(b2[4]), "t_snr": float(t2[4]), "p_snr": float(p2[4])},
       "spearman": {"rho": float(r1), "p": float(p_s1)}, "partial_logSNR": {"rho": float(rp), "p": float(p_rp)}}
with io.open(os.path.join(BASE, "_snr_regression.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("saved _snr_regression.json")
