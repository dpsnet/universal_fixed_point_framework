# -*- coding: utf-8 -*-
"""Phase 104az-59 v3：窗口内振子强度保留份额 S_win(n,B)（m=0 3D 氢）——能量窗归类 + TRK 守恒自检
- 解 m=0 3D 柱坐标氢各 B 本征态
- 加权归一化修正（eigsh 欧几里得归一 → 除以 sqrt(加权范数)）
- n=2 流形：能量窗识别（±0.06 取 2 个最低）
- 对每个解出态 j：d2_j = Σ_{i∈n2}|<i|z|j>|²
- 线窗：光子能量 E_ph(n)=1/8-1/(2n²)，窗 ±ΔE(n)（对应 ±80 Å：ΔE = E_ph·2·80/λ_n）
- S_win(n,B) = 窗内 d2 / 总 d2；TRK 自检：总 d2 随 B 应 ~ 守恒
"""
import json, sys, io, os
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
    return H, r, zk

def solve(N_r, r_max, N_z, z_max, m, B, k=250, sigma=-0.08):
    H, r, zk = hamiltonian_3d(N_r, r_max, N_z, z_max, m, B)
    vals, vecs = eigsh(H.astype(np.float64), k=min(k, H.shape[0]-2),
                       which='LM', sigma=sigma, maxiter=80000, tol=1e-9)
    idx = np.argsort(vals)
    return vals[idx], vecs[:, idx], r, zk

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
N_r, r_max, N_z, z_max = 90, 60.0, 90, 60.0
dr, dz = r_max/N_r, z_max/N_z

def weighted_norm2(psi, r):
    return dr * dz * np.sum(r[:, None] * psi**2)

def z_parity(psi, zk):
    """z 奇偶性：<psi|z|psi>（对角）——大=奇（p 型），小=偶（s 型）"""
    return dr * dz * np.sum(r[:, None] * psi**2 * zk[None, :])

def run(B_au):
    vals, vecs, r, zk = solve(N_r, r_max, N_z, z_max, m=0, B=B_au)
    k = vecs.shape[1]
    # 加权归一化
    for i in range(k):
        psi = vecs[:, i].reshape(N_r, N_z)
        n2 = weighted_norm2(psi, r)
        if n2 > 1e-20:
            vecs[:, i] /= np.sqrt(n2)
    # n=2 流形：E2=-0.125，窗 ±0.06，取 2 个
    E2 = -0.125
    i2 = np.where(np.abs(vals - E2) < 0.06)[0]
    i2 = i2[np.argsort(np.abs(vals[i2] - E2))][:2]
    if len(i2) < 2:
        print("  [WARN] B=%.3f n2 只识别 %d 个" % (B_au, len(i2)), flush=True)
    # 对每个态 j：d2_j = Σ_{i∈n2} |<i|z|j>|²
    d2 = np.zeros(k)
    for j in range(k):
        pj = vecs[:, j].reshape(N_r, N_z)
        tot = 0.0
        for i in i2:
            pi = vecs[:, i].reshape(N_r, N_z)
            val = dr * dz * np.sum(r[:, None] * pi * pj * zk[None, :])
            tot += val**2
        d2[j] = tot
    return vals, d2, i2

# Balmer 线参数：n, λ(Å), E_ph(au)=1/8-1/2n²
LINES = {3: (6562.8, 1.0/8 - 1.0/18),
         4: (4861.3, 1.0/8 - 1.0/32),
         5: (4340.5, 1.0/8 - 1.0/50),
         6: (4101.7, 1.0/8 - 1.0/72),
         7: (3970.1, 1.0/8 - 1.0/98)}
W_ANG = 80.0  # Å

print("=== v3 窗口内保留份额 S_win(n,B)——m=0 π 通道，±80 Å 窗 ===", flush=True)
B_list = (0.0001, 0.005, 0.01, 0.02, 0.05, 0.1)
results = []
for B in B_list:
    print("B=%.4f a.u. (%.1f MG)..." % (B, B*2350), flush=True)
    vals, d2, i2 = run(B)
    E2_avg = np.mean(vals[i2])
    total_d2 = float(np.sum(d2))
    line_out = {}
    for n, (lam, Eph) in LINES.items():
        dE = Eph * 2.0 * W_ANG / lam  # ±80 Å → 能量窗
        # 光子能量 = E_j - E2_avg ∈ Eph ± dE
        mask = np.abs((vals - E2_avg) - Eph) < dE
        s_win = float(np.sum(d2[mask]))
        line_out[str(n)] = {"s_win": s_win, "n_in": int(np.sum(mask))}
    results.append({"B_au": B, "B_MG": B*2350.0, "E2_avg": float(E2_avg),
                    "total_d2": total_d2, "n2_idx": [int(x) for x in i2],
                    "lines": line_out})
    print("  total_d2=%.4e | Hα %.3e Hβ %.3e Hγ %.3e Hδ %.3e Hε %.3e" % (
        total_d2, line_out["3"]["s_win"], line_out["4"]["s_win"],
        line_out["5"]["s_win"], line_out["6"]["s_win"], line_out["7"]["s_win"]), flush=True)

# TRK 守恒自检 + 相对保留
ref_total = results[0]["total_d2"]
print("\n=== TRK 守恒自检：total_d2 / 参考 ===", flush=True)
for res in results:
    print("  B=%6.1f MG: %.3f" % (res["B_MG"], res["total_d2"]/ref_total), flush=True)
print("\n=== S_win 相对保留（以 0.2MG 参考归一）===", flush=True)
ref_lines = results[0]["lines"]
for res in results[1:]:
    line = "B=%6.1f MG |" % res["B_MG"]
    for n in (3,4,5,6,7):
        r0 = ref_lines[str(n)]["s_win"]
        v = res["lines"][str(n)]["s_win"]
        line += " %s %5.1f%%" % ({3:"Hα",4:"Hβ",5:"Hγ",6:"Hδ",7:"Hε"}[n], 100*v/r0 if r0>1e-30 else 0)
    print(line, flush=True)

with io.open(os.path.join(BASE, "_gaia_abs", "paperX_osc_pi_m0_v3.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("\nwritten paperX_osc_pi_m0_v3.json")
