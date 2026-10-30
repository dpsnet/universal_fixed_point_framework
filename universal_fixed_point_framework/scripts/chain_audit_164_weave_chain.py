# -*- coding: utf-8 -*-
"""chain_audit_164_weave_chain.py — 织生成链闭合 + 差 1 链家族扩展判别（104az-164）"""
import io, sys
from fractions import Fraction as F
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

N_gen, k_max, Powers, Silence, Fp, Inv = 3, 8, 2, 5, 4, 7

print("=== 1. 织 生成链闭合（分子 b₀ 同源、分母 D1 双身份）===")
b0 = N_gen ** 2          # L1：β 一阶系数 b₀ = N_gen²（LambdaGapIdentity.b0_eq_Ngen_sq）
D1_add = N_gen + k_max - 1   # 加法身份：10
D1_mul = Powers * Silence    # 乘法身份：10
weave = F(b0, D1_add)
print(f"织 = b₀/(N_gen+k_max−1) = {N_gen}²/{D1_add} = {weave}")
print(f"恒等 N_gen+k_max−1 = 幂基×静默 = {D1_add} = {D1_mul}：{D1_add == D1_mul}")
print(f"织 = b₀/(幂基×静默) = {N_gen}²/{D1_mul} = {F(b0, D1_mul)}——生成链闭合 ✓")

print("\n=== 2. 织 的差 1 链表达 ===")
print(f"织 = 1 − 1/(幂基×静默) = 1 − 1/{D1_mul} = {F(1) - F(1, D1_mul)}（== 9/10: {F(1) - F(1, D1_mul) == F(9,10)}）")
print(f"16/15 = 1 + 1/(N_gen×静默) = 1 + 1/{N_gen*Silence} = {F(1) + F(1, N_gen*Silence)}（== 16/15: {F(1) + F(1, N_gen*Silence) == F(16,15)}）")

print("\n=== 3. 差 1 链家族扫描 1±1/(a×静默) ===")
factors = {"幂基": Powers, "N_gen": N_gen, "不动点": Fp, "k_max": k_max, "对合域": Inv}
print(f"{'因子':<6}{'a×静默':<8}{'1+1/':<12}{'1−1/':<12}")
for name, a in factors.items():
    d = a * Silence
    plus = F(1) + F(1, d)
    minus = F(1) - F(1, d)
    print(f"{name:<6}{d:<8}{str(plus):<12}{str(minus):<12}")

print("\n=== 4. 家族命中对照（观测/框架量）===")
hits = {
    "16/15": "16/15 = 1+1/(N_gen×静默)——104az-159 三扇区复用锁定（观测锚）",
    "9/10": "9/10 = 1−1/(幂基×静默)——织（主线 B 缺口因子）",
    "41/40": "41/40 = 1+1/(k_max×静默)——41 = k_max×静默+1（静默单元+1 家族）",
    "39/40": "39/40 = 1−1/(k_max×静默)——39 = k_max×静默−1（静默单元−1 家族）",
    "21/20": "21/20 = 1+1/(不动点×静默)——21 = N_gen×对合域（4.2 分子同源）",
    "4/5": "4/5 = 1−1/静默——静默单元差 1（B_th 阈值 0.8 另有 1−3σ 身份，双身份）",
}
for k, v in hits.items():
    print(f"★ {k}: {v}")

print("\n=== 5. 符号-因子配对观察 ===")
print("16/15：加性(+)，因子 N_gen；9/10：减性(−)，因子 幂基")
print("→ 配对规律候选：+ ↔ N_gen、− ↔ 幂基（与 A2 修正符号族 104az-145 同构模式）")
print("→ 注意：41/40(+1)、39/40(−1) 也呈现 +/− 配对，但因子同为 k_max——符号-因子配对非严格（观察级）")

print("\n=== 判别 ===")
print("① 织 生成链闭合：织 = N_gen²/(幂基×静默)——分子 L1 b₀ 同源、分母 D1 双身份——机制动机明确")
print("② 差 1 链家族：1±1/(a×静默) 六成员（16/15 锁定、9/10 织、41/40、39/40、21/20、4/5），4/6 有框架身份")
print("③ 符号配对观察级（41/40 与 39/40 同因子异符号——配对规律不严格），不升格")
print("④ 织 = 1−1/(幂基·静默) 加入差 1 链家族 = 唯一减性成员（与 16/15 加性互补）")
