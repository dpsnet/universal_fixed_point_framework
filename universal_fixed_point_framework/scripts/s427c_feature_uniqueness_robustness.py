# -*- coding: utf-8 -*-
"""
S427c 投影特征唯一性鲁棒性检验（2026-10-29）

S427 已示：R-proj 受限空间（72 构造）内 4 个实验偏移各自
σ_score 唯一近零（0.003-0.067），空间内 <0.07σ 点恰 4 = 通道数。

本检验回答开放项 2b 前半："最佳命中=投影特征"的唯一性是否
鲁棒——把 系数空间（1-42 整数+半整数）与 指数空间（5-25）
同时放宽，<0.1σ 的命中点是否仍唯一且恰为真实构造
{5/2, 2, 8, 16} x {19, 18, 18, 7}？

若唯一性保持：真实构造是"全域自然唯一近零点"——R-proj
空间不是被裁剪到只剩真实构造——'投影特征 = 唯一近零构造'
是框架生成链的自然结构（开放项 2b 前半闭合）。
若出现新近零命中：唯一性崩坏——判别需语义命名（S421 式），
R-proj 升格降级。

口径（verbatim，同 S418/S419）：
  基底 M = 137.035999083426
  Cs = 137.035999046(27)  -> delta -3.7426e-8, u 2.7e-8
  a_e= 137.035999166(16)  -> delta +8.2574e-8, u 1.6e-8
  Rb = 137.035999206(11)  -> delta +1.2257e-7, u 1.1e-8
  Q22= 137.035999177(21)  -> delta +9.3574e-8, u 2.1e-8
  链值：d_H: c*ln15*e^-n ; e: c*e^-n ; sigma: c*(1/15)^k
"""
import math

ln15 = 2.70805020110221
EULER = math.e
SIGMA = 1.0 / 15.0
BASE = 137.035999083426

CHANNELS = {
    "Cs_2018": (137.035999046 - BASE, 2.7e-8),
    "a_e_2023": (137.035999166 - BASE, 1.6e-8),
    "Rb_2020": (137.035999206 - BASE, 1.1e-8),
    "Q22_2022": (137.035999177 - BASE, 2.1e-8),
}

ACTUAL = {
    "Cs_2018": ("d_H", 2.5, 19, -1.0),
    "a_e_2023": ("d_H", 2.0, 18, +1.0),
    "Rb_2020": ("e", 8.0, 18, +1.0),
    "Q22_2022": ("sigma", 16.0, 7, +1.0),
}

THRESHOLD = 0.1  # sigma_score 近零阈值


def score_of(chain, c, expo, sign, ch):
    if chain == "d_H":
        v = sign * c * ln15 * (EULER ** (-expo))
    elif chain == "e":
        v = sign * c * (EULER ** (-expo))
    else:
        v = sign * c * (SIGMA ** expo)
    delta_real, u = CHANNELS[ch]
    return abs(v - delta_real) / u


def scan():
    # 系数空间放宽：0.5 步长 1.0 .. 42.0（含 42=ConfinementDomain），
    # 另加框架关键量 {15, 24, 42, 48, 72}
    coeffs = [0.5 * k for k in range(2, 85)]
    coeffs += [15.0, 24.0, 42.0, 48.0, 72.0]
    coeffs = sorted(set(coeffs))
    # 指数空间放宽：5 .. 25（sigma 域 k 3 .. 25）
    print("=" * 96)
    print("S427c 唯一性鲁棒性：系数 1-42(半整数)+{15,24,42,48,72}，指数 5-25")
    print("  近零判定 sigma_score < 0.1")
    print("=" * 96)
    all_unique = True
    for ch in CHANNELS:
        delta_real, u = CHANNELS[ch]
        actual_chain, actual_c, actual_n, actual_s = ACTUAL[ch]
        hits = []
        for chain in ("d_H", "e", "sigma"):
            sign_choices = (-1.0, 1.0) if chain == "d_H" else (1.0,)
            for c in coeffs:
                for expo in range(5, 26):
                    for sign in sign_choices:
                        s = score_of(chain, c, expo, sign, ch)
                        if s < THRESHOLD:
                            marker = " <<< 真实" if (chain == actual_chain and abs(c - actual_c) < 1e-9
                                                     and expo == actual_n and sign == actual_s) else ""
                            hits.append((s, chain, c, expo, sign, marker))
        hits.sort(key=lambda h: h[0])
        print(f"\n通道 {ch}: 真实偏移 {delta_real:+.4e} (u={u:.1e})  <0.1σ 命中 {len(hits)} 个")
        for (s, chain, c, expo, sign, marker) in hits:
            print(f"   σ_score={s:.4f}  {chain:>5s}  c={c:6.1f}  指数={expo:2d}  "
                  f"符号={'+' if sign > 0 else '-'}{marker}")
        if len(hits) != 1 or not hits[0].endswith(" <<< 真实"):
            all_unique = False
    print("\n" + "=" * 96)
    if all_unique:
        verdict = "全部通道 <0.1σ 命中点唯一且恰为真实构造 —— 唯一性鲁棒，开放项2b 前半闭合"
    else:
        verdict = "存在非真实近零命中 —— 唯一性崩坏，需语义命名"
    print("唯一性判定：" + verdict)


if __name__ == "__main__":
    scan()
