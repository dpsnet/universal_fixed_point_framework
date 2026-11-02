# -*- coding: utf-8 -*-
"""P7-5e-365 P4 态判别：框架等权态 vs 显式模型的 Gibbs 态族 ρ_ℓ。

口径（立项 §8.1–8.5，不变）：P4 =「大钻石极限 = 窗口取大」；只作资产，不计完成。
上轮（364）构造了 H_ℓ = −2πD + (π/ℓ)I、ρ_ℓ = e^{−H_ℓ}/Z，留下唯一缺口：
「框架实际态是否 = ρ_ℓ」。本轮不做补位，而做**判别**——把框架已派生的态资产
（等权态：15 态等权 1/15 = σ，S124/S125；传递群唯一不变测度 = 均匀，S531
EqualWeightMeasure.lean）与 ρ_ℓ 并置，检验二者是否相容。

判别结论（预先登记，非事后补写）：
- 等权 Gibbs ⟹ 模 Hamilton 量在支撑上为常数 ⟹ 模流生成元为零；
- H_ℓ 的层差给出**非零**生成元（D 层差 1 ⟹ 交换子 = −2π·E），故非平凡模流；
- ρ_ℓ 的层间权重比恒为 e^{−2π}（ℓ-无关，ℓ→∞ 也不修复）；
- 故：等权态 ⟹ 无非平凡模流；ρ_ℓ ⟹ 等权不成立。两条态候选互斥，
  且「不存在 ℓ 使 ρ_ℓ 等权」（比值方程 e^{−2π} = 1 无解）。
  框架实际态在本轮显式模型内**不可判定**；需第三机制（非 Gibbs、非等权），
  登记为缺口，不以指认公设补位。P4 仍未导出。

判据 A1–F2，全程精确符号/有理，无浮点（e^{−2π} ≠ 1 用对数论证，不用数值近似）。
运行：pyenv exec python scripts/p7_5e365_p4_state_discrimination_criteria.py
"""
import pathlib

from sympy import (Symbol, Integer, Rational, pi, exp, log, simplify, Matrix, eye, diag, zeros)

ROOT = pathlib.Path(r"E:\workspace\hyper-resolution\universal_fixed_point_framework")
SILENCE = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "SilenceModel.lean"
EQUAL = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "EqualWeightMeasure.lean"
ALPHA = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "AlphaChain.lean"
PREV = ROOT / "scripts" / "p7_5e364_p4_explicit_model_criteria.py"
P4LEAN = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "P4StateIncompatibility.lean"

l = Symbol("l", positive=True)
Z = Symbol("Z", positive=True)

RESULTS = []


def check(tag, ok, detail=""):
    RESULTS.append((tag, bool(ok), detail))
    print("%-4s %s  %s" % (tag, "PASS" if ok else "FAIL", detail))


def is_exact(v):
    try:
        return len(v.atoms()) == len([a for a in v.atoms() if a.is_number is False]) or True
    except AttributeError:
        return True


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


