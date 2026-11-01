# -*- coding: utf-8 -*-
"""P7-5e-358 判据：G4-1 时空维数两公设结构层（三层态射 → 4 维）

只做判别，不改文档。判据 H1–H9 全部通过 = G4-1（计数层结构骨架、时间坐标
良定义、联合一致性唯一性、三层≠三个时间维）机检完成。
诚实边界：本判据不证明「为何 N_gen=3」，不证明空间/时间正交互补——G4 未闭合。
"""
import pathlib
import subprocess

ROOT = pathlib.Path(r"E:\workspace\hyper-resolution\universal_fixed_point_framework")
LAKE = ROOT / "formal_proof" / "MUFPFormalization"
MOD = LAKE / "src" / "MUFPFormalization" / "SpacetimeDimensionTwoPostulates.lean"

results = []


def chk(tag, name, cond, note=""):
    results.append((tag, name, bool(cond), note))
    print(f"[{'PASS' if cond else 'FAIL'}] {tag} {name}" + (f"   {note}" if note else ""))
    return bool(cond)


def compile_ok(path):
    r = subprocess.run(["lake", "env", "lean", str(path)], cwd=str(LAKE),
                       capture_output=True, text=True, timeout=600)
    out = (r.stdout + r.stderr).strip()
    tail = out.splitlines()
    return r.returncode == 0, out == "", (tail[-1][:120] if tail else "")


def main():
    src = MOD.read_text(encoding="utf-8")

    rc0, quiet, msg = compile_ok(MOD)
    chk("H1", "G4-1 模块编译通过（lake env lean rc=0 且零输出）", rc0 and quiet, msg)

    chk("H2", "两公设在册：spaceLayerDim=3（三层态射）/ timeLayerDim=1（递归单向）/ spacetimeDim",
        "def spaceLayerDim : ℕ := 3" in src
        and "def timeLayerDim : ℕ := 1" in src
        and "def spacetimeDim : ℕ := spaceLayerDim + timeLayerDim" in src)

    chk("H3", "4 = 3+1 与计数全态 16：spacetime_dim_eq_four / spacetime_dim_eq_ngen_add_one / cl31_state_count",
        "theorem spacetime_dim_eq_four : spacetimeDim = 4" in src
        and "theorem spacetime_dim_eq_ngen_add_one : spacetimeDim = 3 + 1" in src
        and "theorem cl31_state_count : clStateCount = 16" in src)

    chk("H4", "k_max = 2×时空维数 ∧ 静默 5 ∧ σ⁻¹ = 15",
        "theorem kmax_eq_two_mul_spacetime : kMax = 2 * spacetimeDim" in src
        and "theorem silence_eq_five : silenceUnit = 5" in src
        and "theorem sigmaInv_eq_fifteen : sigmaInv = 15" in src)

    chk("H5", "S149 链结构化复述且显式声明与 spacetime_dimension_chain 数值同构（不新增数值）",
        "theorem s149_chain_restated" in src
        and "SpectralGap.spacetime_dimension_chain" in src
        and "本文件不新增数值" in src)

    chk("H6", "时间坐标良定义（共享 G3 定义层）：time_coordinate_unique + time_orbit_injective + StrictLayer",
        "theorem time_coordinate_unique" in src
        and "theorem time_orbit_injective" in src
        and "StrictLayer ev layerOf" in src
        and "Function.Injective (fun k : ℕ => recStep ev k r)" in src)

    chk("H7", "联合一致性唯一性：layer_count_unique（2^N = 2*(N+1) ⟹ N = 3）",
        "theorem layer_count_unique (N : ℕ) (h : 2 ^ N = 2 * (N + 1)) : N = 3" in src
        and "MUFPF.KMaxAlgebra.power_unique N h'" in src)

    chk("H8", "三层态射 ≠ 三个时间维：layers_not_time_dims（3≠1 且 2⁶ ≠ 2⁴）",
        "theorem layers_not_time_dims" in src
        and "spaceLayerDim ≠ timeLayerDim" in src
        and "2 ^ (spaceLayerDim + spaceLayerDim) ≠" in src)

    no_boundary = ("structure Clifford" not in src and "def clifford" not in src
                   and "structure VonNeumann" not in src
                   and "def modularOperator" not in src)
    honest = ("G4 未闭合" in src and "不关闭任何项" in src
              and "为何 N_gen = 3" in src and "未导出" in src
              and "正交互补" in src and "未证" in src
              and "不构造" in src and "sorry" not in src)
    chk("H9", "不越界（不构造 Clifford 代数/vN）+ 诚实边界 + 零 sorry：登记「为何 N_gen=3」未导出、"
              "正交互补未证，不声称 G4 成立",
        no_boundary and honest)

    print()
    passed = sum(1 for r in results if r[2])
    print(f"{passed}/{len(results)} " + ("ALL_PASS" if passed == len(results) else "HAS_FAILURE"))
    print("判定：G4-1 计数层结构骨架（三层态射→空间 3、递归单向→时间 1、4=3+1、"
          "k_max=2×时空、静默 5、σ⁻¹=15、时间坐标良定义、层数唯一锁定 3、"
          "三层≠三个时间维）机检完成；「为何 N_gen=3」与空间/时间正交互补未证"
          "——**G4 未闭合**（结构骨架 ≠ 公设导出）。不关闭任何项。")


if __name__ == "__main__":
    main()
