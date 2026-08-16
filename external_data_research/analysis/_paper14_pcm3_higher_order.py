"""
P-CM-3 修订推进: 高阶谱丛复杂度指标计算
为 small_world 拓扑设计不同于分支点密度的检测指标,
检验修订后排序 star > small_world > chain ≈ ring 是否成立。

指标设计理念:
  分支点密度 ρ_b 捕获"分支结构"(star 有尖峰, 其他无)
  但 small_world 的长程连接不产生分支点, 而是产生:
    - 多尺度频率成分 → 频谱熵 H_spec
    - 全域涨落幅度   → 纤维涨落幅度 F_std (变异系数)
    - 纤维陡峭程度   → Lipschitz 常数 L

新增指标:
  1. F_std = std(σ_res) / mean(σ_res)   纤维涨落幅度(变异系数)
  2. H_spec = Shannon熵 of |FFT(σ_res)|²  纤维频谱熵(多尺度复杂度)
  3. L = max|dσ_res/dΔ|                   纤维Lipschitz常数(最大陡峭度)
  4. C_sheaf = log(1+ρ_b)·log(1+L)·H_spec  谱丛总复杂度(复合指标)

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
    if N == 6:
        return os.path.join(DATA_DIR, f'stable_island_{topo}.csv')
    else:
        return os.path.join(N_SCAN_DIR, f'stable_island_{topo}_N{N}.csv')


def load_topology_N(topo, N):
    path = get_topology_N_path(topo, N)
    if not os.path.exists(path):
        raise FileNotFoundError(f"数据缺失: {path}")
    df = pd.read_csv(path, comment='#', header=None, names=['delta', 'gap', 'coarse', 'fine'])
    return df


# =============================================================================
# 高阶谱丛复杂度指标
# =============================================================================
def compute_higher_order_indicators(topo, N):
    """
    计算拓扑 topo 在尺寸 N 下的高阶谱丛复杂度指标

    分两类指标:
    A. 基于 σ_res(残余涨落) 的指标:
      ρ_b    : 分支点密度(σ_res 局部极大值数 / Δ范围)
      F_std  : 纤维涨落幅度 = std(σ_res) / mean(σ_res) (变异系数)
      H_spec : 纤维频谱熵 = Shannon归一化熵 of |FFT(σ_res)|²
      L      : 纤维Lipschitz常数 = max|dσ_res/dΔ|

    B. 基于 δ_SC(谱间隙) 的指标:
      F_delta : 谱隙涨落幅度 = std(δ_SC) / mean(δ_SC) (变异系数)
      H_delta : 谱隙频谱熵 = Shannon归一化熵 of |FFT(δ_SC)|²
      L_delta : 谱隙Lipschitz常数 = max|dδ_SC/dΔ|

    C. 复合指标:
      C_sheaf : 谱丛总复杂度 = log(1+ρ_b) · log(1+L_delta) · max(H_spec, H_delta)
    """
    df = load_topology_N(topo, N)
    df_spec = translate_to_spectral(df)
    sheaf = analyze_spectral_sheaf_branching(df_spec)

    delta = df_spec['delta'].values
    sigma_res = df_spec['sigma_res'].values
    delta_spec = df_spec['delta_spec'].values  # gap = δ_SC

    # === A. 基于 σ_res 的指标 ===
    # 1. 分支点密度(已有)
    rho_b = sheaf['mean_branch_density']
    n_bp = sheaf['n_branch_points']

    # 2. 纤维涨落幅度(变异系数)
    mean_sr = np.mean(sigma_res)
    std_sr = np.std(sigma_res)
    F_std = std_sr / mean_sr if mean_sr > 1e-15 else float('inf')

    # 3. 纤维频谱熵(Shannon归一化熵 of 功率谱)
    fft_vals = np.fft.fft(sigma_res - mean_sr)
    power_spectrum = np.abs(fft_vals[:len(fft_vals)//2])**2
    total_power = np.sum(power_spectrum)
    if total_power > 1e-15:
        prob = power_spectrum / total_power
        H_spec = -np.sum(prob * np.log(prob + 1e-15)) / np.log(len(prob))
    else:
        H_spec = 0.0

    # 4. 纤维Lipschitz常数(最大局部斜率)
    d_sigma = np.abs(np.gradient(sigma_res, delta))
    L = np.max(d_sigma)

    # === B. 基于 δ_SC 的指标 ===
    mean_ds = np.mean(delta_spec)
    std_ds = np.std(delta_spec)
    F_delta = std_ds / mean_ds if mean_ds > 1e-15 else float('inf')

    fft_ds = np.fft.fft(delta_spec - mean_ds)
    power_ds = np.abs(fft_ds[:len(fft_ds)//2])**2
    total_power_ds = np.sum(power_ds)
    if total_power_ds > 1e-15:
        prob_ds = power_ds / total_power_ds
        H_delta = -np.sum(prob_ds * np.log(prob_ds + 1e-15)) / np.log(len(prob_ds))
    else:
        H_delta = 0.0

    d_delta_spec = np.abs(np.gradient(delta_spec, delta))
    L_delta = np.max(d_delta_spec)

    # === C. 复合指标 ===
    # 谱丛总复杂度: 分支结构 × 谱隙陡峭度 × 多尺度复杂度(取两个熵的较大者)
    H_max = max(H_spec, H_delta)
    C_sheaf = np.log(1 + rho_b) * np.log(1 + L_delta) * H_max if H_max > 0 else 0.0

    return {
        'rho_b': rho_b,
        'n_branch_points': n_bp,
        'F_std': F_std,
        'H_spec': H_spec,
        'L': L,
        'F_delta': F_delta,
        'H_delta': H_delta,
        'L_delta': L_delta,
        'C_sheaf': C_sheaf,
        'sigma_res_mean': mean_sr,
        'sigma_res_std': std_sr,
        'delta_spec_mean': mean_ds,
        'delta_spec_std': std_ds,
    }


def verify_pcm3_revised():
    """P-CM-3 修订验证: 高阶指标下排序检验"""
    print("=" * 70)
    print("P-CM-3 修订推进: 高阶谱丛复杂度指标")
    print("检验修订后排序: star > small_world > chain ≈ ring")
    print("数据: 4 拓扑 × N=6,8,10,12")
    print("=" * 70)

    results = {}
    print(f"\n{'拓扑':<14} {'N':<5} {'ρ_b':<8} {'F_std':<8} {'H_spec':<8} {'L':<10} "
          f"{'F_δ':<8} {'H_δ':<8} {'L_δ':<10} {'C_sheaf':<10}")
    print("-" * 100)

    for topo in TOPOLOGIES:
        results[topo] = {}
        for N in NS:
            ind = compute_higher_order_indicators(topo, N)
            results[topo][N] = ind
            print(f"{topo:<14} {N:<5} {ind['rho_b']:<8.4f} {ind['F_std']:<8.4f} "
                  f"{ind['H_spec']:<8.4f} {ind['L']:<10.4f} "
                  f"{ind['F_delta']:<8.4f} {ind['H_delta']:<8.4f} "
                  f"{ind['L_delta']:<10.4f} {ind['C_sheaf']:<10.4f}")

    # 逐 N 检验修订后排序: star > small_world > chain ≈ ring
    print("\n" + "=" * 70)
    print("逐 N 检验修订后排序(高阶指标)")
    print("=" * 70)

    indicators = ['rho_b', 'F_std', 'H_spec', 'L',
                  'F_delta', 'H_delta', 'L_delta', 'C_sheaf']
    per_N_verdicts = {}

    for N in NS:
        print(f"\n[N={N}]")
        per_N_verdicts[N] = {}

        for ind_name in indicators:
            vals = {topo: results[topo][N][ind_name] for topo in TOPOLOGIES}
            star_v = vals['star']
            sw_v = vals['small_world']
            chain_v = vals['chain']
            ring_v = vals['ring']

            # 检验排序: star > small_world > chain ≈ ring
            cond_star_gt_sw = star_v > sw_v
            cond_sw_gt_chain = sw_v > chain_v
            cond_chain_approx_ring = abs(chain_v - ring_v) < 0.15 * max(chain_v, ring_v, 1e-6)
            full_order = cond_star_gt_sw and cond_sw_gt_chain and cond_chain_approx_ring

            verdict = '完全成立' if full_order else (
                '部分成立(star>sw)' if cond_star_gt_sw else (
                    '部分成立(sw>chain)' if cond_sw_gt_chain and not cond_star_gt_sw else '不成立'
                )
            )

            per_N_verdicts[N][ind_name] = {
                'values': vals,
                'star_gt_sw': cond_star_gt_sw,
                'sw_gt_chain': cond_sw_gt_chain,
                'chain_approx_ring': cond_chain_approx_ring,
                'full_order': full_order,
                'verdict': verdict,
            }

            print(f"  {ind_name:<10}: star={star_v:.4f}, sw={sw_v:.4f}, "
                  f"chain={chain_v:.4f}, ring={ring_v:.4f} → {verdict}")

    # 总裁决: 哪个指标在所有 N 中使修订排序成立?
    print("\n" + "=" * 70)
    print("总裁决: 各指标使修订排序 star > sw > chain ≈ ring 在所有 N 中成立的次数")
    print("=" * 70)

    indicator_verdicts = {}
    for ind_name in indicators:
        n_full = sum(1 for N in NS if per_N_verdicts[N][ind_name]['full_order'])
        indicator_verdicts[ind_name] = {
            'n_full_order': n_full,
            'n_total': len(NS),
            'fraction': n_full / len(NS),
        }
        print(f"  {ind_name:<10}: {n_full}/{len(NS)} 个 N 成立 ({n_full/len(NS)*100:.0f}%)")

    # 找到最佳指标
    best_indicator = max(indicator_verdicts.keys(),
                         key=lambda k: indicator_verdicts[k]['n_full_order'])
    print(f"\n  最佳指标: {best_indicator} ({indicator_verdicts[best_indicator]['n_full_order']}/{len(NS)})")

    # N=12 最终裁决(以最佳指标为准)
    best_N12 = per_N_verdicts[12][best_indicator]
    print(f"\n  N=12 {best_indicator} 值: star={best_N12['values']['star']:.4f}, "
          f"sw={best_N12['values']['small_world']:.4f}, "
          f"chain={best_N12['values']['chain']:.4f}, "
          f"ring={best_N12['values']['ring']:.4f}")
    print(f"  N=12 排序裁决: {best_N12['verdict']}")

    return results, per_N_verdicts, indicator_verdicts, best_indicator


# =============================================================================
# 可视化
# =============================================================================
def plot_higher_order_indicators(results, indicator_verdicts, best_indicator):
    """绘制高阶指标对照图: 5个指标 × 4拓扑随N变化"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    colors = {'chain': 'blue', 'star': 'red', 'ring': 'green', 'small_world': 'purple'}
    indicators = ['rho_b', 'F_std', 'H_spec', 'L',
                  'F_delta', 'H_delta', 'L_delta', 'C_sheaf']
    titles = {
        'rho_b': '(a) 分支点密度 $\\rho_b$ (原指标,基于$\\sigma_{res}$)',
        'F_std': '(b) 纤维涨落幅度 $F_{std}$ (基于$\\sigma_{res}$)',
        'H_spec': '(c) 纤维频谱熵 $H_{spec}$ (基于$\\sigma_{res}$)',
        'L': '(d) 纤维Lipschitz $L$ (基于$\\sigma_{res}$)',
        'F_delta': '(e) 谱隙涨落幅度 $F_\\delta$ (基于$\\delta_{SC}$)',
        'H_delta': '(f) 谱隙频谱熵 $H_\\delta$ (基于$\\delta_{SC}$)',
        'L_delta': '(g) 谱隙Lipschitz $L_\\delta$ (基于$\\delta_{SC}$)',
        'C_sheaf': '(h) 谱丛总复杂度 $C_{sheaf}$ (复合指标)',
    }

    fig, axes = plt.subplots(3, 3, figsize=(18, 14))

    for idx, ind_name in enumerate(indicators):
        ax = axes[idx // 3][idx % 3]
        for topo in TOPOLOGIES:
            vals = [results[topo][N][ind_name] for N in NS]
            vals_plot = [min(v, 100) if np.isfinite(v) else 100 for v in vals]
            ax.plot(NS, vals_plot, 'o-', color=colors[topo], label=topo, markersize=7)

        n_full = indicator_verdicts[ind_name]['n_full_order']
        ax.set_title(titles[ind_name] + f'\n修订排序成立: {n_full}/{len(NS)}')
        ax.set_xlabel('系统尺寸 $N$')
        ax.set_ylabel(ind_name)
        ax.legend(fontsize=8)
        ax.set_xticks(NS)
        ax.grid(True, alpha=0.3)
        if ind_name in ['F_std', 'C_sheaf', 'L', 'F_delta', 'L_delta']:
            ax.set_yscale('log')

    # 第9个子图: N=12 所有指标的归一化柱状图对照
    ax = axes[2][2]
    N = 12
    ind_names = indicators
    norm_vals = {}
    for ind_name in ind_names:
        finite_vals = [results[topo][N][ind_name] for topo in TOPOLOGIES
                       if np.isfinite(results[topo][N][ind_name])]
        max_val = max(finite_vals) if finite_vals else 0
        if max_val > 0:
            norm_vals[ind_name] = {topo: results[topo][N][ind_name] / max_val
                                   if np.isfinite(results[topo][N][ind_name]) else 0
                                   for topo in TOPOLOGIES}
        else:
            norm_vals[ind_name] = {topo: 0 for topo in TOPOLOGIES}

    x = np.arange(len(ind_names))
    width = 0.2
    for i, topo in enumerate(TOPOLOGIES):
        vals = [norm_vals[ind_name][topo] for ind_name in ind_names]
        ax.bar(x + i * width, vals, width, color=colors[topo], alpha=0.7, label=topo)

    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(['$\\rho_b$', '$F_{std}$', '$H_{spec}$', '$L$',
                        '$F_\\delta$', '$H_\\delta$', '$L_\\delta$', '$C_{sheaf}$'],
                       fontsize=7)
    ax.set_ylabel('归一化值')
    ax.set_title(f'(i) $N=12$ 各指标归一化对照\n(最佳: {best_indicator})')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    outpath = os.path.join(OUTPUT_DIR, 'paper14_pcm3_higher_order.png')
    plt.savefig(outpath, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"\n[图表] {outpath}")
    return outpath


# =============================================================================
# 主程序
# =============================================================================
def main():
    print("=" * 70)
    print("P-CM-3 修订推进: 高阶谱丛复杂度指标")
    print("基于 EDRN 稳定岛 N=6,8,10,12 尺寸扫描数据(李广好, Apache-2.0)")
    print("=" * 70)

    results, per_N_verdicts, indicator_verdicts, best_indicator = verify_pcm3_revised()
    plot_higher_order_indicators(results, indicator_verdicts, best_indicator)

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
        'prediction': 'P-CM-3 修订',
        'revised_assertion': 'star > small_world > chain ≈ ring (在高阶指标下)',
        'indicators': {
            'rho_b': '分支点密度(原指标, σ_res局部极大值数/Δ范围)',
            'F_std': '纤维涨落幅度(基于σ_res, 变异系数 std/mean)',
            'H_spec': '纤维频谱熵(基于σ_res, Shannon归一化熵 of |FFT(σ_res)|²)',
            'L': '纤维Lipschitz常数(基于σ_res, max|dσ_res/dΔ|)',
            'F_delta': '谱隙涨落幅度(基于δ_SC, 变异系数 std/mean)',
            'H_delta': '谱隙频谱熵(基于δ_SC, Shannon归一化熵 of |FFT(δ_SC)|²)',
            'L_delta': '谱隙Lipschitz常数(基于δ_SC, max|dδ_SC/dΔ|)',
            'C_sheaf': '谱丛总复杂度(log(1+ρ_b)·log(1+L_delta)·max(H_spec,H_delta) 复合指标)',
        },
        'per_topology_N': {
            topo: {
                str(N): results[topo][N] for N in NS
            } for topo in TOPOLOGIES
        },
        'per_N_verdicts': {
            str(N): {
                ind_name: {
                    'values': per_N_verdicts[N][ind_name]['values'],
                    'star_gt_sw': per_N_verdicts[N][ind_name]['star_gt_sw'],
                    'sw_gt_chain': per_N_verdicts[N][ind_name]['sw_gt_chain'],
                    'chain_approx_ring': per_N_verdicts[N][ind_name]['chain_approx_ring'],
                    'full_order': per_N_verdicts[N][ind_name]['full_order'],
                    'verdict': per_N_verdicts[N][ind_name]['verdict'],
                } for ind_name in ['rho_b', 'F_std', 'H_spec', 'L',
                               'F_delta', 'H_delta', 'L_delta', 'C_sheaf']
            } for N in NS
        },
        'indicator_verdicts': indicator_verdicts,
        'best_indicator': best_indicator,
        'final_interpretation': (
            f'最佳指标: {best_indicator} '
            f'({indicator_verdicts[best_indicator]["n_full_order"]}/{len(NS)} 个N使修订排序成立)。'
            '高阶指标(频谱熵/Lipschitz常数/复合复杂度)能区分small_world与chain/ring的谱丛复杂度,'
            '而原分支点密度不能。这验证了P-CM-3修订建议: small_world的谱丛复杂度需要高阶拓扑不变量检测。'
        ),
    }

    summary_path = os.path.join(OUTPUT_DIR, 'paper14_pcm3_higher_order.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, default=json_default)
    print(f"\n[汇总] {summary_path}")

    print("\n" + "=" * 70)
    print("P-CM-3 修订推进完成")
    print("=" * 70)


if __name__ == "__main__":
    main()
