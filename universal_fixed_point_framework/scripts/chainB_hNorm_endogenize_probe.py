"""
chainB_hNorm_endogenize_probe.py — Chain B hNorm 内生化探点 数值记录 v1.10(rev)
RN-ENDO-010 §8.12 配套探点

hNorm: 24·frobNormSq(S.A) ≤ (4·spectralGap 8)²   (DeviationBound.lean L436)
等价: ‖S.A‖ ≤ (4/√24)·spectralGap8 = √(2/3)·spectralGap8

⚠ v1.11 撤回记录: 本脚本曾误称"√(2/3) 的 LACI 结构来源", 依 Paper I 定义 3.11/3.12a 判定为误读:
  · LACI 判据内核 = 谱间隙单调递减函数族(间隙小⟹指数高⟹静默), 与 hNorm 的"范数上界"是不同类型量
  · γ_ref=0.1 是 Kerr 数值标定, 非平行于 hNorm 的独立结构输入; "两路径收敛"实为同用 spectralGap8
    的同源循环
  · 第三项取值的 √(2/3) 是纯代数运算, 不构成 LACI 结构来源 → 已从文档 §8.13 撤回
本脚本现仅保留诚实数值记录(不声称任何 LACI 来源):
  · V2: hNorm 上界 = √(2/3)·spectralGap8 = (√6−√2)/(6√3)
  · V3: (4/√24)² = dim_ℝℍ²/(8·3) = 2/3 候选恒等(恒等≠结构证明, 未闭合)
  · V5: S.A 非简单 A_GR 第2级投影(上界 0.0996 < λ₂ 0.2887)
"""
import math

def spectral_gap8():
    return (math.sqrt(6) - math.sqrt(2)) / math.sqrt(72)

def ag_eigenvalue(k, kmax=8):
    return math.sqrt(k * (k + 1)) / math.sqrt(kmax * (kmax + 1))

sg = spectral_gap8()
sq23 = math.sqrt(2 / 3)
hNorm_bound = sq23 * sg          # hNorm 归一化上界

print("=" * 72)
print("Chain B hNorm 内生化探点 (数值记录, v1.10 主线)")
print("=" * 72)

print(f"\n[核心] spectralGap8 = (√6−√2)/√72 = {sg:.8f}")
print(f"[核心] hNorm ‖S.A‖ 上界 = √(2/3)·spectralGap8 = {hNorm_bound:.8f}")

# ---- V1/V2: 既有确认 ----
assert abs(sg - (math.sqrt(6) - math.sqrt(2)) / math.sqrt(72)) < 1e-12
alt_bound = (math.sqrt(6) - math.sqrt(2)) / (6 * math.sqrt(3))
print(f"\n[V2] √(2/3)·spectralGap8 = {hNorm_bound:.8f} vs (√6−√2)/(6√3) = {alt_bound:.8f}")
assert abs(hNorm_bound - alt_bound) < 1e-12

# ---- V3: v1.10 dim_ℝℍ 恒等 (保留) ----
dim_H, base8, terms3 = 4.0, 8.0, 3.0
print(f"\n[V3](v1.10) (dim_ℝℍ)²/(底8·项3) = 16/24 = {dim_H**2/(base8*terms3):.8f} = (4/√24)² [恒等保留]")

# ---- 背景注记: Δλ_min 与 spectralGap8 同一性 (诚实事实, 无内生化主张) ----
print("\n" + "=" * 72)
print("[背景] Δλ_min(Paper VI 红外正则化) ≈ spectralGap8 = {:.6f}".format(sg))
print("  此为框架内共享的谱间隙标度(原始事实), 不构成对 hNorm 任何内生化来源的主张")
print("=" * 72)

# ---- V5: ‖S.A‖ 候选对标 (保留, 显示 S.A 非简单投影) ----
print("\n" + "=" * 72)
print("[V5] ‖S.A‖ 上界候选对标 (确认非简单 A_GR 投影)")
print("=" * 72)
lams = [ag_eigenvalue(k) for k in range(1, 9)]
print(f"     hNorm 上界 = {hNorm_bound:.6f};  λ₁ = {lams[0]:.6f}, λ₂ = {lams[1]:.6f}")
print(f"     λ₂ > 上界, 故 S.A 非 A_GR 谱第2级投影; √(2/3) 待结构源(未闭合)")

# ---- 撤回注记: v1.11 LACI 误读 ----
print("\n" + "=" * 72)
print("[撤回注记] v1.11 对 LACI 的连接经 Paper I 定义 3.11/3.12a 复核为误读:")
print("  · LACI 判据内核 = 谱间隙单调递减函数族(高⟹静默), 与 hNorm 范数上界为不同类型量")
print("  · '两路径收敛'实为同用 spectralGap8 的同源循环, 非独立验证")
print(f"  · 第三项取值 √(2/3) 为纯代数运算({sq23:.9f}), 不构成结构来源 → 已从文档撤回")
print("=" * 72)

print("\n" + "=" * 72)
print("结论(v1.10 主线, 未闭合):")
print("  1. hNorm 三常数可解剖: 24=8×3 为证明技术(Lean 定理), 非独立 stipulation")
print("  2. 4 (等效 √(2/3)): 候选恒等 (dim_ℝℍ)²/(8·3)=16/24=2/3, 但恒等≠结构证明")
print("  3. √(2/3) 仍为 Chain B 唯一未闭合实质输入, 无框架结构来源(含 LACI 撤回)")
print("=" * 72)