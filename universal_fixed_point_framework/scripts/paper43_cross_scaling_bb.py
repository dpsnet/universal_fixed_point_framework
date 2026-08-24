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
"""多 L 骨架仿真：验证 D_b(backbone) 的有限尺寸标度。

L ∈ {16, 32, 48, 64, 96, 128, 256}，D ∈ {2.4, 3.0}，c=0，N_CFG=1
仅做 DIP + 骨架提取（跳过红键，计算量可控）。
"""
import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paper43_coupled_spectral_dip as m
import numpy as np

PHI = 0.31
C_VAL = 0.0
L_VALUES = [16, 32, 48, 64, 96, 128, 256]
D_VALUES = [2.4, 3.0]

results = {}

for L in L_VALUES:
    print(f"\n{'='*50}")
    print(f"L = {L}")
    print(f"{'='*50}")
    results[L] = {}
    
    for D in D_VALUES:
        print(f"  D={D} ...", end=" ", flush=True)
        t0 = time.time()
        
        binary, radii, lambdas, U = m.fractal_pore_network(L, PHI, D, seed=0)
        P_arr, S_arr, P_c, S_c, order, Uf = m.run_fractal_dip(binary, U, c=C_VAL, seed=0)
        
        pressures, A_t, lam_edges, snapshots = m.spectral_band_mapping(
            binary, lambdas, P_arr, P_c, Uf)
        idx = np.argmin(np.abs(pressures - P_c))
        cluster = snapshots[idx]
        
        r = {'P_c': float(P_c), 'S_c': float(S_c)}
        
        if cluster.any():
            backbone = m.extract_backbone(cluster)
            if backbone.any():
                Db_bb, r2_bb = m.box_counting_3d(backbone)
                r['Db_backbone'] = float(Db_bb)
                r['r2_backbone'] = float(r2_bb)
                r['bb_fraction'] = float(backbone.sum() / cluster.sum())
            else:
                r['Db_backbone'] = float('nan')
                r['bb_fraction'] = 0.0
        else:
            r['Db_backbone'] = float('nan')
        
        r['elapsed'] = time.time() - t0
        results[L][D] = r
        print(f"P_c={P_c:.4f} Db_bb={r['Db_backbone']:.3f} t={r['elapsed']:.0f}s", flush=True)

# 汇总
print(f"\n{'='*50}")
print("汇总：D_b(backbone) vs L")
print(f"{'='*50}")
print(f"{'L':>5} {'D=2.4':>10} {'bb_frac':>8} {'D=3.0':>10} {'bb_frac':>8}")
print("-" * 50)
for L in L_VALUES:
    r24 = results[L][2.4]
    r30 = results[L][3.0]
    print(f"{L:5d} {r24['Db_backbone']:10.3f} {r24.get('bb_fraction', 0):8.3f} {r30['Db_backbone']:10.3f} {r30.get('bb_fraction', 0):8.3f}")

# 与已有红键数据对比
existing_red = {
    16: {2.4: 0.756, 3.0: 0.756},
    64: {2.4: 0.740, 3.0: 0.701},
}
print(f"\n已有红键数据 D_b(red) vs L：")
print(f"{'L':>5} {'D=2.4':>10} {'D=3.0':>10}")
print("-" * 30)
for L in sorted(existing_red.keys()):
    print(f"{L:5d} {existing_red[L][2.4]:10.3f} {existing_red[L][3.0]:10.3f}")

# 保存
save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'paper43_cross_scaling_bb.json')
with open(save_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, default=str)
print(f"\n结果已保存: {save_path}")
