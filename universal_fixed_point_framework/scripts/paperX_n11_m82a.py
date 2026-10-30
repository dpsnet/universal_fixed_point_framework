# -*- coding: utf-8 -*-
"""M82a（修正）：锚 1 特权解析论证——权重分析
- 0-based：omega[0]=粒子1（唯一负），omega[a]（a=1..n-1）=粒子 a+1（正）
- P1：|ω1| = Σ_{a≥1} ω_a（R₁ 动量守恒——锚 1 权重 = 总正 ω）
- P2：|ω1| ≥ max 正 ω
- P3：锚 1 前缀括号值动态范围 > 相邻单对
"""
import os, sys, json, random
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_degenerate_family_scan import gen_partial_collinear

if __name__ == "__main__":
    n = 11
    N = 20000
    rng = random.Random(20261009)

    prefix_vals = defaultdict(list)
    adj_vals = defaultdict(list)
    w1_ratio = []
    maxw_ratio = []

    for _ in range(N):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        pos = omega[1:n]
        w1_ratio.append(abs(omega[0]) / sum(pos))
        maxw_ratio.append(abs(omega[0]) / max(pos))
        # 锚 1 前缀：s1_2..m = [λ1, Σ_{2..m}λ]——粒子 2..m 对应 omega[1..m-1]
        for m in range(2, n):   # m = 2..n-1（粒子 2..m）
            W = sum(omega[x] for x in range(1, m))
            Z = sum(omega[x] * zbar[x] for x in range(1, m))
            val = omega[0] * (zbar[0] * W - Z)
            prefix_vals["s1_%s" % "".join(str(x) for x in range(2, m + 1))].append(val)
        # 相邻单对：s_{m,m+1}——omega[m-1]*omega[m]
        for m in range(2, n):
            val = omega[m - 1] * omega[m] * (zbar[m - 1] - zbar[m])
            adj_vals["s%s_%s" % (m, m + 1)].append(val)

    p1_ok = all(abs(r - 1) < 1e-9 for r in w1_ratio)
    p2_ok = all(r >= 1.0 for r in maxw_ratio)
    print(f"P1（|ω1|=Σ正ω）：{p1_ok}（{sum(1 for r in w1_ratio if abs(r-1)<1e-9)}/{N}）", flush=True)
    print(f"P2（|ω1|≥max正ω）：{p2_ok}（{sum(1 for r in maxw_ratio if r>=1)}/{N}）", flush=True)

    def stats(d):
        rows = []
        for name, vals in sorted(d.items()):
            mean = sum(vals) / len(vals)
            std = (sum((v - mean) ** 2 for v in vals) / len(vals)) ** 0.5
            small = sum(1 for v in vals if abs(v) < std * 0.1) / len(vals)
            rows.append((name, round(std, 4), round(small, 4)))
        return rows

    p_stats = stats(prefix_vals)
    a_stats = stats(adj_vals)
    p_std_mean = sum(x[1] for x in p_stats) / len(p_stats)
    a_std_mean = sum(x[1] for x in a_stats) / len(a_stats)
    p_nz = sum(x[2] for x in p_stats) / len(p_stats)
    a_nz = sum(x[2] for x in a_stats) / len(a_stats)
    print(f"\n锚 1 前缀 {len(p_stats)} 个——std 均值 {p_std_mean:.3f}——近零占比 {p_nz:.4f}", flush=True)
    print(f"相邻单对 {len(a_stats)} 个——std 均值 {a_std_mean:.3f}——近零占比 {a_nz:.4f}", flush=True)
    print(f"P3（动态范围比）：{p_std_mean / a_std_mean:.2f}——锚 1 前缀更大 = {p_std_mean > a_std_mean}", flush=True)

    out = {"n": n, "N": N, "p1_ok": p1_ok, "p2_ok": p2_ok,
           "p_std_mean": round(p_std_mean, 4), "a_std_mean": round(a_std_mean, 4),
           "p3_ratio": round(p_std_mean / a_std_mean, 2),
           "p_nearzero": round(p_nz, 4), "a_nearzero": round(a_nz, 4),
           "prefix_stats": p_stats, "adj_stats": a_stats}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m82a_weight.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m82a_weight.json", flush=True)
