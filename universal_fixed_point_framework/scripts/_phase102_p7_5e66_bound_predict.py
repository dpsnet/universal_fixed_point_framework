# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-66：束缚态谱框架量预言的先验检验
================================================================
用与 _phase89_eta_sc_B_bound.py 完全相同的参数（N_r=1500, r_max=60, m_max=8, k=300）
重算 3 个新场强点的束缚态数——检验 P7-5e-65 可检验预言：
- B_au=0.07（164.5 MG）→ 若框架量序列真 → 15 或 14（16→13 之间插入）
- B_au=0.25（587.5 MG）→ 若框架量序列真 → 10 或 9（11→7 之间插入；10 = 配置基数）
- B_au=0.45（1057.5 MG）→ 若框架量序列真 → 4 或 3（5 之后继续）
若结果无序 → 预言失败 → 诚实撤回（先算再写）
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
    """最低 k 态中 E<0 计数（SA——保留深束缚态）——同 phase89 口径"""
    H = hamiltonian_2d_hydrogen(N_r, r_max, m, B)
    try:
        vals, _ = eigsh(H.astype(np.float64), k=min(k, N_r - 5),
                        which='SA', maxiter=50000, tol=1e-9)
        return int(np.sum(np.real(vals) < 0))
    except Exception:
        return 0

print("="*104)
print("P7-5e-66：束缚态谱框架量预言的先验检验（同参数重算新场强点）")
print("="*104)

Bs_new = [0.07, 0.25, 0.45]
predictions = {0.07: "15 或 14（若 16→13 间插入）", 0.25: "10 或 9（若 11→7 间插入——10=配置基数）", 0.45: "4 或 3（若 5 后继续）"}

out = []
for B in Bs_new:
    t0 = time.time()
    tot = 0
    per_m = []
    for m in range(-8, 9):
        nb = n_bound(1500, 60.0, m, B)
        per_m.append(nb)
        tot += nb
    out.append({"B_au": B, "B_MG": B * 2350.0, "n_bound": tot, "per_m": per_m, "t_sec": round(time.time() - t0, 1)})
    pred = predictions[B]
    print("B=%5.2f au (%5.1f MG)  束缚态=%d   [预言 %s]  [%.0fs]" % (B, B*2350.0, tot, pred, out[-1]["t_sec"]), flush=True)

print()
print("【裁决】")
print("-"*104)
for r in out:
    B, n = r["B_au"], r["n_bound"]
    pred = predictions[B]
    if B == 0.07:
        verdict = "★ 命中候选" if n in (14, 15) else ("接近" if n in (13, 16) else "预言失败")
    elif B == 0.25:
        verdict = "★ 命中候选" if n in (9, 10) else ("接近" if n in (8, 11) else "预言失败")
    else:
        verdict = "★ 命中候选" if n in (3, 4) else ("接近" if n in (2, 5) else "预言失败")
    print("B=%.2f au → n=%d → %s（预言 %s）" % (B, n, verdict, pred))

json.dump(out, open(os.path.join(BASE, "_phase102_p7_5e66_bound_predict.json"), "w", encoding="utf-8"), indent=1)
print()
print("JSON 落盘 ✓  exit 0")
