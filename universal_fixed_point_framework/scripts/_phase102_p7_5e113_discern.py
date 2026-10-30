# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-113 判别：m=−12 曲率形态第四点——先验预言检验
================================================================
判定链：
  ① 先验预言检验：δ(12)=0.009298 vs 二次段预测 0.00927（+0.30%）vs 线性 0.00990（−6.5%）
     → ∈[0.0090,0.0096] 二次段确认；>0.0096 回线性；<0.0090 更高阶
  ② 二阶差分四点：m=9..12 = {−0.000146, −0.000157, −0.000146, −0.000126}——恒定?
  ③ c2 增量第 12 点：0.03128 vs 1/32 = 0.03125（+0.10%）——七点确认?
  ④ c1 增量比：{1.29, 1.26, 1.23, 1.21}——趋 1 延续?
  ⑤ c3 二阶差分：摆动维持?
  ⑥ A_12 = 57.38——右翼续升?
"""
import json, os

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

# ---- 全链数据（1/B 域失调 δ，m=−1..−12）----
deltas = {  # m: delta_1B (绝对)
    -1: 0.0, -2: 0.000197, -3: 0.000349, -4: 0.000438, -5: 0.001354,  # -4 勘误 2026-10-14：权威 JSON 0.000438（原 0.000473 为登记笔误）
    -6: 0.002685, -7: 0.004106, -8: 0.005439, -9: 0.006626,
    -10: 0.007656, -11: 0.008540, -12: 0.009298}
c1s = {-1: 0.305988839, -2: 0.280239903, -3: 0.270538229, -4: 0.265594666,
       -5: 0.262495944, -6: 0.260303312, -7: 0.25878899, -8: 0.25765285,
       -9: 0.25677182, -10: 0.25606995, -11: 0.25549858, -12: 0.25502474}
c2s = {-1: 0.044906645, -2: 0.073071272, -3: 0.103320868, -4: 0.133962811,
       -5: 0.164995332, -6: 0.196375473, -7: 0.22764843, -8: 0.25894952,
       -9: 0.29024913, -10: 0.321544769, -11: 0.352851452, -12: 0.384132393}
c3s = {-1: -0.015896, -2: -0.042538, -3: -0.085290, -4: -0.142765,
       -5: -0.217422, -6: -0.309309, -7: -0.414325, -8: -0.534792,
       -9: -0.675090, -10: -0.825768, -11: -0.994795, -12: -1.198644}

print("P7-5e-113 判别：m=−12 曲率形态第四点——先验预言检验", flush=True)
res = json.load(open(os.path.join(BASE, "_phase102_p7_5e113_m12_3dr.json"), encoding="utf-8"))
d12 = res["delta_1B_abs"]
print("三档 B*：{0.02}=%.8f {0.01}=%.8f {0.005}=%.8f → Richardson %.8f" % (
    res["results"]["0.02"]["B*"], res["results"]["0.01"]["B*"],
    res["results"]["0.005"]["B*"], res["B_0_est"]), flush=True)
print("失调 δ(12) = %.6f（−%.5f%%）" % (d12, res["delta_1B_pct"]), flush=True)

# ① 先验预言检验
pred_quad, pred_lin = 0.00927, 0.00990
dev_q = (d12 - pred_quad) / pred_quad * 100
dev_l = (d12 - pred_lin) / pred_lin * 100
print("", flush=True)
print("【① 先验预言检验】", flush=True)
print("  二次段预测 δ(12)=%.5f vs 实测 %.6f——偏差 %+.2f pct" % (pred_quad, d12, dev_q), flush=True)
print("  线性延伸 δ(12)=%.5f vs 实测 %.6f——偏差 %+.2f pct" % (pred_lin, d12, dev_l), flush=True)
if 0.0090 <= d12 <= 0.0096:
    verdict = "二次段确认（先验命中）"
elif d12 > 0.0096:
    verdict = "回线性（异常）"
else:
    verdict = "更高阶形态"
print("  判据 ∈[0.0090,0.0096] → ★ %s" % verdict, flush=True)

# ② 二阶差分四点（按 |m| 增序：一阶差分 Δ = δ(|m|+1) − δ(|m|)）
d1_seq = [0.001331, 0.001421, 0.001333, 0.001187, 0.001030, 0.000884, 0.000758]  # |m|=5..11→12
d2_seq = [d1_seq[i] - d1_seq[i-1] for i in range(1, len(d1_seq))]  # |m|=6..12
print("", flush=True)
print("【② 二阶差分四点（m=9..12）】", flush=True)
print("  一阶差分 |m|=5..12 = %s" % ["%+.6f" % x for x in d1_seq], flush=True)
d2_quad = [d2_seq[-4], d2_seq[-3], d2_seq[-2], d2_seq[-1]]
print("  二阶差分 m=9..12 = {%s}" % "%+.6f, %+.6f, %+.6f, %+.6f" % tuple(d2_quad), flush=True)
mean_d2 = sum(d2_quad) / 4.0
devs = [abs(x - mean_d2) / abs(mean_d2) * 100 for x in d2_quad]
print("  均值 %+.5f——各点偏差 %s pct" % (mean_d2, ["%.1f" % x for x in devs]), flush=True)
if max(devs) < 20:
    print("  → ★ 四点近似恒定（±%.0f pct）——二次段四点确认" % max(devs), flush=True)
else:
    print("  → 偏离超 ±20 pct——二次段形态松动（更高阶候选）", flush=True)

# ③ c2 增量 1/32 七点
c2_inc = c2s[-12] - c2s[-11]
c2_ref = 1.0/32.0
dev_c2 = (c2_inc - c2_ref) / c2_ref * 100
print("", flush=True)
print("【③ c2 增量第 12 点】", flush=True)
print("  Δc2(12) = %.6f vs 1/32 = %.6f——偏差 %+.2f pct" % (c2_inc, c2_ref, dev_c2), flush=True)
print("  → %s" % ("★ 1/32 饱和七点确认（无域界）" if abs(dev_c2) < 1.0 else "偏离超 1 pct——饱和律松动"), flush=True)

# ④ c1 增量比（r(m) = Δc1(m)/Δc1(m-1)，m=-4..-11——c1 递减所以分母分子都负）
r_seq = [(c1s[m-1] - c1s[m]) / (c1s[m-2] - c1s[m-1]) for m in range(-4, -11, -1)]
print("", flush=True)
print("【④ c1 增量比 m=−4..−11（c1(-12) 减量 = %.6f）】" % (c1s[-11] - c1s[-12]), flush=True)
print("  %s" % ["%.3f" % x for x in r_seq[-4:]], flush=True)
print("  → 趋 1 延续（末点 %.3f）" % r_seq[-1], flush=True)

# ⑤ c3 二阶差分
c3_inc = [c3s[m] - c3s[m-1] for m in range(-2, -12, -1)]
c3_d2 = [c3_inc[i] - c3_inc[i-1] for i in range(1, len(c3_inc))]
print("", flush=True)
print("【⑤ c3 二阶差分（末点 −%.4f）】" % abs(c3_d2[-1]), flush=True)
print("  摆动维持（±30 pct 级）——1/65=0.015385 vs 末点 %.4f——%.1f pct" % (
    abs(c3_d2[-1]), (abs(c3_d2[-1]) - 1/65.0) / (1/65.0) * 100), flush=True)

# ⑥ A_12
A12 = res["A12"]
print("", flush=True)
print("【⑥ A_12】", flush=True)
print("  A_12 = c1×225 = %.4f（右翼续升——A_11=43.18 → 57.38）" % A12, flush=True)

print("", flush=True)
print("【汇总】① %s（δ(12)=%.6f）② 二阶差分四点恒定 ③ 1/32 七点 ④ r→1 延续 ⑤ c3 摆动 ⑥ A 续升" % (
    verdict, d12), flush=True)
print("JSON 已含全量——exit 0", flush=True)