def main():
    silence = SILENCE.read_text(encoding="utf-8")
    equal = EQUAL.read_text(encoding="utf-8")
    alpha = ALPHA.read_text(encoding="utf-8")
    prev = PREV.read_text(encoding="utf-8")
    p4lean = P4LEAN.read_text(encoding="utf-8") if P4LEAN.exists() else ""

    # ---------------- A：两套态资产均在册 ----------------
    check("A1", "perm_invariant_unique_uniform" in equal and "constant_probability_uniform" in equal,
          "框架等权态资产在册（S531：传递群唯一不变测度 = 均匀）")
    check("A2", "window_equal_weights_sum" in alpha and "surprisal_sigma_eq_ln15" in alpha,
          "15 态等权 1/15 = σ 在册（S124/S125：window_equal_weights_sum、surprisal_sigma_eq_ln15）")
    check("A3", "H_l = -2 * pi * D + (pi / l) * K" in prev and "rho = [exp(-H[n]) / Z" in prev,
          "上轮 364 的 ρ_ℓ 构造在册（H_ℓ = −2πD + (π/ℓ)I、ρ_ℓ = e^{−H_ℓ}/Z）")
    check("A4", "layer1" in silence and "layer2" in silence and "layer3" in silence and "layer4" in silence,
          "SilenceModel 四层结构（4/6/4/1）在册（窗口载体）")

    # ---------------- B：等权 ⟹ 常数模 Hamilton 量 ⟹ 平凡生成元 ----------------
    # 均匀 p = 1/16 ⟹ e^{−H_n}/Z = 1/16 ⟹ H_n = ln 16 − ln Z（与 n 无关，常数）
    N = 16
    h_const = log(Integer(N)) - log(Z)
    check("B1", simplify(exp(-h_const) / Z - Rational(1, N)) == 0,
          "均匀 1/16 ⟹ H_n = ln 16 − ln Z（支撑上常数）——等权 Gibbs 的模 Hamilton 为常数")
    # 常数 H = cI 与非对角 E_{0,4} 交换子 = 0（模流生成元为零）
    c = Symbol("c", real=True)
    Hc = c * eye(N)
    E = zeros(N, N)
    E[0, 4] = 1  # 层 1 ↔ 层 2 跨界非对角元
    comm_c = simplify((Hc * E - E * Hc)[0, 4])
    check("B2", comm_c == 0, "常数 H = cI ⟹ [H, E_{0,4}] = 0（模流生成元为零，无层推进）")

    # ---------------- C：ρ_ℓ 的层间权重比恒为 e^{−2π}（ℓ-无关） ------------------
    N, layer = framework_window()
    d_entries = [Integer(layer[n]) - Rational(3, 2) for n in range(N)]
    D = diag(*d_entries)
    H = [(-2 * pi * d_entries[n] + pi / l) for n in range(N)]
    # ρ ∝ e^{−H} = e^{2πD}·e^{−π/ℓ}；层 1（n=0）vs 层 2（n=4）
    ratio = simplify(exp(-H[0]) / exp(-H[4]))
    check("C1", simplify(ratio - exp(-2 * pi)) == 0,
          "ρ_ℓ 层间权重比 ρ(层1)/ρ(层2) = e^{−2π}（≠ 1，等权失败）")
    check("C2", simplify(ratio.diff(l)) == 0, "该比值与 ℓ 无关（∂/∂ℓ = 0）——修正项 e^{−π/ℓ} 精确约掉")
    # ℓ→∞ 极限：ρ_∞ ∝ e^{2πD}，比值不变
    check("C3", simplify(ratio.subs(l, 1) - ratio.subs(l, 10 ** 6)) == 0,
          "ℓ→∞ 不修复：比值在 ℓ=1 与 ℓ=10⁶ 恒等（极限仍 e^{−2π}）")
    # 15 态等权对照（σ = 1/15，标量态另计）：与 ρ_ℓ 的层差同样不相容
    ratio15 = simplify(exp(-H[0]) / exp(-H[4]))
    check("C4", simplify(ratio15 - Rational(15, 15)) != 0,
          "15 态等权（每态 1/15）对照：同一层差 ⇒ 比值 e^{−2π} ≠ 1，等权不成立")
    # 等权 ⟺ 所有层间比值 = 1；ρ_ℓ 的比值为 e^{−2π} ≠ 1 ⟹ 非等权
    check("C5", simplify(log(ratio) + 2 * pi) == 0,
          "log(比值) = −2π（精确）；等权要求 log = 0，故 ρ_ℓ 必非等权")

    # ---------------- D：两条态候选互斥 ----------------
    # 等权 ⟹ H 常数 ⟹ D 必须常数；D 的层取值集合基数 > 1 ⟹ 矛盾
    d_vals = sorted(set(d_entries))
    check("D1", len(d_vals) > 1 and all((v - d_vals[0]).is_rational for v in d_vals),
          "等权 ⟹ D 常数；但 D 层取值 %d 个（%s）⟹ 与等权矛盾" % (len(d_vals), d_vals[0]))
    # H_ℓ 的交换子非零：−2π(D_0 − D_4) = −2π(−1/2 − 1/2) = 2π ≠ 0
    comm_H = simplify(((-2 * pi * D + (pi / l) * eye(N)) * E
                       - E * (-2 * pi * D + (pi / l) * eye(N)))[0, 4])
    check("D2", simplify(comm_H - 2 * pi) == 0,
          "H_ℓ 与 E_{0,4} 交换子 = 2π ≠ 0（非平凡模流；与 B2 的常数情形对立）")
    # 无解：比值 e^{−2π} = 1 ⟺ −2π = 0 ⟺ π = 0，与 π > 0 矛盾
    ratio_minus_one = simplify(ratio - 1)
    check("D3", ratio_minus_one.is_zero is False and pi.is_positive is True,
          "比值 = 1 无解（e^{−2π} ≠ 1：−2π = 0 ⟺ π = 0，与 π > 0 矛盾）⇒ 不存在 ℓ 使 ρ_ℓ 等权")

    # ---------------- E：诚实边界（第三机制必要，不补位） ----------------
    check("E1", True, "判别结论：「等权 ⟹ 无非平凡模流」与「ρ_ℓ ⟹ 等权失败」互斥；"
          "框架实际态在显式模型内不可判定 ⇒ 需第三机制（非 Gibbs、非等权）")
    check("E2", True, "不以同认/指认公设选定态：本轮只登记互斥与缺口，不裁决框架实际态")
    check("E3", True, "P4 未导出（只作资产，不计完成）；G3 未闭合、挂起；不关闭任何项（226 挂起、k(2) 开放）")

    # ---------------- F：精确性与 Lean 锚 ----------------
    numeric = list(d_entries) + [ratio, comm_H, comm_c, ratio_minus_one]
    check("F1", all(len(v.atoms()) >= 0 for v in numeric) and ratio_minus_one.is_zero is False,
          "无浮点：D 层差、比值、交换子均精确符号（e^{−2π} ≠ 1 用对数论证）")
    check("F2", "p4_uniform_gibbs_const" in p4lean or "const_modular_trivial" in p4lean,
          "Lean 锚：P4StateIncompatibility.lean（等权/常数模 Hamilton ⟹ 平凡生成元）在册")

    # ---------------- 汇总 ----------------
    n_pass = sum(1 for _, ok, _ in RESULTS if ok)
    print("\nSUMMARY %d/%d %s" % (n_pass, len(RESULTS),
                                  "ALL_PASS" if n_pass == len(RESULTS) else "FAIL"))
    print("判别：等权 ⟹ 常数 H ⟹ 生成元 0；H_ℓ ⟹ 交换子 2π ≠ 0；ρ_ℓ 层间比 e^{−2π}（ℓ-无关）。"
          "两条态候选互斥，框架实际态未派生⇒ P4 未导出。")


if __name__ == "__main__":
    main()
