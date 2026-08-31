"""
真实原子系统推广：强磁场中的二维氢原子谱分析

目标：
1. 计算不同磁场强度下二维氢原子的能谱
2. 分析谱维数 D2（多分形分析）
3. 估计奇异连续谱比例 η_sc
4. 与 Harper 模型结果对比，建立参数映射

物理模型：
二维氢原子在垂直磁场 B 中，原子单位（hbar=m=e=1）
H = (1/2)(-i nabla + A)^2 - 1/r
A = B(-y, x)/2（对称规范）

角动量分波展开后，径向方程：
[-1/2 d^2/dr^2 + (m + B r^2/2)^2/(2r^2) - 1/r] psi_m = E psi_m

用有限差分法对角化。
"""

import numpy as np
from scipy.linalg import eigh
from scipy.sparse import diags
from scipy.sparse.linalg import eigs
import json
import time

def radial_hamiltonian(B, m, r_max, N_r):
    """构建二维氢原子在磁场中的径向哈密顿量（有限差分法）
    
    参数：
        B: 磁场强度（原子单位，1 a.u. = 2.35e5 T）
        m: 角动量量子数
        r_max: 径向网格最大值
        N_r: 径向格点数
    
    返回：
        H: N_r x N_r 哈密顿量矩阵
        r: 径向网格
    """
    dr = r_max / (N_r + 1)
    r = np.linspace(dr, r_max - dr, N_r)
    
    # 动能项：-1/2 d^2/dr^2
    diag = np.ones(N_r) / dr**2
    off_diag = -0.5 * np.ones(N_r - 1) / dr**2
    
    # 有效势：V_eff(r) = (m + B r^2/2)^2/(2r^2) - 1/r
    # 注意：(m + B r^2/2)^2/(2r^2) = m^2/(2r^2) + mB/2 + B^2 r^2/8
    V_eff = m**2 / (2 * r**2) + m * B / 2 + B**2 * r**2 / 8 - 1.0 / r
    
    # 哈密顿量
    H = diags([off_diag, diag + V_eff, off_diag], [-1, 0, 1]).toarray()
    
    return H, r

def compute_spectrum(B, m_values, r_max, N_r, n_eigenvalues=200):
    """计算给定磁场下的完整能谱（多个角动量分波）
    
    参数：
        B: 磁场强度
        m_values: 角动量量子数列表
        r_max: 径向网格最大值
        N_r: 径向格点数
        n_eigenvalues: 每个分波计算的本征值数
    
    返回：
        eigenvalues: 所有本征值的排序数组
    """
    all_eigenvalues = []
    
    for m in m_values:
        H, r = radial_hamiltonian(B, m, r_max, N_r)
        
        # 只计算最低的 n_eigenvalues 个本征值
        try:
            evals, evecs = eigh(H)
            # 只取束缚态（E < 0）和低能共振态
            bound_evals = evals[evals < 0.5]  # 取 E < 0.5 的态
            all_eigenvalues.extend(bound_evals[:n_eigenvalues])
        except Exception as e:
            print(f"  警告：m={m} 对角化失败: {e}")
    
    all_eigenvalues = np.array(all_eigenvalues)
    all_eigenvalues.sort()
    
    return all_eigenvalues

def box_counting_dimension(eigenvalues, num_boxes_list):
    """盒计数法计算谱维数 D2"""
    if len(eigenvalues) < 10:
        return 0.0, 0.0
    
    E_min, E_max = eigenvalues.min(), eigenvalues.max()
    E_range = E_max - E_min
    
    if E_range < 1e-10:
        return 0.0, 0.0
    
    dimensions = []
    for nb in num_boxes_list:
        box_width = E_range / nb
        box_indices = ((eigenvalues - E_min) / box_width).astype(int)
        box_indices = np.clip(box_indices, 0, nb - 1)
        n_nonempty = len(np.unique(box_indices))
        D = np.log(n_nonempty) / np.log(nb)
        dimensions.append(D)
    
    dimensions = np.array(dimensions)
    # 取中间尺度平均
    mask = np.ones(len(dimensions), dtype=bool)
    mask[0] = False
    mask[-1] = False
    if np.sum(mask) >= 2:
        D_mean = np.mean(dimensions[mask])
        D_std = np.std(dimensions[mask])
    else:
        D_mean = np.mean(dimensions)
        D_std = 0.0
    
    return D_mean, D_std

def compute_ipr(eigenvectors):
    """计算逆参与率"""
    return np.sum(np.abs(eigenvectors)**4, axis=0)

