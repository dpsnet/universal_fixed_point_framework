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
"""L=128/256 高效仿真：骨架提取 + 少量红键。

策略：
  L=128: D∈{2.4, 3.0}, c=0, N_CFG=1 → 骨架 + 红键(D=3.0 only)
  L=256: D∈{2.4, 3.0}, c=0, N_CFG=1 → 仅骨架（红键计算量过大）
"""
import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paper43_coupled_spectral_dip as m
import numpy as np

PHI = 0.31
C_VAL = 0.0
RESULTS = {}

def run_one(L, D, seed=0, do_red=False):
    """运行单个仿真配置，返回 D_b 结果。"""
    t0 = time.time()
    binary, radii, lambdas, U = m.fractal_pore_network(L, PHI, D, seed=seed)
    P_arr, S_arr, P_c, S_c, order, Uf = m.run_fractal_dip(binary, U, c=C_VAL, seed=seed)
    
    result = {'P_c': float(P_c), 'S_c': float(S_c)}
    
    pressures, A_t, lam_edges, snapshots = m.spectral_band_mapping(
        binary, lambdas, P_arr, P_c, Uf)
    idx = np.argmin(np.abs(pressures - P_c))
    cluster = snapshots[idx]
    
    if not cluster.any():
        return result
    
    # 骨架提取
    backbone = m.extract_backbone(cluster)
    if backbone.any():
        Db_bb, r2_bb = m.box_counting_3d(backbone)
        result['Db_backbone'] = float(Db_bb)
        result['r2_backbone'] = float(r2_bb)
    else:
        result['Db_backbone'] = np.nan
    
    # 红键提取（可选）
    if do_red:
        _, _, _, _, _, _, Db_rd, r2_rd = m.extract_p3(snapshots, pressures, P_c)
        result['Db_red'] = float(Db_rd) if not np.isnan(Db_rd) else np.nan
        result['r2_red'] = float(r2_rd)
    
    result['elapsed'] = time.time() - t0
    return result

# ============ L=128 ============
print("=" * 60)
print("L = 128 仿真")
print("=" * 60)
RESULTS[128] = {}

for D in [2.4, 3.0]:
    do_red = (D == 3.0)  # 仅 D=3.0 做红键提取
    print(f"  D={D} (red={do_red}) ...", end=" ", flush=True)
    r = run_one(128, D, seed=0, do_red=do_red)
    RESULTS[128][D] = r
    print(f"P_c={r['P_c']:.4f} Db_bb={r.get('Db_backbone', float('nan')):.3f}" +
          (f" Db_red={r.get('Db_red', float('nan')):.3f}" if 'Db_red' in r else "") +
          f" t={r['elapsed']:.0f}s", flush=True)

# ============ L=256 ============
print("\n" + "=" * 60)
print("L = 256 仿真（仅骨架）")
print("=" * 60)
RESULTS[256] = {}

for D in [2.4, 3.0]:
    print(f"  D={D} ...", end=" ", flush=True)
    r = run_one(256, D, seed=0, do_red=False)
    RESULTS[256][D] = r
    print(f"P_c={r['P_c']:.4f} Db_bb={r.get('Db_backbone', float('nan')):.3f} t={r['elapsed']:.0f}s", flush=True)

# ============ 汇总 ============
print("\n" + "=" * 60)
print("汇总结果")
print("=" * 60)

# 已有数据
existing_red = {
    16: {2.2: 0.756, 2.4: 0.756, 2.6: 0.756, 2.8: 0.756, 3.0: 0.756, 3.2: 0.756},
    64: {2.2: 0.865, 2.4: 0.740, 2.6: 0.903, 2.8: 0.856, 3.0: 0.701, 3.2: 0.872},
}
existing_bb = {
    16: {2.2: 1.864, 2.4: 1.864, 2.6: 1.864, 2.8: 1.864, 3.0: 1.864, 3.2: 1.864},
    64: {2.2: 1.948, 2.4: 1.962, 2.6: 1.789, 2.8: 1.799, 3.0: 1.988, 3.2: 1.873},
}

print("\n--- D_b(red) vs L ---")
print(f"{'L':>5} {'D=2.4':>8} {'D=3.0':>8}")
print("-" * 30)
for L in [16, 64, 128]:
    D24 = existing_red.get(L, {}).get(2.4, RESULTS.get(L, {}).get(2.4, {}).get('Db_red', 'N/A'))
    D30 = existing_red.get(L, {}).get(3.0, RESULTS.get(L, {}).get(3.0, {}).get('Db_red', 'N/A'))
    if isinstance(D24, float):
        D24_str = f"{D24:.3f}"
    else:
        D24_str = str(D24)
    if isinstance(D30, float):
        D30_str = f"{D30:.3f}"
    else:
        D30_str = str(D30)
    print(f"{L:5d} {D24_str:>8} {D30_str:>8}")

print("\n--- D_b(backbone) vs L ---")
print(f"{'L':>5} {'D=2.4':>8} {'D=3.0':>8}")
print("-" * 30)
for L in [16, 64, 128, 256]:
    D24 = existing_bb.get(L, {}).get(2.4, RESULTS.get(L, {}).get(2.4, {}).get('Db_backbone', 'N/A'))
    D30 = existing_bb.get(L, {}).get(3.0, RESULTS.get(L, {}).get(3.0, {}).get('Db_backbone', 'N/A'))
    if isinstance(D24, float):
        D24_str = f"{D24:.3f}"
    else:
        D24_str = str(D24)
    if isinstance(D30, float):
        D30_str = f"{D30:.3f}"
    else:
        D30_str = str(D30)
    print(f"{L:5d} {D24_str:>8} {D30_str:>8}")

# 保存
save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'paper43_cross_scaling_results.json')
with open(save_path, 'w', encoding='utf-8') as f:
    json.dump(RESULTS, f, indent=2, default=str)
print(f"\n结果已保存: {save_path}")
