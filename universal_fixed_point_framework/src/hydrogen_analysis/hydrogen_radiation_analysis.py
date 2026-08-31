"""
任务 3：直接计算氢原子偶极跃迁矩阵元和辐射速率
验证拓扑禁戒导致的辐射抑制

物理：
- 二维氢原子在磁场中，电偶极跃迁选择定则 Δm = ±1
- 偶极矩算符 d = e r = r(cosθ, sinθ)
- 辐射速率（爱因斯坦 A 系数）：A_ij = (4ω^3 / 3c^3) |<i|d|j>|^2
- 原子单位：c ≈ 137.036

目标：
1. 计算不同 B 值下低能态的本征向量
2. 计算偶极跃迁矩阵元和辐射速率
3. 统计平均辐射速率随 B 的变化
4. 与谱维数 D2 对比，验证辐射抑制与奇异连续谱的关联
"""

import numpy as np
from scipy.linalg import eigh
import json
import time

def radial_hamiltonian(B, m, r_max, N_r):
    """构建径向哈密顿量"""
    dr = r_max / (N_r + 1)
    r = np.linspace(dr, r_max - dr, N_r)
    
    diag = np.ones(N_r) / dr**2
    off_diag = -0.5 * np.ones(N_r - 1) / dr**2
    
    V_eff = m**2 / (2 * r**2) + m * B / 2 + B**2 * r**2 / 8 - 1.0 / r
    
    H = np.diag(diag + V_eff) + np.diag(off_diag, 1) + np.diag(off_diag, -1)
    return H, r

def compute_eigenstates(B, m_values, r_max, N_r, n_states=30):
    """计算给定 B 下的低能本征态（保留本征向量）
    
    返回：
        states: list of dict，每个包含 E, m, vector (径向波函数), r_grid
    """
    all_states = []
    
    for m in m_values:
        H, r = radial_hamiltonian(B, m, r_max, N_r)
        evals, evecs = eigh(H)
        
        # 取最低的 n_states 个束缚态（E < 0）
        bound_mask = evals < 0
        bound_evals = evals[bound_mask]
        bound_evecs = evecs[:, bound_mask]
        
        for i in range(min(n_states, len(bound_evals))):
            all_states.append({
                'E': float(bound_evals[i]),
                'm': int(m),
                'vector': bound_evecs[:, i],
                'r': r,
            })
    
    # 按能量排序
    all_states.sort(key=lambda s: s['E'])
    return all_states

def dipole_matrix_element(state_i, state_j):
    """计算两个态之间的电偶极跃迁矩阵元
    
    二维中，偶极矩 d = r(cosθ, sinθ)
    在角动量分波基中：
    <m'|cosθ|m> = (δ_{m',m+1} + δ_{m',m-1}) / 2
    <m'|sinθ|m> = (δ_{m',m+1} - δ_{m',m-1}) / (2i)
    
    径向积分：∫ R_{m'}(r) * r * R_m(r) * r dr（二维径向测度是 r dr）
    
    总矩阵元：|d|^2 = |d_x|^2 + |d_y|^2
    """
    mi, mj = state_i['m'], state_j['m']
    
    # 选择定则：Δm = ±1
    if abs(mi - mj) != 1:
        return 0.0
    
    # 径向积分（注意：波函数已按 1/sqrt(r) 归一化，所以测度是 dr）
    # 实际上，我们的径向方程是按 u(r) = sqrt(r) R(r) 写的
    # 所以 <i|r|j> = ∫ u_i(r) * r * u_j(r) dr
    r = state_i['r']
    vi, vj = state_i['vector'], state_j['vector']
    
    # 确保 r 网格相同
    if not np.array_equal(r, state_j['r']):
        # 如果网格不同，需要插值（这里假设相同）
        return 0.0
    
    radial_integral = np.trapezoid(vi * r * vj, r)
    
    # 角向因子
    # |d|^2 = (radial_integral)^2 * (|cos 角向因子|^2 + |sin 角向因子|^2)
    # 对于 Δm = ±1，角向因子的模平方和 = 1/2
    # （cos 和 sin 的角向因子各贡献 1/4，合计 1/2）
    angular_factor_sq = 0.5
    
    d_sq = radial_integral**2 * angular_factor_sq
    return float(d_sq)

