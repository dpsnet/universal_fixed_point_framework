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
"""诊断：标准方法和两弦法的 Kerr 支持状态。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from leaver_unified_solver import LeaverUnifiedSolver

Berti = {
    (0.0,2,0): (0.373672, -0.088962),
    (0.5,2,0): (0.355051, -0.095299),
    (0.5,2,2): (0.524581, -0.088274),
    (0.7,2,2): (0.532144, -0.080721),
    (0.9,2,2): (0.584417, -0.087278),
}

def check(label, a, l, m, ref_re, ref_im):
    s_auto = LeaverUnifiedSolver(M=1.0, a=a, s=-2)
    r_auto = s_auto.solve(l=l, m=m, n=0, method='auto')
    w_auto = r_auto['omega']
    d_auto = abs(w_auto - complex(ref_re, ref_im))
    
    s_sf = LeaverUnifiedSolver(M=1.0, a=a, s=-2)
    r_sf = s_sf.solve(l=l, m=m, n=0, method='spectral_fast')
    w_sf = r_sf['omega']
    d_sf = abs(w_sf - complex(ref_re, ref_im))
    
    auto_ok = '✅' if d_auto < 0.03 else '❌'
    sf_ok = '✅' if d_sf < 0.03 else '❌'
    print(f'  {label:25s}:')
    print(f'    标准法: ω={w_auto.real:.6f}{w_auto.imag:+.6f}i  {auto_ok} (偏差={d_auto:.4f}, ρ={r_auto["residual"]:.2e})')
    print(f'    两弦法: ω={w_sf.real:.6f}{w_sf.imag:+.6f}i  {sf_ok} (偏差={d_sf:.4f}, ρ={r_sf["residual"]:.2e})')

print('Kerr 模式诊断')
print('='*60)
print('参考值来源: Berti (2006) 拟合表')
print('='*60)

check('Schwarz a=0, l=2,m=0', 0.0, 2, 0, *Berti[(0.0,2,0)])
check('Kerr a=0.5, l=2,m=0', 0.5, 2, 0, *Berti[(0.5,2,0)])
check('Kerr a=0.5, l=2,m=2', 0.5, 2, 2, *Berti[(0.5,2,2)])
check('Kerr a=0.7, l=2,m=2', 0.7, 2, 2, *Berti[(0.7,2,2)])
check('Kerr a=0.9, l=2,m=2', 0.9, 2, 2, *Berti[(0.9,2,2)])
