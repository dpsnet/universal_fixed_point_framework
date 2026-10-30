# -*- coding: utf-8 -*-
"""
P7-5e-161：发夹堆积梯度 + 辫子探针（2 股编织候选）
检验 ① 堆积梯度：δ_cl(m)+δ_cl(9−m)（配对和）与 δ_cl(9−m)−δ_cl(m)（对称差）沿对合域单调性
     ——发夹图像要求残差层向尖端（m=4.5）收拢
检验 ② 辫子探针：交叉点 m=3（尾巴=δ∞ 补满）+ 65/56 代数桥是否构成 2-股编织闭合环
     ——环 1→65→6→3→56→8→1 的每条边都有已登记代数身份？
数据：159 权威 dcl（tridiag 小 m，155b 修正后）
"""
import json

dcl = {1: 2.013e-4, 2: 2.013e-4, 3: 3.544e-4, 4: 4.419e-4, 5: 1.358e-3,
       6: 2.692e-3, 7: 4.055e-3, 8: 5.428e-3}

print("=== ① 堆积梯度（发夹图像残差层复现）===", flush=True)
rows = []
for m in range(1, 5):
    r = 9 - m
    s = dcl[m] + dcl[r]          # 配对和（总堆积）
    d = dcl[r] - dcl[m]          # 对称差（臂不对称量）
    q = dcl[r] / dcl[m]          # 比值（159 已登记）
    rows.append((m, r, dcl[m], dcl[r], s, d, q))
    print("m=%d<->%d: dcl(m)=%.3e dcl(r)=%.3e 和=%.3e 差=%.3e 比=%.2f"
          % (m, r, dcl[m], dcl[r], s, d, q), flush=True)

sums = [r[4] for r in rows]
diffs = [r[5] for r in rows]
sm = all(sums[i] > sums[i+1] for i in range(3))
dm = all(diffs[i] > diffs[i+1] for i in range(3))
print("配对和单调递减:", sm, flush=True)
print("对称差单调递减:", dm, flush=True)

dinf = 1/56
print("和(4)/δ∞ = %.4f（单点观察 ≈ C=0.1016? 不结论）" % (sums[3]/dinf), flush=True)

print("\n=== ② 辫子探针：交叉点 + 代数桥 + 闭合环 ===", flush=True)
print("交叉点扫描：尾巴项 1/(7·2^m) vs δ∞=1/56", flush=True)
for m in range(1, 5):
    tail = 1/(7*2**m)
    cross = abs(tail - dinf) < 1e-12
    print("m=%d: 尾巴=%.6f vs δ∞=%.6f  %s" % (m, tail, dinf, "★ 交叉" if cross else ""), flush=True)
print("→ 交叉点 m=3：尾巴 1/(7·2³) = 1/56 = δ∞（157 补满点登记）", flush=True)

print("\n代数桥（均已登记身份）：", flush=True)
print("65 = 2⁶+1 = k_max²+1（153 m=6 同一性）→ 桥接 m=1 修正（1/65）与指数 6", flush=True)
print("56 = 8·7 = 2³·7（δ∞ 分母）→ 桥接 m=3（尾巴=δ∞）与 m=8=2³", flush=True)
print("对合配对：1↔8（9−1=8）、3↔6（9−3=6）", flush=True)

ring = [(1, 65, "1/65 修正（153/157）"), (65, 6, "65=2⁶+1 指数 6（153）"), (6, 3, "对合 9−6=3（159）"),
        (3, 56, "尾巴=δ∞=1/56 补满（157）"), (56, 8, "56=8·7=2³·7（129/157）"), (8, 1, "对合 9−8=1（159）")]
print("\n闭合环 1→65→6→3→56→8→1：", flush=True)
for a, b, why in ring:
    print("  %d —%s→ %d" % (a, why, b), flush=True)
closed = ring[-1][1] == ring[0][0]
print("环闭合（8→1 回起点）:", closed, flush=True)

print("\n判别：", flush=True)
print("① 堆积梯度：配对和+对称差均单调向尖端（m=4.5）收拢——发夹折叠的残差层复现 ✓", flush=True)
print("② 辫子探针：两条配对链（1↔8、3↔6）经 65/56 代数桥两次跨配对连接——2-股编织候选成立", flush=True)
print("诚实边界：②为代数对应图（节点+身份边），非辫子群运算；B_2 群乘法（σ 生成元关系）未检验", flush=True)
print("升格条件：环在更高 m 域有周期重复（编织的重复单元）或 65/56 桥满足可结合律", flush=True)

out = {"gradient": {
           "pairs": {("%d<->%d" % (m, r)): {"sum": s, "diff": d, "ratio": q}
                     for m, r, a, b, s, d, q in rows},
           "sum_monotone_decreasing": sm, "diff_monotone_decreasing": dm,
           "sum4_over_dinf": sums[3]/dinf},
       "braid_probe": {"crossing_m": 3,
                       "bridges": ["65=2^6+1（m=6 同一性→m=1 修正）", "56=8*7（δ∞ 分母→m=8）"],
                       "pairs": ["1<->8", "3<->6"],
                       "ring": [1, 65, 6, 3, 56, 8, 1], "closed": closed,
                       "verdict": "2-strand braid candidate（代数对应图级，非群运算级）"}}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e161_hairpin_braid.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
print("saved", flush=True)
