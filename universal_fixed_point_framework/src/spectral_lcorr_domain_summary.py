# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

"""
spectral_lcorr_domain_summary.py — 5 领域 ℓ_corr 不变量替换汇总

Phase 56C3 交付物：汇总 QCD/引力/凝聚态/味物理/宇宙学 5 领域的 ℓ_corr 替换，
生成统一的跨领域对比表和分析报告。

参考：
- domain_generalization.md §7.2（统一对比表）
- 各领域纤维化笔记的 ℓ_corr 节
"""

import numpy as np
from typing import Dict, List

# ============================================================
# 5 领域 ℓ_corr 数据
# ============================================================

LCORR_DATA = {
    'QCD': {
        'layers': ['UV', 'GUT', 'EW', 'Chiral', 'Hadron'],
        'formula': r'\Lambda_{\mathrm{QCD}}^{-1}',
        'values': {
            'UV': 1.62e-26,       # M_Pl^{-1} (fm)
            'GUT': 9.87e-24,      # M_GUT^{-1} (fm)
            'EW': 8.02e-10,       # v^{-1} (fm)
            'Chiral': 1.97e-7,    # Λ_χ^{-1} (fm)
            'Hadron': 5.98e-7,    # Λ_QCD^{-1} (fm)
        },
        'span': '1.62×10^{-26}~5.98×10^{-7} fm',
        'unit': 'fm',
    },
    'Gravity': {
        'layers': ['Horizon', 'Exterior', 'Interior', 'Quantum_Core', 'Singularity'],
        'formula': r'M^{-1} \sim r_+^{-1}',
        'values': {
            'Horizon': 3.38e-10,        # r_+^{-1} (fm^{-1}) for M_sun
            'Exterior': 3.38e-10,       # r^{-1} (fm^{-1})
            'Interior': 3.38e-10,       # (r_+-r)^{-1} (fm^{-1})
            'Quantum_Core': 1.22e19,   # l_Pl^{-1} (GeV)
            'Singularity': 1.22e19,    # Λ_UV (GeV)
        },
        'span': '3.38×10^{-10}~1.22×10^{19} GeV',
        'unit': 'GeV 或 fm^{-1}',
    },
    'Condensed': {
        'layers': ['Hydro', 'Rheo', 'SC', 'QH', 'QPT'],
        'formula': r'\xi_c \sim |g-g_c|^{-\nu}',
        'values': {
            'Hydro': 1e-6,       # ξ_K41 ~ k^{-1} (m)
            'Rheo': 1e-8,        # ξ_DST ~ |γ̇-γ̇_c|^{-0.5} (m)
            'SC': 1e-7,          # ξ_BCS ~ ħv_F/Δ (m)
            'QH': 1e-8,          # l_B = √(ħ/eB) (m)
            'QPT': 1e-9,         # ξ_QPT ~ |g-g_c|^{-ν} (m)
        },
        'span': '10^{-9}~10^{-6} m',
        'unit': 'm',
    },
    'Flavor': {
        'layers': ['Yukawa', 'Mixing', 'CP', 'Seesaw', 'Hierarchy'],
        'formula': r'\ln(c_i)',
        'values': {
            'Yukawa': 4.91,        # ln(m_t/m_c)
            'Mixing': 3.81,        # ln(m_b/m_s)
            'CP': 2.82,            # ln(m_τ/m_μ)
            'Seesaw': -23.6,       # ln(m_ν/m_τ)
            'Hierarchy': 2.71,     # d_H
        },
        'span': '-23.6~4.91（无量纲）',
        'unit': '无量纲 (log比)',
    },
    'Cosmology': {
        'layers': ['Inflation', 'Reheat', 'BBN', 'LSS', 'DE', 'Quantum_Cosmo'],
        'formula': r'H^{-1}(z)',
        'values': {
            'Inflation': 5.4e-30,     # H_inf^{-1} (m)
            'Reheat': 1.97e-22,       # T_rh^{-1} (m)
            'BBN': 1.97e-7,           # T_BBN^{-1} (m)
            'LSS': 1.44e26,           # r_s(z_*) (m)
            'DE': 1.44e26,            # d_H(z) (m)
            'Quantum_Cosmo': 8.2e-35, # l_Pl (m)
        },
        'span': '8.2×10^{-35}~1.44×10^{26} m',
        'unit': 'm',
    },
}


