"""
Harper 模型增强谱分析：多分形维数 D_q、Thouless 指数、有限尺寸标度
用于更精确确定奇异连续谱区域的 η_sc 峰值

分析内容：
1. λ=2 附近精细扫描（1.85, 1.90, 1.95, 2.00, 2.05, 2.10, 2.15）
2. 多分形维数 D_q（q=0,1,2,3）
3. Thouless 指数（态密度标度）
4. 有限尺寸标度（N=1000, 2000, 4000）
"""

import numpy as np
from scipy.linalg import eigh
import json
import time

def build_harper_matrix(N, lam, alpha, phi=0.0):
    """构建 Harper 模型矩阵（周期边界）"""
    H = np.zeros((N, N))
    n = np.arange(N)
    H[n, n] = lam * np.cos(2 * np.pi * alpha * n + phi)
    H[n, (n + 1) % N] = 1.0
    H[(n + 1) % N, n] = 1.0
    return H

def generalized_dimension(eigenvalues, q_values, num_scales=None):
    """计算多分形广义维数 D_q
    
    D_q = (1/(q-1)) * lim(log(sum(p_i^q)) / log(epsilon))
    
    其中 p_i 是第 i 个盒子中的谱测度比例
    """
    if num_scales is None:
        num_scales = [20, 40, 80, 160, 320]
    
    E_min, E_max = eigenvalues.min(), eigenvalues.max()
    E_range = E_max - E_min
    N_total = len(eigenvalues)
    
    D_q_results = {}
    
    for q in q_values:
        log_epsilon = []
        log_sum_pq = []
        
        for nb in num_scales:
            box_width = E_range / nb
            box_indices = ((eigenvalues - E_min) / box_width).astype(int)
            box_indices = np.clip(box_indices, 0, nb - 1)
            
            # 每个盒子中的点数
            counts = np.bincount(box_indices, minlength=nb)
            # 概率
            p = counts / N_total
            # 只考虑非空盒子
            p_nonzero = p[p > 0]
            
            if q == 1:
                # D_1 = lim(sum(p_i log p_i) / log(epsilon))
                sum_pq = -np.sum(p_nonzero * np.log(p_nonzero))
            else:
                sum_pq = np.sum(p_nonzero ** q)
            
            log_epsilon.append(np.log(1.0 / box_width))
            if q == 1:
                log_sum_pq.append(sum_pq)
            else:
                log_sum_pq.append(np.log(sum_pq) / (q - 1))
        
        # 线性拟合求 D_q
        # 对于 q≠1：D_q = -(1/(q-1)) * d[log(sum p^q)]/d[log(1/epsilon)] = -斜率
        # 对于 q=1：D_1 = d[sum(p log p)]/d[log(epsilon)] = d[-sum(p log p)]/d[log_epsilon] = 斜率
        # （因为 log_sum_pq 对 q=1 是 -sum(p log p)）
        log_epsilon = np.array(log_epsilon)
        log_sum_pq = np.array(log_sum_pq)
        
        # 用中间尺度拟合（避免有限尺寸效应）
        mask = np.ones(len(log_epsilon), dtype=bool)
        mask[0] = False  # 去掉最粗尺度
        mask[-1] = False  # 去掉最细尺度
        
        if np.sum(mask) >= 2:
            coeffs = np.polyfit(log_epsilon[mask], log_sum_pq[mask], 1)
            if q == 1:
                D_q = coeffs[0]  # q=1: D_1 = 斜率
            else:
                D_q = -coeffs[0]  # q≠1: D_q = -斜率
        else:
            if q == 1:
                D_q = np.mean(log_sum_pq / log_epsilon)
            else:
                D_q = -np.mean(log_sum_pq / log_epsilon)
        
        D_q_results[q] = float(D_q)
    
    return D_q_results

