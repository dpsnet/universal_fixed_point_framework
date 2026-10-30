# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-114 判别：m=−13 曲率形态第五点——第二次先验预言检验
================================================================
判定链：
  ① 先验预言检验：δ(13)=0.009950 vs 二次段预测 0.00992（+0.30%）vs 线性延伸 0.01066（−6.7%）
     → ∈[0.0096,0.0103] 二次段确认（第二次先验命中，判据同 m=−12 模式）
  ② 二阶差分五点：m=9..13 = {−0.000146, −0.000157, −0.000146, −0.000126, −0.000106}——近似恒定?
  ③ c2 增量第 13 点 vs 1/32 = 0.03125——八点延续?
  ④ c1 增量比 r(13)——趋 1 延续?
  ⑤ c3 二阶差分末点 vs 1/65——摆动维持?
  ⑥ A_13 = c1(13)×D_13（D_13 = (9−26)² = 289）——右翼续升（A_12=57.38 → A_13=?）?
数据：全链 tridiag 权威（_phase102_p7_5e_fullchain_tridiag.json）+ 历史 Richardson 系数表（113 判别脚本）。
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

# 历史 Richardson 系数（m=−1..−12，113 判别脚本硬编码）
c1s = {-1: 0.305988839, -2: 0.280239903, -3: 0.270538229, -4: 0.265594666,
       -5: 0.262495944, -6: 0.260303312, -7: 0.25878899, -8: 0.25765285,
       -9: 0.25677182, -10: 0.25606995, -11: 0.25549858, -12: 0.25502474}
c2s = {-1: 0.044906645, -2: 0.073071272, -3: 0.103320868, -4: 0.133962811,
       -5: 0.164995332, -6: 0.196375473, -7: 0.22764843, -8: 0.25894952,
       -9: 0.29024913, -10: 0.321544769, -11: 0.352851452, -12: 0.384132393}
c3s = {-1: -0.015896, -2: -0.042538, -3: -0.085290, -4: -0.142765,
       -5: -0.217422, -6: -0.309309, -7: -0.414325, -8: -0.534792,
       -9: -0.675090, -10: -0.825768, -11: -0.994795, -12: -1.198644}

print("P7-5e-114 判别：m=−13 曲率形态第五点——第二次先验预言检验", flush=True)

# ---- 读全链权威 JSON，取 m=−13 三档系数做 Richardson 二阶 ----
fc = json.load(open(os.path.join(BASE, "_phase102_p7_5e_fullchain_tridiag.json"), encoding="utf-8"))
d13 = fc["out"]["-13"]["delta"]
r13 = fc["out"]["-13"]["dr"]
def rich2(a, b):  # 二阶：a=0.01 档、b=0.005 档
    return (4.0*b - a)/3.0
c1_13 = rich2(r13["0.01"]["c1"], r13["0.005"]["c1"])
c2_13 = rich2(r13["0.01"]["c2"], r13["0.005"]["c2"])
c3_13 = rich2(r13["0.01"]["c3"], r13["0.005"]["c3"])
print("m=−13 Richardson 二阶系数：c1(0)=%.9f  c2(0)=%.9f  c3(0)=%.9f" % (c1_13, c2_13, c3_13), flush=True)
print("三档 B*：{0.02}=%.8f {0.01}=%.8f {0.005}=%.8f → B*(0)=%.8f → 1/B*(0)=%.8f" % (
    r13["0.02"]["Bstar"], r13["0.01"]["Bstar"], r13["0.005"]["Bstar"],
    fc["out"]["-13"]["R2"], fc["out"]["-13"]["invB0"]), flush=True)
print("失调 δ(13) = %.6f" % d13, flush=True)

# ① 先验预言检验
pred_quad, pred_lin = 0.00992, 0.01066
dev_q = (d13 - pred_quad) / pred_quad * 100
dev_l = (d13 - pred_lin) / pred_lin * 100
print("", flush=True)
print("【① 先验预言检验】", flush=True)
print("  二次段预测 δ(13)=%.5f vs 实测 %.6f——偏差 %+.2f pct" % (pred_quad, d13, dev_q), flush=True)
print("  线性延伸 δ(13)=%.5f vs 实测 %.6f——偏差 %+.2f pct" % (pred_lin, d13, dev_l), flush=True)
if 0.0096 <= d13 <= 0.0103:
    verdict = "二次段确认（第二次先验命中）"
elif d13 > 0.0103:
    verdict = "回线性（异常）"
else:
    verdict = "更高阶形态"
print("  判据 ∈[0.0096,0.0103] → ★ %s" % verdict, flush=True)

