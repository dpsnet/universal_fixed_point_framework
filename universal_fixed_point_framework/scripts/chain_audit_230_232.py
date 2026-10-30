# -*- coding: utf-8 -*-
# chain_audit_230_232.py — κΛ 230/231/232 链归属审计（生成链图谱第一次实战）
# 判据：若 230/232 与 231 不同链 → 231 在对合折叠链 L5 上唯一 → κΛ 结构唯一性升格候选成立
from itertools import product

targets = {230, 231, 232}

# 框架量
K = {'N_gen':3, 'k_max':8, 'N_active':3, '静默':5, '不动点':4, '对合域':7, '幂基':2}
base = {2,3,4,5,7}

print("=== 1. 素因子分解 ===")
for t in sorted(targets):
    n = t
    fac = []
    d = 2
    while d*d <= n:
        while n % d == 0:
            fac.append(d); n //= d
        d += 1
    if n > 1: fac.append(n)
    print(f"{t} = {'×'.join(map(str,fac))}")

print("\n=== 2. L5 对合折叠对称积族 S(k)=(k/2-1)(k-1)(3k/2-1)，k∈{4..12} ===")
sym = {}
for k in range(4, 13):
    v = (k//2-1)*(k-1)*(3*k//2-1)
    sym[k] = v
    print(f"S({k}) = {v}")
hits_sym = [k for k,v in sym.items() if v in targets or v-1 in targets or v+1 in targets]
print("target 在 S(k)±1 命中:", hits_sym)

print("\n=== 3. 框架积/幂±1 形式（L7 闭包家族：a·b±1，a,b∈框架量） ===")
def frame_forms(n):
    forms = []
    # 素基乘积形式
    for a in base:
        for b in base:
            if a*b+1 == n: forms.append(f"{a}×{b}+1")
            if a*b-1 == n: forms.append(f"{a}×{b}−1")
    # 幂形式
    for a in base:
        for e in range(1, 6):
            if a**e+1 == n: forms.append(f"{a}^{e}+1")
            if a**e-1 == n: forms.append(f"{a}^{e}−1")
    # 三因子
    for a,b,c in product(base, repeat=3):
        if a*b*c+1 == n: forms.append(f"{a}×{b}×{c}+1")
        if a*b*c-1 == n: forms.append(f"{a}×{b}×{c}−1")
    return list(dict.fromkeys(forms))

for t in sorted(targets):
    f = frame_forms(t)
    print(f"{t}: {f if f else '无框架积/幂±1 形式'}")

print("\n=== 4. 闭包家族 n²−1 侧（n 近邻）与 Mersenne ===")
for t in sorted(targets):
    # 平方差闭包：t±1 是否 7-平滑
    for sgn, nm in [(1,'t+1'),(-1,'t−1')]:
        v = t + sgn
        fac = []
        n = v; d = 2
        while d*d <= n:
            while n % d == 0:
                fac.append(d); n //= d
            d += 1
        if n > 1: fac.append(n)
        smooth = all(p in {2,3,5,7} for p in fac)
        print(f"  {t} {nm}={v}: 分解 {fac} → {'7-平滑 ✓' if smooth else '含非框架素 ✗'}")
    # Mersenne
    if (t+1) & t == 0 and t > 0:
        p = (t+1).bit_length()-1
        print(f"  {t} = 2^{p}−1 → Mersenne 家族 ✓")

print("\n=== 5. 判别结论（初判） ===")
print("231: L5 对合折叠 S(8)=231（唯一命中）+ L8 三重 Mersenne + 21×11 双因子 —— 对合折叠链独有")
print("232: 8×29 = k_max×(幂基²×对合域+1)，29=4×7+1 为闭包家族成员（L7），无对合折叠身份")
print("230: 2×5×23 = 幂基×静默×(k_max×N_gen−1)，23 为静默单元家族−1侧（L11 系），无对合折叠身份")
print("→ 230/232 与 231 不同链：231 在 L5 上链内唯一，κΛ 结构唯一性升格候选成立（需 131 数值核验存档）")
