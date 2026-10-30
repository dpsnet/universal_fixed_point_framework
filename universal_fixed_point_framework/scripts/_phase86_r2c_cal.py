# -*- coding: utf-8 -*-
"""Phase 86 R2c：Teff 分档 + Gaia G 交叉校准后的绝对残差对比
校准链：F_model_cal(λ) = F_model(λ) x k, k = F_obs(G带) / F_model(G带)（消除视差/质量半径/红化系统因子）
输出 scripts/_gaia_abs/paperX_wd_absflux_cal.json
"""
import json, io, os
import numpy as np
from scipy import stats

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
OUT = os.path.join(BASE, "_gaia_abs")
with io.open(os.path.join(OUT, "paperX_wd_absflux.json"), "r", encoding="utf-8") as f:
    data = json.load(f)
rows = data["rows"]

# 交叉校准：slopeB 带（5000-5800，无 Balmer 线）作为 G 带代理（G ~ 5400 Å）
# k = F_obs(slopeB) / F_mod(slopeB)
for r in rows:
    if r.get("slopeB_obs") and r.get("slopeB_mod"):
        r["k_g"] = r["slopeB_obs"] / r["slopeB_mod"]
        for nm in ["blue", "red", "slopeA"]:
            if r.get(nm + "_obs") and r.get(nm + "_mod"):
                r[nm + "_calres"] = float(np.log10(r[nm + "_obs"] / (r[nm + "_mod"] * r["k_g"])))
    else:
        r["k_g"] = None

with io.open(os.path.join(OUT, "paperX_wd_absflux_cal.json"), "w", encoding="utf-8") as f:
    json.dump({"n": len(rows), "note": "k_g = F_obs(5000-5800)/F_mod(5000-5800) 交叉校准；calres = log10(obs/(mod*k_g))",
               "rows": rows}, f, ensure_ascii=False, indent=1)

def grp(rows, cond, key):
    vs = [r[key] for r in rows if cond(r) and r.get(key) is not None and not (isinstance(r[key], float) and np.isnan(r[key]))]
    return vs

print("=== Teff 分档：校准后绝对残差（弱场 vs 中场）===")
for tmin, tmax, tnm in [(None, 10000, "<10kK"), (10000, 20000, "10-20kK"), (20000, None, ">20kK")]:
    for key in ["blue_calres", "red_calres", "slopeA_calres"]:
        w = grp(rows, lambda r, a=tmin, b=tmax: r["B_MG"] < 10 and (a is None or r["Teff"] >= a) and (b is None or r["Teff"] < b), key)
        m = grp(rows, lambda r, a=tmin, b=tmax: 10 <= r["B_MG"] < 100 and (a is None or r["Teff"] >= a) and (b is None or r["Teff"] < b), key)
        if len(w) >= 3 and len(m) >= 3:
            t, p = stats.ttest_ind(m, w, equal_var=False)
            print("%-9s %-12s 弱场 n=%2d mean=%+.4f | 中场 n=%2d mean=%+.4f | t=%.2f p=%.4f" % (
                tnm, key, len(w), np.mean(w), len(m), np.mean(m), t, p))
        else:
            print("%-9s %-12s 弱场 n=%d 中场 n=%d (样本不足)" % (tnm, key, len(w), len(m)))

print("\n=== 校准因子 k_g 分布 ===")
k = [r["k_g"] for r in rows if r.get("k_g") and not np.isnan(r["k_g"])]
print("k_g: med=%.3f sd=%.3f (1.0 = 模型绝对流量与观测一致)" % (np.median(k), np.std(k)))

print("\n=== 中场-弱场偏移（校准后）vs EW 缺失 ===")
for key in ["blue_calres", "red_calres", "slopeA_calres"]:
    w = grp(rows, lambda r: r["B_MG"] < 10, key)
    m = grp(rows, lambda r: 10 <= r["B_MG"] < 100, key)
    if len(w) >= 5 and len(m) >= 5:
        d = np.mean(m) - np.mean(w)
        print("%-14s 中场-弱场 = %+.4f dex（EW 线缺失 -0.275 dex；Phase 85 slope 偏移 -0.042）" % (key, d))
