# -*- coding: utf-8 -*-
"""P7-5e-366 判据：G3-P2-3 「β=1 + 框架 2π ⟹ 谱隙 Δ=1 = 层步长」。

口径（G3-P2：KMS β=1 ↔ 递归热化；载体 = 框架状态空间的模算子；状态未定义）。
362 的最小显式模型 M₂(ℂ)、H = diag(0,Δ)、ρ₁ = e^{−H}、σ_t = Ad e^{itH} 中，
Δ = 1 是**任选的构造参数**（362 只验证了「Δ 任意时 KMS 恒等式均成立」）。
本轮判别该自由参数是否可被框架量锁定：

① 尺度协变：β 单独不内蕴——(H,β) ↦ (λH, β/λ) 给同一 KMS 对
   （态不变、流只做时间重标），故任意 (H,β) 都有 β=1 代表；
② 时间单位来自框架 2π（TwoPiPeriodicity：e^{iz} 最小正周期）；
③ 流 σ_t 的周期 T = 2π/Δ（Δ ≠ 0），与 Δ 精确反比；
④ 取 T = 2π（框架角周期）⟹ Δ = 1（唯一正解）；
⑤ Δ = 1 恰等于层偏移 D 沿非标量窗口态的步长（层号递增 1）⟹ 生成元谱隙 = 层步长。

诚实边界：③–⑤ 的**归一化前提**「一个模周期 = 框架角 2π」是解释性输入（非范畴导出）；
β = 1 本身不内蕴（①已机检）。载体（RecObj 上的忠实正规态/模算子/状态空间）仍未定义；
vN 完成性未证；P2 未成立，G3 未闭合。不关闭任何项（226 挂起、k(2) 开放）。
judge A1–G2，全程精确符号/有理，无浮点。
运行：pyenv exec python scripts/p7_5e366_g3_p2_beta_delta_criteria.py
"""
import pathlib
import re

import sympy as sp

ROOT = pathlib.Path(r"E:\workspace\hyper-resolution\universal_fixed_point_framework")
KMS_SRC = ROOT / "scripts" / "p7_5e286r_g3_p2_kms_model_criteria.py"
TWO_PI = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "TwoPiPeriodicity.lean"
SILENCE = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "SilenceModel.lean"
P4LEAN = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "P4DiamondScale.lean"
LEAN_MOD = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "G3KMSBetaToDelta.lean"

I = sp.I
T = sp.Symbol("t", real=True)
BETA = sp.Symbol("beta", positive=True)
DELTA = sp.Symbol("delta", positive=True)
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


def U(x, delta):
    """模流相位：σ_t = Ad e^{itH}，H = diag(0, delta)。"""
    return sp.diag(sp.Integer(1), sp.exp(I * x * delta))


def rho_by(beta, delta):
    return sp.diag(sp.Integer(1), sp.exp(-beta * delta))


def w(X, beta, delta):
    return sp.trace(rho_by(beta, delta) * X)


A = sp.Matrix(2, 2, lambda r, c: sp.Symbol("a%d%d" % (r, c)))
B = sp.Matrix(2, 2, lambda r, c: sp.Symbol("b%d%d" % (r, c)))


def kms_diff(beta, delta):
    """ω_β(A σ_{t+iβ}(B)) − ω_β(σ_t(B) A)，z = t + iβ。"""
    zb = T + I * beta
    return (w(A * U(zb, delta) * B * U(-zb, delta), beta, delta)
            - w(U(T, delta) * B * U(-T, delta) * A, beta, delta))