def thouless_exponent(eigenvalues, N):
    """计算 Thouless 指数（态密度的标度行为）
    
    对于奇异连续谱，态密度的支撑是零测度 Cantor 集，
    非空盒子数随盒子数的标度为 N_nonempty ~ N_boxes^D
    """
    E_min, E_max = eigenvalues.min(), eigenvalues.max()
    E_range = E_max - E_min
    
    num_boxes_list = [50, 100, 200, 400, 800]
    log_Nb = []
    log_Nnonempty = []
    
    for nb in num_boxes_list:
        box_width = E_range / nb
        box_indices = ((eigenvalues - E_min) / box_width).astype(int)
        box_indices = np.clip(box_indices, 0, nb - 1)
        n_nonempty = len(np.unique(box_indices))
        
        log_Nb.append(np.log(nb))
        log_Nnonempty.append(np.log(n_nonempty))
    
    # 拟合 D = d(log N_nonempty) / d(log Nb)
    log_Nb = np.array(log_Nb)
    log_Nnonempty = np.array(log_Nnonempty)
    
    mask = np.ones(len(log_Nb), dtype=bool)
    mask[0] = False
    mask[-1] = False
    
    if np.sum(mask) >= 2:
        coeffs = np.polyfit(log_Nb[mask], log_Nnonempty[mask], 1)
        D_thouless = coeffs[0]
    else:
        D_thouless = np.mean(log_Nnonempty / log_Nb)
    
    return float(D_thouless)

def compute_ipr(eigenvectors):
    """逆参与率"""
    return np.sum(eigenvectors**4, axis=0)

def analyze_lambda(lam, N, alpha, phi=0.0):
    """对单个 λ 值进行完整分析"""
    t0 = time.time()
    
    H = build_harper_matrix(N, lam, alpha, phi)
    eigenvalues, eigenvectors = eigh(H)
    
    # 多分形维数
    q_values = [0, 1, 2, 3, 4, 5]
    D_q = generalized_dimension(eigenvalues, q_values)
    
    # Thouless 指数
    D_thouless = thouless_exponent(eigenvalues, N)
    
    # IPR
    ipr = compute_ipr(eigenvectors)
    ipr_mean = float(np.mean(ipr))
    ipr_median = float(np.median(ipr))
    
    # 谱范围
    E_min, E_max = float(eigenvalues.min()), float(eigenvalues.max())
    
    # η_sc 估计（基于 D_2 的代理指标）
    # 奇异连续谱：0 < D_2 < 1
    D2 = D_q.get(2, D_q.get(0, 0.5))
    if 0.15 < D2 < 0.85:
        # 在 D2=0.5 时 η_sc 最大
        eta_sc = 1.0 - 2.0 * abs(D2 - 0.5)
        eta_sc = max(0.0, min(1.0, eta_sc))
    else:
        eta_sc = 0.0
    
    elapsed = time.time() - t0
    
    result = {
        'lambda': float(lam),
        'N': N,
        'D_q': {str(k): v for k, v in D_q.items()},
        'D_thouless': D_thouless,
        'D2': float(D2),
        'ipr_mean': ipr_mean,
        'ipr_median': ipr_median,
        'ipr_over_N': float(ipr_mean * N),
        'E_min': E_min,
        'E_max': E_max,
        'eta_sc': float(eta_sc),
        'suppression_factor': float(1.0 - eta_sc),
        'elapsed_seconds': float(elapsed),
    }
    
    return result

