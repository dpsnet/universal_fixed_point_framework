# -*- coding: utf-8 -*-
"""
P7-5e-371 / G3-P2-6 内/外轴正交判别 —— 四处落盘（probe / apply / verify，幂等）
===========================================================================
用法：
  python scripts/p7_5e371_axis_orthogonality_landing.py probe
  python scripts/p7_5e371_axis_orthogonality_landing.py apply
  python scripts/p7_5e371_axis_orthogonality_landing.py verify

落盘四处：
  RESEARCH_STATE.md                                 新增 362
  paper/paper48_topological_forbidden_frequency.md  新增 286by
  roadmap/phase102_baryon_lepton_parameter_free.md  新增 P7-5e-371
  E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md  新增 八十六
"""

import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P_RS = os.path.join(ROOT, "RESEARCH_STATE.md")
P_P48 = os.path.join(ROOT, "paper", "paper48_topological_forbidden_frequency.md")
P_ROAD = os.path.join(ROOT, "roadmap", "phase102_baryon_lepton_parameter_free.md")
P_DIG = r"E:\workspace\hyper-resolution\P7-5e_最新研究成果_2026-10-30.md"

A_RS = ("载体（RecObj 忠实正规态空间/模算子）仍未定义、vN 完成性未证 ⇒ "
        "**P2 未成立、G3 未闭合**；不关闭任何项（226 挂起、k(2) 开放），G3 继续挂起。")

SEG_RS = (
    "> **362（本轮，G3-P2-6：内/外轴与恒等/非恒等轴正交——有限块判别性 no-go，2026-11-02）**："
    "接 361。P2-4/370 已给载体「非交换」与态「块内非标量」两条并列必要条件；本轮回答剩余判别问题"
    "「内/外这一轴能否充当 P2（模流时间）的判据」。在两层乘积代数 `M₂(ℚ) × M₂(ℚ)`（有限型 I）内机检："
    "①任意单位共轭 `Ad u` 是 `AlgEquiv` 且按定义就是内实现（`innerAutEquiv` / `innerAutEquiv_inner`）"
    "⇒ 有限块中「内实现」构造性普遍；②乘积单位分解（`unitFst`/`unitSnd`/`prodUnit`）⇒ 任何内实现逐块"
    "内实现（`innerRealization_imp_innerBlock`），块交换因而是外（`swapBlock_outer`）且非恒等"
    "（`swapBlock_ne_refl`）；③块内标量态切片恒等（`blockStateAut_trivial`）、块内非标量切片非平凡"
    "（`blockStateAut_nontrivial`）且两者都是内实现（`blockStateAut_inner`）⇒ 时间不必是外；"
    "④块交换与任何块对角内切片不同（`blockwiseAut_ne_swap`）⇒ 外也不必是时间；⑤主定理 "
    "`axes_orthogonal`：四象限中（内,恒等）、（内,非平凡）、（外,非平凡）存在，（外,恒等）不存在"
    "——两轴正交。**结论（判别性 no-go）**：内/外轴在有限块模型内对 P2 无判别力；P2 判据只能落在"
    "模算子/态的谱结构（载体类型）。**资产**：新 Lean 模块 `G3P2AxisOrthogonality.lean`（19 条定义/定理："
    "7 定义 + 12 定理，`lake env lean` rc=0 零输出零告警）；判据 "
    "`scripts/p7_5e371_axis_orthogonality_criteria.py` C01–C14 **14/14 ALL_PASS**。**诚实边界**："
    "仅有限型 I 乘积块模型；经典「I/II 型因子模流由 `ρ^{it} ∈ A^×` 实现」与 **III 型因子外模流**未形式化；"
    "「流」只是常数切片族，未构造连续性/解析延拓/KMS 本体；载体（RecObj 忠实正规态空间/模算子/状态空间）"
    "仍未定义、vN 完成性未证 ⇒ **P2 未成立、G3 未闭合**；不关闭任何项（226 挂起、k(2) 开放），"
    "G3 继续挂起。"
)

