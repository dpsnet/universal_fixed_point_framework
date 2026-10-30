# -*- coding: utf-8 -*-
"""
S427 投影特征规则 R-proj 数值先证伪（2026-10-29）

问题：S419 五口径偏移
  Cs  = -(5/2)*ln15*e^-19   (Parker 2018)
  a_e = +2*ln15*e^-18      (Fan 2023)
  Rb  = +8*e^-18           (Morel 2020)
  Zero = 0                 (CODATA 2018 基底直中)
  Q22 = +16*sigma^7        (CODATA 2022)
的 链选择 / 系数 / 指数 是否具有生成链语义（R-proj 受限空间），
还是"任意可凑"（宽空间同样能凑）？

规则 R-proj（候选，本脚本先证伪）：
  [链] 通道代数域 -> 三重投影域：时空->d_H=ln15；统计->e；冻结->sigma
  [系数] c ∈ F（框架常数集）
        F = {2=Powers, 5/2=SU/P, 3=Ngen, 5=SilenceUnit, 7=Involution,
             8=Kmax, 16=全态, 24=4!}
  [指数] d_H 域: n ∈ {18=SigmaInv+Ngen, 19=SigmaInv+FixedPoint}
          e 域:   n = 18（=SigmaInv+Ngen）
          sigma 域: k ∈ sigma 幂次谱 {3,5,7,8}
  [符号] d_H 可 ±（Z2 分次双向）；e / sigma 只 +

检验：
  A. R-proj 空间枚举（全空间有限，约 100+ 构造）——对 4 个非零
     真实口径计算 sigma_score = |构造值 - 真实偏移| / u(通道)
     命中判据 sigma_score <= 1（达标级）
     -> 输出全部命中点。判别：真实构造是否命中且命中点是否稀少。
  B. 宽空间对照（系数 1..30、指数 5..25、链任意、符号任意）随机
     采样 30000 构造，统计"命中任一真实口径"概率。
     -> 若宽空间命中率显著高于 R-proj 空间，说明受限规则确有判别力。

数值口径（全部与 S418/S419 一致，verbatim）：
  基底（MUFPF 理论值） M = 137.035999083426
  Cs   = 137.035999046(27)   u=2.7e-8
  a_e  = 137.035999166(16)   u=1.6e-8
  Rb   = 137.035999206(11)   u=1.1e-8
  Q22  = 137.035999177(21)   u=2.1e-8
  ln15 = 2.70805020110221
  e    = 2.718281828459045
  sigma= 1/15
"""
import math
import random

# ---------- 框架常数 ----------
ln15 = 2.70805020110221
EULER = math.e
SIGMA = 1.0 / 15.0
SIGMA_POWERS = (3, 5, 7, 8)
F = {
    "Powers(2)": 2.0,
    "SU/P(5/2)": 2.5,
    "Ngen(3)": 3.0,
    "SilenceUnit(5)": 5.0,
    "Involution(7)": 7.0,
    "Kmax(8)": 8.0,
    "All16": 16.0,
    "FourFact(24)": 24.0,
}

# ---------- 真实口径（相对基底的偏移） ----------
BASE = 137.035999083426
CHANNELS = {
    "Cs_2018": (137.035999046 - BASE, 2.7e-8),
    "a_e_2023": (137.035999166 - BASE, 1.6e-8),
    "Rb_2020": (137.035999206 - BASE, 1.1e-8),
    "Q22_2022": (137.035999177 - BASE, 2.1e-8),
}

# ---------- R-proj 空间枚举 ----------
def build_rproj_space():
    space = []  # (链, 系数名, 指数, 符号, 值)
    # d_H 域: c * ln15 * e^-n, n in {18,19}, 符号 ±
    for name, c in F.items():
        for n in (18, 19):
            v = c * ln15 * (EULER ** (-n))
            space.append(("d_H", name, n, -1.0, -v))
            space.append(("d_H", name, n, +1.0, +v))
    # e 域: c * e^-18, 只 +
    for name, c in F.items():
        v = c * (EULER ** (-18))
        space.append(("e", name, 18, +1.0, +v))
    # sigma 域: c * sigma^k, k in {3,5,7,8}, 只 +
    for name, c in F.items():
        for k in SIGMA_POWERS:
            v = c * (SIGMA ** k)
            space.append(("sigma", name, k, +1.0, +v))
    return space

def hit_check(construction, channel):
    delta_real, u = CHANNELS[channel]
    score = abs(construction - delta_real) / u
    return score, score <= 1.0

