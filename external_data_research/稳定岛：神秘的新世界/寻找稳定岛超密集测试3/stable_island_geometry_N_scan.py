"""
稳定岛几何相图测量 —— N 扫描版（N=8, 10, 12）
基于 EDRN 原脚本 stable_island_geometry.py 的算法（于见隐设计），保持物理模型完全一致：
  - 标准 Heisenberg 模型（sx + sy + sz）
  - 矛盾边装置（contradiction_edge 用 Δ 作为 J）
  - 相同的图生成方式（chain/star/ring/small_world seed=42）
  - 相同的矛盾边选择（N//2-1, N//2）
  - 相同的 Δ 范围 [0, 3.0]，1501 点
  - 相同的诊断量（gap, coarse, fine）
  - 相同的 find_stable_islands 算法

性能优化（不改物理，只改实现）：
  1. 预计算稀疏泡利算符 sx_full[i]/sy_full[i]/sz_full[i]（一次性）
  2. build_hamiltonian 只做稀疏矩阵加法（每个 Δ 只更新 J 系数）
  3. 诊断函数复用预计算的 sz_full[i]

用途：P-SI-1 扩展裁决目标 —— 反算 k(N) = ln(σ_岛内/σ_全局)/ln(1/15)，建立换算律
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import time
from pathlib import Path
from scipy.sparse import csc_matrix, eye as sparse_eye
from scipy.sparse.linalg import eigsh

# =============================================
# 稀疏泡利矩阵预计算（性能关键）
# =============================================
def build_pauli_operators(N):
    """预计算每个位点的稀疏泡利算符的 N 重 Kronecker 积"""
    sx = csc_matrix(np.array([[0, 1], [1, 0]], dtype=complex))
    sy = csc_matrix(np.array([[0, -1j], [1j, 0]], dtype=complex))
    sz = csc_matrix(np.array([[1, 0], [0, -1]], dtype=complex))
    I2 = sparse_eye(2, dtype=complex, format='csc')

    sx_full, sy_full, sz_full = [], [], []
    for i in range(N):
        for op, storage in [(sx, sx_full), (sy, sy_full), (sz, sz_full)]:
            ops = [I2] * N
            ops[i] = op
            result = ops[0]
            for k in range(1, N):
                result = scipy_kron(result, ops[k], format='csc')
            storage.append(result)
    return sx_full, sy_full, sz_full


def scipy_kron(a, b, format='csc'):
    """稀疏 kron 封装"""
    from scipy.sparse import kron
    return kron(a, b, format=format)


# =============================================
# 关系图生成（与原脚本完全一致）
# =============================================
def build_graph(graph_type, N):
    if graph_type == 'chain':
        G = nx.Graph()
        G.add_nodes_from(range(N))
        for i in range(N-1):
            G.add_edge(i, i+1, weight=1.0)
        return G
    elif graph_type == 'star':
        G = nx.star_graph(N-1)
        for u, v in G.edges():
            G[u][v]['weight'] = 1.0
        return G
    elif graph_type == 'ring':
        G = nx.cycle_graph(N)
        for u, v in G.edges():
            G[u][v]['weight'] = 1.0
        return G
    elif graph_type == 'small_world':
        G = nx.watts_strogatz_graph(N, 4, 0.1, seed=42)
        for u, v in G.edges():
            G[u][v]['weight'] = 1.0
        return G
    else:
        raise ValueError(f"Unknown graph type: {graph_type}")


# =============================================
# 哈密顿量构建（稀疏优化版，物理与原脚本一致）
# =============================================
def build_hamiltonian_sparse(edges, contradiction_edge, s, sx_full, sy_full, sz_full):
    dim = sx_full[0].shape[0]
    H = csc_matrix((dim, dim), dtype=complex)
    for (i, j) in edges:
        if (i, j) == contradiction_edge or (j, i) == contradiction_edge:
            J = s
        else:
            J = 1.0
        # Heisenberg: J * (Sx_i Sx_j + Sy_i Sy_j + Sz_i Sz_j)
        H = H + J * (sx_full[i] @ sx_full[j] +
                     sy_full[i] @ sy_full[j] +
                     sz_full[i] @ sz_full[j])
    return H


# =============================================
# 诊断函数（稀疏优化版，物理与原脚本一致）
# =============================================
def compute_diagnostics_sparse(edges, contradiction_edge, s, sx_full, sy_full, sz_full, N, num_eig=5):
    H = build_hamiltonian_sparse(edges, contradiction_edge, s, sx_full, sy_full, sz_full)
    dim = H.shape[0]
    k_eig = min(num_eig, dim - 1)
    energies, states = eigsh(H, k=k_eig, which='SA')
    gap = energies[1] - energies[0] if len(energies) > 1 else np.nan
    gs = states[:, 0]

    # Coarse: 磁化率 |<M>| = |sum_i <sz_i>| / N
    mag = 0.0
    for i in range(N):
        mag += np.real(gs.conj().T @ (sz_full[i] @ gs))
    coarse = abs(mag / N)

    # Fine: 关联函数 <sz_i sz_j> 的标准差
    corrs = []
    for (i, j) in edges:
        # <gs|sz_i sz_j|gs> = (sz_full[j] @ gs) 然后再用 sz_full[i]
        sj_gs = sz_full[j] @ gs
        corr = np.real(gs.conj().T @ (sz_full[i] @ sj_gs))
        corrs.append(corr)
    fine = np.std(corrs) if corrs else 0.0

    return float(gap), float(coarse), float(fine)


# =============================================
# 稳定岛识别（与原脚本完全一致，含边界处理）
# =============================================
def find_stable_islands(delta_vals, fine_vals, global_std, min_width=0.02, stability_threshold=0.1):
    N = len(delta_vals)
    islands = []
    in_island = False
    island_start = 0

    for i in range(1, N):
        window_start = max(0, i-5)
        window_end = min(N, i+5)
        local_std = np.std(fine_vals[window_start:window_end])
        local_stability = local_std / global_std if global_std > 1e-12 else 1.0

        if local_stability < stability_threshold and not in_island:
            in_island = True
            island_start = delta_vals[i]
        elif local_stability >= stability_threshold and in_island:
            in_island = False
            island_end = delta_vals[i]
            width = island_end - island_start
            if width >= min_width:
                mask = (delta_vals >= island_start) & (delta_vals <= island_end)
                island_fine = fine_vals[mask]
                island_std = np.std(island_fine)
                island_mean = np.mean(island_fine)
                left_idx = np.searchsorted(delta_vals, island_start)
                right_idx = np.searchsorted(delta_vals, island_end)
                left_slope = abs(fine_vals[min(left_idx, N-1)] - fine_vals[max(0, left_idx-5)]) / 0.01 if left_idx >= 5 else 0
                right_slope = abs(fine_vals[min(right_idx+5, N-1)] - fine_vals[right_idx]) / 0.01 if right_idx <= N-6 else 0
                islands.append({
                    'start': island_start, 'end': island_end, 'width': width,
                    'std': island_std, 'mean': island_mean,
                    'left_slope': left_slope, 'right_slope': right_slope
                })

    if in_island:
        island_end = delta_vals[-1]
        width = island_end - island_start
        if width >= min_width:
            mask = (delta_vals >= island_start) & (delta_vals <= island_end)
            island_fine = fine_vals[mask]
            left_idx = np.searchsorted(delta_vals, island_start)
            islands.append({
                'start': island_start, 'end': island_end, 'width': width,
                'std': np.std(island_fine), 'mean': np.mean(island_fine),
                'left_slope': abs(fine_vals[left_idx] - fine_vals[max(0, left_idx-5)]) / 0.01,
                'right_slope': 0
            })
    return islands


# =============================================
# 主程序：N 扫描
# =============================================
def run_single_N(N, graph_types, delta_vals, out_dir):
    """对给定 N 执行全部拓扑扫描，输出 CSV 和 summary"""
    print(f"\n{'='*60}")
    print(f"N = {N}  (dim = 2^{N} = {2**N})")
    print(f"{'='*60}")

    t_start = time.time()
    sx_full, sy_full, sz_full = build_pauli_operators(N)
    t_precomp = time.time() - t_start
    print(f"泡利算符预计算完成: {t_precomp:.1f}s")

    all_results = {}
    all_islands = {}

    for graph_type in graph_types:
        t_graph = time.time()
        G = build_graph(graph_type, N)
        edges = list(G.edges())
        contradiction_edge = (N//2 - 1, N//2) if graph_type != 'star' else (0, 1)

        gaps, coarse_vals, fine_vals = [], [], []
        n_points = len(delta_vals)

        for idx, delta in enumerate(delta_vals):
            gap, coarse, fine = compute_diagnostics_sparse(
                edges, contradiction_edge, delta, sx_full, sy_full, sz_full, N)
            gaps.append(gap)
            coarse_vals.append(coarse)
            fine_vals.append(fine)

            if idx % 200 == 0 or idx == n_points - 1:
                elapsed = time.time() - t_graph
                eta = elapsed / (idx + 1) * (n_points - idx - 1)
                print(f"  [{graph_type}] Δ={delta:.3f} ({idx+1}/{n_points})  "
                      f"elapsed={elapsed:.1f}s  ETA={eta:.1f}s  "
                      f"fine={fine:.6e}")

        gaps = np.array(gaps)
        coarse_vals = np.array(coarse_vals)
        fine_vals = np.array(fine_vals)

        # 保存 CSV（格式与原脚本完全一致）
        csv_path = out_dir / f'stable_island_{graph_type}_N{N}.csv'
        np.savetxt(csv_path,
                   np.column_stack((delta_vals, gaps, coarse_vals, fine_vals)),
                   header='delta,gap,coarse,fine', delimiter=',', comments='# ')
        print(f"  [保存] {csv_path.name}")

        # 识别稳定岛
        global_std = np.std(fine_vals)
        islands = find_stable_islands(delta_vals, fine_vals, global_std)
        all_islands[graph_type] = islands
        all_results[graph_type] = (delta_vals, gaps, coarse_vals, fine_vals)

        print(f"  全局σ: {global_std:.6e}")
        print(f"  稳定岛数量: {len(islands)}")
        for i, island in enumerate(islands):
            print(f"  岛{i+1}: Δ∈[{island['start']:.3f}, {island['end']:.3f}], "
                  f"宽度={island['width']:.3f}, σ={island['std']:.6e}")
        print(f"  [{graph_type}] 耗时: {time.time()-t_graph:.1f}s")

    # 汇总 CSV
    summary_path = out_dir / f'stable_island_geometry_summary_N{N}.csv'
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("graph_type,num_islands,total_width,avg_std,avg_left_slope,avg_right_slope\n")
        for graph_type in graph_types:
            islands = all_islands[graph_type]
            num = len(islands)
            total_width = sum(i['width'] for i in islands) if islands else 0
            avg_std = np.mean([i['std'] for i in islands]) if islands else 0
            avg_left = np.mean([i['left_slope'] for i in islands]) if islands else 0
            avg_right = np.mean([i['right_slope'] for i in islands]) if islands else 0
            f.write(f"{graph_type},{num},{total_width:.6f},{avg_std:.6e},{avg_left:.6f},{avg_right:.6f}\n")
    print(f"  [保存] {summary_path.name}")

    total_time = time.time() - t_start
    print(f"\nN={N} 总耗时: {total_time:.1f}s ({total_time/60:.1f} min)")
    return all_results, all_islands


def compute_k_N(all_results, all_islands, N, out_dir):
    """反算 k(N) = ln(σ_岛内/σ_全局)/ln(1/15)，输出汇总"""
    S4 = 1.0 / 15.0
    LN_S4_INV = np.log(1.0 / S4)  # ln(15)
    k_threshold = np.log(0.1) / (-LN_S4_INV)

    rows = []
    for graph_type, (delta_vals, gaps, coarse_vals, fine_vals) in all_results.items():
        global_std = np.std(fine_vals)
        islands = all_islands[graph_type]
        if not islands:
            rows.append({
                'N': N, 'graph_type': graph_type,
                'global_std': global_std, 'num_islands': 0,
                'island_std': np.nan, 'k_raw': np.nan,
                'k_ceiling': np.nan, 'note': 'no_island'
            })
            continue
        for j, isl in enumerate(islands):
            R = isl['std'] / global_std if global_std > 1e-18 else 1e-18
            k_raw = np.log(max(R, 1e-18)) / (-LN_S4_INV)
            rows.append({
                'N': N, 'graph_type': graph_type,
                'global_std': global_std, 'num_islands': len(islands),
                'island_std': isl['std'], 'k_raw': k_raw,
                'k_ceiling': int(np.ceil(k_raw)),
                'note': f'island_{j+1}_width={isl["width"]:.3f}'
            })

    k_path = out_dir / f'k_N_summary_N{N}.csv'
    with open(k_path, 'w', encoding='utf-8') as f:
        f.write("N,graph_type,global_std,num_islands,island_std,k_raw,k_ceiling,note\n")
        for r in rows:
            f.write(f"{r['N']},{r['graph_type']},{r['global_std']:.6e},"
                    f"{r['num_islands']},{r['island_std']:.6e},"
                    f"{r['k_raw']:.4f},{r['k_ceiling']},{r['note']}\n")
    print(f"  [保存] {k_path.name}")
    return rows


# =============================================
# 入口
# =============================================
if __name__ == "__main__":
    N_list = [8, 10, 12]
    graph_types = ['chain', 'star', 'ring', 'small_world']
    delta_vals = np.linspace(0.0, 3.0, 1501)

    out_dir = Path(__file__).parent / 'N_scan_results'
    out_dir.mkdir(exist_ok=True)

    print("稳定岛几何相图测量 —— N 扫描版")
    print(f"N_list = {N_list}")
    print(f"graph_types = {graph_types}")
    print(f"Δ范围=[0, 3.0], 步长=0.002, 共 {len(delta_vals)} 个采样点")
    print(f"输出目录: {out_dir}")

    all_k_rows = []
    t_total = time.time()

    for N in N_list:
        all_results, all_islands = run_single_N(N, graph_types, delta_vals, out_dir)
        k_rows = compute_k_N(all_results, all_islands, N, out_dir)
        all_k_rows.extend(k_rows)

    # 全局 k(N) 汇总
    k_global_path = out_dir / 'k_N_global_summary.csv'
    with open(k_global_path, 'w', encoding='utf-8') as f:
        f.write("N,graph_type,global_std,num_islands,island_std,k_raw,k_ceiling,note\n")
        for r in all_k_rows:
            f.write(f"{r['N']},{r['graph_type']},{r['global_std']:.6e},"
                    f"{r['num_islands']},{r['island_std']:.6e},"
                    f"{r['k_raw']:.4f},{r['k_ceiling']},{r['note']}\n")
    print(f"\n[保存] 全局 k(N) 汇总: {k_global_path.name}")

    # 控制台汇总
    print(f"\n{'='*60}")
    print("k(N) 反算汇总（核心目标：检验 k 是否随 N 变化）")
    print(f"{'='*60}")
    print(f"阈值 k(θ=0.1) = {np.log(0.1)/(-np.log(15)):.4f}")
    print(f"{'N':<4} {'graph_type':<14} {'k_raw':<10} {'⌈k⌉':<6} {'island_std':<14} {'global_std':<14}")
    print("-" * 70)
    for r in all_k_rows:
        if np.isnan(r['k_raw']):
            print(f"{r['N']:<4} {r['graph_type']:<14} {'N/A':<10} {'N/A':<6} "
                  f"{'N/A':<14} {r['global_std']:.6e}")
        else:
            print(f"{r['N']:<4} {r['graph_type']:<14} {r['k_raw']:<10.4f} {r['k_ceiling']:<6} "
                  f"{r['island_std']:.6e}  {r['global_std']:.6e}")

    print(f"\n总耗时: {time.time()-t_total:.1f}s = {(time.time()-t_total)/60:.1f} min")
    print("Done.")
