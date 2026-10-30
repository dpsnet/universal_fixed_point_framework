# -*- coding: utf-8 -*-
"""③ 通用 8 分割解析判定器：28 情形先证伪基座。

输入 (8sg tuple, E6, E7, hx)，机械推导 8 分割贡献和 A_BG 预测：
  c1234  = 0（单块 V=Ṽ=1）
  c123_4 = -s51 · Ā₍₂₃₄₎，Ā₍₂₃₄₎ = -s23·s34·θ⁺(s234·s23)·θ⁺(hx·s34)
  c12_34 = 0（2 元素块）
  c12_3_4 = 0（2 元素块）
  c1_234 = (-s12) · (-s34·s45·θ⁺(E6·s34)·θ⁺(E7·s45))   （活分割，两块）
  c1_23_4 = 0（2 元素块）
  c1_2_34 = 0（2 元素块）
  c1_2_3_4 = s23·s34·s45·(∏θ⁺(r) - ∏θ⁻(r))，r=(s23·s12, s34·s123, s45·s51)
  A_BG = -(Σ c)
恒等式依赖：E-a [λ₂,λ₃₄₅]=[λ₁,λ₂]→s12；E-b [λ₂₃,λ₄₅]=[λ₁,λ₂₃]→s123；
E-c [λ₂₃₄,λ₅]=[λ₅,λ₁]→s51；推论5.3 C0 [λ₃,λ₄₅]=[λ₁₂,λ₃]→E6、C1 [λ₃₄,λ₅]=[λ₁₂,λ₃₄]→E7。
hx = sg([λ₂₃,λ₄])（非 8sg 投影序事实，数值侧由采样给出）。

对 14 模式 × 可达 (E6,E7,hx) 组合全验证 vs 采样 A_BG 真值。0 违反才可 Lean 化。
"""
import sys
import json
import random
from collections import defaultdict

sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_jump_symbol_map import sg_pattern5

HARD = {(1, 1, -1, -1, 1, -1, -1, 1), (-1, -1, 1, 1, -1, 1, 1, -1)}
SINGLE_6 = {
    (1, 1, -1, -1, -1, -1, 1, -1), (-1, -1, 1, 1, 1, 1, -1, 1),
    (1, 1, -1, -1, 1, -1, 1, 1), (1, 1, -1, -1, 1, 1, 1, 1),
    (-1, -1, 1, 1, -1, -1, -1, -1), (1, 1, 1, 1, -1, -1, 1, -1),
    (-1, -1, -1, -1, 1, 1, -1, 1), (-1, -1, 1, 1, -1, 1, -1, -1),
}
SINGLE_7 = {
    (-1, 1, -1, -1, -1, -1, 1, -1), (1, -1, 1, 1, 1, 1, -1, 1),
    (1, -1, -1, -1, 1, 1, -1, 1), (1, 1, -1, -1, 1, 1, -1, 1),
    (-1, 1, 1, 1, -1, -1, 1, -1), (-1, -1, 1, 1, -1, -1, 1, -1),
}
TARGET = SINGLE_6 | SINGLE_7


def thetaP(r):
    return 1 if r == -1 else 0


def thetaM(r):
    return 1 if r == 1 else 0


def ext_sgs(omega, zbar):
    return (sg_block(omega, zbar, (0, 1), (0, 1, 2)), sg_block(omega, zbar, (0, 1), (0, 1, 2, 3)))


def h_extra(omega, zbar):
    return sg_block(omega, zbar, (1, 2), (3,))


def abg_predict(s12, s23, s34, s45, s51, s123, s234, s1234, e6, e7, hx):
    """通用 8 分割贡献和（Lean N5HardModeA 结构的参数化）"""
    s = dict(s12=s12, s23=s23, s34=s34, s45=s45, s51=s51, s123=s123, s234=s234, s1234=s1234)
    # c123_4 = -s51·Ā₍₂₃₄₎ = -s51·(-s23·s34·θ⁺(s234·s23)·θ⁺(hx·s34))
    c123_4 = -s["s51"] * (-s["s23"] * s["s34"] * thetaP(s["s234"] * s["s23"]) * thetaP(hx * s["s34"]))
    # c1_234 = (-s12)·(-s34·s45·θ⁺(E6·s34)·θ⁺(E7·s45))
    c1_234 = (-s["s12"]) * (-s["s34"] * s["s45"] * thetaP(e6 * s["s34"]) * thetaP(e7 * s["s45"]))
    # c1_2_3_4 = s23·s34·s45·(∏θ⁺ - ∏θ⁻)，r=(s23·s12, s34·s123, s45·s51)
    r = (s["s23"] * s["s12"], s["s34"] * s["s123"], s["s45"] * s["s51"])
    tp = thetaP(r[0]) * thetaP(r[1]) * thetaP(r[2])
    tm = thetaM(r[0]) * thetaM(r[1]) * thetaM(r[2])
    c1_2_3_4 = s["s23"] * s["s34"] * s["s45"] * (tp - tm)
    total = c123_4 + c1_234 + c1_2_3_4  # 其余 5 项 = 0
    return -total


def main():
    rng = random.Random(20261003)
    bykey = defaultdict(list)  # (pat, e6, e7, hx) -> [a 真值]
    n = 400000
    for _ in range(n):
        omega, zbar, pairs = gen_partial_collinear(5, 0, r1=True, momentum=True, rng=rng)
        pat = sg_pattern5(omega, zbar)
        if pat not in TARGET:
            continue
        a = A_BG(5, omega, zbar)
        e6, e7 = ext_sgs(omega, zbar)
        hx = h_extra(omega, zbar)
        bykey[(pat, e6, e7, hx)].append(a)
    viol = 0
    ncase = 0
    print("=== 通用 8 分割解析判定器 vs 采样真值（14 模式全部 (E6,E7,hx) 组合） ===")
    for (pat, e6, e7, hx), lst in sorted(bykey.items(), key=lambda kv: kv[0]):
        s12, s23, s34, s45, s51, s123, s234, s1234 = pat
        pred = abg_predict(s12, s23, s34, s45, s51, s123, s234, s1234, e6, e7, hx)
        truevals = set(round(x, 6) for x in lst)
        ncase += 1
        ok = all(abs(round(x, 6) - pred) < 1e-6 for x in truevals) and (pred in truevals or all(x == 0.0 for x in truevals))
        # 判定器必须精确预测采样真值（含 0 情形）
        if not all(abs(round(x, 6) - pred) < 1e-6 for x in truevals):
            viol += 1
            print(f"违反: pat={pat} E6={e6} E7={e7} hx={hx} 预测={pred} 真值={truevals}")
    print(f"共 {ncase} 组合，违反 {viol}")
    assert viol == 0
    print("全 PASS")

    # 输出 28 情形表（模式 → 因子列值 → A_BG 预测，供 Lean 定理目标）
    table = defaultdict(dict)
    for (pat, e6, e7, hx), lst in sorted(bykey.items(), key=lambda kv: kv[0]):
        pred = abg_predict(*pat, e6, e7, hx)
        col = 6 if pat in SINGLE_6 else 7
        fv = e6 if col == 6 else e7
        table[str(pat)][str(fv)] = pred
    with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n5_single14_analytic_results.json", "w", encoding="utf-8") as f:
        json.dump({"table": {k: {fv: v for fv, v in d.items()} for k, d in table.items()},
                   "n_combos": ncase, "violations": viol}, f, ensure_ascii=False, indent=1)
    print("DONE -> scripts/paperX_n5_single14_analytic_results.json")


if __name__ == "__main__":
    main()
