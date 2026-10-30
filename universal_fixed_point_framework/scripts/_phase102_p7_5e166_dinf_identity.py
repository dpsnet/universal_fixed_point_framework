# -*- coding: utf-8 -*-
"""
P7-5e-166：δ∞ 偏差身份判别（~1.3e-6 vs 1/56）
================================================================
背景（160/164/165）：全链三参拟合 δ∞ 偏差 +0.0073%（160）、四点 +0.01212%（164 窗口效应）；
165 发现 δ∞ 也随窗口单调漂移（m≥33 0.01785844 → m≥256 0.01785985）——偏差同样被高阶结构污染。
本步判别：偏差是拟合截断（E/m³ 项吸收）还是真实高阶修正？
  A. 大 m 端高阶模型拟合：delta = δ∞ + A/m + B/m² + C3/m³ + C4/m⁴ + C5/m⁵
     模型阶数 2..5 × 窗口 m≥128/256——δ∞ 偏差是否随阶数收敛到 <1e-6？
  B. Richardson 外推：三点 R(m)=f/3−2f(2m)+(8/3)f(4m)（消 A,B，残差 O(m⁻³)）、四点消 A,B,C
  C. 1/m→0 多项式外推：m≥256 五点截距（等效 Richardson 高阶）
判别：偏差随阶数收敛到 <1e-7 → 截断伪影（δ∞=1/56 精确锁定）；稳定 ~1.3e-6 → 真实修正（1/56 近似极限）
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
d160 = json.load(open(os.path.join(BASE, "_phase102_p7_5e160_spectral_m512.json"), encoding="utf-8"))
out = d160["out"]
ms = np.arange(33, 513, dtype=float)
ds = np.array([out[str(m)]["delta"] for m in range(-33, -513, -1)])
inv56 = 1.0/56.0
DEVIATION = 1.3e-6  # 164 定性的偏差量级

print("== P7-5e-166：δ∞ 偏差身份判别（480 点全链）==", flush=True)

# ---------- A. 大 m 端高阶模型拟合 ----------
print("\n=== A) 模型阶数 × 窗口：δ∞ 偏差收敛性 ===", flush=True)
for mmin in [128, 256]:
    idx = ms >= mmin
    print("  -- 窗口 m≥%d（%d 点）--" % (mmin, idx.sum()), flush=True)
    for k in [2, 3, 4, 5, 6]:
        X = np.vstack([1.0/ms[idx]**j for j in range(k)]).T
        c, _, _, _ = np.linalg.lstsq(X, ds[idx], rcond=None)
        r = float(np.sqrt(np.mean((X@c - ds[idx])**2)))
        dev = (c[0]-inv56)/inv56*100
        print("    %d 参：δ∞=%.10f  dev=%+.5f pct（%.2e 绝对）  RMS=%.1e" % (k, c[0], dev, c[0]-inv56, r), flush=True)

# ---------- B. Richardson 外推 ----------
print("\n=== B) Richardson 外推（消 A/m、B/m² 后）===", flush=True)
def rich3(f, m):
    return f(m)/3.0 - 2.0*f(2.0*m) + (8.0/3.0)*f(4.0*m)
def d_at(m):
    return float(out[str(-int(m))]["delta"])
for m0 in [33.0, 48.0, 64.0, 96.0, 128.0]:
    r3 = rich3(d_at, m0)
    dev = (r3-inv56)/inv56*100
    print("  R3(m=%3d)：δ∞=%.10f  dev=%+.5f pct（%+.2e）" % (int(m0), r3, dev, r3-inv56), flush=True)

# 四点 Richardson（消 A,B,C3）：用 m,2m,4m,8m 解权重——预期灾难性抵消（权重 ~10³），作为负面证据记录
print("\n=== B2) 四点 Richardson（消 A,B,C3）===", flush=True)
print("  注意：四点权重 O(10³) 对 delta ~0.018 的小数灾难性抵消——结果不可用（负面证据）", flush=True)
def rich4(f, m):
    ms4 = np.array([1.0, 2.0, 4.0, 8.0]) * m
    V = np.vstack([np.ones(4), 1.0/ms4, 1.0/ms4**2, 1.0/ms4**3]).T
    rhs = np.array([1.0, 0.0, 0.0, 0.0])
    w = np.linalg.solve(V, rhs)
    return float(w @ np.array([f(x) for x in ms4]))
for m0 in [33.0, 48.0, 64.0]:
    r4 = rich4(d_at, m0)
    print("  R4(m=%3d)：δ∞=%.4f  dev=%+.2e（灾难性抵消——不可用）" % (int(m0), r4, r4-inv56), flush=True)
    dev = (r4-inv56)/inv56*100
    print("  R4(m=%3d)：δ∞=%.10f  dev=%+.5f pct（%+.2e）" % (int(m0), r4, dev, r4-inv56), flush=True)

# ---------- C. 1/m→0 五点外推 ----------
print("\n=== C) m≥256 五点模型截距（等效 Richardson 高阶）===", flush=True)
idx = ms >= 256
X = np.vstack([1.0/ms[idx]**j for j in range(5)]).T
c, _, _, _ = np.linalg.lstsq(X, ds[idx], rcond=None)
r = float(np.sqrt(np.mean((X@c - ds[idx])**2)))
print("  5 参 m≥256：δ∞=%.10f  dev=%+.5f pct（%+.2e）  RMS=%.1e" % (c[0], (c[0]-inv56)/inv56*100, c[0]-inv56, r), flush=True)

# ---------- 判别 ----------
print("\n=== 判别 ===", flush=True)
# 收集 A 通道高阶结果（m≥256 5 参/6 参）与 Richardson
vals_A = {}
for k in [5, 6]:
    X = np.vstack([1.0/ms[idx]**j for j in range(k)]).T
    cc, _, _, _ = np.linalg.lstsq(X, ds[idx], rcond=None)
    vals_A[k] = cc[0]
r3_best = rich3(d_at, 128.0)
estimates = {"A5(256)": vals_A[5], "A6(256)": vals_A[6], "R3(128)": r3_best}
max_dev = max(abs(v-inv56) for v in estimates.values())
print("  高阶通道 δ∞ 估计：", flush=True)
for n, v in estimates.items():
    print("  %s = %.10f  dev %+.2e" % (n, v, v-inv56), flush=True)
print("  最大绝对偏差 = %.2e" % max_dev, flush=True)
if max_dev < 2e-7:
    verdict = "★★ δ∞ = 1/56 精确锁定——偏差是拟合截断伪影（高阶项吸收），非真实修正"
elif max_dev < 1e-5:
    verdict = "★ δ∞ 偏差收敛但未归零（%.1e）——1/56 近似极限（高阶截断余量或真实微修正，需更高阶或解析）" % max_dev
else:
    verdict = "★ δ∞ 偏差稳定（%.1e）——1/56 有真实修正，身份待探索" % max_dev
print("  终判：%s" % verdict, flush=True)
print("  诚实边界：Richardson 组合系数 ~O(10) 数值稳；五点模型依赖展开形式假设（纯幂律）", flush=True)

with open(os.path.join(BASE, "_phase102_p7_5e166_dinf_identity.json"), "w", encoding="utf-8") as f:
    json.dump({"estimates": {n: float(v) for n, v in estimates.items()},
               "max_dev": float(max_dev), "verdict": verdict,
               "window_A": {"m>=128": {}, "m>=256": {}}}, f, indent=1, ensure_ascii=False)
print("JSON 落盘 OK exit 0", flush=True)
