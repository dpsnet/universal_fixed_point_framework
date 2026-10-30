# -*- coding: utf-8 -*-
"""P3 负控基线扫描（104az-200 §10 P3 落地 v0.1，2026-10-21）
模板族 T6：分数 a/b，b 的素因子 ⊆ {2,3,5,7,11,13} 且 1 ≤ b ≤ 5000。
统一容差 tol = 1e-3（0.1% 相对）。
对目标 t：族内所有 |a/b − t| ≤ tol·t 的简化分数 = 命中。
指标：命中数（简化分数去重）、最精确命中 dev_min。
decoy 族：D1 随机 8-smooth 常数 30 个；D2 扰动观测 5 个；D3 已知错值 3 个/目标。
判定（草案）：真实 dev_min ≤ 0.1 × decoy 平均 dev_min（精确一个数量级）→ 负控通过。
"""
import math, json, random
from fractions import Fraction

PRIMES = [2, 3, 5, 7, 11, 13]
TOL = 1e-3

def smooth_denoms(maxv):
    s = {1}
    frontier = {1}
    while frontier:
        newf = set()
        for x in frontier:
            for p in PRIMES:
                y = x * p
                if y <= maxv:
                    newf.add(y)
                    s.add(y)
        frontier = newf
    return sorted(s)

def prime_factors(n):
    n = abs(n)
    fs = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            fs.append(d)
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        fs.append(n)
    return fs

def scan(t, denoms):
    """返回 (命中简化分数 dict, dev_min, best Fraction)"""
    hits = {}
    for b in denoms:
        a = round(t * b)
        if a < 1:
            continue
        v = a / b
        if abs(v - t) <= TOL * abs(t):
            fr = Fraction(a, b)
            hits[fr] = v
    if not hits:
        return hits, None, None
    best = min(hits, key=lambda fr: abs(float(fr) - t))
    dev_min = abs(float(best) - t) / abs(t)
    return hits, dev_min, best

def rand_smooth(t, rng):
    e = {p: rng.randint(0, 10) for p in [2, 3, 5, 7]}
    r = (2 ** e[2]) * (3 ** e[3]) * (5 ** e[5]) * (7 ** e[7])
    k = 0
    while r < t / 2:
        r *= 2; k += 1
    while r > 2 * t:
        r /= 2; k -= 1
    return r

TARGETS = {
    "κΛ":        401.73304855,   # 定义值（104az-103）
    "g_p/2":     2.79284734463,  # CODATA 2018
    "m_t/m_b":   41.284,         # PDG 中心口径（104az-169）
    "1/α":       137.035999084,  # CODATA 2018
    "21/100":    0.21,           # 巴耳末精确
}

D3_WRONG = {
    "κΛ":     [400 * (1 + 1/230), 400 * (1 + 1/232), 400.0],
    "g_p/2":  [40213/14400, 40217/14401, 2.79280],
    "m_t/m_b":[41.0, 41.3134 * 1.001, 42.0],
    "1/α":    [137.028, 136.993, 137.01],
    "21/100": [0.209, 0.211, 0.2],
}

FRAME = {
    "κΛ":      92800/231,
    "g_p/2":   40217/14400,
    "m_t/m_b": 167321/4050,
    "1/α":     24*(16259/6000 + 3),
    "21/100":  0.21,
}

def main():
    rng = random.Random(20261021)
    denoms = smooth_denoms(5000)
    print(f"模板族 T6 大小（b ≤ 5000，素因子⊆{{2,3,5,7,11,13}}）: {len(denoms)}")
    print("=" * 120)

    report = {}
    for name, t in TARGETS.items():
        hits, dev_min, best = scan(t, denoms)
        n_hit = len(hits)

        # decoy D1：随机 8-smooth
        d1_devs, d1_n = [], 0
        for _ in range(30):
            r = rand_smooth(t, rng)
            h, d, _ = scan(r, denoms)
            if d is not None:
                d1_devs.append(d); d1_n += len(h)
        # decoy D2：扰动
        d2_devs, d2_n = [], 0
        for delta in [1e-3, -1e-3, 1e-2, -1e-2, 5e-2]:
            h, d, _ = scan(t * (1 + delta), denoms)
            if d is not None:
                d2_devs.append(d); d2_n += len(h)
        # decoy D3：错值
        d3_devs, d3_n = [], 0
        for w in D3_WRONG[name]:
            h, d, _ = scan(w, denoms)
            if d is not None:
                d3_devs.append(d); d3_n += len(h)

        all_d = d1_devs + d2_devs + d3_devs
        avg_dev = sum(all_d) / len(all_d) if all_d else None
        min_dev = min(all_d) if all_d else None
        passed = (dev_min is not None and avg_dev is not None
                  and dev_min <= 0.1 * avg_dev)

        # 框架表达式自身 dev（对照）
        fw = FRAME[name]
        fw_dev = abs(fw - t) / abs(t) if abs(fw - t) > 0 else 0.0
        fr_fw = Fraction(fw).limit_denominator(10**9)

        print(f"目标 {name} = {t:.9f}")
        if best is not None:
            print(f"  命中数(≤0.1%): {n_hit}   dev_min = {format(dev_min, '.3e')}   best = {best.numerator}/{best.denominator}（分子素因子 {prime_factors(best.numerator)}，分母 {best.denominator}）")
        else:
            print(f"  命中数(≤0.1%): {n_hit}   dev_min = NA")
        print(f"  框架表达式对照: {fr_fw.numerator}/{fr_fw.denominator} = {fw:.9f}（对目标 dev = {format(fw_dev, '.3e')}）")
        print(f"  D1 随机(30): 命中总数 {d1_n}, dev 均值 {format(sum(d1_devs)/len(d1_devs), '.3e') if d1_devs else 'NA'}")
        print(f"  D2 扰动(5):  命中总数 {d2_n}, dev 均值 {format(sum(d2_devs)/len(d2_devs), '.3e') if d2_devs else 'NA'}")
        print(f"  D3 错值(3):  命中总数 {d3_n}, dev 均值 {format(sum(d3_devs)/len(d3_devs), '.3e') if d3_devs else 'NA'}")
        print(f"  decoy 全部:  平均 dev = {format(avg_dev, '.3e') if avg_dev else 'NA'}  min dev = {format(min_dev, '.3e') if min_dev else 'NA'}")
        print(f"  负控判定(真实 dev_min ≤ 0.1×decoy 平均 dev): {'通过 ✅' if passed else '未通过 ❌'}")
        print("-" * 120)

        report[name] = {
            "target": t, "n_hit": n_hit, "dev_min": dev_min,
            "best": (str(best) if best else None),
            "best_num_factors": (prime_factors(best.numerator) if best else None),
            "best_den": (best.denominator if best else None),
            "fw": fw, "fw_dev": fw_dev,
            "d1_avg_dev": (sum(d1_devs)/len(d1_devs) if d1_devs else None),
            "d2_avg_dev": (sum(d2_devs)/len(d2_devs) if d2_devs else None),
            "d3_avg_dev": (sum(d3_devs)/len(d3_devs) if d3_devs else None),
            "decoy_avg_dev": avg_dev, "decoy_min_dev": min_dev,
            "passed": passed,
        }

    with open("negative_control_scan.json", "w", encoding="utf-8") as f:
        json.dump({"denom_set_size": len(denoms), "tol": TOL, "report": report},
                  f, ensure_ascii=False, indent=2)
    print("已输出 negative_control_scan.json")

if __name__ == "__main__":
    main()
