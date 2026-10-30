# -*- coding: utf-8 -*-
"""Phase 103f: 转化映射定量化——η_comp(B) 曲线重算 + η_line(B) + ε_trans(B)
1) 氢 n 波函数径向 tail（r > C*l_B），l 分波偶极权重加权
2) 45 MG 验证复现 η_comp=0.530（先证伪再证明）
3) 外推 B=2.5/5/20/45/100/156/235 MG
4) 合并 η_line(B)，对比观测 blue_calres 分档，算 ε_trans(B)
"""
import math

# 框架常数
C = 3.03                      # 环绕循环最小密度半径（P3b-2 第一性定标 p=0.99）
B_CRIT1_MG = 2350.0            # n=1: l_B = a0 的场强（485/√(B[T]) 标度验证：10MG→15.33 a0）
ETA_SIGMA = 0.14871727075589897   # sigma 填充 45MG（T=12000K），B 依赖弱，取定值
B_ION = {'Halpha': 261.0, 'Hbeta': 147.0, 'Hgamma': 94.0, 'Hdelta': 65.0, 'Heps': 48.0}

def laguerre(n, k, x):
    """广义 Laguerre L_n^k(x)（递归，数值稳定版）"""
    if n == 0:
        return 1.0
    if n == 1:
        return 1.0 + k - x
    l0, l1 = 1.0, 1.0 + k - x
    for i in range(2, n + 1):
        l2 = ((2 * i - 1 + k - x) * l1 - (i - 1 + k) * l0) / i
        l0, l1 = l1, l2
    return l1

def radial_tail(n, l, R_L):
    """氢 (n,l) 径向波函数 r>R_L 的积分概率（a0=1 单位）"""
    # R_nl(r) = N * exp(-r/n) * (2r/n)^l * L_{n-l-1}^{2l+1}(2r/n)
    # 概率密度 = |R|^2 * r^2
    norm2 = (2.0 / n) ** 3 * math.factorial(n - l - 1) / (2.0 * n * math.factorial(n + l))
    # 积分 r: R_L -> inf，变量变换 r = R_L + t/(1-t)，t: 0->1
    # 注意：用 log 计算避免溢出
    def prob_density(r):
        z = 2.0 * r / n
        L = laguerre(n - l - 1, 2 * l + 1, z)
        log_R2 = math.log(norm2) + (-2.0 * r / n) + 2.0 * l * math.log(z) + 2.0 * math.log(abs(L)) if L != 0 else -1e6
        return math.exp(log_R2) * r * r
    N = 2000
    total = 0.0
    for i in range(N):
        t = (i + 0.5) / N
        r = R_L + t / (1.0 - t)
        jac = 1.0 / ((1.0 - t) ** 2)
        total += prob_density(r) * jac
    return total / N

def l_weights(n_line):
    """Hβ 上态 l 分波偶极权重（论文 P3b-2 Hbeta_l_decomp）"""
    # 对 n=4（Hβ 上态）：l=0/1/2 权重 + tail 都在 45MG 已给
    if n_line == 4:
        return [(0, 0.01913875595240874), (1, 0.21531100446459822), (2, 0.765550239582993)]
    return None

def eta_comp(B_mg, n):
    """η_comp = 各 l 加权 tail 分数 @ B"""
    lB = math.sqrt(B_CRIT1_MG / B_mg)   # l_B 单位 a0
    R_L = C * lB
    ws = l_weights(n)
    if ws is None:
        return None
    tot = 0.0
    for l, w in ws:
        tot += w * radial_tail(n, l, R_L)
    return tot

def eta_3g(B_mg, line):
    """第三门：B_ion 阈值以上指数禁戒（中场以下=0）"""
    Bt = B_ION[line]
    if B_mg < Bt:
        return 0.0
    # η_3g = 1 - exp(-epsilon)；epsilon 取 (B/Bt - 1) 简单形式（论文 §3.5 口径待查，先给占比）
    eps = (B_mg / Bt) - 1.0
    return 1.0 - math.exp(-eps)

# ========== 验证 45 MG Hβ ==========
print('=== 验证：45 MG Hβ η_comp（应≈0.530）===')
print('eta_comp(45MG,Hb) =', eta_comp(45.0, 4))
print('Hbeta l 分解（45MG）：')
for l, w in l_weights(4):
    lB = math.sqrt(B_CRIT1_MG / 45.0)
    R_L = C * lB
    print('  l=%d w=%.4f tail=%.4f' % (l, w, radial_tail(4, l, R_L)))

# ========== B 依赖 ==========
print()
print('=== η_comp(Hβ) vs B ===')
B_PTS = [2.5, 5.0, 10.0, 20.0, 45.0, 100.0, 156.0, 235.0]
for B in B_PTS:
    print('B=%6.1f MG  l_B=%.2f a0  eta_comp(Hβ)=%.4f' % (B, math.sqrt(B_CRIT1_MG / B), eta_comp(B, 4)))

# ========== 合并 η_line(Hβ, B) vs 观测增强 ==========
print()
print('=== 转化映射：观测连续谱增强(blue_calres) vs η_line(Hβ) vs ε_trans ===')
# 观测增强（分档中位）：{B_rep: blue_calres}
OBS = [(2.5, 0.0385), (5.0, 0.0548), (20.0, 0.0843), (100.0, 0.1404)]   # 分档中位（可信样本）
for B, obs in OBS:
    ec = eta_comp(B, 4)
    e3 = eta_3g(B, 'Hbeta')
    el = 1.0 - (1.0 - ec) * (1.0 - ETA_SIGMA) * (1.0 - e3)
    # 观测增强是 dex（log10），转为流量增强比
    enh_ratio = 10.0 ** obs - 1.0
    eps_trans = enh_ratio / el if el > 0 else float('nan')
    print('B=%5.1f MG | blue_calres=%+.4f dex (enh %.1f%%) | η_comp=%.3f η_3g=%.3f η_line=%.3f | ε_trans=%.3f'
          % (B, obs, enh_ratio * 100, ec, e3, el, eps_trans))
