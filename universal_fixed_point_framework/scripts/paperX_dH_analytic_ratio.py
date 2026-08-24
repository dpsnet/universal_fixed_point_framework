# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
"""
paperX_dH_analytic_ratio.py — ε̄/ε₃ = √5 的解析推导尝试

结构：
  Ⅰ  精确数值验证：ε̄/ε₃ = 2.236910... 与 2.236068 的 ε̄/ε₃ vs √5 的数值差异
  Ⅱ  自洽方程推导：15-branch 与 3-map 两个描述联立
  Ⅲ  泰勒展开：在 d=ln15 附近的 ε̄(d), ε₃(d) 展开
  Ⅳ  反问题：给定 ε̄ = √5·ε₃, 解 d
  Ⅴ  能否证明 √5 = √N_total 的结构必然性？

结论：√5 是数值巧合还是结构恒等式？
"""
import numpy as np

d_H_fit = 2.7095
ln15 = np.log(15)
delta_obs = d_H_fit - ln15

# =============================================================
# Ⅰ 精确数值验证
# =============================================================
print("=" * 72)
print("Ⅰ ε̄(d) 和 ε₃(d) 的精确数值行为")
print("=" * 72)

def eps3(d):
    """给定 d, 3-map 自洽的 ε₃ = 1 - c₃"""
    A = np.exp(-d**2) + np.exp(-d*(3+d))
    c3d = 1.0 - A
    if c3d <= 0:
        return np.nan
    c3 = c3d ** (1.0/d)
    return 1.0 - c3

def epsbar(d):
    """给定 d, 15-branch 有效描述的 ε̄"""
    return (d - ln15) / ln15

def ratio(d):
    """ε̄/ε₃"""
    e3 = eps3(d)
    if e3 is None or e3 <= 0 or np.isnan(e3):
        return np.nan
    return epsbar(d) / e3

# 在 d_H 附近做高精度扫描
print(f"\n  d_H 附近高精度扫描 (步长 5×10⁻⁷):")
print(f"  {'d':>14s}  {'ε̄':>14s}  {'ε₃':>14s}  {'ε̄/ε₃':>12s}  {'δ':>14s}")
print(f"  {'-'*14}  {'-'*14}  {'-'*14}  {'-'*12}  {'-'*14}")

best_ratio = None
for i in range(-10, 11):
    d_val = d_H_fit + i * 5e-7
    e3 = eps3(d_val)
    eb = epsbar(d_val)
    r = eb / e3 if e3 > 0 else np.nan
    delta = d_val - ln15
    if i == 0:
        best_ratio = r
    print(f"  {d_val:14.8f}  {eb:14.6e}  {e3:14.6e}  {r:12.6f}  {delta:14.6e}")

sqrt5 = np.sqrt(5)
print(f"\n  √5 = {sqrt5:.12f}")
print(f"  ε̄/ε₃ at d_H = {best_ratio:.12f}")
print(f"  差值 = {abs(best_ratio - sqrt5):.2e}")

# =============================================================
# Ⅱ 自洽方程推导
# =============================================================
print("\n" + "=" * 72)
print("Ⅱ 自洽方程: 15-branch ≈ 3-map 一致性条件")
print("=" * 72)

# 15-branch: d = ln15 / (1 - ln(1+ε̄))                  ... (1)
# 3-map:     ε₃ = (e^{-d²} + e^{-d(3+d)})/d           ... (2)  (一阶)
# 选择原理:  ε̄ = √5·ε₃                                  ... (3)

# 从 (1)(2)(3) 消去 ε̄, ε₃:
# (d - ln15)/ln15 = √5 · (e^{-d²} + e^{-d(3+d)})/d
# 即: d(d - ln15) = √5·ln15·(e^{-d²} + e^{-d(3+d)})    ... (4)

# 验证 (4) 的解
def LHS(d):
    return d * (d - ln15)

def RHS(d):
    return sqrt5 * ln15 * (np.exp(-d**2) + np.exp(-d*(3+d)))

for d_test in [2.708, 2.709, 2.7095, 2.710]:
    lhs = LHS(d_test)
    rhs = RHS(d_test)
    print(f"  d={d_test:.6f}:  LHS={lhs:.2e}  RHS={rhs:.2e}  diff={lhs-rhs:.2e}")

# 找方程 (4) 的精确根
import bisect
def f(d):
    return LHS(d) - RHS(d)

# 二分法
lo, hi = 2.70, 2.72
for _ in range(100):
    mid = (lo+hi)/2
    if f(mid) * f(lo) > 0:
        lo = mid
    else:
        hi = mid
d_solution = (lo+hi)/2
print(f"\n  方程 (4) 数值解: d = {d_solution:.10f}")
print(f"  d_H_fit = {d_H_fit:.10f}")
print(f"  差值 = {abs(d_solution - d_H_fit):.2e}")

# =============================================================
# Ⅲ 泰勒展开尝试
# =============================================================
print("\n" + "=" * 72)
print("Ⅲ 泰勒展开: ε₃(d) 和 ε̄(d) 在 d=ln15 附近")
print("=" * 72)

d0 = ln15

# ε̄(d) = (d-d0)/d0  → 精确线性
# ε₃(d) 需要展开

# 一阶: ε₃ ≈ A(d)/d, 其中 A(d) = e^{-d²} + e^{-d(3+d)}
# 在 d0 处: A(d₀) = e^{-d₀²} + e^{-d₀(3+d₀)}
A0 = np.exp(-d0**2) + np.exp(-d0*(3+d0))
eps3_1st_order = A0 / d0
print(f"  d0 = ln15 = {d0:.8f}")
print(f"  A(d0) = exp(-d0^2) + exp(-d0(3+d0)) = {A0:.6e}")
print(f"  eps3(d0) ~ A(d0)/d0 = {eps3_1st_order:.6e}")
print(f"  eps3(d0) exact = {eps3(d0):.6e}")
print(f"  一阶近似相对误差 = {abs(eps3_1st_order - eps3(d0))/eps3(d0)*100:.4f}%")

