# -*- coding: utf-8 -*-
"""
P7-5e-377 / G3-P2-9 载体类型判据的谱刚性 —— 四处落盘（probe / apply / verify，幂等）
===========================================================================
用法：
  python scripts/p7_5e377_carrier_type_spectral_landing.py probe [apply|verify]

落盘四处：
  RESEARCH_STATE.md                                 新增 368
  paper/paper48_topological_forbidden_frequency.md  新增 286ce
  roadmap/phase102_baryon_lepton_parameter_free.md  新增 P7-5e-377
  E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md   新增 九十二
"""

import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P_RS = os.path.join(ROOT, "RESEARCH_STATE.md")
P_P48 = os.path.join(ROOT, "paper", "paper48_topological_forbidden_frequency.md")
P_ROAD = os.path.join(ROOT, "roadmap", "phase102_baryon_lepton_parameter_free.md")
P_DIG = r"E:\workspace\hyper-resolution\P7-5e_最新研究成果_2026-10-30.md"

A_RS = ("`local_not_imply_global` 是谓词层反例，不是代数层外自同构构造；载体/vN 完成性未定义 ⇒ "
        "**P2 未成立、G3 未闭合**；不关闭任何项（226 挂起、k(2) 开放）。")

SEG_RS = (
    "> **368（本轮，G3-P2-9：载体类型判据的谱刚性——流只依赖模谱比、类型不由代数单独决定，"
    "2026-11-03）**：接 367（论证上接 363/364）。372 已给载体类型判据的有限型 I 半边，373 给了 "
    "vN 接口；本轮回答判据**依赖态的什么数据**：①对角共轭逐元公式（`diagConj_entry`）："
    "`diag(d₁,d₂)` 把 `aᵢⱼ` 乘上 `dᵢ/dⱼ` ⇒ 流只看见模谱比；②谱比相同 ⟹ 同一块对角流"
    "（`diagConj_eq_of_ratio`/`blockStateAut_eq_of_ratio`/`stateFlow_eq_of_ratio`），与权重的绝对"
    "大小无关；③规范化见证：`(2,1)` 与 `(6,3)` 给出同一流（`stateFlow_scale_invariant`）；"
    "④时间的谱判据：态流恒等 ⟺ 两块谱比皆为 1（`stateFlow_trivial_iff_ratio_one`），即时间存在 "
    "⟺ 某块谱比 ≠ 1；⑤**类型不由代数单独决定**（`carrierType_not_algebra_only`）：同一 "
    "`TwoBlockAlg` 上，忠实态流单位可实现（`stateFlow_unitRealizable`），块交换常数流不是"
    "（`swapFlow_not_unitRealizable`），且两条见证流都非平凡"
    "（`exists_nontrivial_unitRealizable_flow`/`exists_nontrivial_not_unitRealizable_flow`）；"
    "⑥主定理 `carrierType_spectral_criterion` 六支合取。**结论**：P2 的载体类型判据是**谱的**"
    "（只依赖 `d₁/d₂`）且**相对态/流而言**，不是代数单独决定的；这仍不是经典因子类型分类。"
    "**资产**：新 Lean 模块 `G3P2CarrierTypeSpectral.lean`（13 条：1 定义 + 12 定理，rc=0 零输出"
    "零告警；复用 372/373 构件不重复定义）；判据 "
    "`scripts/p7_5e377_carrier_type_spectral_criteria.py` C01–C14 **14/14 ALL_PASS**（纯整数/有理，"
    "无浮点；含无 axiom/sorry/native_decide 机检）。**诚实边界**：仅 `M₂(ℚ)×M₂(ℚ)` 乘积块模型；"
    "谱比只对对角忠实态成立（非对角密度矩阵谱分解未形式化）；「类型不由代数单独决定」只是同一"
    "有限块代数上的两个流见证，不声称一般 vN 代数；`UnitRealizable` 仍为操作性代数替身"
    "（经典 I/II/III 与 Tomita `Δ_mod^{it} ∈ A^×` 未形式化）；载体（RecObj 忠实正规态空间/模算子/"
    "状态空间）仍未定义、vN 完成性未证 ⇒ **P2 未成立、G3 未闭合**；不关闭任何项（226 挂起、"
    "k(2) 开放）。"
)

A_P48 = ("判据 C01–C14 14/14 ALL_PASS。诚实边界：局部化只削弱假设；`LayerStep` 方向性仍未从 "
         "Δ_mod/KMS 导出；谓词层反例≠代数层外自同构构造；载体/vN 完成性缺失 ⇒ P2 未成立、"
         "G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）。")

SEG_P48 = (
    "286ce（2026-11-03，**G3-P2-9 载体类型判据的谱刚性**）：接 286cd（论证上接 286bz/286ca）。"
    "372/373 后仍有「判据依赖态的什么数据」的问题。本轮：①对角共轭逐元公式 `diagConj_entry`："
    "`diag(d₁,d₂)` 把 `aᵢⱼ` 乘上 `dᵢ/dⱼ`；②谱比相同 ⟹ 同一流"
    "（`diagConj_eq_of_ratio`/`blockStateAut_eq_of_ratio`/`stateFlow_eq_of_ratio`）；③规范化不变 "
    "`(2,1)≡(6,3)`（`stateFlow_scale_invariant`）；④态流恒等 ⟺ 两块谱比皆为 1"
    "（`stateFlow_trivial_iff_ratio_one`）；⑤同一载体两类型：忠实态流单位可实现"
    "（`stateFlow_unitRealizable`），块交换常数流不是（`swapFlow_not_unitRealizable`），两条见证"
    "流都非平凡；⑥`carrierType_not_algebra_only` 与主定理 `carrierType_spectral_criterion` 六支。"
    "结论：载体类型判据是谱的且相对态/流而言，不由代数单独决定；仍非经典因子分类。资产："
    "`G3P2CarrierTypeSpectral.lean` 13 条（rc=0 零告警）；判据 C01–C14 14/14 ALL_PASS。"
    "诚实边界：仅乘积块模型；谱比只对角忠实态；「不由代数单独决定」只是同代数的两个见证；"
    "`UnitRealizable` 为操作性替身；载体/vN 完成性缺失 ⇒ P2 未成立、G3 未闭合；不关闭任何项"
    "（226 挂起、k(2) 开放）。"
)

