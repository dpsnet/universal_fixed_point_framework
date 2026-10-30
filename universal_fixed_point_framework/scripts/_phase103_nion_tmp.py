# -*- coding: utf-8 -*-
"""Phase 103k: v2 参数第一性化——n_ion = Landau 化有效电离阈
η_comp(B, n)：氢 n 态横向 tail 被 Landau 化截断的比例（简并加权）
n_ion_eff(B) = 满足 η_comp > 阈值的有效束缚态上限（并入连续谱）
检验：45MG 下 n_ion_eff 是否 ≈ 6（v2 模型参数）
"""
import math

C = 3.03
B_CRIT1_MG = 2350.0

def laguerre(n, k, x):
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
    norm2 = (2.0 / n) ** 3 * math.factorial(n - l - 1) / (2.0 * n * math.factorial(n + l))
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

def eta_comp_degen(B_mg, n):
    """简并加权（(2l+1)/n²）的 η_comp——通用 n"""
    lB = math.sqrt(B_CRIT1_MG / B_mg)
    R_L = C * lB
    tot = 0.0
    for l in range(0, n):          # l = 0..n-1
        w = (2.0 * l + 1) / (n * n)
        tot += w * radial_tail(n, l, R_L)
    return tot

print('=== η_comp（简并加权，通用 n）vs B ===')
B_PTS = [10.0, 20.0, 45.0, 100.0, 156.0, 235.0]
print('n\\B(MG)', end='')
for B in B_PTS:
    print('%8.0f' % B, end='')
print()
for n in range(2, 13):
    print('n=%2d   ' % n, end='')
    for B in B_PTS:
        print('%8.4f' % eta_comp_degen(B, n), end='')
    print()

print()
print('=== n_ion_eff(B) = 最小 n 使 η_comp > 阈值（有效束缚态上限）===')
print('B(MG) | th=0.5 | th=0.7 | th=0.9')
for B in B_PTS:
    row = []
    for th in (0.5, 0.7, 0.9):
        n_eff = None
        for n in range(2, 20):
            if eta_comp_degen(B, n) > th:
                n_eff = n
                break
        row.append(str(n_eff) if n_eff else '>19')
    print('%6.0f | %s | %s | %s' % (B, row[0], row[1], row[2]))

print()
print('=== 对照：v2 模型 n_ion=6（T=12000K 配置）——哪个 B 下成立？ ===')
for B in B_PTS:
    e6 = eta_comp_degen(B, 6)
    print('B=%6.0f MG: η_comp(n=6)=%.4f  (n=6 并入连续谱需 η_comp 高)' % (B, e6))

print()
print('=== 对照：论文 B_ION 阈值序列（第三门，各线上态 n）===')
B_ION = {'Halpha': 261.0, 'Hbeta': 147.0, 'Hgamma': 94.0, 'Hdelta': 65.0, 'Heps': 48.0}
for line, Bt in B_ION.items():
    n_upper = {'Halpha': 2, 'Hbeta': 3, 'Hgamma': 4, 'Hdelta': 5, 'Heps': 6}[line]
    print('%s (n上=%d): B_ion=%6.1f MG | η_comp@B_ion = %.4f' % (line, n_upper, Bt, eta_comp_degen(Bt, n_upper)))
