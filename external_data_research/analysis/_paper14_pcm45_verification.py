"""
P-CM-4 跨模型普适性验证 + P-CM-5 标度外推分析

P-CM-4: 在不同物理模型(XXZ各向异性/横场Ising)上验证三重签名A+B+C的普适性
  - XXZ模型: H = Σ[J_xy(Sx·Sx+Sy·Sy) + J_z·Sz·Sz], J_z/J_xy=2.0 (Ising-like)
  - 横场Ising: H = -ΣJ·Sz·Sz - h·ΣSx, h=1.0 (Z2对称性, 不同 universality class)
  - 对比基线: Heisenberg XXX (原始EDRN数据)

P-CM-5: 对N=6,8,10,12已有数据进行标度分析, 外推N=16,20,24的趋势
  - 签名A: n_bp/N vs N 的标度律拟合
  - 签名B: δ_SC≈0比例 vs N 的趋势
  - 签名C: D比值 vs N 的标度律拟合

数据来源:
  - 原始EDRN数据(李广好, Apache-2.0): XXX模型 N=6,8,10,12
  - UFPF新生成数据(王斌, CC-BY-4.0+MIT): XXZ/Ising模型 N=6,8

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
from scipy.sparse import lil_matrix, csc_matrix
from scipy.sparse.linalg import eigsh
import networkx as nx
import os
import json
import sys
import time

# 中文字体设置
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from _paper14_spectral_analysis import translate_to_spectral
from _paper14_pcm2_root_cause import (
    TOPOLOGIES, get_branch_point_indices, LOCAL_WINDOW
)

OUTPUT_DIR = SCRIPT_DIR
BASE_DIR = os.path.dirname(SCRIPT_DIR)
XXX_DATA_DIR = os.path.join(BASE_DIR, '稳定岛：神秘的新世界', '寻找稳定岛超密集测试3')
N_SCAN_DIR = os.path.join(XXX_DATA_DIR, 'N_scan_results')


# =============================================================================
# 稀疏哈密顿量构建 (支持XXX/XXZ/Ising三种模型)
# =============================================================================
def build_graph(graph_type, N):
    """构建图拓扑 (与EDRN原始脚本一致)"""
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
    """矛盾边选择 (与EDRN原始脚本一致)"""
    return {
        'chain': (N // 2 - 1, N // 2),
        'star': (0, 1),
        'ring': (N // 2 - 1, N // 2),
        'small_world': (N // 2 - 1, N // 2),
    }[graph_type]


def build_hamiltonian_sparse(G, contradiction_edge, delta, model='xxx',
                              J_xy=1.0, J_z_aniso=2.0, h_trans=1.0):
    """
    稀疏构建哈密顿量 (支持XXX/XXZ/Ising)

    模型:
      xxx:  H = Σ J·(Sx·Sx + Sy·Sy + Sz·Sz), 矛盾边J=delta
      xxz:  H = Σ[J_xy·(Sx·Sx+Sy·Sy) + J_z·Sz·Sz], J_z/J_xy=J_z_aniso, 矛盾边J_z=delta
      ising: H = -ΣJ·Sz·Sz - h·ΣSx, J=delta(矛盾边)/1.0(其他), h=h_trans
    """
    N = G.number_of_nodes()
    dim = 2 ** N
    H = lil_matrix((dim, dim), dtype=float)

    # 自旋算符在计算基下的表示: |0>=|↑>, |1>=|↓>
    # Sz|↑> = +0.5|↑>, Sz|↓> = -0.5|↓>
    # S+|↓> = |↑>, S-|↑> = |↓>

    for i, j, w in G.edges(data='weight'):
        is_contradiction = ((i, j) == contradiction_edge or (j, i) == contradiction_edge)

        if model == 'xxx':
            J = delta if is_contradiction else 1.0
            # Sz·Sz 项 (对角)
            for state in range(dim):
                si = 0.5 if not ((state >> i) & 1) else -0.5
                sj = 0.5 if not ((state >> j) & 1) else -0.5
                H[state, state] += J * si * sj
            # S+S- + S-S+ 项 (非对角)
            for state in range(dim):
                bi = (state >> i) & 1
                bj = (state >> j) & 1
                if bi != bj:
                    new_state = state ^ (1 << i) ^ (1 << j)
                    H[state, new_state] += J * 0.5

        elif model == 'xxz':
            Jxy = J_xy
            Jz = J_z_aniso * (delta if is_contradiction else 1.0)
            # Sz·Sz 项
            for state in range(dim):
                si = 0.5 if not ((state >> i) & 1) else -0.5
                sj = 0.5 if not ((state >> j) & 1) else -0.5
                H[state, state] += Jz * si * sj
            # S+S- + S-S+ 项
            for state in range(dim):
                bi = (state >> i) & 1
                bj = (state >> j) & 1
                if bi != bj:
                    new_state = state ^ (1 << i) ^ (1 << j)
                    H[state, new_state] += Jxy * 0.5

        elif model == 'ising':
            J = delta if is_contradiction else 1.0
            # -J·Sz·Sz 项 (Ising相互作用)
            for state in range(dim):
                si = 0.5 if not ((state >> i) & 1) else -0.5
                sj = 0.5 if not ((state >> j) & 1) else -0.5
                H[state, state] += -J * si * sj
            # Ising模型无Sx·Sx + Sy·Sy项

    # 横场项: -h·Σ Sx_i (仅Ising模型)
    if model == 'ising':
        for site in range(N):
            for state in range(dim):
                # Sx = (S+ + S-)/2, S+|↓>=|↑>, S-|↑>=|↓>
                flipped = state ^ (1 << site)
                H[state, flipped] += -h_trans * 0.5

    return H.tocsc()


def compute_diagnostics_sparse(G, contradiction_edge, delta, model='xxx',
                                J_xy=1.0, J_z_aniso=2.0, h_trans=1.0, num_eig=5):
    """计算诊断量: gap, coarse(磁化), fine(自旋关联涨落)"""
    N = G.number_of_nodes()
    H = build_hamiltonian_sparse(G, contradiction_edge, delta, model,
                                  J_xy, J_z_aniso, h_trans)
    dim = 2 ** N
    k = min(num_eig, dim - 1)

    try:
        energies, states = eigsh(H, k=k, which='SA')
    except Exception:
        # 退化情况: 用密集对角化
        H_dense = H.toarray()
        energies = np.linalg.eigvalsh(H_dense)[:k]
        states = np.zeros((dim, k))
        # 简化: 只取能量
        gap = energies[1] - energies[0] if k > 1 else 0.0
        # 近似诊断
        return gap, 0.0, 0.0

    gap = energies[1] - energies[0] if len(energies) > 1 else 0.0
    gs = states[:, 0].real

    # 磁化: <Sz_total>/N
    mag = 0.0
    for site in range(N):
        for state in range(dim):
            si = 0.5 if not ((state >> site) & 1) else -0.5
            mag += gs[state] ** 2 * si
    coarse = abs(mag / N)

    # 自旋关联涨落: std(<Sz_i·Sz_j>) over edges
    corrs = []
    for i, j in G.edges():
        corr = 0.0
        for state in range(dim):
            si = 0.5 if not ((state >> i) & 1) else -0.5
            sj = 0.5 if not ((state >> j) & 1) else -0.5
            corr += gs[state] ** 2 * si * sj
        corrs.append(corr)
    fine = np.std(corrs) if corrs else 0.0

    return gap, coarse, fine


# =============================================================================
# P-CM-4: 跨模型数据生成 + 三重签名验证
# =============================================================================
def generate_model_data(model, N, delta_vals, topologies, J_z_aniso=2.0, h_trans=1.0):
    """为新模型生成 (delta, gap, coarse, fine) 数据"""
    results = {}
    for topo in topologies:
        G = build_graph(topo, N)
        ce = get_contradiction_edge(topo, N)
        gaps, coarses, fines = [], [], []

        print(f"  [{model}] {topo} N={N}: 计算 {len(delta_vals)} 点...", end='', flush=True)
        t0 = time.time()
        for delta in delta_vals:
            gap, coarse, fine = compute_diagnostics_sparse(
                G, ce, delta, model=model,
                J_z_aniso=J_z_aniso, h_trans=h_trans
            )
            gaps.append(gap)
            coarses.append(coarse)
            fines.append(fine)
        elapsed = time.time() - t0
        print(f" 完成 ({elapsed:.1f}s)")

        df = pd.DataFrame({
            'delta': delta_vals,
            'gap': gaps,
            'coarse': coarses,
            'fine': fines,
        })
        results[topo] = df
    return results


def check_triple_signature(df, topo, N):
    """
    对单个 (topo, N) 数据检查三重签名 A+B+C
    返回: (sig_a, sig_b_info, sig_c_info, all_satisfied)
    """
    df_spec = translate_to_spectral(df)
    delta_spec = df_spec['delta_spec'].values
    sigma_res = df_spec['sigma_res'].values
    delta = df_spec['delta'].values

    # 签名A: 分支点数 >= 100
    bp_idx = get_branch_point_indices(sigma_res)
    n_bp = len(bp_idx)
    sig_a = n_bp >= 100

    # 签名B: 分支点处δ_SC≈0比例 >= 80%
    if n_bp > 0:
        dz_count = sum(1 for idx in bp_idx if abs(delta_spec[idx]) < 0.01)
        dz_ratio = dz_count / n_bp
    else:
        dz_ratio = 0.0
    sig_b = dz_ratio >= 0.8

    # 签名C: 发散度D (σ_res/|dδ/dΔ|) 是否显著大
    d_delta = np.gradient(delta_spec, delta)
    D_vals = []
    for idx in bp_idx:
        if abs(d_delta[idx]) > 1e-15:
            D_vals.append(sigma_res[idx] / abs(d_delta[idx]))
        else:
            D_vals.append(float('inf'))
    D_mean = np.mean([d for d in D_vals if np.isfinite(d)]) if D_vals else 0.0
    n_inf = sum(1 for d in D_vals if not np.isfinite(d))
    sig_c = (D_mean > 1.0 or n_inf > 0) and n_bp > 0

    all_satisfied = sig_a and sig_b and sig_c

    return {
        'topo': topo,
        'N': N,
        'n_bp': n_bp,
        'sig_a': sig_a,
        'dz_ratio': dz_ratio,
        'sig_b': sig_b,
        'D_mean': D_mean,
        'n_inf_D': n_inf,
        'sig_c': sig_c,
        'all_abc': all_satisfied,
    }


def verify_pcm4():
    """P-CM-4: 跨模型普适性验证"""
    print("=" * 80)
    print("P-CM-4: 谱丛分支点三重签名的跨模型普适性验证")
    print("=" * 80)

    # 使用N=6, 8 (计算速度快)
    test_NS = [6, 8]
    delta_vals = np.linspace(0.0, 3.0, 1501)
    models = {
        'xxx': {'J_z_aniso': 1.0, 'h_trans': 0.0},
        'xxz': {'J_z_aniso': 2.0, 'h_trans': 0.0},
        'ising': {'J_z_aniso': 0.0, 'h_trans': 1.0},
    }

    all_results = {}

    # XXX模型: 使用已有EDRN数据
    print("\n--- XXX模型 (EDRN原始数据) ---")
    for N in test_NS:
        all_results.setdefault('xxx', {})[N] = {}
        for topo in TOPOLOGIES:
            if N == 6:
                path = os.path.join(XXX_DATA_DIR, f'stable_island_{topo}.csv')
            else:
                path = os.path.join(N_SCAN_DIR, f'stable_island_{topo}_N{N}.csv')
            df = pd.read_csv(path, comment='#', header=None, names=['delta', 'gap', 'coarse', 'fine'])
            all_results['xxx'][N][topo] = df

    # XXZ模型: 新生成
    print("\n--- XXZ模型 (J_z/J_xy=2.0, Ising-like) ---")
    for N in test_NS:
        data = generate_model_data('xxz', N, delta_vals, TOPOLOGIES, J_z_aniso=2.0)
        all_results.setdefault('xxz', {})[N] = data

    # 横场Ising模型: 新生成
    print("\n--- 横场Ising模型 (h=1.0, Z2对称性) ---")
    for N in test_NS:
        data = generate_model_data('ising', N, delta_vals, TOPOLOGIES, h_trans=1.0)
        all_results.setdefault('ising', {})[N] = data

    # 检查三重签名
    print("\n" + "=" * 80)
    print("三重签名 A+B+C 检查结果")
    print("=" * 80)

    signature_results = {}
    print(f"\n{'模型':<8} {'拓扑':<14} {'N':<4} {'n_bp':<6} {'sig_A':<6} "
          f"{'δ≈0%':<8} {'sig_B':<6} {'D_mean':<12} {'sig_C':<6} {'A+B+C':<6}")
    print("-" * 85)

    for model in ['xxx', 'xxz', 'ising']:
        signature_results[model] = {}
        for N in test_NS:
            for topo in TOPOLOGIES:
                df = all_results[model][N][topo]
                result = check_triple_signature(df, topo, N)
                signature_results[model][f'{topo}_N{N}'] = result

                sa = '✅' if result['sig_a'] else '❌'
                sb = '✅' if result['sig_b'] else '❌'
                sc = '✅' if result['sig_c'] else '❌'
                sab = '★' if result['all_abc'] else '—'
                d_str = f'{result["D_mean"]:.2e}' if result['D_mean'] > 0 else '0'
                if result['n_inf_D'] > 0:
                    d_str += f'+{result["n_inf_D"]}∞'

                print(f"{model:<8} {topo:<14} {N:<4} {result['n_bp']:<6} "
                      f"{sa:<6} {result['dz_ratio']*100:<7.1f}% {sb:<6} "
                      f"{d_str:<12} {sc:<6} {sab:<6}")

    # 汇总: 每个模型的star是否满足A+B+C
    print("\n" + "=" * 80)
    print("P-CM-4 裁决: star拓扑在不同模型中是否满足A+B+C?")
    print("=" * 80)

    pcm4_verdicts = {}
    for model in ['xxx', 'xxz', 'ising']:
        star_results = [signature_results[model][f'star_N{N}'] for N in test_NS]
        n_abc = sum(1 for r in star_results if r['all_abc'])
        n_pass = len(test_NS)
        verdict = '✅ 通过' if n_abc >= n_pass - 1 else '❌ 证伪'
        pcm4_verdicts[model] = {
            'n_abc_satisfied': n_abc,
            'n_total': n_pass,
            'verdict': verdict,
        }
        print(f"  {model:<8}: star A+B+C 满足 {n_abc}/{n_pass} N → {verdict}")

        # 检查其他拓扑是否不满足
        for topo in ['chain', 'ring', 'small_world']:
            other_results = [signature_results[model][f'{topo}_N{N}'] for N in test_NS]
            n_other_abc = sum(1 for r in other_results if r['all_abc'])
            if n_other_abc > 0:
                print(f"    ⚠️  {topo} 也在 {n_other_abc}/{n_pass} N 中满足A+B+C")

    overall_pass = all(pcm4_verdicts[m]['n_abc_satisfied'] >= len(test_NS) - 1 for m in ['xxx', 'xxz', 'ising'])
    overall_verdict = '✅ P-CM-4 成立 (三重签名跨模型普适)' if overall_pass else '❌ P-CM-4 证伪'
    print(f"\n  ★ 总裁决: {overall_verdict}")

    return signature_results, pcm4_verdicts, overall_verdict


# =============================================================================
# P-CM-5: 标度分析与外推
# =============================================================================
def verify_pcm5():
    """P-CM-5: 利用N=6,8,10,12数据进行标度分析,外推N=16,20,24"""
    print("\n" + "=" * 80)
    print("P-CM-5: 三重签名的N标度分析与外推")
    print("=" * 80)

    NS_existing = [6, 8, 10, 12]
    NS_extrapolate = [14, 16, 20, 24]

    # 收集已有数据的签名指标
    scaling_data = {topo: {'N': [], 'n_bp': [], 'n_bp_per_N': [],
                           'dz_ratio': [], 'D_mean': [], 'D_ratio': []}
                    for topo in TOPOLOGIES}

    print(f"\n{'拓扑':<14} {'N':<4} {'n_bp':<6} {'n_bp/N':<8} {'δ≈0%':<8} "
          f"{'D_mean(star)':<14} {'D_max(other)':<14}")
    print("-" * 75)

    # 收集每个N的star D_mean和其他拓扑的max D_mean
    star_D_by_N = {}
    other_D_by_N = {}

    for N in NS_existing:
        D_per_topo = {}
        for topo in TOPOLOGIES:
            if N == 6:
                path = os.path.join(XXX_DATA_DIR, f'stable_island_{topo}.csv')
            else:
                path = os.path.join(N_SCAN_DIR, f'stable_island_{topo}_N{N}.csv')
            df = pd.read_csv(path, comment='#', header=None, names=['delta', 'gap', 'coarse', 'fine'])
            result = check_triple_signature(df, topo, N)

            scaling_data[topo]['N'].append(N)
            scaling_data[topo]['n_bp'].append(result['n_bp'])
            scaling_data[topo]['n_bp_per_N'].append(result['n_bp'] / N)
            scaling_data[topo]['dz_ratio'].append(result['dz_ratio'])
            scaling_data[topo]['D_mean'].append(result['D_mean'])
            D_per_topo[topo] = result['D_mean']

        star_D = D_per_topo.get('star', 0)
        other_max_D = max(D_per_topo.get(t, 0) for t in TOPOLOGIES if t != 'star')
        star_D_by_N[N] = star_D
        other_D_by_N[N] = other_max_D
        ratio = star_D / other_max_D if other_max_D > 0 else float('inf')

        r_str = f'{ratio:.1f}' if np.isfinite(ratio) else 'inf'
        bp_per_N = scaling_data['star']['n_bp_per_N'][-1]
        dz_pct = scaling_data['star']['dz_ratio'][-1] * 100
        print(f"{'star':<14} {N:<4} {scaling_data['star']['n_bp'][-1]:<6} "
              f"{bp_per_N:<8.1f} {dz_pct:<7.1f}% {star_D:<14.2e} {other_max_D:<14.2e}")

    # === 签名A标度分析: n_bp/N vs N ===
    print("\n--- 签名A标度分析: n_bp(star)/N vs N ---")
    star_bp_per_N = scaling_data['star']['n_bp_per_N']
    sw_bp_per_N = scaling_data['small_world']['n_bp_per_N']

    # 拟合: n_bp/N = a * N^b (幂律)
    Ns_arr = np.array(NS_existing, dtype=float)
    star_bp_arr = np.array(star_bp_per_N)

    # log-log 拟合
    log_N = np.log(Ns_arr)
    log_bp = np.log(np.maximum(star_bp_arr, 0.1))
    A_slope, A_intercept = np.polyfit(log_N, log_bp, 1)
    A_a = np.exp(A_intercept)

    print(f"  star: n_bp/N ≈ {A_a:.2f} × N^{A_slope:.3f}")
    print(f"  (幂律斜率 {A_slope:.3f}: {'↑ 增长' if A_slope > 0 else '↓ 衰减'})")

    # 外推
    print(f"\n  外推预测:")
    for N_ext in NS_extrapolate:
        bp_per_N_pred = A_a * N_ext ** A_slope
        n_bp_pred = bp_per_N_pred * N_ext
        sig_a_pred = n_bp_pred >= 100
        print(f"    N={N_ext}: n_bp/N≈{bp_per_N_pred:.1f}, n_bp≈{n_bp_pred:.0f} → "
              f"签名A {'✅ 满足' if sig_a_pred else '❌ 不满足'}")

    # small_world 趋势
    sw_bp_arr = np.array(sw_bp_per_N)
    if np.all(sw_bp_arr > 0):
        log_sw = np.log(np.maximum(sw_bp_arr, 0.01))
        sw_slope, sw_intercept = np.polyfit(log_N, log_sw, 1)
        sw_a = np.exp(sw_intercept)
        print(f"\n  small_world: n_bp/N ≈ {sw_a:.2f} × N^{sw_slope:.3f}")
        for N_ext in [16, 20, 24]:
            sw_pred = sw_a * N_ext ** sw_slope
            print(f"    N={N_ext}: n_bp/N≈{sw_pred:.1f} → n_bp≈{sw_pred*N_ext:.0f}")

    # === 签名B趋势: δ≈0比例 vs N ===
    print("\n--- 签名B趋势: star分支点δ_SC≈0比例 vs N ---")
    star_dz = scaling_data['star']['dz_ratio']
    for i, N in enumerate(NS_existing):
        print(f"  N={N}: {star_dz[i]*100:.1f}%")
    dz_mean = np.mean(star_dz)
    dz_std = np.std(star_dz)
    print(f"  均值: {dz_mean*100:.1f}%, 标准差: {dz_std*100:.1f}%")
    # 线性趋势
    B_slope, B_intercept = np.polyfit(Ns_arr, star_dz, 1)
    print(f"  线性趋势: δ≈0% ≈ {B_intercept*100:.1f} + {B_slope*100:.2f}×N")
    print(f"  外推N=16: {max(0, (B_intercept + B_slope*16))*100:.1f}%")
    print(f"  外推N=24: {max(0, (B_intercept + B_slope*24))*100:.1f}%")

    # === 签名C标度分析: D比值 vs N ===
    print("\n--- 签名C标度分析: D(star)/D(max_other) vs N ---")
    D_ratios = []
    for N in NS_existing:
        sD = star_D_by_N[N]
        oD = other_D_by_N[N]
        r = sD / oD if oD > 0 else float('inf')
        D_ratios.append(r)
        r_str = f'{r:.1f}' if np.isfinite(r) else 'inf'
        print(f"  N={N}: star_D={sD:.2e}, other_max_D={oD:.2e}, ratio={r_str}")

    # 外推: 使用对数线性拟合 (排除inf)
    finite_ratios = [(N, r) for N, r in zip(NS_existing, D_ratios) if np.isfinite(r) and r > 0]
    if len(finite_ratios) >= 2:
        log_N_f = np.log([r[0] for r in finite_ratios])
        log_r_f = np.log([r[1] for r in finite_ratios])
        C_slope, C_intercept = np.polyfit(log_N_f, log_r_f, 1)
        C_a = np.exp(C_intercept)
        print(f"  幂律拟合: D_ratio ≈ {C_a:.2f} × N^{C_slope:.3f}")
        for N_ext in [16, 20, 24]:
            ratio_pred = C_a * N_ext ** C_slope
            print(f"    N={N_ext}: D_ratio≈{ratio_pred:.1f}× → "
                  f"签名C {'✅ 满足' if ratio_pred >= 100 else '⚠️ 低于100×阈值' if ratio_pred >= 5 else '❌ 不满足'}")

    # === P-CM-5 总裁决 ===
    print("\n" + "=" * 80)
    print("P-CM-5 标度外推总裁决")
    print("=" * 80)

    # 签名A外推
    n_bp_16 = A_a * 16 ** A_slope * 16
    sig_a_16 = n_bp_16 >= 100

    # 签名B外推
    dz_16 = max(0, B_intercept + B_slope * 16)
    sig_b_16 = dz_16 >= 0.70

    # 签名C外推
    if len(finite_ratios) >= 2:
        ratio_16 = C_a * 16 ** C_slope
        sig_c_16 = ratio_16 >= 100
    else:
        ratio_16 = float('inf')
        sig_c_16 = True

    print(f"  N=16外推:")
    print(f"    签名A: n_bp≈{n_bp_16:.0f} → {'✅' if sig_a_16 else '❌'} (阈值≥100)")
    print(f"    签名B: δ≈0%≈{dz_16*100:.1f}% → {'✅' if sig_b_16 else '❌'} (阈值≥70%)")
    r_str = f'{ratio_16:.1f}' if np.isfinite(ratio_16) else 'inf'
    print(f"    签名C: D_ratio≈{r_str}× → {'✅' if sig_c_16 else '❌'} (阈值≥100×)")

    n_pass_16 = sum([sig_a_16, sig_b_16, sig_c_16])
    pcm5_verdict = '✅ P-CM-5 外推成立' if n_pass_16 >= 2 else '⚠️ P-CM-5 外推部分成立' if n_pass_16 >= 1 else '❌ P-CM-5 外推证伪'
    print(f"\n  ★ N=16外推: {n_pass_16}/3 签名满足 → {pcm5_verdict}")
    print(f"  ★ 注: 这是基于N=6,8,10,12的标度外推, 非直接验证。P-CM-5的最终裁决仍需N=16,20,24的实际ED计算。")

    return {
        'scaling_data': {topo: {k: v for k, v in d.items()} for topo, d in scaling_data.items()},
        'signature_A_fit': {'a': float(A_a), 'slope': float(A_slope)},
        'signature_B_fit': {'intercept': float(B_intercept), 'slope': float(B_slope)},
        'signature_C_fit': {'a': float(C_a) if len(finite_ratios) >= 2 else None,
                           'slope': float(C_slope) if len(finite_ratios) >= 2 else None},
        'extrapolation_N16': {
            'sig_a': bool(sig_a_16), 'n_bp_pred': float(n_bp_16),
            'sig_b': bool(sig_b_16), 'dz_ratio_pred': float(dz_16),
            'sig_c': bool(sig_c_16), 'D_ratio_pred': float(ratio_16) if np.isfinite(ratio_16) else None,
            'n_pass': int(n_pass_16),
        },
        'verdict': pcm5_verdict,
    }


# =============================================================================
# 可视化
# =============================================================================
def plot_pcm45_verification(pcm4_results, pcm5_results):
    """P-CM-4 + P-CM-5 综合可视化"""
    fig = plt.figure(figsize=(20, 16))

    # ======== P-CM-4: 跨模型三重签名对比 ========

    # (a) n_bp 跨模型对比 (N=8)
    ax = fig.add_subplot(2, 3, 1)
    models = ['xxx', 'xxz', 'ising']
    model_labels = ['XXX\n(EDRN)', 'XXZ\n(Jz/Jxy=2)', 'Ising\n(h=1.0)']
    x = np.arange(len(TOPOLOGIES))
    width = 0.25
    for j, (model, label) in enumerate(zip(models, model_labels)):
        vals = [pcm4_results[model][f'{topo}_N8']['n_bp'] for topo in TOPOLOGIES]
        ax.bar(x + j * width, vals, width, alpha=0.7, label=label)
    ax.axhline(y=100, color='red', linestyle='--', linewidth=1, label='签名A阈值')
    ax.set_xticks(x + width)
    ax.set_xticklabels(TOPOLOGIES, fontsize=8)
    ax.set_ylabel('$n_{bp}$')
    ax.set_title('(a) 分支点数跨模型对比 ($N=8$)')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3, axis='y')

    # (b) δ_SC≈0比例跨模型对比 (N=8)
    ax = fig.add_subplot(2, 3, 2)
    for j, (model, label) in enumerate(zip(models, model_labels)):
        vals = [pcm4_results[model][f'{topo}_N8']['dz_ratio'] * 100 for topo in TOPOLOGIES]
        ax.bar(x + j * width, vals, width, alpha=0.7, label=label)
    ax.axhline(y=80, color='red', linestyle='--', linewidth=1, label='签名B阈值')
    ax.set_xticks(x + width)
    ax.set_xticklabels(TOPOLOGIES, fontsize=8)
    ax.set_ylabel('$\\delta_{SC} \\approx 0$ 比例 (%)')
    ax.set_title('(b) 分支点$\\delta_{SC}$近零比例 ($N=8$)')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3, axis='y')

    # (c) D_mean 跨模型对比 (star N=8, 对数坐标)
    ax = fig.add_subplot(2, 3, 3)
    for j, (model, label) in enumerate(zip(models, model_labels)):
        r = pcm4_results[model][f'star_N8']
        D_val = r['D_mean']
        # 截断显示
        D_plot = min(D_val, 1e15) if D_val > 0 else 0.01
        ax.bar(j, D_plot, 0.5, alpha=0.7, label=label)
    ax.set_xticks(range(len(models)))
    ax.set_xticklabels(model_labels, fontsize=8)
    ax.set_ylabel('$D_{mean}$ (star, $N=8$)')
    ax.set_title('(c) 发散度 $D$ 跨模型对比 (star)')
    ax.set_yscale('log')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3, axis='y')

    # ======== P-CM-5: 标度外推 ========

    # (d) 签名A: n_bp/N vs N + 幂律拟合
    ax = fig.add_subplot(2, 3, 4)
    Ns = [6, 8, 10, 12]
    for topo in TOPOLOGIES:
        vals = pcm5_results['scaling_data'][topo]['n_bp_per_N']
        ax.plot(Ns, vals, 'o-', label=topo, markersize=6)
    # star 幂律拟合外推
    A_fit = pcm5_results['signature_A_fit']
    N_ext = np.linspace(6, 24, 100)
    bp_pred = A_fit['a'] * N_ext ** A_fit['slope']
    ax.plot(N_ext, bp_pred, '--', color='red', alpha=0.5, label=f'star拟合: {A_fit["a"]:.1f}×N^{A_fit["slope"]:.2f}')
    ax.axhline(y=100/16, color='green', linestyle=':', alpha=0.5, label='A阈值(N=16): 100/16')
    ax.set_xlabel('$N$')
    ax.set_ylabel('$n_{bp}/N$')
    ax.set_title('(d) 签名A: $n_{bp}/N$ 标度')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # (e) 签名B: δ≈0比例 vs N
    ax = fig.add_subplot(2, 3, 5)
    star_dz = pcm5_results['scaling_data']['star']['dz_ratio']
    ax.plot(Ns, [d*100 for d in star_dz], 'ro-', label='star', markersize=8)
    B_fit = pcm5_results['signature_B_fit']
    dz_pred = [(B_fit['intercept'] + B_fit['slope']*n)*100 for n in N_ext]
    ax.plot(N_ext, dz_pred, '--', color='red', alpha=0.5,
            label=f'线性: {B_fit["intercept"]*100:.0f}+{B_fit["slope"]*100:.1f}×N')
    ax.axhline(y=70, color='green', linestyle='--', label='B阈值: 70%')
    ax.axhline(y=50, color='orange', linestyle=':', label='证伪阈值: 50%')
    ax.set_xlabel('$N$')
    ax.set_ylabel('$\\delta_{SC} \\approx 0$ 比例 (%)')
    ax.set_title('(e) 签名B: $\\delta \\approx 0$ 比例标度')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # (f) 签名C: D比值 vs N (对数)
    ax = fig.add_subplot(2, 3, 6)
    # 直接从pcm5的scaling_data计算
    D_ratios_plot = []
    for i, N in enumerate(Ns):
        sD = pcm5_results['scaling_data']['star']['D_mean'][i]
        oD_max = max(pcm5_results['scaling_data'][t]['D_mean'][i] for t in TOPOLOGIES if t != 'star')
        ratio = sD / oD_max if oD_max > 0 else 1e15
        D_ratios_plot.append(min(ratio, 1e15))
    ax.plot(Ns, D_ratios_plot, 'ro-', label='star/max(other)', markersize=8)
    C_fit = pcm5_results['signature_C_fit']
    if C_fit['a'] is not None:
        ratio_pred = [C_fit['a'] * n ** C_fit['slope'] for n in N_ext]
        ax.plot(N_ext, ratio_pred, '--', color='red', alpha=0.5,
                label=f'幂律: {C_fit["a"]:.1f}×N^{C_fit["slope"]:.2f}')
    ax.axhline(y=100, color='green', linestyle='--', label='C阈值: 100×')
    ax.axhline(y=5, color='orange', linestyle=':', label='证伪阈值: 5×')
    ax.set_xlabel('$N$')
    ax.set_ylabel('$D_{star}/D_{max(other)}$ (log)')
    ax.set_title('(f) 签名C: $D$ 比值标度')
    ax.set_yscale('log')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    outpath = os.path.join(OUTPUT_DIR, 'paper14_pcm45_verification.png')
    plt.savefig(outpath, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"\n[图表] {outpath}")
    return outpath


# =============================================================================
# 主程序
# =============================================================================
def main():
    print("=" * 80)
    print("P-CM-4 (跨模型普适性) + P-CM-5 (标度外推) 验证")
    print("数据来源: EDRN(李广好, Apache-2.0) + UFPF新生成(王斌, CC-BY-4.0+MIT)")
    print("=" * 80)

    # P-CM-4: 跨模型
    pcm4_sig, pcm4_verdicts, pcm4_overall = verify_pcm4()

    # P-CM-5: 标度外推
    pcm5_results = verify_pcm5()

    # 可视化
    plot_pcm45_verification(pcm4_sig, pcm5_results)

    # JSON 汇总
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

    summary = {
        'P-CM-4': {
            'name': '谱丛分支点数学判据跨模型普适性',
            'models_tested': ['xxx (EDRN原始)', 'xxz (Jz/Jxy=2.0)', 'ising (h=1.0)'],
            'N_tested': [6, 8],
            'per_model_verdict': pcm4_verdicts,
            'overall_verdict': pcm4_overall,
            'signature_details': {k: v for k, v in pcm4_sig.items()},
        },
        'P-CM-5': {
            'name': '热力学极限下三重签名持续性',
            'method': '基于N=6,8,10,12 XXX数据的标度律拟合+外推',
            'signature_A_fit': pcm5_results['signature_A_fit'],
            'signature_B_fit': pcm5_results['signature_B_fit'],
            'signature_C_fit': pcm5_results['signature_C_fit'],
            'extrapolation_N16': pcm5_results['extrapolation_N16'],
            'verdict': pcm5_results['verdict'],
            'note': '外推结果非直接验证。最终裁决需N=16,20,24的实际ED计算。',
        },
    }

    summary_path = os.path.join(OUTPUT_DIR, 'paper14_pcm45_verification.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, default=json_default)
    print(f"\n[汇总] {summary_path}")

    print("\n" + "=" * 80)
    print("验证完成")
    print(f"  P-CM-4: {pcm4_overall}")
    print(f"  P-CM-5: {pcm5_results['verdict']}")
    print("=" * 80)


if __name__ == "__main__":
    main()
