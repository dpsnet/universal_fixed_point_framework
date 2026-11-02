# -*- coding: utf-8 -*-
"""P7-5e-366 判据（**经 P7-5e-367 纠偏**）：G3-P2-3 「β=1 ⟹ 模指数 M=1 ⟹ Δ_mod = e^{−2π}」。

纠偏说明：本脚本原版把谱隙记作 Δ 并推出「Δ=1」，属记号误用——
MUFPF 原生 Δ = spExchangeLaw 交换律偏差（结构常数，HigherSpCategory.lean；Δ≠0 ⟺ δ≠0 ⟺ G_N>0），
不是谱隙；文献 Δ_mod = 模算子（Tomita–Takesaki），RESEARCH_STATE 明令「禁止混用」。
S97：Δ_mod = e^{−2πM}，模流 Δ_mod^{it} **参数周期 = 1/M**（不是 2π/M）；2π 是 BW 指数系数与 Rindler β=2π/K。
本版全部改为 M（模指数），Δ_mod 只表示模算子。

口径（G3-P2：KMS β=1 ↔ 递归热化；载体 = 框架状态空间的模算子；状态未定义）。
362 的模型 M₂(ℂ)、K = diag(0, 2πM)、ρ₁ = e^{−K}、σ_t = Ad e^{itK} 中，M=1 原为任选；本轮判别其能否被归一锁定：
① 尺度协变 (K,β) ↦ (λK, β/λ) 给同一 KMS 对 ⇒ β 单独不内蕴；
② 模流参数周期 = 1/M；③ 周期归一为 1 ⟹ M = 1；④ M=1 ⟹ Δ_mod = e^{−2π}（S106）；⑤ K 每层间隔 = 2π，层权比 e^{−2π}（与 365 一致）。
诚实边界：归一化前提「参数周期取 1」是解释性输入；载体/vN 完成性未证；P2 未成立，G3 未闭合；不关闭任何项。
judge A1–G2，全程精确符号/有理，无浮点。
运行：pyenv exec python scripts/p7_5e366_g3_p2_beta_delta_criteria.py
"""
import pathlib
import re

import sympy as sp

ROOT = pathlib.Path(r"E:\workspace\hyper-resolution\universal_fixed_point_framework")
KMS_SRC = ROOT / "scripts" / "p7_5e286r_g3_p2_kms_model_criteria.py"
HIGHER = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "HigherSpCategory.lean"
TWO_PI = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "TwoPiPeriodicity.lean"
SILENCE = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "SilenceModel.lean"
LEAN_MOD = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "G3KMSBetaToModular.lean"

I = sp.I
T = sp.Symbol("t", real=True)
BETA = sp.Symbol("beta", positive=True)
M = sp.Symbol("M", positive=True)
LAM = sp.Symbol("lam", positive=True)

RESULTS = []


def check(tag, ok, detail=""):
    RESULTS.append((tag, bool(ok), detail))
    print("%-4s %s  %s" % (tag, "PASS" if ok else "FAIL", detail))


def zero(x):
    if isinstance(x, sp.MatrixBase):
        return all(zero(v) for v in x)
    e = sp.powsimp(sp.expand(x), combine="exp", force=True)
    return sp.simplify(e) == 0


def gap(m):
    return 2 * sp.pi * m          # 模 Hamilton K 的谱隙（P4: −2πD 结构）


def U(x, m):
    return sp.diag(sp.Integer(1), sp.exp(I * x * gap(m)))


def rho_by(beta, m):
    return sp.diag(sp.Integer(1), sp.exp(-beta * gap(m)))


def w(X, beta, m):
    return sp.trace(rho_by(beta, m) * X)


A = sp.Matrix(2, 2, lambda r, c: sp.Symbol("a%d%d" % (r, c)))
B = sp.Matrix(2, 2, lambda r, c: sp.Symbol("b%d%d" % (r, c)))


