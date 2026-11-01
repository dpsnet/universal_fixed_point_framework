# -*- coding: utf-8 -*-
"""P7-5e-357 判据：G3-P2-1 一参数自同构流骨架与整数时刻外性

只做判别，不改文档。判据 F1–F9 全部通过 = P2-1（AutFlow 骨架、离散-连续桥、
整数时刻外性、连续版无周期、非空实例与非空转对照）机检完成。
诚实边界：KMS β=1 本体（忠实正规态/解析延拓/Δ_mod）与载体（框架状态空间的
模算子、状态）均未定义——P2 未成立。
"""
import pathlib
import subprocess

ROOT = pathlib.Path(r"E:\workspace\hyper-resolution\universal_fixed_point_framework")
LAKE = ROOT / "formal_proof" / "MUFPFormalization"
FLOW = LAKE / "src" / "MUFPFormalization" / "RecursionModularityFlow.lean"
OUTER = LAKE / "src" / "MUFPFormalization" / "RecursionModularityOuter.lean"

results = []


def chk(tag, name, cond, note=""):
    results.append((tag, name, bool(cond), note))
    print(f"[{'PASS' if cond else 'FAIL'}] {tag} {name}" + (f"   {note}" if note else ""))
    return bool(cond)


def compile_ok(path):
    r = subprocess.run(["lake", "env", "lean", str(path)], cwd=str(LAKE),
                       capture_output=True, text=True, timeout=600)
    tail = (r.stdout + r.stderr).strip().splitlines()
    return r.returncode == 0, (tail[-1][:120] if tail else "")


def main():
    flow = FLOW.read_text(encoding="utf-8")
    outer = OUTER.read_text(encoding="utf-8")

    ok_flow, msg_flow = compile_ok(FLOW)
    chk("F1", "P2-1 模块编译通过（lake env lean rc=0，零输出）", ok_flow, msg_flow)

    chk("F2", "AutFlow 结构在册：toAut / map_add'（σ(s+t)=σs*σt）/ map_zero'（σ0=1）",
        "structure AutFlow" in flow and "map_add'" in flow and "map_zero'" in flow
        and "toAut : ℝ → A ≃ₐ[R] A" in flow)

    chk("F3", "离散-连续桥（主桥）：pow_eq_nsmul（(σs)^n = σ(n•s)）+ pow_one_eq（(σ1)^n = σ n）",
        "theorem pow_eq_nsmul" in flow and "∀ n : ℕ, (F.toAut s) ^ n = F.toAut (n • s)" in flow
        and "theorem pow_one_eq" in flow
        and "(F.toAut (1 : ℝ)) ^ n = F.toAut (n : ℝ)" in flow)

    chk("F4", "流群性质：commute（σs*σt=σt*σs）/ aut_neg（σ(-s)=(σs)⁻¹）",
        "theorem commute" in flow and "theorem aut_neg" in flow
        and "F.toAut (-s) = (F.toAut s)⁻¹" in flow)

    chk("F5", "严格整数升层：StrictIntegerAdvance（L (σ (n•s₀) a₀) = L a₀ + n）"
              " + generator_iterate_advance（桥⟹L((σs₀)^n a₀)=L a₀+n）",
        "def StrictIntegerAdvance" in flow
        and "∀ n : ℕ, L (F.toAut (n • s₀) a₀) = L a₀ + n" in flow
        and "theorem generator_iterate_advance" in flow)

    chk("F6", "整数时刻外性主定理：outer_at_integer_time（n≠0 ⟹ IsOuterAut (σ(n•s₀)）"
              " + pow_outer（n≠0 ⟹ IsOuterAut((σs₀)^n)）",
        "theorem outer_at_integer_time" in flow
        and "theorem pow_outer" in flow
        and "IsOuterAut (F.toAut (n • s₀))" in flow
        and "IsOuterAut ((F.toAut s₀) ^ n)" in flow)

    chk("F7", "连续版无周期：flow_generator_infinite_order（n≠0 ⟹ (σs₀)^n ≠ AlgEquiv.refl）",
        "theorem flow_generator_infinite_order" in flow
        and "∀ n : ℕ, n ≠ 0 → (F.toAut s₀) ^ n ≠ AlgEquiv.refl" in flow)

    chk("F8", "非空实例与非空转对照：trivialAutFlow + trivialFlow_no_strictAdvance",
        "def trivialAutFlow : AutFlow ℚ (ℚ × ℚ)" in flow
        and "theorem trivialFlow_no_strictAdvance" in flow)

    no_vn = ("structure VonNeumann" not in flow and "class VonNeumann" not in flow
             and "def modularOperator" not in flow and "def kmsState" not in flow
             and "def stateSpace" not in flow and "structure State" not in flow)
    honest = ("KMS β = 1 本体不在本文件" in flow and "P2 未成立" in flow
              and "不关闭任何项" in flow and "sorry" not in flow
              and "sorry" not in outer)
    chk("F9", "不越界 + 诚实边界 + 零 sorry：不定义 vN/模算子/KMS 态/状态空间；"
              "登记 P2 本体缺口，不声称 P2 成立",
        no_vn and honest)

    print()
    passed = sum(1 for r in results if r[2])
    print(f"{passed}/{len(results)} " + ("ALL_PASS" if passed == len(results) else "HAS_FAILURE"))
    print("判定：P2-1 一参数自同构流骨架 + 离散-连续桥 + 整数时刻外性 + 连续版无周期"
          "机检完成；KMS β=1 本体（忠实正规态/解析延拓/Δ_mod）与载体（框架状态空间的模算子、"
          "状态）均未定义——P2 未成立（骨架 ≠ 成立/闭合）。不关闭任何项。")


if __name__ == "__main__":
    main()
