# -*- coding: utf-8 -*-
# 104az-229 m_p/m_e 合并闭式定案 + 小数部 371/2430 唯一性负控（pyenv 3.11.8）
# 背景：m_p/m_e = 1836（整数部闭式 3·7·8·11−3·4，dev −0.008%，153/289）+ 小数部 371/2430（dev +0.00096%，153）
# 本步：1) 合并闭式 1836+371/2430 全值 dev + CODATA σ 判据
#       2) 小数部候选唯一性扫描（q≤6000 全部有理数，0.002% 窗口，371/2430 排名）
#       3) 全框架量分解核验（371=7×53、2430=3⁵×2×5）与候选竞争分析
m_pe = 1836.15267343   # CODATA
frac_371 = 371/2430
closed = 1836 + frac_371

print("=== 1. 合并闭式定案 ===")
print(f"m_p/m_e 实测    = {m_pe}")
print(f"1836+371/2430   = {closed:.12f}")
dev_abs = closed - m_pe
dev_rel = dev_abs / m_pe
print(f"全值 dev = {dev_abs:+.3e} 绝对（相对小数部 {dev_abs/frac_371:+.3e}）")
print(f"全值相对 dev = {dev_rel:+.3e}（{dev_rel*100:+.6f}%）")
# CODATA m_p/m_e 相对不确定度 ~1.6e-10（g-factor 测量链）→ 绝对 ≈ 2.94e-7
sigma_abs = 1836.15267343*1.6e-10
print(f"CODATA σ（1.6e-10 相对）≈ {sigma_abs:.3e} 绝对 → 全值 σ 数 = {dev_abs/sigma_abs:.2f}σ")
print(f"整数部 1836 dev = {(1836-m_pe)/m_pe:+.3e}（{1836-m_pe:+.6f} 绝对）")

print()
print("=== 2. 小数部候选唯一性扫描（q ≤ 6000，窗口 ±0.002%）===")
target = m_pe - 1836  # 0.15267343
hits = []
for q in range(1, 6001):
    p = round(target*q)
    if p <= 0: continue
    v = p/q
    d = (v - target)/target
    if abs(d) <= 2e-5:
        hits.append((abs(d), p, q, v))
hits.sort()
print(f"窗口内候选总数 = {len(hits)}")
for i, (d, p, q, v) in enumerate(hits[:12]):
    print(f"  #{i+1} dev {d:+.3e}  {p}/{q} = {v:.9f}")
# 371/2430 的排名
rank = next((i+1 for i,(d,p,q,v) in enumerate(hits) if p==371 and q==2430), None)
print(f"371/2430 在窗口内偏差排名 = {rank}（共 {len(hits)}）")

print()
print("=== 3. 全框架量分解核验 ===")
print("371 = 7×53 ?", 7*53 == 371, "（53 = 7²+2² 素数身份，早期登记；371=7×(45+8) 镜像家族 153）")
print("2430 = 3⁵×2×5 ?", 3**5*2*5 == 2430, "（N_gen⁵×幂基×静默，全乘框架量）")
# 竞争候选的全框架检查：扫描窗口内其他候选，看是否有更优全框架分解
print("窗口内竞争候选（前 6 个）全框架性：")
M12 = {2,3,4,5,7,8,15,16,21,42,49,105}
def frame_int(n):
    # 简单乘法型：n 是否 = M12 元素的幂乘积（允许 11、13、29、53 扩展素域幂）
    primes = [2,3,5,7,11,13,29,53]
    x = n
    for p in primes:
        while x % p == 0:
            x //= p
    return x == 1
for d, p, q, v in hits[:6]:
    print(f"  {p}/{q}: 分子框架型={frame_int(p)}（{p}=?, 素分解），分母框架型={frame_int(q)}")
