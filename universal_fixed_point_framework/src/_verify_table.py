"""Verify the experimental comparison table data in the note."""
import iqhe_critical_tmm_validation as iqhe
import numpy as np

hbar_SI = 1.054571817e-34
e_SI = 1.602176634e-19

# All 16 samples: (name, mu, n, B, n_imp, mechanism)
samples = [
    ('#1 最纯 GaAs',      44e6, 2.0e11, 5,    3e7,    '背景杂质'),
    ('#2 GaAs flip-chip', 42e6, 1.5e11, 2,    3e7,    '背景杂质'),
    ('#3 超高迁移率 GaAs', 1e7,  2.0e11, 5,    2e11,   '远程施主'),
    ('#4 GaAs 高迁移率',   5e6,  3.0e11, 4,    3e11,   '远程施主'),
    ('#5 GaAs/AlGaAs 中', 1.5e6, 2.0e11, 2,   2e11,   '远程施主'),
    ('#6 GaAs Cu蔽前',    3e6,  1.5e11, 3,    1.5e11, '远程施主'),
    ('#7 GaAs Cu蔽后',    3e6,  1.5e11, 3,    1.5e11, '远程施主'),
    ('#8 GaAs/AlGaAs 标', 2e5,  5.0e11, 2,    5e11,   '远程施主'),
    ('#9 GaAs/AlGaAs 低', 1e5,  3.0e11, 1,    3e11,   '远程施主'),
    ('#10 InGaAs/InP PP', 1e4,  4.0e11, 0.5,  1e12,   '合金势'),
    ('#11 InGaAs/InP PI', 1e4,  2.0e11, 15.7, 1e12,   '合金势'),
    ('#12 GaAs LL1',      3e4,  2.0e11, 1.5,  1e12,   '远程施主'),
    ('#13 GaAs LL4',      3e4,  2.0e11, 1.5,  1e12,   '远程施主'),
    ('#14 数值模拟',      None, None,   None, None,   '数值'),
    ('#15 石墨烯 FQHE',   1e6,  2.0e12, 2,    1e9,    '背景杂质'),
    ('#16 石墨烯洁净',    1e6,  2.0e12, 2,    1e9,    '背景杂质'),
]

# Values from the CORRECTED note table
note_eps = [3.9e-4, 1.0e-4, 0.26, 0.49, 0.66, 0.33, 0.33, 1.65, 1.97,
            13.2, 0.42, 4.4, 4.4, None, 0.003, 0.003]
note_nus = [1.0002, 1.0001, 1.06, 1.12, 1.17, 1.08, 1.08, 1.42, 1.50,
            2.34, 1.10, 2.00, 2.00, 2.35, 1.001, 1.001]

print(f'{"样品":<22} | {"ε_代码":>8} | {"ν_代码":>8} | {"ε_笔记":>9} | {"ν_笔记":>8} | {"结果"}')
print('-' * 75)

mismatches = []
for i, (name, mu, n, B, n_imp, mech) in enumerate(samples):
    if i == 13:  # #14 数值模拟
        eps_code = float('inf')
        nu_code = 2.35
    else:
        lB2 = hbar_SI / (e_SI * B) * 1e4
        eps_code = n_imp * lB2
        nu_code = iqhe.nu_spec_interp(eps_code)

    eps_note = note_eps[i]
    nu_note = note_nus[i]

    diff = abs(nu_code - nu_note)
    if diff < 0.02:
        ok_str = '✅'
    elif diff < 0.05:
        ok_str = f'⚠差{diff:.3f}'
    else:
        ok_str = f'❌差{diff:.3f}'
        mismatches.append((i + 1, name, diff))

    eps_code_str = f'{eps_code:.4f}' if eps_code != float('inf') else '  ∞  '
    eps_note_str = f'{eps_note:.4f}' if eps_note is not None else '  —  '
    print(f'{name:<22} | {eps_code_str:>8} | {nu_code:8.4f} | {eps_note_str:>9} | {nu_note:>8} | {ok_str}')

print()
if mismatches:
    print(f'发现 {len(mismatches)} 处不匹配:')
    for idx, name, diff in mismatches:
        print(f'  #{idx} {name}: ν差异 = {diff:.3f}')
else:
    print('所有样品 ν_spec 值与代码计算一致 ✅')
