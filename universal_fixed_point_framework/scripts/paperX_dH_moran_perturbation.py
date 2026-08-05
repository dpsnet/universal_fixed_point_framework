#!/usr/bin/env python3
"""
paperX_dH_moran_perturbation.py — d_H 偏差 δ 的一阶响应推导（2026-07-27）
====================================================================

目的
----
文档《层次演化的结构分析》（notes/08_first_principles/spectral_hierarchy_evolution_analysis.md）§3.2 将 d_H 分解为

    d_H = ln 15 + δ,   δ ≈ 0.00145

其中 δ 此前仅有"数值模式识别"（δ₁ = √2×10⁻³，偏差 2.5%）。
本脚本给出 δ 的**一阶结构推导**：将 δ 解释为 Moran 方程解对分支权重
非均匀性的线性响应，并用精确数值解验证。

推导（一阶微扰）
----------------
等权参考系：B 个分支、均匀收缩率 r，Moran 方程 B·r^{d₀} = 1 给出
唯一解 d₀ = ln B / ln(1/r)（唯一性已由 Lean 定理 moran_solution_iff 证明）。

扰动权重 cᵢ = r(1+εᵢ)。对 F(d,ε) = Σᵢ [r(1+εᵢ)]^d - 1 隐函数求导：

    ∂F/∂d|₀  = Σᵢ r^{d₀} ln r = ln r        （因 B·r^{d₀} = 1）
    ∂F/∂εᵢ|₀ = d₀ · r^{d₀} = d₀/B

    ⇒  ∂d/∂εᵢ = -d₀/(B·ln r) = d₀/(B·ln(1/r))

    ⇒  δ = d₀·ε̄/ln(1/r),   ε̄ = (1/B)Σᵢ εᵢ

对 B = 15、r = e⁻¹（ln(1/r) = 1）：**δ = ln(15)·ε̄**。

验证内容
--------
1. 参考解 d₀ = ln 15
2. 一阶公式 vs 精确解（均匀扰动，多个 ε 量级）
3. 反演：由 δ_obs 反推 ε̄（线性 vs 精确）
4. 非均匀扰动：随机 εᵢ，一阶公式 vs 精确求根
5. 实际 3-映射 IFS（c₁=S₃S₄, c₂=S₄, c₃≈1）的灵敏度系数（解析 vs 有限差分）
6. R2（Moran 非刚性）的定量刻画：d 对自由参数 c₃ 的极端敏感性
"""

import math
import random

B = 15
R = math.exp(-1.0)
D0 = math.log(B) / math.log(1.0 / R)   # = ln 15
D_FIT = 2.7095                          # χ² 拟合值（唯象输入）
DELTA_OBS = D_FIT - D0

checks = []
def check(name, ok, detail=""):
    checks.append((name, ok))
    print(f"  [{'✓' if ok else '✗'}] {name}  {detail}")

def moran_residual(d, weights):
    return sum(c ** d for c in weights) - 1.0

def solve_moran(weights, lo=1e-9, hi=50.0, tol=1e-14):
    """二分法求 Moran 方程 Σ cᵢ^d = 1 的唯一正根。"""
    flo, fhi = moran_residual(lo, weights), moran_residual(hi, weights)
    assert flo > 0 > fhi, "根不在区间内"
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        fm = moran_residual(mid, weights)
        if abs(fm) < tol:
            return mid
        if fm > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)

print("=" * 72)
print("d_H 偏差 δ 的一阶响应推导")
print("=" * 72)

# --- 1. 参考解 ----------------------------------------------------------------
print("\n[1] 等权参考解")
print(f"    d₀ = ln B / ln(1/r) = ln 15 = {D0:.7f}")
check("d₀ = ln 15", abs(D0 - math.log(15)) < 1e-12, f"d₀ = {D0:.7f}")

