# -*- coding: utf-8 -*-
"""S304 静默度参数化 + δ 候选 σ_score 严格裁决（2026-10-28）

两部分：
A. δ 候选 σ_score 严格裁决（S301/S302 遗留口径欠账——从未按 σ_score 判定）
   - δ = 15° − θ_F = 2.267180242° = 0.039569760 rad（θ_F = 12.7328197583°）
   - σ_θ = 1.32e-6 rad = 0.0000756°（S300——sens=51.2 传导，m_τ 不确定度 6.75e-5）
   - 裁决：|候选−δ|/σ_θ —— ≤1σ 达标、1-3σ 提示、>3σ 不达标
B. 静默度参数化扫描：θ_F/15°、δ/15° 的无量纲框架量候选
   - 框架常数：活跃=3、静默=5、不动点=4、幂基=2、显态=11、全态=16、
     SigmaInv=15、σ=1/15、约束域=42、k_max=8
   - 有限搜索：框架量小多项式组合
"""
import math

print("=== S304 静默度参数化 + δ 候选 σ_score 严格裁决 ===\n")

# ---- 基本量 ----
theta_F_deg = 12.7328197583
theta_F_rad = math.radians(theta_F_deg)
delta_deg = 15.0 - theta_F_deg          # 2.2671802417°
delta_rad = math.radians(delta_deg)     # 0.039569760 rad
sigma_theta_rad = 1.32e-6               # θ_F 传播不确定度（m_τ 传导——S300）
sigma_theta_deg = math.degrees(sigma_theta_rad)
print(f"θ_F = {theta_F_deg:.10f}° = {theta_F_rad:.12f} rad")
print(f"δ = 15°−θ_F = {delta_deg:.10f}° = {delta_rad:.12f} rad")
print(f"σ_θ = {sigma_theta_rad:.2e} rad = {sigma_theta_deg:.6f}°\n")

# ---- A. δ 候选 σ_score 严格裁决 ----
print("A. δ 候选 σ_score 严格裁决（|候选−δ|/σ_θ）：")
candidates = [
    ("静默⁻² = 1/25 = 0.04 rad", 0.04, "rad"),
    ("34/15° = 2.2666667°", 34/15, "deg"),
    ("15°·活跃/(不动点×静默) = 2.25°", 15*3/20, "deg"),
    ("1/(2·12.6) = 0.0396825 rad", 1/(2*12.6), "rad"),
    ("σ·9/4·15° = 2.25°（同 3）", 15*(1/15)*9/4, "deg"),
]
print(f"  参考：δ = {delta_deg:.10f}° / {delta_rad:.12f} rad——σ_θ = {sigma_theta_deg:.6f}°")
for name, val, unit in candidates:
    if unit == "deg":
        diff_deg = abs(val - delta_deg)
        score = diff_deg / sigma_theta_deg
    else:
        diff_deg = abs(math.degrees(val) - delta_deg)
        score = abs(val - delta_rad) / sigma_theta_rad
    verdict = "✓ 达标" if score <= 1 else ("△ 提示" if score <= 3 else "✗ 不达标(>3σ)")
    print(f"  {name:<38} 偏差 {diff_deg:.6f}°  σ_score = {score:8.2f}  {verdict}")

# ---- B. 静默度参数化扫描 ----
print(f"\nB. 静默度参数化（无量纲比值——有限框架量搜索）：")
t1 = theta_F_deg / 15.0          # θ_F/15°（连续静默度）
t2 = delta_deg / 15.0            # δ/15°（静默未满度）
t3 = theta_F_rad / (math.pi/12)  # θ_F/(π/12)（弧度——15° 的 π/12 身份）
print(f"  θ_F/15°  = {t1:.10f}")
print(f"  δ/15°    = {t2:.10f}")
print(f"  θ_F/(π/12) = {t3:.10f}")

# 框架量组合搜索（小多项式——a/b 型）
active, silent, fixed, power, visible, full, sigmaInv = 3, 5, 4, 2, 11, 16, 15
sigma = 1/15
quantities = {
    "活跃": active, "静默": silent, "不动点": fixed, "幂基": power,
    "显态": visible, "全态": full, "SigmaInv": sigmaInv, "σ": sigma,
    "静默⁻²": silent**-2, "σ²": sigma**2, "σ³": sigma**3,
    "活跃²": active**2, "静默²": silent**2, "不动点²": fixed**2,
    "活跃×静默": active*silent, "幂基²": power**2,
    "活跃²/静默": active**2/silent, "静默/活跃": silent/active,
    "活跃/静默": active/silent, "活跃/不动点": active/fixed,
    "不动点/活跃": fixed/active, "幂基/活跃": power/active,
    "活跃×不动点": active*fixed, "静默×不动点": silent*fixed,
    "σ×不动点": sigma*fixed, "σ×活跃": sigma*active,
    "显态/全态": visible/full, "显态/静默": visible/silent,
    "σ⁵": sigma**5, "σ⁷": sigma**7, "σ⁸": sigma**8,
    "σ⁵×活跃": sigma**5*active, "σ⁷×静默": sigma**7*silent,
}

print(f"\n  θ_F/15° = {t1:.6f}——候选扫描：")
hits1 = []
for name, q in quantities.items():
    if q > 0:
        diff = abs(t1 - q)
        if diff < 0.02:
            hits1.append((diff, name, q))
hits1.sort()
for d, n, q in hits1[:8]:
    print(f"    {n:<14} = {q:.6f}  偏差 {d:.6f}（相对 {d/q*100:.2f}%）")

print(f"\n  δ/15° = {t2:.6f}——候选扫描：")
hits2 = []
for name, q in quantities.items():
    if q > 0:
        diff = abs(t2 - q)
        if diff < 0.02:
            hits2.append((diff, name, q))
hits2.sort()
for d, n, q in hits2[:8]:
    print(f"    {n:<14} = {q:.6f}  偏差 {d:.6f}（相对 {d/q*100:.2f}%）")

print(f"\n  θ_F/(π/12) = {t3:.6f}——候选扫描：")
hits3 = []
for name, q in quantities.items():
    if q > 0:
        diff = abs(t3 - q)
        if diff < 0.02:
            hits3.append((diff, name, q))
hits3.sort()
for d, n, q in hits3[:8]:
    print(f"    {n:<14} = {q:.6f}  偏差 {d:.6f}（相对 {d/q*100:.2f}%）")

# 附加：δ 的轨道缺口视角——15−orbitCount 连续化
print(f"\n  轨道缺口视角：θ_F/15° = {t1:.4f}——连续化 orbitCount = 4+11·t1 = {4+11*t1:.4f}")
print(f"    最近整数轨道：12/13——对应 S.card≈12-13（打断 3-4 层）")
print(f"    无简单整数对应——静默度参数化（θ_F→S.card 线性映射）不可行")

print(f"\n结论：")
print(f"  A. δ 候选严格口径全部 >3σ——正式证伪（S301/S302 粗糙候选降级）")
print(f"  B. θ_F/15°、δ/15°、θ_F/(π/12) 无量纲比——无 <1% 框架量命中——")
print(f"     线性静默度参数化不可行（0.84885 不在任何 k/15 附近）")
