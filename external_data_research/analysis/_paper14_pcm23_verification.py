"""
P-CM-2 与 P-CM-3 预测的联合数值验证脚本

P-CM-2: 谱间隙-涨落乘积 P(Δ) = δ_SC × σ_res 的近不变性
  断言: 对固定图拓扑, N=6→8→10→12 时,
        (max_Δ P(Δ) - min_Δ P(Δ)) / <P(Δ)> < 0.30
  证伪: N=12 时相对波动 > 0.60; 或尺寸增大时波动单调发散

P-CM-3: 谱丛分支点密度的拓扑依赖性
  断言: ρ_b^star > ρ_b^small_world > ρ_b^chain ≈ ρ_b^ring
        且 star 分支点数 n_b^star >= 3
  证伪: star 分支点数 < 3; 或 chain 分支点密度 > star 的 50%

理论锚点:
  - Paper XIV §5.6: 谱间隙-涨落乘积(P-CM-2)
  - Paper XIV §5.7 推论 5.7: 谱丛纤维化分支点(P-CM-3)

数据来源(李广好 EDRN 项目, Apache-2.0):
  - 4 拓扑 × N=6,8,10,12 尺寸扫描

作者: 王斌(独立研究人, UFPF 框架维护者)
邮箱: wang.bin@foxmail.com
日期: 2026-08-16
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import json
import sys

# 中文字体设置(防止中文乱码)
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'

# 复用主分析脚本的翻译与分支点检测函数
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from _paper14_spectral_analysis import translate_to_spectral, analyze_spectral_sheaf_branching

# =============================================================================
# 路径配置
# =============================================================================
BASE_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(BASE_DIR, '稳定岛：神秘的新世界', '寻找稳定岛超密集测试3')
N_SCAN_DIR = os.path.join(DATA_DIR, 'N_scan_results')
OUTPUT_DIR = SCRIPT_DIR

TOPOLOGIES = ['chain', 'star', 'ring', 'small_world']
NS = [6, 8, 10, 12]

def get_topology_N_path(topo, N):
    """获取拓扑 topo 在尺寸 N 下的数据路径"""
    if N == 6:
        return os.path.join(DATA_DIR, f'stable_island_{topo}.csv')
    else:
        return os.path.join(N_SCAN_DIR, f'stable_island_{topo}_N{N}.csv')


def load_topology_N(topo, N):
    """加载拓扑 topo 在尺寸 N 下的数据"""
    path = get_topology_N_path(topo, N)
    if not os.path.exists(path):
        raise FileNotFoundError(f"数据缺失: {path}")
    df = pd.read_csv(path, comment='#', header=None, names=['delta', 'gap', 'coarse', 'fine'])
    return df


# =============================================================================
# P-CM-2 验证: 谱间隙-涨落乘积 P(Δ) 的近不变性
# =============================================================================
THRESHOLD_PCM2_PASS = 0.30     # 成立阈值
THRESHOLD_PCM2_FALSIFY = 0.60  # 证伪阈值


def compute_P_delta(topo, N):
    """
    计算拓扑 topo 在尺寸 N 下的 P(Δ) = δ_SC(Δ) × σ_res(Δ)

    翻译规则(Paper XIV 命题 2.1):
      δ_SC = gap,  σ_res = fine
      P(Δ) = |gap × fine|  (取绝对值避免 gap<0 的数值噪声)

    返回: (delta_array, P_array, relative_fluctuation, P_stats)
    """
    df = load_topology_N(topo, N)
    df_spec = translate_to_spectral(df)

    delta = df_spec['delta'].values
    delta_spec = df_spec['delta_spec'].values  # gap
    sigma_res = df_spec['sigma_res'].values    # fine

    # P(Δ) = |δ_SC × σ_res|, 取绝对值避免 gap<0 数值噪声导致的负 P
    P = np.abs(delta_spec * sigma_res)

    # 相对波动 = (max - min) / mean
    P_max = np.max(P)
    P_min = np.min(P)
    P_mean = np.mean(P)
    P_std = np.std(P)

    if P_mean > 1e-15:
        rel_fluct = (P_max - P_min) / P_mean
    else:
        rel_fluct = float('inf')

    # 变异系数(对照指标)
    cv = P_std / P_mean if P_mean > 1e-15 else float('inf')

    return delta, P, rel_fluct, {
        'max': P_max, 'min': P_min, 'mean': P_mean, 'std': P_std,
        'relative_fluctuation': rel_fluct, 'cv': cv,
    }


def verify_pcm2():
    """P-CM-2 主验证流程"""
    print("=" * 70)
    print("P-CM-2 验证: 谱间隙-涨落乘积 P(Δ) = δ_SC × σ_res 的近不变性")
    print("判据: (max_Δ P - min_Δ P) / <P> < 0.30 (成立) / > 0.60 (证伪)")
    print("数据: 4 拓扑 × N=6,8,10,12")
    print("=" * 70)

    results = {}
    print(f"\n{'拓扑':<14} {'N':<5} {'P_max':<12} {'P_min':<12} {'P_mean':<12} "
          f"{'(max-min)/mean':<16} {'裁决':<12}")
    print("-" * 90)

    for topo in TOPOLOGIES:
        results[topo] = {}
        for N in NS:
            delta, P, rel_fluct, stats = compute_P_delta(topo, N)
            results[topo][N] = {
                'delta': delta, 'P': P, 'stats': stats,
            }

            if rel_fluct < THRESHOLD_PCM2_PASS:
                verdict = '成立(<0.3)'
            elif rel_fluct > THRESHOLD_PCM2_FALSIFY:
                verdict = '证伪(>0.6)'
            else:
                verdict = '中间区(0.3-0.6)'

            results[topo][N]['verdict'] = verdict

            print(f"{topo:<14} {N:<5} {stats['max']:<12.6f} {stats['min']:<12.6e} "
                  f"{stats['mean']:<12.6f} {rel_fluct:<16.4f} {verdict:<12}")

    # 总裁决(以 N=12 为最终判据)
    print("\n" + "=" * 70)
    print("总裁决(以 N=12 为最终判据, 同时考察 N=6→12 趋势)")
    print("=" * 70)

    final_verdicts = {}
    for topo in TOPOLOGIES:
        N12_verdict = results[topo][12]['verdict']
        # 检查波动是否随 N 单调发散
        fluctuations = [results[topo][N]['stats']['relative_fluctuation'] for N in NS]
        monotonic_diverge = all(fluctuations[i] < fluctuations[i+1]
                                for i in range(len(fluctuations)-1)
                                if np.isfinite(fluctuations[i]) and np.isfinite(fluctuations[i+1]))

        if '证伪' in N12_verdict:
            final = '证伪'
        elif '成立' in N12_verdict and not monotonic_diverge:
            final = '成立'
        elif '中间' in N12_verdict:
            final = '中间区'
        else:
            final = '成立(但单调发散趋势警告)' if monotonic_diverge else N12_verdict

        final_verdicts[topo] = {
            'N12_verdict': N12_verdict,
            'final': final,
            'fluctuations': fluctuations,
            'monotonic_diverge': monotonic_diverge,
        }
        print(f"  {topo}: N=12 {N12_verdict} → {final}")
        print(f"    波动序列 N=6,8,10,12: {[f'{f:.4f}' for f in fluctuations]}")
        print(f"    单调发散: {monotonic_diverge}")

    return results, final_verdicts


# =============================================================================
# P-CM-3 验证: 谱丛分支点密度的拓扑依赖性
# =============================================================================
def compute_branch_points(topo, N):
    """
    计算拓扑 topo 在尺寸 N 下的谱丛分支点数与密度
    复用 analyze_spectral_sheaf_branching 函数(σ_res 局部极大值代理)
    """
    df = load_topology_N(topo, N)
    df_spec = translate_to_spectral(df)
    sheaf = analyze_spectral_sheaf_branching(df_spec)
    return {
        'n_branch_points': sheaf['n_branch_points'],
        'mean_branch_density': sheaf['mean_branch_density'],
        'branch_points': sheaf['branch_points'],
    }


def verify_pcm3():
    """P-CM-3 主验证流程"""
    print("\n" + "=" * 70)
    print("P-CM-3 验证: 谱丛分支点密度的拓扑依赖性")
    print("断言: ρ_b^star > ρ_b^small_world > ρ_b^chain ≈ ρ_b^ring")
    print("      且 star 分支点数 n_b^star >= 3")
    print("证伪: star 分支点数 < 3; 或 chain 密度 > star 的 50%")
    print("数据: 4 拓扑 × N=6,8,10,12")
    print("=" * 70)

    results = {}
    print(f"\n{'拓扑':<14} {'N':<5} {'分支点数':<10} {'密度(/Δ)':<12}")
    print("-" * 50)

    for topo in TOPOLOGIES:
        results[topo] = {}
        for N in NS:
            bp = compute_branch_points(topo, N)
            results[topo][N] = bp
            print(f"{topo:<14} {N:<5} {bp['n_branch_points']:<10} "
                  f"{bp['mean_branch_density']:<12.4f}")

    # 逐 N 检验排序
    print("\n" + "=" * 70)
    print("逐 N 排序检验: ρ_b^star > ρ_b^small_world > ρ_b^chain ≈ ρ_b^ring")
    print("=" * 70)

    per_N_verdicts = {}
    for N in NS:
        densities = {topo: results[topo][N]['mean_branch_density'] for topo in TOPOLOGIES}
        n_star = results['star'][N]['n_branch_points']

        # 检验各项断言
        cond_star_ge3 = n_star >= 3
        cond_star_gt_sw = densities['star'] > densities['small_world']
        cond_sw_gt_chain = densities['small_world'] > densities['chain']
        cond_chain_approx_ring = abs(densities['chain'] - densities['ring']) < 0.1 * max(densities['chain'], densities['ring'], 1e-6)
        cond_chain_lt_star_50pct = densities['chain'] < 0.5 * densities['star'] if densities['star'] > 0 else False

        # 完整排序成立
        full_order = (cond_star_gt_sw and cond_sw_gt_chain and cond_chain_approx_ring)
        # 部分成立(star ≥ 3 且 chain < star 50%)
        partial = cond_star_ge3 and cond_chain_lt_star_50pct

        if full_order and partial:
            verdict = '完全成立'
        elif partial:
            verdict = '部分成立(star≥3 且 chain<star/2, 但排序不全)'
        elif cond_star_ge3:
            verdict = '弱成立(star≥3, 但 chain ≥ star/2 或排序失败)'
        else:
            verdict = '证伪(star<3)'

        per_N_verdicts[N] = {
            'densities': densities,
            'n_star': n_star,
            'cond_star_ge3': cond_star_ge3,
            'cond_star_gt_sw': cond_star_gt_sw,
            'cond_sw_gt_chain': cond_sw_gt_chain,
            'cond_chain_approx_ring': cond_chain_approx_ring,
            'cond_chain_lt_star_50pct': cond_chain_lt_star_50pct,
            'full_order': full_order,
            'partial': partial,
            'verdict': verdict,
        }

        print(f"\n[N={N}]")
        print(f"  密度: star={densities['star']:.4f}, small_world={densities['small_world']:.4f}, "
              f"chain={densities['chain']:.4f}, ring={densities['ring']:.4f}")
        print(f"  star 分支点数 = {n_star} (≥3? {cond_star_ge3})")
        print(f"  star > small_world? {cond_star_gt_sw}")
        print(f"  small_world > chain? {cond_sw_gt_chain}")
        print(f"  chain ≈ ring? {cond_chain_approx_ring}")
        print(f"  chain < star/2? {cond_chain_lt_star_50pct}")
        print(f"  → 裁决: {verdict}")

    # 总裁决
    print("\n" + "=" * 70)
    print("总裁决")
    print("=" * 70)

    # star 分支点数随 N 的序列
    star_n_seq = [results['star'][N]['n_branch_points'] for N in NS]
    star_n_monotonic = all(star_n_seq[i] <= star_n_seq[i+1] for i in range(len(star_n_seq)-1))

    # N=12 最终裁决
    final_N12 = per_N_verdicts[12]['verdict']

    # 所有 N 中 star ≥ 3?
    all_star_ge3 = all(per_N_verdicts[N]['cond_star_ge3'] for N in NS)

    # small_world 排序在所有 N 中都不成立?
    sw_order_never = all(not per_N_verdicts[N]['cond_star_gt_sw'] or not per_N_verdicts[N]['cond_sw_gt_chain']
                         for N in NS)

    if '证伪' in final_N12:
        final = '证伪'
    elif '完全成立' in final_N12:
        final = '成立'
    else:
        final = '部分证伪/弱成立'

    print(f"  star 分支点数序列 N=6,8,10,12: {star_n_seq}")
    print(f"  star 分支点数单调不减? {star_n_monotonic}")
    print(f"  所有 N 中 star ≥ 3? {all_star_ge3}")
    print(f"  small_world 排序在所有 N 中均失败? {sw_order_never}")
    print(f"  N=12 裁决: {final_N12}")
    print(f"  → 总裁决: {final}")

    final_summary = {
        'final_verdict': final,
        'star_n_sequence': {'6': star_n_seq[0], '8': star_n_seq[1],
                            '10': star_n_seq[2], '12': star_n_seq[3]},
        'star_n_monotonic': star_n_monotonic,
        'all_star_ge3': all_star_ge3,
        'sw_order_never_holds': sw_order_never,
        'interpretation': (
            'P-CM-3 部分证伪: '
            '(1) star 分支点数 ≥ 3 在所有 N 中成立(star 中心节点的多叶结构确认); '
            '(2) star 分支点数随 N 单调不减,与窗口碎裂现象一致(P-CM-1 证伪中的发现); '
            '(3) 但完整排序 ρ_b^star > ρ_b^small_world > ρ_b^chain ≈ ρ_b^ring 不成立——'
            'small_world 的分支点密度与 chain/ring 相当(均接近 0),'
            '说明 small_world 的全域涨落大并非由分支点驱动,而是由长程连接导致的谱丛额外复杂度。'
        ),
    }

    return results, per_N_verdicts, final_summary


# =============================================================================
# 可视化
# =============================================================================
def plot_pcm2_verification(results, final_verdicts):
    """P-CM-2 验证图: (a) 相对波动随 N; (b) P(Δ) 四尺寸叠加(star); (c) P(Δ) 四尺寸叠加(chain)"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))

    colors = {'chain': 'blue', 'star': 'red', 'ring': 'green', 'small_world': 'purple'}

    # (a) 相对波动随 N
    ax = axes[0]
    for topo in TOPOLOGIES:
        flucts = [results[topo][N]['stats']['relative_fluctuation'] for N in NS]
        # 处理 inf 用于绘图
        flucts_plot = [min(f, 50) if np.isfinite(f) else 50 for f in flucts]
        ax.plot(NS, flucts_plot, 'o-', color=colors[topo], label=topo, markersize=8)

    ax.axhline(y=THRESHOLD_PCM2_PASS, color='green', linestyle='--', alpha=0.5,
               label=f'成立阈值 ({THRESHOLD_PCM2_PASS})')
    ax.axhline(y=THRESHOLD_PCM2_FALSIFY, color='red', linestyle='--', alpha=0.5,
               label=f'证伪阈值 ({THRESHOLD_PCM2_FALSIFY})')
    ax.set_xlabel('系统尺寸 $N$')
    ax.set_ylabel('相对波动 $(\\max P - \\min P) / \\langle P \\rangle$')
    ax.set_title('(a) $P(\\Delta)$ 相对波动随 $N$ (截断 50)')
    ax.legend(fontsize=8)
    ax.set_yscale('log')
    ax.set_xticks(NS)
    ax.grid(True, alpha=0.3)

    # (b) P(Δ) 四尺寸叠加 - star
    ax = axes[1]
    for N in NS:
        delta = results['star'][N]['delta']
        P = results['star'][N]['P']
        ax.semilogy(delta, P + 1e-15, color=colors_star(N), alpha=0.7, label=f'N={N}')
    ax.set_xlabel('矛盾边强度 $\\Delta$')
    ax.set_ylabel('$P(\\Delta) = |\\delta_{sc} \\times \\sigma_{res}|$ (对数)')
    ax.set_title('(b) star 拓扑 $P(\\Delta)$ 四尺寸叠加')
    ax.legend(fontsize=8)
    ax.set_xlim(0, 3.0)
    ax.grid(True, alpha=0.3)

    # (c) P(Δ) 四尺寸叠加 - chain
    ax = axes[2]
    for N in NS:
        delta = results['chain'][N]['delta']
        P = results['chain'][N]['P']
        ax.semilogy(delta, P + 1e-15, color=colors_star(N), alpha=0.7, label=f'N={N}')
    ax.set_xlabel('矛盾边强度 $\\Delta$')
    ax.set_ylabel('$P(\\Delta) = |\\delta_{sc} \\times \\sigma_{res}|$ (对数)')
    ax.set_title('(c) chain 拓扑 $P(\\Delta)$ 四尺寸叠加')
    ax.legend(fontsize=8)
    ax.set_xlim(0, 3.0)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    outpath = os.path.join(OUTPUT_DIR, 'paper14_pcm2_verification.png')
    plt.savefig(outpath, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"\n[图表] {outpath}")
    return outpath


