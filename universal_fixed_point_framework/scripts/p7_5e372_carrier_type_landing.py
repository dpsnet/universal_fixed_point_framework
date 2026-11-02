# -*- coding: utf-8 -*-
"""
P7-5e-372 / G3-P2-7 载体类型判据 —— 四处落盘（probe / apply / verify，幂等）
===========================================================================
用法：
  python scripts/p7_5e372_carrier_type_landing.py probe
  python scripts/p7_5e372_carrier_type_landing.py apply
  python scripts/p7_5e372_carrier_type_landing.py verify

落盘四处：
  RESEARCH_STATE.md                                 新增 363
  paper/paper48_topological_forbidden_frequency.md  新增 286bz
  roadmap/phase102_baryon_lepton_parameter_free.md  新增 P7-5e-372
  E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md   新增 八十七
"""

import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P_RS = os.path.join(ROOT, "RESEARCH_STATE.md")
P_P48 = os.path.join(ROOT, "paper", "paper48_topological_forbidden_frequency.md")
P_ROAD = os.path.join(ROOT, "roadmap", "phase102_baryon_lepton_parameter_free.md")
P_DIG = r"E:\workspace\hyper-resolution\P7-5e_最新研究成果_2026-10-30.md"

A_RS = ("仅有限型 I 乘积块模型；经典「I/II 型因子模流由 `ρ^{it} ∈ A^×` 实现」与 "
        "**III 型因子外模流**未形式化；「流」只是常数切片族，未构造连续性/解析延拓/KMS 本体；"
        "载体（RecObj 忠实正规态空间/模算子/状态空间）仍未定义、vN 完成性未证 ⇒ "
        "**P2 未成立、G3 未闭合**；不关闭任何项（226 挂起、k(2) 开放），G3 继续挂起。")

SEG_RS = (
    "> **363（本轮，G3-P2-7：载体类型判据——有限型 I 模流必内、外流不可由忠实态生成，2026-11-03）**："
    "接 362。371 已证内/外轴对 P2 无判别力，判据只能落在载体类型。本轮把该判据的**可机检部分**"
    "形式化：①任意单位路径流必内（`unitFlow_inner`）；②外自同构不可能等于任何单位共轭 "
    "`Ad u`（`outer_not_unitFlow`）——即模算子 `Δ_mod^{it}` 不在代数单位群内，这是「载体类型」"
    "的代数读法；③有限型 I 的忠实对角态流全内（`finiteTypeI_stateFlow_inner`）且不可能是外流"
    "（`finiteTypeI_stateFlow_not_outer`）；④时间的精确判据：态流恒等 ⟺ 两个块内权重都相等"
    "（`stateFlow_trivial_iff`，补上第二块对称情形 `blockStateAut_nontrivial_snd`）；⑤主定理 "
    "`carrierType_criterion` 四支合取：全内 ∧ 无外态流 ∧ （恒等 ⟺ 块内标量）∧ 非平凡时间存在 ∧ "
    "块交换不是任何态流切片。**结论**：P2 的判据是**载体类型**（Δ_mod^{it} 能否被代数单位实现），"
    "不是内/外轴；有限型 I 内可以同时有非平凡时间与不可生成的外自同构。**资产**：新 Lean 模块 "
    "`G3P2CarrierType.lean`（11 条：3 定义 + 8 定理，`lake env lean` rc=0 零输出零告警）；判据 "
    "`scripts/p7_5e372_carrier_type_criteria.py` C01–C14 **14/14 ALL_PASS**。**诚实边界**："
    "「有限型 I」只指 `M₂(ℚ)×M₂(ℚ)` 乘积块模型；经典 I/II 型因子模流内实现、**III 型因子外模流"
    "的存在性**均未形式化；Tomita `Δ_mod^{it} ∈ A^×` 是**模型输入**（`DiagState.unit` 编码），"
    "不是由 KMS 推出的定理；流为常数切片族，未构造连续性/解析延拓/KMS 本体；载体（RecObj 忠实"
    "正规态空间/模算子/状态空间）仍未定义、vN 完成性未证 ⇒ **P2 未成立、G3 未闭合**；不关闭任何项"
    "（226 挂起、k(2) 开放），G3 继续挂起。"
)

A_P48 = ("诚实边界：仅有限型 I；III 型外模流未形式化；流为常数切片族；载体/vN 完成性缺失 ⇒ "
         "P2 未成立、G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）。")

SEG_P48 = (
    "286bz（2026-11-03，**G3-P2-7 载体类型判据**）：接 286by。机检：①任意单位路径流必内"
    "（`unitFlow_inner`）；②外 ⟹ 无单位实现（`outer_not_unitFlow`）——模算子 `Δ_mod^{it}` 不在"
    "代数单位群内；③有限型 I 的忠实对角态流全内且不可能外（`finiteTypeI_stateFlow_inner` / "
    "`_not_outer`）；④态流恒等 ⟺ 两块权重皆相等（`stateFlow_trivial_iff`）；⑤`carrierType_criterion`："
    "全内 ∧ 无外态流 ∧ 非平凡时间存在 ∧ 块交换非任何态流切片。结论：**P2 判据 = 载体类型"
    "（Δ_mod^{it} 的单位可实现性）**，内/外轴无判别力。资产：`G3P2CarrierType.lean` 11 条"
    "（rc=0 零告警）；判据 C01–C14 14/14 ALL_PASS。诚实边界：仅有限型 I 乘积块模型；"
    "III 型外模流存在性未形式化；Tomita Δ∈A^× 为模型输入；流为常数切片；载体/vN 完成性缺失 "
    "⇒ P2 未成立、G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）。"
)

