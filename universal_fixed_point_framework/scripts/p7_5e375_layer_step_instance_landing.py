# -*- coding: utf-8 -*-
"""
P7-5e-375 / G3-P1b-3 层步输入强度校准 —— 四处落盘（probe / apply / verify，幂等）
===========================================================================
用法：
  python scripts/p7_5e375_layer_step_instance_landing.py probe [apply|verify]

落盘四处：
  RESEARCH_STATE.md                                 新增 366
  paper/paper48_topological_forbidden_frequency.md  新增 286cc
  roadmap/phase102_baryon_lepton_parameter_free.md  新增 P7-5e-375
  E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md   新增 九十
"""

import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P_RS = os.path.join(ROOT, "RESEARCH_STATE.md")
P_P48 = os.path.join(ROOT, "paper", "paper48_topological_forbidden_frequency.md")
P_ROAD = os.path.join(ROOT, "roadmap", "phase102_baryon_lepton_parameter_free.md")
P_DIG = r"E:\workspace\hyper-resolution\P7-5e_最新研究成果_2026-10-30.md"

A_RS = ("**方向性是显式输入、未从 Δ_mod/KMS 导出**；不关闭任何项（226 挂起、k(2) 开放），"
        "G3 继续挂起。")

SEG_RS = (
    "> **366（本轮，G3-P1b-3 层步输入强度校准：非空性 ∧ 外性不可去 ∧ 定向 ⟹ 无有限阶，"
    "2026-11-03）**：接 365/374。374 已证「层对角皆内 + 外 + 层步 ⟹ 严格升层」，但未校准 "
    "`LayerStep` 自身的强度。本轮机检：①`LayerStep` **单独很弱**——恒等对**任意** k 都满足"
    "（`layerStep_refl`），故升降结论**必须**由外性/非对角排除左支（`layerStep_nondiag_ascent`）；"
    "②反证：`¬ ∀σ k, LayerStep id σ k → ∃a, σa=a+k`（`not_layerStep_imp_ascent`，σ=id、k=1 "
    "即反例）⟹ **外性不可去**；③非空性：`advance k` 同时是层步与强制前进（`layerStep_advance` / "
    "`layerAdvance_advance`），不是空壳谓词；④强度：`LayerAdvance` 对恒等失败"
    "（`layerAdvance_not_refl`），且**排除有限阶**：k≠0、m≠0 ⟹ `σ^m ≠ refl`"
    "（`layerAdvance_no_power_refl`）；⑤对照 368：二阶置换 `bnotEquiv` **不可能**是非零强制前进"
    "（`bnotEquiv_not_layerAdvance`）——方向与周期互斥；⑥主定理 `input_necessity` 五支打包。"
    "资产：新 Lean 模块 `G3P1b3LayerStepInstance.lean`（9 条定理，rc=0 零输出零告警；复用 "
    "374/368 不重复定义）；判据 `scripts/p7_5e375_layer_step_instance_criteria.py` C01–C14 "
    "**14/14 ALL_PASS**（纯整数枚举，无浮点；含无 axiom/sorry/native_decide 机检）。"
    "**诚实边界**：`LayerStep`/`LayerAdvance` 仍是**显式输入**，「模流生成元非负 ⟹ 每步至多前进 "
    "k 层」**未形式化**；「无有限阶」只对给定层泛函 L 成立（模流本身仍周期，`σ_{t+1}=σ_t`），"
    "只读作层深单向性；载体/vN 完成性未定义 ⇒ **P2 未成立、G3 未闭合**；层步弱性与外性不可去已"
    "机检；不关闭任何项（226 挂起、k(2) 开放）。"
)

A_P48 = ("载体/vN 完成性缺失 ⇒ P2 未成立、G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）；"
         "方向性为显式输入、未从 Δ_mod/KMS 导出。")

SEG_P48 = (
    "286cc（2026-11-03，**G3-P1b-3 层步输入强度校准**）：接 286cb。374 的条件逆向依赖「层步」，"
    "本轮校准其强度：①恒等对任意 k 都是 `LayerStep` ⟹ 层步单独不强制定向（`layerStep_refl`）；"
    "②故升层结论必须由外性/非对角排除左支，且 `¬∀σ k, LayerStep id σ k → ∃a σa=a+k`"
    "（`not_layerStep_imp_ascent`）⟹ 外性不可去；③`advance k` 是层步且是强制前进 ⟹ 非空性；"
    "④`LayerAdvance` 对恒等失败、并排除有限阶（k,m≠0 ⟹ σ^m≠refl）；⑤二阶置换 `bnotEquiv` "
    "不可能是非零强制前进 ⟹ 方向与周期互斥；⑥主定理 `input_necessity`。资产："
    "`G3P1b3LayerStepInstance.lean` 9 条定理（rc=0 零告警）；判据 C01–C14 14/14 ALL_PASS。"
    "诚实边界：`LayerStep`/`LayerAdvance` 为显式输入、未从 Δ_mod/KMS 导出；无有限阶只对给定 L "
    "成立（模流仍周期）；载体/vN 完成性缺失 ⇒ P2 未成立、G3 未闭合；不关闭任何项（226 挂起、"
    "k(2) 开放）。"
)

