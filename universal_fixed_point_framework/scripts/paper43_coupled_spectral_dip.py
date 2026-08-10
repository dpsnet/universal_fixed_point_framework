#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Paper43 耦合谱流-DIP 正向仿真：从分形孔隙分布 → 两相流 DIP → 谱流标度涌现

验证目标：
  P1: ln P_t ∝ 1/(D-2) 从分形驱动 DIP 自然涌现
  P2: ν(D, c) 漂移模式与现有 DIP 一致
  P3: 突破簇盒计数 D_b 与理论值比对
  谱流方程: dA_t/dt 与生成元线性相关

理论依据：notes/05_condensed_matter/spectral_shale_accumulation.md §11
依赖复用：paperX_shale_p2_ip_uf.py (ip_union_entry)
          paperX_shale_p2_dyn_ip.py (bellman_ford_path_resistance, p2nu, p2nu_split)
"""

import numpy as np
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paperX_shale_p2_ip_uf import ip_union_entry
from paperX_shale_p2_dyn_ip import bellman_ford_path_resistance, p2nu
from scipy import ndimage

# ============================================================
# Washburn 常数（归一化 K=1，阈值 U=1/r）
# ============================================================
R_MIN = 1.0    # 归一化最小孔径（对应最大压力/阈值）
R_MAX = 100.0  # 归一化最大孔径（对应最小压力/阈值）


# ============================================================
# 1. 分形孔隙网络生成
# ============================================================

def fractal_pore_network(n, phi, D, seed=0):
    """生成分形孔径分布的 3D 孔隙网络。

    孔径采样：f(r) ∝ r^{D-3}，逆变换法
    阈值映射：U_i = K/r_i = 1/r_i（Washburn，K=1 归一化）

    返回：binary, radii, lambdas, U
    """
    rng = np.random.default_rng(seed)
    binary = rng.random((n, n, n)) < phi

    # 逆变换采样：r = [r_min^(D-2) + T*(r_max^(D-2) - r_min^(D-2))]^(1/(D-2))
    T = rng.random((n, n, n))
    exp = D - 2
    radii = (R_MIN**exp + T * (R_MAX**exp - R_MIN**exp))**(1.0 / exp)
    radii = np.where(binary, radii, 1.0)  # 固体处占位

    # 谱参数 λ = 1/r
    lambdas = np.where(binary, 1.0 / radii, 0.0)

    # Washburn 阈值 U = 1/r（固体处 2.0 = 不可侵入）
    U = np.where(binary, 1.0 / radii, 2.0)

    return binary, radii, lambdas, U


# ============================================================
# 2. 分形驱动 DIP
# ============================================================

def run_fractal_dip(binary, U, c=0.0, seed=0, res_model=0):
    """分形驱动 DIP：用分形孔径的 Washburn 阈值运行动态侵入渗流。

    c=0：纯毛细极限（阈值 = Washburn 毛管压力）
    c>0：粘性-毛细竞争（有效阈值 = U + c·R_path）
    """
    nz, ny, nx = binary.shape

    if c == 0.0:
        U_eff = U.copy()
    else:
        if res_model == 0:
            r_res = np.ones(binary.shape)
        else:
            r_res = 0.5 + U
        R_path = bellman_ford_path_resistance(
            binary.ravel(), r_res.ravel(), nx, ny, nz
        ).reshape(binary.shape)
        U_eff = U + c * R_path

    pore_idx = np.flatnonzero(binary.ravel())
    Uf = U_eff.ravel()
    order = pore_idx[np.argsort(Uf[pore_idx])]

    P_arr, S_arr, P_c, S_c = ip_union_entry(binary, Uf, order)

    return P_arr, S_arr, P_c, S_c, order, Uf


# ============================================================
# 3. 谱带映射
# ============================================================

def reconstruct_invasion(binary, U_eff_flat, P_level):
    """在给定压力水平重建侵入图样：激活 U_eff ≤ P_level 的孔隙，
    标记与入口面(z=0)连通的簇。"""
    nz, ny, nx = binary.shape
    active = (U_eff_flat <= P_level).reshape(nz, ny, nx)

    labeled, _ = ndimage.label(active, structure=np.ones((3, 3, 3)))

    # 入口面簇标签
    inlet_labels = np.unique(labeled[0])
    inlet_labels = inlet_labels[inlet_labels > 0]

    if len(inlet_labels) == 0:
        return np.zeros_like(binary, dtype=bool)

    invaded = np.isin(labeled, inlet_labels)
    return invaded


def spectral_band_mapping(binary, lambdas, P_arr, P_c, U_eff_flat, n_bands=20):
    """谱带映射：在多个压力水平计算 A_t(λ)。

    A_t(λ_k) = 侵入孔隙中 λ ≤ λ_k 的比例 / 总孔隙数
    """
    n_pore = binary.sum()
    lam_pore = lambdas[binary]
    lam_min, lam_max = lam_pore.min(), lam_pore.max()
    lambda_edges = np.logspace(np.log10(lam_min), np.log10(lam_max), n_bands + 1)

    # 选择压力水平（突破前后各取点）
    P_min = P_arr.min() if len(P_arr) > 0 else 0.01
    P_max = P_arr.max() if len(P_arr) > 0 else 1.0
    if P_c > 0 and P_c < 1e6:
        pressures = np.unique(np.concatenate([
            np.linspace(P_min, P_c * 0.95, 3),
            [P_c],
            np.linspace(P_c * 1.05, P_max, 4),
        ]))
        pressures = pressures[pressures > 0]
    else:
        pressures = np.linspace(P_min, P_max, 8)

    A_t = np.zeros((len(pressures), n_bands))
    snapshots = []

    for i, P in enumerate(pressures):
        invaded = reconstruct_invasion(binary, U_eff_flat, P)
        snapshots.append(invaded)

        lam_inv = lambdas[invaded]
        for k in range(n_bands):
            A_t[i, k] = np.sum(lam_inv <= lambda_edges[k + 1]) / n_pore

    return pressures, A_t, lambda_edges, snapshots


# ============================================================
# 4. P1 涌现验证
# ============================================================

def extract_p1(results):
    """P1 涌现：从 D 扫描结果提取 ln P_t vs 1/(D-2) 线性拟合。
    取 c=0（毛细极限）的突破压力 P_c 作为 P_t 的代理。
    """
    D_vals, Pt_vals = [], []

    for D in sorted(results.keys()):
        if 0.0 in results[D]:
            P_c = results[D][0.0]['P_c']
            if P_c > 0 and P_c < 1e6:
                D_vals.append(D)
                Pt_vals.append(P_c)

    D_vals = np.array(D_vals)
    Pt_vals = np.array(Pt_vals)

    if len(D_vals) < 3:
        return D_vals, Pt_vals, np.nan, np.nan, 0.0

    ln_Pt = np.log(Pt_vals)
    inv_D2 = 1.0 / (D_vals - 2)

    A_ = np.vstack([inv_D2, np.ones_like(inv_D2)]).T
    C, B = np.linalg.lstsq(A_, ln_Pt, rcond=None)[0]
    pred = C * inv_D2 + B
    ss_res = np.sum((ln_Pt - pred) ** 2)
    ss_tot = np.sum((ln_Pt - ln_Pt.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    return D_vals, Pt_vals, C, B, r2


# ============================================================
# 5. P2 涌现验证（复用 p2nu）
# ============================================================

def extract_p2(P_arr, S_arr, P_c):
    """P2 涌现：突破后窗口 ν 拟合。"""
    if P_c < 0 or P_c > 1e6:
        return None
    return p2nu(P_arr, S_arr, P_c)


# ============================================================
# 6. P3 涌现验证（骨架提取 + 盒计数维数）
# ============================================================

def extract_backbone(cluster_3d):
    """提取侵入簇骨架（burning algorithm）。

    骨架 = 从入口面和出口面均可到达的孔隙集合（去除 dangling ends）。

    使用 scipy.ndimage 迭代膨胀实现 BFS：
    1. 从入口面(z=0)膨胀（mask=cluster），得到 inlet_reachable
    2. 从出口面(z=N-1)膨胀（mask=cluster），得到 outlet_reachable
    3. 骨架 = inlet_reachable ∩ outlet_reachable
    """
    structure = np.ones((3, 3, 3))

    # 入口面种子
    seed_in = np.zeros_like(cluster_3d)
    seed_in[0] = cluster_3d[0]

    inlet_reachable = seed_in.copy()
    while True:
        new = ndimage.binary_dilation(inlet_reachable, structure=structure) & cluster_3d
        if np.array_equal(new, inlet_reachable):
            break
        inlet_reachable = new

    # 出口面种子
    seed_out = np.zeros_like(cluster_3d)
    seed_out[-1] = cluster_3d[-1]

    outlet_reachable = seed_out.copy()
    while True:
        new = ndimage.binary_dilation(outlet_reachable, structure=structure) & cluster_3d
        if np.array_equal(new, outlet_reachable):
            break
        outlet_reachable = new

    backbone = inlet_reachable & outlet_reachable
    return backbone


def extract_backbone_fast(cluster_3d):
    """快速骨架提取（scipy.sparse.csgraph BFS，O(V+E)）。

    优化原理：入侵簇按定义已与入口面连通，故
      骨架 = 入口可达 ∩ 出口可达 = 出口可达（在簇内）
    只需从出口面做一次 BFS，无需从入口面 BFS。

    对 L=256（V~255K, E~3M）约 2-5s，对比迭代膨胀 ~500s+。
    """
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import breadth_first_order

    nz, ny, nx = cluster_3d.shape

    # 1. 簇体素 → 节点 ID 映射
    pore_coords = np.argwhere(cluster_3d)
    if len(pore_coords) == 0:
        return np.zeros_like(cluster_3d)

    n_nodes = len(pore_coords)
    node_id = np.full(cluster_3d.shape, -1, dtype=np.int64)
    node_id[cluster_3d] = np.arange(n_nodes)

    # 2. 构建邻接边（13 个正向偏移，无向图去重）
    edges_u = []
    edges_v = []
    half_offsets = [
        (0, 0, 1), (0, 1, 0), (0, 1, 1), (0, 1, -1),
        (1, -1, -1), (1, -1, 0), (1, -1, 1),
        (1, 0, -1), (1, 0, 0), (1, 0, 1),
        (1, 1, -1), (1, 1, 0), (1, 1, 1),
    ]

    for dz, dy, dx in half_offsets:
        z_dst = pore_coords[:, 0] + dz
        y_dst = pore_coords[:, 1] + dy
        x_dst = pore_coords[:, 2] + dx

        valid = ((z_dst >= 0) & (z_dst < nz) &
                 (y_dst >= 0) & (y_dst < ny) &
                 (x_dst >= 0) & (x_dst < nx))

        if not valid.any():
            continue

        dst_ids = node_id[z_dst[valid], y_dst[valid], x_dst[valid]]
        src_ids = np.arange(n_nodes)[valid]

        mask = dst_ids >= 0
        edges_u.append(src_ids[mask])
        edges_v.append(dst_ids[mask])

    if not edges_u:
        return np.zeros_like(cluster_3d)

    edges_u = np.concatenate(edges_u)
    edges_v = np.concatenate(edges_v)

    # 对称化（无向图）
    all_u = np.concatenate([edges_u, edges_v])
    all_v = np.concatenate([edges_v, edges_u])
    data = np.ones(len(all_u), dtype=np.int8)
    adj = csr_matrix((data, (all_u, all_v)), shape=(n_nodes, n_nodes))

    # 3. 从出口面多源 BFS（超源点技巧）
    outlet_nodes = node_id[-1][cluster_3d[-1]]
    outlet_nodes = outlet_nodes[outlet_nodes >= 0]

    if len(outlet_nodes) == 0:
        return np.zeros_like(cluster_3d)

    ss = n_nodes  # 超源点 ID
    ss_u = np.concatenate([all_u, np.full(len(outlet_nodes), ss), outlet_nodes.astype(np.int64)])
    ss_v = np.concatenate([all_v, outlet_nodes.astype(np.int64), np.full(len(outlet_nodes), ss)])
    ss_data = np.ones(len(ss_u), dtype=np.int8)
    adj_ext = csr_matrix((ss_data, (ss_u, ss_v)), shape=(n_nodes + 1, n_nodes + 1))

    reachable = breadth_first_order(adj_ext, i_start=ss, directed=False, return_predecessors=False)

    # 4. 构建 backbone 掩码（排除超源点）
    backbone = np.zeros_like(cluster_3d)
    reachable = reachable[reachable != ss]
    if len(reachable) > 0:
        coords = pore_coords[reachable]
        backbone[coords[:, 0], coords[:, 1], coords[:, 2]] = True

    return backbone


def extract_red_bonds(cluster_3d, backbone=None):
    """提取红键（singly connected bonds / cutting bonds）。

    红键 = 骨架中移除后会使入口-出口断开的孔隙。
    3D 渗流理论：红键维数 D_red = 1/ν ≈ 1.14（ν=0.876）。

    算法：
    1. 先提取骨架（如未提供）
    2. 从入口/出口双向 BFS，得到 t_in/t_out
    3. 测地线长度 L = min(t_in + t_out)
    4. 候选红键 = {s : t_in(s) + t_out(s) = L}（测地线上的点）
    5. 对每个候选点，移除后检验连通性
    """
    if backbone is None:
        backbone = extract_backbone(cluster_3d)

    if not backbone.any():
        return np.zeros_like(cluster_3d)

    structure = np.ones((3, 3, 3))
    nz = cluster_3d.shape[0]

    # 1. 从入口 BFS，记录"燃烧层数"（BFS distance）
    t_in = np.full(cluster_3d.shape, -1, dtype=np.int32)
    current = np.zeros_like(cluster_3d)
    current[0] = backbone[0]
    t_in[current] = 0
    layer = 0
    while current.any():
        layer += 1
        new = ndimage.binary_dilation(current, structure=structure) & backbone & (t_in < 0)
        if not new.any():
            break
        t_in[new] = layer
        current = new

    # 2. 从出口 BFS
    t_out = np.full(cluster_3d.shape, -1, dtype=np.int32)
    current = np.zeros_like(cluster_3d)
    current[-1] = backbone[-1]
    t_out[current] = 0
    layer = 0
    while current.any():
        layer += 1
        new = ndimage.binary_dilation(current, structure=structure) & backbone & (t_out < 0)
        if not new.any():
            break
        t_out[new] = layer
        current = new

    # 3. 测地线长度
    t_sum = t_in.astype(np.int64) + t_out.astype(np.int64)
    valid = (t_in >= 0) & (t_out >= 0)
    if not valid.any():
        return np.zeros_like(cluster_3d)
    L = t_sum[valid].min()

    # 4. 候选红键：测地线上的点
    candidates = valid & (t_sum == L)
    n_cand = candidates.sum()

    if n_cand == 0:
        return np.zeros_like(cluster_3d)

    # 5. 逐个检验：移除候选点后是否仍连通
    red_bonds = np.zeros_like(cluster_3d)
    coords = np.argwhere(candidates)

    for idx in range(len(coords)):
        z, y, x = coords[idx]
        # 移除该点
        test_bb = backbone.copy()
        test_bb[z, y, x] = False

        # 检验入口到出口是否仍连通
        # 从入口燃烧
        seed = np.zeros_like(test_bb)
        seed[0] = test_bb[0]
        reach = seed.copy()
        while True:
            new = ndimage.binary_dilation(reach, structure=structure) & test_bb
            if np.array_equal(new, reach):
                break
            reach = new

        # 如果出口面不可达 → 红键
        if not reach[-1].any():
            red_bonds[z, y, x] = True

    return red_bonds


def extract_red_bonds_tarjan(cluster_3d, backbone=None):
    """Tarjan 桥边算法提取红键（O(V+E)，比 per-candidate BFS 快 100-1000 倍）。

    红键 = 骨架图的桥边（移除后使入口-出口断开的边）。

    算法：
    1. 将骨架体素转换为图（6-邻接或26-邻接）
    2. 添加超级源点 s（连接入口面所有体素）和超级汇点 t（连接出口面所有体素）
    3. 在图上运行 Tarjan 桥边算法：边 (u,v) 是桥边 ⟺ low[v] > disc[u]
    4. 桥边对应的体素对即为红键

    注意：红键是"体素"而非"边"。这里将桥边的两个端点体素都标记为红键。
    """
    if backbone is None:
        backbone = extract_backbone(cluster_3d)

    if not backbone.any():
        return np.zeros_like(cluster_3d)

    nz, ny, nx = backbone.shape

    # 1. 将骨架体素映射为图节点（线性索引）
    pore_coords = np.argwhere(backbone)
    if len(pore_coords) == 0:
        return np.zeros_like(cluster_3d)

    # 建立体素到节点ID的映射
    node_id = np.full(backbone.shape, -1, dtype=np.int64)
    node_id[backbone] = np.arange(len(pore_coords))
    n_nodes = len(pore_coords)

    # 2. 构建邻接表（26-邻接，与 burning algorithm 的 3x3x3 structure 一致）
    # 用 CSR 格式
    # 遍历 26 个方向，对每个方向检查邻接
    adj = [[] for _ in range(n_nodes)]
    offsets = []
    for dz in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dz == 0 and dy == 0 and dx == 0:
                    continue
                offsets.append((dz, dy, dx))

    for idx in range(n_nodes):
        z, y, x = pore_coords[idx]
        for dz, dy, dx in offsets:
            z2, y2, x2 = z + dz, y + dy, x + dx
            if 0 <= z2 < nz and 0 <= y2 < ny and 0 <= x2 < nx:
                if node_id[z2, y2, x2] >= 0:
                    neighbor = node_id[z2, y2, x2]
                    if neighbor > idx:  # 避免重复
                        adj[idx].append(neighbor)
                        adj[neighbor].append(idx)

    # 3. 添加超级源点 s 和超级汇点 t
    # s = n_nodes, t = n_nodes + 1
    s = n_nodes
    t = n_nodes + 1
    n_total = n_nodes + 2

    # 扩展邻接表
    adj.append([])  # s
    adj.append([])  # t

    # s 连接入口面体素
    inlet_nodes = node_id[0][backbone[0]]
    inlet_nodes = inlet_nodes[inlet_nodes >= 0]
    for node in inlet_nodes:
        adj[s].append(int(node))
        adj[int(node)].append(s)

    # t 连接出口面体素
    outlet_nodes = node_id[-1][backbone[-1]]
    outlet_nodes = outlet_nodes[outlet_nodes >= 0]
    for node in outlet_nodes:
        adj[t].append(int(node))
        adj[int(node)].append(t)

    # 4. Tarjan 桥边算法（迭代版，避免递归栈溢出）
    disc = [-1] * n_total
    low = [0] * n_total
    visited = [False] * n_total
    parent = [-1] * n_total
    is_bridge = {}  # (min(u,v), max(u,v)) -> True
    timer = [0]

    # 迭代 DFS（只从 s 开始）
    stack = [(s, -1, iter(adj[s]))]
    visited[s] = True
    disc[s] = low[s] = timer[0]
    timer[0] += 1

    while stack:
        u, par, it = stack[-1]
        found_next = False
        for v in it:
            if v == par:
                continue
            if not visited[v]:
                visited[v] = True
                disc[v] = low[v] = timer[0]
                timer[0] += 1
                parent[v] = u
                stack.append((v, u, iter(adj[v])))
                found_next = True
                break
            else:
                low[u] = min(low[u], disc[v])
        if not found_next:
            stack.pop()
            if stack:
                par_u = stack[-1][0]
                low[par_u] = min(low[par_u], low[u])
                # 检查 (par_u, u) 是否为桥边
                if low[u] > disc[par_u]:
                    key = (min(par_u, u), max(par_u, u))
                    is_bridge[key] = True

    # 5. 找 s-t 路径（通过 parent 回溯）
    if not visited[t]:
        return np.zeros_like(cluster_3d)  # s 和 t 不连通

    st_path = []
    node = t
    while node != -1:
        st_path.append(node)
        node = parent[node]
    st_path.reverse()  # s -> ... -> t

    # 6. 在 s-t 路径上找桥边（红键）
    red_bonds = np.zeros_like(cluster_3d)
    for i in range(len(st_path) - 1):
        u = st_path[i]
        v = st_path[i + 1]
        key = (min(u, v), max(u, v))
        if key in is_bridge:
            # 桥边 (u,v) 在 s-t 路径上 → 红键
            # 跳过超级源点和超级汇点
            if u == s or u == t or v == s or v == t:
                continue
            z_u, y_u, x_u = pore_coords[u]
            z_v, y_v, x_v = pore_coords[v]
            red_bonds[z_u, y_u, x_u] = True
            red_bonds[z_v, y_v, x_v] = True

    return red_bonds


def extract_red_bonds_fast(cluster_3d, backbone=None, method='tarjan'):
    """快速红键提取（自动选择算法）。"""
    if method == 'tarjan':
        return extract_red_bonds_tarjan(cluster_3d, backbone)
    else:
        return extract_red_bonds(cluster_3d, backbone)


def box_counting_3d(cluster_3d):
    """3D 盒计数维数。返回 D_b, R²。"""
    nz, ny, nx = cluster_3d.shape
    n = max(nz, ny, nx)
    epsilons, counts = [], []

    for eps in [1, 2, 4, 8, 16, 32]:
        if eps > n:
            break
        nz2 = (nz // eps) * eps
        ny2 = (ny // eps) * eps
        nx2 = (nx // eps) * eps
        if nz2 == 0 or ny2 == 0 or nx2 == 0:
            continue
        sub = cluster_3d[:nz2, :ny2, :nx2]
        try:
            blocks = sub.reshape(nz2 // eps, eps, ny2 // eps, eps, nx2 // eps, eps)
            N = blocks.any(axis=(1, 3, 5)).sum()
        except ValueError:
            continue
        if N > 0:
            epsilons.append(eps)
            counts.append(N)

    if len(epsilons) < 3:
        return np.nan, 0.0

    ln_eps = np.log(epsilons)
    ln_N = np.log(counts)
    A_ = np.vstack([ln_eps, np.ones_like(ln_eps)]).T
    slope, _ = np.linalg.lstsq(A_, ln_N, rcond=None)[0]
    D_b = -slope

    pred = slope * ln_eps + np.linalg.lstsq(A_, ln_N, rcond=None)[0][1]
    ss_res = np.sum((ln_N - pred) ** 2)
    ss_tot = np.sum((ln_N - ln_N.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    return D_b, r2


def box_counting_1d_projection(cluster_3d):
    """1D 投影盒计数：将侵入簇投影到 z 轴（流动方向），做 1D 盒计数。
    理论 P3 预言 D_b = ln2/ln3 ≈ 0.631（IFS 三分结构）。
    """
    nz = cluster_3d.shape[0]
    # 投影：每个 z 切片是否有侵入孔隙
    projection = cluster_3d.any(axis=(1, 2))  # bool (nz,)

    epsilons, counts = [], []
    for eps in [1, 2, 4, 8, 16, 32]:
        if eps > nz:
            break
        nz2 = (nz // eps) * eps
        if nz2 == 0:
            continue
        sub = projection[:nz2]
        try:
            blocks = sub.reshape(nz2 // eps, eps)
            N = blocks.any(axis=1).sum()
        except ValueError:
            continue
        if N > 0:
            epsilons.append(eps)
            counts.append(N)

    if len(epsilons) < 3:
        return np.nan, 0.0

    ln_eps = np.log(epsilons)
    ln_N = np.log(counts)
    A_ = np.vstack([ln_eps, np.ones_like(ln_eps)]).T
    slope, intercept = np.linalg.lstsq(A_, ln_N, rcond=None)[0]
    D_b = -slope

    pred = slope * ln_eps + intercept
    ss_res = np.sum((ln_N - pred) ** 2)
    ss_tot = np.sum((ln_N - ln_N.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    return D_b, r2


def extract_p3(snapshots, pressures, P_c):
    """P3 涌现：突破时刻侵入簇的盒计数维数。

    测量四种维数：
    - Db_cluster: 全侵入簇 3D 盒计数
    - Db_backbone: 骨架（burning algorithm 去除 dangling ends）3D 盒计数
    - Db_bb_1d: 骨架 z 轴投影 1D 盒计数
    - Db_red: 红键（cutting bonds）3D 盒计数
    """
    if P_c < 0 or P_c > 1e6:
        return np.nan, 0.0, np.nan, 0.0, np.nan, 0.0, np.nan, 0.0

    idx = np.argmin(np.abs(pressures - P_c))
    cluster = snapshots[idx]

    if not cluster.any():
        return np.nan, 0.0, np.nan, 0.0, np.nan, 0.0, np.nan, 0.0

    # 全簇 3D 盒计数
    Db_cluster, r2_cluster = box_counting_3d(cluster)

    # 骨架提取 + 盒计数
    backbone = extract_backbone(cluster)
    if backbone.any():
        Db_bb, r2_bb = box_counting_3d(backbone)
        Db_bb_1d, r2_bb_1d = box_counting_1d_projection(backbone)
    else:
        Db_bb, r2_bb = np.nan, 0.0
        Db_bb_1d, r2_bb_1d = np.nan, 0.0

    # 红键提取 + 盒计数（使用 Tarjan 桥边算法，O(V+E)）
    red = extract_red_bonds_fast(cluster, backbone=backbone, method='tarjan')
    if red.any():
        Db_red, r2_red = box_counting_3d(red)
    else:
        Db_red, r2_red = np.nan, 0.0

    return Db_cluster, r2_cluster, Db_bb, r2_bb, Db_bb_1d, r2_bb_1d, Db_red, r2_red


# ============================================================
# 7. 谱流方程验证（显式生成元分解）
# ============================================================

def verify_spectral_flow(pressures, A_t, lambdas, binary, U_eff_flat, lambda_edges):
    """谱流方程验证：显式构造生成元 g_inj / g_cap，检验 dA_t/dt = g_inj - g_cap。

    生成元物理含义：
      g_inj(λ_k): 注入驱动——压力升高 dP 时，谱带 k 中阈值被跨越的孔隙比例
                  （仅依赖孔径分布 + Washburn 阈值，与连通性无关）
      g_cap(λ_k): 谱隙阻挡——g_inj 中被毛管封堵（未连通入口）的部分
                  g_cap = g_inj - dA_t/dt

    验证判据：
      1. 恒等检验：dA_t/dt = g_inj - g_cap（R² 应为 1.0，sanity check）
      2. 物理签名：g_cap 应集中在谱隙 λ_t 附近（峰值/均值比 > 1）
      3. D 依赖：g_cap 峰值应随 D 增大而增大（小孔多→封堵强）
    """
    n_levels, n_bands = A_t.shape
    if n_levels < 3:
        return None

    n_pore = binary.sum()
    lam_pore = lambdas[binary]
    U_pore = U_eff_flat[binary.ravel()]

    # 将孔隙分配到谱带
    band_idx = np.searchsorted(lambda_edges[1:], lam_pore)  # 0..n_bands-1
    band_idx = np.clip(band_idx, 0, n_bands - 1)

    # 计算每个压力步的 g_inj（阈值跨越率）
    g_inj = np.zeros((n_levels - 1, n_bands))
    for i in range(n_levels - 1):
        P_lo, P_hi = pressures[i], pressures[i + 1]
        # 在 [P_lo, P_hi) 内阈值被跨越的孔隙
        crossed = (U_pore >= P_lo) & (U_pore < P_hi)
        for k in range(n_bands):
            g_inj[i, k] = np.sum(crossed & (band_idx == k)) / n_pore

    # dA_t/dt（实际侵入速率）
    dA_dt = np.diff(A_t, axis=0)

    # g_cap = g_inj - dA_t/dt（被封堵的部分）
    g_cap = g_inj - dA_dt

    # 1. 恒等检验（sanity check）
    pred = g_inj - g_cap  # = dA_dt by construction
    ss_res = np.sum((dA_dt - pred) ** 2)
    ss_tot = np.sum(dA_dt ** 2)
    r2_identity = 1 - ss_res / ss_tot if ss_tot > 1e-20 else 1.0

    # 2. 物理签名：g_cap 的集中度（峰值/均值比）
    g_cap_mean_over_time = np.mean(np.abs(g_cap), axis=0)  # 各谱带的 |g_cap| 时间平均
    g_cap_peak = np.max(g_cap_mean_over_time)
    g_cap_mean = np.mean(g_cap_mean_over_time)
    sharpness = g_cap_peak / g_cap_mean if g_cap_mean > 1e-12 else 0

    # 3. 谱隙位置：g_cap 峰值对应的谱带
    gap_band = np.argmax(g_cap_mean_over_time)
    gap_lambda = lambda_edges[gap_band]

    # 4. g_inj 与 dA_t/dt 的逐带相关性（非平凡检验）
    # g_inj 是独立计算的，dA_t/dt 是仿真结果
    # 如果谱流方程成立，dA_t/dt 应与 g_inj 线性相关（斜率 < 1，因为 g_cap 扣除了一部分）
    r2_list = []
    for k in range(n_bands):
        y = dA_dt[:, k]
        x = g_inj[:, k]
        if np.std(y) < 1e-12 or np.std(x) < 1e-12:
            r2_list.append(0.0)
            continue
        A_ = np.vstack([x, np.ones_like(x)]).T
        a, b = np.linalg.lstsq(A_, y, rcond=None)[0]
        pred_k = a * x + b
        ss_res_k = np.sum((y - pred_k) ** 2)
        ss_tot_k = np.sum((y - y.mean()) ** 2)
        r2_list.append(1 - ss_res_k / ss_tot_k if ss_tot_k > 0 else 0)

    r2_arr = np.array(r2_list)

    return {
        'r2_identity': r2_identity,
        'r2_mean': r2_arr.mean(),
        'r2_max': r2_arr.max(),
        'sharpness': sharpness,
        'gap_band': gap_band,
        'gap_lambda': gap_lambda,
        'g_cap_peak': g_cap_peak,
        'g_cap_profile': g_cap_mean_over_time,
        'g_inj': g_inj,
        'dA_dt': dA_dt,
    }


def verify_spectral_flow_nonlinear(pressures, A_t, lambdas, binary, U_eff_flat, lambda_edges):
    """非线性修正验证：引入渗流雪崩反馈项 g_nl。

    修正模型：dA_t/dt = g_inj × F(A_t) - g_cap_base

    其中 F(A_t) = 1 + κ × A_t × (1 - A_t/A_active) 为可达性因子：
      - A_t × (1 - A_t/A_active)：logistic 项，在 A_t = A_active/2 处达峰（雪崩最强）
      - κ(c, D)：非线性耦合系数，c→∞ 时 κ→0

    线性回归：dA_t/dt / g_inj = 1 + κ × L
    其中 L = A_t × (1 - A_t/A_active)（logistic 变量）
    """
    n_levels, n_bands = A_t.shape
    if n_levels < 3:
        return None

    n_pore = binary.sum()
    lam_pore = lambdas[binary]
    U_pore = U_eff_flat[binary.ravel()]

    band_idx = np.searchsorted(lambda_edges[1:], lam_pore)
    band_idx = np.clip(band_idx, 0, n_bands - 1)

    # g_inj（独立计算）
    g_inj = np.zeros((n_levels - 1, n_bands))
    for i in range(n_levels - 1):
        P_lo, P_hi = pressures[i], pressures[i + 1]
        crossed = (U_pore >= P_lo) & (U_pore < P_hi)
        for k in range(n_bands):
            g_inj[i, k] = np.sum(crossed & (band_idx == k)) / n_pore

    dA_dt = np.diff(A_t, axis=0)

    # A_active：每个压力水平的可用孔隙比例（阈值已跨越，与连通性无关）
    A_active = np.zeros((n_levels, n_bands))
    for i in range(n_levels):
        P = pressures[i]
        active = (U_pore <= P)
        for k in range(n_bands):
            A_active[i, k] = np.sum(active & (band_idx == k)) / n_pore

    # A_active 对应 dA_dt 的区间（取前 n_levels-1 行的起点）
    A_active_mid = A_active[:-1]  # 用区间起点

    # logistic 变量 L = A_t × (1 - A_t / A_active)
    A_t_mid = A_t[:-1]
    # 避免除零（安全除法：先替换分母零值为 1，再 where 选择）
    safe_denom = np.where(A_active_mid > 1e-10, A_active_mid, 1.0)
    ratio_raw = A_t_mid / safe_denom
    ratio = np.where(A_active_mid > 1e-10, ratio_raw, 1.0)
    L = A_t_mid * (1.0 - np.clip(ratio, 0, 1))

    # 线性回归：dA_t/dt / g_inj = 1 + κ × L
    # 只用 g_inj > 0 的点
    mask = g_inj > 1e-10
    if np.sum(mask) < 5:
        return None

    y = (dA_dt[mask] / g_inj[mask]).ravel()
    x = L[mask].ravel()

    # 去除 NaN/Inf
    valid = np.isfinite(y) & np.isfinite(x)
    y, x = y[valid], x[valid]

    if len(y) < 5 or np.std(x) < 1e-15:
        return None

    # 拟合 y = 1 + κ × x（截距固定为 1）
    # 等价于 y - 1 = κ × x
    kappa = np.sum((y - 1) * x) / np.sum(x * x) if np.sum(x * x) > 1e-20 else 0.0
    pred = 1 + kappa * x
    ss_res = np.sum((y - pred) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2_nonlinear = 1 - ss_res / ss_tot if ss_tot > 1e-20 else 1.0

    # 也计算自由截距拟合（用于对比）
    A_ = np.vstack([x, np.ones_like(x)]).T
    a, b = np.linalg.lstsq(A_, y, rcond=None)[0]
    pred_free = a * x + b
    ss_res_free = np.sum((y - pred_free) ** 2)
    r2_free = 1 - ss_res_free / ss_tot if ss_tot > 1e-20 else 1.0

    # 线性模型 R²（g_inj vs dA_t/dt，不除以 g_inj）
    r2_linear_list = []
    for k in range(n_bands):
        yk = dA_dt[:, k]
        xk = g_inj[:, k]
        if np.std(yk) < 1e-12 or np.std(xk) < 1e-12:
            continue
        A_ = np.vstack([xk, np.ones_like(xk)]).T
        ak, bk = np.linalg.lstsq(A_, yk, rcond=None)[0]
        pred_k = ak * xk + bk
        ss_res_k = np.sum((yk - pred_k) ** 2)
        ss_tot_k = np.sum((yk - yk.mean()) ** 2)
        r2_linear_list.append(1 - ss_res_k / ss_tot_k if ss_tot_k > 0 else 0)
    r2_linear = np.mean(r2_linear_list) if r2_linear_list else 0

    # 非线性修正后的 R²：dA_t/dt vs g_inj × (1 + κ × L)
    g_inj_corrected = g_inj * (1 + kappa * L)
    r2_corrected_list = []
    for k in range(n_bands):
        yk = dA_dt[:, k]
        xk = g_inj_corrected[:, k]
        if np.std(yk) < 1e-12 or np.std(xk) < 1e-12:
            continue
        A_ = np.vstack([xk, np.ones_like(xk)]).T
        ak, bk = np.linalg.lstsq(A_, yk, rcond=None)[0]
        pred_k = ak * xk + bk
        ss_res_k = np.sum((yk - pred_k) ** 2)
        ss_tot_k = np.sum((yk - yk.mean()) ** 2)
        r2_corrected_list.append(1 - ss_res_k / ss_tot_k if ss_tot_k > 0 else 0)
    r2_corrected = np.mean(r2_corrected_list) if r2_corrected_list else 0

    return {
        'kappa': kappa,
        'r2_linear': r2_linear,
        'r2_nonlinear': r2_nonlinear,
        'r2_free': r2_free,
        'r2_corrected': r2_corrected,
        'n_points': len(y),
    }


# ============================================================
# 8. 主函数
# ============================================================

def main():
    # 支持命令行快速测试：python paper43_coupled_spectral_dip.py quick
    quick = len(sys.argv) > 1 and sys.argv[1] == 'quick'
    N = 16 if quick else 64
    D_LIST = [2.4, 2.8] if quick else [2.2, 2.4, 2.6, 2.8, 3.0, 3.2]
    C_LIST = [0.0, 1.0] if quick else [0.0, 0.3, 1.0]
    PHI = 0.31
    N_CFG = 1 if quick else 2
    PC_CAP = 1e6

    print("=" * 80)
    print("Paper43 耦合谱流-DIP 正向仿真")
    print(f"参数：{N}³, D∈{D_LIST}, c∈{C_LIST}, φ={PHI}, ncfg={N_CFG}")
    print("=" * 80)

    results = {}

    for D in D_LIST:
        results[D] = {}
        for c in C_LIST:
            Pcs, Scs, nus, nu_r2s = [], [], [], []
            Db_cls, Db_cls_r2 = [], []
            Db_bb, Db_bb_r2 = [], []
            Db_bb1d, Db_bb1d_r2 = [], []
            Db_red, Db_red_r2 = [], []
            sf_r2s, sf_sharpness, sf_gap_lambdas = [], [], []
            sf_kappas, sf_r2_lin, sf_r2_corr = [], [], []
            sf_sigmas = []

            for cfg in range(N_CFG):
                seed = cfg * 1000 + int(D * 100) + int(c * 100)
                binary, radii, lambdas, U = fractal_pore_network(N, PHI, D, seed=seed)

                P_arr, S_arr, P_c, S_c, order, Uf = run_fractal_dip(
                    binary, U, c=c, seed=seed
                )

                if P_c < 0 or P_c > PC_CAP:
                    continue

                # P2
                nu_res = extract_p2(P_arr, S_arr, P_c)
                if nu_res:
                    nus.append(nu_res[0])
                    nu_r2s.append(nu_res[1])

                # 谱带映射 + P3 + 谱流
                pressures, A_t, lam_edges, snapshots = spectral_band_mapping(
                    binary, lambdas, P_arr, P_c, Uf
                )

                Db_c, r2_c, Db_b, r2_b, Db_b1, r2_b1, Db_rd, r2_rd = extract_p3(snapshots, pressures, P_c) if c == 0.0 else (np.nan,0,np.nan,0,np.nan,0,np.nan,0)
                if not np.isnan(Db_c):
                    Db_cls.append(Db_c)
                    Db_cls_r2.append(r2_c)
                if not np.isnan(Db_b):
                    Db_bb.append(Db_b)
                    Db_bb_r2.append(r2_b)
                if not np.isnan(Db_b1):
                    Db_bb1d.append(Db_b1)
                    Db_bb1d_r2.append(r2_b1)
                if not np.isnan(Db_rd):
                    Db_red.append(Db_rd)
                    Db_red_r2.append(r2_rd)

                sf_res = verify_spectral_flow(pressures, A_t, lambdas, binary, Uf, lam_edges)
                if sf_res:
                    sf_r2s.append(sf_res['r2_mean'])
                    sf_sharpness.append(sf_res['sharpness'])
                    sf_gap_lambdas.append(sf_res['gap_lambda'])

                    # Langevin 噪声幅度：线性回归残差的标准差
                    # 残差 = dA_t/dt - alpha * g_inj（逐带线性回归）
                    # 注意：sigma 计算只依赖 sf_res（g_inj / dA_dt），不依赖 sf_nl
                    g_inj_arr = sf_res['g_inj']
                    dA_dt_arr = sf_res['dA_dt']
                    residuals = []
                    for k in range(g_inj_arr.shape[1]):
                        xk = g_inj_arr[:, k]
                        yk = dA_dt_arr[:, k]
                        if np.std(xk) < 1e-12 or np.std(yk) < 1e-12:
                            continue
                        A_ = np.vstack([xk, np.ones_like(xk)]).T
                        a, b = np.linalg.lstsq(A_, yk, rcond=None)[0]
                        residuals.extend(yk - a * xk - b)
                    if residuals:
                        sf_sigmas.append(np.std(residuals))

                # 非线性修正验证（与 sigma 解耦）
                sf_nl = verify_spectral_flow_nonlinear(pressures, A_t, lambdas, binary, Uf, lam_edges)
                if sf_nl:
                    sf_kappas.append(sf_nl['kappa'])
                    sf_r2_lin.append(sf_nl['r2_linear'])
                    sf_r2_corr.append(sf_nl['r2_corrected'])

                Pcs.append(P_c)
                Scs.append(S_c)

            if not Pcs:
                print(f"  D={D:.1f} c={c:.1f}: no breakthrough")
                continue

            results[D][c] = {
                'P_c': np.mean(Pcs),
                'S_c': np.mean(Scs),
                'nu': np.mean(nus) if nus else np.nan,
                'nu_r2': np.mean(nu_r2s) if nu_r2s else np.nan,
                'Db_cluster': np.mean(Db_cls) if Db_cls else np.nan,
                'Db_cluster_r2': np.mean(Db_cls_r2) if Db_cls_r2 else np.nan,
                'Db_backbone': np.mean(Db_bb) if Db_bb else np.nan,
                'Db_backbone_r2': np.mean(Db_bb_r2) if Db_bb_r2 else np.nan,
                'Db_bb_1d': np.mean(Db_bb1d) if Db_bb1d else np.nan,
                'Db_bb_1d_r2': np.mean(Db_bb1d_r2) if Db_bb1d_r2 else np.nan,
                'Db_red': np.mean(Db_red) if Db_red else np.nan,
                'Db_red_r2': np.mean(Db_red_r2) if Db_red_r2 else np.nan,
                'sf_r2': np.mean(sf_r2s) if sf_r2s else np.nan,
                'sf_sharpness': np.mean(sf_sharpness) if sf_sharpness else np.nan,
                'sf_gap_lambda': np.mean(sf_gap_lambdas) if sf_gap_lambdas else np.nan,
                'sf_kappa': np.mean(sf_kappas) if sf_kappas else np.nan,
                'sf_r2_linear': np.mean(sf_r2_lin) if sf_r2_lin else np.nan,
                'sf_r2_corrected': np.mean(sf_r2_corr) if sf_r2_corr else np.nan,
                'sf_sigma': np.mean(sf_sigmas) if sf_sigmas else np.nan,
                'n_break': len(Pcs),
            }

            r = results[D][c]
            print(f"  D={D:.1f} c={c:.1f}: P_c={r['P_c']:.4f} S_c={r['S_c']*100:.1f}% "
                  f"nu={r['nu']:.3f}(R2={r['nu_r2']:.3f}) "
                  f"Db_cl={r['Db_cluster']:.3f} Db_bb={r['Db_backbone']:.3f} "
                  f"Db_red={r['Db_red']:.3f} "
                  f"SF_R2={r['sf_r2']:.3f} sigma={r['sf_sigma']:.5f} "
                  f"n={r['n_break']}", flush=True)

    # ========== P1 涌现 ==========
    print("\n" + "=" * 80)
    print("P1 涌现验证：ln P_t vs 1/(D-2)")
    print("=" * 80)
    D_vals, Pt_vals, C_fit, B_fit, r2_p1 = extract_p1(results)
    if len(D_vals) > 0:
        print(f"  D values: {D_vals}")
        print(f"  P_t values: {Pt_vals}")
        print(f"  ln P_t: {np.log(Pt_vals)}")
        print(f"  1/(D-2): {1.0/(D_vals-2)}")
        print(f"  拟合: ln P_t = {C_fit:.3f}/(D-2) + {B_fit:.3f}, R2={r2_p1:.3f}")
        print(f"  判定: R2 > 0.8 -> {'PASS' if r2_p1 > 0.8 else 'FAIL'}")
    else:
        print("  无有效数据")

    # ========== P2 漂移 ==========
    print("\n" + "=" * 80)
    print("P2 漂移验证：nu(D, c)")
    print("=" * 80)
    header = f"  {'D':>5}"
    for c in C_LIST:
        header += f" {'c='+str(c):>10}"
    print(header)
    for D in sorted(results.keys()):
        row = f"  {D:5.1f}"
        for c in C_LIST:
            if c in results[D] and not np.isnan(results[D][c]['nu']):
                row += f" {results[D][c]['nu']:10.3f}"
            else:
                row += f" {'N/A':>10}"
        print(row)

    # ========== P3 盒计数 ==========
    print("\n" + "=" * 80)
    print("P3 盒计数验证：cluster / backbone / red_bonds vs ln2/ln3=0.631, D_red=1.14")
    print("=" * 80)
    db_target = np.log(2) / np.log(3)
    db_red_target = 1.14  # 3D percolation red bond dimension
    for D in sorted(results.keys()):
        for c in C_LIST:
            if c in results[D] and not np.isnan(results[D][c]['Db_cluster']):
                r = results[D][c]
                red_str = f"Db_red={r['Db_red']:.3f}(R2={r['Db_red_r2']:.3f})" if not np.isnan(r['Db_red']) else "Db_red=N/A"
                print(f"  D={D:.1f} c={c:.1f}: "
                      f"Db_cl={r['Db_cluster']:.3f} "
                      f"Db_bb={r['Db_backbone']:.3f} "
                      f"{red_str} "
                      f"targets: IFS={db_target:.3f} red={db_red_target:.3f}")

    # ========== 谱流方程 ==========
    print("\n" + "=" * 80)
    print("谱流方程验证：g_inj / g_cap 显式分解")
    print("=" * 80)
    print(f"  {'D':>5} {'c':>5} {'R2(g_inj~dA/dt)':>15} {'sharpness':>10} {'gap_lambda':>12}")
    for D in sorted(results.keys()):
        for c in C_LIST:
            if c in results[D] and not np.isnan(results[D][c]['sf_r2']):
                r = results[D][c]
                tag = "PASS" if r['sf_r2'] > 0.7 else "marginal" if r['sf_r2'] > 0.3 else "FAIL"
                print(f"  {D:5.1f} {c:5.1f} {r['sf_r2']:15.3f} "
                      f"{r['sf_sharpness']:10.2f} {r['sf_gap_lambda']:12.4f} {tag}")
    # D 依赖性检验
    print("\n  g_cap sharpness D-dependence (c=0):")
    for D in sorted(results.keys()):
        if 0.0 in results[D] and not np.isnan(results[D][0.0]['sf_sharpness']):
            print(f"    D={D:.1f}: sharpness={results[D][0.0]['sf_sharpness']:.2f}")

    # 非线性修正对比
    print("\n" + "=" * 80)
    print("非线性修正验证：g_nl = kappa * g_inj * A_t * (1 - A_t/A_active)")
    print("=" * 80)
    print(f"  {'D':>5} {'c':>5} {'R2_linear':>10} {'kappa':>8} {'R2_corrected':>13} {'improvement':>12}")
    for D in sorted(results.keys()):
        for c in C_LIST:
            if c in results[D] and not np.isnan(results[D][c].get('sf_r2_linear', np.nan)):
                r = results[D][c]
                imp = r['sf_r2_corrected'] - r['sf_r2_linear']
                tag = "PASS" if r['sf_r2_corrected'] > 0.7 else "marginal"
                print(f"  {D:5.1f} {c:5.1f} {r['sf_r2_linear']:10.3f} "
                      f"{r['sf_kappa']:8.2f} {r['sf_r2_corrected']:13.3f} "
                      f"{imp:+12.3f} {tag}")

    # kappa 的 c 依赖性
    print("\n  kappa c-dependence (D=2.6):")
    for c in C_LIST:
        if c in results.get(2.6, {}) and not np.isnan(results[2.6][c].get('sf_kappa', np.nan)):
            print(f"    c={c:.1f}: kappa={results[2.6][c]['sf_kappa']:.2f}")

    # kappa 的 D 依赖性
    print("\n  kappa D-dependence (c=0):")
    for D in sorted(results.keys()):
        if 0.0 in results[D] and not np.isnan(results[D][0.0].get('sf_kappa', np.nan)):
            print(f"    D={D:.1f}: kappa={results[D][0.0]['sf_kappa']:.2f}")

    # Langevin 噪声幅度
    print("\n" + "=" * 80)
    print("Langevin 噪声幅度 sigma(D, c)")
    print("=" * 80)
    print(f"  {'D':>5} {'c':>5} {'sigma':>12} {'R2_linear':>10}")
    for D in sorted(results.keys()):
        for c in C_LIST:
            if c in results[D] and not np.isnan(results[D][c].get('sf_sigma', np.nan)):
                r = results[D][c]
                print(f"  {D:5.1f} {c:5.1f} {r['sf_sigma']:12.6f} {r['sf_r2_linear']:10.3f}")
    # sigma 的 c 依赖性
    print("\n  sigma c-dependence (D=2.6):")
    for c in C_LIST:
        if c in results.get(2.6, {}) and not np.isnan(results[2.6][c].get('sf_sigma', np.nan)):
            print(f"    c={c:.1f}: sigma={results[2.6][c]['sf_sigma']:.6f}")
    # sigma 的 D 依赖性
    print("\n  sigma D-dependence (c=0):")
    for D in sorted(results.keys()):
        if 0.0 in results[D] and not np.isnan(results[D][0.0].get('sf_sigma', np.nan)):
            print(f"    D={D:.1f}: sigma={results[D][0.0]['sf_sigma']:.6f}")

    # ========== 图件 ==========
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')
        os.makedirs(fig_dir, exist_ok=True)

        # 图1: P1 涌现
        if len(D_vals) >= 3:
            fig, ax = plt.subplots(figsize=(6, 5))
            inv_D2 = 1.0 / (D_vals - 2)
            ln_Pt = np.log(Pt_vals)
            ax.scatter(inv_D2, ln_Pt, c='red', s=80, zorder=5)
            x_fit = np.linspace(inv_D2.min(), inv_D2.max(), 50)
            ax.plot(x_fit, C_fit * x_fit + B_fit, 'b--',
                    label=f'fit: C={C_fit:.2f}, B={B_fit:.2f}, $R^2$={r2_p1:.3f}')
            ax.set_xlabel('1/(D-2)')
            ax.set_ylabel('ln $P_t$')
            ax.set_title('P1 Emergence: ln $P_t$ vs 1/(D-2)')
            ax.legend()
            ax.grid(True, alpha=0.3)
            fig.tight_layout()
            fig.savefig(os.path.join(fig_dir, 'paper43_p1_emergence.png'), dpi=150)
            plt.close(fig)
            print(f"\n图件已保存: {fig_dir}/paper43_p1_emergence.png")

        # 图2: P2 漂移
        fig, ax = plt.subplots(figsize=(7, 5))
        for c in C_LIST:
            Ds, nus = [], []
            for D in sorted(results.keys()):
                if c in results[D] and not np.isnan(results[D][c]['nu']):
                    Ds.append(D)
                    nus.append(results[D][c]['nu'])
            if Ds:
                ax.plot(Ds, nus, 'o-', label=f'c={c:.1f}')
        ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='mean-field 1/2')
        ax.set_xlabel('Fractal dimension D')
        ax.set_ylabel(r'$\nu$')
        ax.set_title(r'P2 Drift: $\nu(D, c)$')
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(fig_dir, 'paper43_p2_drift.png'), dpi=150)
        plt.close(fig)
        print(f"图件已保存: {fig_dir}/paper43_p2_drift.png")

        # 图3: P3 盒计数（cluster / backbone / backbone-1d / red_bonds 四格）
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes_flat = axes.ravel()
        # 四格：前三个目标线 ln2/ln3=0.631，红键目标线 D_red=1.14 + P3 预言 0.631
        labels = [
            ('Db_cluster', 'Cluster 3D', [db_target]),
            ('Db_backbone', 'Backbone 3D', [db_target]),
            ('Db_bb_1d', 'Backbone 1D proj', [db_target]),
            ('Db_red', 'Red bonds 3D', [db_target, db_red_target]),
        ]
        for col, (key, title, targets) in enumerate(labels):
            ax = axes_flat[col]
            for c in C_LIST:
                Ds, Dbs = [], []
                for D in sorted(results.keys()):
                    if c in results[D] and not np.isnan(results[D][c].get(key, np.nan)):
                        Ds.append(D)
                        Dbs.append(results[D][c][key])
                if Ds:
                    ax.plot(Ds, Dbs, 's-', label=f'c={c:.1f}')
            # 目标线
            styles = ['red', 'darkred']
            for ti, tgt in enumerate(targets):
                lbl = f'ln2/ln3={tgt:.3f}' if ti == 0 else f'D_red={tgt:.3f}'
                ax.axhline(y=tgt, color=styles[ti], linestyle='--', alpha=0.6, label=lbl)
            ax.set_xlabel('D')
            ax.set_ylabel('$D_b$')
            ax.set_title(f'P3: {title}')
            ax.legend(fontsize=8)
            ax.grid(True, alpha=0.3)

        fig.tight_layout()
        fig.savefig(os.path.join(fig_dir, 'paper43_p3_boxcount.png'), dpi=150)
        plt.close(fig)
        print(f"图件已保存: {fig_dir}/paper43_p3_boxcount.png")

        # 图4: Langevin 噪声幅度 sigma(D, c)
        fig, ax = plt.subplots(figsize=(7, 5))
        for c in C_LIST:
            Ds, sigs = [], []
            for D in sorted(results.keys()):
                if c in results[D] and not np.isnan(results[D][c].get('sf_sigma', np.nan)):
                    Ds.append(D)
                    sigs.append(results[D][c]['sf_sigma'])
            if Ds:
                ax.plot(Ds, sigs, 'o-', label=f'c={c:.1f}')
        ax.set_xlabel('Fractal dimension D')
        ax.set_ylabel(r'$\sigma(D, c)$')
        ax.set_title(r'Langevin noise amplitude $\sigma$ vs $D$ and $c$')
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(fig_dir, 'paper43_sigma_DC.png'), dpi=150)
        plt.close(fig)
        print(f"图件已保存: {fig_dir}/paper43_sigma_DC.png")

        # 图5: 非线性修正对比 R²_linear vs R²_corrected（c=0 为主）
        fig, ax = plt.subplots(figsize=(8, 5))
        width = 0.35
        Ds_plot = sorted(results.keys())
        x_pos = np.arange(len(Ds_plot))
        for ci, c in enumerate(C_LIST):
            r2_lin_vals, r2_corr_vals = [], []
            for D in Ds_plot:
                if c in results[D]:
                    r2_lin_vals.append(results[D][c].get('sf_r2_linear', np.nan))
                    r2_corr_vals.append(results[D][c].get('sf_r2_corrected', np.nan))
                else:
                    r2_lin_vals.append(np.nan)
                    r2_corr_vals.append(np.nan)
            r2_lin_vals = np.array(r2_lin_vals, dtype=float)
            r2_corr_vals = np.array(r2_corr_vals, dtype=float)
            offset = (ci - (len(C_LIST) - 1) / 2.0) * width * 2
            mask_valid = ~np.isnan(r2_lin_vals)
            if mask_valid.any():
                ax.bar(x_pos[mask_valid] + offset, r2_lin_vals[mask_valid], width,
                       label=f'R²_linear (c={c:.1f})', alpha=0.7, color=f'C{ci*2}')
                ax.bar(x_pos[mask_valid] + offset + width, r2_corr_vals[mask_valid], width,
                       label=f'R²_corrected (c={c:.1f})', alpha=0.7, color=f'C{ci*2+1}')
        ax.axhline(y=0.7, color='gray', linestyle=':', alpha=0.5, label='PASS threshold 0.7')
        ax.set_xticks(x_pos)
        ax.set_xticklabels([f'D={D:.1f}' for D in Ds_plot])
        ax.set_ylabel('$R^2$')
        ax.set_title('Nonlinear correction: $R^2_{linear}$ vs $R^2_{corrected}$\n(logistic $\\kappa$ feedback; deterministic correction fails)')
        ax.legend(fontsize=8, loc='lower right')
        ax.grid(True, alpha=0.3, axis='y')
        fig.tight_layout()
        fig.savefig(os.path.join(fig_dir, 'paper43_nonlinear_correction.png'), dpi=150)
        plt.close(fig)
        print(f"图件已保存: {fig_dir}/paper43_nonlinear_correction.png")

    except Exception as e:
        print(f"绘图跳过: {e}")

    print("\n" + "=" * 80)
    print("仿真完成")
    print("=" * 80)


if __name__ == "__main__":
    main()
