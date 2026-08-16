"""
P-CM-5 直接验证: ED 计算 N=14, 16 的 XXX 数据, 检验三重签名持续性

方法: 与 EDRN 原始脚本(stable_island_geometry.py / N_scan 版)物理一致
  - Heisenberg XXX 哈密顿量 (全空间), 矛盾边 J=Δ, 其他边 J=1
  - eigsh(which='SA') 求最低 5 特征值
  - gap = E1-E0, coarse = |<Sz_total>|/N, fine = std(<Sz_i·Sz_j> over edges)
实现优化(不改物理):
  - 向量化 COO 构建哈密顿量 (位运算, 每点重建)
  - multiprocessing 并行多 Δ 点
  - 结果 checkpoint 保存 CSV

检验 P-CM-5 标度外推预测 (签名A/B/C 判据按点数归一化):
  签名 A: star 分支点密度 n_bp/n_points 不衰减
          (N=6..12 实测密度 0.079~0.089, 外推 N=16 保持 >0.06)
  签名 B: star δ≈0比例 ≥ 70%
  签名 C: star D比值 ≥ 100×
  反向:  small_world n_bp 密度远低于 star (N≥8 后 <0.005)

数据来源:
  - EDRN 原始数据(李广好, Apache-2.0): N=6,8,10,12
  - UFPF 新计算(王斌, CC-BY-4.0+MIT): N=14,16

作者: 王斌(独立研究人, UFPF框架维护者)
邮箱: wang.bin@foxmail.com
日期: 2026-08-16
许可: CC-BY-4.0 + MIT
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.sparse import coo_matrix, csc_matrix
from scipy.sparse.linalg import eigsh
import networkx as nx
import os
import json
import sys
import time
import multiprocessing as mp

# 中文字体设置
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from _paper14_spectral_analysis import translate_to_spectral
from _paper14_pcm2_root_cause import get_branch_point_indices

OUTPUT_DIR = SCRIPT_DIR
BASE_DIR = os.path.dirname(SCRIPT_DIR)
XXX_DATA_DIR = os.path.join(BASE_DIR, '稳定岛：神秘的新世界', '寻找稳定岛超密集测试3')
N_SCAN_DIR = os.path.join(XXX_DATA_DIR, 'N_scan_results')

# 新计算数据的保存目录 (analysis/ 下, 不混入 EDRN 目录)
NEW_DATA_DIR = os.path.join(OUTPUT_DIR, 'pcm5_ed_data')
os.makedirs(NEW_DATA_DIR, exist_ok=True)

TOPOLOGIES = ['chain', 'star', 'ring', 'small_world']
NS_EXISTING = [6, 8, 10, 12]
NS_NEW = [14, 16]

NUM_EIG = 5
NCV = 40  # ARPACK 迭代空间 (对 65536 维, 默认 ncv=11 太小)


# =============================================================================
# 图构建 (与 EDRN 完全一致)
# =============================================================================
def build_graph(graph_type, N):
    if graph_type == 'chain':
        G = nx.Graph()
        G.add_nodes_from(range(N))
        for i in range(N - 1):
            G.add_edge(i, i + 1, weight=1.0)
    elif graph_type == 'star':
        G = nx.star_graph(N - 1)
        for u, v in G.edges():
            G[u][v]['weight'] = 1.0
    elif graph_type == 'ring':
        G = nx.cycle_graph(N)
        for u, v in G.edges():
            G[u][v]['weight'] = 1.0
    elif graph_type == 'small_world':
        G = nx.watts_strogatz_graph(N, 4, 0.1, seed=42)
        for u, v in G.edges():
            G[u][v]['weight'] = 1.0
    else:
        raise ValueError(f"Unknown graph type: {graph_type}")
    return G


def get_contradiction_edge(graph_type, N):
    return {
        'chain': (N // 2 - 1, N // 2),
        'star': (0, 1),
        'ring': (N // 2 - 1, N // 2),
        'small_world': (N // 2 - 1, N // 2),
    }[graph_type]


# =============================================================================
# 向量化 COO 哈密顿量构建 (物理与 EDRN 一致, 实现快)
# =============================================================================
def build_hamiltonian_fast(N, edges, contradiction_edge, delta):
    """
    构建 Heisenberg XXX 稀疏哈密顿量 (实对称), 与 EDRN 原始脚本物理完全一致
    H = Σ J_ij (σx_i σx_j + σy_i σy_j + σz_i σz_j)   [未归一化泡利 σ, EDRN 标度]
    位编码: bit=0 → |↑⟩ (σz=+1), bit=1 → |↓⟩ (σz=-1),  σz = 1 - 2·bit
    对角项: J_ij × σz_i × σz_j = J_ij × (1 - 2(b_i+b_j) + 4 b_i b_j)
    非对角(flip): (σx_i σx_j + σy_i σy_j) 的 flip 矩阵元 = 2·J_ij
    (标准 S=σ/2 Heisenberg 的 4 倍能量, 保证与 EDRN N=6..12 数据同一能量标度)
    """
    dim = 1 << N
    Js = np.zeros(len(edges))
    for e, (i, j) in enumerate(edges):
        is_contra = (i, j) == contradiction_edge or (j, i) == contradiction_edge
        Js[e] = delta if is_contra else 1.0

    # 对角项: 对所有 state 向量化 (位采样直接用节点编号 i, j)
    states = np.arange(dim, dtype=np.int64)
    diag = np.zeros(dim)
    for e, (i, j) in enumerate(edges):
        b_i = ((states >> i) & 1).astype(np.float64)
        b_j = ((states >> j) & 1).astype(np.float64)
        diag += Js[e] * (1.0 - 2.0 * (b_i + b_j) + 4.0 * b_i * b_j)

    # 非对角项 (flip i,j): 全量过滤法, 每对取 state < state^mask 去重
    row_off = []
    col_off = []
    data_off = []
    full = np.arange(dim, dtype=np.int64)
    for e, (i, j) in enumerate(edges):
        mask = (1 << i) | (1 << j)
        bi_full = ((full >> i) & 1).astype(np.int64)
        bj_full = ((full >> j) & 1).astype(np.int64)
        sel = (bi_full != bj_full)
        s_sel = full[sel]
        s_flip = s_sel ^ mask
        keep = s_sel < s_flip
        s_sel = s_sel[keep]
        s_flip = s_flip[keep]
        row_off.append(s_sel)
        col_off.append(s_flip)
        data_off.append(np.full(len(s_sel), 2.0 * Js[e]))

    row = np.concatenate(row_off)
    col = np.concatenate(col_off)
    data = np.concatenate(data_off)

    # 组装稀疏矩阵
    H = coo_matrix((data, (row, col)), shape=(dim, dim)).tocsr()
    H = H + H.T  # 对称化 (补齐另一半)
    # 加对角
    diag_sp = coo_matrix((diag, (np.arange(dim), np.arange(dim))), shape=(dim, dim))
    H = H + diag_sp
    return H.tocsc()


def compute_diagnostics_fast(N, edges, contradiction_edge, delta):
    """单个 Δ 点的诊断量计算"""
    H = build_hamiltonian_fast(N, edges, contradiction_edge, delta)
    k = min(NUM_EIG, (1 << N) - 1)
    energies, states = eigsh(H, k=k, which='SA', ncv=min(NCV, (1 << N) - 1))
    gap = energies[1] - energies[0] if len(energies) > 1 else np.nan
    gs = states[:, 0]  # 实向量

    # coarse: |<Σ σz_i>| / N = |Σ_i (1 - 2<bit_i>)| / N   (EDRN 标度 σz)
    N_sites = N
    mag = 0.0
    gs2 = gs ** 2  # 实对称矩阵本征向量实
    for i in range(N_sites):
        b = ((np.arange(1 << N) >> i) & 1).astype(np.float64)
        mag += np.dot(gs2, 1.0 - 2.0 * b)
    coarse = abs(mag / N_sites)

    # fine: std over edges of <σz_i σz_j> = Σ_state |gs|² (1-2b_i)(1-2b_j)  (EDRN 标度)
    corrs = []
    for i, j in edges:
        bi = ((np.arange(1 << N) >> i) & 1).astype(np.float64)
        bj = ((np.arange(1 << N) >> j) & 1).astype(np.float64)
        corr = np.dot(gs2, (1.0 - 2.0 * bi) * (1.0 - 2.0 * bj))
        corrs.append(corr)
    fine = np.std(corrs) if corrs else 0.0

    return float(gap), float(coarse), float(fine)


# =============================================================================
# 并行 worker
# =============================================================================
def worker_delta(args):
    """计算单个 Δ 点 (并行 worker)"""
    N, topo, delta = args
    G = build_graph(topo, N)
    ce = get_contradiction_edge(topo, N)
    edges = list(G.edges())
    try:
        gap, coarse, fine = compute_diagnostics_fast(N, edges, ce, delta)
        return delta, gap, coarse, fine
    except Exception as e:
        print(f"  [错误] {topo} N={N} Δ={delta:.4f}: {e}", flush=True)
        return delta, np.nan, np.nan, np.nan


def compute_and_save_parallel(topo, N, delta_vals, n_proc=None):
    """并行计算并保存 (checkpoint)"""
    path = os.path.join(NEW_DATA_DIR, f'stable_island_{topo}_N{N}.csv')
    if os.path.exists(path):
        print(f"  [已存在] {topo} N={N}: 跳过", flush=True)
        return pd.read_csv(path, comment='#', header=None, names=['delta', 'gap', 'coarse', 'fine'])

    if n_proc is None:
        n_proc = max(1, mp.cpu_count() - 1)

    tasks = [(N, topo, float(d)) for d in delta_vals]
    print(f"  [计算] {topo} N={N} ({len(delta_vals)} 点, 维度 {2**N}, {n_proc} 进程)...", flush=True)
    t0 = time.time()

    results = []
    with mp.Pool(n_proc) as pool:
        for i, res in enumerate(pool.imap_unordered(worker_delta, tasks, chunksize=4)):
            results.append(res)
            if (i + 1) % 100 == 0 or i + 1 == len(tasks):
                elapsed = time.time() - t0
                print(f"    ... {i+1}/{len(tasks)} 完成 ({elapsed:.0f}s)", flush=True)

    elapsed = time.time() - t0
    results.sort(key=lambda r: r[0])
    df = pd.DataFrame(results, columns=['delta', 'gap', 'coarse', 'fine'])
    df = df.dropna()
    np.savetxt(path, df.values, header='delta,gap,coarse,fine', delimiter=',', comments='#')
    print(f"  [完成] {topo} N={N} ({elapsed:.0f}s, {elapsed/len(delta_vals):.2f}s/点)", flush=True)
    return df


# =============================================================================
# 数据加载
# =============================================================================
def load_xxx_csv(topo, N):
    if N in NS_EXISTING:
        if N == 6:
            path = os.path.join(XXX_DATA_DIR, f'stable_island_{topo}.csv')
        else:
            path = os.path.join(N_SCAN_DIR, f'stable_island_{topo}_N{N}.csv')
        if not os.path.exists(path):
            return None
        return pd.read_csv(path, comment='#', header=None, names=['delta', 'gap', 'coarse', 'fine'])
    else:
        path = os.path.join(NEW_DATA_DIR, f'stable_island_{topo}_N{N}.csv')
        if not os.path.exists(path):
            return None
        return pd.read_csv(path, comment='#', header=None, names=['delta', 'gap', 'coarse', 'fine'])


def compute_signature(topo, N):
    df = load_xxx_csv(topo, N)
    if df is None:
        return None
    df_spec = translate_to_spectral(df)
    delta_spec = df_spec['delta_spec'].values
    sigma_res = df_spec['sigma_res'].values
    delta = df_spec['delta'].values

    bp_idx = get_branch_point_indices(sigma_res)
    n_bp = len(bp_idx)
    n_points = len(delta)
    bp_density = n_bp / n_points

    dz_ratio = 0.0
    if n_bp > 0:
        dz_count = sum(1 for idx in bp_idx if abs(delta_spec[idx]) < 1e-2)
        dz_ratio = dz_count / n_bp

    d_delta = np.gradient(delta_spec, delta)
    D_vals = []
    for idx in bp_idx:
        if abs(d_delta[idx]) > 1e-15:
            D_vals.append(sigma_res[idx] / abs(d_delta[idx]))
        else:
            D_vals.append(float('inf'))
    D_mean = np.mean([d for d in D_vals if np.isfinite(d)]) if D_vals else 0.0
    n_inf = sum(1 for d in D_vals if not np.isfinite(d))

    return {
        'topo': topo, 'N': N, 'n_bp': n_bp, 'n_points': n_points,
        'bp_density': bp_density, 'dz_ratio': dz_ratio,
        'D_mean': D_mean, 'n_inf_D': n_inf,
    }


# =============================================================================
# 主程序
# =============================================================================
def main():
    print("=" * 80)
    print("P-CM-5 直接验证: ED 计算 N=14, 16 的 XXX 数据")
    print("方法: 与 EDRN 原始脚本物理一致 (Heisenberg XXX, eigsh SA)")
    print(f"CPU 核数: {mp.cpu_count()}")
    print("=" * 80)

    # ========== 阶段1: 新数据计算 ==========
    print("\n--- 阶段1: 新数据计算 ---")
    delta_vals_14 = np.linspace(0.0, 3.0, 751)   # N=14: 步长0.004
    delta_vals_16 = np.linspace(0.0, 3.0, 501)   # N=16: 步长0.006

    for topo in TOPOLOGIES:
        compute_and_save_parallel(topo, 14, delta_vals_14)

    compute_and_save_parallel('star', 16, delta_vals_16)
    compute_and_save_parallel('small_world', 16, delta_vals_16)

    # ========== 阶段2: 签名计算 ==========
    print("\n--- 阶段2: 三重签名指标 (含点数归一化密度) ---")
    all_sigs = {}
    for N in NS_EXISTING + NS_NEW:
        for topo in TOPOLOGIES:
            sig = compute_signature(topo, N)
            if sig is not None:
                all_sigs[(topo, N)] = sig

    print(f"\n{'拓扑':<14} {'N':<4} {'点数':<6} {'n_bp':<6} {'密度':<8} {'δ≈0%':<8} {'D_mean':<12}")
    print("-" * 75)
    for N in NS_EXISTING + NS_NEW:
        for topo in TOPOLOGIES:
            if (topo, N) in all_sigs:
                s = all_sigs[(topo, N)]
                d_str = f'{s["D_mean"]:.2e}' if s['D_mean'] > 0 else '0'
                if s['n_inf_D'] > 0:
                    d_str += f'+{s["n_inf_D"]}∞'
                print(f"{topo:<14} {N:<4} {s['n_points']:<6} {s['n_bp']:<6} "
                      f"{s['bp_density']:<8.4f} {s['dz_ratio']*100:<7.1f}% {d_str:<12}")

    # ========== 阶段3: P-CM-5 裁决 ==========
    print("\n" + "=" * 80)
    print("P-CM-5 裁决 (直接验证)")
    print("=" * 80)

    verdicts = {}

    for N in NS_NEW:
        print(f"\n--- N={N} ---")
        star_sig = all_sigs.get(('star', N))
        if star_sig is None:
            print(f"  [数据缺失] star N={N}")
            continue

        # 参考: N=6..12 star 的分支点密度
        ref_densities = [all_sigs[('star', n)]['bp_density'] for n in NS_EXISTING
                         if ('star', n) in all_sigs]
        ref_density_mean = np.mean(ref_densities) if ref_densities else 0.0

        # 签名 A: star 分支点密度不衰减 (≥ 0.8 × 历史均值)
        sig_a = star_sig['bp_density'] >= 0.8 * ref_density_mean
        print(f"  签名A (密度≥{0.8*ref_density_mean:.4f}): star 密度={star_sig['bp_density']:.4f} "
              f"(历史均值 {ref_density_mean:.4f}) → {'✅ 满足' if sig_a else '❌ 不满足'}")

        # 签名 B: star δ≈0 比例 ≥ 70%
        sig_b = star_sig['dz_ratio'] >= 0.70
        print(f"  签名B (δ≈0≥70%): star {star_sig['dz_ratio']*100:.1f}% → {'✅ 满足' if sig_b else '❌ 不满足'}")

        # 签名 C: star D比值 ≥ 100×
        other_sigs = [all_sigs[(t, N)] for t in TOPOLOGIES if t != 'star' and (t, N) in all_sigs]
        other_max_D = max((s['D_mean'] for s in other_sigs), default=0.0)
        if other_max_D > 0:
            D_ratio = star_sig['D_mean'] / other_max_D
        else:
            D_ratio = float('inf')
        sig_c = D_ratio >= 100
        r_str = f'{D_ratio:.1f}' if np.isfinite(D_ratio) else 'inf'
        print(f"  签名C (D比值≥100×): star_D={star_sig['D_mean']:.2e}, other_max={other_max_D:.2e}, "
              f"ratio={r_str} → {'✅ 满足' if sig_c else '❌ 不满足'}")

        # 反向: small_world 密度远低于 star
        sw_sig = all_sigs.get(('small_world', N))
        if sw_sig is not None:
            sw_ok = sw_sig['bp_density'] < 0.2 * star_sig['bp_density']
            print(f"  反向断言 (sw密度<0.2×star): sw={sw_sig['bp_density']:.4f} vs star={star_sig['bp_density']:.4f} "
                  f"→ {'✅ 成立' if sw_ok else '❌ 不成立'}")

        n_pass = sum([sig_a, sig_b, sig_c])
        verdict = '✅ P-CM-5 直接验证成立' if n_pass >= 2 else '❌ P-CM-5 直接验证证伪'
        print(f"  → {n_pass}/3 签名满足: {verdict}")
        verdicts[N] = {
            'n_pass': n_pass,
            'sig_a': sig_a, 'sig_b': sig_b, 'sig_c': sig_c,
            'star_bp_density': star_sig['bp_density'],
            'star_dz_ratio': star_sig['dz_ratio'],
            'D_ratio': D_ratio if np.isfinite(D_ratio) else None,
            'verdict': verdict,
        }

    passed = [v for v in verdicts.values() if '成立' in v['verdict']]
    if len(verdicts) == 0:
        overall = '❌ 数据不足, 无法裁决'
    elif len(passed) == len(verdicts):
        overall = '✅ P-CM-5 直接验证成立 (所有新尺寸均满足)'
    elif len(passed) >= 1:
        overall = '⚠️ P-CM-5 部分成立 (部分新尺寸满足)'
    else:
        overall = '❌ P-CM-5 直接验证证伪'

    print("\n" + "=" * 80)
    print(f"总裁决: {overall}")
    print("=" * 80)

    # ========== 阶段4: 可视化 ==========
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # (a) 签名A: bp_density vs N
    ax = axes[0]
    Ns_all = sorted(set(n for (_, n) in all_sigs.keys()))
    dens_star = []
    dens_sw = []
    for N in Ns_all:
        if ('star', N) in all_sigs:
            dens_star.append(all_sigs[('star', N)]['bp_density'])
        if ('small_world', N) in all_sigs:
            dens_sw.append(all_sigs[('small_world', N)]['bp_density'])
    Ns_star = [N for N in Ns_all if ('star', N) in all_sigs]
    Ns_sw = [N for N in Ns_all if ('small_world', N) in all_sigs]
    ax.plot(Ns_star, dens_star, 'ro-', label='star (实测)', markersize=7)
    ax.plot(Ns_sw, dens_sw, 'purple', 'o--', label='small_world (实测)', markersize=7)
    ax.axhline(y=0.08 * 0.8, color='green', linestyle=':', alpha=0.7, label='A阈值 (0.8×历史均值)')
    ax.set_xlabel('$N$')
    ax.set_ylabel('分支点密度 $n_{bp}/n_{points}$')
    ax.set_title('(a) 签名A: 分支点密度直接验证')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # (b) 签名B: δ≈0 比例 vs N
    ax = axes[1]
    Ns_b = []
    dz_star = []
    for N in Ns_all:
        if ('star', N) in all_sigs:
            Ns_b.append(N)
            dz_star.append(all_sigs[('star', N)]['dz_ratio'] * 100)
    ax.plot(Ns_b, dz_star, 'ro-', label='star (实测)', markersize=7)
    ax.axhline(y=70, color='green', linestyle='--', label='B阈值: 70%')
    ax.axhline(y=50, color='orange', linestyle=':', label='证伪线: 50%')
    ax.set_xlabel('$N$')
    ax.set_ylabel('$\\delta_{SC} \\approx 0$ 比例 (%)')
    ax.set_title('(b) 签名B: $\\delta \\approx 0$ 比例直接验证')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # (c) 签名C: D比值 vs N (对数)
    ax = axes[2]
    Ns_c = []
    D_ratios = []
    for N in Ns_all:
        star_s = all_sigs.get(('star', N))
        if star_s is None:
            continue
        other_sigs = [all_sigs[(t, N)] for t in TOPOLOGIES if t != 'star' and (t, N) in all_sigs]
        other_max = max((s['D_mean'] for s in other_sigs), default=0.0)
        if other_max > 0:
            r = star_s['D_mean'] / other_max
        else:
            r = float('inf')
        Ns_c.append(N)
        D_ratios.append(min(r, 1e15) if np.isfinite(r) else 1e15)
    ax.plot(Ns_c, D_ratios, 'ro-', markersize=7, label='star/max(other) (实测)')
    ax.axhline(y=100, color='green', linestyle='--', label='C阈值: 100×')
    ax.axhline(y=5, color='orange', linestyle=':', label='证伪线: 5×')
    ax.set_xlabel('$N$')
    ax.set_ylabel('$D_{star}/D_{max(other)}$ (log)')
    ax.set_title('(c) 签名C: $D$ 比值直接验证')
    ax.set_yscale('log')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    outpath = os.path.join(OUTPUT_DIR, 'paper14_pcm5_direct_verification.png')
    plt.savefig(outpath, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"\n[图表] {outpath}")

    # ========== JSON 汇总 ==========
    def json_default(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, float) and (np.isnan(obj) or np.isinf(obj)):
            return None
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

    sig_data = {}
    for (topo, N), s in all_sigs.items():
        sig_data[f'{topo}_N{N}'] = {
            'n_bp': s['n_bp'], 'n_points': s['n_points'],
            'bp_density': s['bp_density'], 'dz_ratio': s['dz_ratio'],
            'D_mean': s['D_mean'], 'n_inf_D': s['n_inf_D'],
        }

    summary = {
        'P-CM-5_direct_verification': {
            'method': 'ED计算N=14,16的XXX数据(与EDRN脚本物理一致: Heisenberg XXX + eigsh SA)',
            'resolution': {
                'N14': '751点(步长0.004)',
                'N16': '501点(步长0.006)',
                'note': '分支点判据按点数归一化为密度 n_bp/n_points, 与N=6..12的1501点数据可比',
            },
            'data_source': {
                'N6_12': 'EDRN原始(李广好, Apache-2.0)',
                'N14_16': 'UFPF新计算(王斌, CC-BY-4.0+MIT)',
            },
            'signatures': sig_data,
            'verdicts': {str(k): v for k, v in verdicts.items()},
            'overall': overall,
        },
    }

    summary_path = os.path.join(OUTPUT_DIR, 'paper14_pcm5_direct_verification.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, default=json_default)
    print(f"[汇总] {summary_path}")

    print("\n完成.")


if __name__ == "__main__":
    main()