def run_projection_enumeration():
    space = build_rproj_space()
    print(f"R-proj 空间总构造数: {len(space)}")
    print("=" * 90)
    for ch in CHANNELS:
        delta_real, u = CHANNELS[ch]
        hits = []
        for (chain, cname, expo, sign, val) in space:
            score, ok = hit_check(val, ch)
            if ok:
                hits.append((score, chain, cname, expo, sign, val))
        hits.sort(key=lambda h: h[0])
        print(f"\n通道 {ch}: 真实偏移 {delta_real:+.4e} (u={u:.1e})  命中 {len(hits)} 个构造")
        for (score, chain, cname, expo, sign, val) in hits:
            marker = "  <<< 真实构造" if is_actual(ch, chain, cname, expo, sign) else ""
            print(f"   sigma_score={score:6.3f}  {chain:>5s}  c={cname:>14s}  "
                  f"指数={expo} 符号={'+' if sign > 0 else '-'}  构造={val:+.4e}{marker}")
    return space

def is_actual(ch, chain, cname, expo, sign):
    actual = {
        "Cs_2018": ("d_H", "SU/P(5/2)", 19, -1.0),
        "a_e_2023": ("d_H", "Powers(2)", 18, +1.0),
        "Rb_2020": ("e", "Kmax(8)", 18, +1.0),
        "Q22_2022": ("sigma", "All16", 7, +1.0),
    }[ch]
    return (chain, cname, expo, sign) == actual

def run_wide_space():
    """宽空间对照：系数 1..30（整数/半整数）、指数 5..25、链任意、符号任意"""
    random.seed(20261029)
    n_samples = 30000
    hit_count = 0
    hit_detail = {}
    hit_scores = []   # S427b：记录全部命中构造的 sigma_score
    for _ in range(n_samples):
        c = random.choice([0.5 * i for i in range(2, 61)])  # 1.0 .. 30.0 步长 0.5
        expo = random.randint(5, 25)
        chain = random.choice(["d_H", "e", "sigma"])
        sign = random.choice([-1.0, 1.0])
        if chain == "d_H":
            v = sign * c * ln15 * (EULER ** (-expo))
        elif chain == "e":
            v = sign * c * (EULER ** (-expo))
        else:
            v = sign * c * (SIGMA ** expo)
        best_score = None
        for ch in CHANNELS:
            score, ok = hit_check(v, ch)
            if ok:
                best_score = score
                hit_count += 1
                hit_detail.setdefault(ch, 0)
                hit_detail[ch] += 1
                break
        if best_score is not None:
            hit_scores.append(best_score)
    print("=" * 90)
    print(f"宽空间对照（30000 随机构造，系数 1-30、指数 5-25、链任意、符号任意）")
    print(f"  命中任一真实口径: {hit_count} / 30000 = {hit_count/30000*100:.2f}%")
    for ch in hit_detail:
        print(f"    {ch}: {hit_detail[ch]} 次")
    # S427b：命中构造的 sigma_score 分布
    if hit_scores:
        hit_scores_sorted = sorted(hit_scores)
        n = len(hit_scores_sorted)
        med = hit_scores_sorted[n // 2] if n % 2 == 1 else \
            (hit_scores_sorted[n // 2 - 1] + hit_scores_sorted[n // 2]) / 2
        mn = hit_scores_sorted[0]
        q25 = hit_scores_sorted[n // 4]
        q75 = hit_scores_sorted[3 * n // 4]
        frac_below_01 = sum(1 for s in hit_scores_sorted if s < 0.1) / n
        frac_below_07 = sum(1 for s in hit_scores_sorted if s < 0.07) / n
        print(f"\n[S427b] 宽空间命中构造的 sigma_score 分布（n={n}）:")
        print(f"  min={mn:.3f}  Q25={q25:.3f}  中位数={med:.3f}  Q75={q75:.3f}")
        print(f"  sigma_score < 0.10 的比例: {frac_below_01*100:.2f}%")
        print(f"  sigma_score < 0.07 的比例: {frac_below_07*100:.2f}%")
        print(f"  真实四构造 sigma_score: Cs=0.019, a_e=0.005, Rb=0.067, Q22=0.003")
        print(f"  -> 判别：若宽空间命中分数几乎都 >= 0.1（占比极低），则"
              f"真实构造的 0.003-0.067 精度是 R-proj 结构性质，非普遍性质")

if __name__ == "__main__":
    run_projection_enumeration()
    run_wide_space()
