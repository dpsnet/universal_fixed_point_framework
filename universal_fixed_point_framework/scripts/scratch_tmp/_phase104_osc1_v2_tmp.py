# -*- coding: utf-8 -*-
"""Phase 104az-59 v2：π 通道振子强度保留份额 S_pi(n,B)（m=0 3D 氢）——投影归类版
- 零场参考态（B=0.0001）解出后按能量窗识别 n=2,3,4,5,6,7 各态（窗 ±0.05）
- 每个 B 解态后：投影归类 <psi_B | ref> 最大者 → 属于该 n
- S_pi(n,B) = Σ_{j∈n(B)} |<ref_2s + ref_2pz| z | psi_j>|² / 零场总
- 归一化修正：eigsh 欧几里得归一 ≠ 加权内积——D 乘以修正因子（用参考态自检）
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

def solve(N_r, r_max, N_z, z_max, m, B, k=200, sigma=-0.08):
    H, r, zk = hamiltonian_3d(N_r, r_max, N_z, z_max, m, B)
    vals, vecs = eigsh(H.astype(np.float64), k=min(k, H.shape[0]-2),
                       which='LM', sigma=sigma, maxiter=60000, tol=1e-8)
    idx = np.argsort(vals)
    return vals[idx], vecs[:, idx], r, zk

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
N_r, r_max, N_z, z_max = 80, 50.0, 80, 50.0
dr, dz = r_max/N_r, z_max/N_z
W = 0.05  # 能量窗

def identify_ref(vals, vecs):
    """零场参考态：按能量窗归类 n=2..7（m=0 每 n 有 n 个态）"""
    refs = {}
    for n in range(2, 8):
        En = -1.0/(2.0*n*n)
        idx = np.where(np.abs(vals - En) < W)[0]
        # 取最接近的 n 个（按能量排序取前 n 个）
        idx = idx[np.argsort(np.abs(vals[idx] - En))][:n]
        refs[n] = idx
    return refs

def z_matrix(vecs, r, zk, idxs):
    """z 偶极矩阵元（m 不变，π 通道）：只算 idxs 间的——idxs 是状态索引列表"""
    k = len(idxs)
    D = np.zeros((k, k))
    for a in range(k):
        pa = vecs[:, idxs[a]].reshape(N_r, N_z)
        for b in range(a, k):
            pb = vecs[:, idxs[b]].reshape(N_r, N_z)
            val = dr * dz * np.sum(r[:, None] * pa * pb * zk[None, :])
            D[a, b] = D[b, a] = val
    return D

def run(B_au):
    vals, vecs, r, zk = solve(N_r, r_max, N_z, z_max, m=0, B=B_au)
    refs = identify_ref(vals, vecs)
    # 归一化自检：加权范数 <psi|psi>_w = sum |psi|^2 r dr dz——应为 1（连续）；离散偏离给出修正
    norm2 = {}
    for n, idxs in refs.items():
        for i in idxs:
            psi = vecs[:, i].reshape(N_r, N_z)
            norm2[i] = dr * dz * np.sum(r[:, None] * psi**2)
    out = {"B_au": B_au, "B_MG": B_au*2350.0, "n2_idx": [int(x) for x in refs[2]],
           "refs": {str(n): [int(x) for x in idxs] for n, idxs in refs.items()},
           "norm2": {str(i): float(norm2[i]) for i in norm2}}
    return out, vals, vecs, r, zk

# 主流程：先解 B=0.0001 参考，再各 B 投影
print("=== v2 π 通道 m=0：投影归类振子强度保留份额 ===", flush=True)
B_list = (0.0001, 0.005, 0.01, 0.02, 0.05, 0.1)
solutions = {}
for B in B_list:
    print("B=%.4f a.u. (%.1f MG) 求解..." % (B, B*2350), flush=True)
    out, vals, vecs, r, zk = run(B)
    solutions[B] = (out, vals, vecs)
    print("   n2 态数=%d, n3=%d n4=%d n5=%d n6=%d n7=%d" % (
        len(out["refs"]["2"]), len(out["refs"]["3"]), len(out["refs"]["4"]),
        len(out["refs"]["5"]), len(out["refs"]["6"]), len(out["refs"]["7"])), flush=True)

# 参考态（B=0.0001）：2s/2p_z 组合——取 n=2 流形整体（2 态）
ref_out, ref_vals, ref_vecs = solutions[0.0001]
n2_ref = ref_out["n2_idx"]
print("\n参考 n=2 流形 idx=%s (E=%.4f, %.4f)" % (n2_ref, ref_vals[n2_ref[0]], ref_vals[n2_ref[1]]), flush=True)

# 各 B：投影归类上态 + 偶极强度
print("\n=== S_pi(n,B) 相对强度（以 B=0.0001 为参考归一）===", flush=True)
results = []
for B in B_list:
    out, vals, vecs = solutions[B]
    refs = out["refs"]
    # 参考态 n=2 组合向量（加权归一化）：先对参考 2s/2p_z 做正交化?——简并组合任意——用整体 D 更稳
    # 直接：对每个 B 的 n=2 态与上态算 z 偶极——绝对 d2 用 norm2 修正后相对比较
    n2_idxs = refs["2"]
    D_n2 = z_matrix(vecs, r, zk, n2_idxs)  # n2×n2（π 内 n=2 自耦合——非 Balmer）
    # 与上态：需要全向量矩阵——算 n2 × (所有态) 的偶极——用全 k
    k = vecs.shape[1]
    d2_line = {}
    for n in (3,4,5,6,7):
        up = refs[str(n)]
        if len(up) == 0:
            d2_line[str(n)] = 0.0
            continue
        tot = 0.0
        for i in n2_idxs:
            pi = vecs[:, i].reshape(N_r, N_z)
            for j in up:
                pj = vecs[:, j].reshape(N_r, N_z)
                val = dr * dz * np.sum(r[:, None] * pi * pj * zk[None, :])
                tot += val**2
        d2_line[str(n)] = float(tot)
    results.append({"B_au": B, "B_MG": B*2350.0, "n2_idx": [int(x) for x in n2_idxs],
                    "S_pi_abs": d2_line})
    print("B=%6.1f MG | Hα %9.3e Hβ %9.3e Hγ %9.3e Hδ %9.3e Hε %9.3e" % (
        B*2350, d2_line["3"], d2_line["4"], d2_line["5"], d2_line["6"], d2_line["7"]), flush=True)

# 相对保留份额
ref = results[0]["S_pi_abs"]
print("\n=== 相对保留份额 S_pi(n,B)/S_pi(n,0.2MG) ===", flush=True)
for res in results[1:]:
    line = "B=%6.1f MG |" % res["B_MG"]
    for n in (3,4,5,6,7):
        r0 = ref[str(n)]
        v = res["S_pi_abs"][str(n)]
        line += " %s %5.1f%%" % ({3:"Hα",4:"Hβ",5:"Hγ",6:"Hδ",7:"Hε"}[n], 100*v/r0 if r0 > 0 else 0)
    print(line, flush=True)

with io.open(os.path.join(BASE, "_gaia_abs", "paperX_osc_pi_m0_v2.json"), "w", encoding="utf-8") as f:
    json.dump({"results": results, "ref": ref}, f, ensure_ascii=False, indent=1)
print("\nwritten paperX_osc_pi_m0_v2.json")
