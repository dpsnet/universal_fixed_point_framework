# -*- coding: utf-8 -*-
"""
P7-5e-369 / G3-P2-4 载体必要性判别 —— 四处落盘（probe / apply / verify，幂等）
=========================================================================
用法：
  python scripts/p7_5e369_carrier_necessity_landing.py probe
  python scripts/p7_5e369_carrier_necessity_landing.py apply
  python scripts/p7_5e369_carrier_necessity_landing.py verify

落盘四处：
  RESEARCH_STATE.md                                 新增 360
  paper/paper48_topological_forbidden_frequency.md  新增 286bw
  roadmap/phase102_baryon_lepton_parameter_free.md  新增 P7-5e-369
  E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md  新增 八十四
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
    "> **360（本轮，G3-P2-4：载体必要性判别——交换载体无模流、层对角模流恒等、"
    "外步与内流互斥，2026-11-02）**：接 359。P2 载体缺口（RecObj 忠实正规态/模算子/"
    "状态空间未定义）本轮不做补位，而给出**载体必要条件**（精确符号，无浮点）："
    "①中心单位共轭平凡（`conj_eq_of_commute`）：与 a 交换的 u 满足 `u a u⁻¹=a`；"
    "②块标量（层内迹态 / 层对角模 Hamilton 量）实现必恒等（`blockScalarRealization_trivial`）"
    "⇒ **层权 e^{−2πn} 单独不产生模流**（层权不同也不行，C10）；块内非标量才给出非平凡共轭（C09）；"
    "③交换载体上**外 ⟺ 非恒等**（`isOuter_iff_ne_refl`），但任何内流恒等于单位流"
    "（`innerFlow_all_refl_of_commutative`）⇒ 交换载体不能同时承载非平凡模流与非平凡外步"
    "——**载体必须非交换**（C05–C06）；④内流切片非外（`innerFlow_slice_not_outer` / "
    "`outer_slice_not_innerFlow`）：Tomita 侧模流切片由 `Δ_mod^{it} ∈ A^×` 实现，故内；"
    "因此**外步 σ_s 不可能是任何忠实正规态的模流时刻**——P1（外性/单向）与 P2（KMS 时间）"
    "是**两条独立腿**（368「外性单独 ⇏ 无周期」的载体版）。最小非交换两层块模型：块交换外"
    "（353/354），但块标量流恒等（`swapBlock_not_blockScalar`）。**资产**：新 Lean 模块 "
    "`G3CarrierNecessity.lean`（16 条定理/定义，`lake env lean` rc=0 零输出零告警）；"
    "判据 `scripts/p7_5e369_carrier_necessity_criteria.py` C01–C16 **16/16 ALL_PASS**；"
    "并更正 `G3KMSBetaToModular.lean` 的「模指数」遗留称谓（数值结论不变）。**诚实边界**："
    "Tomita 事实「`Δ_mod^{it} ∈ A^×`」未形式化（只编码其代数替身 `InnerFlow`）；忠实正规态"
    "存在性/唯一性与 vN 完成性未定义 ⇒ **P2 未成立、G3 未闭合**；不关闭任何项"
    "（226 挂起、k(2) 开放）；G3 继续挂起。"
)

A_P48 = ("诚实边界：参数周期归一为解释性输入；载体/vN 完成性缺失 ⇒ P2 未成立、G3 未闭合；"
         "不关闭任何项（226 挂起、k(2) 开放）。")

SEG_P48 = (
    "286bw（2026-11-02，**G3-P2-4 载体必要性判别**）：接 286bv。①中心单位共轭平凡；"
    "②块标量（层内迹态/层对角模 Hamilton）实现恒等 ⇒ 层权 e^{−2πn} 单独不产生模流；"
    "块内非标量才产生非平凡共轭；③交换载体「外 ⟺ 非恒等」但内流恒等于单位流 ⇒ 交换载体"
    "不能同时承载非平凡模流与非平凡外步（载体必须非交换）；④模流切片内实现 ⟹ 外步不是"
    "任何忠实正规态的模流时刻 ⇒ P1（外/单向）与 P2（KMS 时间）是两条独立腿。资产："
    "`G3CarrierNecessity.lean`（16 条，rc=0 零告警）；判据 C01–C16 16/16 ALL_PASS；"
    "KMS 模块「模指数」遗留称谓已更正。诚实边界：Tomita `Δ_mod^{it} ∈ A^×` 未形式化；"
    "忠实正规态/vN 完成性缺失 ⇒ P2 未成立、G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）。"
)

A_ROAD = ("缺口：参数周期归一为解释性输入；载体（RecObj 忠实正规态/模算子/状态空间）与 vN "
          "完成性仍未定义 ⇒ P2 未成立、G3 未闭合。不关闭任何项（226 挂起、k(2) 开放）。")

SEG_ROAD = (
    "P7-5e-369（G3-P2-4：载体必要性判别——交换载体无模流/层对角模流恒等/外步≠模流，"
    "2026-11-02）：接 368。**结论**：①中心单位共轭平凡；②块标量（层内迹态/层对角模 "
    "Hamilton）实现恒等 ⇒ 层权 e^{−2πn} 单独不构成时间推进；块内非标量才有非平凡模流；"
    "③交换载体「外 ⟺ 非恒等」但内流恒等于单位流 ⇒ 载体必须非交换；④模流切片内实现 ⇒ "
    "外步 σ_s 不可能是任何忠实正规态的模流时刻 ⇒ P1（外/单向）与 P2（KMS 时间）两条独立腿。"
    "最小非交换块模型：块交换外但块标量流恒等。资产：`G3CarrierNecessity.lean` 16 条"
    "（rc=0 零告警）；判据 `p7_5e369_carrier_necessity_criteria.py` C01–C16 16/16；"
    "KMS 模块「模指数」称谓更正。缺口：Tomita `Δ_mod^{it} ∈ A^×` 未形式化；忠实正规态/"
    "vN 完成性未定义 ⇒ P2 未成立、G3 未闭合。不关闭任何项（226 挂起、k(2) 开放）。"
)

A_DIG = ("**诚实边界**：载体（RecObj 忠实正规态/模算子/状态空间）未定义、vN 完成性未证 ⇒ "
         "P2 未成立、G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）。")

SEG_DIG = (
    "## 八十四、G3-P2-4 载体必要性判别：交换载体无模流、层对角模流恒等、外步 ≠ 模流（2026-11-02）\n\n"
    "**口径**：接 359。P2 的载体缺口（RecObj 忠实正规态/模算子/状态空间未定义）本轮不做补位，"
    "只机检**载体必要条件**（精确符号，无浮点；C01–C16 16/16 ALL_PASS）。\n\n"
    "1. **中心单位共轭平凡**：与 a 交换的单位 u 满足 `u a u⁻¹ = a`。因此块标量实现"
    "（层内迹态 / 层对角模 Hamilton 量）必恒等——**层权 `e^{−2πn}` 单独不产生模流**；"
    "即使层权不同也不产生（C10）。块内**非标量**才给出非平凡共轭（C09）。\n"
    "2. **交换载体判别**：交换代数上「外 ⟺ 非恒等」；但任何内流（每时刻内实现）必恒等于"
    "单位流。故交换载体**不能同时**承载非平凡模流与非平凡外步——**载体必须非交换**。\n"
    "3. **内流与外步互斥**：Tomita 侧模流切片由 `Δ_mod^{it} ∈ A^×` 实现，故每个切片都是"
    "内自同构；于是**外步 `σ_s` 不可能是任何忠实正规态的模流时刻**。P1（外性/单向）与 "
    "P2（KMS 时间）是**两条独立腿**，不是同一条——这正是 359「外性单独 ⇏ 无周期」的载体版。\n"
    "4. **最小非交换模型**：两层块 `M₂(ℚ)×M₂(ℚ)` 的块交换是外（353/354），但块标量流恒等；"
    "该模型能承载外步，不能承载层对角时间。\n\n"
    "**资产**：`G3CarrierNecessity.lean`（16 条定理/定义，`lake env lean` rc=0 零输出零告警）；"
    "`scripts/p7_5e369_carrier_necessity_criteria.py` C01–C16 16/16 ALL_PASS；同时更正 "
    "`G3KMSBetaToModular.lean` 的「模指数」遗留称谓（数值结论不变）。\n\n"
    "**诚实边界**：Tomita 事实「`Δ_mod^{it} ∈ A^×`」未形式化（本模块只编码代数替身 "
    "`InnerFlow`）；忠实正规态的存在性/唯一性与 vN 完成性（σ-弱闭、因子性）未定义 ⇒ "
    "P2 未成立、G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）。"
)

ITEMS = [
    ("RS", P_RS, A_RS, SEG_RS, "360（本轮，G3-P2-4"),
    ("P48", P_P48, A_P48, SEG_P48, "286bw（2026-11-02"),
    ("ROAD", P_ROAD, A_ROAD, SEG_ROAD, "P7-5e-369（G3-P2-4"),
    ("DIG", P_DIG, A_DIG, SEG_DIG, "## 八十四、"),
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
