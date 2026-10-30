# p7_5e262_triad.py - ① D/E 镜像对 b 唯一性+符号方向  ② k(2) 档位扫描独立通道  ③ 5³=2⁷−3 塔锚差分身份
import json, numpy as np

SRC = r'C:\Users\dps_n\DoubaoWork\chats\2026-10-07\new-chat\p7_5e260ae_e0pts.json'
pts = json.load(open(SRC, encoding='utf-8'))
out = {}

# ---------- ③ 先做：5³=2⁷−3 塔锚差分身份（纯代数） ----------
out['tower'] = {}
kmax = 8
out['tower']['5^3=2^7-3'] = (125 == 2**7 - 3)
out['tower']['2000=2^4*5^3=2^4*(2^7-3)'] = (2000 == 16*125 and 125 == 128-3)
out['tower']['b^3 vs 2^(kmax-1)-3 sweep'] = {}
for b in range(1, 10):
    val = b**3
    target = 2**(kmax-1) - 3
    out['tower']['b^3 vs 2^(kmax-1)-3 sweep'][f'b={b}'] = {
        'b3': val, 'target': target, 'match': val == target,
        'rel_dev': (val-target)/target if target else None}
# 分母家族塔锚谱系
fam = {
    '128': 128, '2048': 2048, '2000': 2000, '272': 272, '293': 293, '727': 727,
}
out['tower']['denominator_family'] = {
    '128 = 2^7': 128 == 2**7,
    '2048 = 2^11 = 2^4*2^7': 2048 == 16*128,
    '2000 = 2^4*(2^7-3)': 2000 == 16*125,
    '272 = 2^4*(2^4+1) = 16*17': 272 == 16*17,
    '293 = (2^11+3)/7': 293*7 == 2048+3,
    '727 = 56*13-1': 727 == 56*13-1,
}
# 2^4*(2^j ± small) 家族命中枚举
hits = []
for j in range(3, 9):
    for sgn in (+1, -1):
        for small in (1, 3, 5, 7):
            v = 16 * (2**j + sgn*small)
            if v in fam.values():
                hits.append((v, j, sgn, small))
out['tower']['2^4*(2^j±small) family hits'] = hits

# ---------- ① D/E 镜像对 b 唯一性 + 符号方向（纯代数） ----------
out['mirror'] = {}
D_star, E_star = 41/2000, 39/2000
b_sweep = {}
for b in range(1, 10):
    Dp = (8*b + 1) / (16 * b**3)
    Em = (8*b - 1) / (16 * b**3)
    b_sweep[f'b={b}'] = {
        'D+=(8b+1)/(16b^3)': Dp, 'dev_D_pct': (Dp-D_star)/D_star*100,
        'E-=(8b-1)/(16b^3)': Em, 'dev_E_pct': (Em-E_star)/E_star*100,
    }
out['mirror']['b_sweep'] = b_sweep
# 符号方向：41 配 +1 vs 配 −1
out['mirror']['sign_direction'] = {
    'D with +1 (41/2000)': abs(41/2000 - D_star)/D_star*100,
    'D with -1 (39/2000)': abs(39/2000 - D_star)/D_star*100,
    'E with +1 (41/2000)': abs(41/2000 - E_star)/E_star*100,
    'E with -1 (39/2000)': abs(39/2000 - E_star)/E_star*100,
}
# b 的幂唯一性：D=(8*5+1)/(16*5^k), k∈{1,2,3,4}
p_sweep = {}
for k in (1, 2, 3, 4):
    Dk = 41 / (16 * 5**k)
    p_sweep[f'k={k}'] = {'D': Dk, 'dev_D_pct': (Dk-D_star)/D_star*100}
out['mirror']['b_power_sweep'] = p_sweep

# ---------- ② k(2) 档位扫描独立通道 ----------
def f_model(x):
    return 0.5*x - np.sqrt(0.5*x)
def g_inf(x):
    return -0.125 + np.sqrt(0.5*x)/8 + x/16

mm = np.array([p['mm'] for p in pts], dtype=float)
x  = np.array([p['x'] for p in pts], dtype=float)
E0 = np.array([p['E0'] for p in pts], dtype=float)
u  = x - 2.0

def design(M, U):
    n = len(M)
    cols = []
    # u^k/m²  k=1..6
    for k in range(1, 7): cols.append(U**k / M**2)
    # 1/m³, u^k/m³ k=1..4
    cols.append(1/M**3)
    for k in range(1, 5): cols.append(U**k / M**3)
    # 1/m⁴, u^k/m⁴ k=1..5
    cols.append(1/M**4)
    for k in range(1, 6): cols.append(U**k / M**4)
    # 1/m⁵, u^k/m⁵ k=1..3, u⁵/m⁵
    cols.append(1/M**5)
    for k in range(1, 4): cols.append(U**k / M**5)
    cols.append(U**5 / M**5)
    # 1/m⁶
    cols.append(1/M**6)
    return np.column_stack(cols)

r_full = E0*mm - f_model(x) - g_inf(x)/mm - (7/64)/mm**2
A_full = design(mm, u)
coef_full, res_full, *_ = np.linalg.lstsq(A_full, r_full, rcond=None)
k2_full = coef_full[17]   # 1/m⁵ 列 index 17

mcut_list = [32, 48, 64, 96, 128, 192, 256, 384, 512, 768, 1024]
k2_scan = {}
for mc in mcut_list:
    sel = mm >= mc
    m_ = mm[sel]
    u_ = u[sel]
    A_ = design(m_, u_)
    r_ = r_full[sel]
    c_, *_ = np.linalg.lstsq(A_, r_, rcond=None)
    k2_scan[f'm>={mc}'] = {'k2': float(c_[17]), 'dev_vs_full_pct': (c_[17]-k2_full)/k2_full*100}

# 全链对比候选
cand = {'-3/272': -3/272, '-11/997': -11/997, '-13/1178': -13/1178, '-7/634': -7/634, '-5/453': -5/453}
cand_dev = {k: (v-k2_full)/k2_full*100 for k, v in cand.items()}

out['k2'] = {
    'k2_full': float(k2_full),
    'scan': k2_scan,
    'candidate_dev_pct': cand_dev,
}

# 完整输出
with open(r'E:\workspace\hyper-resolution\p7_5e262_triad_result.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print('k2_full:', k2_full)
print('scan:', json.dumps(k2_scan, indent=1))
print('cand_dev:', json.dumps(cand_dev, indent=1))
print('b_sweep b=5:', json.dumps(b_sweep['b=5'], indent=1))
print('sign:', json.dumps(out['mirror']['sign_direction'], indent=1))
print('p_sweep:', json.dumps(p_sweep, indent=1))
print('tower hits:', hits)
print('tower keys:', {k: v for k, v in out['tower'].items() if k != 'b^3 vs 2^(kmax-1)-3 sweep'})
