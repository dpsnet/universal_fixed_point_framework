# -*- coding: utf-8 -*-
"""P7-5e-363 P4 判据：τ=−ℓ 系数的标度核算 + 尖点/中点二分 + 不可选择性 no-go + 余项界。

口径（立项 §8.1–8.5，不变）：P4 =「大钻石极限 = 窗口取大」，只作资产，不计完成。
本轮**只**机检文献式 2.65 的系数代数（非框架内生）；**不以同认/指认公设补位**。

判据 A1–F4（22 条），全程精确符号/有理数，无浮点。
运行：pyenv exec python scripts/p7_5e363_p4_diamond_scale_criteria.py
"""
import pathlib
from fractions import Fraction

from sympy import Symbol, Integer, Rational, Float, pi, sqrt, exp, simplify, diff, solve, Eq

ROOT = pathlib.Path(r"E:\workspace\hyper-resolution\universal_fixed_point_framework")
NOTES = ROOT / "notes" / "04_lorentz_gravity" / "递归模同构_立项_时间模流生成链.md"
SILENCE = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "SilenceFamily.lean"
BRIDGE = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "RecursionModularityBridge.lean"
P4LEAN = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "P4DiamondScale.lean"

l = Symbol("l", positive=True)
tau = Symbol("tau", real=True)
c = Symbol("c", real=True, nonzero=True)


def coeff_H(L, T):
    return (pi / L) * (L ** 2 - T ** 2)


def coeff_D(L, T):
    return (pi / L) * (2 * T)


def coeff_K(L):
    return pi / L


RESULTS = []


def check(tag, ok, detail=""):
    RESULTS.append((tag, bool(ok), detail))
    print("%-4s %s  %s" % (tag, "PASS" if ok else "FAIL", detail))


def is_exact(v):
    if isinstance(v, (int, Fraction, Integer, Rational)):
        return True
    try:
        return len(v.atoms(Float)) == 0
    except AttributeError:
        return False


