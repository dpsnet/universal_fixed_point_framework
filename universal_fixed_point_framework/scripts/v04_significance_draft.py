# -*- coding: utf-8 -*-
"""P3 显著性草案 v0.4（104az-212 候选）—— 负控六元组全字段 + decoy 10× + Fisher 精确检验
六元组：①表达式语法 ②原子集 ③深度上限 ④候选总数 ⑤命中数 ⑥容差；
新增：⑦decoy 命中率（10×，同域随机）⑧Fisher p（真实 vs decoy 合并列联表）⑨假阳性率判定。
模板族复用 v0.3（T1 κΛ / T2 21-100 / T3 m_t/m_b）；T4（g_p/2 跨参数）用现有选择性覆盖数据，
不做新 decoy 扫描（1760 万组合太慢），单列记录。
判据（10× 标准）：真实命中率 > 10× 平均 decoy 命中率 或 Fisher p < 0.05 → 超基线；
否则 → 与基线不可区分。本脚本为草案（draft），结论以方法学登记。
"""
import json, random, sys, time
from fractions import Fraction
from scipy.stats import fisher_exact

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

P7 = p_smooth(500, [2, 3, 5, 7])
P7L = p_smooth(5000, [2, 3, 5, 7])
TOL = 0.001  # 0.1% 相对容差

def run_t1(T, tol=TOL):
    """T1: A*(1+1/n)，A ∈ F(16)，n ∈ [1,5000] → 族大小 80000"""
    total = 0
    for A in F:
        for n in range(1, 5001):
            v = A * (1 + 1.0 / n)
            if abs(v - T) / T <= tol:
                total += 1
    return total, len(F) * 5000

def run_t2(T, tol=TOL):
    """T2: 1/p - 1/q，p,q ∈ P7 → 族大小 |P7|²"""
    total = 0
    size = len(P7) * len(P7)
    for p in P7:
        for q in P7:
            if q == p:
                continue
            v = 1.0 / p - 1.0 / q
            if v <= 0:
                continue
            if abs(v - T) / T <= tol:
                total += 1
    return total, size

def run_t3(T, tol=TOL):
    """T3: a - b^3/c - d/e，a∈F，b∈{3,5,7}，c,e∈P7L，d=round(R*e)"""
    total = 0
    size = len(F) * 3 * len(P7L) * len(P7L)
    for a in F:
        for b in (3, 5, 7):
            b3 = b ** 3
            for c in P7L:
                R = a - b3 / c - T
                if R <= 0:
                    continue
                for e in P7L:
                    d = int(round(R * e))
                    if d < 1:
                        continue
                    v = a - b3 / c - d / e
                    if abs(v - T) / T <= tol:
                        total += 1
    return total, size

def gen_decoy(T, n, seed):
    rng = random.Random(seed)
    return [T * (0.9 + 0.2 * rng.random()) for _ in range(n)]

def fisher(real_hits, real_size, decoy_hits, decoy_size):
    table = [[real_hits, real_size - real_hits],
             [decoy_hits, decoy_size - decoy_hits]]
    _, p = fisher_exact(table, alternative="greater")
    return p

def main(out_path):
    TARGETS = [
        ("T1 κΛ", "kappa", 401.73304855, run_t1),
        ("T2 21/100", "t2", 0.21, run_t2),
        ("T3 m_t/m_b", "mttb", 41.284, run_t3),
    ]
    results = []
    for label, key, T, runner in TARGETS:
        t0 = time.time()
        real_hits, real_size = runner(T)
        decoys = gen_decoy(T, 10, seed=hash(key) % 10000)
        d_hits, d_size = 0, 0
        per_decoy = []
        for i, dT in enumerate(decoys):
            h, s = runner(dT)
            per_decoy.append((dT, h, s))
            d_hits += h
            d_size += s
        d_rate = d_hits / d_size if d_size else 0
        real_rate = real_hits / real_size
        p = fisher(real_hits, real_size, d_hits, d_size)
        verdict = "超基线" if (real_rate > 10 * d_rate or p < 0.05) else "与基线不可区分"
        results.append({
            "family": label, "T": T, "real_hits": real_hits, "real_size": real_size,
            "real_rate": real_rate, "decoy_hits": d_hits, "decoy_size": d_size,
            "decoy_rate": d_rate, "decoy_per_target": per_decoy,
            "fisher_p": p, "verdict": verdict, "secs": round(time.time() - t0, 1),
        })
        print("== %s ==" % label, flush=True)
        print("  真实：%d/%d（%.2e）；decoy：%d/%d（%.2e）；Fisher p=%.4g；判定=%s（%.1fs）"
              % (real_hits, real_size, real_rate, d_hits, d_size, d_rate, p, verdict,
                 time.time() - t0), flush=True)
        print("  decoy 逐目标命中：%s" % [h for _, h, _ in per_decoy], flush=True)
    # T4 现有选择性覆盖数据（对象 3，104az-207）：g_p/2 1 命中、g_n/2 0、1/α 0、21/100 22（同域目标即天然 decoy 对照）
    t4 = {
        "family": "T4 g_p/2（跨参数，现有数据）",
        "note": "对象 3（104az-207）：T4 对 4 个同域目标扫（1760 万组合/目标）命中 = [g_p/2:1, g_n/2:0, 1/α:0, 21/100:22]；"
                "选择性覆盖 = 特异性反向证据；4 样本不足做 Fisher，登记为统计样本不足、不判超基线",
        "hits_per_target": {"g_p_over_2": 1, "g_n_over_2": 0, "alpha_inv": 0, "21_100": 22},
    }
    out = {
        "version": "v0.4 draft",
        "date": "2026-10-21",
        "method": "六元组 + decoy 10×（同域 [0.9T,1.1T] 随机 10 个/家族）+ Fisher 精确检验（alternative=greater，decoy 合并一列）",
        "tol": TOL,
        "results": results,
        "t4_existing": t4,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("saved -> %s" % out_path, flush=True)

if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "v04_significance_draft.json"
    main(out_path)
