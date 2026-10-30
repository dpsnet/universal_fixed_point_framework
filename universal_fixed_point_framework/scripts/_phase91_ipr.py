# -*- coding: utf-8 -*-
"""Phase 91 M91-1/2：2D 氢原子奇异连续谱直接谱分解（IPR 盒子标度）
内嵌 hamiltonian_2d_hydrogen（环境缺 PIL，不 import paper48_convergence）
- 对 B/m 组合求正能区本征态，计算 IPR（径向加权）
- r_max 变化（L 标度，dr 固定）→ D2 谱维数 = -dlog(IPR)/dlog(L)
"""
import json, io, os, sys
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

def get_positive_states(N_r, r_max, m, B, emin=0.0, emax=3.0, k=120):
    H, r = hamiltonian_2d_hydrogen(N_r, r_max, m, B)
    try:
        vals, vecs = eigsh(H.astype(np.float64), k=min(k, N_r - 5),
                           which='LM', sigma=1.0, maxiter=30000, tol=1e-9)
    except Exception:
        try:
            vals, vecs = eigsh(H.astype(np.float64), k=min(k, N_r - 5),
                               which='LM', sigma=0.5, maxiter=30000, tol=1e-9)
        except Exception:
            return []
    vals = np.real(vals)
    sel = [(v, vecs[:, i]) for i, v in enumerate(vals) if emin <= v <= emax]
    return [(v, psi) for v, psi in sorted(sel, key=lambda x: x[0])]

def ipr_radial(psi, r, dr):
    """径向加权参与比：IPR = (Σ|ψ|⁴ r dr) / (Σ|ψ|² r dr)²"""
    w = psi * np.sqrt(r * dr)  # 归一化到 ∫|ψ|² r dr = 1
    w = w / np.sqrt(np.sum(np.abs(w)**2))
    return float(np.sum(np.abs(w)**4))

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
DR = 0.1
results = []
for B in (0.01, 0.05, 0.1):
    for m in (0, 1, 2):
        scales = []
        for r_max in (60.0, 120.0, 240.0):
            N_r = int(r_max / DR)
            sts = get_positive_states(N_r, r_max, m, B, emin=0.0, emax=3.0, k=150)
            if not sts:
                scales.append(None)
                continue
            iprs = [ipr_radial(psi, np.arange(N_r) * DR + DR / 2, DR) for _, psi in sts[:15]]
            scales.append(float(np.median(iprs)))
        rec = {"B": B, "m": m, "scales": scales, "L": [60, 120, 240]}
        # D2 谱维数（用最后两档 L）
        if scales[1] and scales[2] and scales[1] > 0 and scales[2] > 0:
            D2 = -np.log(scales[2] / scales[1]) / np.log(240.0 / 120.0)
            rec["D2"] = float(D2)
        else:
            rec["D2"] = None
        results.append(rec)
        print("B=%.2f m=%d IPR(L=60/120/240)=%s D2=%s" % (
            B, m, ["%.3g" % s if s else "—" for s in scales],
            "%.3f" % rec["D2"] if rec["D2"] is not None else "—"), flush=True)

with io.open(os.path.join(BASE, "_gaia_abs", "paperX_spectrum_ipr.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("written paperX_spectrum_ipr.json")
