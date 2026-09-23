# -*- coding: utf-8 -*-
"""
多带谱间隙谱系数值验证 —— Paper LVII §8.6e / MultibandSpectralBridge.lean
==========================================================================

验证目标（对应 Lean4 定理，零 sorry）：
  1. 三分支多带谱间隙 δ_SC^(i) = Δλ_i / r*（共享唯一自洽根，非自由参数）
  2. 多带隙比保持 SU(2) Casimir 量化：δ_SC^(1):δ_SC^(2):δ_SC^(3)
     = Δλ₁:Δλ₂:Δλ₃ = √(1/3):1:√2         （band_ratio_*）
  3. Casimir 升序三级塔：Δλ₂/Δλ₁ = √3、Δλ₃/Δλ₂ = √2、Δλ₃/Δλ₁ = √6
     （casimir_tower_*，且 k₁₂·k₂₃ = √6 乘积闭合）
  4. 带2 即单级定量桥 δ_SC = Δλ_min/r*   （band2_eq_categorical / ∎§8.6b）
  5. 带1/带3 相对单级：√(1/3)·δ_SC 与 √2·δ_SC

采用 mpmath 高精度（50 位）。Δλ_min 取归一化 1（比例不变）。
"""
import mpmath as mp
mp.mp.dps = 50

a_BCS = mp.mpf(1) / mp.mpf("1.764")
c     = a_BCS**3 * 4 * mp.pi
f     = lambda r: (1 + mp.sqrt(3) * mp.sqrt(r)) * r

lo, hi = mp.mpf(0), mp.mpf(10)
for _ in range(1000):
    mid = (lo + hi) / 2
    if f(mid) < c:
        lo = mid
    else:
        hi = mid
r_star = (lo + hi) / 2
assert mp.almosteq(f(r_star), c, rel_eps=mp.mpf("1e-48"))

# 三个 Casimir 分量（比例不变）
dl1 = mp.mpf(1) / mp.sqrt(3)   # Δλ₁ = √(1/3)·Δλ_min
dl2 = mp.mpf(1)                # Δλ₂ = Δλ_min
dl3 = mp.sqrt(2)               # Δλ₃ = √2·Δλ_min

# 三分支多带谱间隙
b1 = dl1 / r_star              # δ_SC^(1)
b2 = dl2 / r_star              # δ_SC^(2)
b3 = dl3 / r_star              # δ_SC^(3)

eps = mp.mpf("1e-45")
checks = []

# --- 多带隙比保持（SU(2) Casimir 量化） ---
checks.append(("δ^(1)/δ^(2) = Δλ₁/Δλ₂ = 1/√3", mp.almosteq(b1/b2, dl1/dl2, rel_eps=eps)))
checks.append(("δ^(3)/δ^(2) = Δλ₃/Δλ₂ = √2",   mp.almosteq(b3/b2, dl3/dl2, rel_eps=eps)))
checks.append(("δ^(3)/δ^(1) = √6",             mp.almosteq(b3/b1, mp.sqrt(6), rel_eps=eps)))

# --- Casimir 升序三级塔 ---
checks.append(("Δλ₂/Δλ₁ = √3 (= RG_k1)",       mp.almosteq(dl2/dl1, mp.sqrt(3), rel_eps=eps)))
checks.append(("Δλ₃/Δλ₂ = √2",                 mp.almosteq(dl3/dl2, mp.sqrt(2), rel_eps=eps)))
checks.append(("Δλ₃/Δλ₁ = √6",                 mp.almosteq(dl3/dl1, mp.sqrt(6), rel_eps=eps)))
checks.append(("k₁₂·k₂₃ = √6 (塔乘积闭合)",    mp.almosteq((dl2/dl1)*(dl3/dl2), mp.sqrt(6), rel_eps=eps)))

# --- 分支相对单级 δ_SC (带2 / §8.6b) ---
checks.append(("δ^(1) = √(1/3)·δ_SC",          mp.almosteq(b1, (mp.mpf(1)/mp.sqrt(3))*b2, rel_eps=eps)))
checks.append(("δ^(3) = √2·δ_SC",               mp.almosteq(b3, mp.sqrt(2)*b2, rel_eps=eps)))

print(f"r_star      = {mp.nstr(r_star, 15)}")
print(f"Δλ₁:Δλ₂:Δλ₃ = {mp.nstr(dl1,6)} : {mp.nstr(dl2,6)} : {mp.nstr(dl3,6)}")
print(f"δ^(1):δ^(2):δ^(3) = {mp.nstr(b1,6)} : {mp.nstr(b2,6)} : {mp.nstr(b3,6)}  (∝ √(1/3):1:√2)")
print(f"δ^(1)/δ^(2) = {mp.nstr(b1/b2, 15)}   (期望 1/√3 = {mp.nstr(1/mp.sqrt(3),15)})")
print(f"δ^(3)/δ^(2) = {mp.nstr(b3/b2, 15)}   (期望 √2 = {mp.nstr(mp.sqrt(2),15)})")
print(f"δ^(3)/δ^(1) = {mp.nstr(b3/b1, 15)}   (期望 √6 = {mp.nstr(mp.sqrt(6),15)})")

print("\n--- 结果 ---")
all_ok = all(ok for _, ok in checks)
for name, ok in checks:
    print(f"  [{'OK ' if ok else 'FAIL'}] {name}")
print(f"\n全部通过: {all_ok}")
assert all_ok, "存在数值验证失败项"