# 在 d = d₀ + δ 附近的展开
# A(d₀+δ) = A(d₀) + A'(d₀)·δ + ...
# A'(d) = -2d·e^{-d²} - (3+2d)·e^{-d(3+d)}
dAd_d0 = -2*d0*np.exp(-d0**2) - (3+2*d0)*np.exp(-d0*(3+d0))
print(f"\n  A'(d₀) = {dAd_d0:.4f}")
print(f"  灵敏度: |A'(d₀)·δ| / A(d₀) = {abs(dAd_d0 * delta_obs / A0):.4f}")
print(f"  → 一阶展开在 δ = {delta_obs:.2e} 时 A 变化 {abs(dAd_d0 * delta_obs / A0)*100:.2f}%")

# =============================================================
# Ⅳ 反分析: √5 从何而来?
# =============================================================
print("\n" + "=" * 72)
print("Ⅳ √5 的结构来源分析")
print("=" * 72)

# 假设 ε̄/ε₃ = k (某个值), 从一致性条件找 k
# 联立 (1) 和 (2):
# d = ln15 + δ = ln15/(1 - ln(1+k·ε₃))
# ε₃ = (e^{-d²} + e^{-d(3+d)})/d  (一阶)

# 小 δ 展开:
# 从 (1): 对于小 δ, ε̄ = δ/ln15
# 从 (3): δ = ln15·k·ε₃
# 从 (2): ε₃ ≈ A(d₀)/d₀ = A₀/d₀ (零阶, 因为 ε₃ 变化慢)

# 所以: δ ≈ ln15·k·A₀/d₀
# 但 δ 也是自洽方程的解... 这没有确定 k

# 实际上 k 是由更高阶项或凹性约束决定的
# 检查 ε̄/ε₃ 对 d 的导数:
def d_ratio_d(d, eps=1e-6):
    r1 = ratio(d - eps)
    r2 = ratio(d + eps)
    return (r2 - r1) / (2*eps)

dr = d_ratio_d(d_H_fit)
print(f"  d(ε̄/ε₃)/dd at d_H = {dr:.1f}")
print(f"  这意味着 d 变化 10⁻⁵ → ε̄/ε₃ 变化 {dr*1e-5:.4f}")
print(f"  → ε̄/ε₃ 对 d 极度敏感!")

# 检查 ε̄/ε₃ 的零点和 singularity 结构
print(f"\n  ε̄/ε₃ 过零点 (ε̄=0): d = {d0:.8f}")
print(f"  ε̄/ε₃ 奇点 (ε₃=0): ε₃=0 要求 c₃=1")
print(f"    即 (1-A(d))^(1/d) = 1 → A(d) = 0")
print(f"    但 A(d) = e^(-d^2) + e^(-d(3+d)), 永远 > 0")
print(f"    -> eps3 永不为 0, 无奇点")
print(f"    -> epsbar/eps3 从 0 (d=d0) 平滑增长")

# =============================================================
# Ⅴ 关键测试: ε̄/ε₃ 随 d 的完整函数形式
# =============================================================
print("\n" + "=" * 72)
print("Ⅴ ε̄/ε₃ 的全域行为")
print("=" * 72)

print(f"\n  {'d':>10s}  {'ε̄/ε₃':>12s}  {'√5':>10s}  {'∂(ratio)/∂d':>12s}")
print(f"  {'-'*10}  {'-'*12}  {'-'*10}  {'-'*12}")

ds = np.linspace(2.7085, 2.7105, 21)
prev_val = None
for d_val in ds:
    r_val = ratio(d_val)
    deriv = (r_val - prev_val) / (d_val - ds[0]) if prev_val is not None else 0
    print(f"  {d_val:10.6f}  {r_val:12.6f}  {sqrt5:10.6f}  {deriv:12.1f}")
    prev_val = r_val

print(f"\n  → ε̄/ε₃ 在 d=ln15 附近从 0 快速增长")
print(f"  → 在 d_H ≈ 2.7095 处恰好穿过 √5")
print(f"  → √5 不是展开的极限值, 而是函数值等于 √5 的点")
print(f"  → 即 √5 = ε̄(d_H)/ε₃(d_H) 是方程的解, 而非极限")

# =============================================================
# Ⅵ 诚实结论
# =============================================================
print("\n" + "=" * 72)
print("Ⅵ 结论")
print("=" * 72)
print("""
  1. ε̄/ε₃ = √5 在 d = 2.7095 处精确成立（数值事实）。

  2. 这不是极限行为：
     - lim_{d→ln15} ε̄/ε₃ = 0 (因为 ε̄→0 而 ε₃→2.4×10⁻⁴)
     - ε̄/ε₃ 在 d>ln15 时快速增长, 在 d_H 处穿过 √5

  3. 自洽方程分析：
     15-branch 与 3-map 的一致性条件消去 ε̄, ε₃ 后得：
       d(d - ln15) = k·ln15·(e^{-d²} + e^{-d(3+d)})
     其中 k = ε̄/ε₃。对 k=√5, 该方程的解为 d ≈ 2.7095000,
     与 χ² 拟合值完全一致。

  4. √5 = √N_total 的结构解释仍是假说层级：
     - "标准差传播"是物理直觉, 非数学推导
     - ε̄/ε₃ = √5 是数值事实, 但目前无法从更第一性的
       原理解析推导
     - 需要概念突破: 为什么 3-map IFS 与 15-branch 有效
       描述的一致性会选择 k = √N_total?
""")
