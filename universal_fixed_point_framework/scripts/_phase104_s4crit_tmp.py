# -*- coding: utf-8 -*-
"""
Phase 104az-42 (26.16j-90): "为什么 S_4" -- 静默临界层机制候选
S_4 = s^d_H = 1/15 (辫子静默层 = Ruelle zeta 极点处静默 -- 08_silence_unified_derivation §13-14)
判别: 3S_4=0.2 (命中 0.8) vs 3S_3=0.149 (0.851 不命中) vs 其他静默层
完整链: 0.8 = 1-N_active*S_4 = 1-N_active/B = (N_total-1)/N_total
机制: 完全静默 = 静默临界 (zeta 极点层) -- 三机制通道达静默临界
"""
import json, math, os

k_max, N_active, N_Weyl, N_gen = 8, 3, 4, 3
s = math.e**(-1)
d_H = math.log(15)
B = 2*k_max - 1
N_total = B // N_active

S = {1: s**1, 2: s**2, 3: s**N_active, 4: s**d_H, 5: s**5}

print('=== 静默层谱系 ===')
for k, v in S.items():
    print(f'S_{k} = {v:.6f}')

print()
print('=== "为什么 S_4" 判别 (3 通道各 σ 的 σ 候选) ===')
res = {'layers': {f'S_{k}': round(v,6) for k, v in S.items()}}
for k, v in S.items():
    thr = 1 - N_active*v
    hit = abs(thr - 0.8) < 1e-9
    print(f'3×S_{k} = {3*v:.4f} -> 1-3×S_{k} = {thr:.6f}  {"★ 精确命中 0.8" if hit else f"(差 {abs(thr-0.8)*100:.2f}%)"}')
    res[f'3S_{k}'] = {'thr': round(thr,6), 'hit_0.8': hit}

print()
print('=== 静默临界机制 (zeta 极点) ===')
print(f'ζ_R(s) = 1/(1-15e^-s) 极点 s = ln15 = d_H = {d_H:.6f}')
print(f'S_4 = s^d_H = e^-ln15 = 1/15 = 1/B -- 静默临界层 (ζ 发散点)')
print(f'S_3 = s^N_active = e^-3 = 0.0498 -- 主动层静默 (对象静默 -- 非临界)')
print(f'判别: 3S_4=0.2 精确命中 0.8; 3S_3=0.149 -> 0.851 不命中; S_1/S_2/S_5 均不命中')
print(f'→ 机制静默取静默临界层 (ζ 极点) 而非主动层/其他层')

print()
print('=== 完整链 ===')
v_final = 1 - N_active*S[4]
print(f'0.8 = 1 - N_active×S_4 = 1 - 3/15 = 1 - N_active/B = (N_total-1)/N_total = {v_final:.6f}')
print(f'S_4 与三代静默权重同源: c_2 = S_4 (charm 代 -- 辫子静默层 -- ζ 极点) -- 08_silence §14.1')

res['chain'] = {
    '0.8': round(1-N_active*S[4], 10),
    'identity': '1-N_active*S_4 = 1-N_active/B = (N_total-1)/N_total',
    'S4_mechanism': '静默临界层 (Ruelle ζ 极点 s=ln15=d_H 处静默 -- ζ 发散)',
    'S4_generation_identity': 'c_2 = S_4 (charm 代 -- 辫子静默 -- §14.1 三代静默权重)',
    'discriminant': '3S_4=0.2 精确命中 (vs 3S_3=0.149->0.851 不命中 -- S_4 胜出)',
    'verdict': '"为什么 S_4": 完全静默=静默临界 (ζ 极点层) -- 三机制通道在阈值区达静默临界 (相变) -- 总静默=N_active/B=3/15 -- 0.8 阈值'
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_phase104_s4crit_tmp.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print(f'已存盘: {out}')
