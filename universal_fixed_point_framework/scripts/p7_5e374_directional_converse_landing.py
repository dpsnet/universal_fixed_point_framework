# -*- coding: utf-8 -*-
"""
P7-5e-374 / G3-P1b-3 真逆向条件形式 —— 四处落盘（probe / apply / verify，幂等）
===========================================================================
用法：
  python scripts/p7_5e374_directional_converse_landing.py probe
  python scripts/p7_5e374_directional_converse_landing.py apply
  python scripts/p7_5e374_directional_converse_landing.py verify

落盘四处：
  RESEARCH_STATE.md                                 新增 365
  paper/paper48_topological_forbidden_frequency.md  新增 286cb
  roadmap/phase102_baryon_lepton_parameter_free.md  新增 P7-5e-374
  E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md   新增 八十九
"""

import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P_RS = os.path.join(ROOT, "RESEARCH_STATE.md")
P_P48 = os.path.join(ROOT, "paper", "paper48_topological_forbidden_frequency.md")
P_ROAD = os.path.join(ROOT, "roadmap", "phase102_baryon_lepton_parameter_free.md")
P_DIG = r"E:\workspace\hyper-resolution\P7-5e_最新研究成果_2026-10-30.md"

A_RS = ("Tomita `Δ_mod^{it} ∈ A^×` 是**模型输入**（`DiagState.unit` 编码），不是由 KMS 推出的定理；"
        "流为常数切片族，未构造连续性/解析延拓/KMS 本体；载体（RecObj 忠实正规态空间/模算子/状态空间）"
        "仍未定义、vN 完成性未证 ⇒ **P2 未成立、G3 未闭合**；不关闭任何项（226 挂起、k(2) 开放），"
        "G3 继续挂起。")

SEG_RS = (
    "> **365（本轮，G3-P1b-3：真逆向的条件形式——层步定向 ⟹ 严格升层、模权改变、无回退，2026-11-03）**："
    "接 364。368 只机检了「外 ⟹ 模权不可被内实现吸收」（`outer_not_diagonal` / "
    "`outer_moves_modular_weight`），**未做**「外 ⟹ 严格升层」——后者需要方向性（每步只能「保持」或"
    "「前进 k 层」）。本轮把方向性**显式化**为输入并机检条件链：①`LayerStep L σ k := ∀a, "
    "L(σa)=L a ∨ L(σa)=L a+k`，`k=0` 两支重合 ⟹ 退化为层对角（`layerStep_zero_iff`）；②层对角皆内"
    "实现（`hdiag_inner`，与 368 同口径）+ 外 + 层步 ⟹ **存在 a 使 `L(σa)=L a+k`**"
    "（`layerStep_outer_ascent`）；③严格升层 ⟹ 该元素模权改变（`layerStep_outer_weight_moves`）；"
    "gap>0 时模权**严格下降**（`ascent_weight_decreases`，层权比 `e^{−2π·gap·k}<1`）；④每点都 +k"
    "（`LayerAdvance`）⟹ m 步迭代 `L(σ^m a)=L a+m·k=advanceIter k m (L a)`"
    "（`layerAdvance_iterate` / `layerAdvance_iterate_eq_advanceIter`），k≠0、m≠0 时无回退"
    "（`layerAdvance_iterate_no_return`）；⑤主定理 `directional_converse` 三支打包（升层 ∧ 模权改变 ∧ "
    "非恒等）；⑥反例：`boolLayer` 下 `bnotEquiv` 移动层但**不是任何 k 的层步**"
    "（`bnotEquiv_not_directed`）⟹ 方向不能由外性/非对角自动得到。资产：新 Lean 模块 "
    "`G3P1b3DirectionalConverse.lean`（17 条：4 定义 + 13 定理，`lake env lean` rc=0 零输出零告警，"
    "复用 368 构件不重复定义）；判据 `scripts/p7_5e374_directional_converse_criteria.py` C01–C16 "
    "**16/16 ALL_PASS**（精确有理/符号，无浮点；含无 axiom/sorry/native_decide 机检）。**诚实边界**："
    "`LayerStep`/`LayerAdvance` 是**显式输入**，不是从 Tomita `Δ_mod` 或 KMS β=1 推出的定理"
    "（「模流生成元非负 ⟹ 每步至多前进 k 层」**未形式化**）；本模块只把 368 的模权链补到「严格升层」"
    "这一环，**不宣称由外性推出单向**（单向性由 P1a' `p1a_no_cycle` 机检）；载体（RecObj 忠实正规态"
    "空间/模算子/状态空间）仍未定义、vN 完成性未证 ⇒ **P2 未成立、G3 未闭合**；**方向性是显式输入、"
    "未从 Δ_mod/KMS 导出**；不关闭任何项（226 挂起、k(2) 开放），G3 继续挂起。"
)

A_P48 = ("诚实边界：仅有限型 I 乘积块模型；III 型外模流存在性未形式化；Tomita Δ∈A^× 为模型输入；"
         "流为常数切片；载体/vN 完成性缺失 ⇒ P2 未成立、G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）。")

