# -*- coding: utf-8 -*-
"""
P7-5e-370 / G3-P2-5 态侧必要性判别 —— 四处落盘（probe / apply / verify，幂等）
=========================================================================
用法：
  python scripts/p7_5e370_state_necessity_landing.py probe
  python scripts/p7_5e370_state_necessity_landing.py apply
  python scripts/p7_5e370_state_necessity_landing.py verify

落盘四处：
  RESEARCH_STATE.md                                 新增 361
  paper/paper48_topological_forbidden_frequency.md  新增 286bx
  roadmap/phase102_baryon_lepton_parameter_free.md  新增 P7-5e-370
  E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md  新增 八十五
"""

import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P_RS = os.path.join(ROOT, "RESEARCH_STATE.md")
P_P48 = os.path.join(ROOT, "paper", "paper48_topological_forbidden_frequency.md")
P_ROAD = os.path.join(ROOT, "roadmap", "phase102_baryon_lepton_parameter_free.md")
P_DIG = r"E:\workspace\hyper-resolution\P7-5e_最新研究成果_2026-10-30.md"

A_RS = "**P2 未成立、G3 未闭合**；不关闭任何项（226 挂起、k(2) 开放）。"

SEG_RS = (
    "> **361（本轮，G3-P2-5：态侧必要性判别——块内标量态模流恒等、非标量权重才给出时间、"
    "忠实≠时间，2026-11-02）**：接 360。P2-4 已给载体**代数侧**必要条件（载体必须非交换、"
    "块标量实现恒等）；本轮补**态侧**一半（精确符号，无浮点）：①块内标量 ⟺ 对角权重相等"
    "（`diagMat_isScalar_iff`）；②块内标量忠实态（迹态型，如权重 1/2,1/2）的模实现是标量"
    "共轭 ⇒ 共轭恒等（`DiagState.conj_trivial`）；③块内非标量权重（如 2/3,1/3）⇒ 非对角"
    "探针 E₁₂ 被缩放 d₁/d₂≠1 ⇒ 存在非平凡共轭（`DiagState.conj_nontrivial`），逆否即"
    "「模实现恒等 ⟹ 权重相等」（`nontrivial_imp_nonScalar`）；④**忠实性本身不决定时间**"
    "（`faithful_not_imp_nontrivial`）：忠实块标量态恒等、非标量忠实态非平凡并存；"
    "⑤层权不同但块内标量仍恒等（`layerWeight_blockScalar_trivial`）⇒ **层权 e^{−2πn} 单独"
    "不构成时间推进**（369 C10 的态侧读法）。合读：载体侧「非交换」+ 态侧「块内非标量」"
    "是 P2 的两条并列必要条件。**资产**：新 Lean 模块 `G3StateNecessity.lean`（16 条定义/定理，"
    "`lake env lean` rc=0 零输出零告警）；判据 `scripts/p7_5e370_state_necessity_criteria.py` "
    "C01–C14 **14/14 ALL_PASS**。**诚实边界**：「忠实」只编码为对角权重为正（正定⟺忠实、"
    "正规性、σ-弱闭、因子性均未形式化）；`ρ^{it}` 复相位未构造；非对角密度矩阵谱分解未做；"
    "载体（RecObj 忠实正规态空间/模算子）仍未定义、vN 完成性未证 ⇒ **P2 未成立、G3 未闭合**；"
    "不关闭任何项（226 挂起、k(2) 开放），G3 继续挂起。"
)

A_P48 = ("诚实边界：参数周期归一为解释性输入；载体/vN 完成性缺失 ⇒ P2 未成立、G3 未闭合；"
         "不关闭任何项（226 挂起、k(2) 开放）。")

SEG_P48 = (
    "286bx（2026-11-02，**G3-P2-5 态侧必要性判别**）：接 286bw。①块内标量 ⟺ 对角权重相等；"
    "②块内标量忠实态（迹态型）模实现标量共轭 ⇒ 恒等；③块内非标量权重 ⇒ E₁₂ 被缩放 "
    "d₁/d₂≠1 ⇒ 非平凡共轭；逆否：恒等 ⟹ 权重相等；④忠实性本身不决定时间（块标量忠实态恒等、"
    "非标量忠实态非平凡并存）；⑤层权不同但块内标量仍恒等 ⇒ 层权 e^{−2πn} 单独不构成时间。"
    "合读：载体「非交换」+ 态「块内非标量」为 P2 两条并列必要条件。资产：`G3StateNecessity.lean`"
    "（16 条，rc=0 零告警）；判据 C01–C14 14/14 ALL_PASS。诚实边界：忠实只编码为对角权重正；"
    "ρ^{it} 复相位未构造；非对角谱分解未做；载体/vN 完成性缺失 ⇒ P2 未成立、G3 未闭合；"
    "不关闭任何项（226 挂起、k(2) 开放）。"
)

A_ROAD = ("缺口：参数周期归一为解释性输入；载体（RecObj 忠实正规态/模算子/状态空间）与 vN "
          "完成性仍未定义 ⇒ P2 未成立、G3 未闭合。不关闭任何项（226 挂起、k(2) 开放）。")