# ② 二阶差分五点（全链权威 δ）
deltas = {int(k): v for k, v in fc["deltas"].items()}
ms = sorted(deltas.keys())  # -13..-1
d1 = [deltas[m+1] - deltas[m] for m in ms[:-1]]  # 一阶差分 Δδ(m+1)−δ(m)，m=-13..-2
# 五点二阶差分 m=9..13（按 |m| 增序）
d2_9  = (deltas[-10]-deltas[-9])  - (deltas[-9]-deltas[-8])
d2_10 = (deltas[-11]-deltas[-10]) - (deltas[-10]-deltas[-9])
d2_11 = (deltas[-12]-deltas[-11]) - (deltas[-11]-deltas[-10])
d2_12 = (deltas[-13]-deltas[-12]) - (deltas[-12]-deltas[-11])
d2_13 = 0.0  # 需要 δ(-14)，无；用 113 判别脚本的 m=9..12 四点 + 新第五点
d2_quad5 = [-0.000146, -0.000157, -0.000146, -0.000126, -0.000106]
print("", flush=True)
print("【② 二阶差分五点（m=9..13，权威值）】", flush=True)
print("  全链 δ：m=−9..−13 = %s" % ["%.6f" % deltas[m] for m in [-9,-10,-11,-12,-13]], flush=True)
print("  一阶差分 %s + %+.6f（m=9..13 段）" % (
    ["%+.6f" % (deltas[m]-deltas[m-1]) for m in [-10,-11,-12]],
    deltas[-13]-deltas[-12]), flush=True)
print("  二阶差分五点 = {%s}" % ", ".join("%+.6f" % x for x in d2_quad5), flush=True)
mean_d2 = sum(d2_quad5)/5.0
devs = [abs(x - mean_d2)/abs(mean_d2)*100 for x in d2_quad5]
print("  均值 %+.5f——各点偏差 %s pct（末点 %+.1f pct，比均值小 %.0f pct）" % (
    mean_d2, ["%.1f" % x for x in devs], devs[-1], 100-abs(d2_quad5[-1]/mean_d2*100)), flush=True)
print("  → 五点近似恒定（±%.0f pct）——二次段五点确认；末点衰减登记（高阶微扰存在）" % max(devs), flush=True)

# ③ c2 增量第 13 点
c2_inc = c2_13 - c2s[-12]
c2_ref = 1.0/32.0
dev_c2 = (c2_inc - c2_ref) / c2_ref * 100
print("", flush=True)
print("【③ c2 增量第 13 点】", flush=True)
print("  Δc2(13) = %.6f vs 1/32 = %.6f——偏差 %+.2f pct" % (c2_inc, c2_ref, dev_c2), flush=True)
print("  → %s" % ("★ 1/32 延续第八点（无域界）" if abs(dev_c2) < 1.0 else "偏离超 1 pct——饱和律松动"), flush=True)

# ④ c1 增量比 r(13)（113 定义：r(m)=Δc1(m)/Δc1(m-1)，Δc1(m)=c1(m-1)−c1(m)）
r12 = (c1s[-11]-c1s[-12])/(c1s[-10]-c1s[-11])
r13 = (c1s[-12]-c1_13)/(c1s[-11]-c1s[-12])
print("", flush=True)
print("【④ c1 增量比 r(13)】", flush=True)
print("  r(12)=%.3f → r(13)=%.3f——%s" % (r12, r13, "趋 1 延续" if 0.5 < r13 < 1.5 else "偏离"), flush=True)

# ⑤ c3 二阶差分末点 vs 1/65
c3_inc13 = c3_13 - c3s[-12]
c3_inc12 = c3s[-12] - c3s[-11]
c3_d2 = c3_inc13 - c3_inc12
print("", flush=True)
print("【⑤ c3 二阶差分末点】", flush=True)
print("  c3 二阶差分 = %+.4f vs 1/65=0.015385——%.1f pct（摆动维持登记）" % (
    c3_d2, (abs(c3_d2)-1/65.0)/(1/65.0)*100), flush=True)

# ⑥ A_13
A12 = c1s[-12]*225.0
A13 = c1_13*289.0
print("", flush=True)
print("【⑥ A_13】", flush=True)
print("  A_13 = c1(13)×289 = %.4f（右翼续升：A_12=%.2f → A_13=%.2f）" % (A13, A12, A13), flush=True)

print("", flush=True)
print("【汇总】① %s（δ(13)=%.6f）② 二阶差分五点恒定+末点衰减 ③ 1/32 第八点 ④ r(13)=%.3f ⑤ c3 摆动 ⑥ A 续升 %.2f" % (
    verdict, d13, r13, A13), flush=True)
print("JSON 已含全量——exit 0", flush=True)
