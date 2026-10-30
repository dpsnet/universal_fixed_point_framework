# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-67：束缚态计数网格收敛性检验
================================================================
隐患：束缚态计数依赖网格（N_r=1500, r_max=60）——若换网格计数变化，
则框架量身份（49/40/30/.../8/7/5）可能是网格选择伪影——必须排除。

检验：同一场强（B_au=0.25——n=8=k_max、B_au=0.01——n=40、B_au=0.001——n=53）
用不同 N_r/r_max 重算：
- (1500, 60)  原参数
- (2000, 80)  加密+扩大
- (3000, 100) 更密+更大
若 n_bound 稳定 → 框架量身份非网格伪影（收敛）
若 n_bound 变化 → 网格依赖登记（身份存疑）
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
print("P7-5e-67：束缚态计数网格收敛性检验")
print("="*104)

grids = [(1500, 60.0), (2000, 80.0), (3000, 100.0)]
test_Bs = [0.001, 0.01, 0.25]

results = {}
for B in test_Bs:
    row = {}
    print()
    print("【B_au=%.3f（%.1f MG）——原计数 %d】" % (B, B*2350, {0.001:53, 0.01:40, 0.25:8}[B]))
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
    orig = {0.001:53, 0.01:40, 0.25:8}[B]
    verdict = "★★ 稳定（非网格伪影）" if spread == 0 else ("★ 近似稳定（%d 波动）" % spread if spread <= 2 else "✗ 网格依赖（框架量身份存疑）")
    print("  B=%.3f: %s → %s" % (B, row, verdict))

json.dump(results, open(os.path.join(BASE, "_phase102_p7_5e67_grid_conv.json"), "w", encoding="utf-8"), indent=1)
print()
print("JSON 落盘 ✓  exit 0")
