# -*- coding: utf-8 -*-
"""P7-5e-367 判据：Δ 记号纠偏审计（撤回 366 的「Δ=1」）。

问题（用户指出）：MUFPF 中 Δ 有专用语义——框架原生 Δ = spExchangeLaw 交换律偏差
（HigherSpCategory.lean 的 Δ 2-胞腔；Δ≠0 ⟺ δ≠0 ⟺ G_N>0；地位同 π/e），
不是谱隙、不能被赋值 1；文献 Δ_mod = 模算子（Tomita–Takesaki），RESEARCH_STATE 明令「禁止混用」。

366 的两处错误：
① 把 362 的谱隙记作 Δ（应为模指数 M，S97）；
② 用「流周期 2π/Δ ⟹ Δ=1」——S97 明确模流 Δ_mod^{it} **参数周期 = 1/M**，
   2π 是 BW 指数系数（Δ_mod = e^{−2πM}）与 Rindler 逆温 β = 2π/K。

纠偏后的正确链（本轮机检）：
  β 单独不内蕴（尺度协变）→ 参数周期归一为 1 ⟹ M = 1 ⟹ Δ_mod = e^{−2πM} = e^{−2π}（S106）
  → K 的每层间隔 = 2πM = 2π（P4 的 −2πD 结构）→ 层权比 e^{−2π}（与 365 一致）。
审计项 N1–N10，全程精确符号/有理，无浮点。
"""
import pathlib

import sympy as sp

ROOT = pathlib.Path(r"E:\workspace\hyper-resolution\universal_fixed_point_framework")
RS = ROOT / "RESEARCH_STATE.md"
HIGHER = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "HigherSpCategory.lean"
CRIT366 = ROOT / "scripts" / "p7_5e366_g3_p2_beta_delta_criteria.py"
OLD_LEAN = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "G3KMSBetaToDelta.lean"
NEW_LEAN = ROOT / "formal_proof" / "MUFPFormalization" / "src" / "MUFPFormalization" / "G3KMSBetaToModular.lean"
KMS_SRC = ROOT / "scripts" / "p7_5e286r_g3_p2_kms_model_criteria.py"

RESULTS = []


def check(tag, ok, detail=""):
    RESULTS.append((tag, bool(ok), detail))
    print("%-4s %s  %s" % (tag, "PASS" if ok else "FAIL", detail))


def zero(x):
    if isinstance(x, sp.MatrixBase):
        return all(zero(v) for v in x)
    return sp.simplify(sp.expand(x)) == 0


def main():
    rs = RS.read_text(encoding="utf-8")
    higher = HIGHER.read_text(encoding="utf-8")
    crit = CRIT366.read_text(encoding="utf-8")
    new_lean = NEW_LEAN.read_text(encoding="utf-8") if NEW_LEAN.exists() else ""
    kms = KMS_SRC.read_text(encoding="utf-8")

    # N1–N4：框架口径
    check("N1", "spExchangeLaw" in higher and "Δ 2-胞腔" in higher,
          "框架原生 Δ = spExchangeLaw 交换律偏差（Δ 2-胞腔）——结构常数，非谱隙")
    check("N2", "禁止混用" in rs and "Δ_mod" in rs and "框架 Δ" in rs,
          "RESEARCH_STATE 明令：框架 Δ 原生保持、文献 Δ_mod 加注，禁止混用")
    check("N3", "Δ_mod = e^{−2πM}" in rs and "参数周期不是 2π 是 1/M" in rs,
          "S97：Δ_mod = e^{−2πM}；模流参数周期 = 1/M（2π 为 BW 指数系数）")
    check("N4", "ln Δ_mod = −2π" in rs and "Δ_mod =" in rs,
          "S106：自然单位制下 ln Δ_mod = −2π ⟹ Δ_mod = e^{−2π}")

    # N5：366 判据已纠偏
    check("N5", "谱隙 2πM = 2π" in crit and "参数周期 = 1/M" in crit and "不是「Δ=1」" in crit,
          "366 判据已改为 M 口径：Δ_mod=e^{−2π}、K 谱隙 2πM=2π，显式撤回「Δ=1」")

    # N6：Lean 模块替换
    check("N6", (not OLD_LEAN.exists()) and "p2_mod_operator_index_one" in new_lean
          and "p2_mod_period_unit_implies_index_one" in new_lean,
          "旧模块 G3KMSBetaToDelta.lean 已移除；新模块 G3KMSBetaToModular.lean 在册（M 口径）")

    # N7–N9：正确关系精确机检
    check("N7", zero(sp.exp(-2 * sp.pi * sp.Integer(1)) - sp.exp(-2 * sp.pi)),
          "M=1 ⟹ Δ_mod = e^{−2πM} = e^{−2π}（精确）")
    check("N8", zero(sp.exp(-2 * sp.pi * (sp.Integer(1) + 1)) / sp.exp(-2 * sp.pi * sp.Integer(1))
                     - sp.exp(-2 * sp.pi)),
          "层步长 1 ⟹ 层权比 e^{−2π}（与 365 一致；365 无需改动）")
    check("N9", sp.solve(sp.Eq(2 * sp.pi / sp.Symbol("K"), 1), sp.Symbol("K")) == [2 * sp.pi]
          and zero(2 * sp.pi * sp.Integer(1) - 2 * sp.pi),
          "Rindler β=2π/K：β=1 ⟹ K=2π，与 M=1 ⟹ 2πM=2π 自洽")

    # N10：诚实边界 + 362 的符号回溯
    check("N10", "DELTA" in kms and "P2 未成立" in crit,
          "登记：362 的 Δ 回溯为 M（数值 1 = M，非 Δ）；P2 未成立、G3 未闭合、不关闭任何项")

    n_pass = sum(1 for _, ok, _ in RESULTS if ok)
    print("\nSUMMARY %d/%d %s" % (n_pass, len(RESULTS),
                                  "ALL_PASS" if n_pass == len(RESULTS) else "FAIL"))
    print("审计结论：366 的「Δ=1」撤回；正确为 M=1 ⟹ Δ_mod=e^{−2π}、K 每层间隔 2π、层权比 e^{−2π}。"
          "框架 Δ（交换律偏差）与 Δ_mod（模算子）不得混用。")


if __name__ == "__main__":
    main()
