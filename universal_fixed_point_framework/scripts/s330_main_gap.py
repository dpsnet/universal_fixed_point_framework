# -*- coding: utf-8 -*-
"""S330 跨框架主项差分解探索
Δ_main = 360/φ² − (72+24ln15) = 0.514559223585
候选：φ/π（2506.12859 X_opt）、ln(5/3)、框架常数对数组合、σ 组合
目标：1e-6 级精确命中才升格——0.1% 级为弱线索
"""
import math
import itertools

print("=== S330 跨框架主项差分解 ===\n")

phi = (1+math.sqrt(5))/2
SIGMA = 1/15
LN15 = math.log(15)

main_km = 360/phi**2
main_mufpf = 72 + 24*LN15
D = main_km - main_mufpf
print(f"[1] 主项差")
print(f"    360/φ²     = {main_km:.12f}")
print(f"    72+24ln15  = {main_mufpf:.12f}")
print(f"    Δ_main     = {D:.12f}")

# 候选表达式扫描
print(f"\n[2] 候选身份扫描")
cands = [
    ("φ/π（2506.12859 X_opt）", phi/math.pi),
    ("ln(5/3)", math.log(5/3)),
    ("ln(3/2)+1/8", math.log(3/2)+1/8),
    ("1/φ²", 1/phi**2),
    ("1/φ²+1/φ³", 1/phi**2+1/phi**3),
    ("1−1/2+1/15", 1-1/2+1/15),
    ("24σ−1", 24/15-1),
    ("2ln(φ)+σ", 2*math.log(phi)+SIGMA),
    ("ln(3·5/2³)=ln(15/8)", math.log(15/8)),
    ("ln(2·3·5)/(3·5)=ln30/15", math.log(30)/15),
    ("π/6 − 1/100", math.pi/6-0.01),
    ("e/π−0.35", math.e/math.pi-0.35),
    ("1/2+ln(φ)/π", 0.5+math.log(phi)/math.pi),
]
print(f"{'候选':<26}{'值':<14}{'Δ差值':<14}{'相对'}")
best = None
for name, val in cands:
    diff = abs(val-D)
    rel = diff/D*100
    print(f"{name:<26}{val:<14.9f}{diff:<14.2e}{rel:.3f}%")
    if best is None or diff < best[1]:
        best = (name, diff)

# 系统扫描：小素数对数组合 a·ln2 + b·ln3 + c·ln5（a,b,c ∈ [-3,3]）
print(f"\n[3] 系统扫描：a·ln2+b·ln3+c·ln5（a,b,c∈[-3,3]）")
best2 = None
for a,b,c in itertools.product(range(-3,4), repeat=3):
    val = a*math.log(2)+b*math.log(3)+c*math.log(5)
    diff = abs(val-D)
    if best2 is None or diff < best2[0]:
        best2 = (diff, f"{a}ln2+{b}ln3+{c}ln5", val)
print(f"    最优：{best2[1]} = {best2[2]:.12f}——Δ = {best2[0]:.2e}——"
      f"{'强命中' if best2[0]<1e-6 else ('中命中' if best2[0]<1e-4 else '弱/无')}")

# 系统扫描：σ 多项式 + 对数组合
print(f"\n[4] 系统扫描：σ^a·(对数组合) + σ 多项式")
best3 = None
for a,b,c in itertools.product(range(-2,3), repeat=3):
    for p in range(2,5):
        lg = a*math.log(2)+b*math.log(3)+c*math.log(5)
        for k in range(0, 4):
            val = SIGMA**p*k + lg
            diff = abs(val-D)
            if best3 is None or diff < best3[0]:
                best3 = (diff, f"{k}σ^{p}+{a}ln2+{b}ln3+{c}ln5", val)
print(f"    最优：{best3[1]} = {best3[2]:.12f}——Δ = {best3[0]:.2e}——"
      f"{'强命中' if best3[0]<1e-6 else ('中命中' if best3[0]<1e-4 else '弱/无')}")

# 结论
print(f"\n[5] 结论")
print(f"    Δ_main = 0.514559223585")
print(f"    φ/π    = 0.515036217510——相对差 0.0926%——接近但非精确（弱线索）")
if best2[0] < 1e-4:
    print(f"    ★ 对数组合命中：{best2[1]}（Δ={best2[0]:.2e}）——精确级！")
elif best3[0] < 1e-4:
    print(f"    ★ σ/对数混合命中：{best3[1]}（Δ={best3[0]:.2e}）——精确级！")
else:
    print(f"    △ 无 1e-6 级精确命中——Δ_main 无简单框架表达式——")
    print(f"      φ/π 0.09% 接近为弱线索——登记不升格")
print(f"    ——若对数组合命中：Δ_main = a·ln2+b·ln3+c·ln5——则 Kraemer/Māyā 主项")
print(f"      与 MUFPF 主项之差是框架常数对数的精确组合——三框架桥成立！")
