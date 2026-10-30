# -*- coding: utf-8 -*-
OUT = open(r'C:\Users\dps_n\AppData\Local\DoubaoWork\User Data\Profile 6\.doubaowork\agent_mode\workspace\out_105.txt', 'w', encoding='utf-8')
def P(*a):
    OUT.write(' '.join(map(str, a)) + '\n')

"""
Phase 104az-105: κΛ 内生化强候选系统检验
κΛ = 401.73304855（恒等 A 口径）
候选: κΛ = 2k_max·静默²·(1+1/231)，231 = N_gen·(k_max−1)·(N_active+k_max) = 21·11 纯框架组合
系统搜索: 纯框架量组合（含 (1±1/D) 修正型），容差分层
"""
import math
from itertools import product, combinations

kappa = 401.73304855
Ngen, kmax, sil, Nact = 3, 8, 5, 3
dH = 2.709532
dlmin_inv = 3*(math.sqrt(3)+1)
sigma_inv = 15

# 框架量库（正数）
F = {
    "Ngen": Ngen, "kmax": kmax, "sil": sil, "Nact": Nact,
    "sig_inv": sigma_inv, "dlmin_inv": dlmin_inv, "dH3": dH+3,
    "7": 7.0, "11": 11.0, "16": 16.0, "21": 21.0, "96": 96.0,
    "49": 49.0, "10": 10.0, "9": 9.0, "65": 65.0, "64": 64.0,
    "32": 32.0, "25": 25.0, "675": 675.0, "320": 320.0, "6": 6.0,
    "2": 2.0, "231": 231.0, "77": 77.0, "5": 5.0, "3": 3.0,
    "8": 8.0,
}

P("=" * 70)
P("[1] 主候选验证")
cand1 = 400 * (1 + 1/231)
P(f"  κΛ = 2k_max·静默²·(1+1/231) = {cand1:.10f}")
P(f"  231 = N_gen·(k_max−1)·(N_active+k_max) = 3·7·11 = 21·11（纯框架）")
P(f"  dev = {(cand1/kappa-1)*100:+.7f}%")

P("\n[2] 系统搜索：(1±1/D) 修正型，主量 a·b")
hits = []
for (na, a), (nb, b) in product(F.items(), F.items()):
    base = a * b
    for Dname, D in F.items():
        for sgn in [1, -1]:
            v = base * (1 + sgn / D)
            dev = v / kappa - 1
            if abs(dev) < 1e-5:  # 0.001%
                hits.append((abs(dev), f"{na}·{nb}·(1{'−' if sgn<0 else '+'}1/{Dname})", v, dev))
hits.sort()
P(f"  0.001% 内命中: {len(hits)}")
for d, n, v, dev in hits[:20]:
    P(f"    {n} = {v:.8f} → dev {dev*100:+.6f}%")

P("\n[3] 系统搜索：a·b/c 型")
hits2 = []
for (na, a), (nb, b), (nc, c) in product(F.items(), F.items(), F.items()):
    if c == 0:
        continue
    v = a * b / c
    dev = v / kappa - 1
    if abs(dev) < 2e-5:  # 0.002%
        hits2.append((abs(dev), f"{na}·{nb}/{nc}", v, dev))
hits2.sort()
P(f"  0.002% 内命中: {len(hits2)}")
for d, n, v, dev in hits2[:15]:
    P(f"    {n} = {v:.8f} → dev {dev*100:+.5f}%")

P("\n[4] 系统搜索：a·(1±1/D) 单量型")
hits3 = []
for na, a in F.items():
    for Dname, D in F.items():
        for sgn in [1, -1]:
            v = a * (1 + sgn / D)
            dev = v / kappa - 1
            if abs(dev) < 5e-5:  # 0.005%
                hits3.append((abs(dev), f"{na}·(1{'−' if sgn<0 else '+'}1/{Dname})", v, dev))
hits3.sort()
P(f"  0.005% 内命中: {len(hits3)}")
for d, n, v, dev in hits3[:15]:
    P(f"    {n} = {v:.8f} → dev {dev*100:+.5f}%")

P("\n[5] 判别结论")
P(f"  主候选 dev −0.00036%——强数值候选（纯框架组合，231 三框架身份）")
P(f"  若 κΛ = 400·(1+1/231) 成立: κΛ 内生化达成（不再依赖 ln10/π）")
P(f"  → 恒等 B 张力重定义: 张力 = κΛ 表达残差（−0.00036%）")
P(f"  诚实边界: 搜索命中性质未排除（框架量库 ~29 个，组合自由度 ~10⁴）")
P(f"  → 需机制动机（为何 231 = N_gen·7·11 作修正分母）才能升格")
