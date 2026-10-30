# -*- coding: utf-8 -*-
"""chain_audit_185_msTc_weave.py — 织³ vs 织a 判别（m_s/T_c 代数身份通道）
104az-99 判定"F_np/m_s/T_c 双检验均无法区分"——复查：
m_s/T_c 代数身份（104az-80 准精确，独立于 a₀）：m_s/T_c = 5Δλ_min − 319/648000
m_s = Λ·(C_F/2)² 候选（104az-72）+ T_c = a₀Λ（D9）→ m_s/T_c = 4/(9a₀) → a₀ 反解
若此反解精确命中织a（0.72913527），则 m_s/T_c 通道有判别力。
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import mpmath as mp
mp.mp.dps = 60

d3 = mp.sqrt(mp.mpf(3))
dlmin = (d3 - 1) / 6          # Δλ_min = (√3−1)/6
sigma = mp.mpf(1)/15          # σ = 1/15
weave3 = mp.mpf(729)/1000     # 织³ = (9/10)³ = N_gen⁶/10³
weavea = mp.power(mp.mpf(62)/3 / (12*mp.pi*mp.sqrt(2)), mp.mpf(1)/3)  # d_eff=62/3 的 a₀

print("=== 织³ vs 织a 判别：m_s/T_c 代数身份通道 ===\n")
print(f"Δλ_min = (√3−1)/6 = {mp.nstr(dlmin, 30)}")
print(f"织³ = 729/1000 = {mp.nstr(weave3, 30)}")
print(f"织a = [62/3/(12π√2)]^(1/3) = {mp.nstr(weavea, 30)}")
print(f"两织差 = {mp.nstr((weavea-weave3)/weave3*100, 8)}%")

# 104az-80 m_s/T_c 代数身份（准精确 1.24e-7%）
msTc_id = 5*dlmin - mp.mpf(319)/648000
print(f"\n① m_s/T_c 代数身份（104az-80，独立于 a₀）：5Δλ_min − 319/648000 = {mp.nstr(msTc_id, 30)}")

# ② 两织口径 → m_s/T_c 预测（m_s = Λ·4/9, T_c = a₀Λ）
print("\n② m_s = Λ·(C_F/2)² = Λ·4/9（104az-72 候选）∧ T_c = a₀Λ（D9）→ m_s/T_c = 4/(9a₀)")
for name, a in [("织³ = 729/1000", weave3), ("织a = d_eff 身份", weavea)]:
    pred = mp.mpf(4)/9/a
    dev = (pred - msTc_id)/msTc_id*100
    tag = "准锁定 <0.01%" if abs(dev) < 0.01 else ("超判据 >0.01%" if abs(dev) > 0.01 else "0.01% 边缘")
    print(f"  {name}: m_s/T_c = {mp.nstr(pred, 20)}  dev = {mp.nstr(dev, 8)}%  [{tag}]")

# ③ a₀ 反解：4/(9·m_s/T_c_id)
a0_back = mp.mpf(4)/9/msTc_id
print(f"\n③ a₀ 反解：a₀ = 4/(9·m_s/T_c_id) = {mp.nstr(a0_back, 40)}")
print(f"   vs 织a = {mp.nstr(weavea, 40)}：dev = {mp.nstr((a0_back-weavea)/weavea*100, 6)}%")
print(f"   vs 织³ = {mp.nstr(weave3, 20)}：dev = {mp.nstr((a0_back-weave3)/weave3*100, 6)}%")

# ④ 判别力
dev_a = abs((mp.mpf(4)/9/weavea - msTc_id)/msTc_id)
dev_3 = abs((mp.mpf(4)/9/weave3 - msTc_id)/msTc_id)
print(f"\n④ 判别力：|dev_织³|/|dev_织a| = {mp.nstr(dev_3/dev_a, 6)} 倍")

# ⑤ F_np 通道正确参照复核（104az-75 ③：F(210.0)=4.21505 / F(210.3)=4.22108）
print("\n⑤ F_np 通道正确参照（104az-75 ③ 勘误，观测参照 Λ=210.0/210.3 非 4.2）")
rge3 = mp.e**(-mp.pi**2 * 2**3)  # rge3 = e^{−π²·2^B₀}, B₀=? 用 4.9.8214/rge3? 直接引用登记值
# 104az-75 ③: F(210.0)=4.21505 / F(210.3)=4.22108（rge3·M_Pl = 49.8214）
Flo, Fhi = mp.mpf("4.21505"), mp.mpf("4.22108")
for name, Fv in [("织³口径 4.218700", mp.mpf("4.218700")), ("织a口径 4.219483", mp.mpf("4.219483")), ("不动点口径 4.214266", mp.mpf("4.214266"))]:
    dev_lo = (Fv - Flo)/Flo*100
    dev_hi = (Fv - Fhi)/Fhi*100
    print(f"  {name}: vs F(210.0) {mp.nstr(dev_lo, 5)}% / vs F(210.3) {mp.nstr(dev_hi, 5)}% —— 均 ~0.1% 级，无分辨力")

print("\n⑥ 结论：m_s/T_c 代数身份通道对织因子有判别力（织a 准锁定 vs 织³ 超判据）——")
print("   与 104az-99 的'双检验无法区分'表述冲突，需修正登记；F_np 通道确认无分辨力。")
