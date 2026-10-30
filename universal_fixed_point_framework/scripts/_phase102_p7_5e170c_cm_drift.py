# -*- coding: utf-8 -*-
"""
P7-5e-170c：C_m 漂移形式诊断——解释 0.10148→0.09902 的系统性偏离
================================================================
数据：160 JSON 的 Cm_seq_fixed（64/128/256/384/512）+ 170 全链（768/1024，同口径）。
模型候选：
  M1: C_m = C + D/m          （纯幂律高阶）
  M2: C_m = C + κ/√m         （慢衰减）
  M3: C_m = C + κ·log(m)/m   （log 修正）
  M4: C_m = C + κ/m^α        （自由指数）
判别：哪个模型 RMS 最低 + 外推 C 与 13/128 = 0.1015625 的距离。
"""
import json, numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
# 160 Cm_seq_fixed
d160 = json.load(open(BASE + r"\_phase102_p7_5e160_spectral_m512.json", encoding="utf-8"))
cm160 = {int(k): v for k, v in d160.get("Cm_seq_fixed", {}).items()}
# 170 全链重算（同口径）
d170 = json.load(open(BASE + r"\_phase102_p7_5e170_spectral_m1024.json", encoding="utf-8"))
out = d170["out"]

print("== P7-5e-170c：C_m 漂移形式诊断 ==", flush=True)
print("  160 Cm_seq_fixed 字段：%s" % {k: "%.8f" % v for k, v in sorted(cm160.items())}, flush=True)

# 170 口径重算（与 170b 一致）64/128 档
vals = {}
for m in [64, 128, 256, 384, 512, 768, 1024]:
    if m in cm160:
        vals[m] = cm160[m]
    else:
        invB = 1.0/out[str(-m)]["Bstar"]
        vals[m] = (invB - (m/2.0 + 1.0/8.0)) * m
ms = np.array(sorted(vals), dtype=float)
cm = np.array([vals[m] for m in ms])
print("  合并序列（%d 点）：%s" % (len(ms), {int(m): "%.6f" % vals[int(m)] for m in ms}), flush=True)

c13 = 13.0/128.0
print("\n  C_m 相对 13/128 偏离：%s" % {int(m): "%+.5f pct" % ((vals[int(m)]-c13)/c13*100) for m in ms}, flush=True)

def fit_model(model, ms_, cm_):
    A = np.vstack([np.ones_like(ms_), model(ms_)]).T
    c, _, _, _ = np.linalg.lstsq(A, cm_, rcond=None)
    r = float(np.sqrt(np.mean((A@c - cm_)**2)))
    return c, r

models = {
    "M1 C+D/m":       (lambda m: 1.0/m, "C+D/m"),
    "M2 C+κ/√m":      (lambda m: 1.0/np.sqrt(m), "C+κ/√m"),
    "M3 C+κ·lnm/m":   (lambda m: np.log(m)/m, "C+κ·ln(m)/m"),
    "M4a C+κ/m^0.5":  (lambda m: 1.0/m**0.5, "C+κ/m^0.5"),
}
print("\n-- 全序列（64..1024，%d 点）模型比较 --" % len(ms), flush=True)
results = {}
for name, (fn, lab) in models.items():
    c, r = fit_model(fn, ms, cm)
    results[name] = (c[0], r)
    print("  %s：C∞ = %.8f（13/128 差 %+.5f pct）RMS=%.2e" % (lab, c[0], (c[0]-c13)/c13*100, r), flush=True)

# M4 自由指数（非线性——扫 α）
print("\n-- M4 自由指数 α 扫描（C + κ/m^α）--", flush=True)
best = None
for alpha in np.linspace(0.1, 2.0, 39):
    c, r = fit_model(lambda m, a=alpha: 1.0/m**a, ms, cm)
    if best is None or r < best[2]:
        best = (alpha, c[0], r)
print("  最优 α = %.2f：C∞ = %.8f（13/128 差 %+.5f pct）RMS=%.2e" %
      (best[0], best[1], (best[1]-c13)/c13*100, best[2]), flush=True)

# 尾段（256..1024）只拟合幂律
print("\n-- 尾段（256..1024，%d 点）--" % len(ms[ms >= 256]), flush=True)
for name, (fn, lab) in models.items():
    sel = ms >= 256
    c, r = fit_model(fn, ms[sel], cm[sel])
    print("  %s：C∞ = %.8f（13/128 差 %+.5f pct）RMS=%.2e" % (lab, c[0], (c[0]-c13)/c13*100, r), flush=True)

# 尾段差分（ΔC_m vs Δ(1/m^α)）——看下降形态
print("\n-- 尾段差分形态（256→1024）--", flush=True)
for i in range(len(ms)-1):
    dm = ms[i+1] - ms[i]
    dcm = cm[i+1] - cm[i]
    print("  Δm=%4d→%4d：ΔC_m = %+.6f（Δ(1/m) = %+.2e）" % (ms[i], ms[i+1], dcm, 1.0/ms[i+1]-1.0/ms[i]), flush=True)
print("exit 0", flush=True)
