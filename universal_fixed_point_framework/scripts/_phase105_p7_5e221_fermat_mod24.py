# -*- coding: utf-8 -*-
"""P7-5e-221 (㉑) 偶 Fermat 交集与 mod24 联合周期 —— 数值先证伪
按 §7.5 第 11 项 ⑳/㉑ 登记逐字翻译：
  TT1: m≡1 mod 3 子列 ∩ Fermat 数 = 偶 Fermat 全部 (3t+1=2^n ⟺ n 偶, t=(2^n-1)/3)
  TT2: 2^(2r) ≡ 1 mod 3 (偶 Fermat 指数落子列); 2^(2r+1) ≡ 2 mod 3 (奇 Fermat 不在)
  TT3: Fermat 命中点 t 间隔 = 2^(2r) (1,4,16,64,...); 129 是子列非 Fermat 成员 (m=7 非 2 幂)
  UU1: GG 族 m_k mod 24 两分支闭式 (k 奇 → 3k+2: 5,11,17,23; k 偶 → 3k-6: 0,6,12,18)
  UU2: mod 24 周期 8 (5,0,11,6,17,12,23,18 循环)
  UU3: CRT 合成 — mod 8 遍历 (II2) × mod 3 交替 (RR2) 联合于 lcm(3,8)=24
"""
import json, math

def fermat(k):
    return 2 ** (2 ** k) + 1

def gg_m(k):
    return (2 ** (3 * k + 1) + 21 * k - 2) // 7

res = {}

# TT1: 3t+1=2^n 有整数解 ⟺ n 偶（等价 3 | 2^n - 1，t=(2^n-1)/3）
tt1_ok = all((2 ** n - 1) % 3 == 0 if n % 2 == 0 else (2 ** n - 1) % 3 != 0 for n in range(0, 15))
res['tt1_iff'] = tt1_ok
res['tt1_t_vals'] = [(2 ** n - 1) // 3 for n in range(0, 13, 2)]  # 0,1,5,21,85,341,1365

# TT2: Fermat 指数奇偶性 ↔ m mod 3 类
tt2_ok = all(2 ** (2 * r) % 3 == 1 for r in range(0, 10)) and \
         all(2 ** (2 * r + 1) % 3 == 2 for r in range(0, 10))
res['tt2_parity'] = tt2_ok

# TT3: 命中点 t 间隔 = 2^(2r)
t_vals = [(2 ** n - 1) // 3 for n in range(0, 13, 2)]
gaps = [t_vals[i + 1] - t_vals[i] for i in range(len(t_vals) - 1)]
res['tt3_gaps'] = gaps  # expect [1,4,16,64,256,1024] = 2^0,2^2,2^4,2^6,2^8,2^10
res['tt3_gaps_ok'] = gaps == [2 ** (2 * r) for r in range(len(gaps))]
# 129: m=7=3*2+1 落子列、但 7 非 2 幂 → 129 非 Fermat 数
res['tt3_129_in_sub'] = (129 == 2 ** 7 + 1) and (7 % 3 == 1)
res['tt3_129_not_fermat'] = all(fermat(k) != 129 for k in range(0, 9))
res['tt3_129_mod3_vs_fermat_mod3'] = [129 % 3] + [fermat(k) % 3 for k in range(0, 7)]

# UU1: GG 族 mod 24 两分支
res['uu1_odd'] = all(gg_m(k) % 24 == (3 * k + 2) % 24 for k in [1, 3, 5, 7])
res['uu1_even'] = all(gg_m(k) % 24 == (3 * k - 6) % 24 for k in [2, 4, 6, 8])

# UU2: mod 24 周期 8
cycle = [gg_m(k) % 24 for k in range(1, 9)]
res['uu2_cycle'] = cycle  # expect [5,0,11,6,17,12,23,18]
res['uu2_period8'] = all(gg_m(k + 8) % 24 == gg_m(k) % 24 for k in range(1, 12))

# UU3: CRT 合成 — (m_k mod 8) = II2 序列, (m_k mod 3) = RR2 交替, lcm(3,8)=24
crt_ok = True
for k in range(1, 9):
    exp8 = [5, 0, 3, 6, 1, 4, 7, 2][k - 1]
    exp3 = 2 if k % 2 == 1 else 0
    if gg_m(k) % 8 != exp8 or gg_m(k) % 3 != exp3:
        crt_ok = False
res['uu3_crt'] = crt_ok
res['uu3_lcm'] = math.lcm(3, 8)

fails = [k for k, v in res.items() if v is False]
out = {'total_checks': len(res), 'fails': fails, 'all_pass': len(fails) == 0, 'res': res}
with open(r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase105_p7_5e221_fermat_mod24.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
