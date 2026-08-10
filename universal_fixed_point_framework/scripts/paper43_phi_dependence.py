#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D_plateau 的 φ 依赖性验证：L=16, D=2.6, φ∈{0.20,0.25,0.31,0.35,0.40}。"""
import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paper43_coupled_spectral_dip as m
import numpy as np

L = 16
D = 2.6
PHI_LIST = [0.20, 0.25, 0.31, 0.35, 0.40]
N_CFG = 3

results = {}
print("=" * 60)
print(f"D_plateau φ 依赖性验证 (L={L}, D={D}, N_CFG={N_CFG})")
print("=" * 60)

for phi in PHI_LIST:
    Db_red_list = []
    Db_bb_list = []
    for cfg in range(N_CFG):
        binary, radii, lambdas, U = m.fractal_pore_network(L, phi, D, seed=cfg*1000)
        P_arr, S_arr, P_c, S_c, order, Uf = m.run_fractal_dip(binary, U, c=0.0, seed=cfg*1000)
        if P_c <= 0 or P_c > 1e6:
            continue
        pressures, A_t, lam_edges, snapshots = m.spectral_band_mapping(
            binary, lambdas, P_arr, P_c, Uf)
        idx = np.argmin(np.abs(pressures - P_c))
        cluster = snapshots[idx]
        if not cluster.any():
            continue
        _, _, Db_b, _, _, _, Db_rd, _ = m.extract_p3(snapshots, pressures, P_c)
        if not np.isnan(Db_rd):
            Db_red_list.append(Db_rd)
            Db_bb_list.append(Db_b)
    
    results[phi] = {
        'Db_red_mean': float(np.mean(Db_red_list)) if Db_red_list else float('nan'),
        'Db_red_std': float(np.std(Db_red_list)) if Db_red_list else float('nan'),
        'Db_bb_mean': float(np.mean(Db_bb_list)) if Db_bb_list else float('nan'),
        'n_valid': len(Db_red_list),
    }
    r = results[phi]
    print(f"  φ={phi:.2f}: D_b(red)={r['Db_red_mean']:.3f}±{r['Db_red_std']:.3f}  D_b(bb)={r['Db_bb_mean']:.3f}  n={r['n_valid']}", flush=True)

print("\n" + "=" * 60)
print("结论")
print("=" * 60)
Db_vals = [results[p]['Db_red_mean'] for p in PHI_LIST if not np.isnan(results[p]['Db_red_mean'])]
if len(Db_vals) >= 2:
    Db_range = max(Db_vals) - min(Db_vals)
    Db_mean = np.mean(Db_vals)
    cv = Db_range / Db_mean if Db_mean > 0 else float('nan')
    print(f"D_b(red) 范围: {min(Db_vals):.3f} - {max(Db_vals):.3f}")
    print(f"变异系数 (range/mean): {cv:.4f}")
    if cv < 0.05:
        print("✓ D_plateau 与 φ 无关（变异系数 < 5%）→ 普适性确认")
    else:
        print("✗ D_plateau 对 φ 有依赖（变异系数 ≥ 5%）→ 非普适")

save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'paper43_phi_dependence.json')
with open(save_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, default=str)
print(f"\n结果已保存: {save_path}")
