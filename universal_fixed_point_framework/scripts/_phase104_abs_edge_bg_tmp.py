# -*- coding: utf-8 -*-
"""
Phase 104az-5: 吸收边标准物理背景建模（P1 严格比例裁决前置）
=============================================================
数据源: arXiv:2203.04319 (O'Hare et al.) Eq.21/22/24 + Table 1
目标: 对三颗有 Lp 定量值的高场星(J135141 773MG / J234605 706MG / J100356 668MG),
      量化"标准物理吸收边偏振背景"在观测波长窗口内的覆盖与谱形状,
      判断观测 Lp 中有多少可被标准物理吸收边解释, 残余是否仍支持 P1(1/8) 预言.

物理要点:
- Eq.24: 远离吸收边 Lp_astro(omega) ~ Omega_C^2 / omega^5 * sin^2(theta)
         -> 谱形状随波长: 蓝端强于红端 (omega^-5)
- Eq.21: Lp_astro = (delta_s/4)|2K0-K+-K-|sin^2(theta), 吸收边处特征增强
- Table 1: J135141 (353-705 MG) 吸收边列表(波长区间 A), 覆盖几乎全光学谱
- 吸收边能量: eps_nlmq = E_nlm(B) + Theta(m_f Omega_C)
- 边位置随 B 标度: 表 1 区间为 353-705 MG 对应, 其他星按 B 内插/外推
"""

import numpy as np

# ============ Table 1 吸收边数据 (J135141, B range 353-705 MG) ============
# (nl, q, lambda_min_Ang, lambda_max_Ang)  —— q=0,+-1 的边区间合并为覆盖范围
edges_J135141 = [
    ('2p_1',  -1, 5860.0, 6170.0),   # "5860+" → 上限按观测窗口截断估计
    ('3p_-1',  0, 4630.0, 5290.0),
    ('3p_0',   0, 5800.0, 6270.0),
    ('3p_1',   0, 4630.0, 5270.0),
    ('3d_0',   0, 6090.0, 6730.0),
    ('4d_-2',  0, 5420.0, 6480.0),
    ('4d_2',   0, 5420.0, 6440.0),
    ('4f_-2',  0, 3650.0, 4580.0),
    ('4f_2',   0, 3650.0, 4560.0),
]

B_ref_lo, B_ref_hi = 353.0, 705.0   # Table 1 对应的表面场范围

# ============ 三颗观测星 ============
# (星名, Kepler BHa_MG, Lp_obs_%, Lp_obs_err_%, 观测窗口 A, 来源)
stars = [
    ('J135141+5419', 773.0, 0.62, 0.40, (4000, 6500), 'SAO 2007'),
    ('J234605+3853', 706.0, 1.33, 0.20, (4200, 8400), 'SPOL/MMT'),
    ('J100356+0538', 668.0, 0.60, 0.16, (4200, 8400), 'Keck 2023'),
]

P1_pred = 0.058/8*100.0   # 0.725% (连续增强 5.8% / k_max=8)
print('P1 预言 Lp = %.3f%%  (连续增强 5.8%%/8)' % P1_pred)
print('='*110)

