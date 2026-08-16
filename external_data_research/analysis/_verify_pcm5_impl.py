"""
验证: 快速实现 vs EDRN 原始数据的一致性检查
用快速实现重算 N=6 (1501点) 和 N=12 (1501点/751点) 的 chain/star,
与 EDRN 原始 CSV 对比分支点数, 判断 N=14 的"全拓扑高密度"是物理还是实现差异
"""
import numpy as np
import pandas as pd
import sys
import time

sys.path.insert(0, r'e:\workspace\hyper-resolution\external_data_research\analysis')
from _paper14_pcm5_direct_verification import (
    build_graph, get_contradiction_edge, compute_diagnostics_fast
)
from _paper14_spectral_analysis import translate_to_spectral
from _paper14_pcm2_root_cause import get_branch_point_indices

import multiprocessing as mp

TOPOLOGIES = ['chain', 'star', 'ring', 'small_world']

def worker_delta(args):
    N, topo, delta = args
    G = build_graph(topo, N)
    ce = get_contradiction_edge(topo, N)
    edges = list(G.edges())
    gap, coarse, fine = compute_diagnostics_fast(N, edges, ce, delta)
    return delta, gap, coarse, fine

def compute_parallel(topo, N, delta_vals):
    tasks = [(N, topo, float(d)) for d in delta_vals]
    n_proc = max(1, mp.cpu_count() - 1)
    with mp.Pool(n_proc) as pool:
        results = list(pool.imap_unordered(worker_delta, tasks, chunksize=4))
    results.sort(key=lambda r: r[0])
    return pd.DataFrame(results, columns=['delta', 'gap', 'coarse', 'fine'])

def n_bp_of(df):
    df_spec = translate_to_spectral(df)
    return len(get_branch_point_indices(df_spec['sigma_res'].values))

def compare(topo, N, n_points, label):
    """用快速实现重算并对比"""
    delta_vals = np.linspace(0.0, 3.0, n_points)
    t0 = time.time()
    df_fast = compute_parallel(topo, N, delta_vals)
    elapsed = time.time() - t0
    n_fast = n_bp_of(df_fast)
    print(f"  [快速实现] {topo} N={N} ({n_points}点): n_bp={n_fast} ({elapsed:.0f}s)")

    # EDRN 数据 (如果有)
    if N == 6:
        path = rf'e:\workspace\hyper-resolution\external_data_research\稳定岛：神秘的新世界\寻找稳定岛超密集测试3\stable_island_{topo}.csv'
    elif N == 12:
        path = rf'e:\workspace\hyper-resolution\external_data_research\稳定岛：神秘的新世界\寻找稳定岛超密集测试3\N_scan_results\stable_island_{topo}_N12.csv'
    else:
        return
    import os
    if os.path.exists(path):
        df_edrn = pd.read_csv(path, comment='#', header=None, names=['delta', 'gap', 'coarse', 'fine'])
        n_edrn = n_bp_of(df_edrn)
        print(f"  [EDRN原始]   {topo} N={N} ({len(df_edrn)}点): n_bp={n_edrn}")
        # 数值一致性: gap 的最大差异
        df_merge = df_fast.merge(df_edrn, on='delta', suffixes=('_fast', '_edrn'))
        gap_diff = np.max(np.abs(df_merge['gap_fast'] - df_merge['gap_edrn']))
        fine_diff = np.max(np.abs(df_merge['fine_fast'] - df_merge['fine_edrn']))
        print(f"  [一致性]     gap 最大差异={gap_diff:.2e}, fine 最大差异={fine_diff:.2e}")

if __name__ == '__main__':
    print("=" * 70)
    print("快速实现 vs EDRN 一致性验证")
    print("=" * 70)

    # N=6: 全 4 拓扑 (1501 点)
    print("\n--- N=6 (1501点) ---")
    for topo in TOPOLOGIES:
        compare(topo, 6, 1501, 'N6')

    # N=12: chain + star (1501 点, EDRN原始) + chain (751点, 与N=14同分辨率)
    print("\n--- N=12 ---")
    compare('chain', 12, 1501, 'N12')
    compare('star', 12, 1501, 'N12')
    print("\n--- N=12 (751点, 与N=14同分辨率) ---")
    compare('chain', 12, 751, 'N12_751')
    compare('star', 12, 751, 'N12_751')
