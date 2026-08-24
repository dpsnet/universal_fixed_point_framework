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
spectral_ch3cho_pyscf.py  v1.0 — 外部参考计算（非谱框架内部推导）
===================================================
⚠️ 重要声明：
  本脚本调用 PySCF 进行 HF + CIS 计算，本质上是 Schrödinger 方程的数值解，
  不是谱框架内部的谱流推导。它仅作为 Bun(Reac) 层的"实例假设替换"参考——
  即用更精确的外部 QC 方法替代 3-轨道 EHT 模型，但不涉及谱框架的
  结构定理（谱流方程、ℓ_corr 不变量、纤维化链等）。

目的: 与 3-轨道 EHT 模型 (6.4 eV) 和实验值 (4.1 eV) 对比
      框架内部分析请参见 Paper XXIII (spectral_flow_ch3cho_npi.md)
"""

import numpy as np

# ── CH3CHO 几何 (实验平衡构型) ──
# 单位: Angstrom
# 坐标系: C1=CH3, C2=CHO, O 在 C2
ch3cho_geom = """
C        0.00000    0.00000    0.00000
C        1.54000    0.00000    0.00000
O        2.06000    1.22000    0.00000
H       -0.38000    1.03000    0.00000
H       -0.38000   -0.52000    0.89000
H       -0.38000   -0.52000   -0.89000
H        2.00000   -0.92000    0.00000
"""

# ── 构建分子 ──
from pyscf import gto, scf, dft, tddft, lib

mol = gto.M(
    atom=ch3cho_geom,
    basis='sto-3g',
    verbose=4,
    symmetry=False,
)

print("=" * 72)
print("CH3CHO ab initio (HF/STO-3G) 计算结果")
print("=" * 72)
print(f"\n分子几何:\n{ch3cho_geom}")
print(f"原子数: {mol.natm}")
print(f"电子数: {mol.nelectron}")
print(f"基函数数: {mol.nao}")

# ── RHF 计算 ──
print("\n\n>>> 1. RHF/STO-3G 基态计算 <<<")
print("-" * 50)
mf = scf.RHF(mol)
mf.kernel()
hf_energy = mf.e_tot

print(f"\n基态总能量 E_HF = {hf_energy:.8f} Hartree = {hf_energy * 27.2114:.4f} eV")

# 轨道能级
mo_energy = mf.mo_energy
n_occ = mol.nelectron // 2
print(f"\nHOMO 能量: {mo_energy[n_occ - 1]:.6f} Hartree = {mo_energy[n_occ - 1] * 27.2114:.4f} eV")
print(f"LUMO 能量: {mo_energy[n_occ]:.6f} Hartree = {mo_energy[n_occ] * 27.2114:.4f} eV")
print(f"HOMO-LUMO 间隙: {(mo_energy[n_occ] - mo_energy[n_occ - 1]) * 27.2114:.4f} eV")

# ── CIS/TDHF 激发态计算 ──
print("\n\n>>> 2. CIS (TDHF) 激发态计算 <<<")
print("-" * 50)

# TDHF (RPA) 计算 (包含 CIS + deexcitation)
n_states = 10
td = tddft.TDHF(mf)
td.nroots = n_states
td.kernel()

# 打印前 6 个激发态
print(f"\n前 {min(6, n_states)} 个激发态 (TDHF):")
print(f"{'态':>6} {'能量 (eV)':>12} {'波长 (nm)':>12} {'振子强度':>12} {'跃迁偶极':>12}")
print("-" * 56)
for i in range(min(6, n_states)):
    e_ev = td.e[i] * 27.2114
    wl_nm = 1239.84 / e_ev if e_ev > 0 else float('inf')
    f_osc = getattr(td, 'oscillator_strength', None)
    if f_osc is None:
        f_osc = getattr(td, 'f', [0.0]*n_states)
    f_val = f_osc[i] if hasattr(f_osc, '__getitem__') else 0.0
    print(f"{i + 1:>6} {e_ev:>12.4f} {wl_nm:>12.2f} {f_val:>12.6f}")

# ── DFT/TDDFT (B3LYP/STO-3G) ──
print("\n\n>>> 3. B3LYP/STO-3G 基态 <<<")
print("-" * 50)
mf_dft = dft.RKS(mol)
mf_dft.xc = 'b3lyp'
mf_dft.kernel()
dft_energy = mf_dft.e_tot
print(f"B3LYP 总能量: {dft_energy:.8f} Hartree = {dft_energy * 27.2114:.4f} eV")

mo_energy_dft = mf_dft.mo_energy
print(f"HOMO: {mo_energy_dft[n_occ - 1] * 27.2114:.4f} eV")
print(f"LUMO: {mo_energy_dft[n_occ] * 27.2114:.4f} eV")
print(f"HOMO-LUMO 间隙: {(mo_energy_dft[n_occ] - mo_energy_dft[n_occ - 1]) * 27.2114:.4f} eV")

# TDDFT
print("\n>>> 4. TD-B3LYP/STO-3G 激发态 <<<")
print("-" * 50)
td_dft = tddft.TDDFT(mf_dft)
td_dft.nroots = n_states
td_dft.kernel()

print(f"\n前 {min(6, n_states)} 个激发态 (TD-B3LYP):")
print(f"{'态':>6} {'能量 (eV)':>12} {'波长 (nm)':>12} {'振子强度':>12} {'跃迁偶极':>12}")
print("-" * 56)
for i in range(min(6, n_states)):
    e_ev = td_dft.e[i] * 27.2114
    wl_nm = 1239.84 / e_ev if e_ev > 0 else float('inf')
    f_osc_dft = getattr(td_dft, 'oscillator_strength', None)
    if f_osc_dft is None:
        f_osc_dft = getattr(td_dft, 'f', [0.0]*n_states)
    f_val_dft = f_osc_dft[i] if hasattr(f_osc_dft, '__getitem__') else 0.0
    print(f"{i + 1:>6} {e_ev:>12.4f} {wl_nm:>12.2f} {f_val_dft:>12.6f}")

# ── 识别 n→π* 跃迁 ──
print("\n\n>>> 5. n→π* 跃迁分析 <<<")
print("-" * 50)

# 对 CH3CHO, n→π* 是第一个激发态 (S1, 能量最低的激发态)
# 特征: 振子强度很弱 (~0.001 量级), 主要为 HOMO→LUMO

for label, td_obj, mf_obj in [("TDHF", td, mf), ("TD-B3LYP", td_dft, mf_dft)]:
    e0_ev = td_obj.e[0] * 27.2114
    # oscillator strength
    f_osc_td = getattr(td_obj, 'oscillator_strength', None)
    if callable(f_osc_td):
        f_osc_arr = f_osc_td()
    else:
        f_osc_arr = getattr(td_obj, 'f', None)
    f0 = f_osc_arr[0] if f_osc_arr is not None and hasattr(f_osc_arr, '__getitem__') else 0.0
    print(f"\n{label} S1 (n→π*):")
    print(f"  跃迁能: {e0_ev:.4f} eV = {e0_ev * 8065.54:.1f} cm^-1")
    print(f"  波长: {1239.84 / e0_ev:.2f} nm")
    print(f"  振子强度: {f0:.6f}")
    
    # NTO 分析 (仅在可用时)
    try:
        from pyscf.tdscf import tda as tda_mod
        # 跳过 NTO
        pass
    except:
        pass
    
    # 主要 MO 贡献
    print(f"  MO 贡献 (主要成分):")
    if hasattr(td_obj, 'xy') and td_obj.xy is not None:
        xy = td_obj.xy[0]
        x0 = np.asarray(xy[0]).ravel()
        y0 = np.asarray(xy[1]).ravel()
        # 打印前3个最重要的跃迁
        weights = x0**2 - y0**2
        top_idx = np.argsort(-np.abs(weights))[:3]
        for idx in top_idx:
            w = float(weights[idx])
            if abs(w) > 0.001:
                print(f"    跃迁 {idx}: 权重 = {w:.4f}")

# ── 大基组验证 (6-31G*) ──
print("\n\n>>> 6. 大基组验证 (HF/6-31G*) <<<")
print("-" * 50)
try:
    mol2 = gto.M(
        atom=ch3cho_geom,
        basis='6-31g*',
        verbose=0,
    )
    mf2 = scf.RHF(mol2)
    mf2.kernel()
    print(f"HF/6-31G* 总能量: {mf2.e_tot:.8f} Hartree")
    print(f"HF/6-31G* HOMO: {mf2.mo_energy[n_occ - 1] * 27.2114:.4f} eV")
    print(f"HF/6-31G* LUMO: {mf2.mo_energy[n_occ] * 27.2114:.4f} eV")
    print(f"HF/6-31G* 间隙: {(mf2.mo_energy[n_occ] - mf2.mo_energy[n_occ - 1]) * 27.2114:.4f} eV")
    
    td2 = tddft.TDHF(mf2)
    td2.nroots = n_states
    td2.kernel()
    f_osc2_fn = getattr(td2, 'oscillator_strength', None)
    if callable(f_osc2_fn):
        f_osc2_arr = f_osc2_fn()
    else:
        f_osc2_arr = getattr(td2, 'f', None)
    f2_val = f_osc2_arr[0] if f_osc2_arr is not None and hasattr(f_osc2_arr, '__getitem__') else 0.0
    print(f"TDHF/6-31G* S1: {td2.e[0] * 27.2114:.4f} eV (f = {f2_val:.6f})")
except Exception as e:
    print(f"6-31G* 计算跳过: {e}")

# ── 总结 ──
print("\n" + "=" * 72)
print("总  结")
print("=" * 72)

s1_hf = td.e[0] * 27.2114 if hasattr(td, 'e') and len(td.e) > 0 else float('nan')
s1_dft = td_dft.e[0] * 27.2114 if hasattr(td_dft, 'e') and len(td_dft.e) > 0 else float('nan')

print(f"\nCH3CHO n→π* 跃迁能:")
print(f"  HF/STO-3G + TDHF:   {s1_hf:.4f} eV")
print(f"  B3LYP/STO-3G + TD:  {s1_dft:.4f} eV")
print(f"  实验值 (气相):       4.1 eV")
print(f"  3-轨道 EHT 模型:     6.4 eV (偏差最大)")
print(f"\n偏差分析:")
print(f"  HF/STO-3G vs 实验:  {abs(s1_hf - 4.1):.1f} eV ({abs(s1_hf - 4.1)/4.1*100:.1f}%)")
print(f"  B3LYP/STO-3G vs 实验: {abs(s1_dft - 4.1):.1f} eV ({abs(s1_dft - 4.1)/4.1*100:.1f}%)")
print(f"  3-轨道 EHT vs 实验:  {abs(6.4 - 4.1):.1f} eV ({abs(6.4 - 4.1)/4.1*100:.1f}%)")
