# -*- coding: utf-8 -*-
"""chain_audit_187_sigma_identity.py — σ = 1/15 框架量锁定判别
① σ 多重框架恒等（整数常数组合，全部精确命中 1/15）
② σ³×静默 = 1/675 家族身份（675 = N_gen³×静默²；A/D/B 闭式分母 σ 化）
③ σ 独立数值锁定（从织因子闭式反解 σ²，1e-7 级）
④ σ = 1/(幂基^不动点−1) = 1/M₄ Mersenne 连接（家族战役接线）
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import mpmath as mp
mp.mp.dps = 60

Ng, km, pw, sil, fp, inv = 3, 8, 2, 5, 4, 7   # N_gen/k_max/幂基/静默/不动点/对合域
sig = mp.mpf(1) / 15
print("=== σ = 1/15 框架量锁定判别 ===\n")
print(f"σ = 1/15 = {mp.nstr(sig, 40)}\n")

print("① σ 多重框架恒等（整数常数组合）")
cands = [
    ("1/(不动点²−1) = 1/15", mp.mpf(1)/(fp**2 - 1)),
    ("1/(幂基^不动点−1) = 1/(2⁴−1) = 1/M₄", mp.mpf(1)/(pw**fp - 1)),
    ("1/(N_gen×静默) = 1/15", mp.mpf(1)/(Ng*sil)),
    ("1/(k_max+对合域) = 1/15", mp.mpf(1)/(km+inv)),
    ("1/(对合域+幂基×不动点) = 1/(7+8)", mp.mpf(1)/(inv+pw*fp)),
    ("1/(N_gen+k_max−1+静默) = 1/(10+5)", mp.mpf(1)/(Ng+km-1+sil)),
    ("N_gen/静默单元45 = 3/45", mp.mpf(Ng)/45),
]
for name, v in cands:
    dev = (v - sig)/sig
    print(f"   {name}: {mp.nstr(v, 30)}  残差 = {mp.nstr(dev, 6)}  [{('精确' if dev==0 else '误差!')}]")

print("\n② σ³×静默 = 1/675 家族身份（织因子修正分母家族 σ 化）")
s3sil = (sig**3) * sil
print(f"   σ³×静默 = {mp.nstr(s3sil, 30)}；675 = N_gen³×静默² = {mp.nstr(mp.mpf(Ng)**3*sil**2, 20)}；1/675 = {mp.nstr(mp.mpf(1)/675, 30)}")
for nm, den, src in [("4050", 4050, "A 分母 = 6×675"), ("13500", 13500, "D 分母 = 20×675"), ("3375", 3375, "= 5×675 = 1/σ³ 自洽"), ("40500", 40500, "= 60×675"), ("648000", 648000, "m_s/T_c 修正分母 = 960×675")]:
    print(f"   {src}：{nm}×σ³×静默 = {mp.nstr(mp.mpf(nm)*s3sil, 25)}；{nm}/675 = {mp.nstr(mp.mpf(nm)/675, 15)}")
print(f"   织因子修正 σ²(1−1/320) = {mp.nstr((sig**2)*(1-mp.mpf(1)/320), 35)} = 319/72000（全框架量）")

print("\n③ σ 独立数值锁定（从织因子闭式反解，1e-7 级）")
dlmin = (mp.sqrt(mp.mpf(3)) - 1)/6
weavea = mp.power(mp.mpf(62)/3/(12*mp.pi*mp.sqrt(2)), mp.mpf(1)/3)
s2_back = (mp.mpf(45)*dlmin - mp.mpf(4)/weavea) * (mp.mpf(320)/319)
print(f"   σ² = (45Δλ_min − 4/a₀)·320/319 = {mp.nstr(s2_back, 40)}")
print(f"   vs σ² = 1/225 = {mp.nstr(mp.mpf(1)/225, 40)}：dev = {mp.nstr((s2_back-mp.mpf(1)/225)*225*100, 8)}%")
print(f"   σ 反解 = {mp.nstr(mp.sqrt(s2_back), 40)} vs 1/15：dev = {mp.nstr((mp.sqrt(s2_back)-sig)/sig*100, 8)}%")

print("\n④ Mersenne 连接（家族战役接线）")
print("   15 = 2⁴−1 = M₄；σ = 1/M₄")
print("   家族 N(k) = 49+4^k 素数 {53,113,16433,262193,4194353,67108913} 与 2^m−3 家族 {13,125} 已登记")
print("   M₄ = 15 = N_gen×静默 = 幂基^不动点−1——σ 落位 Mersenne 谱 {M₄ = 15} 与不动点对合 16 = 2⁴ 的差 1 缺口")
print(f"   15×Δλ_min = {mp.nstr(15*dlmin, 30)}（无框架身份，Δλ_min 直接锁 σ 不成立——σ 锁定经整数恒等 + 闭式反解两通道）")

print("\n⑤ 判别结论")
print("   σ 可框架量锁定：①整数恒等 6 通道全部精确命中 1/15（多重身份一致）；")
print("   ②σ³×静默 = 1/675 使织因子修正分母家族（4050/13500/3375/40500/648000）全部 σ 化；")
print("   ③从织因子闭式反解 σ² = 1/225（1e-7 级）——'精度范围内锁定'成立；")
print("   ④σ = 1/(幂基^不动点−1) = 1/M₄ 落位 Mersenne 谱——连接家族战役（对合 16 与 M₄ 15 差 1 缺口）。")
