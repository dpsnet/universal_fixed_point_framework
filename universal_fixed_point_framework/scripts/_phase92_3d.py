# -*- coding: utf-8 -*-
"""Phase 92 M92-1/2/3：3D 圆柱坐标氢原子（m 固定）
H = -1/(2r)d/dr(r d/dr) - 1/2 d2/dz2 + (m+Br^2/2)^2/(2r^2) - 1/sqrt(r^2+z^2)
- 束缚态计数（E<0）→ 3D η_sc(B)
- 正能态 IPR 随 Lz 标度 → D2 谱维数
"""
import json, io, os, sys
import numpy as np
from scipy.sparse import diags, kron, identity
from scipy.sparse.linalg import eigsh

def hamiltonian_3d(N_r, r_max, N_z, z_max, m, B):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    # 径向算子（同 2D）
    off_r = np.ones(N_r - 1) / (2.0 * dr**2)
    diag_r = np.ones(N_r) / dr**2 + (m + 0.5 * B * r**2)**2 / (2.0 * r**2)
    T_r = diags([-off_r, diag_r, -off_r], offsets=[-1, 0, 1], shape=(N_r, N_r), format='csr')
    # z 方向算子
    dz = z_max / N_z
    zk = (np.arange(N_z) - N_z / 2.0) * dz
    off_z = np.ones(N_z - 1) / (2.0 * dz**2)
    diag_z = np.ones(N_z) / dz**2
    T_z = diags([-off_z, diag_z, -off_z], offsets=[-1, 0, 1], shape=(N_z, N_z), format='csr')
    # Kronecker 和
    H = kron(T_r, identity(N_z, format='csr')) + kron(identity(N_r, format='csr'), T_z)
    # 库仑势（对角）
    V = -1.0 / np.sqrt(r[:, None]**2 + zk[None, :]**2)
    H = H + diags(V.ravel(), offsets=0, format='csr')
    return H, r, zk

def count_bound(N_r, r_max, N_z, z_max, m, B, k=80):
    H, r, zk = hamiltonian_3d(N_r, r_max, N_z, z_max, m, B)
    try:
        vals = eigsh(H.astype(np.float64), k=min(k, H.shape[0] - 2),
                     which='LM', sigma=-0.15, maxiter=40000, tol=1e-8,
                     return_eigenvectors=False)
        vals = np.real(vals)
        return int(np.sum(vals < -1e-4))
    except Exception:
        try:
            vals = eigsh(H.astype(np.float64), k=min(k, H.shape[0] - 2),
                         which='SA', maxiter=40000, tol=1e-8,
                         return_eigenvectors=False)
            return int(np.sum(np.real(vals) < -1e-4))
        except Exception as e:
            print("  [ERR] m=%d B=%.3f: %s" % (m, B, str(e)[:80]), file=sys.stderr)
            return None

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

# M92-1 收敛性：B=0.01, m=0 —— r_max/z_max 扫描（小网格先验证）
print("=== M92-1 收敛性（B=0.01, m=0, 束缚态数）===", flush=True)
for cfg in [(60, 40, 60, 40), (80, 50, 80, 50), (100, 60, 100, 60)]:
    n = count_bound(cfg[0], cfg[1], cfg[2], cfg[3], m=0, B=0.01)
    print("  N_r=%d r_max=%d N_z=%d z_max=%d -> 束缚态数=%s" % (cfg[0], cfg[1], cfg[2], cfg[3], n), flush=True)

# M92-2 3D η_sc：B 扫描（m=0 单分波先行，全部 m 后期）
print("\n=== M92-2 3D η_sc（m=0，B 扫描）===", flush=True)
results = []
for B in (0.005, 0.01, 0.02, 0.05, 0.1, 0.2):
    n = count_bound(100, 60, 100, 60, m=0, B=B)
    results.append({"B": B, "n_bound_m0": n})
    print("  B=%.3f a.u. (%5.1f MG) m=0 束缚态=%s" % (B, B * 2350, n), flush=True)
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_eta_3d_m0.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("written paperX_eta_3d_m0.json")