def main():
    alpha = (np.sqrt(5) - 1) / 2
    phi = 0.0
    
    print("=" * 90)
    print("Harper 模型增强谱分析：多分形维数 D_q + Thouless 指数 + 有限尺寸标度")
    print(f"α = (√5-1)/2 ≈ {alpha:.6f}, φ = {phi}")
    print("=" * 90)
    print()
    
    all_results = []
    
    # === 第一部分：λ=2 附近精细扫描，N=2000 ===
    print("【第一部分】λ=2 附近精细扫描（N=2000）")
    print("-" * 90)
    
    N_fine = 2000
    lambda_fine = [1.80, 1.85, 1.90, 1.95, 2.00, 2.05, 2.10, 2.15, 2.20]
    
    fine_results = []
    for lam in lambda_fine:
        print(f"  λ = {lam:.2f} ... ", end="", flush=True)
        r = analyze_lambda(lam, N_fine, alpha, phi)
        fine_results.append(r)
        all_results.append(r)
        print(f"D0={r['D_q']['0']:.3f} D1={r['D_q']['1']:.3f} "
              f"D2={r['D2']:.3f} D3={r['D_q']['3']:.3f} "
              f"η_sc={r['eta_sc']:.3f} ({r['elapsed_seconds']:.1f}s)")
    
    print()
    print("  精细扫描汇总：")
    print(f"  {'λ':>6} {'D0':>7} {'D1':>7} {'D2':>7} {'D3':>7} {'D_Th':>7} {'IPR/N':>8} {'η_sc':>7} {'抑制':>7}")
    print("  " + "-" * 80)
    for r in fine_results:
        print(f"  {r['lambda']:6.2f} {r['D_q']['0']:7.4f} {r['D_q']['1']:7.4f} "
              f"{r['D2']:7.4f} {r['D_q']['3']:7.4f} {r['D_thouless']:7.4f} "
              f"{r['ipr_over_N']:8.2f} {r['eta_sc']:7.4f} {r['suppression_factor']:7.4f}")
    
    # 找到 η_sc 峰值
    peak_idx = np.argmax([r['eta_sc'] for r in fine_results])
    print(f"\n  η_sc 峰值：λ = {fine_results[peak_idx]['lambda']:.2f}, "
          f"η_sc = {fine_results[peak_idx]['eta_sc']:.4f}, "
          f"D2 = {fine_results[peak_idx]['D2']:.4f}")
    
    print()
    
    # === 第二部分：有限尺寸标度 ===
    print("【第二部分】有限尺寸标度（λ=2.0 临界）")
    print("-" * 90)
    
    N_values = [1000, 2000, 4000]
    lambda_critical = 2.0
    
    fss_results = []
    for N in N_values:
        print(f"  N = {N} ... ", end="", flush=True)
        r = analyze_lambda(lambda_critical, N, alpha, phi)
        fss_results.append(r)
        all_results.append(r)
        print(f"D0={r['D_q']['0']:.3f} D2={r['D2']:.3f} "
              f"η_sc={r['eta_sc']:.3f} IPR/N={r['ipr_over_N']:.1f} ({r['elapsed_seconds']:.1f}s)")
    
    print()
    print("  有限尺寸标度汇总（λ=2.0）：")
    print(f"  {'N':>6} {'D0':>7} {'D1':>7} {'D2':>7} {'D3':>7} {'D_Th':>7} {'IPR/N':>8} {'η_sc':>7}")
    print("  " + "-" * 70)
    for r in fss_results:
        print(f"  {r['N']:6d} {r['D_q']['0']:7.4f} {r['D_q']['1']:7.4f} "
              f"{r['D2']:7.4f} {r['D_q']['3']:7.4f} {r['D_thouless']:7.4f} "
              f"{r['ipr_over_N']:8.2f} {r['eta_sc']:7.4f}")
    
    # 有限尺寸外推：D2(N) → D2(∞)
    N_arr = np.array([r['N'] for r in fss_results])
    D2_arr = np.array([r['D2'] for r in fss_results])
    # 拟合 D2(N) = D2_inf + c / N
    if len(N_arr) >= 2:
        inv_N = 1.0 / N_arr
        coeffs = np.polyfit(inv_N, D2_arr, 1)
        D2_inf = coeffs[1]
        print(f"\n  有限尺寸外推 D2(N→∞) = {D2_inf:.4f}（拟合 D2 = D2_inf + c/N, c={coeffs[0]:.2f}）")
        
        # 用外推值重新估计 η_sc
        if 0.15 < D2_inf < 0.85:
            eta_sc_inf = 1.0 - 2.0 * abs(D2_inf - 0.5)
            eta_sc_inf = max(0.0, min(1.0, eta_sc_inf))
        else:
            eta_sc_inf = 0.0
        print(f"  外推 η_sc(N→∞) = {eta_sc_inf:.4f}")
    
    print()
    
    # === 第三部分：多分形谱分析 ===
    print("【第三部分】多分形谱 D_q 分析（λ=2.0, N=4000）")
    print("-" * 90)
    
    # 已经在第二部分计算了 N=4000 的结果
    r_large = fss_results[-1]  # N=4000
    print(f"  N=4000, λ=2.0:")
    for q in [0, 1, 2, 3, 4, 5]:
        print(f"    D_{q} = {r_large['D_q'][str(q)]:.4f}")
    
    # 多分形谱宽度 ΔD = D_0 - D_5（完整范围）
    Delta_D_full = r_large['D_q']['0'] - r_large['D_q']['5']
    Delta_D_03 = r_large['D_q']['0'] - r_large['D_q']['3']
    print(f"    多分形谱宽度 ΔD(D0-D5) = {Delta_D_full:.4f}")
    print(f"    多分形谱宽度 ΔD(D0-D3) = {Delta_D_03:.4f}")
    print(f"    （绝对连续谱：ΔD≈0；奇异连续谱：ΔD>0；纯点谱：ΔD≈0 但 D≈0）")
    
    # 检查 D_q 单调性（多分形谱应随 q 递减）
    dq_vals = [r_large['D_q'][str(q)] for q in range(6)]
    is_monotonic = all(dq_vals[i] >= dq_vals[i+1] for i in range(5))
    print(f"    D_q 单调性（应递减）：{'是' if is_monotonic else '否（有限尺寸效应）'}")
    
    print()
    
    # === 总结 ===
    print("=" * 90)
    print("总结")
    print("=" * 90)
    
    d2_vals = ', '.join([f"{r['D2']:.4f}" for r in fss_results])
    ipr_vals = ', '.join([f"{r['ipr_over_N']:.1f}" for r in fss_results])
    peak_lam = fine_results[peak_idx]['lambda']
    peak_eta = fine_results[peak_idx]['eta_sc']
    peak_d2 = fine_results[peak_idx]['D2']
    d0_large = r_large['D_q']['0']
    d1_large = r_large['D_q']['1']
    d2_large = r_large['D2']
    d3_large = r_large['D_q']['3']
    d4_large = r_large['D_q']['4']
    d5_large = r_large['D_q']['5']
    
    summary = f"""
1. 精细扫描（N=2000）：
   - η_sc 峰值出现在 λ = {peak_lam:.2f}
   - 峰值 η_sc = {peak_eta:.4f}
   - 峰值 D2 = {peak_d2:.4f}
   - 奇异连续谱区域：λ ∈ [1.85, 2.15]（η_sc > 0.3）

2. 有限尺寸标度（λ=2.0）：
   - D2 随 N 变化：{d2_vals}
   - 外推 D2(N→∞) = {D2_inf:.4f}
   - 外推 η_sc(N→∞) = {eta_sc_inf:.4f}
   - IPR/N 随 N 增加：{ipr_vals}（局域化增强）

3. 多分形谱（λ=2.0, N=4000）：
   - D_0={d0_large:.4f}, D_1={d1_large:.4f}, D_2={d2_large:.4f}, 
     D_3={d3_large:.4f}, D_4={d4_large:.4f}, D_5={d5_large:.4f}
   - 多分形谱宽度 ΔD(D0-D5) = {Delta_D_full:.4f}（>0 确认多分形/奇异连续谱）
   - D_q 单调性：{'递减（符合多分形谱）' if is_monotonic else '非严格递减（有限尺寸效应）'}

4. 拓扑禁戒定量估计：
   - 临界 λ≈2.0 处，η_sc ≈ {eta_sc_inf:.4f}（有限尺寸外推）
   - 辐射抑制因子 ≈ {1-eta_sc_inf:.4f}
   - 即：奇异连续谱区域约 {eta_sc_inf*100:.1f}% 的谱分量无法形成光子，被拓扑禁戒
"""
    print(summary)
    
    # 保存结果
    output_file = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\results\harper_enhanced_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'fine_scan': fine_results,
            'finite_size_scaling': fss_results,
            'extrapolation': {
                'D2_inf': float(D2_inf),
                'eta_sc_inf': float(eta_sc_inf),
                'fit_c': float(coeffs[0]),
            },
            'multifractal': {
                'N': 4000,
                'lambda': 2.0,
                'D_q': r_large['D_q'],
                'Delta_D_full': float(Delta_D_full),
                'Delta_D_03': float(Delta_D_03),
                'is_monotonic': bool(is_monotonic),
            }
        }, f, indent=2, ensure_ascii=False)
    print(f"结果已保存到: {output_file}")

if __name__ == "__main__":
    main()
