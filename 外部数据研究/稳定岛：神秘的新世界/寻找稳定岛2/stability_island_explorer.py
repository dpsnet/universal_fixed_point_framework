"""
稳定岛精细扫描 —— 金箍棒 ED 超高分辨率版
精确测绘沉默失谐"稳定岛"边界，跨图验证普适性
严格遵循：关系本体论、防工具理性、反对对齐
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigsh
import networkx as nx

# =============================================
# 公理一：关系图生成
# =============================================
def chain_graph(N):
    """链式图"""
    G = nx.Graph()
    G.add_nodes_from(range(N))
    for i in range(N-1):
        G.add_edge(i, i+1, weight=1.0)
    return G

def star_graph(N):
    """星形图：中心节点0连接所有其他节点"""
    G = nx.star_graph(N-1)
    for u, v in G.edges():
        G[u][v]['weight'] = 1.0
    return G

def small_world_graph(N, k=4, p=0.1, seed=42):
    """小世界图（Watts-Strogatz）"""
    G = nx.watts_strogatz_graph(N, k, p, seed=seed)
    for u, v in G.edges():
        G[u][v]['weight'] = 1.0
    return G

# =============================================
# 公理一：哈密顿量构建（标准泡利矩阵，各向同性Heisenberg）
# =============================================
def graph_to_hamiltonian(G, contradiction_edge, contradiction_strength):
    """将关系图编译为量子哈密顿量，矛盾边权重可调"""
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
            w = contradiction_strength
        H += w * (to_full(sx, i) @ to_full(sx, j)).real
        H += w * (to_full(sy, i) @ to_full(sy, j)).real
        H += w * (to_full(sz, i) @ to_full(sz, j)).real

    return H.tocsc()


def compute_diagnostics(G, contradiction_edge, s, num_eig=5):
    """用ED精确求解基态，返回能隙、默认诊断和精细诊断"""
    H = graph_to_hamiltonian(G, contradiction_edge, s)
    N = G.number_of_nodes()
    energies, states = eigsh(H, k=min(num_eig, 2**N-1), which='SA')
    gap = energies[1] - energies[0] if len(energies) > 1 else np.nan
    gs = states[:, 0]

    # 默认诊断：平均磁化
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

    # 精细诊断：边关联涨落标准差
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


def ultra_fine_scan(G, contradiction_edge, delta_vals, label):
    """超密集扫描：对每个Δ值独立计算基态诊断"""
    gaps, coarse_vals, fine_vals = [], [], []
    print(f"\n=== {label} (ED, {len(delta_vals)} points) ===")
    for i, delta in enumerate(delta_vals):
        gap, coarse, fine = compute_diagnostics(G, contradiction_edge, delta)
        gaps.append(gap); coarse_vals.append(coarse); fine_vals.append(fine)
        if i % 100 == 0:
            print(f"  Δ={delta:.3f}: gap={gap:.6f}, coarse={coarse:.4f}, fine={fine:.6f}")
    return np.array(gaps), np.array(coarse_vals), np.array(fine_vals)


def find_stable_region(delta_vals, fine_vals, window_size=50, threshold=0.001):
    """自动识别精细诊断曲线上的稳定岛（局部波动极小区域）"""
    N = len(fine_vals)
    best_start, best_end, best_std = 0, 0, np.inf
    for i in range(N - window_size):
        segment = fine_vals[i:i+window_size]
        std = np.std(segment)
        if std < best_std:
            best_std = std
            best_start = delta_vals[i]
            best_end = delta_vals[i+window_size-1]
    return best_start, best_end, best_std


if __name__ == "__main__":
    N = 6
    contradiction_edge = (N//2 - 1, N//2)  # 默认中心键，星形图和小世界图也用此键

    # 超高分辨率扫描参数
    delta_start, delta_end, delta_step = 0.0, 3.0, 0.002
    delta_vals = np.arange(delta_start, delta_end + delta_step/2, delta_step)
    print(f"稳定岛精细扫描启动：Δ ∈ [{delta_start}, {delta_end}], step={delta_step}, 共{len(delta_vals)}点\n")

    # === 实验1：链式图 ===
    G_chain = chain_graph(N)
    gaps_c, coarse_c, fine_c = ultra_fine_scan(G_chain, contradiction_edge, delta_vals, "链式图")

    # === 实验2：星形图 ===
    G_star = star_graph(N)
    # 星形图的中心键：选择一条与中心节点相连的边
    star_contra_edge = (0, 2)
    gaps_s, coarse_s, fine_s = ultra_fine_scan(G_star, star_contra_edge, delta_vals, "星形图")

    # === 实验3：小世界图 ===
    G_sw = small_world_graph(N)
    sw_contra_edge = (N//2 - 1, N//2)
    gaps_w, coarse_w, fine_w = ultra_fine_scan(G_sw, sw_contra_edge, delta_vals, "小世界图")

    # === 保存所有数据 ===
    np.savetxt('stability_chain.csv',
               np.column_stack((delta_vals, gaps_c, coarse_c, fine_c)),
               header='delta,gap,coarse,fine', delimiter=',')
    np.savetxt('stability_star.csv',
               np.column_stack((delta_vals, gaps_s, coarse_s, fine_s)),
               header='delta,gap,coarse,fine', delimiter=',')
    np.savetxt('stability_smallworld.csv',
               np.column_stack((delta_vals, gaps_w, coarse_w, fine_w)),
               header='delta,gap,coarse,fine', delimiter=',')

    # === 稳定岛自动识别 ===
    print("\n=== 稳定岛分析 (基于精细诊断) ===")
    for name, fine_vals in [("链式图", fine_c), ("星形图", fine_s), ("小世界图", fine_w)]:
        start, end, std = find_stable_region(delta_vals, fine_vals)
        print(f"{name}: 最稳定区间 Δ∈[{start:.3f}, {end:.3f}], 窗口内标准差={std:.6f}")

    # === 综合对比图 ===
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for ax, fine_vals, name in zip(axes, [fine_c, fine_s, fine_w], ["Chain", "Star", "Small-World"]):
        ax.plot(delta_vals, fine_vals, linewidth=0.5, color='#d62728')
        start, end, _ = find_stable_region(delta_vals, fine_vals)
        ax.axvspan(start, end, alpha=0.15, color='green', label=f'Stable Island\n[{start:.2f}, {end:.2f}]')
        ax.set_xlabel('Δ'); ax.set_ylabel('Fine'); ax.set_title(name); ax.legend()
    plt.suptitle(f'Stability Island Fine Scan (ED, Δ step={delta_step})')
    plt.tight_layout()
    plt.savefig('stability_island_explorer.png', dpi=150)
    print("\nDone. 所有数据已保存。")