A_P48 = ("诚实边界：忠实只编码为对角权重正；ρ^{it} 复相位未构造；非对角谱分解未做；"
         "载体/vN 完成性缺失 ⇒ P2 未成立、G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）。")

SEG_P48 = (
    "286by（2026-11-02，**G3-P2-6 内/外轴正交判别**）：接 286bx。在 `M₂(ℚ)×M₂(ℚ)` 内机检："
    "①任意单位共轭 `Ad u` 即内实现（`innerAutEquiv_inner`）；②乘积单位分解使任何内实现逐块内实现 ⇒ "
    "块交换外（`swapBlock_outer`）且非恒等；③块内标量态切片恒等、非标量切片非平凡，两者皆内 ⇒ "
    "时间不必是外；④块交换 ≠ 任何块对角切片 ⇒ 外不必是时间；⑤`axes_orthogonal`：四象限仅"
    "「外,恒等」不存在 ⇒ 两轴正交。结论：**内/外轴对 P2 无判别力**（判别性 no-go）。资产："
    "`G3P2AxisOrthogonality.lean` 19 条（rc=0 零告警）；判据 C01–C14 14/14 ALL_PASS。诚实边界："
    "仅有限型 I；III 型外模流未形式化；流为常数切片族；载体/vN 完成性缺失 ⇒ P2 未成立、G3 未闭合；"
    "不关闭任何项（226 挂起、k(2) 开放）。"
)

A_ROAD = ("缺口：忠实只编码为对角权重正；ρ^{it} 复相位未构造；非对角谱分解未做；"
          "载体/vN 完成性未定义 ⇒ P2 未成立、G3 未闭合。不关闭任何项（226 挂起、k(2) 开放）。")

SEG_ROAD = (
    "P7-5e-371（G3-P2-6：内/外轴与恒等/非恒等轴正交——判别性 no-go，2026-11-02）：接 370。"
    "**结论**：①有限块中任意单位共轭都是内实现；②乘积单位分解 ⇒ 内 ⟹ 逐块内；块交换是外且非恒等；"
    "③块内标量态切片恒等、非标量切片非平凡，两者皆内 ⇒ 时间不必外；④块交换 ≠ 块对角切片 ⇒ "
    "外不必时间；⑤主定理 `axes_orthogonal`：四象限仅「外,恒等」不存在 ⇒ 内/外轴与时间/非时间轴"
    "正交，内/外对 P2 无判别力。资产：`G3P2AxisOrthogonality.lean` 19 条（rc=0 零告警）；判据 "
    "`p7_5e371_axis_orthogonality_criteria.py` C01–C14 14/14。缺口：仅有限型 I 乘积块模型；"
    "III 型外模流未形式化；流为常数切片族；载体/vN 完成性未定义 ⇒ P2 未成立、G3 未闭合。"
    "不关闭任何项（226 挂起、k(2) 开放）。"
)

A_DIG = ("## 八十五、G3-P2-5 态侧必要性判别：块内标量态无模流、非标量权重才给出时间（2026-11-02）")

