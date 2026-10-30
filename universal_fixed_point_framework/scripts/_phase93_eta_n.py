# -*- coding: utf-8 -*-
"""Phase 93 M93-2：η_sc(n) 量子标度——逐主量子数 n 的束缚态衰减
2D 氢原子（同 §3.2.4），B 扫描，按束缚能 |E_n|≈1/(2n²) 归类 n
检验 NMLO 拟合参数 |EW_n|=A_s n^m（m=3.39）的量子基础：η_sc(n) 是否随 n 幂律增
"""
import json, io, os
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh

def hamiltonian_2d_hydrogen(N_r, r_max, m, B):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    off_diag = np.ones(N_r - 1) / (2.0 * dr**2)
    diag_main = np.ones(N_r) / dr**2
    landau_centrifugal = (m + 0.5 * B * r**2)**2 / (2.0 * r**2)
    coulomb = -1.0 / r
    H_mat = diags([-off_diag, diag_main + landau_centrifugal + coulomb, -off_diag],
                  offsets=[-1, 0, 1], shape=(N_r, N_r), format='csr')
    return H_mat, r

def bound_states_by_n(N_r, r_max, m, B, k=150):
    """束缚态按 n 归类（E<0，n=round(sqrt(1/(2|E|)))）"""
    H, r = hamiltonian_2d_hydrogen(N_r, r_max, m, B)
    vals = eigsh(H.astype(np.float64), k=min(k, N_r - 5), which='SA',
                 maxiter=40000, tol=1e-9, return_eigenvectors=False)
    vals = np.real(vals)
    counts = {}
    for v in vals:
        if v < -1e-5:
            n = int(round(np.sqrt(1.0 / (2.0 * abs(v)))))
            counts[n] = counts.get(n, 0) + 1
    return counts

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_gaia_abs"
N_R, R_MAX = 1500, 60.0
results = []
print("=== M93-2 η_sc(n) 量子标度（2D 氢原子，全分波 m=-8..8 合并）===", flush=True)
for B in (0.005, 0.01, 0.02, 0.05, 0.1):
    tot = {}
    for m in range(-8, 9):
        c = bound_states_by_n(N_R, R_MAX, m, B)
        for n, cnt in c.items():
            tot[n] = tot.get(n, 0) + cnt
    results.append({"B": B, "by_n": {str(k): v for k, v in sorted(tot.items())}})
    print("  B=%.3f a.u. 各n束缚态数: %s" % (B, {k: v for k, v in sorted(tot.items())}), flush=True)

# η_sc(n)：ref B=0.005 → 各 B
ref = {int(k): v for k, v in results[0]["by_n"].items()}
print("\n=== η_sc(n) 对照（ref B=0.005）===", flush=True)
eta_table = []
for r in results[1:]:
    B = r["B"]
    cur = {int(k): v for k, v in r["by_n"].items()}
    row = {"B": B}
    for n in sorted(set(ref) | set(cur)):
        r0, rB = ref.get(n, 0), cur.get(n, 0)
        eta = 1.0 - rB / r0 if r0 > 0 else None
        row[str(n)] = round(eta, 3) if eta is not None else None
    eta_table.append(row)
    print("  B=%.3f: %s" % (B, {k: v for k, v in row.items() if k != 'B'}), flush=True)
with io.open(os.path.join(BASE, "paperX_eta_sc_n.json"), "w", encoding="utf-8") as f:
    json.dump({"raw": results, "eta_n": eta_table}, f, ensure_ascii=False, indent=1)
print("written paperX_eta_sc_n.json")
