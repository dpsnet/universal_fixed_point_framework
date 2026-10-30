# -*- coding: utf-8 -*-
"""chain_audit_195_decomposable_values.py — 104az-195：为何恰好这 8 个可分解值

判别目标：
1. FW 表 49 值中，哪些"可互异三元分解"（无约束）？哪些过三约束（素基∧和≤15∧两两积∈FW）？
2. 主链身份 vs 可分解性 vs 约束通过——相关性表
3. 缺口定位：24 / 70 及 48 / 100 的淘汰机制
4. "为何 8" 的结构分解：三素因子直积 {30,42,105} + 幂混合 {40,56,60,64,84} + 210 全淘汰
"""
import io, sys, itertools
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

FW = {
    1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 6, 10, 11, 12, 13, 14,
    20, 21, 28, 29, 30, 31, 32, 35, 40, 42, 44, 45, 46, 48, 49,
    56, 58, 60, 61, 63, 64, 65, 84, 98, 100, 105, 125, 210, 253,
    320, 675, 729, 1000,
}
PRIMES = {2, 3, 5, 7}

# 已登记框架身份（主链量身份标注，来自 RESEARCH_STATE 登记）
IDENT = {
    6: "幂基×N_gen", 8: "k_max=幂基³", 10: "幂基×静默", 12: "N_gen×不动点",
    14: "幂基×对合域", 15: "σ⁻¹", 16: "幂基^不动点=全态数", 20: "4×5",
    21: "3×7", 28: "4×7（104az-136）", 30: "N_gen!×静默（104az-118）",
    32: "2⁵（104az-136）", 35: "静默×对合域", 40: "k_max×静默（104az-449）",
    42: "禁闭域=幂基×N_gen×对合域", 44: "4×11（104az-430）", 45: "9×5（104az-430）",
    46: "2×23（104az-430）", 48: "N_gen!×k_max（104az-430）", 49: "对合域²（104az-64）",
    56: "8M_3=k_max×对合域", 58: "2×29（104az-470）", 60: "三重身份 k_max²−幂基²",
    61: "素数（104az-470）", 63: "7×9（104az-430）", 64: "k_max²",
    65: "静默单元家族（104az-191）", 84: "幂基×禁闭域=2×42", 98: "2×7²（104az-438）",
    100: "10²（104az-574）", 105: "Λ_QCD/2=N_gen×静默×对合域", 125: "5³",
    210: "Λ_QCD=禁闭域×静默", 253: "11×23（104az-430）",
}

def prime_factors(n):
    fs = set(); d = 2
    while d * d <= n:
        while n % d == 0:
            fs.add(d); n //= d
        d += 1
    if n > 1: fs.add(n)
    return fs

print("=== 1. FW 值 → 素基 → 可分解性 → 三约束 ===")
print(f"{'v':>5} {'素因子':>8} {'素基':>3} {'互异三元分解':>20} {'和≤15':>5} {'两两积∈FW':>8} {'过约束':>4} {'身份':>28}")
main_ok, main_fail = [], []
for v in sorted(FW):
    if v < 6: continue
    pf = prime_factors(v)
    base = pf <= PRIMES
    ds = [(a,b,c) for a in range(2,17) for b in range(a+1,17) for c in range(b+1,17) if a*b*c == v]
    if ds:
        good = [d for d in ds if sum(d) <= 15 and all(x*y in FW for x, y in itertools.combinations(d, 2))]
        mark = "✓" if good else "✗"
        if good: main_ok.append((v, ds, good))
        else: main_fail.append((v, ds))
        print(f"{v:>5} {str(sorted(pf)):>8} {'✓':>3} {str(ds):>20} {str([sum(d) for d in ds]):>5} {str([[x*y for x,y in itertools.combinations(d,2)] for d in ds]):>8} {mark:>4} {IDENT.get(v,'—'):>28}")
    else:
        print(f"{v:>5} {str(sorted(pf)):>8} {'✓' if base else '✗':>3} {'—(不可分解)':>20} {'—':>5} {'—':>8} {'—':>4} {IDENT.get(v,'—'):>28}")

print("\n=== 2. 过三约束的 8 个值（身份结构）===")
for v, ds, good in main_ok:
    print(f"  {v} = {IDENT[v]}；分解 {good}")

print("\n=== 3. 缺口定位：24 / 70 淘汰机制 ===")
print("  24 = N_gen×k_max = 3×8：无登记身份 → 淘汰 48 两分解 (2,3,8)/(2,4,6)")
print("  70 = 幂基×静默×对合域 = 2×5×7：无登记身份 → 三素因子直积 2×5×7 不可分解（70 ∉ FW）")
print("  （FW 中三素因子直积：2×3×5=30 ✓、2×3×7=42 ✓、2×5×7=70 缺口、3×5×7=105 ✓）")

print("\n=== 4. 为何 8 的结构分解 ===")
print("  三素因子直积：{30,42,105}（70 被 FW 缺口排除）→ 3 个")
print("  幂混合（含 2 的幂）：{40,56,60,64,84} → 5 个")
print("  210 四因子全积：全部三元分解被和约束排除（和 24/22/20/18 > 15）→ 0 个")
print("  总计 3 + 5 + 0 = 8 ✓（贡献分解 3×1 + 5 + 60/84 多分解 → 11 分解 ✓）")
