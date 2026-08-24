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
"""验证 Tarjan 桥边算法的正确性和速度。"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paper43_coupled_spectral_dip as m
import numpy as np

print("=" * 60)
print("Tarjan 桥边算法验证")
print("=" * 60)

# L=16 验证正确性
L = 16
D = 2.6
phi = 0.31

for seed in [0, 1000, 2000]:
    binary, radii, lambdas, U = m.fractal_pore_network(L, phi, D, seed=seed)
    P_arr, S_arr, P_c, S_c, order, Uf = m.run_fractal_dip(binary, U, c=0.0, seed=seed)
    pressures, A_t, lam_edges, snapshots = m.spectral_band_mapping(
        binary, lambdas, P_arr, P_c, Uf)
    idx = np.argmin(np.abs(pressures - P_c))
    cluster = snapshots[idx]
    if not cluster.any():
        continue
    
    backbone = m.extract_backbone(cluster)
    
    # 旧算法（per-candidate BFS）
    t0 = time.time()
    red_old = m.extract_red_bonds(cluster, backbone=backbone)
    t_old = time.time() - t0
    n_old = red_old.sum()
    
    # 新算法（Tarjan 桥边）
    t0 = time.time()
    red_new = m.extract_red_bonds_tarjan(cluster, backbone=backbone)
    t_new = time.time() - t0
    n_new = red_new.sum()
    
    # 对比
    overlap = (red_old & red_new).sum()
    old_only = (red_old & ~red_new).sum()
    new_only = (~red_old & red_new).sum()
    
    print(f"\nseed={seed}: P_c={P_c:.4f}")
    print(f"  旧算法: n_red={n_old} t={t_old:.3f}s")
    print(f"  Tarjan: n_red={n_new} t={t_new:.3f}s")
    print(f"  加速比: {t_old/t_new:.1f}x" if t_new > 0 else "  加速比: N/A")
    print(f"  重叠: {overlap}, 旧独有: {old_only}, 新独有: {new_only}")
    
    # 盒计数对比
    if n_old > 0 and n_new > 0:
        Db_old, _ = m.box_counting_3d(red_old)
        Db_new, _ = m.box_counting_3d(red_new)
        print(f"  D_b(red) 旧={Db_old:.3f} 新={Db_new:.3f} 差={abs(Db_old-Db_new):.4f}")

# L=128 速度测试
print(f"\n{'='*60}")
print("L=128 速度测试")
print(f"{'='*60}")

L = 128
for D in [2.4, 3.0]:
    binary, radii, lambdas, U = m.fractal_pore_network(L, phi, D, seed=0)
    P_arr, S_arr, P_c, S_c, order, Uf = m.run_fractal_dip(binary, U, c=0.0, seed=0)
    pressures, A_t, lam_edges, snapshots = m.spectral_band_mapping(
        binary, lambdas, P_arr, P_c, Uf)
    idx = np.argmin(np.abs(pressures - P_c))
    cluster = snapshots[idx]
    if not cluster.any():
        continue
    
    t0 = time.time()
    backbone = m.extract_backbone(cluster)
    t_bb = time.time() - t0
    
    t0 = time.time()
    red = m.extract_red_bonds_tarjan(cluster, backbone=backbone)
    t_red = time.time() - t0
    
    n_red = red.sum()
    n_bb = backbone.sum()
    n_cluster = cluster.sum()
    
    Db_red = float('nan')
    if red.any():
        Db_red, r2_red = m.box_counting_3d(red)
    
    print(f"D={D}: P_c={P_c:.4f} n_cluster={n_cluster} n_bb={n_bb} n_red={n_red}")
    print(f"  t_backbone={t_bb:.1f}s t_tarjan={t_red:.1f}s D_b(red)={Db_red:.3f}")