def compute_radiation_rates(states, c=137.036):
    """计算所有允许跃迁的辐射速率（爱因斯坦 A 系数）
    
    A_ij = (4ω^3 / 3c^3) * |d_ij|^2
    ω = E_j - E_i（E_j > E_i，从高能态跃迁到低能态）
    
    返回：
        transitions: list of dict，包含 i, j, E_i, E_j, omega, d_sq, A
    """
    transitions = []
    n = len(states)
    
    for i in range(n):
        for j in range(i+1, n):
            # 高能态 j 跃迁到低能态 i
            omega = states[j]['E'] - states[i]['E']
            if omega <= 0:
                continue
            
            d_sq = dipole_matrix_element(states[i], states[j])
            if d_sq < 1e-15:
                continue
            
            # 爱因斯坦 A 系数（原子单位）
            A = (4.0 * omega**3 / (3.0 * c**3)) * d_sq
            
            transitions.append({
                'i': i, 'j': j,
                'E_i': states[i]['E'],
                'E_j': states[j]['E'],
                'm_i': states[i]['m'],
                'm_j': states[j]['m'],
                'omega': float(omega),
                'd_sq': float(d_sq),
                'A': float(A),
            })
    
    return transitions

def analyze_B(B, m_values, r_max, N_r, n_states=25):
    """分析单个 B 值的辐射性质"""
    t0 = time.time()
    
    # 计算本征态
    states = compute_eigenstates(B, m_values, r_max, N_r, n_states)
    n_states_actual = len(states)
    
    if n_states_actual < 5:
        print(f"  B={B:.4f}: 仅 {n_states_actual} 个态，跳过")
        return None
    
    # 计算辐射速率
    transitions = compute_radiation_rates(states)
    n_transitions = len(transitions)
    
    if n_transitions == 0:
        print(f"  B={B:.4f}: 无允许跃迁，跳过")
        return None
    
    # 统计
    A_values = np.array([t['A'] for t in transitions])
    d_sq_values = np.array([t['d_sq'] for t in transitions])
    omega_values = np.array([t['omega'] for t in transitions])
    
    # 按能量区间统计（验证高能/低能态的辐射速率差异）
    energy_mid = (states[0]['E'] + states[-1]['E']) / 2
    
    # 平均辐射速率（对数平均，因为 A 跨度大）
    A_mean = float(np.mean(A_values))
    A_median = float(np.median(A_values))
    A_log_mean = float(np.exp(np.mean(np.log(A_values + 1e-20))))
    
    # 偶极矩阵元统计
    d_sq_mean = float(np.mean(d_sq_values))
    d_sq_median = float(np.median(d_sq_values))
    
    # 每个态的总辐射速率（所有从该态出发的跃迁的 A 之和）
    total_A_per_state = np.zeros(n_states_actual)
    n_transitions_per_state = np.zeros(n_states_actual)
    for t in transitions:
        total_A_per_state[t['j']] += t['A']  # 从高能态 j 跃迁
        n_transitions_per_state[t['j']] += 1
    
    # 有辐射跃迁的态的比例
    n_radiating_states = np.sum(n_transitions_per_state > 0)
    radiating_fraction = float(n_radiating_states / n_states_actual)
    
    # 平均每个态的辐射速率
    mean_A_per_state = float(np.mean(total_A_per_state[total_A_per_state > 0])) if n_radiating_states > 0 else 0.0
    
    elapsed = time.time() - t0
    
    result = {
        'B': float(B),
        'n_states': int(n_states_actual),
        'n_transitions': int(n_transitions),
        'E_min': float(states[0]['E']),
        'E_max': float(states[-1]['E']),
        'A_mean': A_mean,
        'A_median': A_median,
        'A_log_mean': A_log_mean,
        'd_sq_mean': d_sq_mean,
        'd_sq_median': d_sq_median,
        'omega_mean': float(np.mean(omega_values)),
        'radiating_fraction': radiating_fraction,
        'mean_A_per_radiating_state': mean_A_per_state,
        'total_A_all_states': float(np.sum(total_A_per_state)),
        'elapsed_seconds': float(elapsed),
    }
    
    return result, states, transitions