A_ROAD = ("谓词层反例≠代数层构造；载体/vN 完成性未定义 ⇒ P2 未成立、G3 未闭合。"
          "不关闭任何项（226 挂起、k(2) 开放）。")

SEG_ROAD = (
    "P7-5e-377（G3-P2-9：载体类型判据的谱刚性——流只依赖模谱比、类型不由代数单独决定，"
    "2026-11-03）：接 376（论证上接 372/373）。①对角共轭逐元公式（`diagConj_entry`）："
    "`diag(d₁,d₂)` 把 `aᵢⱼ` 乘上 `dᵢ/dⱼ`；②谱比相同 ⟹ 同一流（`diagConj_eq_of_ratio`/"
    "`blockStateAut_eq_of_ratio`/`stateFlow_eq_of_ratio`）；③规范化不变（`stateFlow_scale_invariant`）；"
    "④态流恒等 ⟺ 两块谱比皆为 1（`stateFlow_trivial_iff_ratio_one`）；⑤同一 `TwoBlockAlg` 上"
    "单位可实现流（`stateFlow_unitRealizable`）与非单位可实现流（`swapFlow_not_unitRealizable`）"
    "并存且都非平凡 ⇒ `carrierType_not_algebra_only`；⑥主定理 `carrierType_spectral_criterion` "
    "六支合取。资产：`G3P2CarrierTypeSpectral.lean` 13 条（rc=0 零告警）；判据 "
    "`p7_5e377_carrier_type_spectral_criteria.py` C01–C14 14/14。缺口：仅乘积块模型；谱比只对角"
    "忠实态（非对角谱分解未形式化）；「类型不由代数单独决定」只是同代数两见证，不声称一般 vN；"
    "`UnitRealizable` 为操作性替身（经典因子分类与 Tomita `Δ_mod^{it} ∈ A^×` 未形式化）；"
    "载体/vN 完成性未定义 ⇒ P2 未成立、G3 未闭合。不关闭任何项（226 挂起、k(2) 开放）。"
)

A_DIG = "## 九十一、G3-P1b-3 逆向链局部化"

SEG_DIG = (
    "## 九十二、G3-P2-9 载体类型判据的谱刚性：流只依赖模谱比、类型不由代数单独决定（2026-11-03）\n\n"
    "**口径**：接 368（论证上接 363/364）。372/373 之后回答「判据依赖态的什么数据」。\n\n"
    "1. **逐元公式**：`diag(d₁,d₂)` 共轭把 `aᵢⱼ` 乘上 `dᵢ/dⱼ`——流只看见模谱比。\n"
    "2. **谱比决定流**：两块谱比相同 ⟹ 同一流，与权重绝对值无关（`stateFlow_eq_of_ratio`）。\n"
    "3. **规范化不变**：`(2,1)` 与 `(6,3)` 给出同一流（`stateFlow_scale_invariant`）。\n"
    "4. **时间谱判据**：态流恒等 ⟺ 两块谱比皆为 1（`stateFlow_trivial_iff_ratio_one`）。\n"
    "5. **类型不由代数单独决定**：同一 `TwoBlockAlg` 上，忠实态流单位可实现、块交换常数流不是，"
    "两条见证都非平凡（`carrierType_not_algebra_only`）。\n"
    "6. **主定理**：`carrierType_spectral_criterion` 六支合取。\n\n"
    "**资产**：`G3P2CarrierTypeSpectral.lean`（13 条，rc=0 零告警）；"
    "`p7_5e377_carrier_type_spectral_criteria.py` C01–C14 14/14 ALL_PASS。\n\n"
    "**诚实边界**：仅 `M₂(ℚ)×M₂(ℚ)` 乘积块模型；谱比只对角忠实态成立；「不由代数单独决定」只是"
    "同一有限块代数上的两个流见证；`UnitRealizable` 仍为操作性代数替身（经典 I/II/III 与 "
    "Tomita `Δ_mod^{it} ∈ A^×` 未形式化）；载体/vN 完成性未定义 ⇒ P2 未成立、G3 未闭合；"
    "不关闭任何项（226 挂起、k(2) 开放）。"
)

ITEMS = [
    ("RS", P_RS, A_RS, SEG_RS, "368（本轮，G3-P2-9", "after"),
    ("P48", P_P48, A_P48, SEG_P48, "286ce（2026-11-03", "after"),
    ("ROAD", P_ROAD, A_ROAD, SEG_ROAD, "P7-5e-377（G3-P2-9", "after"),
    ("DIG", P_DIG, A_DIG, SEG_DIG, "## 九十二、", "before"),
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
        nl = "CRLF" if nl_of(raw) == "\r\n" else "LF"
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
