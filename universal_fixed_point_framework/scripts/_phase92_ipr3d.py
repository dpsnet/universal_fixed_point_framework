# -*- coding: utf-8 -*-
"""Phase 92 M92-3：3D 正能态 IPR 随 Lz 标度（奇异连续谱检测）
B=0.05/0.1 a.u., m=0，正能区 E∈[0,2]，Lz∈{30,60,120}（dz 固定 0.5）
D2 = -dlog(IPR)/dlog(Lz)
"""
import json, io, os
import numpy as np
from scipy.sparse import diags, kron, identity
from scipy.sparse.linalg import eigsh

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
    return H, r, zk, dz

def pos_states_ipr(N_r, r_max, N_z, z_max, m, B, emin=0.0, emax=2.0, k=100):
    H, r, zk, dz = hamiltonian_3d(N_r, r_max, N_z, z_max, m, B)
    dr = r_max / N_r
    try:
        vals, vecs = eigsh(H.astype(np.float64), k=min(k, H.shape[0] - 2),
                           which='LM', sigma=0.8, maxiter=40000, tol=1e-9)
    except Exception:
        try:
            vals, vecs = eigsh(H.astype(np.float64), k=min(k, H.shape[0] - 2),
                               which='LM', sigma=0.3, maxiter=40000, tol=1e-9)
        except Exception as e:
            print("  [ERR] %s" % str(e)[:80], file=sys.stderr)
            return []
    vals = np.real(vals)
    # 3D IPR：Σ|ψ|⁴ r dr dz / (Σ|ψ|² r dr dz)²
    rw = np.sqrt(r * dr)
    zc = np.sqrt(dz)  # 均匀 z 网格常权重
    iprs = []
    for i, v in enumerate(vals):
        if emin <= v <= emax:
            psi = vecs[:, i].reshape(N_r, N_z)
            w = psi * rw[:, None] * zc
            w = w / np.sqrt(np.sum(w**2))
            iprs.append(float(np.sum(w**4)))
    return iprs

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
DZ = 0.5
results = []
print("=== M92-3 3D 正能态 IPR 随 Lz 标度 ===", flush=True)
for B in (0.05, 0.1):
    for z_max in (30.0, 60.0, 120.0):
        N_z = int(z_max / DZ)
        iprs = pos_states_ipr(80, 40, N_z, z_max, m=0, B=B)
        if iprs:
            med = float(np.median(iprs[:10]))
        else:
            med = None
        print("  B=%.2f Lz=%3.0f (Nz=%d) 正能态=%d IPR中位=%s" % (
            B, z_max, N_z, len(iprs), "%.3g" % med if med is not None else "—"), flush=True)
        results.append({"B": B, "Lz": z_max, "n": len(iprs), "ipr_med": med})
    # D2（用 60/120 档）
    a = [r for r in results if r["B"] == B]
    if len(a) >= 3 and a[1]["ipr_med"] and a[2]["ipr_med"] and a[1]["ipr_med"] > 0:
        D2 = -np.log(a[2]["ipr_med"] / a[1]["ipr_med"]) / np.log(2.0)
        print("  B=%.2f D2(Lz 60->120) = %.3f" % (B, D2), flush=True)
        a[-1]["D2"] = float(D2)
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_spectrum_ipr3d.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("written paperX_spectrum_ipr3d.json")
