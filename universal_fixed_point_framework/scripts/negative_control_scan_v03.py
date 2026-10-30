# -*- coding: utf-8 -*-
"""P3 负控 v0.3 —— 框架量表达式模板族唯一性检验（104az-203）

v0.1（裸分数族）结论：分子不约束则"精确命中"平凡、0.1% 命中普遍。
v0.2（扩展框架素域分数族）结论：g_p/2 与 1/α 呈"精度孤岛"；κΛ 素域不唯一（17 更优），
    唯一性只能靠模板结构；m_t/m_b 无判别力。
v0.3 目标：把"模板结构层"制度化 —— 对每个旗舰扫其自身模板族（参数取框架量/框架素域），
    报告：族内命中总数、优于框架表达式的命中数、最优命中参数与身份。

模板族（全部确定性、可复核）：
  T1: A*(1+1/n)          A ∈ 框架量 F，n ∈ 整数 [1,5000]        （κΛ: 400*(1+1/231) 型）
  T2: 1/p - 1/q          p,q ∈ P-smooth({2,3,5,7}) ≤ 500         （21/100: 1/4-1/25 型）
  T3: a - b^3/c - d/e    a ∈ F，b ∈ {3,5,7}，c,e ∈ P-smooth({2,3,5,7}) ≤ 5000，
                         d = round(R*e)（最近邻）                （m_t/m_b: 42-7^3/500-2/3375 型）

判别指标：hits_tol（0.1% 容差命中总数）；hits_better（dev < 框架 dev）；top5 最优命中。
"""
import json, sys
from fractions import Fraction

# ---- 框架量原子集（§10.1 v0.2 升级方向 + κΛ 主结构 400）----
F = [2, 3, 4, 5, 7, 8, 15, 16, 21, 42, 49, 105, 231, 320, 675, 400]

def p_smooth(maxv, primes):
    res = [1]
    def gen(i, cur):
        if i >= len(primes):
            return
        p = primes[i]
        nxt = cur * p
        while nxt <= maxv:
            gen(i, nxt)
            res.append(nxt)
            nxt *= p
        gen(i + 1, cur)
    gen(0, 1)
    return sorted(set(res))

P7 = p_smooth(500, [2, 3, 5, 7])      # T2 分母域
P7L = p_smooth(5000, [2, 3, 5, 7])    # T3 c/e 域

TARGETS = {
    "kappa_lambda": {"label": "κΛ 定义值 4ln10/Δλ_EM = 401.73304855",
                     "T": 401.73304855, "frame": "92800/231", "frame_dev": 3.6014423e-6},
    "g_p_over_2":   {"label": "μ_p/μ_N CODATA 2018 = 2.79284734463",
                     "T": 2.79284734463, "frame": "40217/14400", "frame_dev": 4.3829026e-8},
    "m_t_over_m_b": {"label": "PDG 中心口径 41.284±0.237",
                     "T": 41.284, "frame": "557731/13500", "frame_dev": 7.1231972e-4},
    "alpha_inv":    {"label": "α⁻¹ CODATA 2018 = 137.035999084",
                     "T": 137.035999084, "frame": "34259/250", "frame_dev": 6.6843750e-9},
    "twenty_one_hundred": {"label": "Hγ n=5 相对频率 0.21",
                     "T": 0.21, "frame": "21/100", "frame_dev": 0.0},
}

TOL = 0.001  # 0.1% 相对容差（与 v0.1 基线一致）

def run_t1(T, tol):
    """T1: A*(1+1/n)，A ∈ F，n ∈ [1,5000] 整数。返回 (命中总数, top5)。"""
    total = 0
    hits = []
    for A in F:
        for n in range(1, 5001):
            v = A * (1 + 1.0 / n)
            dev = abs(v - T) / T
            if dev <= tol:
                total += 1
                hits.append((dev, "A=%d*(1+1/%d)=%.10f" % (A, n, v)))
    hits.sort()
    return {"hits_tol": total, "top5": hits[:5]}

def run_t2(T, tol):
    """T2: 1/p - 1/q，p,q ∈ P7（{2,3,5,7}-smooth ≤500）。"""
    total = 0
    better = 0
    top = []
    for p in P7:
        for q in P7:
            if q == p:
                continue
            v = 1.0 / p - 1.0 / q
            if v <= 0:
                continue
            dev = abs(v - T) / T
            if dev <= tol:
                total += 1
                top.append((dev, "1/%d-1/%d=%.12f" % (p, q, v)))
    top.sort()
    top = top[:5]
    return {"hits_tol": total, "top5": top}

def run_t3(T, tol, frame_dev):
    """T3: a - b^3/c - d/e，a ∈ F，b ∈ {3,5,7}，c,e ∈ P7L，d=round(R*e)。
    返回 (命中总数, 优于框架数, top5)。"""
    total = 0
    better = 0
    top = []
    for a in F:
        for b in (3, 5, 7):
            b3 = b ** 3
            for c in P7L:
                R = a - b3 / c - T   # 需解的 d/e 值（框架 m_t/m_b: 42-7^3/500-2/3375）
                if R <= 0:
                    continue
                for e in P7L:
                    d = int(round(R * e))
                    if d < 1:
                        continue
                    v = a - b3 / c - d / e
                    dev = abs(v - T) / T
                    if dev <= tol:
                        total += 1
                        if dev < frame_dev:
                            better += 1
                            if len(top) < 5 or dev < top[-1][0]:
                                top.append((dev, "a=%d-b^3/c(d=%d/%d) [a=%d,b=%d,c=%d,d=%d,e=%d]=%.10f"
                                           % (a, d, e, a, b, c, d, e, v)))
                                top.sort()
                                top = top[:5]
    return {"hits_tol": total, "hits_better_than_frame": better, "top5": top}

def main(out_path):
    results = {}
    for name, cfg in TARGETS.items():
        T = cfg["T"]
        r = {"label": cfg["label"], "T": T, "frame": cfg["frame"], "frame_dev": cfg["frame_dev"],
             "t1": None, "t2": None, "t3": None}
        # T1 对所有目标
        t1 = run_t1(T, TOL)
        r["t1"] = {"hits_tol": t1["hits_tol"], "top5": t1["top5"]}
        # T2 主要针对 21/100 型（1/p-1/q）；对全部目标跑以保持一致基线
        t2 = run_t2(T, TOL)
        r["t2"] = {"hits_tol": t2["hits_tol"], "top5": t2["top5"]}
        # T3 主要针对 m_t/m_b 型（a-b^3/c-d/e）
        t3 = run_t3(T, TOL, cfg["frame_dev"])
        r["t3"] = {"hits_tol": t3["hits_tol"],
                   "hits_better_than_frame": t3["hits_better_than_frame"],
                   "top5": t3["top5"]}
        results[name] = r
    out = {
        "version": "v0.3",
        "date": "2026-10-21",
        "method": ("框架量表达式模板族：T1 A*(1+1/n) [A∈F,n∈整数1..5000]；"
                   "T2 1/p-1/q [p,q∈{2,3,5,7}-smooth≤500]；"
                   "T3 a-b^3/c-d/e [a∈F,b∈{3,5,7},c,e∈{2,3,5,7}-smooth≤5000,d最近邻]；"
                   "统一相对容差 0.1%"),
        "results": results,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "negative_control_scan_v03.json"
    main(out_path)