for name, B, Lp, Lp_err, (wlo, whi), src in stars:
    # --- 1. 吸收边按 B 线性标度 (表 1 区间 / B 范围 -> 每 MG 的边位置斜率) ---
    # 简化: 边位置与 B 近似线性 (二次 Zeeman 区内插; 诚实边界: 非线性未计入)
    f = (B - B_ref_lo) / (B_ref_hi - B_ref_lo)   # 0..1
    edge_win = []
    for nl, q, lam_lo, lam_hi in edges_J135141:
        # 表 1 的边区间对应 B_ref_lo..B_ref_hi; 对当前 B 内插
        elo = lam_lo + f * (lam_hi - lam_lo)
        ehi = lam_hi + f * (lam_hi - lam_lo)   # 简化: 区间宽度保守不变
        edge_win.append((nl, elo, ehi))

    # --- 2. 观测窗口内吸收边覆盖度 ---
    covered = []
    for nl, elo, ehi in edge_win:
        ov_lo = max(elo, wlo); ov_hi = min(ehi, whi)
        if ov_hi > ov_lo:
            covered.append((nl, ov_lo, ov_hi))
    tot_cover = sum(ehi-elo for _, elo, ehi in covered)
    win_width = whi - wlo
    cov_frac = tot_cover / win_width

    # --- 3. Eq.24 谱形状在窗口内的相对变化 (omega^-5 ∝ lambda^5) ---
    # Lp_astro(lambda) ~ lambda^5 (omega^-5), 相对蓝端归一
    lam_blue, lam_red = wlo, whi
    ratio = (lam_blue/lam_red)**5 if lam_red > 0 else 0.0   # 蓝端/红端比值
    # 窗口内平均相对强度 (归一化到蓝端=1)
    lam_grid = np.linspace(wlo, whi, 400)
    shape = (lam_grid / lam_blue)**5
    mean_shape = shape.mean()

    print(f'\n--- {name}  (B={B:.0f} MG, 观测 Lp={Lp:.2f}±{Lp_err:.2f}%, {src}) ---')
    print(f'  吸收边覆盖: {len(covered)} 个边特征落入窗口 {wlo}-{whi} Å, 覆盖率 {cov_frac*100:.1f}%')
    for nl, elo, ehi in covered:
        print(f'    {nl:8s}  q:  {elo:7.0f}-{ehi:7.0f} Å  (窗口内)')
    print(f'  Eq.24 幂律谱形: Lp ∝ λ^5 → 红端偏好, 红端/蓝端 = {1.0/ratio:.1f} 倍  窗口平均相对强度 = {mean_shape:.2f} (蓝端=1)')
    print(f'  → 标准物理背景: 吸收边覆盖 {(cov_frac*100):.0f}% 窗口(含重叠) → 谱结构应含密集边特征;')
    print(f'    幂律部分红端偏好 (λ^5), 红端贡献约为蓝端的 {1.0/ratio:.1f} 倍')

    # --- 4. 观/预言 vs 标准背景解释力 ---
    obs_pred = Lp / P1_pred
    print(f'  观/预言 = {obs_pred:.2f}   (Lp={Lp:.2f}% vs P1={P1_pred:.3f}%)')
    print(f'  ★ 若标准物理(吸收边)可解释全部 Lp → 需边特征贡献占窗口 {cov_frac*100:.0f}% 且特征强度密集;')
    print(f'    若吸收边解释部分 → 判别需看波长结构: P1(1/8) 预言近波长无关, 标准边特征有强波长结构')

print()
print('='*110)
print('综合判定:')
print('1. 三颗星吸收边覆盖 >140% 观测窗口(重叠) —— B>=100MG 时边几乎连续覆盖全光学谱(2203.04319 明示)')
print('2. 标准物理背景为"强波长结构化"偏振: 密集边特征 + 幂律红端偏好(λ^5); P1(1/8) 预言近波长无关')
print('3. 判别路径: (a) 分波长 bin 拟合 Lp(lambda) 谱, 扣除边特征+幂律后检验常数残余;')
print('   (b) 与 83-bin 谱 (J135141) 逐 bin 对照; (c) 多星 B 依赖一致性')
print('4. ★★ 2203.04319 对 J135141 83-bin 数据做 {轴子+天体物理+系统} 联合拟合:')
print('   best-fit A_astro = 0 —— 观测 Lp 谱的波长结构与标准吸收边模型不一致')
print('   (边特征在数据中不明显, 或 bin 太粗无法约束) —— 方向性支持 P1(偏振非吸收边主导)')
print('5. 诚实边界: 绝对标度 delta_s(线积分电子密度) 未定 → 无法绝对预测 Lp_astro 量级;')
print('   只能做谱形/覆盖率判别; 边位置线性标度为近似(二次 Zeeman 非线性未计入);')
print('   A_astro=0 也可能因数据噪声/bin 粗导致, 为方向性证据非判别')
