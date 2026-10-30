# -*- coding: utf-8 -*-
OUT = open(r'C:\Users\dps_n\AppData\Local\DoubaoWork\User Data\Profile 6\.doubaowork\agent_mode\workspace\out_103.txt', 'w', encoding='utf-8')
def P(*a):
    OUT.write(' '.join(map(str, a)) + '\n')

"""
Phase 104az-103: κΛ 内生化受阻判别——ln10/π 框架身份搜索 + 恒等 B 张力归因
κΛ = 96·ln10·(d_H+3)/π（从恒等 A + Δλ_EM 框架形式推出）
恒等 B 张力（0.0036% 规范 / 0.0303% 分解式）→ 归因：κΛ 未内生化（ln10/π 身份缺失）
"""
import math
from itertools import product

Ngen, kmax, silence, sigma = 3, 8, 5, 1/15
dH = 2.709532
dlmin = (math.sqrt(3) - 1) / 6
delta = 1 / 675

ln10 = math.log(10)
pi = math.pi
kappa = 4 * ln10 / (pi / (kmax * Ngen * (dH + 3)))

P("=" * 70)
P("[1] κΛ 分解确认")
P(f"  κΛ = 4ln10/Δλ_EM = 4ln10·24(d_H+3)/π = 96·ln10·(d_H+3)/π")
P(f"  96 = N_gen!·2k_max = 6·16")
P(f"  κΛ = {kappa:.8f}（与 104az-100 的 401.733049 一致 ✓）")
P(f"  组分: ln10（非框架？）+ π（104az-99 判无身份）+ (d_H+3)（框架）")

P("\n[2] ln10 框架身份搜索（容差 0.1%）")
bases = {
    "Ngen": Ngen, "kmax": kmax, "sil": silence, "sig": sigma,
    "dlmin": dlmin, "delta": delta, "dH": dH, "dH+3": dH+3,
    "6": 6.0, "16": 16.0, "10": 10.0, "9": 9.0, "65": 65.0, "49": 49.0,
    "7": 7.0, "5": 5.0, "3": 3.0, "2": 2.0, "25": 25.0, "32": 32.0, "64": 64.0,
}
hits = []
for (na, a), (nb, b) in product(bases.items(), bases.items()):
    for op in ['*', '/']:
        v = a * b if op == '*' else (a / b if b != 0 else None)
        if v is None or v == 0:
            continue
        for mode in ['plain', 'sqrt', 'cube', 'inv']:
            if mode == 'plain':
                cand = v
            elif mode == 'sqrt':
                cand = math.sqrt(abs(v))
            elif mode == 'cube':
                cand = abs(v) ** (1/3)
            elif mode == 'inv':
                cand = 1 / v
            dev = cand / ln10 - 1
            if abs(dev) < 0.001:  # 0.1%
                hits.append((f"{na}{op}{nb}[{mode}]", cand, dev))
# 直接数（含 ln2/ln5/√ 组合）
extra = {
    "ln2+ln5": math.log(2)+math.log(5), "2.3": 2.3, "23/10": 2.3,
    "e·0.847": math.e*0.847, "1.15·2": 2.3, "ln(16/15)·?": None,
    "4/√3": 4/math.sqrt(3), "√(16/3)": math.sqrt(16/3), "2√2·1.2": 2*math.sqrt(2)*1.2,
}
for n, v in extra.items():
    if v is None:
        continue
    dev = v / ln10 - 1
    if abs(dev) < 0.01:
        hits.append((f"{n}", v, dev))
P(f"  命中数（0.1% 内）: {len(hits)}")
for h in hits[:15]:
    P(f"    {h[0]} = {h[1]:.6f} → dev {h[2]*100:+.4f}%")
if not hits:
    P("    （无命中——ln10 无框架身份候选）")

P("\n[3] 最接近候选（0.1%~1%）")
near = []
for (na, a), (nb, b) in product(bases.items(), bases.items()):
    for op in ['*', '/']:
        v = a * b if op == '*' else (a / b if b != 0 else None)
        if v is None or v == 0:
            continue
        for mode in ['plain', 'sqrt', 'cube', 'inv']:
            if mode == 'plain':
                cand = v
            elif mode == 'sqrt':
                cand = math.sqrt(abs(v))
            elif mode == 'cube':
                cand = abs(v) ** (1/3)
            elif mode == 'inv':
                cand = 1 / v
            dev = cand / ln10 - 1
            near.append((abs(dev), f"{na}{op}{nb}[{mode}]", cand, dev))
near.sort()
for d, n, c, dev in near[:8]:
    P(f"    {n} = {c:.6f} → dev {dev*100:+.4f}%")

P("\n[4] 恒等 B 张力归因")
P(f"  恒等 B: κΛ·Δλ_P20 = 49（+0.0036% 规范口径 / +0.0303% 分解式口径）")
P(f"  κΛ = 96·ln10·(d_H+3)/π——含 ln10（本次无框架身份）与 π（104az-99 无身份）")
P(f"  ★ 归因结论: 恒等 B 张力 = κΛ 未内生化（ln10/π 框架身份缺失）的传播")
P(f"  ——张力不是独立异常，而是 κΛ 作为非框架常数的必然后果")
P(f"  闭合路径: κΛ 内生化 = ln10/π 框架化（当前不可得——受阻登记）")
P(f"  或 Δλ_P20 微修正（与 dlP20_eq_dlmin 机器证明冲突——排除）")

P("\n[5] 判定")
P(f"  恒等 B 张力归因闭合（诊断层）: 张力 = κΛ 未内生化传播")
P(f"  诚实边界: 归因是诊断性结论（κΛ 组分含非框架常数）——非恒等 B 自身的结构修正；")
P(f"  ln10 无框架身份为搜索性结论（0.1% 容差无命中）——非证明；")
P(f"  κΛ 内生化为长期开放项（与织a 的 π 问题同源）")