# --- 2. 一阶公式 vs 精确解（均匀扰动） ----------------------------------------
print("\n[2] 均匀扰动 cᵢ = r(1+ε)：一阶公式 δ = d₀·ε̄/ln(1/r) vs 精确解")
print(f"    {'ε':>10s} {'精确 δ':>12s} {'一阶 δ':>12s} {'相对误差':>10s}")
worst_rel = 0.0
for eps in [1e-4, 5e-4, 1e-3, 5e-3, 1e-2]:
    d_exact = solve_moran([R * (1 + eps)] * B)
    delta_exact = d_exact - D0
    delta_lin = D0 * eps / math.log(1.0 / R)
    rel = abs(delta_exact - delta_lin) / abs(delta_exact)
    worst_rel = max(worst_rel, rel if eps <= 1e-3 else 0.0)
    print(f"    {eps:>10.1e} {delta_exact:>12.6e} {delta_lin:>12.6e} {rel:>10.2e}")
check("一阶公式在 ε ≤ 10⁻³ 时相对误差 < 1%", worst_rel < 0.01,
      f"最大相对误差 = {worst_rel:.2e}")

# --- 3. 反演：δ_obs ⇒ ε̄ ------------------------------------------------------
print("\n[3] 由观测偏差反推平均权重扰动")
eps_lin = DELTA_OBS * math.log(1.0 / R) / D0
# 精确反演：d(ε) = ln15/(ln(1/r) - ln(1+ε)) = D_FIT
#   ⇒ ln(1+ε) = ln(1/r) - ln15/D_FIT
eps_exact = math.exp(math.log(1.0 / R) - math.log(B) / D_FIT) - 1.0
print(f"    δ_obs = {DELTA_OBS:.6e}")
print(f"    ε̄（线性） = {eps_lin:.6e}")
print(f"    ε̄（精确） = {eps_exact:.6e}")
rel_inv = abs(eps_exact - eps_lin) / eps_exact
check("线性反演与精确反演一致（<1%）", rel_inv < 0.01,
      f"相对偏差 = {rel_inv:.2e}")
print(f"    ⇒ δ ≈ 0.00145 对应 15 个等效分支的权重平均上调 {eps_exact*100:.4f}%")

# --- 4. 非均匀扰动 -------------------------------------------------------------
print("\n[4] 非均匀扰动：一阶公式 δ = d₀·mean(εᵢ)/ln(1/r) vs 精确求根")
random.seed(42)
worst_nu = 0.0
for trial in range(5):
    eps_i = [random.uniform(-1e-3, 2e-3) for _ in range(B)]
    d_exact = solve_moran([R * (1 + e) for e in eps_i])
    delta_lin = D0 * (sum(eps_i) / B) / math.log(1.0 / R)
    delta_exact = d_exact - D0
    if abs(delta_exact) > 1e-8:
        rel = abs(delta_exact - delta_lin) / abs(delta_exact)
        worst_nu = max(worst_nu, rel)
check("非均匀扰动下一阶公式仍成立（<2%）", worst_nu < 0.02,
      f"最大相对误差 = {worst_nu:.2e}")

# --- 5. 实际 3-映射 IFS 的灵敏度 ----------------------------------------------
print("\n[5] 实际 3-映射 IFS（c₁ = e^{-(3+d)}, c₂ = e^{-d}, c₃ 自由）的灵敏度")
def weights_3map(d, c3):
    return [math.exp(-(3.0 + d)), math.exp(-d), c3]
# 先求与 d = D_FIT 自洽的 c₃：c₃^d = 1 - c₁^d - c₂^d
c1d = math.exp(-(3.0 + D_FIT)) ** D_FIT
c2d = math.exp(-D_FIT) ** D_FIT
c3_fit = (1.0 - c1d - c2d) ** (1.0 / D_FIT)
print(f"    自洽 c₃ = {c3_fit:.7f}（文档 A.1 给出 ≈ 0.9998 ✓）")
# 解析灵敏度：∂d/∂ln cᵢ = -cᵢ^d / Σⱼ cⱼ^d ln cⱼ（对 ln c₃ 求导需考虑
# c₁, c₂ 对 d 的依赖；固定 c₁(d), c₂(d) 函数形式后 F(d, c₃) = 0）
def F3(d, c3):
    w = weights_3map(d, c3)
    return sum(x ** d for x in w) - 1.0
