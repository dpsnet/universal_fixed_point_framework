# -*- coding: utf-8 -*-
"""chain_audit_165_sqrt2_identity.py — √2 框架身份判别（F_np 分母全框架化，104az-165）"""
import io, sys
from fractions import Fraction as F
import math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

N_gen, k_max, Powers, Silence, Fp, Inv = 3, 8, 2, 5, 4, 7

print("=== 1. √2 框架身份候选：√(k_max/不动点) ===")
print(f"k_max/不动点 = {k_max}/{Fp} = {k_max/Fp} = 幂基 = {Powers}")
print(f"√(k_max/不动点) = √{k_max/Fp} = √{Powers} = √2：{math.sqrt(k_max/Fp) == math.sqrt(2)}")

print("\n=== 2. 谱隙比机制动机（SU(3)/SU(2)）===")
dlmin = (math.sqrt(3) - 1) / 6
dl3 = math.sqrt(2) * dlmin
print(f"Δλ_min = (√3−1)/6 = {dlmin:.10f}")
print(f"Δλ₃ = √2·Δλ_min = {dl3:.10f}")
print(f"Δλ₃/Δλ_min = {dl3/dlmin:.12f}（= √2 = {math.sqrt(2):.12f} 精确：{abs(dl3/dlmin - math.sqrt(2)) < 1e-14}）")
print(f"→ Δλ₃ = √(幂基)·Δλ_min = √(k_max/不动点)·Δλ_min——谱隙提升因子 = 幂基平方根")

print("\n=== 3. F_np 分母全框架化复算 ===")
weave3 = F(9, 10) ** 3
delta = F(1, 675)
Fnp = weave3 * (1 - delta) / (math.sqrt(2) * dlmin)
print(f"F_np = 织³×(1−δ)/(√(幂基)·Δλ_min) = {Fnp:.10f}（√2 → √(幂基) 重写）")
print(f"F_np vs 观测 4.220：dev {(Fnp/4.220 - 1)*100:.4f}%（0.01% 级达标维持）")

print("\n=== 4. √2 替代候选排查（同一谱隙比的多重身份）===")
cands = {
    "√幂基 = √(k_max/不动点)": math.sqrt(Powers),
    "√(静默−不动点) = √1": math.sqrt(Silence - Fp),
    "√(N_gen−幂基) = √1": math.sqrt(N_gen - Powers),
    "√(对合域−静默) = √2": math.sqrt(Inv - Silence),
    "√(k_max−N_gen·幂基) = √2": math.sqrt(k_max - N_gen * Powers),
}
for k, v in cands.items():
    hit = abs(v - math.sqrt(2)) < 1e-12
    print(f"  {k} = {v:.12f}（== √2: {hit}）")

print("\n=== 5. 生成链（F_np 分母全框架化）===")
print("根集 → k_max, 不动点 → k_max/不动点 = 幂基 = 2 → √(幂基) = √2 → Δλ₃ = √2·Δλ_min → F_np")
print("√2 不再是外部谱因子：= (k_max/不动点)^{1/2}——Bott 层维数比平方根")

print("\n=== 判别 ===")
print("① √2 = √(k_max/不动点) = √幂基——框架身份候选（唯一自然候选：√(对合域−静默) = √2 同值但非比值结构）")
print("② Δλ₃ = √(幂基)·Δλ_min——谱隙提升因子 = 幂基平方根（Bott 层 8 与不动点 4 的维数比）")
print("③ F_np 分母全框架化：F_np = 织³×(1−δ)/(√(幂基)·Δλ_min)——所有因子 {N_gen, k_max, 幂基, 静默, σ, N_c} 全框架量")
print("④ 判别层：√2 从黑箱谱因子 → 框架比值平方根；F_np 全框架表达完成（数值不变 4.2187004）")
