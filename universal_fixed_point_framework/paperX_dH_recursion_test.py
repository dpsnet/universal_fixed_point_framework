#!/usr/bin/env python3
"""
paperX_dH_recursion_test.py — δ 的两级粘合递归 IFS 检验（2026-07-27）
====================================================================

目的
----
检验文档 §3.5.4b 候选假说的"15 递归"解读：
δ = (29/2)×10⁻⁴ 中 29 = 2×15 − 1 是否来自两级粘合递归 IFS 的结构。

模型
----
两级递归：15 个一级分支中，14 个（主动层）各细分出 15 个二级分支
（收缩率 r²），1 个（对象层，非主动）保持不细分（粘合/共享分支，
收缩率 r）。对象层可部分细分，比例 ρ ∈ [0,1]：

    F(d) = (1−ρ)·r^d + (B(B−1) + ρB)·r^{2d} − 1 = 0

关键解析事实（本脚本数值验证）
------------------------------
1. 均匀收缩率下，x = r^d 满足 B(B−1)x² + x − 1 = 0（ρ = 0），
   判别式 1 + 4B(B−1) = (2B−1)² 对任意 B 为完全平方，
   精确根 x = 1/B ⟹ d = ln B/ln(1/r) = ln 15（δ = 0）。
   且该结果与粘合比例 ρ 无关（自相似守恒）。
   ⇒ 递归结构本身锁定 d = ln 15，δ 只能来自收缩率非均匀性。
2. 对扰动（一级分支 r(1+ε₁)，二级分支 r²(1+ε₂)）隐函数求导：
       ∂F/∂d = −(2B−1)/B² · ln(1/r)  …（29 出现在响应分母）
       δ = ln B/ln(1/r) · (ε₁ + (B−1)ε₂)/(2B−1)
   B = 15, r = e⁻¹ 时：δ = ln(15)·(ε₁ + 14ε₂)/29。
   ⇒ 29 的结构角色是响应系数分母 (2B−1)，而非 δ 的分子。
3. 每级均匀扰动（一级 r(1+ε)、二级复合 r²(1+ε)²，即 ε₂ = (1+ε)²−1）
   退化为一阶公式 δ = ln(15)·ε（与 paperX_dH_moran_perturbation.py
   一致，交叉验证）。注意 ε₂ 定义为二级复合收缩率的相对超出。
"""

import math

B = 15
R = math.exp(-1.0)
D0 = math.log(B)                      # ln 15（r = e⁻¹ 时 ln(1/r) = 1）
D_FIT = 2.7095
DELTA_OBS = D_FIT - D0

checks = []
def check(name, ok, detail=""):
    checks.append((name, ok))
    print(f"  [{'✓' if ok else '✗'}] {name}  {detail}")

def F_glued(d, rho=0.0, e1=0.0, e2=0.0):
    """两级粘合递归 Moran 残差。
    一级（对象层分支）：权重 (1−ρ)，收缩率 r(1+ε₁)
    二级分支：B(B−1) + ρB 个，收缩率 r²(1+ε₂)"""
    return ((1 - rho) * (R * (1 + e1)) ** d
            + (B * (B - 1) + rho * B) * (R ** 2 * (1 + e2)) ** d - 1.0)

def solve(d_lo=1.0, d_hi=5.0, **kw):
    flo = F_glued(d_lo, **kw)
    assert flo > 0 > F_glued(d_hi, **kw)
    for _ in range(300):
        mid = 0.5 * (d_lo + d_hi)
        fm = F_glued(mid, **kw)
        if abs(fm) < 1e-16:
            return mid
        if fm > 0:
            d_lo = mid
        else:
            d_hi = mid
    return 0.5 * (d_lo + d_hi)

print("=" * 72)
print("δ 的两级粘合递归 IFS 检验")
print("=" * 72)

# --- 1. 精确根 x = 1/15（判别式 841 = 29²） ------------------------------------
print("\n[1] 粘合递归 Moran 方程 B(B−1)x² + x − 1 = 0 的精确根")
disc = 1 + 4 * B * (B - 1)
x_exact = (-1 + math.isqrt(disc)) / (2 * B * (B - 1))
print(f"    判别式 1 + 4·{B}·{B-1} = {disc} = {math.isqrt(disc)}²")
print(f"    x = {x_exact:.10f}，1/B = {1/B:.10f}")
check("判别式为完全平方且 x = 1/B 精确",
      math.isqrt(disc) ** 2 == disc and abs(x_exact - 1 / B) < 1e-15,
      f"√{disc} = {math.isqrt(disc)} = 2B−1")

# --- 2. 递归维数锁定：d = ln 15，与粘合比例 ρ 无关 ------------------------------
print("\n[2] 均匀收缩率下递归维数锁定（δ = 0，∀ρ）")
worst = 0.0
for rho in [0.0, 0.25, 0.5, 0.75, 1.0]:
    d = solve(rho=rho)
    worst = max(worst, abs(d - D0))
    print(f"    ρ = {rho:.2f}  ⇒  d = {d:.10f}（ln 15 = {D0:.10f}）")
check("d = ln 15 精确锁定（所有 ρ）", worst < 1e-10,
      f"最大偏差 = {worst:.2e}")

# --- 3. 完全平方恒等式对任意 B 成立 ----------------------------------------------
print("\n[3] 恒等式 1 + 4B(B−1) = (2B−1)² 的一般性")
ok_all = all(1 + 4 * b * (b - 1) == (2 * b - 1) ** 2 for b in range(2, 1000))
check("1 + 4B(B−1) = (2B−1)² 对 B = 2..999 成立", ok_all, "代数恒等式")