def dF3_dd(d, c3):
    w = weights_3map(d, c3)
    # c₁, c₂ 本身依赖 d：c₁^d = e^{-(3+d)d}, c₂^d = e^{-d²}
    t1 = math.exp(-(3.0 + d) * d) * (-(3.0 + 2.0 * d))
    t2 = math.exp(-d * d) * (-2.0 * d)
    t3 = (c3 ** d) * math.log(c3)
    return t1 + t2 + t3
def dF3_dlnc3(d, c3):
    # ∂F/∂ln c₃ = c₃ · ∂F/∂c₃ = c₃ · d·c₃^{d-1} = d·c₃^d
    return d * (c3 ** d)
sens_analytic = -dF3_dlnc3(D_FIT, c3_fit) / dF3_dd(D_FIT, c3_fit)
# 有限差分
h = 1e-7
c3_up = c3_fit * math.exp(h)
d_up = solve_moran(weights_3map(2.0, c3_up), lo=1.0, hi=5.0) if False else None
# 自洽求根：F3(d, c3) = 0
def solve_F3(c3, lo=1.0, hi=5.0):
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        fm = F3(mid, c3)
        if abs(fm) < 1e-15:
            return mid
        if fm > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)
d_num_up = solve_F3(c3_fit * math.exp(1e-6))
d_num_dn = solve_F3(c3_fit * math.exp(-1e-6))
sens_fd = (d_num_up - d_num_dn) / (2e-6)
print(f"    ∂d/∂ln c₃（解析）= {sens_analytic:.1f}")
print(f"    ∂d/∂ln c₃（差分）= {sens_fd:.1f}")
check("灵敏度解析与差分一致（<1%）",
      abs(sens_analytic - sens_fd) / abs(sens_fd) < 0.01,
      f"解析 {sens_analytic:.1f} vs 差分 {sens_fd:.1f}")

# --- 6. R2 的定量刻画 -----------------------------------------------------------
print("\n[6] Moran 非刚性（命题 R2）的定量验证")
dc3 = 1e-6
dd = solve_F3(c3_fit * (1 + dc3)) - D_FIT
print(f"    c₃ 相对变化 {dc3:.0e} ⇒ d 变化 {dd:.2e}")
print(f"    即 c₃ 的 10⁻⁶ 量级扰动即可产生与 δ 同量级的 d 移动")
print(f"    ⇒ d_H 被自由参数 c₃（近 1 收缩率）控制，无法由 Moran 方程锁定")
check("d 对 c₃ 的响应量级 ≈ 500×Δc₃/c₃", abs(dd) > 1e-4,
      f"Δd = {dd:.2e}（与 δ = {DELTA_OBS:.2e} 同量级）")

# --- 汇总 ----------------------------------------------------------------------
print("\n" + "=" * 72)
n_pass = sum(1 for _, ok in checks if ok)
print(f"汇总: {n_pass} / {len(checks)} 检查通过")
print("=" * 72)
print("""
结论
----
1. δ 的一阶结构公式：δ = ln(15)·ε̄（B = 15, r = e⁻¹），即偏差是分支权重
   平均相对扰动的 ln 15 倍。δ_obs = 0.00145 ⟺ ε̄ ≈ 5.35×10⁻⁴（0.054%）。
   这把 δ 从"数值模式识别"升级为可检验的单参数定量关系。
2. 新目标：从规范耦合/质量层级推导 ε̄ ≈ 5.4×10⁻⁴（替代此前 δ₁ = √2×10⁻³
   的猜测，后者隐含 ε̄₁ = δ₁/ln15 ≈ 5.22×10⁻⁴，偏差 2.5%）。
3. 实际 3-映射 IFS 中 d 对 c₃ 的灵敏度 ≈ 721（解析与差分一致），
   定量证实了命题 R2：Moran 方程不能锁定 d_H——c₃ 的 10⁻⁶ 相对扰动
   即可移动 d 约 7×10⁻⁴（与 δ 同量级）。范畴期望值 ln 15 的地位来自
   结构推导（§3.5），而非拟合。
""")
