"""
P-CM-1 预测的数值验证脚本
利用 EDRN 项目提供的 N=6, 8, 10, 12 尺寸扫描数据,
对 star 拓扑的谱间隙锁定窗口(稳定岛)中心 Δ_center 随尺寸 N 的漂移进行裁决。

预测 P-CM-1 断言:
  |Δ_center(N) - Δ_center(N=6)| / IslandWidth(N=6) < 0.2

证伪条件:
  漂移 > 50% 宽度;或锁定窗口消失

理论锚点:
  - Paper XIV 命题 2.2: 谱间隙锁定/坍缩是量子相变标志
  - 量子相变临界点 g_c 由拓扑不变量决定,与尺寸 N 无关

数据来源(李广好 EDRN 项目, Apache-2.0):
  - N=6:  stable_island_star.csv
  - N=8:  N_scan_results/stable_island_star_N8.csv
  - N=10: N_scan_results/stable_island_star_N10.csv
  - N=12: N_scan_results/stable_island_star_N12.csv

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

# 复用主分析脚本的翻译与检测函数
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from _paper14_spectral_analysis import translate_to_spectral, detect_spectral_gap_locking

# =============================================================================
# 路径配置
# =============================================================================
BASE_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(BASE_DIR, '稳定岛：神秘的新世界', '寻找稳定岛超密集测试3')
N_SCAN_DIR = os.path.join(DATA_DIR, 'N_scan_results')
OUTPUT_DIR = SCRIPT_DIR

# star 拓扑的 N 扫描数据路径
STAR_FILES = {
    6:  os.path.join(DATA_DIR, 'stable_island_star.csv'),
    8:  os.path.join(N_SCAN_DIR, 'stable_island_star_N8.csv'),
    10: os.path.join(N_SCAN_DIR, 'stable_island_star_N10.csv'),
    12: os.path.join(N_SCAN_DIR, 'stable_island_star_N12.csv'),
}

THRESHOLD_PASS = 0.2    # P-CM-1 断言阈值
THRESHOLD_FALSIFY = 0.5  # 证伪阈值


def load_star_data(N):
    """加载 star 拓扑在尺寸 N 下的数据"""
    path = STAR_FILES[N]
    if not os.path.exists(path):
        raise FileNotFoundError(f"尺寸 N={N} 的 star 数据缺失: {path}")
    df = pd.read_csv(path, comment='#', header=None, names=['delta', 'gap', 'coarse', 'fine'])
    return df


def detect_island_center_and_width(df):
    """
    对 star 数据做谱量翻译 + 锁定窗口检测,
    返回 (中心 Δ_center, 宽度, 完整窗口信息列表, df_spec)
    若多个窗口, 取最窄(最稳定)的一个; 若无窗口, 返回 (None, 0, [], df_spec)

    同时返回最宽窗口信息用于对照分析(揭示窗口碎裂现象)
    """
    df_spec = translate_to_spectral(df)
    islands = detect_spectral_gap_locking(df_spec)
    if not islands:
        return None, 0.0, [], df_spec

    # 取最窄窗口(最稳定的锁定区) — P-CM-1 主判据
    narrowest = min(islands, key=lambda x: x['width'])
    center = (narrowest['start'] + narrowest['end']) / 2.0
    width = narrowest['width']
    return center, width, islands, df_spec


def detect_widest_island(df):
    """对照分析: 取最宽窗口(主导锁定区), 用于揭示窗口碎裂现象"""
    df_spec = translate_to_spectral(df)
    islands = detect_spectral_gap_locking(df_spec)
    if not islands:
        return None, 0.0
    widest = max(islands, key=lambda x: x['width'])
    center = (widest['start'] + widest['end']) / 2.0
    width = widest['width']
    return center, width


def verify_pcm1():
    """P-CM-1 主验证流程"""
    print("=" * 70)
    print("P-CM-1 预测验证: 谱间隙锁定窗口的拓扑不变性")
    print("数据对象: star 拓扑, N = 6, 8, 10, 12")
    print("判据: |Δ_center(N) - Δ_center(N=6)| / IslandWidth(N=6) < 0.2")
    print("=" * 70)

    # 加载并检测每个 N 的锁定窗口
    results = {}
    df_specs = {}
    for N in [6, 8, 10, 12]:
        print(f"\n[N={N}] 加载并检测 star 锁定窗口...")
        df = load_star_data(N)
        center, width, islands, df_spec = detect_island_center_and_width(df)
        wide_center, wide_width = detect_widest_island(df)
        df_specs[N] = df_spec
        results[N] = {
            'center': center,
            'width': width,
            'n_islands': len(islands),
            'islands': islands,
            'widest_center': wide_center,
            'widest_width': wide_width,
        }
        if islands:
            print(f"  检测到 {len(islands)} 个窗口")
            for i, isl in enumerate(islands):
                print(f"    窗口{i+1}: Δ∈[{isl['start']:.4f}, {isl['end']:.4f}], "
                      f"宽度={isl['width']:.4f}, "
                      f"σ_res均值={isl['sigma_res_mean']:.6f}, "
                      f"δ_sc均值={isl['delta_spec_mean']:.6e}")
            print(f"  → 最窄窗口(主判据): Δ_center = {center:.4f}, 宽度 = {width:.4f}")
            print(f"  → 最宽窗口(对照):   Δ_center = {wide_center:.4f}, 宽度 = {wide_width:.4f}")
        else:
            print(f"  未检测到锁定窗口 → 锁定窗口消失")

    # 以 N=6 为基准计算漂移比
    base_center = results[6]['center']
    base_width = results[6]['width']

    print("\n" + "=" * 70)
    print("P-CM-1 漂移比裁决")
    print("=" * 70)
    print(f"基准: N=6, Δ_center = {base_center:.4f}, IslandWidth = {base_width:.4f}")
    print(f"\n{'N':<5} {'Δ_center':<12} {'宽度':<10} {'漂移|Δc-Δc6|':<15} {'漂移/宽度6':<12} {'裁决':<10}")
    print("-" * 70)

    verdict_per_N = {}
    for N in [8, 10, 12]:
        center_N = results[N]['center']
        width_N = results[N]['width']

        if center_N is None:
            # 锁定窗口消失 → 证伪
            drift = float('nan')
            ratio = float('inf')
            verdict = '证伪(窗口消失)'
        else:
            drift = abs(center_N - base_center)
            ratio = drift / base_width if base_width > 1e-15 else float('inf')
            if ratio < THRESHOLD_PASS:
                verdict = '成立(<0.2)'
            elif ratio > THRESHOLD_FALSIFY:
                verdict = '证伪(>0.5)'
            else:
                verdict = '中间区(0.2-0.5)'

        verdict_per_N[N] = {
            'center': center_N,
            'width': width_N,
            'drift': drift,
            'drift_ratio': ratio,
            'verdict': verdict,
        }
        print(f"{N:<5} {center_N if center_N is not None else float('nan'):<12.4f} "
              f"{width_N:<10.4f} {drift:<15.4f} {ratio:<12.4f} {verdict:<10}")

    # 总裁决
    all_pass = all(v['drift_ratio'] < THRESHOLD_PASS for v in verdict_per_N.values() if v['center'] is not None)
    any_falsify = any(
        (v['center'] is None) or (v['drift_ratio'] > THRESHOLD_FALSIFY)
        for v in verdict_per_N.values()
    )

    if all_pass and not any(v['center'] is None for v in verdict_per_N.values()):
        final_verdict = 'P-CM-1 成立'
    elif any_falsify:
        final_verdict = 'P-CM-1 证伪'
    else:
        final_verdict = 'P-CM-1 部分成立(中间区)'

    print("\n" + "=" * 70)
    print(f"总裁决(最窄窗口判据): {final_verdict}")
    print("=" * 70)

    # ========== 对照分析: 最宽窗口(揭示窗口碎裂现象) ==========
    print("\n" + "=" * 70)
    print("对照分析: 最宽窗口(主导锁定区)漂移比")
    print("用途: 揭示 star 拓扑窗口碎裂现象(N=6 单窗口 → N≥8 多窗口)")
    print("=" * 70)
    print(f"基准: N=6, 最宽窗口 Δ_center = {results[6]['widest_center']:.4f}, 宽度 = {results[6]['widest_width']:.4f}")
    print(f"\n{'N':<5} {'窗口数':<8} {'最宽中心':<12} {'最宽宽度':<10} {'漂移比':<10} {'裁决':<10}")
    print("-" * 70)

    widest_verdict_per_N = {}
    base_wide_center = results[6]['widest_center']
    base_wide_width = results[6]['widest_width']
    for N in [8, 10, 12]:
        wc = results[N]['widest_center']
        ww = results[N]['widest_width']
        n_isl = results[N]['n_islands']
        if wc is None:
            ratio_w = float('inf')
            verdict_w = '无窗口'
        else:
            drift_w = abs(wc - base_wide_center)
            ratio_w = drift_w / base_wide_width if base_wide_width > 1e-15 else float('inf')
            if ratio_w < THRESHOLD_PASS:
                verdict_w = '成立(<0.2)'
            elif ratio_w > THRESHOLD_FALSIFY:
                verdict_w = '证伪(>0.5)'
            else:
                verdict_w = '中间区'
        widest_verdict_per_N[N] = {
            'widest_center': wc,
            'widest_width': ww,
            'n_islands': n_isl,
            'drift_ratio': ratio_w,
            'verdict': verdict_w,
        }
        print(f"{N:<5} {n_isl:<8} {wc if wc is not None else float('nan'):<12.4f} "
              f"{ww:<10.4f} {ratio_w:<10.4f} {verdict_w:<10}")

    # 窗口碎裂诊断
    n_islands_seq = [results[N]['n_islands'] for N in [6, 8, 10, 12]]
    fragmentation = n_islands_seq[0] == 1 and any(n > 1 for n in n_islands_seq[1:])
    print(f"\n窗口碎裂诊断: N=6→{n_islands_seq[0]}窗口, N=8→{n_islands_seq[1]}, "
          f"N=10→{n_islands_seq[2]}, N=12→{n_islands_seq[3]}")
    print(f"碎裂现象: {'是 — 单一窗口随尺寸增大碎裂为多窗口' if fragmentation else '否'}")
    print("=" * 70)

    # 生成图表
    plot_pcm1_verification(results, verdict_per_N, df_specs)

    # 汇总输出 JSON
    summary = {
        'prediction': 'P-CM-1',
        'assertion': '|Δ_center(N) - Δ_center(N=6)| / IslandWidth(N=6) < 0.2',
        'threshold_pass': THRESHOLD_PASS,
        'threshold_falsify': THRESHOLD_FALSIFY,
        'baseline_N6': {
            'center': base_center,
            'width': base_width,
            'widest_center': results[6]['widest_center'],
            'widest_width': results[6]['widest_width'],
        },
        'per_N_results_narrowest': {
            str(N): {
                'center': v['center'],
                'width': v['width'],
                'drift': v['drift'],
                'drift_ratio': v['drift_ratio'],
                'verdict': v['verdict'],
                'n_islands': results[N]['n_islands'],
            } for N, v in verdict_per_N.items()
        },
        'per_N_results_widest': {
            str(N): {
                'widest_center': v['widest_center'],
                'widest_width': v['widest_width'],
                'n_islands': v['n_islands'],
                'drift_ratio': v['drift_ratio'],
                'verdict': v['verdict'],
            } for N, v in widest_verdict_per_N.items()
        },
        'fragmentation_diagnosis': {
            'n_islands_sequence': {'6': n_islands_seq[0], '8': n_islands_seq[1],
                                   '10': n_islands_seq[2], '12': n_islands_seq[3]},
            'fragmentation_detected': fragmentation,
            'interpretation': 'star 拓扑单一锁定窗口随尺寸增大碎裂为多窗口 — P-CM-1 拓扑不变性假设失效' if fragmentation else '无碎裂',
        },
        'final_verdict_narrowest': final_verdict,
        'final_verdict_interpretation': (
            'P-CM-1 证伪: 最窄窗口中心漂移随 N 单调发散(N=10,12 漂移比>0.5)。'
            '物理原因: star 拓扑的谱丛分支点结构随尺寸增大而复杂化,'
            '单一锁定窗口碎裂为多窗口,导致"窗口中心"失去拓扑不变性。'
            '这是 Paper XIV §5.7 推论 5.7(谱丛纤维化)的间接体现: '
            'star 中心节点的多叶结构在有限尺寸下产生尺寸依赖的分支点重组。'
        ),
    }

    def json_default(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, float) and np.isnan(obj):
            return None
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

    summary_path = os.path.join(OUTPUT_DIR, 'paper14_pcm1_verification.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, default=json_default)
    print(f"\n[汇总] {summary_path}")

    return summary


def plot_pcm1_verification(results, verdict_per_N, df_specs):
    """绘制 P-CM-1 验证图: (a) 窗口中心随 N 的漂移; (b) σ_res(Δ) 四尺寸叠加; (c) 窗口数碎裂"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))

    # (a) 窗口中心随 N 的漂移(最窄 + 最宽对照)
    ax = axes[0]
    Ns = [6, 8, 10, 12]
    centers_narrow = [results[N]['center'] if results[N]['center'] is not None else np.nan for N in Ns]
    widths_narrow = [results[N]['width'] for N in Ns]
    centers_wide = [results[N]['widest_center'] if results[N]['widest_center'] is not None else np.nan for N in Ns]
    widths_wide = [results[N]['widest_width'] for N in Ns]

    half_narrow = [w / 2.0 if w > 0 else 0 for w in widths_narrow]
    half_wide = [w / 2.0 if w > 0 else 0 for w in widths_wide]

    ax.errorbar(Ns, centers_narrow, yerr=half_narrow, fmt='o-', color='red',
                ecolor='orange', elinewidth=2, capsize=6, markersize=8,
                label='最窄窗口(主判据)')
    ax.errorbar([n + 0.15 for n in Ns], centers_wide, yerr=half_wide, fmt='s--', color='purple',
                ecolor='violet', elinewidth=1.5, capsize=5, markersize=7,
                label='最宽窗口(对照)')

    base_center = centers_narrow[0]
    ax.axhline(y=base_center, color='blue', linestyle='--', alpha=0.5,
               label=f'基准 $\\Delta_{{center}}$(N=6)={base_center:.3f}')

    base_width = widths_narrow[0]
    if base_width > 0:
        ax.axhspan(base_center - 0.2 * base_width,
                   base_center + 0.2 * base_width,
                   alpha=0.15, color='green', label='P-CM-1 容忍带 ($\\pm 0.2 W_6$)')
        ax.axhspan(base_center - 0.5 * base_width,
                   base_center + 0.5 * base_width,
                   alpha=0.08, color='red', label='证伪阈值 ($\\pm 0.5 W_6$)')

    ax.set_xlabel('系统尺寸 $N$')
    ax.set_ylabel('窗口中心 $\\Delta_{center}$')
    ax.set_title('(a) star 锁定窗口中心随 $N$ 漂移 (最窄+最宽对照)')
    ax.legend(fontsize=7, loc='best')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(Ns)

    # (b) σ_res(Δ) 四尺寸叠加(对数纵轴便于观察临界行为)
    ax = axes[1]
    colors = {6: 'blue', 8: 'green', 10: 'orange', 12: 'red'}
    for N in Ns:
        df_spec = df_specs[N]
        ax.semilogy(df_spec['delta'], df_spec['sigma_res'] + 1e-12,
                    color=colors[N], alpha=0.7, label=f'N={N}')
        if results[N]['center'] is not None:
            for isl in results[N]['islands']:
                ax.axvspan(isl['start'], isl['end'], alpha=0.12, color=colors[N])

    ax.set_xlabel('矛盾边强度 $\\Delta$')
    ax.set_ylabel('残余涨落 $\\sigma_{res}$ (对数)')
    ax.set_title('(b) star $\\sigma_{res}(\\Delta)$ 四尺寸叠加 (彩色带=锁定窗口)')
    ax.legend(fontsize=8, loc='best')
    ax.set_xlim(0, 3.0)
    ax.grid(True, alpha=0.3)

    # (c) 窗口数碎裂诊断
    ax = axes[2]
    n_isls = [results[N]['n_islands'] for N in Ns]
    bars = ax.bar(Ns, n_isls, color=[colors[N] for N in Ns], alpha=0.7, edgecolor='black')
    for bar, n in zip(bars, n_isls):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15,
                str(n), ha='center', fontsize=11, fontweight='bold')
    ax.set_xlabel('系统尺寸 $N$')
    ax.set_ylabel('锁定窗口数')
    ax.set_title('(c) star 窗口碎裂诊断 (N=6 单窗口 $\\to$ N=12 多窗口)')
    ax.set_xticks(Ns)
    ax.set_yticks(range(0, max(n_isls) + 2))
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    outpath = os.path.join(OUTPUT_DIR, 'paper14_pcm1_verification.png')
    plt.savefig(outpath, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"[图表] {outpath}")
    return outpath


if __name__ == "__main__":
    verify_pcm1()
