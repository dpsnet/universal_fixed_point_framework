"""
任务 4：推广到其他真实原子系统

1. Rydberg 原子在电场中的简化模型（一维 s 波径向方程 + Stark 微扰）
2. 概念性推广：三维氢原子、量子点、超冷原子

物理：
Rydberg 原子在电场中，经典动力学是混沌的（电场中的开普勒问题）。
量子谱在电离阈附近表现出复杂的共振结构（Stark 态的混合）。

简化模型：一维 s 波径向方程，电场作为微扰/有效势
H = -1/2 d^2/dr^2 + l(l+1)/(2r^2) - 1/r + F*r*<cosθ>
对于 s 波（l=0），<cosθ> = 0，所以电场的一阶效应为零。
需要考虑 l 混合（至少 l=0 和 l=1 的耦合）。

更简化：用二维模型（m=0 分波），电场在平面内。
H = -1/2 d^2/dr^2 + m^2/(2r^2) - 1/r + F*r（m=0 时电场有效）
"""

import numpy as np
from scipy.linalg import eigh
import json
import time

def stark_hamiltonian(F, m, r_max, N_r):
    """构建 Rydberg 原子在电场中的二维径向哈密顿量
    
    参数：
        F: 电场强度（原子单位，1 a.u. = 5.14e11 V/m）
        m: 角动量量子数
        r_max: 径向网格最大值
        N_r: 径向格点数
    """
    dr = r_max / (N_r + 1)
    r = np.linspace(dr, r_max - dr, N_r)
    
    # 动能
    diag = np.ones(N_r) / dr**2
    off_diag = -0.5 * np.ones(N_r - 1) / dr**2
    
    # 有效势：库仑 + 离心 + 电场（m=0 时电场沿径向，F*r）
    # 对于 m≠0，电场的角向平均为零，但这里用简化模型
    # 实际上电场破坏角动量守恒，需要 l 混合。这里用有效势近似。
    V_eff = m**2 / (2 * r**2) - 1.0 / r
    
    # 电场项：对于 m=0，电场沿径向，有效势为 F*r（线性 Stark 效应）
    # 对于 m≠0，电场的一阶效应为零，但二阶效应存在
    if m == 0:
        V_eff += F * r
    else:
        # 二阶 Stark 效应近似（微扰）
        V_eff += -0.5 * F**2 * r**2 / 4.0  # 简化的二阶项
    
    H = np.diag(diag + V_eff) + np.diag(off_diag, 1) + np.diag(off_diag, -1)
    return H, r

def compute_stark_spectrum(F, m_values, r_max, N_r, n_eigenvalues=100):
    """计算给定电场下的能谱"""
    all_eigenvalues = []
    
    for m in m_values:
        H, r = stark_hamiltonian(F, m, r_max, N_r)
        evals, evecs = eigh(H)
        # 取束缚态和低能共振态（E < 电离阈）
        # 电场中电离阈为 E = 0（简化模型）
        bound_evals = evals[evals < 0.1]
        all_eigenvalues.extend(bound_evals[:n_eigenvalues])
    
    all_eigenvalues = np.array(all_eigenvalues)
    all_eigenvalues.sort()
    return all_eigenvalues

def box_counting_D2(eigenvalues, num_boxes_list):
    """盒计数法计算谱维数 D2"""
    if len(eigenvalues) < 10:
        return 0.0
    
    E_min, E_max = eigenvalues.min(), eigenvalues.max()
    E_range = E_max - E_min
    if E_range < 1e-10:
        return 0.0
    
    dimensions = []
    for nb in num_boxes_list:
        box_width = E_range / nb
        box_indices = ((eigenvalues - E_min) / box_width).astype(int)
        box_indices = np.clip(box_indices, 0, nb - 1)
        n_nonempty = len(np.unique(box_indices))
        D = np.log(n_nonempty) / np.log(nb)
        dimensions.append(D)
    
    dimensions = np.array(dimensions)
    mask = np.ones(len(dimensions), dtype=bool)
    mask[0] = False
    mask[-1] = False
    if np.sum(mask) >= 2:
        return float(np.mean(dimensions[mask]))
    return float(np.mean(dimensions))

