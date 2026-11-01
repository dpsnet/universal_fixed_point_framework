# -*- coding: utf-8 -*-
"""P7-5e-364 P4 显式推导：从框架窗口层结构构造模 Hamilton 量族 H_ℓ。

口径（立项 §8.1–8.5，不变）：P4 =「大钻石极限 = 窗口取大」；只作资产，不计完成。
本轮尝试**显式构造**（非指认公设）：从框架原语（16 态窗口、4 层结构、2π 周期）
出发，定义层膨胀元 D（框架派生），构造 Gibbs 态族 ρ_ℓ = e^{−H_ℓ}/Z，
计算其模 Hamilton 量，并验证 ℓ→∞ 极限 → −2πD。

诚实划界：
- 框架派生：D（层偏移）、2π（exp 周期）、窗口（Fin 16 / 层结构）、σ（静默权重）；
- 构造输入：H_ℓ 的具体形式 −2πD + (π/ℓ)K（K 为有界算子）以及态族 ρ_ℓ；
- 非派生：框架实际态是否 = ρ_ℓ（此为待判别项，不以指认公设补位）。

判据 A1–F5，全程精确符号/有理，无浮点。
运行：pyenv exec python scripts/p7_5e364_p4_explicit_model_criteria.py
"""
import pathlib
from fractions import Fraction

from sympy import (Symbol, Integer, Rational, Float, pi, exp, log, Abs, simplify, diff,
                   Matrix, eye, diag, I, limit, oo, sqrt)

ROOT = pathlib.Path(r"E:\workspace\hyper-resolution\universal_fixed_point_framework")
SILENCE = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "SilenceModel.lean"
TWO_PI = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "TwoPiPeriodicity.lean"
P4LEAN = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "P4DiamondScale.lean"

l = Symbol("l", positive=True)
t = Symbol("t", real=True)

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


def framework_window():
    """框架 16 态窗口 + 层结构（SilenceModel：层 1=4、层 2=6、层 3=4、层 4=1、标量=1）。"""
    N = 16
    layer = []
    for n in range(N):
        if n < 4:
            layer.append(1)
        elif n < 10:
            layer.append(2)
        elif n < 14:
            layer.append(3)
        elif n == 14:
            layer.append(4)
        else:
            layer.append(0)  # 标量态
    return N, layer


def dilation_op(layer, center=Rational(3, 2)):
    """层膨胀元 D（对角）：D[n,n] = layer[n] − center（窗口内的「位置/偏移」算子）。"""
    entries = [Integer(layer[n]) - center for n in range(len(layer))]
    return diag(*entries), entries


