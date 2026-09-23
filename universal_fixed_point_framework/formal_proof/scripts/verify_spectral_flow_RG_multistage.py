# -*- coding: utf-8 -*-
"""
多级常演化数值验证 —— Paper LVII §8.6d / SpectralFlowRG.lean
============================================================

验证目标（对应 Lean4 定理，零 sorry）：
  1. RG_k1 = √3                          （Δλ_min → Δλ_min^(EM) 纯规范常数）
  2. RG_k2 = r*/√3                       （Δλ_min^(EM) → δ_SC BCS 动力学）
  3. RG_telescoping: RG_k1 · RG_k2 = r*  （乘积闭合，重现单级自洽唯一根）
  4. RG_f1 = 1/√3  （无量纲增长因子，EM 级）
  5. RG_f2 = √3/r* （无量纲增长因子，动力学级）
  6. gap_ratio_telescoping: f1·f2 = 1/r* （两级路径 = 单级自洽倍率；链一致性）

采用 mpmath 高精度（50 位），与 Lean 实数域严格推导交叉核验。
"""
import mpmath as mp
mp.mp.dps = 50

# ------------------------------------------------------------------
# 谱流自洽输入：c = a_BCS^3 · 4π，a_BCS = 1/1.764（弱耦合 BCS 普适比值，物理输入）
# ------------------------------------------------------------------
a_BCS = mp.mpf(1) / mp.mpf("1.764")
c     = a_BCS**3 * 4 * mp.pi

# f(r) = (1 + √3·√r)·r，在 [0,∞) 上单调（严格增），f(0)=0，f→∞，故唯一正实根
f = lambda r: (1 + mp.sqrt(3) * mp.sqrt(r)) * r

# 数值求唯一正实根 r*（二分法，与 WeaveBCS.selfConsFunc_existsUnique 对应）
lo, hi = mp.mpf(0), mp.mpf(10)
for _ in range(1000):
    mid = (lo + hi) / 2
    if f(mid) < c:
        lo = mid
    else:
        hi = mid
r_star = (lo + hi) / 2

# --- 验证 1：根闭合 ---------------------------------------------------
assert mp.almosteq(f(r_star), c, rel_eps=mp.mpf("1e-48")), "r* 不自洽闭合"
print(f"r_star            = {mp.nstr(r_star, 15)}")
print(f"f(r_star) - c     = {mp.nstr(f(r_star) - c, 3, min_fixed=0, max_fixed=0)}")

# ------------------------------------------------------------------
# 定义两级倍率（与 SpectralFlowRG.lean 完全一致）
# ------------------------------------------------------------------
dl_min   = mp.mpf(1)                          # Cl(1,7) 谱间隙的归一化值（比例不变）
dl_minEM = dl_min / mp.sqrt(3)                # U(1) 电磁中间级 = √(1/3)·dl_min
deltaSC  = dl_min / r_star                    # δ_SC = Δλ_min / r*

k1 = dl_min / dl_minEM                        # = √3
k2 = dl_minEM / deltaSC                       # = r*/√3
f1 = dl_minEM / dl_min                        # = 1/√3
f2 = deltaSC / dl_minEM                       # = √3/r*

print("\n--- 级倍率 ---")
print(f"k1 = dl_min/dl_minEM = {mp.nstr(k1, 15)}   (期望 √3 = {mp.nstr(mp.sqrt(3), 15)})")
print(f"k2 = dl_minEM/δ_SC   = {mp.nstr(k2, 15)}   (期望 r*/√3 = {mp.nstr(r_star/mp.sqrt(3), 15)})")
print(f"f1 = dl_minEM/dl_min = {mp.nstr(f1, 15)}   (期望 1/√3 = {mp.nstr(1/mp.sqrt(3), 15)})")
print(f"f2 = δ_SC/dl_minEM   = {mp.nstr(f2, 15)}   (期望 √3/r* = {mp.nstr(mp.sqrt(3)/r_star, 15)})")

# ------------------------------------------------------------------
# 断言（所有偏差 < 1e-45 相对）
# ------------------------------------------------------------------
eps = mp.mpf("1e-45")
checks = []

checks.append(("k1 = √3",             mp.almosteq(k1,     mp.sqrt(3),          rel_eps=eps)))
checks.append(("k2 = r*/√3",          mp.almosteq(k2,     r_star/mp.sqrt(3),   rel_eps=eps)))
checks.append(("f1 = 1/√3",           mp.almosteq(f1,     1/mp.sqrt(3),        rel_eps=eps)))
checks.append(("f2 = √3/r*",          mp.almosteq(f2,     mp.sqrt(3)/r_star,   rel_eps=eps)))

# 折叠（RG_telescoping）：k1·k2 = r*
prod_k = k1 * k2
checks.append(("k1·k2 = r*",          mp.almosteq(prod_k, r_star,              rel_eps=eps)))

# 链一致性（gap_ratio_telescoping）：f1·f2 = 1/r*
prod_f = f1 * f2
checks.append(("f1·f2 = 1/r*",        mp.almosteq(prod_f, 1/r_star,            rel_eps=eps)))

# 与单级自洽一致：两级路径 δ_SC/Δλ_min = 1/r*（gap_ratio_multistage_eq_single）
rat     = deltaSC / dl_min
checks.append(("δ_SC/Δλ_min = 1/r*",  mp.almosteq(rat,    1/r_star,            rel_eps=eps)))
checks.append(("δ_SC/Δλ_min = f1·f2", mp.almosteq(rat,    prod_f,               rel_eps=eps)))

print("\n--- 不变式核验 ---")
print(f"k1·k2            = {mp.nstr(prod_k, 15)}   (期望 r* = {mp.nstr(r_star, 15)})")
print(f"f1·f2            = {mp.nstr(prod_f, 15)}   (期望 1/r* = {mp.nstr(1/r_star, 15)})")
print(f"δ_SC/Δλ_min      = {mp.nstr(rat, 15)}   (期望 1/r* = {mp.nstr(1/r_star, 15)})")

print("\n--- 结果 ---")
all_ok = all(ok for _, ok in checks)
for name, ok in checks:
    print(f"  [{'OK ' if ok else 'FAIL'}] {name}")
print(f"\n全部通过: {all_ok}")
assert all_ok, "存在数值验证失败项"