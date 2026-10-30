# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-67c：补测过渡区 0.02/0.1/0.2 au 网格收敛性
================================================================
P7-5e-67/67b 裁决：低场伪影（53/49 撤回）、高场收敛（8 稳定）
过渡区未测——0.02 au（30=3×10）、0.1 au（12 平台起点）、0.2 au（11=k_max+N_gen）
补测确定"框架量身份区"的精确边界
"""
import json, os, time
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import warnings
warnings.filterwarnings('ignore')

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def hamiltonian_2d_hydrogen(N_r, r_max, m, B):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    off_diag = np.ones(N_r - 1) / (2.0 * dr ** 2)
    diag_main = np.ones(N_r) / dr ** 2
    landau_centrifugal = (m + 0.5 * B * r ** 2) ** 2 / (2.0 * r ** 2)
    coulomb = -1.0 / r
    H_mat = diags([-off_diag, diag_main + landau_centrifugal + coulomb, -off_diag],
                  offsets=[-1, 0, 1], shape=(N_r, N_r), format='csr')
    return H_mat

def n_bound(N_r, r_max, m, B, k=300):
    H = hamiltonian_2d_hydrogen(N_r, r_max, m, B)
    try:
        vals, _ = eigsh(H.astype(np.float64), k=min(k, N_r - 5),
                        which='SA', maxiter=50000, tol=1e-9)
        return int(np.sum(np.real(vals) < 0))
    except Exception:
        return 0

def scan(B, N_r, r_max, m_max=8, k=300):
    tot = 0
    for m in range(-m_max, m_max + 1):
        tot += n_bound(N_r, r_max, m, B, k)
    return tot

print("="*104)
print("P7-5e-67c：补测过渡区 0.02/0.1/0.2 au 网格收敛性")
print("="*104)

grids = [(1500, 60.0), (2000, 80.0), (3000, 100.0)]
tests = {0.02: (30, "3×10"), 0.1: (12, "N_gen·k_max/2（12 平台起点）"), 0.2: (11, "k_max+N_gen")}

results = {}
for B, (orig, ident) in tests.items():
    print()
    print("【B_au=%.2f（%.1f MG）——原计数 %d = %s】" % (B, B*2350, orig, ident))
    row = {}
    for (N_r, r_max) in grids:
        t0 = time.time()
        n = scan(B, N_r, r_max)
        row["%dx%s" % (N_r, r_max)] = n
        print("  N_r=%d r_max=%.0f → n_bound=%d  [%.0fs]" % (N_r, r_max, n, time.time()-t0), flush=True)
    results[B] = row

print()
print("【收敛性裁决】")
print("-"*104)
for B, row in results.items():
    vals = list(row.values())
    spread = max(vals) - min(vals)
    orig, ident = tests[B]
    if spread == 0:
        v = "★★ 完全稳定——%d = %s 身份可信（非网格伪影）" % (orig, ident)
    elif spread <= 2:
        v = "★ 近似稳定（%d 波动）——身份倾向保留但标注敏感性" % spread
    else:
        v = "✗ 网格依赖（%d 波动）——%d = %s 身份撤回" % (spread, orig, ident)
    print("  B=%.2f: %s → %s" % (B, row, v))

json.dump(results, open(os.path.join(BASE, "_phase102_p7_5e67c_transition_conv.json"), "w", encoding="utf-8"), indent=1)
print()
print("JSON 落盘 ✓  exit 0")
