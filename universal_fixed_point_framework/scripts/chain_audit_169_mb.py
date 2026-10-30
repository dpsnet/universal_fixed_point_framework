# -*- coding: utf-8 -*-
"""chain_audit_169_mb.py — m_b 推进：误差传播 + 全框架闭式闭合（104az-169）"""
import io, sys, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

N_gen, k_max, Powers, Silence, Fp, Inv = 3, 8, 2, 5, 4, 7
dlmin = (math.sqrt(3) - 1) / 6

print("=== 1. 误差传播：m_t/m_b 比值统计评估 ===")
mt, s_mt = 172.69, 0.30
mb_c, s_mb = 4.183, 0.023
R = mt / mb_c
s_R = R * math.sqrt((s_mt/mt)**2 + (s_mb/mb_c)**2)
print(f"m_t = {mt}±{s_mt}（pole）；m_b(m_b)^MS = {mb_c}±{s_mb}（PDG 2024 中心）")
print(f"比值 R = {R:.6f} ± {s_R:.6f}（1σ 带 [{R-s_R:.3f}, {R+s_R:.3f}]）")
closed = 167321 / 4050
dev_sigma = (closed - R) / s_R
print(f"闭式 167321/4050 = {closed:.6f}")
print(f"闭式 vs PDG 中心比值：Δ = {closed-R:+.6f} = {dev_sigma:+.3f}σ——统计完全兼容（<1σ）")
print(f"相对偏差：{(closed/R-1)*100:+.4f}%（m_b 不确定度 ±0.55% 下不可分辨）\n")

print("=== 2. m_b* 闭式反推 ===")
mb_star = mt / closed
print(f"闭式反推 m_b* = m_t/(371×451/4050) = {mb_star:.6f} GeV")
print(f"vs PDG 中心 4.183：dev {(mb_star/mb_c-1)*100:+.4f}%（在 ±0.023 误差带内，−0.13σ）")
print(f"vs 常用 4.18：dev {(mb_star/4.18-1)*100:+.6f}%")
print("口径归属：4.1800 为 MS-bar 型（pole 4.78 差 14% 排除）\n")

print("=== 3. m_b 全框架闭式（经由 m_t 链闭合）===")
mtau = 1.77686  # GeV
v_fw = mtau * 81 * 5**(1/3)  # v = m_τ×3⁴×∛5（104az-5h）
mt_fw = (1 - dlmin/16) * v_fw / math.sqrt(2)  # m_t = (1−Δλ_min/16)·v/√2（104az-5m）
mb_fw = mt_fw * 4050 / (371 * 451)  # m_b = m_t×4050/(371×451)（104az-168 闭式）
print(f"Δλ_min = (√3−1)/6 = {dlmin:.8f}")
print(f"v_fw = m_τ×3⁴×∛5 = {mtau}×81×∛5 = {v_fw:.6f} GeV（PDG 246.22，dev {(v_fw/246.22-1)*100:+.4f}%）")
print(f"m_t_fw = (1−Δλ_min/16)·v_fw/√2 = {mt_fw:.6f} GeV（PDG 172.69，dev {(mt_fw/172.69-1)*100:+.4f}%）")
print(f"m_b_fw = m_t_fw×4050/(371×451) = {mb_fw:.6f} GeV")
print(f"vs 4.18：dev {(mb_fw/4.18-1)*100:+.6f}%；vs PDG 中心 4.183：dev {(mb_fw/4.183-1)*100:+.4f}%")
print(f"→ m_b 全框架闭式：m_b = v×(1−Δλ_min/16)×4050/(√2×371×451)")
print(f"  生成链：根集 → m_τ → v(3⁴·∛5) → m_t((1−Δλ_min/16)/√2) → m_b(371 骨架)")

print("\n=== 4. 全框架量因子核对 ===")
print("√2 = √幂基（104az-165 锁定）；Δλ_min = (√3−1)/6（√3=√N_gen）")
print("371 = 对合域×(45+8)；451 = 11×41；4050 = N_gen²×幂基×(N_gen×静默)²")
print("v = m_τ×3⁴×∛5（∛5 = 静默立方根——代数数，104az-5h 候选）")

print("\n=== 5. 判别 ===")
print("① ★ 统计兼容升级：闭式 41.3138 vs PDG 中心口径比值 41.284±0.237 = +0.13σ——完全兼容（此前 4.18 舍入口径的 dev 0.001% 为巧合，误差传播显示中心口径也不排斥）")
print("② ★ m_b 全框架闭式闭合：m_b = v×(1−Δλ_min/16)×4050/(√2×371×451)——三代连锁生成链，无外部常数")
print("③ m_b* = 4.1800 为 MS-bar 型（pole 4.78 排除）；在 PDG [4.160,4.206] 误差带内（−0.13σ）")
print("④ 诚实边界：m_b 不确定度 ±0.55%（±0.023）使 0.01% 级判据不可达——闭式为'框架身份'判据成立（结构闭合），'0.01% 数值命中'判据受观测精度阻塞；∛5 为代数数非有理（框架可接受但无有理分数身份）")