A_ROAD = ("缺口：仅有限型 I 乘积块模型；III 型外模流未形式化；流为常数切片族；"
          "载体/vN 完成性未定义 ⇒ P2 未成立、G3 未闭合。不关闭任何项（226 挂起、k(2) 开放）。")

SEG_ROAD = (
    "P7-5e-372（G3-P2-7：载体类型判据——有限型 I 模流必内、外流不可由忠实态生成，2026-11-03）："
    "接 371。**结论**：①任意单位路径流必内；②外 ⟹ 无单位实现 `Ad u`（模算子 `Δ_mod^{it}` 不在"
    "代数单位群内）；③有限型 I 的忠实对角态流全内、不可能是外流；④态流恒等 ⟺ 两块权重皆相等"
    "（时间存在 ⟺ 块内非标量，含第二块对称情形）；⑤主定理 `carrierType_criterion`：全内 ∧ "
    "无外态流 ∧ 时间判据 ∧ 非平凡时间存在 ∧ 块交换非任何态流切片 ⇒ **P2 判据 = 载体类型"
    "（Δ_mod^{it} 的单位可实现性）**，内/外轴无判别力。资产：`G3P2CarrierType.lean` 11 条"
    "（rc=0 零告警）；判据 `p7_5e372_carrier_type_criteria.py` C01–C14 14/14。缺口：仅有限型 I "
    "乘积块模型；III 型外模流存在性未形式化；Tomita Δ∈A^× 为模型输入；流为常数切片族；"
    "载体/vN 完成性未定义 ⇒ P2 未成立、G3 未闭合。不关闭任何项（226 挂起、k(2) 开放）。"
)

A_DIG = "## 八十六、G3-P2-6 内/外轴正交：内/外不是时间判据（判别性 no-go，2026-11-02）"

SEG_DIG = (
    "## 八十七、G3-P2-7 载体类型判据：有限型 I 模流必内、外流不可由忠实态生成（2026-11-03）\n\n"
    "**口径**：接 362。371 已证内/外轴对 P2 无判别力，判据只能落在载体类型。本轮把该判据的"
    "可机检部分形式化（精确符号，无浮点；C01–C14 14/14 ALL_PASS）。\n\n"
    "1. **单位路径流必内**：任意 `u : ℝ → A^×` 给出的 `Ad u_t` 每切片都是内实现。\n"
    "2. **外 ⟹ 无单位实现**：外自同构不可能等于任何 `Ad u`；即模算子 `Δ_mod^{it}` 不在代数"
    "单位群内——这是「载体类型」的代数读法。\n"
    "3. **有限型 I 的态流全内**：忠实对角态的模实现被编码为单位共轭，故其流必内、不可能是外流。\n"
    "4. **时间的精确判据**：态流恒等 ⟺ 两个块内权重都相等（时间存在 ⟺ 块内非标量；含第二块"
    "对称情形）。\n"
    "5. **主定理 `carrierType_criterion`**：全内 ∧ 无外态流 ∧ 时间判据 ∧ 非平凡时间存在 ∧ "
    "块交换不是任何态流切片 ⇒ **P2 的判据是载体类型（Δ_mod^{it} 的单位可实现性）**，而不是"
    "内/外轴；有限型 I 内可以同时有非平凡时间与不可生成的外自同构。\n\n"
    "**资产**：`G3P2CarrierType.lean`（11 条定义/定理：3 定义 + 8 定理，`lake env lean` rc=0 "
    "零输出零告警）；`scripts/p7_5e372_carrier_type_criteria.py` C01–C14 14/14 ALL_PASS。\n\n"
    "**诚实边界**：只证 `M₂(ℚ)×M₂(ℚ)` 乘积块模型；经典 I/II 型因子模流内实现与 **III 型因子"
    "外模流的存在性**均未形式化；Tomita `Δ_mod^{it} ∈ A^×` 是模型输入（`DiagState.unit` 编码），"
    "不是由 KMS 推出的定理；「流」为常数切片族，未构造连续性/解析延拓/KMS 本体；载体（RecObj "
    "忠实正规态空间/模算子）仍未定义、vN 完成性未证 ⇒ P2 未成立、G3 未闭合；不关闭任何项"
    "（226 挂起、k(2) 开放）。"
)

ITEMS = [
    ("RS", P_RS, A_RS, SEG_RS, "363（本轮，G3-P2-7", "after"),
    ("P48", P_P48, A_P48, SEG_P48, "286bz（2026-11-03", "after"),
    ("ROAD", P_ROAD, A_ROAD, SEG_ROAD, "P7-5e-372（G3-P2-7", "after"),
    ("DIG", P_DIG, A_DIG, SEG_DIG, "## 八十七、", "before"),
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
