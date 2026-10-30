# -*- coding: utf-8 -*-
"""α_v 修正的全扇区交叉验证（2026-10-26）——先验检验 (b)

α_v' = 1.8846 vs 旧 1.8831（+0.081%）的影响：
① v = m_t·c_1^{α_v−α_t}（静默公式 paper11 L398）——v 链 σ 数
② 夸克 Formula B y_i = c_i^{α_v}——U=I 版本漂移
③ β_u = α_u/α_v 漂移
"""
import math

alpha_v_old = 1.8831
alpha_v_new = 16/15 + math.sqrt(2/3)*(1+6*(1/15)**3)   # 1.884615
alpha_t = 1.945
m_t = 172.7                      # 框架预测（GeV）
c1, c2, c3 = 0.003314, 0.066554, 0.999761
v_exp = 246.22                   # GeV（实验）
N_H = 1.001

print("=== ① v 链（m_t·c_1^{α_v−α_t}）===")
for n, av in [("旧 α_v=1.8831", alpha_v_old), ("新 α_v'=1.8846", alpha_v_new)]:
    v = m_t*c1**(av-alpha_t)
    print(f"  {n:14s} → v = {v:.3f} GeV vs 实验 {v_exp}（偏差 {(v-v_exp)/v_exp*100:+.2f}%）")
print(f"  v 链 σ_score 口径：实验 v = 246.22(0.05?) GeV——需查 CODATA/PDG 不确定度")
print()

print("=== ② 夸克 Formula B y_i = c_i^{α_v}（U=I 版本）===")
ys = [("u", c1), ("c", c2), ("t", c3)]
print(f"{'粒子':4s} {'y(旧)':14s} {'y(新)':14s} {'漂移':8s}")
for nm, c in ys:
    y_old = c**alpha_v_old
    y_new = c**alpha_v_new
    print(f"  {nm:2s}  {y_old:.5e}  {y_new:.5e}  {(y_new-y_old)/y_old*100:+.2f}%")
print()

print("=== ③ β_u = α_u/α_v ===")
for n, av in [("旧", alpha_v_old), ("新", alpha_v_new)]:
    beta_u = alpha_t/av
    print(f"  α_v = {av:.4f} → β_u = {beta_u:.4f}（漂移 {(beta_u-1.945/1.8831)/(1.945/1.8831)*100:+.3f}%）")
print()

print("=== ④ α_v^A（ln7−Δλ_min/2）对照 ===")
avA = 1.8849
for n, av in [("α_v^A=1.8849", avA)]:
    v = m_t*c1**(av-alpha_t)
    print(f"  {n:12s} → v = {v:.3f}（{(v-v_exp)/v_exp*100:+.2f}%）、β_u = {alpha_t/av:.4f}")
print()

print("=== ⑤ 判别：α_v 修正 0.081% 的扇区承受力 ===")
print(f"  v 链：漂移 {(m_t*c1**(alpha_v_new-alpha_t)-v_exp)/v_exp*100 - (m_t*c1**(alpha_v_old-alpha_t)-v_exp)/v_exp*100:+.2f}% 点（旧偏差→新偏差）")
print(f"  u/c 夸克 y：+{(c1**alpha_v_new/c1**alpha_v_old-1)*100:.2f}%/+{(c2**alpha_v_new/c2**alpha_v_old-1)*100:.2f}%——U 优化容量（>10%）可吸收")
print(f"  β_u：−0.08%——Formula B^β 的 β 敏感度低（MSE 平台 ~1e-30）→ 可吸收")