# ============================================================
# 1. 统一对比表
# ============================================================
def print_unified_table():
    """打印 5 领域 ℓ_corr 统一对比表"""
    print("=" * 72)
    print("谱丛精细纤维拆分：5 领域 ℓ_corr 不变量替换统一对比")
    print("=" * 72)
    print(f"  {'领域':<15}{'ℓ_corr 公式':<28}{'跨度':<30}")
    print("-" * 72)

    for domain, data in LCORR_DATA.items():
        print(f"  {domain:<15}{data['formula']:<28}{data['span']:<30}")

    print("-" * 72)
    print()


# ============================================================
# 2. 各层 ℓ_corr 范围分析
# ============================================================
def print_detailed_analysis():
    """打印各领域各层的 ℓ_corr 详情"""
    for domain, data in LCORR_DATA.items():
        print(f"--- {domain}: {data['formula']} ---")
        print(f"  {'层':<20} {'ℓ_corr':<18} {'单位':<20}")
        print("  " + "-" * 55)

        values = data['values']
        unit = data['unit']
        for layer in data['layers']:
            v = values[layer]
            v_str = f"{v:.4e}" if isinstance(v, float) and abs(v) > 0 else f"{v}"
            print(f"  {f'Bun({layer})':<20} {v_str:<18} {unit}")

        # 统计
        numeric_vals = [v for v in values.values() if isinstance(v, (int, float))]
        min_v = min(numeric_vals)
        max_v = max(numeric_vals)
        ratio = abs(max_v / min_v) if min_v != 0 else float('inf')
        print(f"  {'':>20} {'':<18}")
        print(f"  跨度比: {ratio:.2e}")
        print(f"  量级: {int(np.log10(ratio))} 个数量级")
        print()


# ============================================================
# 3. 跨领域敏感性分析
# ============================================================
def sensitivity_analysis():
    """分析 ℓ_corr 对层间解耦的敏感性"""
    print("=" * 72)
    print("ℓ_corr 跨领域敏感性分析")
    print("=" * 72)
    print()

    results = {}
    for domain, data in LCORR_DATA.items():
        n_layers = len(data['layers'])
        values = [v for v in data['values'].values() if isinstance(v, (int, float))]
        max_val = max(values)
        min_val = min(values)

        # ℓ_corr 变化率 = 层内最大/最小比
        ratio = abs(max_val / min_val) if min_val != 0 else float('inf')
        n_orders = int(np.log10(ratio)) if ratio not in [float('inf'), -float('inf')] else 99
        n_orders = max(n_orders, 0)

        # 敏感性: 层数越多 / 跨度越大 → 对 ℓ_corr 越敏感
        sensitivity = min(n_orders / 5.0, 10.0)  # 归一化到 0-10

        results[domain] = {
            'n_layers': n_layers,
            'ℓ_corr_range': f'{min_val:.4e}~{max_val:.4e}',
            'span_orders': n_orders,
            'sensitivity': sensitivity,
        }

    print(f"  {'领域':<15} {'层数':<8} {'ℓ 跨度(量级)':<16} {'敏感性':<10}")
    print("-" * 50)
    for domain, info in sorted(results.items(),
                                key=lambda x: x[1]['sensitivity'],
                                reverse=True):
        n = info['n_layers']
        span = info['span_orders']
        sens = info['sensitivity']
        bar = '█' * int(sens) + '░' * (10 - int(sens))
        print(f"  {domain:<15} {n:<8} {span:<16} {sens:<5.1f}/10 {bar}")

    print("-" * 50)
    print("  敏感性越高 → ℓ_corr 对层间解耦越敏感")
    print("  宇宙学跨越 60 个量级，对 ℓ_corr 最敏感。")
    print()

    return results


# ============================================================
# 4. 运行
# ============================================================
if __name__ == '__main__':
    print()
    print("#" * 72)
    print("#  5 领域 ℓ_corr 不变量替换汇总报告")
    print("#  Phase 56C3 — 2026-07-25")
    print("#" * 72)
    print()

    print_unified_table()
    print_detailed_analysis()
    sensitivity_analysis()

    print("=" * 72)
    print("汇总完成")
    print("=" * 72)