A_ROAD = ("缺口：方向性为显式输入（未从 Δ_mod/KMS 导出）；「模流生成元非负 ⟹ 每步至多前进 k 层」"
          "未形式化；载体/vN 完成性未定义 ⇒ P2 未成立、G3 未闭合。不关闭任何项（226 挂起、k(2) 开放）。")

SEG_ROAD = (
    "P7-5e-375（G3-P1b-3：层步输入强度校准——非空性 ∧ 外性不可去 ∧ 定向 ⟹ 无有限阶，2026-11-03）："
    "接 374。374 的条件逆向依赖层步；本轮校准：①恒等对任意 k 都是层步 ⟹ 层步不强制定向"
    "（`layerStep_refl`）；②升层必须由外性排除对角支（`layerStep_nondiag_ascent`），且 "
    "`¬∀σ k, LayerStep id σ k → ∃a σa=a+k`（`not_layerStep_imp_ascent`）；③`advance k` 同时是"
    "层步与强制前进（非空性）；④`LayerAdvance` 对恒等失败（`layerAdvance_not_refl`），并排除有限阶"
    "（`layerAdvance_no_power_refl`）；⑤二阶置换 `bnotEquiv` 不是非零强制前进"
    "（`bnotEquiv_not_layerAdvance`）；⑥主定理 `input_necessity`。资产："
    "`G3P1b3LayerStepInstance.lean` 9 条（rc=0 零告警）；判据 "
    "`p7_5e375_layer_step_instance_criteria.py` C01–C14 14/14。缺口：层步/强制前进为显式输入"
    "（未从 Δ_mod/KMS 导出）；无有限阶只对给定 L 成立（模流仍周期 σ_{t+1}=σ_t）；载体/vN 完成性"
    "未定义 ⇒ P2 未成立、G3 未闭合。不关闭任何项（226 挂起、k(2) 开放）。"
)

A_DIG = "## 八十九、G3-P1b-3 真逆向的条件形式：层步定向 ⟹ 严格升层、模权改变、无回退（2026-11-03）"

SEG_DIG = (
    "## 九十、G3-P1b-3 层步输入强度校准：非空性 ∧ 外性不可去 ∧ 定向 ⟹ 无有限阶（2026-11-03）\n\n"
    "**口径**：接 366（374 的条件逆向依赖层步）。本轮只校准输入强度，不新增物理断言。\n\n"
    "1. **弱性**：恒等对任意 k 都是 `LayerStep` ⟹ 层步本身不强制定向。\n"
    "2. **外性不可去**：`¬∀σ k, LayerStep id σ k → ∃a σa=a+k`（σ=id、k=1 反例）。\n"
    "3. **非空性**：`advance k` 是层步且是强制前进。\n"
    "4. **强度**：`LayerAdvance` 对恒等失败，并排除有限阶（k,m≠0 ⟹ σ^m≠refl）。\n"
    "5. **与周期互斥**：二阶 `bnotEquiv` 不是非零强制前进。\n"
    "6. **主定理**：`input_necessity` 五支打包。\n\n"
    "**资产**：`G3P1b3LayerStepInstance.lean`（9 条定理，rc=0 零告警）；"
    "`p7_5e375_layer_step_instance_criteria.py` C01–C14 14/14 ALL_PASS。\n\n"
    "**诚实边界**：层步/强制前进为显式输入，未从 Δ_mod/KMS 导出；无有限阶只对给定 L 成立"
    "（模流仍周期）；载体/vN 完成性未定义 ⇒ P2 未成立、G3 未闭合；不关闭任何项（226 挂起、"
    "k(2) 开放）。"
)

ITEMS = [
    ("RS", P_RS, A_RS, SEG_RS, "366（本轮，G3-P1b-3", "after"),
    ("P48", P_P48, A_P48, SEG_P48, "286cc（2026-11-03", "after"),
    ("ROAD", P_ROAD, A_ROAD, SEG_ROAD, "P7-5e-375（G3-P1b-3", "after"),
    ("DIG", P_DIG, A_DIG, SEG_DIG, "## 九十、", "before"),
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
