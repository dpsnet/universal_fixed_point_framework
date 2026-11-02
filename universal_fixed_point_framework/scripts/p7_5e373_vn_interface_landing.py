# -*- coding: utf-8 -*-
"""
P7-5e-373 / G3-P2-8 载体类型接口骨架 —— 四处落盘（probe / apply / verify，幂等）
===========================================================================
用法：
  python scripts/p7_5e373_vn_interface_landing.py probe
  python scripts/p7_5e373_vn_interface_landing.py apply
  python scripts/p7_5e373_vn_interface_landing.py verify

落盘四处：
  RESEARCH_STATE.md                                 新增 364
  paper/paper48_topological_forbidden_frequency.md  新增 286ca
  roadmap/phase102_baryon_lepton_parameter_free.md  新增 P7-5e-373
  E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md   新增 八十八
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
    "> **364（本轮，G3-P2-8：载体类型接口骨架——只定义与桥接，不含未证存在性，2026-11-03）**："
    "接 363。372 已机检载体类型判据的有限型 I 半边；本轮搭起通向 vN / III 型的**接口**，"
    "刻意只做定义与桥接：①`ModularDatum`（载体+流，**不含 KMS 条件**）；②`UnitRealizable`"
    "（流可由代数单位路径实现 = Tomita `Δ_mod^{it} ∈ A^×` 的代数替身）；③`TypeIII` 作为"
    "**操作性定义** `¬ UnitRealizable`（**不是**经典因子类型分类）；④`UnitRealizableDatum` 把"
    "「有限型 I ⟹ 单位可实现」写成显式字段（模型输入而非定理）；⑤桥接定理 "
    "`innerFlow_iff_unitRealizable`（逐时刻内实现 ⟺ 存在单位路径，用选择公理）与 "
    "`not_innerFlow_iff_exists_outer`（¬内流 ⟺ 存在外时刻）；⑥主定理 `carrierType_interface`："
    "单位可实现数据必内/非外/非 III、有限型 I 的任一忠实对角态皆非 III、非平凡时间存在、"
    "且块交换常数流构成操作性 III 实例（它不是任何忠实态流，372 已证）。**接口纪律**：模块内"
    "**无 `axiom`、无 `sorry`、无未证存在性断言**；`TypeIII` 仅为操作性谓词。**资产**：新 Lean 模块 "
    "`G3P2VNInterface.lean`（14 条：7 定义 + 7 定理，`lake env lean` rc=0 零输出零告警）；判据 "
    "`scripts/p7_5e373_vn_interface_criteria.py` C01–C14 **14/14 ALL_PASS**（含「无 axiom 声明」"
    "与「代码区无 sorry」机检）。**诚实边界**：`TypeIII` 与 Takesaki 因子类型（I/II/III）的等价"
    "**未证明**；「III 型因子存在外模流」**未形式化**，仅以块交换给出操作性实例；Tomita "
    "`Δ_mod^{it} ∈ A^×` 在 `UnitRealizableDatum` 中是**字段假设**，不是定理；载体（RecObj 忠实"
    "正规态空间/模算子/状态空间）仍未定义、vN 完成性未证 ⇒ **P2 未成立、G3 未闭合**；不关闭任何项"
    "（226 挂起、k(2) 开放），G3 继续挂起。"
)

A_P48 = ("诚实边界：仅有限型 I 乘积块模型；III 型外模流存在性未形式化；Tomita Δ∈A^× 为模型输入；"
         "流为常数切片；载体/vN 完成性缺失 ⇒ P2 未成立、G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）。")

SEG_P48 = (
    "286ca（2026-11-03，**G3-P2-8 载体类型接口骨架**）：接 286bz。只定义不打公设："
    "`ModularDatum`（载体+流，无 KMS 条件）；`UnitRealizable`（单位路径实现 = `Δ_mod^{it} ∈ A^×` "
    "代数替身）；`TypeIII := ¬UnitRealizable`（操作性定义，非经典因子分类）；"
    "`UnitRealizableDatum`（把「有限型 I ⟹ 单位可实现」显式化为字段）。桥接："
    "`innerFlow_iff_unitRealizable`、`not_innerFlow_iff_exists_outer`；主定理 "
    "`carrierType_interface`：单位可实现数据必内/非外/非 III；有限型 I 忠实对角态皆非 III；"
    "非平凡时间存在；块交换常数流为操作性 III 实例且非任何忠实态流。资产："
    "`G3P2VNInterface.lean` 14 条（rc=0 零告警，无 axiom/sorry）；判据 C01–C14 14/14 ALL_PASS。"
    "诚实边界：操作性与经典类型等价未证；III 型外模流存在性未形式化；Tomita Δ∈A^× 为字段假设；"
    "载体/vN 完成性缺失 ⇒ P2 未成立、G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）。"
)

A_ROAD = ("缺口：仅有限型 I 乘积块模型；III 型外模流存在性未形式化；Tomita Δ∈A^× 为模型输入；"
          "流为常数切片族；载体/vN 完成性未定义 ⇒ P2 未成立、G3 未闭合。不关闭任何项（226 挂起、k(2) 开放）。")

SEG_ROAD = (
    "P7-5e-373（G3-P2-8：载体类型接口骨架，2026-11-03）：接 372。**只定义与桥接，不含未证存在性**："
    "①`ModularDatum`（载体+流，无 KMS 条件）；②`UnitRealizable`（`Δ_mod^{it} ∈ A^×` 的代数替身）；"
    "③`TypeIII := ¬UnitRealizable`（操作性定义，与经典因子类型等价未证）；④`UnitRealizableDatum`"
    "（「有限型 I ⟹ 单位可实现」为显式字段）；⑤桥接 `innerFlow_iff_unitRealizable` / "
    "`not_innerFlow_iff_exists_outer`；⑥主定理 `carrierType_interface`：单位可实现数据必内/非外/"
    "非 III，有限型 I 忠实态皆非 III，非平凡时间存在，块交换常数流为操作性 III 实例且非态流。"
    "资产：`G3P2VNInterface.lean` 14 条（rc=0 零告警，无 axiom/sorry）；判据 "
    "`p7_5e373_vn_interface_criteria.py` C01–C14 14/14。缺口：操作性与经典 III 型等价未证；"
    "III 型外模流存在性未形式化；Tomita Δ∈A^× 为字段假设；载体/vN 完成性未定义 ⇒ P2 未成立、"
    "G3 未闭合。不关闭任何项（226 挂起、k(2) 开放）。"
)

A_DIG = "## 八十七、G3-P2-7 载体类型判据：有限型 I 模流必内、外流不可由忠实态生成（2026-11-03）"

SEG_DIG = (
    "## 八十八、G3-P2-8 载体类型接口骨架：只定义与桥接（2026-11-03）\n\n"
    "**口径**：接 363。372 已机检载体类型判据的有限型 I 半边；本轮搭起通向 vN / III 型的接口，"
    "**只定义、只桥接，不宣称证明**（C01–C14 14/14 ALL_PASS，含「无 axiom 声明」与「代码区无 "
    "sorry」机检）。\n\n"
    "1. **`ModularDatum`**：载体 + 流；**不含** KMS 条件，不对流的解析性作任何假设。\n"
    "2. **`UnitRealizable`**：流可由代数单位路径实现——Tomita `Δ_mod^{it} ∈ A^×` 的代数替身。\n"
    "3. **`TypeIII`**：操作性定义 `¬ UnitRealizable`；与 Takesaki 因子类型分类的等价**未证明**。\n"
    "4. **`UnitRealizableDatum`**：把「有限型 I ⟹ 单位可实现」写成**显式字段**（模型输入），"
    "而不是由 KMS 推出的定理。\n"
    "5. **桥接**：`innerFlow_iff_unitRealizable`（逐时刻内 ⟺ 单位路径，选择公理）；"
    "`not_innerFlow_iff_exists_outer`（¬内流 ⟺ 存在外时刻）。\n"
    "6. **主定理 `carrierType_interface`**：单位可实现数据必内/非外/非 III；有限型 I 的任一忠实"
    "对角态皆非 III；非平凡时间存在；块交换常数流构成操作性 III 实例（它不是任何忠实态流）。\n\n"
    "**接口纪律**：模块内无 `axiom`、无 `sorry`、无未证存在性断言；`TypeIII` 仅为操作性谓词。\n\n"
    "**资产**：`G3P2VNInterface.lean`（14 条：7 定义 + 7 定理，`lake env lean` rc=0 零输出零告警）；"
    "`scripts/p7_5e373_vn_interface_criteria.py` C01–C14 14/14 ALL_PASS。\n\n"
    "**诚实边界**：`TypeIII` 与经典因子类型（I/II/III）的等价未证明；「III 型因子存在外模流」"
    "未形式化，仅以块交换给出操作性实例；Tomita `Δ_mod^{it} ∈ A^×` 是**字段假设**；载体（RecObj "
    "忠实正规态空间/模算子）仍未定义、vN 完成性未证 ⇒ P2 未成立、G3 未闭合；不关闭任何项"
    "（226 挂起、k(2) 开放）。"
)

ITEMS = [
    ("RS", P_RS, A_RS, SEG_RS, "364（本轮，G3-P2-8", "after"),
    ("P48", P_P48, A_P48, SEG_P48, "286ca（2026-11-03", "after"),
    ("ROAD", P_ROAD, A_ROAD, SEG_ROAD, "P7-5e-373（G3-P2-8", "after"),
    ("DIG", P_DIG, A_DIG, SEG_DIG, "## 八十八、", "before"),
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