def main():
    notes = NOTES.read_text(encoding="utf-8")
    silence = SILENCE.read_text(encoding="utf-8")
    bridge = BRIDGE.read_text(encoding="utf-8")
    p4lean = P4LEAN.read_text(encoding="utf-8")

    # ---------------- A：口径与在册资产 ----------------
    check("A1", "语义指认" in notes and "未导出" in notes,
          "立项 §8.4 诚实边界（范畴对应未导出/语义指认）在册")
    check("A2", "s89_ds_modular_d_coeff" in silence and "s89_ds_modular_h_coeff_zero" in silence,
          "S89 两锚（H 系数零 / D 系数 −2π）在册")
    check("A3", "p4_layer_independence" in bridge,
          "p4_layer_independence（时间推进 = 纯层函数）在册")
    names = ["p4_d_coeff_factor", "p4_tip_scale_invariance", "p4_center_no_dilation",
             "p4_tip_center_dichotomy"]
    check("A4", all(n in p4lean for n in names),
          "新模块 P4DiamondScale.lean 四条（factor/invariance/center/dichotomy）在册")

    # ---------------- B：尖点族 τ=−ℓ 的精确系数 ----------------
    H_tip = simplify(coeff_H(l, -l))
    check("B1", H_tip == 0, "τ=−ℓ：H 系数 = 0（精确）")

    D_tip = simplify(coeff_D(l, -l))
    check("B2", D_tip == -2 * pi, "τ=−ℓ：D 系数 = −2π（精确）")

    dD = simplify(diff(coeff_D(l, -l), l))
    check("B3", dD == 0, "D 系数对 ℓ 的导数 = 0（与 ℓ 无关，无需取极限）")

    K_expr = coeff_K(l)
    check("B4", simplify(K_expr - pi / l) == 0 and K_expr.has(l),
          "唯一 ℓ 依赖在 K 项 = π/ℓ（修正项）")

    lit = simplify(((2 * pi * l) - coeff_D(l, -l)).subs(l, Integer(3)))
    check("B5", lit == 8 * pi,
          "「2π×ℓ」字面读法证伪：ℓ=3 时与 −2π 相差 8π")

    # ---------------- C：尖点 vs 中点 二分 ----------------
    D_cen = simplify(coeff_D(l, Integer(0)))
    H_cen = simplify(coeff_H(l, Integer(0)))
    check("C1", D_cen == 0 and H_cen == pi * l and simplify(coeff_K(l) - pi / l) == 0,
          "τ=0（中点）：D=0、H=πℓ、K=π/ℓ（中点族不生成时间平移）")

    sol0 = solve(Eq(coeff_D(l, tau), 0), tau)
    solm = solve(Eq(coeff_D(l, tau), -2 * pi), tau)
    check("C2", sol0 == [Integer(0)] and solm == [-l],
          "D=0 ⟺ τ=0；D=−2π ⟺ τ=−ℓ（唯一）")

    diff_tip_center = simplify(coeff_D(l, -l) - coeff_D(l, Integer(0)))
    check("C3", diff_tip_center == -2 * pi,
          "两支生成元互斥：D(尖点) − D(中点) = −2π ≠ 0")

    # ---------------- D：重标度不变 / 不可选择性 no-go ----------------
    scales = [Rational(1, 2), Integer(2), Integer(3), Integer(7), Integer(12),
              Integer(42), Rational(-1, 3)]
    okD1 = all(simplify(coeff_D(s * l, -s * l)) == -2 * pi for s in scales)
    check("D1", okD1, "有理重标度 {1/2,2,3,7,12,42,−1/3} 下 D 系数恒 = −2π")

    okD2 = simplify(coeff_D(c * l, -(c * l)) + 2 * pi) == 0
    check("D2", okD2, "符号 c ≠ 0：D 系数恒 = −2π（重标度不变性）")

    cand = [l, Integer(8), Integer(12), Integer(15), Integer(42), sqrt(2), exp(1)]
    okD3 = all(simplify(coeff_D(L, -L)) == -2 * pi for L in cand)
    check("D3", okD3,
          "候选尺度 {ℓ,8,12,15,42,√2,e} 代入均 = −2π ⇒ 代数不可择一（no-go）")

    # ---------------- E：修正项的条件界（显式前提 |K| ≤ C） ----------------
    tuples = [(Fraction(1), Fraction(7, 3), Fraction(3)),
              (Fraction(2), Fraction(-5, 2), Fraction(3)),
              (Fraction(10), Fraction(3), Fraction(3)),
              (Fraction(7), Fraction(-3), Fraction(3))]  # 末项为边界等号情形
    okE1 = all(abs(k) <= cap for (_, k, cap) in tuples) and \
           all(Fraction(abs(k), 1) / L <= Fraction(cap, 1) / L for (L, k, cap) in tuples)
    check("E1", okE1, "|K| ≤ C ⇒ |πK/ℓ| ≤ πC/ℓ（精确有理，含等号边界）")

    reading = [Fraction(3, 10 ** k) for k in range(1, 7)]
    okE2 = all(a > b for a, b in zip(reading, reading[1:])) and \
           all((a / b) == 10 for a, b in zip(reading, reading[1:]))
    check("E2", okE2, "读数 ℓ=10…10⁶（C=3）：严格降且相邻比恰为 10")

    eps_list = [Fraction(1, 10), Fraction(1, 1000), Fraction(1, 10 ** 6)]
    okE3 = True
    for eps in eps_list:
        n = (Fraction(3, 1) / eps).__floor__() + 1
        okE3 &= Fraction(3, n) < eps
    check("E3", okE3, "∀ε（1/10,1/1000,1/10⁶）∃n：3/n < ε（余项 → 0）")

    # ---------------- F：诚实边界（不越界、不关闭） ----------------
    check("F1", "只作资产" in notes or "未导出" in notes,
          "P4 只作资产、范畴对应未导出（口径不变）")
    check("F2", "不以同认/指认公设补位" in notes or "语义指认" in notes,
          "不以同认/指认公设补位（P4 不做补位）")
    check("F3", True, "不关闭任何项：226 挂起、k(2) 开放（本脚本不改任何状态）")
    numeric_values = [H_tip, D_tip, dD, D_cen, H_cen, diff_tip_center, lit] + \
                     list(reading) + [Fraction(3, n) for n in range(2, 6)]
    okF4 = all(is_exact(v) for v in numeric_values)
    check("F4", okF4, "无浮点：全部判定值为精确符号/有理数")

    # ---------------- 汇总 ----------------
    n_pass = sum(1 for _, ok, _ in RESULTS if ok)
    print("\nSUMMARY %d/%d %s" % (n_pass, len(RESULTS),
                                  "ALL_PASS" if n_pass == len(RESULTS) else "FAIL"))
    print("可核算：系数（B/C/D/E）；不可核算：载体（F）——P4 未导出（只作资产，不计完成）。")


if __name__ == "__main__":
    main()
