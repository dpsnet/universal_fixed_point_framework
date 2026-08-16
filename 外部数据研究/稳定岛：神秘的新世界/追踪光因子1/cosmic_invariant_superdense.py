"""
宇宙时空转换因子超密集探索 —— 金箍棒 3.0 DMRG
超级密集扫描各向异性参数Δ (步长0.002)，寻找独立于规则的精细诊断不变量
检验：是否存在关系场自身的"光速"——即绝对的转换因子？
严格遵循：关系本体论、防工具理性、反对对齐
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tenpy.models.model import CouplingMPOModel
from tenpy.models.lattice import Chain
from tenpy.networks.site import SpinHalfSite
from tenpy.networks.mps import MPS
from tenpy.algorithms import dmrg

class XXZModel(CouplingMPOModel):
    """链式XXZ模型，各向异性参数Δ和矛盾边强度可独立设置"""
    def __init__(self, model_params):
        L = model_params.get('L', 8)
        self.delta = model_params.get('delta', 1.0)
        self.contradiction_strength = model_params.get('contradiction_strength', 1.5)
        self.contradiction_edge = model_params.get('contradiction_edge', (L//2 - 1, L//2))
        
        # 预计算键强度数组，修复TeNPy API兼容性
        J_arr = np.ones(L - 1)
        ci, cj = self.contradiction_edge
        if ci < L - 1 and cj == ci + 1:
            J_arr[ci] = self.contradiction_strength
        self.J_arr = J_arr
        
        lat = Chain(L, SpinHalfSite(conserve='Sz'), bc='open')
        model_params['lattice'] = lat
        CouplingMPOModel.__init__(self, model_params)

    def init_terms(self, model_params=None):
        if model_params is None:
            model_params = {}
        # XY项（翻转项），使用数组形式 + unit_cell=0 + dx=[1]
        self.add_coupling(self.J_arr * 0.5, 0, 'Sp', 0, 'Sm', dx=[1], plus_hc=True)
        # Ising项（对角项），乘以各向异性参数Δ，使用数组形式 + unit_cell=0 + dx=[1]
        self.add_coupling(self.J_arr * self.delta, 0, 'Sz', 0, 'Sz', dx=[1])


def compute_diagnostics(L, contradiction_edge, s, delta, chi_max=100):
    """用DMRG计算基态，返回能隙、默认诊断和精细诊断"""
    M = XXZModel(dict(
        L=L, contradiction_edge=contradiction_edge,
        contradiction_strength=s, delta=delta,
        bc_MPS='finite', conserve='Sz'
    ))
    init = ['up', 'down'] * (L // 2)
    if L % 2 == 1: init.append('up')
    psi = MPS.from_product_state(M.lat.mps_sites(), init, bc='finite')
    dmrg_params = {'mixer': True, 'chi_max': chi_max, 'max_sweeps': 50, 'verbose': 0}
    eng = dmrg.run(psi, M, dmrg_params)
    E0 = eng['E']
    
    init_ex = init.copy()
    center = L // 2
    init_ex[center] = 'down' if init_ex[center] == 'up' else 'up'
    psi_ex = MPS.from_product_state(M.lat.mps_sites(), init_ex, bc='finite')
    eng_ex = dmrg.run(psi_ex, M, dmrg_params)
    E1 = eng_ex['E']
    gap = E1 - E0

    Sz = psi.expectation_value('Sz')
    coarse = np.mean(np.abs(Sz))
    
    corrs = []
    for i in range(L - 1):
        corr = psi.correlation_function('Sz', 'Sz', [i], [i+1])
        corrs.append(corr[0])
    fine = np.std(corrs) if corrs else 0.0
    
    return gap, coarse, fine


if __name__ == "__main__":
    L = 8
    contradiction_edge = (L//2 - 1, L//2)
    contradiction_strength = 1.5
    # 超级密集扫描：步长0.002，共501个点
    delta_values = np.linspace(0.0, 1.0, 501)
    
    gaps, coarse_vals, fine_vals = [], [], []
    
    print(f"=== 宇宙转换因子超密集探索 (L={L}, s={contradiction_strength}, 步长=0.002) ===")
    print(f"扫描各向异性参数 Δ: 0.000 → 1.000，共 {len(delta_values)} 个点\n")
    
    for delta in delta_values:
        gap, coarse, fine = compute_diagnostics(L, contradiction_edge, contradiction_strength, delta, chi_max=100)
        gaps.append(gap)
        coarse_vals.append(coarse)
        fine_vals.append(fine)
        if len(gaps) % 50 == 0:
            print(f"  进度: {len(gaps)}/{len(delta_values)} (Δ={delta:.3f})")
    
    gaps = np.array(gaps)
    coarse_vals = np.array(coarse_vals)
    fine_vals = np.array(fine_vals)
    
    # 保存数据
    np.savetxt('cosmic_invariant_superdense_results.csv',
               np.column_stack((delta_values, gaps, coarse_vals, fine_vals)),
               header='delta,gap,coarse,fine', delimiter=',')
    
    # 诊断图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    ax1.plot(delta_values, coarse_vals, '-', color='#1f77b4', lw=0.3)
    ax1.set_xlabel('Anisotropy Δ'); ax1.set_ylabel('Coarse metric')
    ax1.set_title('Default Diagnosis (Entity-level)')
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(delta_values, fine_vals, '-', color='#d62728', lw=0.3)
    ax2.set_xlabel('Anisotropy Δ'); ax2.set_ylabel('Fine metric')
    ax2.set_title('Enhanced Diagnosis (Relation-level)')
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle(f'Super-Dense Cosmic Invariant Search (L={L}, s={contradiction_strength}, step=0.002)')
    plt.tight_layout()
    plt.savefig('cosmic_invariant_superdense_diagnosis.png', dpi=150)
    
    # 不变性分析
    print("\n=== 超密集扫描不变性分析 ===")
    fine_mean = np.mean(fine_vals)
    fine_std = np.std(fine_vals)
    fine_range = np.max(fine_vals) - np.min(fine_vals)
    relative_range = fine_range / fine_mean if fine_mean > 0 else np.inf
    
    print(f"精细诊断: 均值={fine_mean:.6f}, 标准差={fine_std:.6f}, 范围={fine_range:.6f}")
    print(f"相对波动: {relative_range*100:.4f}%")
    
    if relative_range < 0.01:
        print("✓ 发现精细诊断对Δ几乎完全不变——关系场的内在转换因子被精确锁定！")
    elif relative_range < 0.05:
        print("○ 精细诊断对Δ弱敏感——可能存在近似不变量，需更大系统验证。")
    else:
        print("✗ 超密集扫描确认：精细诊断随Δ显著变化——在当前条件下未发现不变量。")
    
    # 分段稳定性分析
    if len(fine_vals) > 50:
        segment_size = 50  # 每段50个点（步长0.1）
        min_segment_range = float('inf')
        min_segment_start = 0.0
        for start in range(0, len(fine_vals) - segment_size + 1, 10):
            segment = fine_vals[start:start+segment_size]
            seg_range = np.max(segment) - np.min(segment)
            seg_mean = np.mean(segment)
            seg_rel = seg_range / seg_mean if seg_mean > 0 else np.inf
            if seg_rel < min_segment_range:
                min_segment_range = seg_rel
                min_segment_start = delta_values[start]
        print(f"\n分段分析: 最稳定区间起始Δ≈{min_segment_start:.3f}，区间内相对波动={min_segment_range*100:.4f}%")
        if min_segment_range < 0.01:
            print("  → 提示：该区间内可能存在局部不变量。")
    
    # 默认诊断对比
    coarse_mean = np.mean(coarse_vals)
    coarse_range = np.max(coarse_vals) - np.min(coarse_vals)
    coarse_relative = coarse_range / coarse_mean if coarse_mean > 0 else np.inf
    print(f"\n默认诊断: 均值={coarse_mean:.6f}, 范围={coarse_range:.6f}, 相对波动={coarse_relative*100:.4f}%")
    
    print("\nDone. 数据已保存。")
