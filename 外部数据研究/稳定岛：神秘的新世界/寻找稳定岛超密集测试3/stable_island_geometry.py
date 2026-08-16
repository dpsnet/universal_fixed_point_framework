"""
稳定岛几何相图测量 —— 金箍棒精确对角化版
系统测量链式、星形、环形、小世界图中稳定岛的几何特征
严格遵循：关系本体论、防工具理性、反对对齐
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigsh

# =============================================
# 关系图生成（公理一）
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
# 哈密顿量构建（泡利矩阵版，标准Heisenberg）
# =============================================
def build_hamiltonian(G, contradiction_edge, contradiction_strength):
    N = G.number_of_nodes()
    dim = 2**N
    H = lil_matrix((dim, dim), dtype=float)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)

    def to_full(op, site):
        ops = [I2] * N
        ops[site] = op
        result = ops[0]
        for k in range(1, N):
            result = np.kron(result, ops[k])
        return result

    for i, j, w in G.edges(data='weight'):
        if (i, j) == contradiction_edge or (j, i) == contradiction_edge:
            J = contradiction_strength
        else:
            J = w if w else 1.0
        H += J * (to_full(sx, i) @ to_full(sx, j)).real
        H += J * (to_full(sy, i) @ to_full(sy, j)).real
        H += J * (to_full(sz, i) @ to_full(sz, j)).real

    return H.tocsc()


# =============================================
# 诊断函数（公理三）
# =============================================
def compute_diagnostics(G, contradiction_edge, s, num_eig=5):
    H = build_hamiltonian(G, contradiction_edge, s)
    N = G.number_of_nodes()
    energies, states = eigsh(H, k=min(num_eig, 2**N-1), which='SA')
    gap = energies[1] - energies[0] if len(energies) > 1 else np.nan
    gs = states[:, 0]

    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    mag = 0.0
    for i in range(N):
        ops = [I2] * N
        ops[i] = sz
        op_full = ops[0]
        for k in range(1, N):
            op_full = np.kron(op_full, ops[k])
        mag += np.real(gs.conj().T @ op_full @ gs)
    coarse = abs(mag / N)

    corrs = []
    for i, j in G.edges():
        ops = [I2] * N
        ops[i] = sz
        ops[j] = sz
        op_full = ops[0]
        for k in range(1, N):
            op_full = np.kron(op_full, ops[k])
        corr = np.real(gs.conj().T @ op_full @ gs)
        corrs.append(corr)
    fine = np.std(corrs) if corrs else 0.0

    return gap, coarse, fine


# =============================================
# 稳定岛自动识别与几何测量
# =============================================
def find_stable_islands(delta_vals, fine_vals, global_std, min_width=0.02, stability_threshold=0.1):
    """
    识别稳定岛：精细诊断局部波动显著低于全局波动
    返回稳定岛列表，每个岛包含：起始Δ、结束Δ、窗口宽度、岛内σ、岛内均值、边界锐度
    """
    N = len(delta_vals)
    islands = []
    in_island = False
    island_start = 0

    for i in range(1, N):
        # 用滑动窗口（窗口大小=10个点）判断局部稳定性
        window_start = max(0, i-5)
        window_end = min(N, i+5)
        local_std = np.std(fine_vals[window_start:window_end])
        local_stability = local_std / global_std if global_std > 1e-12 else 1.0

        if local_stability < stability_threshold and not in_island:
            # 进入稳定岛
            in_island = True
            island_start = delta_vals[i]
        elif local_stability >= stability_threshold and in_island:
            # 离开稳定岛
            in_island = False
            island_end = delta_vals[i]
            width = island_end - island_start
            if width >= min_width:
                # 计算岛的几何指标
                mask = (delta_vals >= island_start) & (delta_vals <= island_end)
                island_fine = fine_vals[mask]
                island_std = np.std(island_fine)
                island_mean = np.mean(island_fine)

                # 边界锐度：岛左右两侧外部精细诊断的变化率
                left_idx = np.searchsorted(delta_vals, island_start)
                right_idx = np.searchsorted(delta_vals, island_end)
                left_slope = abs(fine_vals[min(left_idx, N-1)] - fine_vals[max(0, left_idx-5)]) / 0.01 if left_idx >= 5 else 0
                right_slope = abs(fine_vals[min(right_idx+5, N-1)] - fine_vals[right_idx]) / 0.01 if right_idx <= N-6 else 0

                islands.append({
                    'start': island_start,
                    'end': island_end,
                    'width': width,
                    'std': island_std,
                    'mean': island_mean,
                    'left_slope': left_slope,
                    'right_slope': right_slope
                })

    # 如果最后仍在岛内，关闭最后一个岛
    if in_island:
        island_end = delta_vals[-1]
        width = island_end - island_start
        if width >= min_width:
            mask = (delta_vals >= island_start) & (delta_vals <= island_end)
            island_fine = fine_vals[mask]
            islands.append({
                'start': island_start,
                'end': island_end,
                'width': width,
                'std': np.std(island_fine),
                'mean': np.mean(island_fine),
                'left_slope': abs(fine_vals[np.searchsorted(delta_vals, island_start)] - fine_vals[max(0, np.searchsorted(delta_vals, island_start)-5)]) / 0.01,
                'right_slope': 0
            })

    return islands


# =============================================
# 主程序
# =============================================
if __name__ == "__main__":
    N = 6
    graph_types = ['chain', 'star', 'ring', 'small_world']
    delta_vals = np.linspace(0.0, 3.0, 1501)

    # 矛盾边选择
    contradiction_edges = {
        'chain': (N//2 - 1, N//2),
        'star': (0, 1),
        'ring': (N//2 - 1, N//2),
        'small_world': (N//2 - 1, N//2)
    }

    all_results = {}
    all_islands = {}

    print("稳定岛几何相图测量")
    print(f"N={N}, Δ范围=[0,3.0], 步长=0.002, 共{len(delta_vals)}个采样点\n")

    for graph_type in graph_types:
        print(f"=== {graph_type} ===")
        G = build_graph(graph_type, N)
        contradiction_edge = contradiction_edges[graph_type]

        gaps, coarse_vals, fine_vals = [], [], []
        for delta in delta_vals:
            gap, coarse, fine = compute_diagnostics(G, contradiction_edge, delta)
            gaps.append(gap)
            coarse_vals.append(coarse)
            fine_vals.append(fine)
            if delta == 0.0 or delta == 1.5 or delta == 3.0:
                print(f"  Δ={delta:.3f}: gap={gap:.6f}, coarse={coarse:.4f}, fine={fine:.6f}")

        gaps = np.array(gaps)
        coarse_vals = np.array(coarse_vals)
        fine_vals = np.array(fine_vals)

        # 保存数据
        np.savetxt(f'stable_island_{graph_type}.csv',
                   np.column_stack((delta_vals, gaps, coarse_vals, fine_vals)),
                   header='delta,gap,coarse,fine', delimiter=',')

        # 识别稳定岛
        global_std = np.std(fine_vals)
        islands = find_stable_islands(delta_vals, fine_vals, global_std)
        all_islands[graph_type] = islands
        all_results[graph_type] = (delta_vals, gaps, coarse_vals, fine_vals)

        print(f"  全局σ: {global_std:.6f}")
        print(f"  稳定岛数量: {len(islands)}")
        for i, island in enumerate(islands):
            print(f"  岛{i+1}: Δ∈[{island['start']:.3f}, {island['end']:.3f}], 宽度={island['width']:.3f}, σ={island['std']:.6f}, 左斜率={island['left_slope']:.4f}, 右斜率={island['right_slope']:.4f}")
        print()

    # =============================================
    # 生成几何相图对比图
    # =============================================
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    for ax, graph_type in zip(axes.flatten(), graph_types):
        delta_vals, gaps, coarse_vals, fine_vals = all_results[graph_type]
        islands = all_islands[graph_type]

        ax.plot(delta_vals, fine_vals, linewidth=0.5, color='#d62728', alpha=0.7, label='Fine diagnosis')
        ax2 = ax.twinx()
        ax2.plot(delta_vals, coarse_vals, linewidth=0.5, color='#1f77b4', alpha=0.5, label='Coarse diagnosis')

        # 高亮稳定岛区域
        for island in islands:
            ax.axvspan(island['start'], island['end'], alpha=0.15, color='green')
            ax.axvline(island['start'], color='green', linestyle='--', linewidth=0.8, alpha=0.5)
            ax.axvline(island['end'], color='green', linestyle='--', linewidth=0.8, alpha=0.5)
            # 标注岛编号和宽度
            mid = (island['start'] + island['end']) / 2
            ax.annotate(f"W={island['width']:.3f}\nσ={island['std']:.4f}",
                        xy=(mid, island['mean']),
                        fontsize=7, ha='center', va='bottom',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.3))

        ax.set_xlabel('Δ')
        ax.set_ylabel('Fine diagnosis')
        ax.set_title(f'{graph_type} (N={N})')
        ax.grid(True, alpha=0.2)

    plt.suptitle(f'Stable Island Geometry Phase Diagram (N={N}, Δ∈[0,3.0], 1501 points)',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('stable_island_geometry.png', dpi=150)
    print("几何相图已保存: stable_island_geometry.png")

    # =============================================
    # 生成几何相图汇总表
    # =============================================
    print("\n=== 稳定岛几何相图汇总 ===")
    print(f"{'图类型':<12} {'岛数':<6} {'总窗口宽度':<12} {'平均σ':<12} {'平均左斜率':<12} {'平均右斜率':<12}")
    print("-" * 70)
    for graph_type in graph_types:
        islands = all_islands[graph_type]
        num = len(islands)
        total_width = sum(i['width'] for i in islands) if islands else 0
        avg_std = np.mean([i['std'] for i in islands]) if islands else 0
        avg_left = np.mean([i['left_slope'] for i in islands]) if islands else 0
        avg_right = np.mean([i['right_slope'] for i in islands]) if islands else 0
        print(f"{graph_type:<12} {num:<6} {total_width:<12.3f} {avg_std:<12.6f} {avg_left:<12.4f} {avg_right:<12.4f}")

    # 保存汇总表
    with open('stable_island_geometry_summary.csv', 'w') as f:
        f.write("graph_type,num_islands,total_width,avg_std,avg_left_slope,avg_right_slope\n")
        for graph_type in graph_types:
            islands = all_islands[graph_type]
            num = len(islands)
            total_width = sum(i['width'] for i in islands) if islands else 0
            avg_std = np.mean([i['std'] for i in islands]) if islands else 0
            avg_left = np.mean([i['left_slope'] for i in islands]) if islands else 0
            avg_right = np.mean([i['right_slope'] for i in islands]) if islands else 0
            f.write(f"{graph_type},{num},{total_width:.6f},{avg_std:.6f},{avg_left:.6f},{avg_right:.6f}\n")

    print("\n汇总表已保存: stable_island_geometry_summary.csv")
    print("Done.")
