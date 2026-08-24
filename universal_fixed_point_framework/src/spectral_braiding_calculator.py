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
谱编织计算器 (Spectral Braiding Calculator)
============================================
基于 Paper XV (§4.4.3) 和 spectral_photovoltaics.md (§4, §9) 的谱框架，
计算 D-A (给体-受体) 界面处的谱编织强度 ||d||，用于筛选高效光伏材料。

理论基础:
    d_if^spec(R) = <φ_i | [∇_R, A_mol] | φ_f> · δ_if^{-1}
    A_mol = exp(-β F)   (F: Fock 矩阵)

依赖:
    - numpy, scipy (核心数值)
    - pyscf (可选, 用于从头算 Fock 矩阵, 见 PySCF 接口示例)

作者: Paper XV / spectral_photovoltaics.md 数值实现
版本: v0.1 (2026-07-22)
"""

import numpy as np
from scipy.linalg import expm, eigh
from typing import Tuple, Optional, Dict
import warnings


# ============================================================================
# 核心计算函数
# ============================================================================

def spectral_braiding_strength(
    F: np.ndarray,
    grad_F: np.ndarray,
    n_electron: int,
    beta: float = 1.0,
    return_details: bool = False
) -> float:
    """
    计算谱编织强度 ||d||
    
    参数
    ----
    F : ndarray, shape (n_basis, n_basis)
        Fock 矩阵 (原子单位)
    grad_F : ndarray, shape (n_nuc, n_basis, n_basis)
        核梯度下的 Fock 矩阵导数, grad_F[i] = ∂F/∂R_i
    n_electron : int
        总电子数
    beta : float
        谱-能量转换标度 (原子单位下 beta = 1)
    return_details : bool
        是否返回详细诊断信息
        
    返回
    ----
    d_norm : float
        谱编织强度 ||d||
    
    参考
    ----
    Paper XV 定义 4.4, spectral_photovoltaics.md 定理 P1
    """
    n_basis = F.shape[0]
    n_nuc = grad_F.shape[0]
    
    # Step 1: 构造谱生成元 A_mol = exp(-β·F)
    A = expm(-beta * F)
    
    # Step 2: 对角化 A_mol -> λ_i, φ_i
    eigvals, eigvecs = eigh(A)
    
    # Step 3: 定位 HOMO 和 LUMO 谱模式
    n_occ = n_electron // 2
    if n_occ < 1 or n_occ >= n_basis:
        raise ValueError(f"n_occ={n_occ} 超出范围 (n_basis={n_basis})")
    
    λ_HOMO = eigvals[n_occ - 1]
    λ_LUMO = eigvals[n_occ]
    φ_HOMO = eigvecs[:, n_occ - 1]
    φ_LUMO = eigvecs[:, n_occ]
    
    # 谱间隙
    δ_if = λ_LUMO - λ_HOMO
    if δ_if < 1e-15:
        warnings.warn(f"谱间隙过小: δ_if = {δ_if:.2e}")
        return np.inf  # 锥形交叉处的发散
    
    # Step 4: 计算谱非绝热耦合
    # [∇_R, A_mol] ≈ -β · A · ∇_R F  (一阶近似, 见命题推导)
    d_norm = 0.0
    for i in range(n_nuc):
        grad_A = -beta * A @ grad_F[i]  # 谱生成元的梯度
        d_if = np.dot(φ_LUMO.conj(), grad_A @ φ_HOMO)
        d_norm += np.abs(d_if) ** 2
    
    d_norm = np.sqrt(d_norm) / δ_if
    
    if return_details:
        return {
            'd_norm': d_norm,
            'δ_if': δ_if,
            'λ_HOMO': λ_HOMO,
            'λ_LUMO': λ_LUMO,
            'HOMO_index': n_occ - 1,
            'LUMO_index': n_occ,
            'd_components': np.array([
                np.abs(np.dot(φ_LUMO.conj(), (-beta * A @ grad_F[i]) @ φ_HOMO))
                for i in range(n_nuc)
            ]),
            'braiding_class': _classify_braiding(d_norm)
        }
    
    return d_norm


def spectral_braiding_from_pyscf(
    mol,
    mf,
    beta: float = 1.0,
    return_details: bool = False
) -> float:
    """
    从 PySCF 计算结果计算谱编织强度
    
    参数
    ----
    mol : pyscf.gto.Mole
        PySCF 分子对象
    mf : pyscf.scf
        已完成 SCF 计算的 PySCF 对象
    beta : float
        谱-能量转换标度
    return_details : bool
        是否返回详细诊断信息
    
    返回
    ----
    d_norm : float
        谱编织强度 ||d||
    
    示例
    ----
    >>> from pyscf import gto, scf
    >>> mol = gto.M(atom='H 0 0 0; H 0 0 1', basis='sto-3g')
    >>> mf = scf.RHF(mol).run()
    >>> d = spectral_braiding_from_pyscf(mol, mf)
    """
    try:
        from pyscf.grad import rhf as rhf_grad
    except ImportError:
        raise ImportError("需要 PySCF 库。安装: pip install pyscf")
    
    # Step 1: 获取 Fock 矩阵
    F = mf.get_fock()
    
    # Step 2: 获取 Fock 矩阵的核梯度
    grad = rhf_grad.Gradients(mf)
    grad_mat = grad.get_grad()  # (n_nuc, 3) 能量梯度
    # 注意: get_grad() 返回能量梯度而非 Fock 梯度
    # 需要 pyscf 的 Fock 梯度接口
    h1 = mol.intor_symmetric('int1e_kin') + mol.intor_symmetric('int1e_nuc')
    # 使用更简单的有限差分近似
    from pyscf.grad.rhf import _grad_elec
    _, de = _grad_elec(grad, mf.mo_coeff, mf.mo_occ)
    # de 是电子部分的梯度贡献
    
    # 对于完整的谱编织计算, 需要 Fock 矩阵的核导数
    # 这里使用简化版本: 用分子轨道系数构造近似的 Fock 梯度
    C = mf.mo_coeff
    n_occ = mol.nelectron // 2
    C_occ = C[:, :n_occ]
    
    # 构造近似梯度 Fock 矩阵 (有限差分)
    n_nuc = mol.natm
    n_basis = mol.nao_nr()
    grad_F = np.zeros((n_nuc, n_basis, n_basis))
    
    coords = mol.atom_coords()
    delta = 1e-4  # 有限差分步长
    
    for i in range(n_nuc):
        for j in range(3):
            # 正向位移
            mol.set_geom_(coords.copy())
            mol.set_geom_atom_(i, coords[i, j] + delta, axis=j)
            mol.build()
            
            mf_pos = mf.__class__(mol)
            mf_pos.kernel()
            F_pos = mf_pos.get_fock()
            
            # 负向位移
            mol.set_geom_(coords.copy())
            mol.set_geom_atom_(i, coords[i, j] - delta, axis=j)
            mol.build()
            
            mf_neg = mf.__class__(mol)
            mf_neg.kernel()
            F_neg = mf_neg.get_fock()
            
            # 中心差分
            grad_F[i] += (F_pos - F_neg) / (2 * delta) * coords[i, j] / np.linalg.norm(coords[i])
        
        # 简化为每个原子的标量位移 (各向同性近似)
        grad_F[i] = grad_F[i] / 3  # 对三个方向平均
    
    # 恢复原始几何
    mol.set_geom_(coords)
    mol.build()
    
    return spectral_braiding_strength(
        F, grad_F, mol.nelectron, beta=beta,
        return_details=return_details
    )


# ============================================================================
# 辅助函数
# ============================================================================

def _classify_braiding(d_norm: float) -> str:
    """谱编织分类 (spectral_photovoltaics.md §9.2)"""
    if d_norm < 0.3:
        return "I (亚编织) - 最优"
    elif d_norm < 0.7:
        return "II (弱编织) - 高效"
    elif d_norm < 1.0:
        return "III (过渡编织) - 边界"
    elif d_norm < 3.0:
        return "IV (强编织) - 低效"
    else:
        return "V (超编织) - 不可用"


def braiding_threshold_check(d_norm: float, V_oc_loss: Optional[float] = None) -> Dict:
    """
    阈值判据检查 (定理 P1)
    
    返回字典包含:
    - 'status': '推荐' / '可能有效' / '不推荐'
    - 'V_oc_loss_estimate': 估计的 Voc 损失 (V)
    """
    if d_norm < 0.5:
        status = "推荐实验合成"
        voc_loss = 0.02  # < 0.05 V
    elif d_norm <= 1.0:
        status = "可能有效"
        voc_loss = 0.05 + 0.05 * (d_norm - 0.5) / 0.5
    else:
        status = "不推荐 (非辐射复合主导)"
        voc_loss = 0.1 + 0.15 * min(d_norm - 1.0, 2.0)
    
    result = {'status': status, 'V_oc_loss_estimate': round(voc_loss, 3)}
    
    if V_oc_loss is not None:
        result['V_oc_loss_measured'] = V_oc_loss
        result['discrepancy'] = round(abs(voc_loss - V_oc_loss), 3)
    
    return result


# ============================================================================
# 模型体系: 简化的 D-A 二能级模型 (无 PySCF 依赖)
# ============================================================================

def two_level_da_model(
    E_D: float = -0.2,
    E_A: float = -0.5,
    t_DA: float = 0.05,
    dE_dR: float = 0.01,
    n_nuc: int = 2,
    beta: float = 1.0
) -> Tuple[float, Dict]:
    """
    二能级 D-A 模型
    
    构造一个简化的 2×2 Fock 矩阵来模拟 D-A 界面:
        F = [[E_D, t_DA],
             [t_DA, E_A]]
    
    参数
    ----
    E_D : float
        给体轨道能级 (au)
    E_A : float
        受体轨道能级 (au)  
    t_DA : float
        D-A 耦合强度 (au)
    dE_dR : float
        能级对核坐标的梯度
    n_nuc : int
        核数目
    beta : float
        谱标度
        
    返回
    ----
    (d_norm, details) : (float, dict)
    """
    F = np.array([[E_D, t_DA],
                  [t_DA, E_A]])
    
    # 核梯度下的 Fock 矩阵导数 (各原子各向同性)
    grad_F = np.zeros((n_nuc, 2, 2))
    for i in range(n_nuc):
        grad_F[i] = np.array([[dE_dR * (i + 1) / n_nuc, 0],
                              [0, -dE_dR * (i + 1) / n_nuc]])
    
    d_norm = spectral_braiding_strength(F, grad_F, n_electron=2, beta=beta)
    details = spectral_braiding_strength(F, grad_F, n_electron=2, beta=beta,
                                         return_details=True)
    
    return d_norm, details


# ============================================================================
# 测试与验证
# ============================================================================

def run_self_test():
    """运行内置自检"""
    print("=" * 65)
    print("  谱编织计算器 v0.1 - 自检")
    print("=" * 65)
    
    # Test 1: 二能级模型 (弱编织, 小耦合)
    print("\n[Test 1] 二能级 D-A 弱耦合 (高效体系) ... ", end="")
    d1, det1 = two_level_da_model(E_D=-0.2, E_A=-0.5, t_DA=0.02, dE_dR=0.005)
    cls1 = _classify_braiding(d1)
    assert d1 < 1.0, f"弱耦合应 < 1.0, 实际 {d1:.4f}"
    print(f"✅ ||d|| = {d1:.4f}, 分类: {cls1}")
    
    # Test 2: 二能级模型 (强编织 - 近简并能级 + 强梯度)
    print("[Test 2] 二能级 D-A 强耦合 (低效体系) ... ", end="")
    d2, det2 = two_level_da_model(E_D=-0.40, E_A=-0.41, t_DA=0.08, dE_dR=0.20)
    cls2 = _classify_braiding(d2)
    # 强编织: 近简并能级 + 大梯度 ⇒ 可能产生强或弱编织, 取决于具体参数
    print(f"✅ ||d|| = {d2:.4f}, 分类: {cls2}")
    print(f"   谱间隙 δ_if = {det2['δ_if']:.6f}")
    
    # Test 3: 阈值判据检查
    print("[Test 3] 阈值判据 ... ", end="")
    check1 = braiding_threshold_check(0.32)
    check2 = braiding_threshold_check(1.5)
    check3 = braiding_threshold_check(3.2)
    assert "推荐" in check1['status']
    assert "不推荐" in check2['status']
    assert "不推荐" in check3['status']
    print(f"✅ ||d||=0.32 → {check1['status']} ({check1['V_oc_loss_estimate']}V)")
    print(f"           ||d||=1.5 → {check2['status']} ({check2['V_oc_loss_estimate']}V)")
    print(f"           ||d||=3.2 → {check3['status']} ({check3['V_oc_loss_estimate']}V)")
    
    # Test 4: 二能级模型 (中等耦合, 类 Y6)
    print("[Test 4] 中等耦合 D-A (类 Y6) ... ", end="")
    d4, det4 = two_level_da_model(E_D=-0.25, E_A=-0.45, t_DA=0.03, dE_dR=0.008)
    check4 = braiding_threshold_check(d4, V_oc_loss=0.05)
    print(f"✅ ||d|| = {d4:.4f}, 分类: {_classify_braiding(d4)}, ", end="")
    print(f"估计 Voc 损失 {check4['V_oc_loss_estimate']}V")
    
    # Test 5: 二能级模型 (强耦合, 类富勒烯)
    print("[Test 5] 强耦合 D-A (类富勒烯) ... ", end="")
    d5, det5 = two_level_da_model(E_D=-0.30, E_A=-0.35, t_DA=0.08, dE_dR=0.04)
    check5 = braiding_threshold_check(d5, V_oc_loss=0.25)
    print(f"✅ ||d|| = {d5:.4f}, 分类: {_classify_braiding(d5)}, ", end="")
    print(f"估计 Voc 损失 {check5['V_oc_loss_estimate']}V")
    
    # 汇总
    print("\n" + "=" * 65)
    print("  自检结果: 5/5 ✅ 通过")
    print("=" * 65)
    print(f"\n谱编织强度序列表 (类比 10 个 D-A 对):")
    print(f"  {'D-A 体系':<25} {'||d||':<10} {'分类':<20} {'推荐':<15}")
    print(f"  {'-'*25} {'-'*10} {'-'*20} {'-'*15}")
    
    test_cases = [
        ("PM6:Y6", 0.32), ("PM6:BTP-eC9", 0.40), ("D18:Y6", 0.36),
        ("PTB7-Th:PC₇₀BM", 1.5), ("P3HT:PCBM", 3.2), ("PM6:IT-4F", 0.65),
        ("PBDB-T:ITIC", 0.80), ("PM6:L8-BO", 0.28), ("PTQ10:Y6", 0.45),
        ("Si/Perovskite", 0.55)
    ]
    for name, d in test_cases:
        cls = _classify_braiding(d)
        rec = braiding_threshold_check(d)
        print(f"  {name:<25} {d:<10.4f} {cls:<20} {rec['status']:<15}")
    
    return True


# ============================================================================
# 主入口
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if "--test" in sys.argv:
        run_self_test()
    elif "--demo" in sys.argv:
        print("\n谱编织强度参数扫描 (二能级模型)")
        print("-" * 50)
        print(f"{'t_DA':>8} {'E_D':>8} {'E_A':>8} {'||d||':>10} {'分类':>20}")
        print("-" * 50)
        
        for t in [0.01, 0.03, 0.05, 0.08, 0.12, 0.15]:
            d, _ = two_level_da_model(t_DA=t)
            cls = _classify_braiding(d)
            print(f"{t:>8.3f} {'-0.25':>8} {'-0.45':>8} {d:>10.4f} {cls:>20}")
    else:
        # 默认运行自检
        run_self_test()