SEG_P48 = (
    "286cb（2026-11-03，**G3-P1b-3 真逆向条件形式**）：接 286ca（论证上接 368）。368 已机检"
    "「外 ⟹ 模权不可内吸收」，本轮补「外 ⟹ 严格升层」这一环，把方向性显式化为输入："
    "`LayerStep L σ k`（每点保持或 +k）；`k=0` 退化 ⟹ 层对角；层对角皆内实现 + 外 + 层步 ⟹ "
    "∃a `L(σa)=L a+k`（`layerStep_outer_ascent`）⟹ 模权改变（`layerStep_outer_weight_moves`）；"
    "gap>0 时模权严格下降（层权比 e^{−2π·gap·k}<1）；`LayerAdvance`（每点 +k）⟹ m 步 = "
    "`advanceIter k m`、k,m≠0 无回退；主定理 `directional_converse` 三支打包。反例：`bnotEquiv` "
    "移动层但不是任何 k 的层步 ⟹ 方向不能由外性自动得到。资产：`G3P1b3DirectionalConverse.lean` "
    "17 条（rc=0 零告警）；判据 C01–C16 16/16 ALL_PASS。诚实边界：`LayerStep`/`LayerAdvance` 为显式"
    "输入，未从 Δ_mod/KMS 导出；只补严格升层一环，不宣称由外性推出单向（P1a' `p1a_no_cycle` 已机检）；"
    "载体/vN 完成性缺失 ⇒ P2 未成立、G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）；方向性为显式"
    "输入、未从 Δ_mod/KMS 导出。"
)

A_ROAD = ("缺口：仅有限型 I 乘积块模型；III 型外模流存在性未形式化；Tomita Δ∈A^× 为模型输入；"
          "流为常数切片族；载体/vN 完成性未定义 ⇒ P2 未成立、G3 未闭合。不关闭任何项（226 挂起、k(2) 开放）。")

SEG_ROAD = (
    "P7-5e-374（G3-P1b-3：真逆向的条件形式——层步定向 ⟹ 严格升层，2026-11-03）：接 373（论证上接 "
    "368）。368 只证「外 ⟹ 模权不可内吸收」；本轮把方向性显式化为输入并机检条件链："
    "①`LayerStep L σ k`（每点保持或 +k），`k=0` ⟹ 层对角；②层对角皆内 + 外 + 层步 ⟹ ∃a "
    "`L(σa)=L a+k`；③升层 ⟹ 模权改变，gap>0 时严格下降（层权比 e^{−2π·gap·k}<1）；④"
    "`LayerAdvance` ⟹ m 步 = `advanceIter k m`，k,m≠0 无回退；⑤主定理 `directional_converse` "
    "三支打包；⑥反例 `bnotEquiv` 移动层但不是任何 k 的层步。资产："
    "`G3P1b3DirectionalConverse.lean` 17 条（rc=0 零告警）；判据 "
    "`p7_5e374_directional_converse_criteria.py` C01–C16 16/16。缺口：方向性为显式输入（未从 "
    "Δ_mod/KMS 导出）；「模流生成元非负 ⟹ 每步至多前进 k 层」未形式化；载体/vN 完成性未定义 ⇒ "
    "P2 未成立、G3 未闭合。不关闭任何项（226 挂起、k(2) 开放）。"
)

A_DIG = "## 八十八、G3-P2-8 载体类型接口骨架：只定义与桥接（2026-11-03）"

SEG_DIG = (
    "## 八十九、G3-P1b-3 真逆向的条件形式：层步定向 ⟹ 严格升层、模权改变、无回退（2026-11-03）\n\n"
    "**口径**：接 365。368 已机检「外 ⟹ 模权不可内吸收」；本轮补「外 ⟹ 严格升层」这一环，"
    "**把方向性显式化为输入**（`LayerStep` / `LayerAdvance`），只机检条件链，不从 Δ_mod/KMS 导出方向。\n\n"
    "1. **`LayerStep L σ k`**：每点「保持」或「+k」；`k=0` 两支重合 ⟹ 层对角。\n"
    "2. **定向逆向**：层对角皆内实现 + 外 + 层步 ⟹ 存在 a 被抬高 k 层（`layerStep_outer_ascent`）。\n"
    "3. **模权后果**：升层 ⟹ 模权改变；gap>0 时严格下降（层权比 e^{−2π·gap·k}<1）。\n"
    "4. **单向桥接**：`LayerAdvance`（每点 +k）⟹ m 步 = `advanceIter k m`；k,m≠0 无回退。\n"
    "5. **主定理 `directional_converse`**：升层 ∧ 模权改变 ∧ 非恒等三支打包。\n"
    "6. **反例**：`bnotEquiv` 移动层但不是任何 k 的层步 ⟹ 方向不能由外性/非对角自动得到。\n\n"
    "**资产**：`G3P1b3DirectionalConverse.lean`（17 条：4 定义 + 13 定理，rc=0 零输出零告警；"
    "复用 368 构件不重复定义）；`scripts/p7_5e374_directional_converse_criteria.py` C01–C16 "
    "16/16 ALL_PASS（精确有理/符号，无浮点）。\n\n"
    "**诚实边界**：`LayerStep`/`LayerAdvance` 为**显式输入**，「模流生成元非负 ⟹ 每步至多前进 k 层」"
    "**未形式化**；不宣称由外性推出单向（P1a' `p1a_no_cycle` 已机检）；载体/vN 完成性未定义 ⇒ "
    "P2 未成立、G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）。"
)

ITEMS = [
    ("RS", P_RS, A_RS, SEG_RS, "365（本轮，G3-P1b-3", "after"),
    ("P48", P_P48, A_P48, SEG_P48, "286cb（2026-11-03", "after"),
    ("ROAD", P_ROAD, A_ROAD, SEG_ROAD, "P7-5e-374（G3-P1b-3", "after"),
    ("DIG", P_DIG, A_DIG, SEG_DIG, "## 八十九、", "before"),
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
