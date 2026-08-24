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
验证 spectral_BCS_weave.md §6.5 表格中的 Z_BCS 值和相干峰比
对比实际代码输出与笔记中的 AI 生成值
"""
import numpy as np

r_ref = 0.815
materials = {
    'Al': {'Tc': 1.2, 'wD': 428, 'EF': 1.36e5, 'mu*': 0.10, 'NdV': 0.167, 'lam': 0.4,
           'D0_meV': 0.18, 'Gamma_meV': 0.002},
    'Sn': {'Tc': 3.7, 'wD': 200, 'EF': 1.0e5,  'mu*': 0.11, 'NdV': 0.25,  'lam': 0.7,
           'D0_meV': 0.59, 'Gamma_meV': 0.008},
    'Pb': {'Tc': 7.2, 'wD': 105, 'EF': 1.1e5,  'mu*': 0.12, 'NdV': 0.353, 'lam': 1.55,
           'D0_meV': 1.50, 'Gamma_meV': 0.10},
    'Nb': {'Tc': 9.3, 'wD': 275, 'EF': 0.9e5,  'mu*': 0.13, 'NdV': 0.32,  'lam': 1.0,
           'D0_meV': 1.55, 'Gamma_meV': 0.05},  # Nb 展宽估计
}

print("=" * 72)
print("Z_BCS 和相干峰比 — 实际代码计算 vs 笔记表格对比")
print("=" * 72)
print()

# 实际代码计算 Z_BCS
print("━" * 72)
print("实际代码计算的 Z_BCS (spectral_BCS_v2_comprehensive.py Q2 代码)")
print("━" * 72)

for name, mat in materials.items():
    wD_over_EF = mat['wD'] * 0.08617e-3 / mat['EF']
    dZ_ret = 0.5 * wD_over_EF * np.log(1/wD_over_EF) if wD_over_EF > 0 else 0
    dZ_mu = mat['mu*'] / mat['NdV'] * np.sqrt(r_ref)
    Gi = (mat['Tc']/mat['EF'])**(4-3)
    dZ_fluc = Gi * np.sqrt(mat['Tc']/mat['EF'])
    Z = 1.0 + dZ_ret + dZ_mu + dZ_fluc
    
    print(f"  {name}:")
    print(f"    dZ_ret  = {dZ_ret:.4f} (延迟效应, wD/EF={wD_over_EF:.6f})")
    print(f"    dZ_mu   = {dZ_mu:.4f} (Coulomb 赝势)")
    print(f"    dZ_fluc = {dZ_fluc:.6f} (热涨落)")
    print(f"    Z_BCS   = {Z:.4f}")
    print()

print("━" * 72)
print("笔记表格中的 Z_BCS (AI 生成)")
print("━" * 72)
print("  Al=1.01, Sn=1.08, Pb=1.55, Nb=1.22")
print()

print("━" * 72)
print("公式自洽性检查: 相干峰比 = 1/sqrt(2*eta) / Z_BCS")
print("  其中 eta = Gamma / Delta_0")
print("━" * 72)

for name, mat in materials.items():
    eta = mat['Gamma_meV'] / mat['D0_meV']
    formula_ratio = 1.0 / np.sqrt(2 * eta)
    
    # 用笔记中的 AI 值
    ai_z = {'Al': 1.01, 'Sn': 1.08, 'Pb': 1.55, 'Nb': 1.22}[name]
    ai_peak = {'Al': 35, 'Sn': 25, 'Pb': 6, 'Nb': 12}[name]
    
    # 用实际代码值
    wD_over_EF = mat['wD'] * 0.08617e-3 / mat['EF']
    dZ_ret = 0.5 * wD_over_EF * np.log(1/wD_over_EF) if wD_over_EF > 0 else 0
    dZ_mu = mat['mu*'] / mat['NdV'] * np.sqrt(r_ref)
    Gi = (mat['Tc']/mat['EF'])**(4-3)
    dZ_fluc = Gi * np.sqrt(mat['Tc']/mat['EF'])
    actual_z = 1.0 + dZ_ret + dZ_mu + dZ_fluc
    
    ai_peak_from_formula = formula_ratio / ai_z
    actual_peak_from_formula = formula_ratio / actual_z
    
    print(f"  {name}: eta={eta:.4f}, 1/sqrt(2eta)={formula_ratio:.1f}")
    print(f"    笔记 AI 值: Z={ai_z}, 峰比={ai_peak}")
    print(f"      公式计算峰比={ai_peak_from_formula:.1f}  vs  笔记写={ai_peak}  {'✓ 自洽' if abs(ai_peak_from_formula - ai_peak) < 2 else '✗ 不自洽'}")
    print(f"    实际代码: Z={actual_z:.4f}")
    print(f"      公式计算峰比={actual_peak_from_formula:.1f}")
    print()

print("━" * 72)
print("结论")
print("━" * 72)
print()
print("  1. Z_BCS 值：笔记中 Al=1.01, Sn=1.08, Pb=1.55, Nb=1.22")
print("     实际代码输出：Al={:.4f}, Sn={:.4f}, Pb={:.4f}, Nb={:.4f}".format(
    *[1.0 + materials[m]['mu*']/materials[m]['NdV']*np.sqrt(r_ref) + 
      0.5 * (materials[m]['wD']*0.08617e-3/materials[m]['EF']) * np.log(1/max(materials[m]['wD']*0.08617e-3/materials[m]['EF'], 1e-30))
      + (materials[m]['Tc']/materials[m]['EF']) * np.sqrt(materials[m]['Tc']/materials[m]['EF'])
      for m in ['Al','Sn','Pb','Nb']]
))
print("     两者完全不同 → Z_BCS 是 AI 编造的")
print()
print("  2. 相干峰比：笔记用公式 1/√(2η)·1/Z 计算，但代入后")
print("     与笔记写值不一致（Al: 公式算≈7, 写~35）")
print("     → 连公式自洽性都未通过")
print()
print("  3. 处理建议：删除该表格，或用实际代码计算的值替换")
