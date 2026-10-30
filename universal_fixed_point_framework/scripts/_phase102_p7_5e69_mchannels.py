# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-69：束缚态 m 通道分解——2²+k² 的物理来源
================================================================
P7-5e-68：n = 2² + k²（k 随场强递减）——2² = 4 固定第一项
候选物理：m 通道分解——每个 m 的束缚态数 N_m——n = Σ N_m
检验：N_m 结构——4 = 2² 是否 = 2 个主通道×2？k² 是否 = 次通道？
"""
import json, os, time
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import warnings
warnings.filterwarnings('ignore')

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def n_bound_m(N_r, r_max, m, B, k=300):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    off_diag = np.ones(N_r - 1) / (2.0 * dr ** 2)
    diag_main = np.ones(N_r) / dr ** 2
    landau_centrifugal = (m + 0.5 * B * r ** 2) ** 2 / (2.0 * r ** 2)
    coulomb = -1.0 / r
    H = diags([-off_diag, diag_main + landau_centrifugal + coulomb, -off_diag],
              offsets=[-1, 0, 1], shape=(N_r, N_r), format='csr')
    try:
        vals, _ = eigsh(H.astype(np.float64), k=min(k, N_r - 5),
                        which='SA', maxiter=50000, tol=1e-9)
        return int(np.sum(np.real(vals) < 0))
    except Exception:
        return 0

print("="*104)
print("P7-5e-69：束缚态 m 通道分解——2²+k² 的物理来源")
print("="*104)

N_r, r_max, m_max = 1500, 60.0, 8
tests = [(0.001, 53), (0.04, 20), (0.07, 13), (0.25, 8), (0.4, 5)]

for B, n_total in tests:
    print()
    print("【B_au=%.3f（%.1f MG）——n_total=%d = 2²+k² 检验】" % (B, B*2350, n_total))
    Ns = {}
    for m in range(-m_max, m_max + 1):
        t0 = time.time()
        n = n_bound_m(N_r, r_max, m, B)
        Ns[m] = n
    nonzero = {m: n for m, n in Ns.items() if n > 0}
    tot = sum(Ns.values())
    print("  Σ_m N_m = %d（校验 n_total=%d）" % (tot, n_total))
    print("  非零通道（%d 个）：" % len(nonzero), nonzero)
    # 分析结构
    vals = sorted(nonzero.values(), reverse=True)
    if len(vals) >= 2:
        lead = vals[0]
        rest = vals[1:]
        print("  首通道 N= %d；其余通道 = %s；其余和 = %d" % (lead, rest, sum(rest)))
        # 检验 4 + k² 分解
        rem = tot - lead
        if tot == 4 + int(np.sqrt(tot-4))**2 if tot >= 4 else False:
            k = int(np.sqrt(tot - 4))
            print("  ★★ n = 2² + %d²：首通道 %d = 4？其余 %d = %d²？" % (k, lead, rem, k))
    else:
        print("  单通道：N = %s" % vals)

json.dump({}, open(os.path.join(BASE, "_phase102_p7_5e69_mchannels.json"), "w", encoding="utf-8"), indent=1)
print()
print("JSON 落盘 ✓  exit 0")
