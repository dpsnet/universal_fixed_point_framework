"""
Paper XIV 同域谱框架独立分析脚本
将 EDRN 稳定岛原始数据翻译为 UFPF 凝聚态谱表述(Paper XIV)的谱量,
计算谱流方程在边界扰动(矛盾边强度 Δ)下的响应。

理论锚点:
  - Paper XIV: 凝聚态物理的谱表述(谱间隙=序参量, 谱流方程=动力学)
  - 谱临界统一框架: ∂Rec_D 谱边界 + 量子相变临界慢化

数据来源(李广好 EDRN 项目, Apache-2.0):
  - 稳定岛 CSV: 4 拓扑 × 1501 点 (delta, gap, coarse, fine)
  - 追踪光因子 CSV: 1501 点 (delta, gap, coarse, fine)

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

# 中文字体设置(防止中文乱码)
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'

# =============================================================================
# 路径配置
# =============================================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, '稳定岛：神秘的新世界')
OUTPUT_DIR = os.path.join(BASE_DIR, 'analysis')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 4 拓扑数据路径
TOPOLOGY_FILES = {
    'chain': os.path.join(DATA_DIR, '寻找稳定岛超密集测试3', 'stable_island_chain.csv'),
    'star': os.path.join(DATA_DIR, '寻找稳定岛超密集测试3', 'stable_island_star.csv'),
    'ring': os.path.join(DATA_DIR, '寻找稳定岛超密集测试3', 'stable_island_ring.csv'),
    'small_world': os.path.join(DATA_DIR, '寻找稳定岛超密集测试3', 'stable_island_small_world.csv'),
}

# 追踪光因子数据路径
COSMIC_FILE = os.path.join(DATA_DIR, '追踪光因子1', 'cosmic_invariant_superdense_results.csv')


# =============================================================================
# 1. 数据加载
# =============================================================================
def load_csv(filepath):
    """加载 EDRN 原始 CSV 数据"""
    df = pd.read_csv(filepath, comment='#', header=None, names=['delta', 'gap', 'coarse', 'fine'])
    return df


def load_all_topologies():
    """加载全部 4 拓扑数据"""
    data = {}
    for topo, path in TOPOLOGY_FILES.items():
        if os.path.exists(path):
            data[topo] = load_csv(path)
            print(f"  [加载] {topo}: {len(data[topo])} 点, Δ∈[{data[topo]['delta'].min():.3f}, {data[topo]['delta'].max():.3f}]")
        else:
            print(f"  [缺失] {topo}: {path}")
    return data


# =============================================================================
# 2. Paper XIV 谱量翻译
# =============================================================================
"""
Paper XIV 核心对应:
  - 能隙 gap → 谱间隙 δ = min σ_+(A)
  - Fine(自旋关联涨落) → 谱生成元残余涨落 σ_residual(A)
  - Coarse(粗粒化磁化) → 谱投影的宏观期望值 ⟨P(A)⟩
  - 矛盾边强度 Δ → ∂Rec_D 谱边界扰动参数

谱临界统一框架:
  - 稳定岛(Fine 极小且平坦) → 谱间隙锁定窗口
  - 稳定岛外(Fine 飙升) → 谱间隙坍缩 Δλ_min → 0 (量子相变临界)
