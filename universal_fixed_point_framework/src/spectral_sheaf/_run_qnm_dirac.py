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

#!/usr/bin/env python3
"""
_run_qnm_dirac.py —— 用 qnm 包计算 Dirac QNM 基准值
"""

from qnm import angular, cached, radial
import numpy as np

# 先下载数据
from qnm.cached import download_data, get_cachedir
download_data()

print("=" * 70)
print("qnm Dirac s=-0.5 Schwarzschild a=0 基准值")
print("=" * 70)

# 方法 1：使用 KerrSpinSeq
print("\n方法 1: KerrSpinSeq")
for l_code in [1, 2, 3]:
    l_phys = l_code - 0.5
    try:
        ks = cached.KerrSpinSeq(s=-0.5, a=0.0, l_max=15)
        om = ks(l_code, 0, 0, real=True)
        print(f"  l={l_phys:.1f} (code={l_code}): ω = {om[0]:.10f} {om[1]:+.10f}i")
    except Exception as e:
        print(f"  l={l_phys:.1f}: {type(e).__name__}: {e}")

# 方法 2: 手动使用 radial 模块
print("\n方法 2: radial 模块连分数")

def compute_qnm_manual(s, a, l_code, m_code, n, M=1.0, max_iter=500):
    """手动计算 QNM，直接评估径向连分数。"""
    # 使用 qnm 的 ang 模块求解角向特征值
    from qnm.angular import sep_consts, M_matrix
    
    # 角向特征值
    c = a * 0.0  # a=0 时 σ=0
    # 对 a=0，λ = l(l+1) - s(s+1)
    lam = l_code * (l_code + 1) - s * (s + 1)
    
    # 径向连分数
    # 构建 radial 函数
    from qnm.radial import leaver_cf_trunc_inversion, D_coeffs
    
    # 计算 D 系数
    D = D_coeffs(s, a, lam, m_code, 0, omega_val=0.0)  # 初始猜测
    
    # 尝试在 Schwarzschild 极限下
    # 使用 qnm 的径向连分数
    # ...
    
    print(f"  l_code={l_code}, m={m_code}: λ={lam}")

compute_qnm_manual(-0.5, 0.0, 1, 0, 0)

print("\n" + "=" * 70)
print("参考值 (Dolan & Gair 2006)")
print("=" * 70)
for l, w in [(0.5, "0.378721-0.096458i"), (1.5, "0.522988-0.089964i"), (2.5, "0.640418-0.091694i")]:
    print(f"  l={l:.1f}: ω = {w}")
