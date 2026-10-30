# -*- coding: utf-8 -*-
"""Phase 104az-59 ★★★ 决定性计算 v0：π 通道振子强度保留份额 S_pi(n,B)（m=0 3D 氢）
KIMI 建议的"从混合态本征解算振子强度分布"最小可行版：
- m=0 分波（π 通道，Δm=0，z 偶极）
- 解 3D 柱坐标氢本征态（含向量），按零场能量窗归类 Balmer 上态
- S_pi(n,B) = 窗口内上态 π 偶极强度 / 零场总 π 偶极强度
- 判别：S_pi 保留高（>0.7）→ 中场"π 中心深度下降"不能归因标准 l-混合 π 稀释 → 支持禁戒
        S_pi 大幅降 → 标准可解释 → 论文归因需修正
注意：σ 通道（m=±1）后续单独算；本版为 π 通道先行（观测 §4.9 π 分量系统性消失的关键判别）
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

def solve(N_r, r_max, N_z, z_max, m, B, k=140):
    H, r, zk = hamiltonian_3d(N_r, r_max, N_z, z_max, m, B)
    vals, vecs = eigsh(H.astype(np.float64), k=min(k, H.shape[0]-2),
                       which='LM', sigma=-0.12, maxiter=60000, tol=1e-8)
    # sigma 附近排序
    idx = np.argsort(vals)
    return vals[idx], vecs[:, idx], r, zk

def z_matrix(vecs, r, zk, N_r, N_z):
    """z 偶极矩阵元（m 不变，π 通道）：<a|z|b> 按状态指标"""
    # 每个态 psi = vecs[:,i] 形状 (N_r*N_z)——reshape (N_r, N_z)
    k = vecs.shape[1]
    D = np.zeros((k, k))
    for a in range(k):
        pa = vecs[:, a].reshape(N_r, N_z)
        for b in range(a, k):
            pb = vecs[:, b].reshape(N_r, N_z)
            val = dr * dz * np.sum(r[:, None] * pa * pb * zk[None, :])
            D[a, b] = D[b, a] = val
    return D

dr = dz = None  # 全局供 z_matrix 用

def run(B_au, N_r=70, r_max=45.0, N_z=70, z_max=45.0):
    global dr, dz
    dr = r_max / N_r; dz = z_max / N_z
    vals, vecs, r, zk = solve(N_r, r_max, N_z, z_max, m=0, B=B_au, k=120)
    # 零场参考能量：E_n = -1/(2n^2) au
    E2 = -1.0/8.0   # n=2
    # 识别 n=2 流形（m=0：2s + 2p_z）
    i2 = np.where(np.abs(vals - E2) < 0.012)[0]
    if len(i2) < 1:
        print("  [WARN] B=%.3f n=2 流形未识别 len=%d" % (B_au, len(i2)), flush=True)
        i2 = np.where(np.abs(vals - E2) < 0.03)[0]
    # Balmer 上态能量窗（n=3..7）
    wins = {}
    for n in (3, 4, 5, 6, 7):
        En = -1.0/(2.0*n*n)
        wins[n] = np.where(np.abs(vals - En) < 0.012)[0]
    # π 偶极强度：D_z[i2, up] 平方
    D = z_matrix(vecs, r, zk, N_r, N_z)
    out = {"B_au": B_au, "B_MG": B_au*2350.0, "E2_idx": i2.tolist(), "per_line": {}}
    for n, idxs in wins.items():
        if len(idxs) == 0:
            out["per_line"][str(n)] = {"n_up": 0, "S_pi": 0.0, "d2": 0.0}
            continue
        d2 = np.sum(D[np.ix_(i2, idxs)]**2)
        out["per_line"][str(n)] = {"n_up": int(len(idxs)), "d2": float(d2)}
    # 零场参考（B=0.0001 近似）单独传——用 d2 比值需要外部参考
    return out

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
results = []
print("=== π 通道 m=0 3D 氢：Balmer 上态偶极强度（绝对 d2，零场参考另算）===", flush=True)
for B in (0.0001, 0.005, 0.01, 0.02, 0.05, 0.1):
    print("B=%.4f a.u. (%.1f MG)..." % (B, B*2350), flush=True)
    try:
        out = run(B)
        results.append(out)
        pl = out["per_line"]
        print("   n=3 d2=%.3e n_up=%d | n=4 d2=%.3e n_up=%d | n=5 d2=%.3e n_up=%d | n=6 d2=%.3e n_up=%d | n=7 d2=%.3e n_up=%d" % (
            pl.get("3",{}).get("d2",0), pl.get("3",{}).get("n_up",0),
            pl.get("4",{}).get("d2",0), pl.get("4",{}).get("n_up",0),
            pl.get("5",{}).get("d2",0), pl.get("5",{}).get("n_up",0),
            pl.get("6",{}).get("d2",0), pl.get("6",{}).get("n_up",0),
            pl.get("7",{}).get("d2",0), pl.get("7",{}).get("n_up",0)), flush=True)
    except Exception as e:
        print("  [ERR] B=%.3f: %s" % (B, str(e)[:120]), file=sys.stderr, flush=True)
with io.open(os.path.join(BASE, "_gaia_abs", "paperX_osc_pi_m0.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("written paperX_osc_pi_m0.json")