def main():
    print("=" * 90)
    print("任务 4：推广到 Rydberg 原子在电场中（简化二维模型）")
    print("=" * 90)
    print()
    
    # 计算参数
    r_max = 100.0  # Rydberg 原子半径大，需要大 r_max
    N_r = 2000
    m_values = [0, 1, 2, 3]  # 低角动量分波
    
    # 电场强度扫描（原子单位）
    # 经典电离阈 F_c = 1/(16n^4)，对于 n=20，F_c ≈ 2e-4 a.u. ≈ 1e8 V/m
    # 实验室可达到的电场：~1e5-1e7 V/m = 2e-7 - 2e-5 a.u.
    # 但 Rydberg 原子（n~50-100）的电离阈更低
    F_values = [1e-6, 5e-6, 1e-5, 5e-5, 1e-4, 5e-4, 1e-3]
    
    print(f"计算参数：")
    print(f"  r_max = {r_max} a.u., N_r = {N_r}")
    print(f"  m_values = {m_values}")
    print(f"  F_values = {F_values}")
    print(f"  1 a.u. F = 5.14e11 V/m")
    print()
    
    results = []
    
    for F in F_values:
        t0 = time.time()
        print(f"F = {F:.2e} a.u. ({F*5.14e11:.2e} V/m) ... ", end="", flush=True)
        
        eigenvalues = compute_stark_spectrum(F, m_values, r_max, N_r, 150)
        n_states = len(eigenvalues)
        
        if n_states < 10:
            print(f"仅 {n_states} 个态，跳过")
            continue
        
        D2 = box_counting_D2(eigenvalues, [20, 40, 80, 160, 320])
        
        # η_sc 估计
        if 0.1 < D2 < 0.9:
            eta_sc = 1.0 - 2.0 * abs(D2 - 0.5)
            eta_sc = max(0.0, min(1.0, eta_sc))
        else:
            eta_sc = 0.0
        
        elapsed = time.time() - t0
        results.append({
            'F': float(F),
            'F_Vm': float(F * 5.14e11),
            'n_states': int(n_states),
            'E_min': float(eigenvalues.min()),
            'E_max': float(eigenvalues.max()),
            'D2': float(D2),
            'eta_sc': float(eta_sc),
            'suppression_factor': float(1.0 - eta_sc),
            'elapsed_seconds': float(elapsed),
        })
        print(f"态数={n_states}, D2={D2:.4f}, η_sc={eta_sc:.4f}, "
              f"抑制={1-eta_sc:.4f} ({elapsed:.1f}s)")
    
    print()
    print("=" * 90)
    print("结果汇总")
    print("=" * 90)
    print()
    
    print(f"{'F (a.u.)':>12} {'F (V/m)':>12} {'态数':>6} {'E_min':>10} {'E_max':>10} "
          f"{'D2':>8} {'η_sc':>8} {'抑制因子':>10}")
    print("-" * 90)
    
    for r in results:
        print(f"{r['F']:12.2e} {r['F_Vm']:12.2e} {r['n_states']:6d} "
              f"{r['E_min']:10.4f} {r['E_max']:10.4f} "
              f"{r['D2']:8.4f} {r['eta_sc']:8.4f} {r['suppression_factor']:10.4f}")
    
    print()
    
    if results:
        peak_idx = np.argmax([r['eta_sc'] for r in results])
        peak = results[peak_idx]
        print(f"η_sc 峰值：F = {peak['F']:.2e} a.u. ({peak['F_Vm']:.2e} V/m)")
        print(f"  D2 = {peak['D2']:.4f}")
        print(f"  η_sc = {peak['eta_sc']:.4f}")
        print(f"  辐射抑制因子 = {peak['suppression_factor']:.4f}")
        print(f"  即：约 {peak['eta_sc']*100:.1f}% 的谱分量被拓扑禁戒")
    
    print()
    print("=" * 90)
    print("概念性推广：其他真实原子系统")
    print("=" * 90)
    print()
    print("1. 三维氢原子在磁场中：")
    print("   - 与二维模型相比，三维有更多的角动量自由度（l=0,1,2,...）")
    print("   - 经典混沌更显著（三维开普勒问题在磁场中完全混沌）")
    print("   - 预期奇异连续谱特征更强，η_sc 更大")
    print("   - 计算量：三维哈密顿量需要基组展开（如 Sturmian 基），")
    print("     或用分波法耦合不同 l，计算量比二维大 1-2 个数量级")
    print()
    print("2. Rydberg 原子在电场中：")
    print("   - 经典电离阈 F_c = 1/(16n^4)，n=50 时 F_c ≈ 1e-7 a.u.")
    print("   - 实验室可达到 F ~ 1e-7 - 1e-5 a.u.，正好在电离阈附近")
    print("   - 预期：在电离阈附近，谱表现出奇异连续特征，η_sc 峰值")
    print("   - 优势：Rydberg 原子寿命长，辐射速率可精确测量")
    print()
    print("3. 半导体量子点：")
    print("   - 人工原子，电子在三维受限势中运动")
    print("   - 外加磁场/电场可诱导混沌（如体育场形量子点）")
    print("   - 谱可通过输运测量（库仑阻塞峰）探测")
    print("   - 预期：混沌量子点的谱表现出奇异连续特征")
    print()
    print("4. 超冷原子在光晶格中：")
    print("   - 准周期势（如 Harper 模型的物理实现）")
    print("   - 可通过调节激光强度精确控制 λ 参数")
    print("   - 谱可通过 Bragg 光谱或量子气体显微镜探测")
    print("   - 这是 Harper 模型最直接的实验实现")
    print()
    
    # 保存结果
    output_file = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\results\rydberg_stark_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'parameters': {
                'r_max': r_max,
                'N_r': N_r,
                'm_values': m_values,
            },
            'results': results,
            'peak': peak if results else None,
        }, f, indent=2, ensure_ascii=False)
    print(f"结果已保存到: {output_file}")

if __name__ == "__main__":
    main()
