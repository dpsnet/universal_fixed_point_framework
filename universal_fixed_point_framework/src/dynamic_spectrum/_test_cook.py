#!/usr/bin/env python3
"""验证 Leaver 乘积形式残差在参考 QNM 频率处的行为。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from leaver_unified_solver import LeaverUnifiedSolver, LeaverResidual

# QNM_REF_TABLE (Cook-Zalutskiy 2014 自洽值)
ref_table = {
    (0.0, 2, 0): complex(0.373672, -0.088962),
    (0.5, 2, 0): complex(0.383318, -0.087069),
    (0.5, 2, 2): complex(0.464123, -0.085639),
    (0.7, 2, 2): complex(0.532600, -0.080793),
    (0.9, 2, 2): complex(0.671614, -0.064869),
    (0.5, 2, 1): complex(0.420632, -0.086173),
}

# Berti 原始表 (Leaver 1985 系数)
berti_table = {
    (0.0, 2, 0): complex(0.373672, -0.088962),
    (0.5, 2, 0): complex(0.355051, -0.095299),
    (0.5, 2, 2): complex(0.524581, -0.088274),
    (0.7, 2, 2): complex(0.532144, -0.080721),
    (0.9, 2, 2): complex(0.584417, -0.087278),
}

print('验证 Leaver 乘积形式残差在参考 QNM 频率处的行为')
print('='*72)
print(f'  {"a":>4s} {"l,m":>6s} {"参考源":>10s} {"ω":>22s} {"|R(ω)|":>16s}')
print(f'  {"-"*60}')

for (a, l, m), omega_ref in ref_table.items():
    for label, table in [('Cook-Zal', ref_table), ('Berti', berti_table)]:
        if (a, l, m) in table or (a, l, m) in berti_table:
            w = table.get((a,l,m), omega_ref)
            r = LeaverResidual(M=1.0, a=a, s=-2)
            res = r.full_residual(w, l, m)
            src = label
            ok = '≈0 ✅' if abs(res) < 1e-6 else '❌'
            print(f'  {a:>4.1f}  l={l},m={m}  {src:>10s}  {w.real:.6f}{w.imag:+.6f}i  |R|={abs(res):.4e}  {ok}')

print()
print('Newton 收敛测试（从参考值出发）：')
for (a, l, m), omega_ref in ref_table.items():
    solver = LeaverUnifiedSolver(M=1.0, a=a, s=-2)
    w_start = omega_ref
    w_final, res = solver._newton_solve(w_start, l, m, max_iter=30)
    ref_type = 'Cook' if (a,l,m) in ref_table else 'Berti'
    if abs(w_final - omega_ref) < 0.001:
        print(f'  a={a:.1f},l={l},m={m}: {w_start.real:.6f}{w_start.imag:+.6f}i → {w_final.real:.6f}{w_final.imag:+.6f}i ✅ (保持不变)')
    else:
        print(f'  a={a:.1f},l={l},m={m}: {w_start.real:.6f}{w_start.imag:+.6f}i → {w_final.real:.6f}{w_final.imag:+.6f}i ❌ (漂移!)')
