# -*- coding: utf-8 -*-
"""P7-5e-355 判据：G3-P1b 定义层（外自同构定义 + 层移动 ⟹ 外 + Subalgebra 载体收口 + P1b-3 逆向影子）

只做判别，不改文档。判据 D1–D23 全部通过 = P1b-1（定义层骨架）、P1b-2（非交换块模型）、
P1b-2 完成性收口（Subalgebra 载体 + 代数内部单位）与 P1b-3 逆向影子
（严格升层 ⟹ 全迭代非内 ⟹ 无限阶 ⟹ 有限块塔不可能）机检完成。
"""
import pathlib
import subprocess

ROOT = pathlib.Path(r"E:\workspace\hyper-resolution\universal_fixed_point_framework")
LAKE = ROOT / "formal_proof" / "MUFPFormalization"
OUTER = LAKE / "src" / "MUFPFormalization" / "RecursionModularityOuter.lean"
BRIDGE = LAKE / "src" / "MUFPFormalization" / "RecursionModularityBridge.lean"

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
    outer = OUTER.read_text(encoding="utf-8")
    bridge = BRIDGE.read_text(encoding="utf-8")

    ok_outer, msg_outer = compile_ok(OUTER)
    chk("D1", "P1b 模块编译通过（lake env lean rc=0）", ok_outer, msg_outer)

    chk("D2", "定义层在册：InnerRealization / IsOuterAut",
        "def InnerRealization" in outer and "def IsOuterAut" in outer)

    chk("D3", "核心定理：层移动 ⟹ 外（isOuter_of_layer_shift）",
        "theorem isOuter_of_layer_shift" in outer)

    chk("D4", "严格升层 ⟹ 外（isOuter_of_strictLayer，与 P1a StrictLayer 同形）",
        "theorem isOuter_of_strictLayer" in outer)

    chk("D5", "零 sorry（P1b 新模块 + P1a 桥）",
        "sorry" not in outer and "sorry" not in bridge)

    chk("D6", "非空实例在册（swapAlgEquiv / layerOfPair / swap_outer_witness）",
        all(t in outer for t in ("swapAlgEquiv", "layerOfPair", "swap_outer_witness")))

    no_vn = ("def vonNeumann" not in outer and "structure VonNeumann" not in outer
             and "class VonNeumann" not in outer and "def modularOperator" not in outer)
    chk("D7", "不越界：不定义 vN 代数 / 模算子（仅边界声明提及）", no_vn)

    gaps = ("P1b-2" in outer and "P1b-3" in outer and "vN 完成性" in outer)
    chk("D8", "缺口登记：P1b-3（逆向）/ vN 完成性（P1b-2 已完成）", gaps)

    chk("D9", "诚实边界：不声称 P1 成立", "不声称 P1 成立" in outer)

    ok_bridge, msg_bridge = compile_ok(BRIDGE)
    p1a = ["recStep", "StrictLayer", "p1a_unidirectional", "p1a_no_cycle"]
    chk("D10", "P1a 回归：桥编译通过 + 四定理在册",
        ok_bridge and all(t in bridge for t in p1a), msg_bridge)

    chk("D11", "非交换块模型在册（BlockMat / TwoBlockAlg / InnerBlockRealization / swapBlockAlgEquiv）",
        all(t in outer for t in ("BlockMat", "TwoBlockAlg", "InnerBlockRealization",
                                 "swapBlockAlgEquiv")))

    chk("D12", "块模型两定理：innerBlock_preserves_layer / swapBlock_not_inner",
        "theorem innerBlock_preserves_layer" in outer
        and "theorem swapBlock_not_inner" in outer)

    chk("D13", "非交换性可核：块 = M₂(ℚ)（非交换）+ 关键引理 conj_eq_zero_iff（只用逆元）",
        "Matrix (Fin 2) (Fin 2) ℚ" in outer and "theorem conj_eq_zero_iff" in outer)

    chk("D14", "Subalgebra 载体在册：BlockMat4 / blockDiagAlgHom / blockDiagSubalgebra",
        all(t in outer for t in ("abbrev BlockMat4", "def blockDiagAlgHom",
                                 "def blockDiagSubalgebra : Subalgebra ℚ BlockMat4")))

    chk("D15", "载体迁移通道：blockDiagEquiv（AlgEquiv.ofInjective）+ 块对角嵌入单射",
        "noncomputable def blockDiagEquiv" in outer
        and "AlgEquiv.ofInjective blockDiagAlgHom" in outer
        and "theorem blockDiagAlgHom_injective" in outer)

    chk("D16", "中心元判据通用化：inner_fixes_central（内实现固定中心元）",
        "theorem inner_fixes_central" in outer)

    chk("D17", "块投影中心性 + 层移动：blockDiagP₀_central / blockDiagP₀_ne_P₁ / swapSubAlg_shifts",
        all(t in outer for t in ("theorem blockDiagP₀_central", "theorem blockDiagP₀_ne_P₁",
                                 "theorem swapSubAlg_shifts")))

    chk("D18", "完成性收口主定理：swapSubAlg_not_inner + swapSubAlg_outer（IsOuterAut 口径）",
        "theorem swapSubAlg_not_inner" in outer and "theorem swapSubAlg_outer" in outer)

    chk("D19", "P1b-3 迭代升层：layer_iterate（L ((σ ^ n) a₀) = L a₀ + n）",
        "theorem layer_iterate" in outer
        and "∀ n : ℕ, L ((σ ^ n) a₀) = L a₀ + n" in outer)

    chk("D20", "P1b-3 无内回退：iterate_not_inner（n ≠ 0 ⟹ IsOuterAut (σ ^ n)）",
        "theorem iterate_not_inner" in outer
        and "{n : ℕ} (hn : n ≠ 0) : IsOuterAut (σ ^ n)" in outer)

    chk("D21", "P1b-3 无周期：strictLayer_infinite_order（n ≠ 0 ⟹ σ ^ n ≠ AlgEquiv.refl）",
        "theorem strictLayer_infinite_order" in outer
        and "∀ n : ℕ, n ≠ 0 → σ ^ n ≠ AlgEquiv.refl" in outer)

    chk("D22", "P1b-3 反例对照：swapBlock_sq（二阶）+ swapBlock_no_strictLayer（有限块塔不可能承载严格升层）",
        "theorem swapBlock_sq : swapBlockAlgEquiv ^ 2 = AlgEquiv.refl" in outer
        and "theorem swapBlock_no_strictLayer" in outer)

    chk("D23", "P1b-3 诚实边界：真逆向（外 ⟹ 单向）属 P2，本文件不证",
        "真逆向（外 ⟹ 单向）不在本文件证明" in outer)

    print()
    passed = sum(1 for r in results if r[2])
    print(f"{passed}/{len(results)} " + ("ALL_PASS" if passed == len(results) else "HAS_FAILURE"))
    print("判定：P1b-1 定义层骨架 + P1b-2 非交换块模型 + Subalgebra 载体完成性收口 + "
          "P1b-3 逆向影子（严格升层 ⟹ 全迭代非内 ⟹ 无限阶 ⟹ 有限块塔不可能）机检完成；"
          "P1b-3 真逆向（外 ⟹ 单向，需 Δ_mod/KMS β=1，属 P2）与 vN 完成性仍是缺口，"
          "P1 未成立（入轨/判别 ≠ 成立/闭合）。")


if __name__ == "__main__":
    main()
