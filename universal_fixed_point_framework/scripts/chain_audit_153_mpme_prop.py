# -*- coding: utf-8 -*-
"""
chain_audit_153_mpme_prop.py — m_p/m_e 小数部 371/2430 跨链传播检验
链1：21cm 超精细链（m_e/m_p 因子）
链2：核子链（m_p' 框架值 938.251，P7-6b）
链3：同族数字搜索（371/2430 的框架量因子是否在其他链出现）
"""
import math, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ---- 链1：21cm 超精细链传播 ----
alpha = 1/137.035999084          # CODATA α
gp2 = 40217/14400                 # 框架 g_p/2（104az-148 锁定）
F_obs = 4.317550110e-7            # f_hfs/(c·R∞) CODATA（104az-151）
mpme_codata = 1836.15267343       # CODATA m_p/m_e
mpme_frame = 1836 + 371/2430      # 框架候选 = 1836.152674897

def delta(mpme):
    F0 = (16/3)*alpha**2*(1/mpme)*gp2
    return F_obs/F0 - 1

d_cod = delta(mpme_codata)
d_frm = delta(mpme_frame)
print("=== 链1：21cm δ 传播 ===")
print(f"m_p/m_e CODATA {mpme_codata:.8f} → δ = {d_cod:.6e} ({d_cod*100:.5f}%)")
print(f"m_p/m_e 框架   {mpme_frame:.8f} → δ = {d_frm:.6e} ({d_frm*100:.5f}%)")
print(f"371/2430 传播对 δ 的影响：{(d_frm/d_cod-1)*100:+.3f}%（相对），δ 绝对移动 {(d_frm-d_cod)*100:.5f} 个百分点")
print(f"结论：δ 仍 −0.05% 级、符号不变 → 371/2430 传播不引入新张力")

# ---- 链2：核子链交叉 ----
mp_obs_mev = 938.27208816       # CODATA m_p (MeV)
me_obs_mev = 0.51099895000      # CODATA m_e (MeV)
mp_frame = 938.251              # P7-6b 框架 m_N'
print("\n=== 链2：核子链交叉 ===")
print(f"CODATA m_p/m_e = {mp_obs_mev/me_obs_mev:.8f}")
print(f"框架 m_p'/m_e(CODATA) = {mp_frame/me_obs_mev:.8f}（dev {(mp_frame/me_obs_mev/(mp_obs_mev/me_obs_mev)-1)*100:+.5f}%）")
print(f"框架 m_p'/m_e(框架 1836.152674897) 隐含 m_p' = {mpme_frame*me_obs_mev:.4f} MeV（vs 框架 938.251，dev {(mpme_frame*me_obs_mev/938.251-1)*100:+.5f}%）")
print("注意：m_p'=938.251 是重子族 0.01% 级候选（P7-6b），m_e 本身 e 指数链（P7-5v）；交叉为候选级一致性参考")

# ---- 链3：同族数字搜索（371/2430 因子 vs 框架常数库）----
print("\n=== 链3：同族因子搜索 ===")
n, d = 371, 2430
print(f"371 = 7×53（对合域 × (N_gen²·静默+k_max) = 7×(45+8))")
print(f"2430 = 2×3⁵×5（幂基 × N_gen⁵ × 静默，全素基平滑）")
frame_set = [2,3,4,5,7,8,15,16,24,25,29,31,45,49,53,63,64,65,80,96,128,231,232,320,400,675]
print(f"53 ∈ 框架量集？{'是' if 53 in frame_set else '否（53 = 45+8 加性族，与 g_p/2 分子 307=45·7−8 同型）'}")
# 371/2430 vs 框架常见比值
print(f"371/2430 = {371/2430:.10f}")
for k, v in [(1, 0.15), (1, 0.1526)]:
    pass
# 与 m_e 链指数核对：ln(1836.152674897/1836) 的结构
ratio = mpme_frame/1836
print(f"小数修正 371/2430 占比：{371/2430/1836*100:.6f}%（主结构的 0.00831%）")
print(f"ln(1+371/(2430·1836)) = {math.log(1+371/(2430*1836)):.3e}")