SEG_ROAD = (
    "P7-5e-370（G3-P2-5：态侧必要性判别——块内标量态模流恒等/非标量权重才给出时间/"
    "忠实≠时间，2026-11-02）：接 369。**结论**：①块内标量 ⟺ 对角权重相等；②块内标量忠实态"
    "（迹态型 1/2,1/2）模实现标量共轭 ⇒ 共轭恒等；③块内非标量权重（2/3,1/3）⇒ E₁₂ 被缩放 "
    "d₁/d₂≠1 ⇒ 非平凡共轭；逆否：恒等 ⟹ 权重相等；④忠实性本身不决定时间（两类忠实态并存）；"
    "⑤层权不同但块内标量仍恒等 ⇒ **层权 e^{−2πn} 单独不构成时间推进**（369 C10 态侧读法）。"
    "合读：载体「非交换」（369）+ 态「块内非标量」（370）为 P2 两条并列必要条件。资产："
    "`G3StateNecessity.lean` 16 条（rc=0 零告警）；判据 `p7_5e370_state_necessity_criteria.py` "
    "C01–C14 14/14。缺口：忠实只编码为对角权重正；ρ^{it} 复相位未构造；非对角谱分解未做；"
    "载体/vN 完成性未定义 ⇒ P2 未成立、G3 未闭合。不关闭任何项（226 挂起、k(2) 开放）。"
)

A_DIG = ("**诚实边界**：载体（RecObj 忠实正规态/模算子/状态空间）未定义、vN 完成性未证 ⇒ "
         "P2 未成立、G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）。")

SEG_DIG = (
    "## 八十五、G3-P2-5 态侧必要性判别：块内标量态无模流、非标量权重才给出时间（2026-11-02）\n\n"
    "**口径**：接 360。P2-4 给出载体代数侧必要条件（载体必须非交换、块标量实现恒等）；"
    "本轮补态侧一半（精确符号，无浮点；C01–C14 14/14 ALL_PASS）。\n\n"
    "1. **块内标量 ⟺ 对角权重相等**：对角密度矩阵是标量矩阵当且仅当两个权重相等。\n"
    "2. **块内标量忠实态 ⇒ 模流恒等**：迹态型态（权重 1/2,1/2）的模实现是标量共轭，"
    "故共轭不动任何元素——**忠实不等于非平凡时间**。\n"
    "3. **块内非标量权重 ⇒ 非平凡共轭**：权重 2/3,1/3 时非对角元素 E₁₂ 被缩放 2，故模实现"
    "不恒等；其逆否即「模实现恒等 ⟹ 权重必须相等」。\n"
    "4. **层权单独不构成时间**：两层块内标量、块间权重不等（如 1/2 与 4）的全块共轭仍是"
    "恒等——层权 `e^{−2πn}` 只在块间起作用（369 C10 的态侧读法）。\n"
    "5. **合读**：载体侧「非交换」+ 态侧「块内非标量」是 P2 的两条**并列必要条件**；"
    "任一缺失都不能得到非平凡时间。\n\n"
    "**资产**：`G3StateNecessity.lean`（16 条定义/定理，`lake env lean` rc=0 零输出零告警）；"
    "`scripts/p7_5e370_state_necessity_criteria.py` C01–C14 14/14 ALL_PASS。\n\n"
    "**诚实边界**：「忠实」只编码为对角权重为正（正定⟺忠实、正规性、σ-弱闭、因子性未形式化）；"
    "ρ^{it} 复相位未构造；非对角密度矩阵谱分解未做；载体（RecObj 忠实正规态空间/模算子）仍未"
    "定义、vN 完成性未证 ⇒ P2 未成立、G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）。"
)

ITEMS = [
    ("RS", P_RS, A_RS, SEG_RS, "361（本轮，G3-P2-5"),
    ("P48", P_P48, A_P48, SEG_P48, "286bx（2026-11-02"),
    ("ROAD", P_ROAD, A_ROAD, SEG_ROAD, "P7-5e-370（G3-P2-5"),
    ("DIG", P_DIG, A_DIG, SEG_DIG, "## 八十五、"),
]


def read_raw(path):
    with io.open(path, "r", encoding="utf-8", newline="") as fh:
        return fh.read()


def nl_of(raw):
    return "\r\n" if "\r\n" in raw else "\n"


def probe():
    ok = True
    for name, path, anchor, _seg, marker in ITEMS:
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
    for name, path, anchor, seg, marker in ITEMS:
        raw = read_raw(path)
        nl = nl_of(raw)
        if marker in raw:
            print(f"[{name}] already applied, skip")
            continue
        if name == "DIG":
            new = raw.replace(anchor, anchor + nl + nl + seg, 1)
        else:
            new = raw.replace(anchor, anchor + nl + seg, 1)
        with io.open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(new)
        print(f"[{name}] applied")
    return True


def verify():
    ok = True
    for name, path, anchor, _seg, marker in ITEMS:
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