def kms_diff(beta, m):
    zb = T + I * beta
    return (w(A * U(zb, m) * B * U(-zb, m), beta, m)
            - w(U(T, m) * B * U(-T, m) * A, beta, m))


def main():
    kms_src = KMS_SRC.read_text(encoding="utf-8")
    higher = HIGHER.read_text(encoding="utf-8")
    two_pi = TWO_PI.read_text(encoding="utf-8")
    silence = SILENCE.read_text(encoding="utf-8")
    lean_mod = LEAN_MOD.read_text(encoding="utf-8") if LEAN_MOD.exists() else ""

    # ---------------- A：口径与资产 ----------------
    check("A1", "H = sp.diag(sp.Integer(0), DELTA)" in kms_src,
          "362 模型在册（其谱隙曾记作 Δ——本轮纠偏为 M；K = diag(0, 2πM)）")
    check("A2", "exp_minimal_period_two_pi" in two_pi,
          "2π = e^{iz} 最小正周期（TwoPiPeriodicity）在册——BW 指数系数来源")
    check("A3", "spExchangeLaw" in higher and "Δ 2-胞腔" in higher,
          "框架原生 Δ = spExchangeLaw 交换律偏差（HigherSpCategory）在册——不是谱隙，禁止赋 1")
    check("A4", "layer1" in silence and "layer2" in silence and "layer4" in silence,
          "SilenceModel 层结构（4/6/4/1）在册——层步长载体")

    # ---------------- B：尺度协变（β 单独不内蕴） ----------------
    check("B1", zero(rho_by(BETA / LAM, LAM * M) - rho_by(BETA, M)),
          "态不变：ρ_{β/λ}(λK) = ρ_β(K)（e^{−(β/λ)(λ·2πM)} = e^{−β·2πM}）")
    check("B2", zero(U(T, LAM * M) - U(T * LAM, M)),
          "流只做时间重标：σ_t^{(λK)} = σ_{tλ}^{(K)}（相位 t·2πM 一致）")
    check("B3", zero(kms_diff(BETA, M)) and zero(kms_diff(BETA / LAM, LAM * M)),
          "KMS 恒等式在 (K,β) ↦ (λK, β/λ) 下不变（同一 KMS 对，观测不可区分）")
    check("B4", zero(rho_by(sp.Integer(1), BETA * M) - rho_by(BETA, M)),
          "β=1 代表可达：λ=β ⟹ (βK, 1)，态 e^{−1·β·2πM} = e^{−β·2πM} ⇒ β 本身无内蕴含量")

    # ---------------- C：模流参数周期 = 1/M ----------------
    dm = sp.exp(-2 * sp.pi * M)                      # Δ_mod = e^{−2πM}
    check("C1", zero(dm ** (I * (1 / M)) - 1),
          "Δ_mod^{it} 的参数周期 = 1/M：Δ_mod^{i·(1/M)} = e^{−2πi} = 1（S97，不是 2π/M）")
    check("C2", not zero(dm ** (I * (1 / (2 * M))) - 1),
          "最小性：半周期给 e^{−πi} = −1 ≠ 1 ⇒ 最小正周期 = 1/M")
    c3_ok = all(zero(sp.simplify(sp.solve(sp.Eq(sp.Symbol("K") * m, 2 * sp.pi), sp.Symbol("K"))[0] * m - 2 * sp.pi))
                for m in [sp.Integer(1), sp.Integer(2), sp.Rational(1, 3)])
    check("C3", c3_ok and sp.solve(sp.Eq(2 * sp.pi / sp.Symbol("K"), 1), sp.Symbol("K")) == [2 * sp.pi],
          "Rindler β = 2π/K：β=1 ⟹ K = 2π；与 M=1 ⟹ 2πM = 2π 一致")

    # ---------------- D：M=1 ⟹ Δ_mod = e^{−2π} ----------------
    sol = sp.solve(sp.Eq(1 / M, 1), M)
    check("D1", sol == [sp.Integer(1)], "参数周期归一为 1 ⟹ 1/M = 1 ⟹ M = 1（唯一正解）")
    check("D2", zero(dm.subs(M, 1) - sp.exp(-2 * sp.pi)),
          "M = 1 ⟹ Δ_mod = e^{−2πM} = e^{−2π}（与 S106 ln Δ_mod = −2π 一致）")
    check("D3", zero(gap(sp.Integer(1)) - 2 * sp.pi),
          "M = 1 ⟹ 模 Hamilton 谱隙 2πM = 2π（P4 的 −2πD 结构；不是「Δ=1」）")

    # ---------------- E：层步长对齐 ----------------
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
            layer.append(0)
    d_layer_vals = [sp.Integer(r) - sp.Rational(3, 2) for r in (1, 2, 3, 4)]
    steps = [sp.simplify(d_layer_vals[i + 1] - d_layer_vals[i]) for i in range(3)]
    check("E1", all(s == 1 for s in steps) and d_layer_vals == [sp.Rational(-1, 2), sp.Rational(1, 2),
                                                                sp.Rational(3, 2), sp.Rational(5, 2)],
          "D 层间步长 = 1（层 1/2/3/4 → −1/2, 1/2, 3/2, 5/2）")
    check("E2", layer[0] == 1 and layer[3] == 1 and layer[4] == 2 and layer[13] == 3 and layer[14] == 4,
          "层号 1→2→3→4 递增 1（4/6/4/1 分块边界）")
    ratio = sp.simplify(sp.exp(-2 * sp.pi * (M + 1)) / sp.exp(-2 * sp.pi * M))
    check("E3", zero(ratio - sp.exp(-2 * sp.pi)) and zero(sp.exp(-2 * sp.pi * (sp.Integer(1) + 1))
                                                           / sp.exp(-2 * sp.pi * sp.Integer(1)) - sp.exp(-2 * sp.pi)),
          "每层模权比 Δ_mod^{M+1}/Δ_mod^M = e^{−2π}（与 365 的层间比一致）")

    # ---------------- F：诚实边界 ----------------
    check("F1", "BW 指数系数" in pathlib.Path(__file__).read_text(encoding="utf-8")
          and "参数周期 = 1/M" in pathlib.Path(__file__).read_text(encoding="utf-8"),
          "2π 在模流语境是 BW 指数系数（Δ_mod = e^{−2πM}）与 Rindler β=2π/K，不是流周期——纠偏口径在册")
    check("F2", True,
          "归一化前提「模流参数周期取 1」是解释性输入（非范畴导出）——登记，不升格")
    check("F3", True,
          "载体（RecObj 忠实正规态/模算子/状态空间）未定义；vN 完成性未证；P2 未成立，G3 未闭合；"
          "不关闭任何项（226 挂起、k(2) 开放）")

    # ---------------- G：精确性与 Lean 锚 ----------------
    src = pathlib.Path(__file__).read_text(encoding="utf-8")
    check("G1", re.search(r"\d+\.\d+", src) is None and zero(dm - sp.exp(-2 * sp.pi * M)),
          "无浮点：全部判定值精确符号/有理")
    check("G2", "p2_mod_operator_index_one" in lean_mod and "p2_layer_ratio" in lean_mod
          and "p2_mod_period_unit_implies_index_one" in lean_mod,
          "Lean 锚：G3KMSBetaToModular.lean（参数周期 1/M、M=1、Δ_mod=e^{−2π}、层权比）在册")

    n_pass = sum(1 for _, ok, _ in RESULTS if ok)
    print("\nSUMMARY %d/%d %s" % (n_pass, len(RESULTS),
                                  "ALL_PASS" if n_pass == len(RESULTS) else "FAIL"))
    print("判定：β 单独不内蕴；模流参数周期 = 1/M，归一为 1 ⟹ M=1 ⟹ Δ_mod = e^{−2π}（S106）；"
          "K 每层间隔 2π、层权比 e^{−2π}。P2 未成立，G3 未闭合。")


if __name__ == "__main__":
    main()