SEG_DIG = (
    "## 八十六、G3-P2-6 内/外轴正交：内/外不是时间判据（判别性 no-go，2026-11-02）\n\n"
    "**口径**：接 361。P2-4/370 已给出载体「非交换」与态「块内非标量」两条并列必要条件；"
    "本轮判别「内/外轴」能否充当 P2 的判据（精确符号，无浮点；C01–C14 14/14 ALL_PASS）。\n\n"
    "1. **内实现构造性普遍**：在 `M₂(ℚ)×M₂(ℚ)` 中任意单位 u 的共轭 `Ad u` 都是 `AlgEquiv`，"
    "且按定义满足内实现。\n"
    "2. **内 ⟹ 逐块内**：乘积单位分解（`unitFst`/`unitSnd`）给出逐块实现；块交换因此是外"
    "（且非恒等）。\n"
    "3. **时间不必是外**：块内标量态切片恒等、非标量切片非平凡，两类都是内实现。\n"
    "4. **外也不必是时间**：块交换与任何块对角内切片都不同。\n"
    "5. **主定理 `axes_orthogonal`**：四象限中（内,恒等）、（内,非平凡）、（外,非平凡）存在，"
    "（外,恒等）不存在 ⇒ 两轴正交，**内/外对 P2 无判别力**。\n\n"
    "**资产**：`G3P2AxisOrthogonality.lean`（19 条定义/定理，`lake env lean` rc=0 零输出零告警）；"
    "`scripts/p7_5e371_axis_orthogonality_criteria.py` C01–C14 14/14 ALL_PASS。\n\n"
    "**诚实边界**：只证有限型 I 乘积块模型；经典 I/II 型因子模流内实现与 **III 型因子外模流**未形式化；"
    "「流」仅为常数切片族，未构造连续性/解析延拓/KMS 本体；载体（RecObj 忠实正规态空间/模算子）仍未"
    "定义、vN 完成性未证 ⇒ P2 未成立、G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）。"
)

ITEMS = [
    ("RS", P_RS, A_RS, SEG_RS, "362（本轮，G3-P2-6", "after"),
    ("P48", P_P48, A_P48, SEG_P48, "286by（2026-11-02", "after"),
    ("ROAD", P_ROAD, A_ROAD, SEG_ROAD, "P7-5e-371（G3-P2-6", "after"),
    ("DIG", P_DIG, A_DIG, SEG_DIG, "## 八十六、", "before"),
]


def read_raw(path):
    with io.open(path, "r", encoding="utf-8", newline="") as fh:
        return fh.read()


def nl_of(raw):
    return "\r\n" if "\r\n" in raw else "\n"


def probe():
    ok = True
    for name, path, anchor, _seg, marker, _where in ITEMS:
        raw = read_raw(path)
        ca = raw.count(anchor)
        cm = raw.count(marker)
        nl = "CRLF" if nl_of(raw) == chr(13) + chr(10) else "LF"
        print(f"[{name}] anchor_count={ca} marker_count={cm} newline={nl}")
        if ca != 1 or cm > 1:
            ok = False
    return ok


def apply():
    if not probe():
        print("PROBE FAIL — 锚点不唯一，停止 apply")
        return False
    for name, path, anchor, seg, marker, where in ITEMS:
        raw = read_raw(path)
        nl = nl_of(raw)
        if marker in raw:
            print(f"[{name}] already applied, skip")
            continue
        body = seg.replace("\n", nl)
        if where == "before":
            new = raw.replace(anchor, body + nl + nl + anchor, 1)
        elif name == "DIG":
            new = raw.replace(anchor, anchor + nl + nl + body, 1)
        else:
            new = raw.replace(anchor, anchor + nl + body, 1)
        with io.open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(new)
        print(f"[{name}] applied ({where})")
    return True


def verify():
    ok = True
    for name, path, anchor, _seg, marker, _where in ITEMS:
        raw = read_raw(path)
        ca = raw.count(anchor)
        cm = raw.count(marker)
        print(f"[{name}] anchor={ca} marker={cm}")
        if ca != 1 or cm != 1:
            ok = False
    raw = read_raw(P_ROAD)
    crlf = raw.count("\r\n")
    lf_solo = raw.count("\n") - crlf
    print(f"[ROAD] CRLF={crlf} LF-solo={lf_solo}")
    if lf_solo != 0:
        ok = False
    print("VERIFY " + ("ALL_PASS" if ok else "FAILED"))
    return ok


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "probe"
    if mode == "probe":
        sys.exit(0 if probe() else 1)
    if mode == "apply":
        sys.exit(0 if apply() else 1)
    if mode == "verify":
        sys.exit(0 if verify() else 1)
    print(f"unknown mode: {mode}")
    sys.exit(2)
