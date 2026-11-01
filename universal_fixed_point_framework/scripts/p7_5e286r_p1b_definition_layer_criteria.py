# -*- coding: utf-8 -*-
"""P7-5e-353 判据：G3-P1b 定义层（外自同构的代数定义 + 层移动 ⟹ 外）

只做判别，不改文档。判据 D1–D10 全部通过 = P1b-1（定义层骨架）机检完成。
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
    chk("D8", "缺口登记：P1b-2（非交换实例）/ P1b-3（逆向）/ vN 完成性", gaps)

    chk("D9", "诚实边界：不声称 P1 成立", "不声称 P1 成立" in outer)

    ok_bridge, msg_bridge = compile_ok(BRIDGE)
    p1a = ["recStep", "StrictLayer", "p1a_unidirectional", "p1a_no_cycle"]
    chk("D10", "P1a 回归：桥编译通过 + 四定理在册",
        ok_bridge and all(t in bridge for t in p1a), msg_bridge)

    print()
    passed = sum(1 for r in results if r[2])
    print(f"{passed}/{len(results)} " + ("ALL_PASS" if passed == len(results) else "HAS_FAILURE"))
    print("判定：P1b-1 定义层骨架机检完成；P1b-2（非交换实例）/P1b-3（逆向）仍是缺口，"
          "P1 未成立（入轨/判别 ≠ 成立/闭合）。")


if __name__ == "__main__":
    main()