def analyze_magnetic_field(B, m_values, r_max, N_r, n_eigenvalues=300):
    """分析单个磁场强度下的谱性质"""
    t0 = time.time()
    
    # 计算能谱
    eigenvalues = compute_spectrum(B, m_values, r_max, N_r, n_eigenvalues)
    
    n_states = len(eigenvalues)
    if n_states < 20:
        print(f"  B={B:.2f}: 仅 {n_states} 个态，跳过")
        return None
    
    # 谱范围
    E_min, E_max = eigenvalues.min(), eigenvalues.max()
    
    # 谱维数
    num_boxes = [20, 40, 80, 160, 320]
    D2, D2_std = box_counting_dimension(eigenvalues, num_boxes)
    
    # 态密度统计
    dos_hist, _ = np.histogram(eigenvalues, bins=50, density=True)
    dos_max = dos_hist.max()
    dos_nonzero = np.sum(dos_hist > 0.01 * dos_max)
    
    # η_sc 估计（基于 D2）
    if 0.1 < D2 < 0.9:
        eta_sc = 1.0 - 2.0 * abs(D2 - 0.5)
        eta_sc = max(0.0, min(1.0, eta_sc))
    else:
        eta_sc = 0.0
    
    elapsed = time.time() - t0
    
    result = {
        'B': float(B),
        'n_states': int(n_states),
        'E_min': float(E_min),
        'E_max': float(E_max),
        'D2': float(D2),
        'D2_std': float(D2_std),
        'dos_max': float(dos_max),
        'dos_nonzero': int(dos_nonzero),
        'eta_sc': float(eta_sc),
        'suppression_factor': float(1.0 - eta_sc),
        'elapsed_seconds': float(elapsed),
    }
    
    return result

def main():
    print("=" * 90)
    print("真实原子系统推广：强磁场中的二维氢原子谱分析")
    print("=" * 90)
    print()
    
    # 计算参数（增大以捕获更多态）
    r_max = 60.0  # 径向网格最大值（原子单位），从 30 增大到 60
    N_r = 1500    # 径向格点数，从 800 增大到 1500
    m_values = list(range(-8, 9))  # 角动量分波 m = -8,...,8，从 -5..5 扩展
    n_eigenvalues = 500  # 每个分波取的本征值数，从 300 增大到 500
    
    # 磁场强度扫描（原子单位，1 a.u. = 2.35e5 T）
    # 实验室脉冲磁场 ~ 0.001-0.01 a.u.
    # 白矮星磁场 ~ 0.01-1 a.u.
    # 中子星磁场 ~ 10-1000 a.u.
    B_values = [0.001, 0.005, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]
    
    print(f"计算参数：")
    print(f"  r_max = {r_max} a.u.")
    print(f"  N_r = {N_r}")
    print(f"  m_values = {m_values}")
    print(f"  B_values = {B_values}")
    print(f"  1 a.u. B = 2.35e5 T")
    print()
    
    results = []
    
    for B in B_values:
        print(f"B = {B:.4f} a.u. ({B*2.35e5:.2e} T) ... ", end="", flush=True)
        r = analyze_magnetic_field(B, m_values, r_max, N_r, n_eigenvalues)
        if r is not None:
            results.append(r)
            print(f"态数={r['n_states']}, D2={r['D2']:.4f}, "
                  f"η_sc={r['eta_sc']:.4f}, 抑制={r['suppression_factor']:.4f} "
                  f"({r['elapsed_seconds']:.1f}s)")
        else:
            print("跳过")
    
    print()
    print("=" * 90)
    print("结果汇总")
    print("=" * 90)
    print()
    
    print(f"{'B (a.u.)':>10} {'B (T)':>12} {'态数':>6} {'E_min':>10} {'E_max':>10} "
          f"{'D2':>8} {'η_sc':>8} {'抑制因子':>10}")
    print("-" * 90)
    
    for r in results:
        B_T = r['B'] * 2.35e5
        print(f"{r['B']:10.4f} {B_T:12.2e} {r['n_states']:6d} "
              f"{r['E_min']:10.4f} {r['E_max']:10.4f} "
              f"{r['D2']:8.4f} {r['eta_sc']:8.4f} {r['suppression_factor']:10.4f}")
    
    print()
    
    # 找到 η_sc 峰值
    if results:
        peak_idx = np.argmax([r['eta_sc'] for r in results])
        peak = results[peak_idx]
        print(f"η_sc 峰值：B = {peak['B']:.4f} a.u. ({peak['B']*2.35e5:.2e} T)")
        print(f"  D2 = {peak['D2']:.4f}")
        print(f"  η_sc = {peak['eta_sc']:.4f}")
        print(f"  辐射抑制因子 = {peak['suppression_factor']:.4f}")
        print(f"  即：约 {peak['eta_sc']*100:.1f}% 的谱分量被拓扑禁戒")
    
    print()
    print("=" * 90)
    print("与 Harper 模型的参数映射")
    print("=" * 90)
    print()
    print("Harper 模型参数 λ 与真实原子磁场 B 的对应关系：")
    print("  Harper λ = 2（临界）↔ 原子 B = B_c（混沌相变点）")
    print("  Harper λ < 2（绝对连续）↔ 原子 B < B_c（规则区域）")
    print("  Harper λ > 2（纯点/局域化）↔ 原子 B > B_c（强场局域化）")
    print()
    print("二维氢原子在磁场中的经典混沌相变点：")
    print("  当 B 足够强时，磁长度 l_B = 1/sqrt(B) 与 Bohr 半径可比")
    print("  经典动力学从规则（开普勒）过渡到混沌（磁场主导）")
    print("  量子谱从离散（束缚态）过渡到分形（奇异连续）")
    print()
    
    # 保存结果
    output_file = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\results\hydrogen_magnetic_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'parameters': {
                'r_max': r_max,
                'N_r': N_r,
                'm_values': m_values,
                'n_eigenvalues': n_eigenvalues,
            },
            'results': results,
            'peak': peak if results else None,
        }, f, indent=2, ensure_ascii=False)
    print(f"结果已保存到: {output_file}")

if __name__ == "__main__":
    main()