# --- 4. 响应系数公式 δ = ln15·(ε₁ + 14ε₂)/29 ------------------------------------
print("\n[4] 扰动响应公式 δ = ln(15)·(ε₁ + 14ε₂)/29 vs 精确解")
print(f"    {'ε₁':>9s} {'ε₂':>9s} {'精确 δ':>12s} {'公式 δ':>12s} {'相对误差':>10s}")
worst_resp = 0.0
for e1, e2 in [(1e-3, 0.0), (0.0, 1e-3), (5e-4, 5e-4), (-2e-4, 8e-4), (1e-3, -1e-4)]:
    d = solve(e1=e1, e2=e2)
    delta_exact = d - D0
    delta_formula = D0 * (e1 + (B - 1) * e2) / (2 * B - 1)
    rel = abs(delta_exact - delta_formula) / max(abs(delta_exact), 1e-12)
    if abs(delta_exact) > 1e-8:
        worst_resp = max(worst_resp, rel)
    print(f"    {e1:>9.1e} {e2:>9.1e} {delta_exact:>12.6e} {delta_formula:>12.6e} {rel:>10.2e}")
check("响应公式与精确解一致（<1%）", worst_resp < 0.01,
      f"最大相对误差 = {worst_resp:.2e}")

# --- 5. 均匀极限退化为一阶公式 ---------------------------------------------------
# 注意：真正的"均匀"扰动是每级收缩率都乘 (1+ε)，此时二级复合收缩率为
# (r(1+ε))² = r²(1+ε)²，即 ε₂ = (1+ε)² − 1 = 2ε + ε²（而非 ε₂ = ε）。
print("\n[5] 每级均匀扰动 ⇒ ε₂ = (1+ε)²−1，退化：δ = ln(15)·ε")
eps = 5e-4
d = solve(e1=eps, e2=(1 + eps) ** 2 - 1)
delta_exact = d - D0
delta_uniform = D0 * eps
rel = abs(delta_exact - delta_uniform) / abs(delta_exact)
print(f"    ε = {eps:.1e}（ε₂ = {(1+eps)**2-1:.6e}）：精确 δ = {delta_exact:.6e}，一阶公式 δ = {delta_uniform:.6e}")
check("均匀极限与 paperX_dH_moran_perturbation 一致（<1%）", rel < 0.01,
      f"相对误差 = {rel:.2e}")

# --- 6. 反演与预测 ---------------------------------------------------------------
print("\n[6] 反演：δ_obs 需要的扰动组合")
e2_needed = (2 * B - 1) * DELTA_OBS / ((B - 1) * D0)
e1_needed = (2 * B - 1) * DELTA_OBS / D0
print(f"    纯二级扰动：ε₂ = 29δ/(14·ln15) = {e2_needed:.4e}")
print(f"    纯一级扰动：ε₁ = 29δ/ln15     = {e1_needed:.4e}")
d_check = solve(e2=e2_needed)
check("纯二级扰动反演自洽（|d − d_fit| < 10⁻⁵）",
      abs(d_check - D_FIT) < 1e-5, f"d = {d_check:.7f}")

print("\n    预测对照（δ_obs = {:.6e}）：".format(DELTA_OBS))
for label, e1, e2 in [("ε₂ = 10⁻³（质量层级量级，纯二级）", 0.0, 1e-3),
                      ("ε₁ = 10⁻³（纯一级对象分支）", 1e-3, 0.0),
                      ("每级均匀 ε = 5.35×10⁻⁴", 5.352e-4, (1 + 5.352e-4) ** 2 - 1)]:
    d = solve(e1=e1, e2=e2)
    delta_pred = d - D0
    dev = abs(delta_pred - DELTA_OBS) / DELTA_OBS
    print(f"    {label:<36s} δ = {delta_pred:.4e}（偏差 {dev:.1%}）")

# --- 汇总 ------------------------------------------------------------------------
print("\n" + "=" * 72)
n_pass = sum(1 for _, ok in checks if ok)
print(f"汇总: {n_pass} / {len(checks)} 检查通过")
print("=" * 72)
print("""
结论
----
1. 【递归不变性】两级粘合递归 IFS 在均匀收缩率下把维数**精确锁定**在
   d = ln B（B = 15 时 ln 15），与粘合比例 ρ 无关。这从递归角度
   **加强**了 d_H = ln 15 的地位：ln 15 是递归不动点，而非偶然数值。
2. 【29 的结构角色】粘合 Moran 方程判别式 1 + 4B(B−1) = (2B−1)²
   （B = 15 时 841 = 29²）是完全平方恒等式；29 = 2B−1 出现在
   **扰动响应系数的分母**：δ = ln(15)·(ε₁ + 14ε₂)/29。
   这解释了候选假说中 29 的"出现"，但其结构位置在响应函数中，
   而非 δ 的分子——§3.5.4b 的 δ = (29/2)×10⁻⁴ 读法可能是
   对响应结构的误读。
3. 【δ 的来源】递归本身不产生 δ（δ = 0 精确），δ 必须来自收缩率的
   层级非均匀性 (ε₁, ε₂)。δ_obs 要求：纯二级 ε₂ ≈ 1.11×10⁻³，
   或纯一级 ε₁ ≈ 1.55×10⁻²，或每级均匀 ε ≈ 5.35×10⁻⁴（同前结论）。
4. 【权重通道】扰动按 (1, B−1, 2B−1) = (1, 14, 29) 的分支计数加权：
   对象层分支 1 票、14 个主动细分分支各 1 票——层表（L151-159）的
   主动/非主动划分直接决定了响应结构。
""")