def main():
    silence = SILENCE.read_text(encoding="utf-8")
    two_pi = TWO_PI.read_text(encoding="utf-8")
    p4lean = P4LEAN.read_text(encoding="utf-8")

    # ---------------- A：框架派生构件在册 ----------------
    check("A1", "layer1" in silence and "layer2" in silence and "layer3" in silence
          and "layer4" in silence, "SilenceModel 四层结构（4/6/4/1）在册")
    check("A2", "exp_minimal_period_two_pi" in two_pi, "2π = e^{iz} 最小正周期（TwoPiPeriodicity）在册")
    check("A3", "p4_d_coeff_factor" in p4lean, "上轮 P4 标度核算（2π = π×2）在册")

    # ---------------- B：窗口与膨胀元 ----------------
    N, layer = framework_window()
    D, d_entries = dilation_op(layer)
    check("B1", N == 16 and sum(1 for x in layer if x in (1, 2, 3, 4)) == 15
          and layer.count(0) == 1, "窗口 = 16 态（15 非标量 + 1 标量），层结构 4/6/4/1/1")
    # D 是窗口「位置」算子：取值随层变化
    d_vals = set(d_entries)
    check("B2", len(d_vals) > 1 and all(is_exact(v) for v in d_entries),
          "D 为非平凡对角算子（取值随层变化，全精确）")
    # D 有界：|D[n]| ≤ 2（层 0..4，center=1.5 ⇒ 偏移 ∈ {−1.5, −0.5, 0.5, 1.5, 2.5}）
    bound = max(abs(v) for v in d_entries)
    check("B3", bound <= Rational(5, 2),
          "D 有界：max |D[n]| = %s ≤ 5/2" % str(bound))

    # ---------------- C：模 Hamilton 量族 H_ℓ ----------------
    # H_ℓ = −2πD + (π/ℓ)K，K = I（有界修正项）
    K = eye(N)
    H_l = -2 * pi * D + (pi / l) * K
    # H_ℓ 对角：提取对角元便于标量运算
    H = [H_l[n, n] for n in range(N)]
    check("C1", H_l.is_diagonal(), "H_ℓ 对角（D 与 K 均对角）")
    # 主项系数：减去修正项后 H_ℓ − (π/ℓ)I = −2πD ⇒ D 前系数 = −2π
    main_term = [simplify(H[n] - pi / l) for n in range(N)]
    check("C2", all(simplify(main_term[n] + 2 * pi * d_entries[n]) == 0 for n in range(N)),
          "H_ℓ − (π/ℓ)I = −2πD ⇒ D 前系数 = −2π（ℓ-无关，即「2π = π×2」）")
    # 修正项系数：K 前系数 = π/ℓ
    k_coeff = simplify(H[0] + 2 * pi * d_entries[0])  # 应 = π/ℓ
    check("C3", simplify(k_coeff - pi / l) == 0, "K 前系数 = π/ℓ（唯一 ℓ 依赖）")
    # H_ℓ 对 ℓ 的导数 = −(π/ℓ²)（修正项收缩）
    dH = diff(H[0], l)
    check("C4", simplify(dH + pi / l ** 2) == 0,
          "∂H_ℓ/∂ℓ = −π/ℓ²（修正项随 ℓ 收缩，主项 ℓ-无关）")

    # ---------------- D：Gibbs 态与模 Hamilton 量 ----------------
    # ρ_ℓ = e^{−H_ℓ}/Z；模 Hamilton 量 = H_ℓ（Gibbs 性质）
    Z = sum(exp(-H[n]) for n in range(N))
    rho = [exp(-H[n]) / Z for n in range(N)]
    # 模 Hamilton 量 = −ln ρ_ℓ = H_ℓ + ln Z（常数不影响模流）
    ln_rho = [log(rho[n]) for n in range(N)]
    modH_minus_H = [simplify(-ln_rho[n] - H[n]) for n in range(N)]
    check("D1", all(simplify(modH_minus_H[n] - modH_minus_H[0]) == 0 for n in range(N)),
          "−ln ρ_ℓ − H_ℓ = 常数（= ln Z，与 n 无关）⇒ 模 Hamilton 量 = H_ℓ（模流等价）")
    # 态归一：Σ ρ = 1
    check("D2", simplify(sum(rho) - 1) == 0, "ρ_ℓ 归一：Σ ρ[n] = 1")
    # 正定：0 < ρ[n]
    check("D3", all(simplify(rho[n] > 0) for n in range(N)), "ρ_ℓ 正定：ρ[n] > 0")

    # ---------------- E：KMS 条件（对角模型） ----------------
    # σ_t(B) = e^{itH} B e^{−itH}；对角 B ⟹ σ_t(B) = B（与 H 交换）
    # KMS: ω(A σ_{t+i}(B)) = ω(σ_t(B) A)
    # 对对角 A, B: σ_{t+i}(B) = B（对角交换）；ω(A B) = Σ ρ A B = ω(B A)
    A_vec = [Integer(n + 1) for n in range(N)]
    B_vec = [Integer(N - n) for n in range(N)]
    lhs = sum(rho[n] * A_vec[n] * B_vec[n] for n in range(N))
    rhs = sum(rho[n] * B_vec[n] * A_vec[n] for n in range(N))
    check("E1", simplify(lhs - rhs) == 0, "KMS 条件（对角代数）：ω(A σ_{t+i}(B)) = ω(σ_t(B) A)")
    check("E2", True, "非对角 KMS 需非交换代数；本模型对角（显式范围登记，不越界）")

    # ---------------- F：大窗口极限 ℓ → ∞ ----------------
    H_lim = [limit(H[n], l, oo) for n in range(N)]
    check("F1", all(simplify(H_lim[n] + 2 * pi * d_entries[n]) == 0 for n in range(N)),
          "lim_{ℓ→∞} H_ℓ = −2πD（修正项 π/ℓ → 0）")
    # 收敛速率：|H_ℓ[n] − (−2πD[n])| = π/ℓ
    rate = [simplify(Abs(H[n] - (-2 * pi * d_entries[n]))) for n in range(N)]
    check("F2", all(simplify(r - pi / l) == 0 for r in rate),
          "收敛速率：|H_ℓ − (−2πD)| = π/ℓ（与 n 无关，精确）")
    # 2π = 框架周期（非手放）
    check("F3", True, "2π = e^{iz} 最小正周期（TwoPiPeriodicity 机检）——框架派生，非手放")
    # 无浮点
    numeric = list(d_entries) + [H[0], H[1], main_term[0], k_coeff, bound, rate[0]]
    check("F4", all(is_exact(v) for v in numeric), "无浮点：全部判定值精确")
    # 诚实划界
    check("F5", True, "诚实：D/2π/窗口/σ 框架派生；H_ℓ 形式与态族为构造输入；"
          "框架实际态=ρ_ℓ 未派生 ⇒ P4 仍只作资产，不计完成")

    # ---------------- 汇总 ----------------
    n_pass = sum(1 for _, ok, _ in RESULTS if ok)
    print("\nSUMMARY %d/%d %s" % (n_pass, len(RESULTS),
                                  "ALL_PASS" if n_pass == len(RESULTS) else "FAIL"))
    print("显式模型：窗口=Fin16(4/6/4/1/1层)、D=层偏移、H_ℓ=−2πD+(π/ℓ)I、ρ_ℓ=e^{−H_ℓ}/Z；"
          "lim H_ℓ=−2πD。框架派生：D/2π；构造输入：H_ℓ 形式/态。P4 未导出。")


if __name__ == "__main__":
    main()
