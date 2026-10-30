# -*- coding: utf-8 -*-
"""chain_audit_191_active_silent_vieta.py — 活跃/静默韦达结构 + Mersenne k_max 和分解唯一性
① 活跃3+静默5 = k_max=8（104az-84 已立）、活跃3×静默5 = σ⁻¹=15 → x²−k_max·x+σ⁻¹ = 0 两根
② M_n = ab（a+b = k_max）分解唯一性：判别式 D(n) = k_max²−4M_n = 68−2^{n+2} 完全平方 ⟺ n∈{3,4}
③ 奇数塔 {1,3,5,7}：Σ = 16 = 幂基^不动点；配对和 = 8、配对积 = M_3/M_4；全积 105 = Λ_QCD/2
④ σ 新通道：σ⁻¹ = (k_max²−幂基²)/不动点 = 60/4 = 15
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import mpmath as mp
mp.mp.dps = 40

Ng, km, B, S, F, I, sig_inv = 3, 8, 2, 5, 4, 7, 15
print("=== 活跃/静默韦达结构判别（104az-191 候选）===\n")

print("① 韦达方程 x² − k_max·x + σ⁻¹ = 0")
print(f"   和：活跃+静默 = 3+5 = {3+5} = k_max ✓；积：活跃×静默 = 3×5 = {3*5} = σ⁻¹ ✓")
disc = km*km - 4*sig_inv
print(f"   判别式 D = k_max²−4σ⁻¹ = {km}²−4×{sig_inv} = {disc} = 幂基² = {B}² ✓（完全平方 → 整数根）")
print(f"   根 = (k_max±幂基)/2 = ({km}±{B})/2 = {[(km+B)//2, (km-B)//2]} = {{静默, 活跃}} ✓\n")

print("② Mersenne k_max 和分解唯一性：M_n = ab 且 a+b = k_max = 8")
print(f"   D(n) = k_max²−4M_n = 68−2^(n+2)")
for n in range(1, 9):
    Mn = 2**n - 1
    D = 68 - 2**(n+2)
    sq = int(D**0.5)**2 == D if D >= 0 else False
    tag = "✓ 完全平方" if sq and D >= 0 else ("负 ✗" if D < 0 else "✗")
    if sq and D >= 0:
        s = int(D**0.5)
        a, b = (km+s)//2, (km-s)//2
        print(f"   n={n}: M_n={Mn}，D = {D} = {s}² {tag} → 分解 {{a,b}} = {{{a},{b}}}（和 {a+b} = k_max ✓，积 {a*b} = M_n ✓）")
    else:
        print(f"   n={n}: M_n={Mn}，D = {D} {tag}")
print(f"   → n∈{{3,4}} 唯一（n=3: {{7,1}} = {{对合域,单位元}}；n=4: {{5,3}} = {{静默,活跃}}）")
print(f"   D(3) = 36 = (幂基×N_gen)² = (2×3)²；D(4) = 4 = 幂基² ——判别式自身框架化\n")

print("③ 奇数塔 {1,3,5,7}（公差 2 = 幂基；= k_max−奇数坐标系 104az-84 格点）")
odd = [1, 3, 5, 7]
print(f"   Σ = 1+3+5+7 = {sum(odd)} = 幂基^不动点 = 2⁴ = 16 = Cℓ(3,1) 全态数 ✓")
print(f"   (7,1) 和 = 8 = k_max（Cℓ(3,0) 全态数）；(5,3) 和 = 8 = k_max ✓")
print(f"   (7,1) 积 = 7 = M_3 = 对合域；(5,3) 积 = 15 = M_4 = σ⁻¹ ✓")
prod = 1
for x in odd: prod *= x
print(f"   全积 = 1×3×5×7 = {prod} = N_gen×静默×对合域 = 3×5×7")
print(f"   = 禁闭域×静默/幂基 = 42×5/2 = {42*5//2} ✓；Λ_QCD~210 = 2×105 = 禁闭域×静默（104az-155 已立）")
print(f"   → 奇数塔全积 = Λ_QCD/2——奇数塔连接主线 B\n")

print("④ σ 新通道：σ⁻¹ = (k_max²−幂基²)/不动点")
print(f"   (64−4)/4 = { (km*km - B*B)//F } = σ⁻¹ ✓；60 = k_max²−幂基²（104az-86 60 三重身份成员）")
print(f"   → σ⁻¹ 第七通道：平方差/不动点（与六通道 104az-187 并列）\n")

print("⑤ 观察级：迭代 x_{n+1} = k_max − σ⁻¹/x_n 的不动点结构")
for x0 in [2, 4]:
    x = mp.mpf(x0)
    seq = []
    for _ in range(12):
        x = mp.mpf(km) - mp.mpf(sig_inv)/x
        seq.append(mp.nstr(x, 6))
    print(f"   x0={x0}: {' → '.join(seq[:8])}... → 收敛 {mp.nstr(x, 6)}（静默 5 吸引不动点）")
print(f"   静默 5：|f'(5)| = 15/25 = 0.6 < 1 吸引；活跃 3：|f'(3)| = 15/9 = 5/3 > 1 排斥——观察级（静默稳定/活跃不稳定语义）\n")

print("⑥ 诚实边界")
print("   韦达方程 = 已立恒等（和/积）的合并陈述——新意在与 Mersenne 唯一分解 + 奇数塔全积 105")
print("   M_n k_max 和分解唯一性为判别式完全平方条件的代数事实（框架意义在 n=3,4 根恰为框架量）")
print("   全积 105 = Λ_QCD/2 连接为观察级（210 = 5×42 已立，105 = 42×5/2 为其简单推论）")
print("   迭代不动点语义（静默稳定/活跃不稳定）为动力系统候选解读，未独立验证")