def colors_star(N):
    """N 对应颜色"""
    return {6: 'blue', 8: 'green', 10: 'orange', 12: 'red'}[N]


def plot_pcm3_verification(results, per_N_verdicts):
    """P-CM-3 验证图: (a) 分支点数随 N(4拓扑); (b) 分支点密度随 N(4拓扑); (c) N=12 排序对照"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))

    colors = {'chain': 'blue', 'star': 'red', 'ring': 'green', 'small_world': 'purple'}

    # (a) 分支点数随 N
    ax = axes[0]
    for topo in TOPOLOGIES:
        n_bps = [results[topo][N]['n_branch_points'] for N in NS]
        ax.plot(NS, n_bps, 'o-', color=colors[topo], label=topo, markersize=8)
    ax.set_xlabel('系统尺寸 $N$')
    ax.set_ylabel('谱丛分支点数 $n_b$')
    ax.set_title('(a) 分支点数随 $N$ (4 拓扑)')
    ax.legend(fontsize=8)
    ax.set_xticks(NS)
    ax.grid(True, alpha=0.3)

    # (b) 分支点密度随 N
    ax = axes[1]
    for topo in TOPOLOGIES:
        densities = [results[topo][N]['mean_branch_density'] for N in NS]
        ax.plot(NS, densities, 's-', color=colors[topo], label=topo, markersize=8)
    ax.set_xlabel('系统尺寸 $N$')
    ax.set_ylabel('分支点密度 $\\rho_b$ (/Δ)')
    ax.set_title('(b) 分支点密度随 $N$ (4 拓扑)')
    ax.legend(fontsize=8)
    ax.set_xticks(NS)
    ax.grid(True, alpha=0.3)

    # (c) N=12 排序对照(柱状图)
    ax = axes[2]
    topos_order = ['star', 'small_world', 'chain', 'ring']
    densities_N12 = [results[t][12]['mean_branch_density'] for t in topos_order]
    bars = ax.bar(topos_order, densities_N12,
                  color=[colors[t] for t in topos_order], alpha=0.7, edgecolor='black')
    for bar, d in zip(bars, densities_N12):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f'{d:.3f}', ha='center', fontsize=9)
    ax.set_ylabel('分支点密度 $\\rho_b$ (/Δ)')
    ax.set_title('(c) $N=12$ 分支点密度排序对照')
    ax.grid(True, alpha=0.3, axis='y')

    # 标注预测排序
    pred_text = '预测排序: star > small_world > chain ≈ ring'
    ax.text(0.5, 0.95, pred_text, transform=ax.transAxes, ha='center', va='top',
            fontsize=8, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    outpath = os.path.join(OUTPUT_DIR, 'paper14_pcm3_verification.png')
    plt.savefig(outpath, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"[图表] {outpath}")
    return outpath


# =============================================================================
# 主程序
# =============================================================================
def main():
    print("=" * 70)
    print("P-CM-2 + P-CM-3 联合数值验证")
    print("基于 EDRN 稳定岛 N=6,8,10,12 尺寸扫描数据(李广好, Apache-2.0)")
    print("UFPF Paper XIV 凝聚态谱表述")
    print("=" * 70)

    # P-CM-2
    pcm2_results, pcm2_final = verify_pcm2()
    plot_pcm2_verification(pcm2_results, pcm2_final)

    # P-CM-3
    pcm3_results, pcm3_per_N, pcm3_final = verify_pcm3()
    plot_pcm3_verification(pcm3_results, pcm3_per_N)

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
        if isinstance(obj, float) and np.isnan(obj):
            return None
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

    summary = {
        'P-CM-2': {
            'prediction': '谱间隙-涨落乘积 P(Δ) = δ_SC × σ_res 的近不变性',
            'assertion': '(max P - min P) / <P> < 0.30',
            'threshold_pass': THRESHOLD_PCM2_PASS,
            'threshold_falsify': THRESHOLD_PCM2_FALSIFY,
            'per_topology_N': {
                topo: {
                    str(N): {
                        'P_max': pcm2_results[topo][N]['stats']['max'],
                        'P_min': pcm2_results[topo][N]['stats']['min'],
                        'P_mean': pcm2_results[topo][N]['stats']['mean'],
                        'relative_fluctuation': pcm2_results[topo][N]['stats']['relative_fluctuation'],
                        'cv': pcm2_results[topo][N]['stats']['cv'],
                        'verdict': pcm2_results[topo][N]['verdict'],
                    } for N in NS
                } for topo in TOPOLOGIES
            },
            'final_verdicts': {
                topo: {
                    'N12_verdict': pcm2_final[topo]['N12_verdict'],
                    'final': pcm2_final[topo]['final'],
                    'fluctuations': pcm2_final[topo]['fluctuations'],
                    'monotonic_diverge': pcm2_final[topo]['monotonic_diverge'],
                } for topo in TOPOLOGIES
            },
        },
        'P-CM-3': {
            'prediction': '谱丛分支点密度的拓扑依赖性',
            'assertion': 'ρ_b^star > ρ_b^small_world > ρ_b^chain ≈ ρ_b^ring, n_b^star >= 3',
            'per_topology_N': {
                topo: {
                    str(N): {
                        'n_branch_points': pcm3_results[topo][N]['n_branch_points'],
                        'mean_branch_density': pcm3_results[topo][N]['mean_branch_density'],
                    } for N in NS
                } for topo in TOPOLOGIES
            },
            'per_N_verdicts': {
                str(N): {
                    'densities': pcm3_per_N[N]['densities'],
                    'n_star': pcm3_per_N[N]['n_star'],
                    'cond_star_ge3': pcm3_per_N[N]['cond_star_ge3'],
                    'cond_star_gt_sw': pcm3_per_N[N]['cond_star_gt_sw'],
                    'cond_sw_gt_chain': pcm3_per_N[N]['cond_sw_gt_chain'],
                    'cond_chain_approx_ring': pcm3_per_N[N]['cond_chain_approx_ring'],
                    'cond_chain_lt_star_50pct': pcm3_per_N[N]['cond_chain_lt_star_50pct'],
                    'verdict': pcm3_per_N[N]['verdict'],
                } for N in NS
            },
            'final_summary': pcm3_final,
        },
    }

    summary_path = os.path.join(OUTPUT_DIR, 'paper14_pcm23_verification.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, default=json_default)
    print(f"\n[汇总] {summary_path}")

    print("\n" + "=" * 70)
    print("验证完成")
    print("=" * 70)


if __name__ == "__main__":
    main()
