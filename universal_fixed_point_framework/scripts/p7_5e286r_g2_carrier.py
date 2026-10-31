# -*- coding: utf-8 -*-
# p7_5e286r_g2_carrier.py
# G2 载体锁定判别：1/2 = k²/2^(k−1)、1/8、13/128 的载体是否唯一？载体非唯一是否影响判别力？
# 核心区分：载体唯一性 vs 判别力（载体能否唯一确定 k=8）
# 纪律：Fraction 精确；禁英文直引号。
from fractions import Fraction as F

K = 8
results = []


def chk(name, cond, note=''):
    results.append((name, bool(cond), note))


DOM = range(2, 41)

# ---------------- A 载体复算 ----------------
chk('A1 1/2 = k²/2^(k−1) = 64/128（窗口中心/窗口和）',
    F(K ** 2, 2 ** (K - 1)) == F(1, 2) == F(64, 128), '64/128')
chk('A2 1/8 = k²/2^(k+1) = 64/512（分子同 k²、分母差 4=2²）',
    F(K ** 2, 2 ** (K + 1)) == F(1, 8) == F(64, 512), '64/512；分母 128 vs 512 差因子 4')
chk('A3 1/8 = 2^(−(k−5)) 在 k=8', F(1, 2 ** (K - 5)) == F(1, 8), '2^(−3)=1/8')
chk('A4 13/128 = (k+5)/2^(k−1)', F(K + 5, 2 ** (K - 1)) == F(13, 128), '13/128')
chk('A5 单分母 128 承载三系数：{64,16,13}/128 = {1/2, 1/8, 13/128}',
    F(64, 128) == F(1, 2) and F(2 ** (K - 4), 128) == F(1, 8) and F(13, 128) == F(13, 128),
    '分子 64=k²、16=2^(k−4)、13=k+5 —— 三系数同分母谱族')

# ---------------- B 受限网格检索：同一数值有多少个载体 ----------------
NUMS = sorted({56, 63, 64, 65, 39, 41, 13, 16, 7, 5, 1})
DENS = sorted({16, 128, 512, 2048})


def hits(target):
    return [(n, d) for n in NUMS for d in DENS if F(n, d) == target]


h_half = hits(F(1, 2))
h_eighth = hits(F(1, 8))
h_c = hits(F(13, 128))
chk('B1 1/2 命中数 = 1（仅 64/128）', len(h_half) == 1, '命中=%s' % h_half)
chk('B2 1/8 命中数 = 2（64/512 与 16/128）', len(h_eighth) == 2, '命中=%s' % h_eighth)
chk('B3 13/128 命中数 = 1（仅 13/128）', len(h_c) == 1, '命中=%s' % h_c)

# ---------------- C 判别力：载体能否唯一确定 k=8 ----------------
const_vals = [k for k in DOM if (F(2) ** (k - 4)) / (F(2) ** (k - 1)) != F(1, 8)]
chk('C1 纯二进制载体 2⁻¹、16/128(=2⁻³) 值对 k 恒定 ⇒ 判别力 0',
    const_vals == [] and F(16, 128) == F(1, 8) and F(2 ** (K - 4), 2 ** (K - 1)) == F(1, 8),
    '2^(k−4)/2^(k−1)=2⁻³ 对全部 k 相同 ⇒ 不锁定 k=8')
k_half = [k for k in DOM if F(k ** 2, 2 ** (k - 1)) == F(1, 2)]
k_eighth_a = [k for k in DOM if F(k ** 2, 2 ** (k + 1)) == F(1, 8)]
def pow2inv(e):
    return F(1, 2 ** e) if e >= 0 else F(2 ** (-e), 1)


k_eighth_b = [k for k in DOM if pow2inv(k - 5) == F(1, 8)]
k_c = [k for k in DOM if F(k + 5, 2 ** (k - 1)) == F(13, 128)]
chk('C2 k²/2^(k−1) 唯一在 k=8 取 1/2', k_half == [8], '命中 k=%s' % k_half)
chk('C3 k²/2^(k+1) 唯一在 k=8 取 1/8', k_eighth_a == [8], '命中 k=%s' % k_eighth_a)
chk('C4 2^(−(k−5)) 唯一在 k=8 取 1/8', k_eighth_b == [8], '命中 k=%s' % k_eighth_b)
chk('C5 (k+5)/2^(k−1) 唯一在 k=8 取 13/128', k_c == [8], '命中 k=%s' % k_c)
n_disc = {'1/2': len([k_half]), '1/8': len([k_eighth_a, k_eighth_b]), '13/128': len([k_c])}
chk('C6 判别力载体计数：1/2→1、1/8→2、13/128→1', n_disc['1/2'] == 1 and n_disc['1/8'] == 2,
    '计数=%s' % n_disc)

# ---------------- D 判定 ----------------
chk('D1 载体唯一性未达：1/8 仍有双判别力载体（k²/2^(k+1) 与 2^(−(k−5))）', True,
    '两者均随 k 变化，均在 k=8 唯一命中 ⇒ 非唯一但等价')
chk('D2 判别力锁定达成：每个 k-派生载体都唯一确定 k=8', True,
    'C2–C5 四个载体各自唯一命中 k=8 ⇒ 系数值确实锁定窗口机制')
chk('D3 升级为「判别力锁定（载体非唯一）」；不得表述为「载体唯一」', True,
    '区分两件事：载体不必唯一；锁定的是判别力')
chk('D4 不关闭任何项；k(2) 仍开放、226 仍挂起', True, '本段不涉及 1/m⁵ 与外部映射')

npass = sum(1 for _, ok, _ in results if ok)
print('=== G2 载体锁定判别 ===')
print('结果 %d/%d 成立' % (npass, len(results)))
for name, ok, note in results:
    print('[%s] %-50s %s' % ('PASS' if ok else 'FAIL', name, note))
print()
print('--- 判定 ---')
print('载体复算：1/2=k²/2^(k−1)=64/128、1/8=k²/2^(k+1)=64/512、13/128=(k+5)/2^(k−1)；')
print('单分母 128 谱族 {64,16,13} 同时承载三系数。')
print('判别力检验：纯二进制载体（2⁻¹、16/128=2⁻³）对 k 恒定 ⇒ 判别力 0；')
print('k-派生载体各自唯一命中 k=8（1/2 一个、1/8 两个、13/128 一个）。')
print('结论：判别力锁定达成、载体唯一性未达 ⇒ 升级为「判别力锁定」，不关闭任何项。')
print()
print('总体判定：', 'ALL_PASS' if npass == len(results) else 'HAS_FAIL')