"""


def translate_to_spectral(df):
    """
    将 EDRN 原始诊断量翻译为 Paper XIV 谱量

    翻译规则(Paper XIV 命题 2.1 直接应用):
      gap(Δ)        → δ_sc(Δ)     : 谱间隙 = 能隙
      fine(Δ)       → σ_res(Δ)    : 谱生成元残余涨落
      coarse(Δ)     → ⟨P⟩(Δ)      : 谱投影宏观期望值

    附加计算:
      δ_sc × σ_res  → P(Δ)        : 谱间隙-涨落乘积(Paper XIV §5.6 类比)
      σ_res / δ_sc  → χ_spec(Δ)   : 谱磁化率(类比 BCS 磁化率)
    """
    result = df.copy()
    result.rename(columns={
        'gap': 'delta_spec',       # 谱间隙 δ_sc
        'fine': 'sigma_res',       # 谱生成元残余涨落
        'coarse': 'proj_macro',    # 谱投影宏观期望值
    }, inplace=True)

    # 谱间隙-涨落乘积(Paper XIV §5.6 预言的格点版本)
    result['P_spec'] = result['delta_spec'] * result['sigma_res']

    # 谱磁化率(类比 BCS 磁化率 χ = dM/dH ~ 1/δ)
    result['chi_spec'] = result['sigma_res'] / (result['delta_spec'] + 1e-15)

    # 谱间隙的相对变化率 d(δ)/dΔ(谱流方程的离散版本)
    result['d_delta_dDelta'] = np.gradient(result['delta_spec'].values, result['delta'].values)

    # 残余涨落的相对变化率 d(σ)/dΔ
    result['d_sigma_dDelta'] = np.gradient(result['sigma_res'].values, result['delta'].values)

    return result


# =============================================================================
# 3. 稳定岛的谱间隙锁定检测
# =============================================================================
def detect_spectral_gap_locking(df_spec, window=10, threshold=0.1):
    """
    检测谱间隙锁定窗口(稳定岛的 Paper XIV 翻译)

    判据(Paper XIV §2.2 + 谱临界统一框架):
      - 谱生成元残余涨落 σ_res 的局部标准差 / 全局标准差 < threshold
      - 等价于:谱间隙被锁定,系统远离量子相变临界点

    这与 EDRN 原生算法(stable_island_geometry.py find_stable_islands)共享同一阈值
    (stability_threshold = 0.1),但在 Paper XIV 框架中获得了不同的物理诠释:
      EDRN:  "沉默失谐极小化窗口"
      UFPF:  "谱间隙锁定窗口(量子相变临界慢化的逆过程)"
    """
    delta = df_spec['delta'].values
    sigma_res = df_spec['sigma_res'].values
    global_std = np.std(sigma_res)

    islands = []
    in_island = False
    island_start = 0

    for i in range(1, len(delta)):
        ws = max(0, i - window // 2)
        we = min(len(delta), i + window // 2)
        local_std = np.std(sigma_res[ws:we])
        local_ratio = local_std / global_std if global_std > 1e-15 else 1.0

        if local_ratio < threshold and not in_island:
            in_island = True
            island_start = delta[i]
        elif local_ratio >= threshold and in_island:
            in_island = False
            island_end = delta[i]
            width = island_end - island_start
            if width >= 0.02:
                mask = (delta >= island_start) & (delta <= island_end)
                island_sigma = sigma_res[mask]
                island_delta = df_spec['delta_spec'].values[mask]
                islands.append({
                    'start': island_start,
                    'end': island_end,
                    'width': width,
                    'sigma_res_mean': np.mean(island_sigma),
                    'sigma_res_std': np.std(island_sigma),
                    'delta_spec_mean': np.mean(island_delta),
                    'delta_spec_min': np.min(island_delta),
                    'delta_spec_max': np.max(island_delta),
                    'spec_gap_variation': (np.max(island_delta) - np.min(island_delta)) / (np.mean(island_delta) + 1e-15),
                })

    if in_island:
        island_end = delta[-1]
        width = island_end - island_start
        if width >= 0.02:
            mask = (delta >= island_start) & (delta <= island_end)
            island_sigma = sigma_res[mask]
            island_delta = df_spec['delta_spec'].values[mask]
            islands.append({
                'start': island_start,
                'end': island_end,
                'width': width,
                'sigma_res_mean': np.mean(island_sigma),
                'sigma_res_std': np.std(island_sigma),
                'delta_spec_mean': np.mean(island_delta),
                'delta_spec_min': np.min(island_delta),
                'delta_spec_max': np.max(island_delta),
                'spec_gap_variation': (np.max(island_delta) - np.min(island_delta)) / (np.mean(island_delta) + 1e-15),
            })

    return islands


# =============================================================================
# 4. ∂Rec_D 谱边界扰动分析
# =============================================================================
def analyze_boundary_perturbation(df_spec):
    """
    分析矛盾边强度 Δ 对谱间隙的扰动效应

    理论(Paper XIV §2.2 + 谱临界统一框架):
      - Δ = 0: 无边界扰动,谱间隙处于自然值
      - Δ 增大: 边界扰动增强,谱间隙被调制
      - 稳定岛内: 谱间隙锁定(不随 Δ 显著变化)
      - 稳定岛外: 谱间隙坍缩或剧烈变化(量子相变临界)

    输出:谱间隙 δ_sc(Δ) 的边界响应函数
    """
    delta = df_spec['delta'].values
    delta_spec = df_spec['delta_spec'].values
    sigma_res = df_spec['sigma_res'].values

    # 谱间隙的相对变化(归一化到 Δ=0 时的值)
    delta_spec_0 = delta_spec[0] if delta_spec[0] > 1e-15 else delta_spec[np.argmax(delta_spec > 1e-15)]
    relative_gap = delta_spec / (delta_spec_0 + 1e-15)

    # 残余涨落的相对变化
    sigma_0 = sigma_res[0] if sigma_res[0] > 1e-15 else np.mean(sigma_res[:10])
    relative_sigma = sigma_res / (sigma_0 + 1e-15)

    # 谱间隙压缩率(∂Rec_D 边界逼近指标)
    # 当 Δλ_min → 0 时,系统逼近量子相变临界点
    gap_compression = 1.0 - relative_gap

    return {
        'delta': delta,
        'relative_gap': relative_gap,
        'relative_sigma': relative_sigma,
        'gap_compression': gap_compression,
    }


# =============================================================================
# 5. 谱丛分支点分析(Paper XIV §5.7)
# =============================================================================
def analyze_spectral_sheaf_branching(df_spec, N=6):
    """
    Paper XIV §5.7: NRG Wilson 链三对角谱丛结构

    在 EDRN 稳定岛数据中,不同拓扑对应不同的谱丛纤维化实现:
      - chain:  一维三对角链(Wilson 链的标准实现)
      - star:   中心节点分支(谱丛的多叶结构)
      - ring:   周期性三对角链(边界条件修改)
      - small_world: 长程连接(谱丛的额外分支点)

    分析:计算等效谱丛分支点密度 ρ_b(ω) 的代理量
    """
    delta = df_spec['delta'].values
    sigma_res = df_spec['sigma_res'].values

    # 谱丛分支点的代理量:σ_res 的局部极大值
    # (Paper XIV §5.7:记忆函数 M(ω) 的虚部峰值 = 谱丛分支点)
    from scipy.signal import argrelextrema

    # 平滑后寻找局部极大值
    from scipy.ndimage import uniform_filter1d
    sigma_smooth = uniform_filter1d(sigma_res, size=20)
    local_max_idx = argrelextrema(sigma_smooth, np.greater, order=30)[0]

    # 筛选显著的极大值(高于均值的 1.5 倍)
    mean_sigma = np.mean(sigma_res)
    significant_max = [i for i in local_max_idx if sigma_smooth[i] > 1.5 * mean_sigma]

    branch_points = []
    for idx in significant_max:
        branch_points.append({
            'delta': delta[idx],
            'sigma_res': sigma_res[idx],
            'relative_height': sigma_res[idx] / mean_sigma,
        })

    return {
        'n_branch_points': len(branch_points),
        'branch_points': branch_points,
        'mean_branch_density': len(branch_points) / (delta[-1] - delta[0]) if len(branch_points) > 0 else 0,
    }


# =============================================================================
# 6. 量子相变临界指数分析(谱临界统一框架 主定理 F3)
# =============================================================================
def analyze_qpt_critical_exponent(df_spec, islands):
    """
    谱临界统一框架主定理 F3:
      量子相变临界慢化在 zν = 1/2 时与流变硬化精确同构
      τ ∝ |g - g_c|^{-zν}

    在稳定岛数据中:
      - 稳定岛边界 = 量子相变临界点 g_c 的代理
      - σ_res 在边界附近的发散 = 弛豫时间发散的代理
      - 拟合 σ_res ∝ |Δ - Δ_c|^{-α} 得到临界指数 α

    若 α ≈ 1/2,则与 zν = 1/2 的量子相变同构(so(1,1) Lie 代数)
    """
    delta = df_spec['delta'].values
    sigma_res = df_spec['sigma_res'].values

    results = []
    for island in islands:
        # 在稳定岛左边界附近拟合临界行为
        dc_left = island['start']
        dc_right = island['end']

        # 左边界:Δ < dc_left 的区域
        mask_left = (delta < dc_left) & (delta > dc_left - 0.3) & (sigma_res > 1e-6)
        if np.sum(mask_left) > 10:
            dist_left = dc_left - delta[mask_left]
            sigma_left = sigma_res[mask_left]
            # 拟合 log(σ) = -α log|Δ - Δ_c| + c
            log_dist = np.log(dist_left + 1e-10)
            log_sigma = np.log(sigma_left + 1e-10)
            # 线性回归
            valid = np.isfinite(log_dist) & np.isfinite(log_sigma)
            if np.sum(valid) > 5:
                coeffs = np.polyfit(log_dist[valid], log_sigma[valid], 1)
                alpha_left = -coeffs[0]
                results.append({
                    'boundary': 'left',
                    'delta_c': dc_left,
                    'alpha': alpha_left,
                    'n_points': np.sum(valid),
                })

        # 右边界:Δ > dc_right 的区域
        mask_right = (delta > dc_right) & (delta < dc_right + 0.3) & (sigma_res > 1e-6)
        if np.sum(mask_right) > 10:
            dist_right = delta[mask_right] - dc_right
            sigma_right = sigma_res[mask_right]
            log_dist = np.log(dist_right + 1e-10)
            log_sigma = np.log(sigma_right + 1e-10)
            valid = np.isfinite(log_dist) & np.isfinite(log_sigma)
            if np.sum(valid) > 5:
                coeffs = np.polyfit(log_dist[valid], log_sigma[valid], 1)
                alpha_right = -coeffs[0]
                results.append({
                    'boundary': 'right',
                    'delta_c': dc_right,
                    'alpha': alpha_right,
                    'n_points': np.sum(valid),
                })

    return results


# =============================================================================
# 7. SU(2) Casimir 谱隙比检验(Paper XIV 预言 6.1)
# =============================================================================
def check_casimir_gap_ratio(data_spec):
    """
    Paper XIV 预言 6.1:
      多带超导体中,n 个配对通道的谱隙 δ_n 之比:
        δ_n / δ_1 = sqrt(n(n+1)) / sqrt(2), n = 1,2,...,8

    在 EDRN 稳定岛数据中:
      - 不同拓扑(chain/star/ring/small_world)的稳定岛内谱间隙
        可类比为不同"配对通道"的谱隙
      - 检验它们的比值是否符合 SU(2) Casimir 量化

    注意:这是一个弱检验——自旋链不是多带超导体,
          但如果谱隙比接近 Casimir 序列,则提示存在深层谱结构
    """
    casimir_ratios = {}
    delta_spec_values = {}

    for topo, df_spec in data_spec.items():
        islands = detect_spectral_gap_locking(df_spec)
        if islands:
            # 取最窄(最稳定)的岛
            narrowest = min(islands, key=lambda x: x['width'])
            delta_spec_values[topo] = narrowest['delta_spec_mean']

    # 按 δ_spec 排序
    sorted_topos = sorted(delta_spec_values.keys(), key=lambda t: delta_spec_values[t])
    if len(sorted_topos) >= 2:
        base = delta_spec_values[sorted_topos[0]]
        for i, topo in enumerate(sorted_topos):
            n = i + 1
            casimir_pred = np.sqrt(n * (n + 1)) / np.sqrt(2)
            actual_ratio = delta_spec_values[topo] / base
            casimir_ratios[topo] = {
                'n': n,
                'delta_spec': delta_spec_values[topo],
                'actual_ratio': actual_ratio,
                'casimir_predicted': casimir_pred,
                'deviation_pct': (actual_ratio - casimir_pred) / casimir_pred * 100,
            }

    return casimir_ratios


# =============================================================================
# 8. 可视化
# =============================================================================
def plot_spectral_translation(data_spec, output_dir):
    """绘制谱量翻译对照图"""

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    colors = {'chain': 'blue', 'star': 'red', 'ring': 'green', 'small_world': 'purple'}

    # 8.1 谱间隙 δ_sc(Δ) vs 原始 gap(Δ)
    ax = axes[0, 0]
    for topo, df in data_spec.items():
        ax.plot(df['delta'], df['delta_spec'], label=f'{topo}', color=colors.get(topo, 'gray'), alpha=0.8)
    ax.set_xlabel('矛盾边强度 $\\Delta$')
    ax.set_ylabel('谱间隙 $\\delta_{sc}$ (= gap)')
    ax.set_title('(a) 谱间隙 $\\delta_{sc}(\\Delta)$ — Paper XIV 命题 2.1')
    ax.legend()
    ax.set_xlim(0, 3.0)
    ax.grid(True, alpha=0.3)

    # 8.2 谱生成元残余涨落 σ_res(Δ) vs 原始 Fine(Δ)
    ax = axes[0, 1]
    for topo, df in data_spec.items():
        ax.plot(df['delta'], df['sigma_res'], label=f'{topo}', color=colors.get(topo, 'gray'), alpha=0.8)
    ax.set_xlabel('矛盾边强度 $\\Delta$')
    ax.set_ylabel('残余涨落 $\\sigma_{res}$ (= Fine)')
    ax.set_title('(b) 谱生成元残余涨落 $\\sigma_{res}(\\Delta)$')
    ax.legend()
    ax.set_xlim(0, 3.0)
    ax.grid(True, alpha=0.3)

    # 8.3 谱间隙-涨落乘积 P(Δ) = δ × σ
    ax = axes[1, 0]
    for topo, df in data_spec.items():
        ax.plot(df['delta'], df['P_spec'], label=f'{topo}', color=colors.get(topo, 'gray'), alpha=0.8)
    ax.set_xlabel('矛盾边强度 $\\Delta$')
    ax.set_ylabel('$P = \\delta_{sc} \\times \\sigma_{res}$')
    ax.set_title('(c) 谱间隙-涨落乘积 $P(\\Delta)$ — P-CM-2 目标量')
    ax.legend()
    ax.set_xlim(0, 3.0)
    ax.grid(True, alpha=0.3)

    # 8.4 谱间隙压缩率(∂Rec_D 边界逼近指标)
    ax = axes[1, 1]
    for topo, df in data_spec.items():
        bp = analyze_boundary_perturbation(df)
        ax.plot(bp['delta'], bp['gap_compression'], label=f'{topo}', color=colors.get(topo, 'gray'), alpha=0.8)
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    ax.set_xlabel('矛盾边强度 $\\Delta$')
    ax.set_ylabel('谱间隙压缩率 $1 - \\delta/\\delta_0$')
    ax.set_title('(d) $\\partial\\mathbf{Rec}_D$ 谱边界逼近指标')
    ax.legend()
    ax.set_xlim(0, 3.0)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    outpath = os.path.join(output_dir, 'paper14_spectral_translation.png')
    plt.savefig(outpath, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"  [图表] {outpath}")
    return outpath


def plot_island_detection(data_spec, output_dir):
    """绘制稳定岛(谱间隙锁定窗口)检测图"""

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    colors = {'chain': 'blue', 'star': 'red', 'ring': 'green', 'small_world': 'purple'}

    for idx, (topo, df) in enumerate(data_spec.items()):
        ax = axes[idx // 2, idx % 2]
        sigma_res = df['sigma_res'].values
        delta = df['delta'].values
        global_std = np.std(sigma_res)

        # 滑动窗口局部标准差比
        from scipy.ndimage import uniform_filter1d
        local_std = uniform_filter1d(sigma_res, size=10, mode='nearest')
        for i in range(len(local_std)):
            ws = max(0, i - 5)
            we = min(len(sigma_res), i + 5)
            local_std[i] = np.std(sigma_res[ws:we])
        local_ratio = local_std / (global_std + 1e-15)

        ax.plot(delta, local_ratio, color=colors.get(topo, 'gray'), alpha=0.8, label=f'{topo} 局部涨落比')
        ax.axhline(y=0.1, color='red', linestyle='--', alpha=0.5, label='锁定阈值 $\\theta$=0.1')

        # 标记稳定岛
        islands = detect_spectral_gap_locking(df)
        for island in islands:
            ax.axvspan(island['start'], island['end'], alpha=0.2, color='yellow', label=f'谱间隙锁定窗口 (宽={island["width"]:.3f})')

        ax.set_xlabel('矛盾边强度 $\\Delta$')
        ax.set_ylabel('$\\sigma_{res}^{local} / \\sigma_{res}^{global}$')
        ax.set_title(f'({chr(97+idx)}) {topo} — 谱间隙锁定窗口检测')
        ax.legend(fontsize=8)
        ax.set_xlim(0, 3.0)
        ax.set_ylim(-0.1, 2.0)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    outpath = os.path.join(output_dir, 'paper14_island_detection.png')
    plt.savefig(outpath, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"  [图表] {outpath}")
    return outpath


def plot_qpt_critical_fit(data_spec, output_dir):
    """绘制量子相变临界指数拟合图"""

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    colors = {'chain': 'blue', 'star': 'red', 'ring': 'green', 'small_world': 'purple'}

    for idx, (topo, df) in enumerate(data_spec.items()):
        ax = axes[idx // 2, idx % 2]
        delta = df['delta'].values
        sigma_res = df['sigma_res'].values
        islands = detect_spectral_gap_locking(df)

        ax.plot(delta, sigma_res, color=colors.get(topo, 'gray'), alpha=0.6, label='$\\sigma_{res}(\\Delta)$')

        # 拟合临界指数
        qpt_results = analyze_qpt_critical_exponent(df, islands)
        for qpt in qpt_results:
            dc = qpt['delta_c']
            alpha = qpt['alpha']
            ax.axvline(x=dc, color='red', linestyle='--', alpha=0.5)
            ax.text(dc + 0.02, np.max(sigma_res) * 0.8,
                    f'$\\Delta_c$={dc:.2f}\n$\\alpha$={alpha:.3f}',
                    fontsize=8, color='red')

        ax.set_xlabel('矛盾边强度 $\\Delta$')
        ax.set_ylabel('残余涨落 $\\sigma_{res}$')
        ax.set_title(f'({chr(97+idx)}) {topo} — 量子相变临界指数拟合')
        ax.legend(fontsize=8)
        ax.set_xlim(0, 3.0)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    outpath = os.path.join(output_dir, 'paper14_qpt_critical_fit.png')
    plt.savefig(outpath, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"  [图表] {outpath}")
    return outpath


# =============================================================================
# 9. 主程序
# =============================================================================
def main():
    print("=" * 70)
    print("Paper XIV 同域谱框架独立分析")
    print("基于 EDRN 稳定岛原始数据(李广好, Apache-2.0)")
    print("UFPF 凝聚态谱表述(Paper XIV) + 谱临界统一框架")
    print("=" * 70)

    # 加载数据
    print("\n[1] 加载 EDRN 原始数据...")
    data = load_all_topologies()

    # 谱量翻译
    print("\n[2] Paper XIV 谱量翻译...")
    data_spec = {}
    for topo, df in data.items():
        data_spec[topo] = translate_to_spectral(df)
        print(f"  [翻译] {topo}: δ_sc∈[{data_spec[topo]['delta_spec'].min():.6f}, {data_spec[topo]['delta_spec'].max():.6f}]")

    # 稳定岛检测
    print("\n[3] 谱间隙锁定窗口(稳定岛)检测...")
    all_islands = {}
    for topo, df in data_spec.items():
        islands = detect_spectral_gap_locking(df)
        all_islands[topo] = islands
        print(f"  [{topo}] 检测到 {len(islands)} 个锁定窗口:")
        for i, isl in enumerate(islands):
            print(f"    窗口{i+1}: Δ∈[{isl['start']:.3f}, {isl['end']:.3f}], "
                  f"宽度={isl['width']:.3f}, "
                  f"σ_res均值={isl['sigma_res_mean']:.6f}, "
                  f"δ_sc均值={isl['delta_spec_mean']:.6f}, "
                  f"δ_sc变化率={isl['spec_gap_variation']:.4f}")

    # ∂Rec_D 边界扰动分析
    print("\n[4] ∂Rec_D 谱边界扰动分析...")
    for topo, df in data_spec.items():
        bp = analyze_boundary_perturbation(df)
        print(f"  [{topo}] 谱间隙压缩率范围: [{bp['gap_compression'].min():.4f}, {bp['gap_compression'].max():.4f}]")

    # 谱丛分支点分析
    print("\n[5] 谱丛分支点分析(Paper XIV §5.7)...")
    for topo, df in data_spec.items():
        sheaf = analyze_spectral_sheaf_branching(df)
        print(f"  [{topo}] 分支点数: {sheaf['n_branch_points']}, "
              f"平均密度: {sheaf['mean_branch_density']:.4f}/Δ")

    # 量子相变临界指数
    print("\n[6] 量子相变临界指数分析(谱临界统一框架 F3)...")
    all_qpt = {}
    for topo, df in data_spec.items():
        qpt = analyze_qpt_critical_exponent(df, all_islands[topo])
        all_qpt[topo] = qpt
        print(f"  [{topo}] 临界指数拟合:")
        for q in qpt:
            print(f"    {q['boundary']}边界: Δ_c={q['delta_c']:.3f}, α={q['alpha']:.4f}, 点数={q['n_points']}")

    # SU(2) Casimir 谱隙比检验
    print("\n[7] SU(2) Casimir 谱隙比检验(Paper XIV 预言 6.1)...")
    casimir = check_casimir_gap_ratio(data_spec)
    print(f"  Casimir 谱隙比:")
    print(f"  {'拓扑':<15} {'n':<5} {'δ_sc':<15} {'实际比值':<15} {'Casimir预测':<15} {'偏差%':<10}")
    for topo, info in casimir.items():
        print(f"  {topo:<15} {info['n']:<5} {info['delta_spec']:<15.6f} {info['actual_ratio']:<15.4f} {info['casimir_predicted']:<15.4f} {info['deviation_pct']:<10.2f}")

    # 可视化
    print("\n[8] 生成图表...")
    plot1 = plot_spectral_translation(data_spec, OUTPUT_DIR)
    plot2 = plot_island_detection(data_spec, OUTPUT_DIR)
    plot3 = plot_qpt_critical_fit(data_spec, OUTPUT_DIR)

    # 汇总输出
    print("\n[9] 汇总...")
    summary = {
        'topologies': list(data_spec.keys()),
        'islands': {topo: [{'start': i['start'], 'end': i['end'], 'width': i['width'],
                            'sigma_res_mean': i['sigma_res_mean'], 'delta_spec_mean': i['delta_spec_mean'],
                            'spec_gap_variation': i['spec_gap_variation']}
                           for i in islands] for topo, islands in all_islands.items()},
        'qpt_critical_exponents': {topo: qpt for topo, qpt in all_qpt.items()},
        'casimir_ratios': casimir,
    }
    def json_default(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

    summary_path = os.path.join(OUTPUT_DIR, 'paper14_analysis_summary.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, default=json_default)
    print(f"  [汇总] {summary_path}")

    print("\n" + "=" * 70)
    print("分析完成。输出文件:")
    print(f"  图表: {plot1}")
    print(f"  图表: {plot2}")
    print(f"  图表: {plot3}")
    print(f"  汇总: {summary_path}")
    print("=" * 70)


if __name__ == "__main__":
    main()
