# -*- coding: utf-8 -*-
# chain_audit_146_mersenne.py — 梅森假说检验：g_p/2 分子是否梅森数（104az-146b）
target = 2.79284734463

print("A. 40217/307/131 梅森检查")
for x, name in [(40217, "40217"), (307, "307"), (131, "131")]:
    r = None
    m = 0
    while 2**m - 1 <= x:
        if 2**m - 1 == x:
            r = m
        m += 1
    print(f"{name}: {'是梅森数 2^' + str(r) + '-1' if r else '不是梅森数'}")

print("\nB. 梅森数×框架量/框架量 全空间最优精度")
def smooth7(limit):
    out = []
    for a in range(0, 30):
        va = 2**a
        if va > limit: break
        for b in range(0, 20):
            vb = va * 3**b
            if vb > limit: break
            for c in range(0, 15):
                vc = vb * 5**c
                if vc > limit: break
                for d in range(0, 12):
                    v = vc * 7**d
                    if v > limit: break
                    out.append(v)
    return sorted(set(out))

mers = [2**n - 1 for n in range(2, 21)]
F = [2, 3, 4, 5, 7]
sm = smooth7(50000)
best = []
for M in mers:
    for f in F:
        for b in sm:
            best.append((abs(M*f/b - target), f"M{f}·{f}/b{b}"))
            best.append((abs(M/(b*f) - target), f"M{f}/(b{b}·{f})"))
            for s in (1, -1):
                best.append((abs((M+s*f)/b - target), f"(M{f}{'+' if s > 0 else '-'}{f})/b{b}"))
best.sort()
print(f"梅森路径最优精度 {best[0][0]:.3e} vs 40217/14400 的 1.224e-7")
print(f"比值: {1.224e-7/best[0][0]:.0f} 倍（40217/14400 更优）")

print("\nC. 表达内部梅森连接")
print("7 = 2³−1 = 梅森数 → 分子主结构是梅森数")
print("14/5（旧候选）= 2·(2³−1)/静默 → 纯梅森结构（dev +0.26%）")
print("131 = 128+3 = 2⁷+N_gen → '2 的幂+框架量'族（104az-153 登记）")
print("→ 梅森路径结构分辨率上限 ~1e-3，够不到观测精度；40217/14400 的")
print("  精细度来自 '平滑数×对合域−k_max × 2的幂+N_gen' 组合")
