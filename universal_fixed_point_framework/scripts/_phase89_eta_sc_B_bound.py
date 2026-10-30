# -*- coding: utf-8 -*-
"""Phase 89 M89-1 修正：束缚态衰减口径 η_sc(B)
物理定义：η_sc = 1 - N_bound(B)/N_bound(B_ref)——束缚态（可辐射跃迁通道）被奇异连续谱化的比例
- 论文表 3.2.2 态数锚：0.001→303, 0.01→300, 0.05→152, 0.1→69, 0.2→33（B_ref=0.001 a.u.=0.235 MG）
- 补算中间点（0.005/0.02/0.03/0.04/0.06/0.08/0.15）束缚态计数（SA 最低态，同口径相对衰减校验）
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
    """最低 k 态中 E<0 计数（SA——保留深束缚态）"""
    H = hamiltonian_2d_hydrogen(N_r, r_max, m, B)
    try:
        vals, _ = eigsh(H.astype(np.float64), k=min(k, N_r - 5),
                        which='SA', maxiter=50000, tol=1e-9)
        return int(np.sum(np.real(vals) < 0))
    except Exception:
        return 0

def scan_bound(Bs, N_r=1500, r_max=60.0, m_max=8, k=300):
    out = []
    for B in Bs:
        t0 = time.time()
        tot = 0
        per_m = []
        for m in range(-m_max, m_max + 1):
            nb = n_bound(N_r, r_max, m, B, k)
            per_m.append(nb)
            tot += nb
        out.append({"B_au": B, "B_T": B * 2.35e5, "B_MG": B * 2.35e5 / 100.0,
                    "n_bound": tot, "per_m": per_m, "t_sec": round(time.time() - t0, 1)})
        print("B=%6.3f au (%8.0f T = %7.1f MG) 束缚态=%3d [%.0fs]" % (
            B, B * 2.35e5, B * 2.35e5 / 100.0, tot, out[-1]["t_sec"]), flush=True)
    return out

if __name__ == "__main__":
    Bs = [0.001, 0.005, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1, 0.15, 0.2, 0.3, 0.4]
    res = scan_bound(Bs)
    with open(os.path.join(BASE, "_gaia_abs", "paperX_eta_sc_B_bound.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print("written paperX_eta_sc_B_bound.json")
