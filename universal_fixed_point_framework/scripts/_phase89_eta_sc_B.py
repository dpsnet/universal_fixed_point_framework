# -*- coding: utf-8 -*-
"""Phase 89 M89-1 最终版：η_sc(B) 曲线（§3.5 收敛检验口径——全谱 + (0.95-D2)/0.45）
B: 0.001-0.5 a.u.（覆盖观测中场 10-100 MG 全域 = 0.043-0.425 a.u.）
输出：paperX_eta_sc_B2d.json + 控制台表（含压制因子与观测对照）"""
import json, os, time
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import warnings
warnings.filterwarnings('ignore')

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def hamiltonian_2d_hydrogen(N_r, r_max, m, B):
    """论文式 3.4 口径（m^2 离心项 + Landau 项）：(m + B r^2/2)^2/(2r^2) - 1/r，半偏移网格"""
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

def compute_d2(lambdas, n_scales=30, eps_min_frac=1e-4, eps_max_frac=0.5):
    if len(lambdas) < 50:
        return 0.5, 0.0
    lam = np.array(lambdas, dtype=np.float64)
    lam_min, lam_max = lam.min(), lam.max()
    if lam_max <= lam_min:
        return 0.5, 0.0
    lam_n = (lam - lam_min) / (lam_max - lam_min)
    N = len(lam_n)
    if N > 5000:
        idx = np.random.choice(N, 5000, replace=False)
        lam_n = lam_n[idx]; N = 5000
    diffs = np.abs(lam_n[:, None] - lam_n[None, :])
    iu = np.triu_indices(N, k=1)
    dists = diffs[iu]
    dists = dists[dists > 1e-18]
    if len(dists) < 100:
        return 0.5, 0.0
    eps_min = max(eps_min_frac, dists.min() * 2)
    eps_max = min(eps_max_frac, dists.max() * 0.5)
    if eps_min >= eps_max:
        eps_min, eps_max = dists.min() * 2, dists.max() * 0.5
    eps_list = np.logspace(np.log10(eps_min), np.log10(eps_max), n_scales)
    C2 = np.array([np.sum(dists < eps) / len(dists) for eps in eps_list])
    mask = (C2 > 1e-4) & (C2 < 0.8)
    if mask.sum() < 5:
        return 0.5, 0.0
    log_eps = np.log10(eps_list[mask])
    log_C2 = np.log10(C2[mask])
    try:
        coeffs = np.polyfit(log_eps, log_C2, 1)
        D2 = float(np.clip(coeffs[0], 0.0, 2.0))
        y_pred = coeffs[0] * log_eps + coeffs[1]
        ss_res = np.sum((log_C2 - y_pred) ** 2)
        ss_tot = np.sum((log_C2 - np.mean(log_C2)) ** 2)
        r_sq = 1.0 - ss_res / ss_tot if ss_tot > 1e-12 else 0.0
        return D2, float(r_sq)
    except Exception:
        return 0.5, 0.0

def partial_spectrum(N_r, r_max, m, B, k=400):
    H = hamiltonian_2d_hydrogen(N_r, r_max, m, B)
    for attempt in range(3):
        try:
            vals, _ = eigsh(H.astype(np.float64), k=min(k, N_r - 5),
                            which='LM', sigma=-0.5, maxiter=50000, tol=1e-8)
            vals = np.real(vals)
            vals = vals[(vals > -5.0) & (vals < 10.0)]
            return sorted(vals)
        except Exception:
            continue
    return []

def scan_B(Bs, N_r=1500, r_max=60.0, m_max=8, k_per_m=400):
    out = []
    for B in Bs:
        t0 = time.time()
        lambdas = []
        for m in range(-m_max, m_max + 1):
            lambdas.extend(partial_spectrum(N_r, r_max, m, B, k_per_m))
        lambdas = np.sort(np.array(lambdas, dtype=np.float64))
        n = len(lambdas)
        if n < 100:
            D2, r2, eta = 0.5, 0.0, 0.0
        else:
            D2, r2 = compute_d2(lambdas)
            eta = max(0.0, min(1.0, (0.95 - D2) / 0.45))
        rec = {"B_au": B, "B_T": B * 2.35e5, "B_MG": B * 2.35e5 / 1e6,
               "n_states": n, "D2": D2, "r_sq": r2, "eta_sc": eta,
               "suppress": 1.0 - eta, "t_sec": round(time.time() - t0, 1)}
        out.append(rec)
        print("B=%6.3f au (%6.2f MG) n=%4d D2=%.4f (R2=%.3f) eta_sc=%.4f 抑制因子=%.4f [%.0fs]" % (
            B, B * 2.35e5 / 1e6, n, D2, r2, eta, rec["suppress"], rec["t_sec"]), flush=True)
    return out

if __name__ == "__main__":
    Bs = [0.001, 0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]
    res = scan_B(Bs)
    with open(os.path.join(BASE, "_gaia_abs", "paperX_eta_sc_B2d.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print("\nwritten paperX_eta_sc_B2d.json")
