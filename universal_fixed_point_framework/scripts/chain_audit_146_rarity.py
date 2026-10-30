# -*- coding: utf-8 -*-
# chain_audit_146_rarity.py — g_p/2 = 40217/14400 命中稀有性评估（104az-146）
# 主评估：7-平滑分母分数空间中该精度的稀有性；结构评估：分子框架身份唯一性
target = 2.79284734463
cand_n, cand_d = 40217, 14400

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

LIM = 50000
dens = smooth7(LIM)
print(f"7-平滑分母 ≤{LIM}: {len(dens)} 个")

hits = []
for b in dens:
    a = round(target * b)
    err = abs(a/b - target)
    hits.append((err, a, b))
hits.sort()
print("\n=== 最优 8 名 ===")
for i, (err, a, b) in enumerate(hits[:8], 1):
    mark = "  ← 40217/14400" if (a, b) == (cand_n, cand_d) else ""
    print(f"#{i} |a/b−t|={err:.3e}  a/b={a}/{b}{mark}")

for w in (1e-6, 1e-7, 1e-8):
    n = sum(1 for e, _, _ in hits if e < w)
    print(f"窗口 |err| < {w:.0e}: {n} 个候选")

rank = next(i for i, (e, a, b) in enumerate(hits, 1) if (a, b) == (cand_n, cand_d))
print(f"\n40217/14400 精度排名: #{rank}/{len(hits)}（{rank/len(hits)*100:.2f}%）")

print("\n=== 结构层：窗口内候选的框架身份 ===")
# 7-平滑分母 + 分子可分解为框架量组合（307=315−8、131=128+3）
print("71846 = 2×35923（35923 素数，无框架构造）→ 无框架身份")
print("40217 = 307×131；307=45×7−8=N_gen²·静默·对合域−k_max；131=128+3=幂基·k_max²+N_gen")
print("14400 = N_gen²·静默²·k_max² → 唯一框架出生证明候选")
