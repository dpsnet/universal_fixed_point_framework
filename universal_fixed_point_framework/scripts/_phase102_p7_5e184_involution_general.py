# -*- coding: utf-8 -*-
# P7-5e-184: 对合折叠 k_max 推广域检验
# 一般化 m ↦ K+1−m（K=2^p 候选族），检验发夹折叠是否框架通用结构
# 数据源：159（对合域常数 9=2^3+1、D_m=(9-2m)^2、镜像比 2^(9-2m)=2^sqrt(D_m)）、
#         161/162（发夹折叠三项、沉默位点 {4,5}=尖端位点）、121（δ∞=1/7-1/8 望远镜差分）、
#         129（闭式 1/B*=|m|/2+1/7+1/(7·2^|m|)）、169b/181（h(2)=7/64、h'(2)=13/600 候选）、
#         176-179（D=41/2000 五通道）、174e（镜像假设 D=-E）
# 纯代数/结构检验，无谱方法
import json, math

K_list = [4, 8, 16, 32]  # 2 的幂候选族；K=8 为已锁实例（2D 氢原子通道数）
out = {}

# ---------- A. 结构保持块（先验/代数恒等——通用性判别） ----------
A = {}
for K in K_list:
    p = int(round(math.log2(K)))
    center = (K + 1) / 2
    inv_range = list(range(1, K + 1))
    Dm = [(K + 1 - 2 * m) ** 2 for m in inv_range]
    # 镜像比（159 A 比值恒等）：尾巴(m)/尾巴(K+1−m) = 2^{K+1−2m}；指数绝对值 |K+1−2m| = √D_m（代数恒等）
    # 正确表述：比值指数 K+1−2m 与 D_m=(K+1−2m)² 的根匹配
    mirror_ok = all(abs(K + 1 - 2 * m) == math.sqrt(Dm[m - 1]) for m in inv_range)
    net_twist = sum(K + 1 - 2 * m for m in inv_range)
    # 望远镜差分 δ∞_K = 1/(K-1) - 1/K
    delta_inf = 1 / (K - 1) - 1 / K
    telescope = 1 / (K * (K - 1))
    # 域界自指：K+1 = 2^p + 1（2^m+1 家族成员）
    domain_edge = K + 1
    self_ref = (domain_edge == 2 ** p + 1)
    tip_pair = (K // 2, K // 2 + 1)
    # 闭式尾形式 1/(K-1) + 1/((K-1)·2^m)（K=8 → 1/7 + 1/(7·2^m)）
    A[K] = {
        'p': p,
        'involution': f'm ↦ {K+1}-m（中心 {center}）',
        'D_m_set': sorted(set(Dm)),
        'D_m_min_pair_D=1': tip_pair,
        'mirror_ratio_2^sqrtD': mirror_ok,
        'net_twist': net_twist,
        'delta_inf_1/(K-1)-1/K': delta_inf,
        'telescope_1/(K(K-1))': telescope,
        'delta_inf_exact': abs(delta_inf - telescope) < 1e-15,
        'tail_form': f'1/{K-1} + 1/({K-1}·2^m)',
        'domain_edge': domain_edge,
        'self_ref_2^p+1': self_ref,
    }

# ---------- B. 沉默位点模式（尖端指数 vs 域界——K 相关判别） ----------
B = {}
for K in K_list:
    p = int(round(math.log2(K)))
    tip_idx = (2 ** (p - 1), 2 ** (p - 1) + 1)   # 尖端最近对位置 (K/2, K/2+1) = (2^(p-1), 2^(p-1)+1)
    fam_val = (2 ** tip_idx[0] + 1, 2 ** tip_idx[1] + 1)  # 对应 2^m+1 家族成员
    domain_edge = K + 1
    B[K] = {
        'tip_indices': tip_idx,
        'family_values': fam_val,
        'domain_edge': domain_edge,
        'both_outside_domain': (fam_val[0] > domain_edge and fam_val[1] > domain_edge),
    }

# ---------- C. 框架量身份一般化（后验候选——K=8 复现校验） ----------
C = {}
for K in K_list:
    p = int(round(math.log2(K)))
    Np = K - 3                       # N' = K-3（K=8 → 5）
    Ck = (2 ** 2 + p ** 2) / (2 ** (K - 1))         # (2²+p²)/2^(K−1)：13=2²+3²、128=2⁷
    hk = (K - 1) / (2 ** (K - 2))                   # (K−1)/2^(K−2)：7/2⁶=7/64
    hpk = (2 ** 2 + p ** 2) / (3 * K * Np ** 2)     # (2²+p²)/(N_gen·K·(K−3)²)：13/(3·8·25)=13/600
    Dk = (K * Np + 1) / (2 ** (K // 2) * Np ** 3)   # (K(K−3)+1)/(2^(K/2)·(K−3)³)：41/(2⁴·125)=41/2000
    C[K] = {
        'N_prime_K-3': Np,
        'C_K=(4+p^2)/2^(K-1)': Ck,
        'h_K=(K-1)/2^(K-2)': hk,
        "h'_K=(4+p^2)/(3·K·(K-3)^2)": hpk,
        'D_K=(K(K-3)+1)/(2^(K/2)·(K-3)^3)': Dk,
        'E_K=-D_K': -Dk,
    }

# K=8 复现校验（候选常数精确复现；数值锁定值偏差登记）
repro = {
    'C_8==13/128': abs(C[8]['C_K=(4+p^2)/2^(K-1)'] - 13 / 128) < 1e-15,
    'h_8==7/64': abs(C[8]['h_K=(K-1)/2^(K-2)'] - 7 / 64) < 1e-15,
    "h'_8==13/600": abs(C[8]["h'_K=(4+p^2)/(3·K·(K-3)^2)"] - 13 / 600) < 1e-15,
    'D_8==41/2000': abs(C[8]['D_K=(K(K-3)+1)/(2^(K/2)·(K-3)^3)'] - 41 / 2000) < 1e-15,
}

# ---------- 综合判别 ----------
structure_universal = all(A[K]['mirror_ratio_2^sqrtD'] and A[K]['net_twist'] == 0
                          and A[K]['delta_inf_exact'] and A[K]['self_ref_2^p+1']
                          for K in K_list)
silence_universal_p3 = all(B[K]['both_outside_domain'] for K in [8, 16, 32])  # p>=3 保持
silence_K4_special = B[4]['both_outside_domain'] is False  # K=4：尖端指数 2 家族成员 5=域界

conclusion = {
    'structure_layer_universal': structure_universal,
    'structure_note': '对合/D_m 奇数平方/镜像比 2^√D_m/域界自指/望远镜差分/闭式尾形式/净扭转=0/尖端——全部 K=2^p 通用',
    'silence_pattern': {
        'universal_p_ge_3': silence_universal_p3,
        'K4_special': silence_K4_special,
        'note': 'p≥3 时尖端指数 2^(p-1)、2^(p-1)+1 的 2^m+1 成员全部域外（沉默）；K=8 为第一个 2^(p-1)>p 实例；K=4 时尖端指数 2 的成员 5=域界本身（非沉默）——沉默位点模式 p≥3 通用',
    },
    'identity_layer': {
        'K8_reproduce': repro,
        'all_K8_exact': all(repro.values()),
        'note': "C_K/h_K/h'_K/D_K/E_K=-D_K 后验 K 参数化——K=8 候选常数全部精确复现；K=4 退化（C_4=1、N'=1）；K=16/32 无物理实例数值验证（诚实边界）",
    },
    'verdict': '发夹折叠 = K=2^p 参数化通用结构族（结构层成立）；框架量身份族同时参数化（候选层）；最小非平凡实例 K=8；数值验证限于 K=8（无 K≠8 物理系统）',
    'degraded_K4': "C_4=1（整数退化）、N'_4=1——身份候选族最小非平凡 K = 8",
}

out = {'structure_block': A, 'silence_block': B, 'identity_block': C, 'conclusion': conclusion}

with open(r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e184_involution_general.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print('=== P7-5e-184 对合折叠 k_max 推广域检验 ===')
for K in K_list:
    d = C[K]
    hpk = d["h'_K=(4+p^2)/(3·K·(K-3)^2)"]
    print(f'[K={K}] D_m set: {A[K]["D_m_set"]} | mirror {A[K]["mirror_ratio_2^sqrtD"]} | twist {A[K]["net_twist"]} | delta_inf {A[K]["delta_inf_1/(K-1)-1/K"]} | self-ref {A[K]["self_ref_2^p+1"]}')
    print(f'        silence: indices {B[K]["tip_indices"]} fam {B[K]["family_values"]} vs edge {B[K]["domain_edge"]} outside={B[K]["both_outside_domain"]}')
    print(f'        C_K {d["C_K=(4+p^2)/2^(K-1)"]:.6f} | h_K {d["h_K=(K-1)/2^(K-2)"]:.6f} | hp_K {hpk:.6f} | D_K {d["D_K=(K(K-3)+1)/(2^(K/2)·(K-3)^3)"]:.6f}')
print('[structure universal]', structure_universal)
print('[K8 reproduce]', repro)
print('[verdict]', conclusion['verdict'])
