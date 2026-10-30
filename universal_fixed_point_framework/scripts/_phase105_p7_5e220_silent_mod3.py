# -*- coding: utf-8 -*-
"""P7-5e-220 (⑳) 静默 mod 3 子列与原根自由度 —— 数值先证伪
按 §7.5 第 11 项 ⑳ 登记逐字翻译：
  RR1: 静默家族 m≡1 mod 3 子列 {2^(3t+1)+1} = {3,17,129,1025,8193,65537,...}
       —— 含种子 3 (m=1)、F_2=17 (m=4)、闭式常数 129 (m=7)、F_4=65537 (m=16)
  RR2: GG 族 m_k mod 3 = 2,0 交替 (k 奇→2, k 偶→0, 2^(3k+1) mod 3 主导)
  RR3: GG 族 m_k 永 ≠ 1 mod 3 —— 与静默家族 m≡1 mod 3 子列无交集
       (余项 3k-2≡1 mod 3 恒成立但与 m_k 本身 mod 3 脱钩)
  SS1: 3/5 是 mod 7 原根 (阶 6) → 2^a 3^b 5^c 遍历全部 mod 7 类 → ≡2 可解
       (⑫ CC2 的 35 解 <5e5); 固定 6·2^a 缺自由度仅 {6,5,3}
  SS2: 含 3 因子非必要 (100=2^2·5^2 无 3 也解)
  SS3: 6·2^a = 2^(a+1)·3 是缺 5 因子的 {2,3} 纯积, 5 因子加入恢复可解性
"""
import json, math

def gg_m(k):
    return (2 ** (3 * k + 1) + 21 * k - 2) // 7

def silent_val(t):
    """静默家族下标 m=3t+1 时的值 2^m+1 = 2^(3t+1)+1"""
    return 2 ** (3 * t + 1) + 1

def fermat(k):
    return 2 ** (2 ** k) + 1

def order_mod7(a):
    o, v = 1, a % 7
    while v != 1:
        v = (v * a) % 7
        o += 1
        if o > 8:
            break
    return o

res = {}

# RR1: 子列枚举 + 框架成员核对
rr1_vals = [silent_val(t) for t in range(0, 6)]
res['rr1_vals'] = rr1_vals  # expect [3,17,129,1025,8193,65537]
res['rr1_vals_ok'] = rr1_vals == [3, 17, 129, 1025, 8193, 65537]
res['rr1_members'] = {
    'seed_3_m1': silent_val(0) == 3,
    'F2_17_m4': silent_val(1) == fermat(2),
    'const_129_m7': silent_val(2) == 129,
    'F4_65537_m16': silent_val(5) == fermat(4),
}
res['rr1_sub_mod3'] = all((3 * t + 1) % 3 == 1 for t in range(0, 10))

# RR2: GG 族 mod 3 交替 (k 奇→2, k 偶→0)
res['rr2_vals'] = [gg_m(k) % 3 for k in range(1, 9)]  # expect [2,0,2,0,2,0,2,0]
res['rr2_alternate'] = all(gg_m(k) % 3 == (2 if k % 2 == 1 else 0) for k in range(1, 13))
# 机制: 7·m_k = 2^(3k+1)+21k−2, mod 3 → m_k ≡ 2^(3k+1)−2 mod 3
#   k 奇: 3k+1 偶 → 2^(3k+1)≡1 → m_k ≡ 1−2 ≡ 2
#   k 偶: 3k+1 奇 → 2^(3k+1)≡2 → m_k ≡ 2−2 ≡ 0
res['rr2_dominant'] = all((2 ** (3 * k + 1) - 2) % 3 == (2 if k % 2 == 1 else 0) for k in range(1, 13))

# RR3: GG 族永 ≠ 1 mod 3 (与静默子列无交集); 余项脱钩
res['rr3_no_intersect'] = all(gg_m(k) % 3 != 1 for k in range(1, 15))
res['rr3_remainder_mod3'] = all((3 * k - 2) % 3 == 1 for k in range(1, 15))
res['rr3_decouple'] = all(((3 * k - 2) % 3 == 1) and (gg_m(k) % 3 != 1) for k in range(1, 15))

# SS1: 3/5 是 mod 7 原根 (阶 6)
res['ss1_order3'] = order_mod7(3) == 6
res['ss1_order5'] = order_mod7(5) == 6
# 2^a 3^b 5^c 遍历 mod 7 全部非零类 (乘法群 (Z/7)^× = {1..6}, 因子均非 7 倍数故不含 0 类)
classes = {((2 ** a % 7) * (3 ** b % 7) * (5 ** c % 7)) % 7 for a in range(6) for b in range(6) for c in range(6)}
res['ss1_span'] = classes == set(range(1, 7))
# ≡2 可解: 2^a 3^b 5^c ≡ 2 mod 7 且值 <5e5 —— 复验 ⑫ CC2 口径 (a<9, b<5, c<5, nv>=1 → 登记 35 解)
sols_cc2 = []
for a in range(0, 9):
    for b in range(0, 5):
        for c in range(0, 5):
            v = (2 ** a) * (3 ** b) * (5 ** c)
            if v < 5 * 10 ** 5 and v % 7 == 2 and (v - 2) // 7 >= 1:
                sols_cc2.append((a, b, c, v))
res['ss1_sol_count_cc2'] = len(sols_cc2)
res['ss1_sols_ok'] = len(sols_cc2) == 35
# 扩展口径: v<5e5 全范围 (a≤18, b≤11, c≤8) —— 登记诚实边界注明
sols_full = []
for a in range(0, 19):
    for b in range(0, 12):
        for c in range(0, 9):
            v = (2 ** a) * (3 ** b) * (5 ** c)
            if v < 5 * 10 ** 5 and v % 7 == 2:
                sols_full.append((a, b, c, v))
res['ss1_sol_count_full'] = len(sols_full)
# 固定 6·2^a 缺自由度仅 {6,5,3}
res['ss1_fixed_6_2a'] = sorted({(6 * 2 ** a) % 7 for a in range(0, 7)}) == [3, 5, 6]
res['ss1_2_not_in_fixed'] = 2 not in {(6 * 2 ** a) % 7 for a in range(0, 7)}

# SS2: 含 3 因子非必要 (100=2^2·5^2 无 3 也解)
res['ss2_100'] = (100 % 7 == 2) and (100 == 2 ** 2 * 5 ** 2)

# SS3: 6·2^a = 2^(a+1)·3 缺 5 因子; 5 因子加入恢复可解性 (∃c: 6·2^a·5^c ≡ 2 mod 7)
res['ss3_pure23'] = all(6 * 2 ** a == 2 ** (a + 1) * 3 for a in range(0, 8))
res['ss3_fix5'] = all(any((6 * 2 ** a * 5 ** c) % 7 == 2 for c in range(0, 6)) for a in range(0, 8))

fails = [k for k, v in res.items() if v is False]
out = {'total_checks': len(res), 'fails': fails, 'all_pass': len(fails) == 0, 'res': res}
with open(r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase105_p7_5e220_silent_mod3.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
