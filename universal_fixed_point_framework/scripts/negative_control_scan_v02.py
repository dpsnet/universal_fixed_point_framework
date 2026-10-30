# -*- coding: utf-8 -*-
"""
P3 负控基线扫描 v0.2（104az-202 素材）
扩展框架素域分数族内的框架表达式唯一性检验

v0.1 结论：无约束分数族内"精确命中"为平凡事件（有理数稠密）；
v0.2 把扫描族收窄为"扩展框架素域"——分子、分母的素因子均 ⊆ P 的分数，
     检验框架表达式（92800/231 等）在该约束族内是否唯一达到其自身精度。

扩展框架素因子集 P = {2,3,5,7}（框架常数素因子）+ 11（S(8)=231=3·7·11）
                     + 13（41/39 家族）+ 29（92800=2^6·5^2·29，29=静默²+不动点）
分母域 b <= 14400（覆盖 g_p/2 分母 14400）
分子域 a <= ceil(T·14400·1.02)（按目标动态）

判别输出：
  - 框架分数是否在扩展域内（分子/分母素因子 ⊆ P）
  - 族内 dev_min、最优命中及其素因子分解
  - 达到框架 dev 或更优的族内命中数
  - 若框架分数在族内：其 dev 在族内排名（唯一性检验）
"""
import json, sys, bisect, math
from fractions import Fraction

P = [2, 3, 5, 7, 11, 13, 29]
B_MAX = 14400


def p_smooth(primes, maxv):
    res = []

    def gen(i, cur):
        if cur > maxv:
            return
        res.append(cur)
        for j in range(i, len(primes)):
            p = primes[j]
            nxt = cur * p
            while nxt <= maxv:
                gen(j, nxt)
                nxt *= p

    gen(0, 1)
    return sorted(set(res))


def factorize(n):
    f = {}
    x = n
    for p in P:
        while x % p == 0:
            f[p] = f.get(p, 0) + 1
            x //= p
    return f, x  # x == 1 => 素因子 ⊆ P


def fmt_factor(f, residue):
    core = "*".join("%d^%d" % (p, e) for p, e in sorted(f.items())) if f else "1"
    if residue != 1:
        return core + " * %d(余素)" % residue
    return core


targets = {
    "kappa_lambda": {"T": 401.73304855,
                     "frame": ("92800/231", Fraction(92800, 231)),
                     "label": "κΛ 定义值 4ln10/Δλ_EM"},
    "g_p_over_2": {"T": 2.79284734463,
                   "frame": ("40217/14400", Fraction(40217, 14400)),
                   "label": "μ_p/μ_N CODATA 2018"},
    "m_t_over_m_b": {"T": 41.284,
                     "frame": ("557731/13500", Fraction(557731, 13500)),
                     "label": "PDG 中心口径 41.284±0.237（D 闭式 42-7^3/500-2/3375）"},
    "alpha_inv": {"T": 137.035999084,
                  "frame": ("34259/250", Fraction(34259, 250)),
                  "label": "α^-1 CODATA 2018（路径A 16259/6000 -> 24(d_H+3)）"},
    "twenty_one_hundred": {"T": 0.21,
                           "frame": ("21/100", Fraction(21, 100)),
                           "label": "Hγ n=5 相对频率（R∞ 精度 1.9e-12）"},
}


def scan(name, cfg):
    T = cfg["T"]
    frame_str, frame_frac = cfg["frame"]
    A_MAX = int(math.ceil(T * B_MAX * 1.02))
    A = p_smooth(P, A_MAX)
    B = p_smooth(P, B_MAX)
    tol = 0.01  # 候选级容差（相对 1e-4）
    hits = []  # (dev, a, b)
    for b in B:
        ta = T * b
        idx = bisect.bisect_left(A, ta)
        for a in (A[idx] if idx < len(A) else None,
                  A[idx - 1] if idx > 0 else None):
            if a is None:
                continue
            dev = abs(a / b - T) / T
            if dev <= tol:
                hits.append((dev, a, b))
    hits.sort(key=lambda h: h[0])
    fn, fr = factorize(frame_frac.numerator)
    fd, dr = factorize(frame_frac.denominator)
    frame_in_domain = (fr == 1 and dr == 1)
    fval = float(frame_frac)
    fdev = abs(fval - T) / T if T != 0 else 0.0
    tighter = [h for h in hits if h[0] <= fdev * 1.000001] if fdev > 0 else list(hits)
    rank = None
    if frame_in_domain and frame_frac.numerator <= A_MAX:
        count_less = sum(1 for h in hits if h[0] < fdev)
        count_leq = sum(1 for h in hits if h[0] <= fdev)
        rank = {"dev_less_in_family": count_less,
                "dev_leq_in_family": count_leq,
                "hit_total_tol001pct": len(hits)}
    best = None
    if hits:
        ba, bb = hits[0][1], hits[0][2]
        best = {"a": ba, "b": bb, "dev": hits[0][0],
                "a_factor": fmt_factor(*factorize(ba)),
                "b_factor": fmt_factor(*factorize(bb)),
                "value": ba / bb}
    return {
        "target": name, "label": cfg["label"],
        "T": T, "tol": tol,
        "frame": frame_str, "frame_value": fval, "frame_dev": fdev,
        "frame_in_extended_domain": frame_in_domain,
        "frame_num_factor": fmt_factor(fn, fr),
        "frame_den_factor": fmt_factor(fd, dr),
        "family_size_num": len(A), "family_size_den": len(B),
        "hits_tol001pct": len(hits),
        "hits_reaching_frame_dev": len(tighter),
        "best_hit": best,
        "frame_rank": rank,
    }


results = {name: scan(name, cfg) for name, cfg in targets.items()}
out = {
    "version": "v0.2",
    "date": "2026-10-21",
    "method": ("扩展框架素域分数族 a/b：a <= ceil(T*14400*1.02)、b <= 14400、"
               "分子分母素因子均 ⊆ {2,3,5,7,11,13,29}；相对容差 0.01%；"
               "框架 dev 对照 = 框架分数对观测/定义值的相对偏差"),
    "results": results,
}
path = sys.argv[1] if len(sys.argv) > 1 else "negative_control_scan_v02.json"
with open(path, "w", encoding="utf-8") as fp:
    json.dump(out, fp, ensure_ascii=False, indent=2)
print(json.dumps(out, ensure_ascii=False, indent=2))
