# -*- coding: utf-8 -*-
"""Phase 96 M96-1：3D 氢原子全分波（m=-8..8）束缚态计数 → 3D 全分波 η_sc(B)
复用 _phase92_3d.py 的 hamiltonian_3d/count_bound；m_max=8（与 Phase 89/93 2D 全分波同口径）
网格：N_r=100/r_max=60/N_z=100/z_max=60（Phase 92 M92-1 收敛性验证的成熟配置）
"""
import json, io, os, sys
import numpy as np

def hamiltonian_3d(N_r, r_max, N_z, z_max, m, B):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    off_r = np.ones(N_r - 1) / (2.0 * dr**2)
    diag_r = np.ones(N_r) / dr**2 + (m + 0.5 * B * r**2)**2 / (2.0 * r**2)
    T_r = diags([-off_r, diag_r, -off_r], offsets=[-1, 0, 1], shape=(N_r, N_r), format='csr')
    dz = z_max / N_z
    zk = (np.arange(N_z) - N_z / 2.0) * dz
    off_z = np.ones(N_z - 1) / (2.0 * dz**2)
    diag_z = np.ones(N_z) / dz**2
    T_z = diags([-off_z, diag_z, -off_z], offsets=[-1, 0, 1], shape=(N_z, N_z), format='csr')
    H = kron(T_r, identity(N_z, format='csr')) + kron(identity(N_r, format='csr'), T_z)
    V = -1.0 / np.sqrt(r[:, None]**2 + zk[None, :]**2)
    H = H + diags(V.ravel(), offsets=0, format='csr')
    return H, r, zk

def count_bound(N_r, r_max, N_z, z_max, m, B, k=80):
    H, r, zk = hamiltonian_3d(N_r, r_max, N_z, z_max, m, B)
    try:
        vals = eigsh(H.astype(np.float64), k=min(k, H.shape[0] - 2),
                     which='LM', sigma=-0.15, maxiter=40000, tol=1e-8,
                     return_eigenvectors=False)
        return int(np.sum(np.real(vals) < -1e-4))
    except Exception:
        try:
            vals = eigsh(H.astype(np.float64), k=min(k, H.shape[0] - 2),
                         which='SA', maxiter=40000, tol=1e-8,
                         return_eigenvectors=False)
            return int(np.sum(np.real(vals) < -1e-4))
        except Exception as e:
            print("  [ERR] m=%d B=%.3f: %s" % (m, B, str(e)[:80]), file=sys.stderr)
            return None

from scipy.sparse import diags, kron, identity
from scipy.sparse.linalg import eigsh

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
MS = list(range(-8, 9))
BS = (0.005, 0.01, 0.02, 0.05, 0.1, 0.2)

print("=== M96-1 3D 全分波束缚态计数（m=-8..8, B 扫描）===", flush=True)
rows = []
for B in BS:
    total = 0
    per_m = {}
    for m in MS:
        n = count_bound(100, 60, 100, 60, m, B)
        per_m[str(m)] = n
        total += (n or 0)
    rows.append({"B": B, "n_bound_full": total, "per_m": per_m})
    print("  B=%.3f a.u. (%5.1f MG) 全分波束缚态=%d" % (B, B * 2350, total), flush=True)

with io.open(os.path.join(BASE, "_gaia_abs", "paperX_eta_3d_full.json"), "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=1)
print("written paperX_eta_3d_full.json")