def main():
    print("=" * 90)
    print("任务 3：氢原子偶极跃迁矩阵元和辐射速率直接计算")
    print("=" * 90)
    print()
    
    # 计算参数
    r_max = 60.0
    N_r = 1500
    m_values = list(range(-5, 6))  # m = -5,...,5（控制计算量）
    n_states = 25  # 每个 m 取 25 个最低能态
    
    # 代表性 B 值（规则区 + 过渡区 + 混沌区）
    B_values = [0.001, 0.01, 0.05, 0.1, 0.15, 0.2]
    
    print(f"计算参数：")
    print(f"  r_max = {r_max}, N_r = {N_r}")
    print(f"  m_values = {m_values}")
    print(f"  n_states per m = {n_states}")
    print(f"  B_values = {B_values}")
    print(f"  c = 137.036 a.u.")
    print()
    
    results = []
    all_states_by_B = {}
    all_transitions_by_B = {}
    
    for B in B_values:
        print(f"B = {B:.4f} a.u. ({B*2.35e5:.2e} T) ... ", end="", flush=True)
        r = analyze_B(B, m_values, r_max, N_r, n_states)
        if r is not None:
            result, states, transitions = r
            results.append(result)
            all_states_by_B[B] = states
            all_transitions_by_B[B] = transitions
            print(f"态数={result['n_states']}, 跃迁数={result['n_transitions']}, "
                  f"A_median={result['A_median']:.3e}, "
                  f"辐射态比例={result['radiating_fraction']:.3f} "
                  f"({result['elapsed_seconds']:.1f}s)")
        else:
            print("跳过")
    
    print()
    print("=" * 90)
    print("结果汇总")
    print("=" * 90)
    print()
    
    print(f"{'B':>8} {'B(T)':>10} {'态数':>5} {'跃迁':>5} {'A_median':>12} "
          f"{'A_logmean':>12} {'d_sq_med':>12} {'辐射态%':>8} {'每态A':>12}")
    print("-" * 100)
    
    for r in results:
        B_T = r['B'] * 2.35e5
        print(f"{r['B']:8.4f} {B_T:10.2e} {r['n_states']:5d} {r['n_transitions']:5d} "
              f"{r['A_median']:12.3e} {r['A_log_mean']:12.3e} "
              f"{r['d_sq_median']:12.3e} {r['radiating_fraction']*100:8.1f} "
              f"{r['mean_A_per_radiating_state']:12.3e}")
    
    print()
    
    # 关键分析：辐射速率随 B 的变化
    if len(results) >= 2:
        print("=" * 90)
        print("关键分析：辐射抑制与拓扑禁戒")
        print("=" * 90)
        print()
        
        # 以最低 B（规则区）为参考
        ref = results[0]
        print(f"参考（规则区 B={ref['B']:.4f}）：")
        print(f"  A_median = {ref['A_median']:.3e}")
        print(f"  d_sq_median = {ref['d_sq_median']:.3e}")
        print(f"  辐射态比例 = {ref['radiating_fraction']*100:.1f}%")
        print()
        
        print(f"{'B':>8} {'A_med/A_ref':>12} {'d_sq/d_ref':>12} {'辐射态%/ref':>12} {'总A/A_ref':>12}")
        print("-" * 60)
        
        for r in results:
            A_ratio = r['A_median'] / ref['A_median'] if ref['A_median'] > 0 else 0
            d_ratio = r['d_sq_median'] / ref['d_sq_median'] if ref['d_sq_median'] > 0 else 0
            frac_ratio = r['radiating_fraction'] / ref['radiating_fraction'] if ref['radiating_fraction'] > 0 else 0
            total_A_ratio = r['total_A_all_states'] / ref['total_A_all_states'] if ref['total_A_all_states'] > 0 else 0
            
            print(f"{r['B']:8.4f} {A_ratio:12.4f} {d_ratio:12.4f} {frac_ratio:12.4f} {total_A_ratio:12.4f}")
        
        print()
        
        # 最强 B 处的抑制
        strongest = results[-1]
        total_suppression = 1.0 - strongest['total_A_all_states'] / ref['total_A_all_states'] if ref['total_A_all_states'] > 0 else 0
        print(f"最强混沌区（B={strongest['B']:.4f}）相对于规则区：")
        print(f"  总辐射速率抑制 = {total_suppression*100:.1f}%")
        print(f"  偶极矩阵元中值抑制 = {(1-strongest['d_sq_median']/ref['d_sq_median'])*100:.1f}%")
        print(f"  辐射态比例抑制 = {(1-strongest['radiating_fraction']/ref['radiating_fraction'])*100:.1f}%")
        print()
        print("解释：")
        print("  - 偶极矩阵元抑制 = 标准局域化效应（波函数重叠减小）")
        print("  - 辐射态比例抑制 = 拓扑禁戒效应（满足选择定则但无法辐射的态）")
        print("  - 总辐射速率抑制 = 两者之和")
        print()
    
    # 保存结果
    output_file = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\results\hydrogen_radiation_results.json"
    
    # 转换为可序列化格式（去掉 vector）
    serializable_results = []
    for r in results:
        serializable_results.append({k: v for k, v in r.items()})
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'parameters': {
                'r_max': r_max,
                'N_r': N_r,
                'm_values': m_values,
                'n_states_per_m': n_states,
            },
            'results': serializable_results,
        }, f, indent=2, ensure_ascii=False)
    print(f"结果已保存到: {output_file}")

if __name__ == "__main__":
    main()
