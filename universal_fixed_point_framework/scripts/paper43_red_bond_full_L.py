# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全 L 范围红键仿真（Tarjan 桥边算法）：L∈{16,32,48,64,96,128,256}。

D∈{2.4,3.0}, c=0, N_CFG=3
目标：验证 D_b(red) 的 L 依赖性和 D 依赖性
"""
import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paper43_coupled_spectral_dip as m
import numpy as np

PHI = 0.31
C_VAL = 0.0
L_VALUES = [16, 32, 48, 64, 96, 128, 256]
D_VALUES = [2.4, 3.0]
N_CFG = 3

results = {}

for L in L_VALUES:
    print(f"\n{'='*60}")
    print(f"L = {L}")
    print(f"{'='*60}")
    results[L] = {}
    
    for D in D_VALUES:
        Db_red_list = []
        n_red_list = []
        P_c_list = []
        
        for cfg in range(N_CFG):
            t0 = time.time()
            binary, radii, lambdas, U = m.fractal_pore_network(L, PHI, D, seed=cfg*1000)
            P_arr, S_arr, P_c, S_c, order, Uf = m.run_fractal_dip(binary, U, c=C_VAL, seed=cfg*1000)
            if P_c <= 0 or P_c > 1e6:
                continue
            
            pressures, A_t, lam_edges, snapshots = m.spectral_band_mapping(
                binary, lambdas, P_arr, P_c, Uf)
            idx = np.argmin(np.abs(pressures - P_c))
            cluster = snapshots[idx]
            if not cluster.any():
                continue
            
            # 骨架 + Tarjan 红键（大 L 用快速 BFS 骨架提取）
            if L <= 128:
                backbone = m.extract_backbone(cluster)
            else:
                backbone = m.extract_backbone_fast(cluster)
            if not backbone.any():
                continue

            red = m.extract_red_bonds_tarjan(cluster, backbone=backbone)
            n_red = int(red.sum())
            
            if n_red > 0:
                Db_red, _ = m.box_counting_3d(red)
                Db_red_list.append(float(Db_red))
                n_red_list.append(n_red)
                P_c_list.append(float(P_c))
            
            elapsed = time.time() - t0
            print(f"  D={D} cfg={cfg}: P_c={P_c:.4f} n_red={n_red} D_b={Db_red:.3f} t={elapsed:.1f}s", flush=True)
        
        results[L][D] = {
            'Db_red_mean': float(np.mean(Db_red_list)) if Db_red_list else float('nan'),
            'Db_red_std': float(np.std(Db_red_list)) if Db_red_list else float('nan'),
            'Db_red_list': Db_red_list,
            'n_red_mean': float(np.mean(n_red_list)) if n_red_list else 0,
            'P_c_mean': float(np.mean(P_c_list)) if P_c_list else float('nan'),
            'n_valid': len(Db_red_list),
        }

# 汇总
print(f"\n{'='*60}")
print("汇总：D_b(red) vs L")
print(f"{'='*60}")
print(f"{'L':>5} {'D=2.4 mean':>12} {'D=2.4 std':>10} {'D=3.0 mean':>12} {'D=3.0 std':>10}")
print("-" * 55)
for L in L_VALUES:
    r24 = results[L][2.4]
    r30 = results[L][3.0]
    print(f"{L:5d} {r24['Db_red_mean']:12.3f} {r24['Db_red_std']:10.3f} {r30['Db_red_mean']:12.3f} {r30['Db_red_std']:10.3f}")

# 保存
save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'paper43_red_bond_full_L.json')
with open(save_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, default=str)
print(f"\n结果已保存: {save_path}")