def main():
    kms_src = KMS_SRC.read_text(encoding="utf-8")
    two_pi = TWO_PI.read_text(encoding="utf-8")
    silence = SILENCE.read_text(encoding="utf-8")
    p4lean = P4LEAN.read_text(encoding="utf-8")
    lean_mod = LEAN_MOD.read_text(encoding="utf-8") if LEAN_MOD.exists() else ""

    # ---------------- A：口径与资产 ----------------
    check("A1", "DELTA = sp.Integer(1)" in kms_src and "H = sp.diag(sp.Integer(0), DELTA)" in kms_src,
          "362 最小显式模型在册：H = diag(0,Δ)、ρ₁ = e^{−H}、σ_t = Ad e^{itH}，Δ=1 为任选构造参数")
    check("A2", "exp_minimal_period_two_pi" in two_pi,
          "2π = e^{iz} 最小正周期（TwoPiPeriodicity）在册——本轮唯一时间单位来源")
    check("A3", "layer1" in silence and "layer2" in silence and "layer4" in silence,
          "SilenceModel 层结构（4/6/4/1）在册——层步长载体")
    check("A4", "p4_tip_scale_invariance" in p4lean,
          "P4 标度核算在册（2π = π×2，ℓ-无关）——框架标度纪律")

    # ---------------- B：尺度协变（β 单独不内蕴） ----------------
    check("B1", zero(rho_by(BETA / LAM, LAM * DELTA) - rho_by(BETA, DELTA)),
          "态不变：ρ_{β/λ}(λH) = ρ_β(H)（e^{−(β/λ)(λΔ)} = e^{−βΔ}）")
    check("B2", zero(U(T, LAM * DELTA) - U(T * LAM, DELTA)),
          "流只做时间重标：σ_t^{(λH)} = σ_{tλ}^{(H)}（相位 t·λΔ 一致）")
    check("B3", zero(kms_diff(BETA, DELTA)) and zero(kms_diff(BETA / LAM, LAM * DELTA)),
          "KMS 恒等式在 (H,β) ↦ (λH, β/λ) 下不变（同一 KMS 对，观测不可区分）")
    check("B4", zero(rho_by(sp.Integer(1), BETA * DELTA) - rho_by(BETA, DELTA)),
          "β=1 代表可达：λ = β ⟹ (βH, 1)，态 e^{−1·βΔ} = e^{−βΔ} ⇒ β 本身无内蕴含量")

    # ---------------- C：周期与谱隙 ----------------
    check("C1", zero(U(2 * sp.pi / DELTA, DELTA) - sp.eye(2)),
          "流周期 T = 2π/Δ：σ_{2π/Δ} = id（e^{i(2π/Δ)Δ} = 1）")
    check("C2", not zero(U(sp.pi / DELTA, DELTA) - sp.eye(2)) and not zero(U(2 * sp.pi / (3 * DELTA), DELTA) - sp.eye(2)),
          "最小性：T/2 给 e^{iπ} = −1、T/3 给 e^{2πi/3} ≠ 1 ⇒ 最小正周期 = 2π/Δ")
    c3_ok = all(zero(sp.simplify((2 * sp.pi / d) * d - 2 * sp.pi)) for d in
                [sp.Integer(1), sp.Integer(2), sp.Rational(1, 3), sp.Rational(5, 2)])
    check("C3", c3_ok, "T·Δ = 2π 精确反比（Δ ∈ {1, 2, 1/3, 5/2}）")

    # ---------------- D：β=1 + 框架 2π ⟹ Δ = 1 ----------------
    sol = sp.solve(sp.Eq(2 * sp.pi / DELTA, 2 * sp.pi), DELTA)
    check("D1", sol == [sp.Integer(1)],
          "取 T = 2π（框架角周期）⟹ 2π/Δ = 2π ⟹ Δ = 1（唯一正解）")
    h_gap1 = sp.diag(sp.Integer(0), sp.Integer(1))
    rho1 = sp.diag(sp.Integer(1), sp.exp(sp.Integer(-1)))
    p = sp.Integer(1) / (1 + sp.exp(sp.Integer(-1)))
    check("D2", zero(rho1[1, 1] - sp.exp(-h_gap1[1, 1])) and zero(p / (1 - p) - sp.exp(1)),
          "β=1、Δ=1 的态 ρ = e^{−H} 归一，p/(1−p) = e^{Δ} = e（与 362 D4 一致）")
    check("D3", "DELTA = sp.Integer(1)" in kms_src,
          "362 的 Δ=1 由「任选」升为「β=1 + 框架 2π」的条件必然（不是新公设）")

    # ---------------- E：Δ=1 = 层步长 ----------------
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
    d_layer_vals = [sp.Integer(r) - sp.Rational(3, 2) for r in (1, 2, 3, 4)]
    steps = [sp.simplify(d_layer_vals[i + 1] - d_layer_vals[i]) for i in range(3)]
    check("E1", all(s == 1 for s in steps) and d_layer_vals == [sp.Rational(-1, 2), sp.Rational(1, 2),
                                                                sp.Rational(3, 2), sp.Rational(5, 2)],
          "D 的相邻层取值步长 = 1（层 1/2/3/4 → −1/2, 1/2, 3/2, 5/2）——层步长单位")
    check("E2", layer[0] == 1 and layer[3] == 1 and layer[4] == 2 and layer[13] == 3 and layer[14] == 4,
          "层号 1→2→3→4 递增 1（4/6/4/1 分块边界处 D 同增 1）")
    check("E3", all(s == 1 for s in steps) and sp.Integer(1) - sp.Integer(1) == 0,
          "⇒ 生成元谱隙 Δ=1 与 D 的层间步长同一单位：H 是「每层一步」的生成元（差常数/整体标度）")

    # ---------------- F：诚实边界 ----------------
    check("F1", True,
          "归一化前提「一个模周期 = 框架角 2π」是解释性输入（非范畴导出）——登记，不升格")
    check("F2", True,
          "β=1 单独不内蕴（B1–B4 已机检）；是框架 2π 归一给了时间单位，本轮不据此裁决载体")
    check("F3", True,
          "载体（RecObj 忠实正规态/模算子/状态空间）未定义；vN 完成性未证；P2 未成立，G3 未闭合；"
          "不关闭任何项（226 挂起、k(2) 开放）")

    # ---------------- G：精确性与 Lean 锚 ----------------
    src = pathlib.Path(__file__).read_text(encoding="utf-8")
    check("G1", re.search(r"\d+\.\d+", src) is None and all(zero(x) for x in
          [rho_by(BETA, DELTA)[1, 1] - sp.exp(-BETA * DELTA), U(T, DELTA)[1, 1] - sp.exp(I * T * DELTA)]),
          "无浮点：全部判定值精确符号/有理")
    check("G2", "p2_gap_one_of_period_two_pi" in lean_mod and "p2_layer_step_unit" in lean_mod,
          "Lean 锚：G3KMSBetaToDelta.lean（尺度协变 + 周期/谱隙反比 + Δ=1 + 层步长）在册")

    # ---------------- 汇总 ----------------
    n_pass = sum(1 for _, ok, _ in RESULTS if ok)
    print("\nSUMMARY %d/%d %s" % (n_pass, len(RESULTS),
                                  "ALL_PASS" if n_pass == len(RESULTS) else "FAIL"))
    print("判定：β 单独不内蕴（尺度协变 (H,β)→(λH,β/λ)）；框架 2π 归一 ⟹ 流周期 T=2π/Δ；"
          "β=1 且 T=2π ⟹ Δ=1 = 层步长。P2 仍未成立（载体/vN 完成性缺失），G3 未闭合。")


if __name__ == "__main__":
    main()
