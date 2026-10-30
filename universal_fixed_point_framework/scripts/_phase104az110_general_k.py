# -*- coding: utf-8 -*-
OUT = open(r'C:\Users\dps_n\AppData\Local\DoubaoWork\User Data\Profile 6\.doubaowork\agent_mode\workspace\out_110.txt', 'w', encoding='utf-8')
def P(*a):
    OUT.write(' '.join(map(str, a)) + '\n')

"""
Phase 104az-110: 对合折叠对称积的 k_max 推广域判别
231 = (a−b)·a·(a+b), a = k_max−1, b = k_max/2
判别: a−b = N_gen 是否唯一锁定 k_max = 8（Clifford(3,1) 必然性传递到 κΛ）
"""
Ngen = 3

P("=" * 70)
P("[1] 一般 k_max 下的对称积（k 偶数）")
P("  S(k) = (k/2−1)·(k−1)·(3k/2−1)")
vals = {}
for k in [2, 4, 6, 8, 10, 12, 16, 32, 64]:
    S = (k//2 - 1) * (k - 1) * (3*k//2 - 1)
    vals[k] = S
    tag = ""
    if k == 8:
        tag = "  ← 231 锁定（k_max = 8）"
    P(f"  k={k:3d}: S = {S}{tag}")

P("\n[2] k_max = 8 唯一性判别（框架身份锁定）")
P(f"  身份 A: a−b = N_gen → k_max/2−1 = {Ngen} → k_max = 2({Ngen}+1) = {2*(Ngen+1)}")
P(f"    ★ 唯一解 k_max = 8——与 P7-5e-263/264 代数唯一性一致")
P(f"  身份 B: a+b = N_active+k_max → 3k_max/2−1 = k_max+3 → k_max = {2*4}")
P(f"    ★ 同样唯一解 k_max = 8（双身份同锁）")
P(f"  身份 C: b = k_max/2 为对合不动点——所有偶数 k_max 平凡成立")
P(f"  → 231 对称积作为框架身份: 三因子 (N_gen, k_max−1, N_active+k_max)")
P(f"    全部唯一要求 k_max = 8——对称积是 k_max=8 特化身份")

P("\n[3] 2 幂列（Bott 塔）对称积身份候选")
for k in [2, 4, 8, 16, 32, 64]:
    S = vals[k]
    fac = []
    n = S
    d = 2
    while n > 1:
        if n % d == 0:
            c = 0
            while n % d == 0:
                n //= d
                c += 1
            fac.append(f"{d}^{c}" if c > 1 else str(d))
        d += 1
    P(f"  k={k:3d}: S = {S} = {'·'.join(fac)}")

P("\n[4] κΛ 一般形式与闭合")
P("  κΛ(k) = 2k·静默²·(1 + 1/S(k))——静默 = k−3（框架关系）")
kmax = 8
sil = kmax - 3
for k in [4, 6, 8, 10, 16]:
    s = k - 3
    S = vals[k]
    kl = 2 * k * s * s * (1 + 1/S)
    P(f"  k={k:3d}: 静默={s}, S={S}, κΛ(k) = {kl:.6f}")

P("\n[5] 判别结论")
P("  ★★ 对合折叠对称积推广域判别:")
P("    (1) S(k) = (k/2−1)(k−1)(3k/2−1) 在 k_max=8 锁定 231——唯一性由")
P("        a−b = N_gen（k_max = 2(N_gen+1)）与 a+b = N_active+k_max 双身份锁定")
P("    (2) k_max=8 必然性（Clifford(3,1) 代数唯一性）直接传递到 κΛ 修正分母:")
P("        修正分母 231 是 k_max=8 特化——不是搜索偶然（结构身份链）")
P("    (3) 2 幂列 S(4)=15=2⁴−1 Mersenne——对称积在 Bott 塔低层退化/特殊化")
P("    (4) κΛ 候选机制动机闭合: 对合折叠对称积 = k_max 特化结构,")
P("        与 P7-5e-184 发夹折叠推广域检验同源——待独立预言判别")
P("  诚实边界: 判别为结构身份链（非观测判别）；κΛ 数值仍受 d_H 精度限制;")
P("            对称积的一般 k_max 行为是反事实检验（框架 k_max=8 已锁定）")
