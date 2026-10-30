# -*- coding: utf-8 -*-
# P7-5e-185: 2^m 尾巴机制判别——"离散量子化"假说检验（159 E 推进）
# 本机（Windows）复算版，与云 VM 版逻辑一致；输出 json 到 scripts 目录
# 检验 A（Landau 计数排除）：若尾巴来自 Landau 能级/简并度量子化，其 m 依赖应
#   与 Landau 简并度 N_L(B*) = B*/(2π) 同型（幂律）；实际尾巴 1/(7·2^m) 是指数。
#   判别：N_L 的 ln-ln 斜率（幂律≈−1）vs tail 的半log 斜率（指数=−ln2）。
# 检验 B（离散区→连续极限）：尾巴区（m≤8）δ_cl·2^m→−1/7 恒定减半率（二进制计数指纹）。
# 数据源：闭式 129（1/B* = m/2 + 1/7 + 1/(7·2^m)，m=1 例外 +1/65）
import math, json, os, sys

def Bstar_inv(m):
    if m == 1:
        return m/2 + 1/7 + 1/(7*2**m) + 1/65   # 129 例外项
    return m/2 + 1/7 + 1/(7*2**m)

out = {'A_landau_vs_tail': {}, 'B_transition': {}, 'conclusion': {}}

# ---------- 检验 A ----------
ms = list(range(1, 41))
rows = []
for m in ms:
    invB = Bstar_inv(m)
    B = 1.0/invB
    N_L = B/(2*math.pi)                 # Landau 简并度（单位面积，自然单位）
    tail = 1/(7*2**m)                   # 尾巴项
    rows.append({'m': m, 'B*': B, 'N_L': N_L, 'tail': tail,
                 'tail_share': tail/invB})  # 尾巴占 1/B* 比例

# ln-ln 斜率（幂律判别）：ln N_L vs ln m（m=4..32 段）
loglog = []
for i in range(1, len(rows)):
    m1, m2 = rows[i-1]['m'], rows[i]['m']
    if m1 >= 4:
        dlnN = math.log(rows[i]['N_L']) - math.log(rows[i-1]['N_L'])
        dlnm = math.log(m2) - math.log(m1)
        loglog.append(dlnN/dlnm)
loglog_slope = sum(loglog[-8:])/8  # 尾部平均

# 半 log 斜率（指数判别）：ln tail vs m
semilog = []
for i in range(1, len(rows)):
    m1, m2 = rows[i-1]['m'], rows[i]['m']
    dlnT = math.log(rows[i]['tail']) - math.log(rows[i-1]['tail'])
    dm = m2 - m1
    semilog.append(dlnT/dm)
semilog_slope = sum(semilog)/len(semilog)

# 比值对照（m=1..8 离散区）
ratio_NL = [rows[i]['N_L']/rows[i+1]['N_L'] for i in range(7)]
ratio_tail = [rows[i]['tail']/rows[i+1]['tail'] for i in range(7)]

out['A_landau_vs_tail'] = {
    'N_L(m) ln-ln slope (幂律判别，期望≈−1)': round(loglog_slope, 4),
    'tail(m) semilog slope (指数判别，期望=−ln2≈−0.6931)': round(semilog_slope, 4),
    'N_L 相邻比 (m=1..8)': [round(v, 3) for v in ratio_NL],
    'tail 相邻比 (m=1..8)': [round(v, 3) for v in ratio_tail],
    'tail_share(m=1..8) 尾巴占 1/B* 比例': [round(r['tail_share'], 4) for r in rows[:8]],
    'tail_share(m=33)': round(rows[32]['tail_share'], 12),
    '结论': 'Landau 简并度 N_L ∝ 1/m 幂律（ln-ln 斜率≈−1）；尾巴 ∝ 2^−m 指数（半log 斜率≈−ln2）——'
            '两者 m 依赖完全不同型 → "尾巴 = Landau 能级/简并度计数"数值排除',
}

# ---------- 检验 B ----------
# δ_cl(m) = (m/2+1/7) − 1/B* = −1/(7·2^m)（m≥2 闭式恒等，129）
trans = []
for m in ms:
    invB = Bstar_inv(m)
    delta_cl = (m/2 + 1/7) - invB
    trans.append({'m': m, 'delta_cl': delta_cl, 'delta_cl_x_2m': delta_cl*2**m,
                  'delta_cl_x_m': delta_cl*m})
out['B_transition'] = {
    'delta_cl·2^m (m=1..8，尾巴区指纹→−1/7 恒定减半率)': [round(t['delta_cl_x_2m'], 6) for t in trans[:8]],
    'delta_cl·m (m=9..16)': [round(t['delta_cl_x_m'], 6) for t in trans[8:16]],
    'delta_cl·m (m=17..32)': [round(t['delta_cl_x_m'], 6) for t in trans[16:32]],
    '解读': 'δ_cl = (m/2+1/7) − 1/B* = −1/(7·2^m)（m≥2 闭式恒等）→ δ_cl·2^m = −1/7 精确常数：'
            '尾巴的 2 进指纹 = "每增加一个通道，尾巴精确减半"（恒定减半率 2——二进制计数特征）；'
            'm≥13 后 2^−m 指数级不可见（δ_cl·m→0），尾巴区结束、幂律渐近区接管（174e δ=1/56−C/m−...）',
}

out['conclusion'] = {
    '离散量子化假说精确化': '部分成立——"离散性"真（有限通道 8=2^3、指数衰减 2^−m、2 进计数），'
            '但机制是代数/组合（对合折叠、域界自指 K+1=2^p+1、家族 2^m+1），非 Landau 能级物理（检验 A 排除）',
    '为何 2 进（159 E 推进）': 'm 通道轴以二进制组织（通道数 2^p、静默单元 2^3×k+1、家族 2^m+1、对合域 K+1=2^p+1 自指、'
            '184 的 K=2^p 族通用）——"离散量子化"即"二进制量子化"：可数通道按 2 的幂组织、边界效应按 2 的幂衰减',
    '判别检验设计': '检验 A（Landau 计数排除）已完成；检验 B（离散区指纹）已完成；检验 C（2 进计数谱：2^m+1 家族 3/5/9/17/33/65 '
            '在闭式中的角色构成完整计数谱）与检验 D（域界穿透：m=9 尾巴消失，110/111 已登记）可后续推进',
}

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '_phase102_p7_5e185_tail_quantization.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print('=== P7-5e-185 2^m 尾巴机制判别（离散量子化假说）本机复算 ===')
print('[A] Landau N_L ln-ln 斜率:', round(loglog_slope, 4), '(幂律≈−1)')
print('[A] tail 半log 斜率:', round(semilog_slope, 4), '(指数=−ln2=−0.6931)')
print('[A] N_L 相邻比:', [round(v,3) for v in ratio_NL])
print('[A] tail 相邻比:', [round(v,3) for v in ratio_tail])
print('[B] δ_cl·2^m (m=1..8):', [round(t['delta_cl_x_2m'],6) for t in trans[:8]], '→ −1/7?')
print('[B] δ_cl·m (m=17..32):', [round(t['delta_cl_x_m'],6) for t in trans[16:32]])
print('[结论]', out['conclusion']['离散量子化假说精确化'])
print('json ->', out_path)
