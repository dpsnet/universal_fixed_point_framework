# -*- coding: utf-8 -*-
"""
P7-5e-376 / G3-P1b-3 逆向链局部化 —— 四处落盘（probe / apply / verify，幂等）
===========================================================================
用法：
  python scripts/p7_5e376_local_diagonal_landing.py probe [apply|verify]

落盘四处：
  RESEARCH_STATE.md                                 新增 367
  paper/paper48_topological_forbidden_frequency.md  新增 286cd
  roadmap/phase102_baryon_lepton_parameter_free.md  新增 P7-5e-376
  E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md   新增 九十一
"""

import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P_RS = os.path.join(ROOT, "RESEARCH_STATE.md")
P_P48 = os.path.join(ROOT, "paper", "paper48_topological_forbidden_frequency.md")
P_ROAD = os.path.join(ROOT, "roadmap", "phase102_baryon_lepton_parameter_free.md")
P_DIG = r"E:\workspace\hyper-resolution\P7-5e_最新研究成果_2026-10-30.md"

A_RS = "层步弱性与外性不可去已机检；不关闭任何项（226 挂起、k(2) 开放）。"

SEG_RS = (
    "> **367（本轮，G3-P1b-3 逆向链局部化：hdiag_inner 由全局降为单点，结论不变，2026-11-03）**："
    "接 366/374。368 的 `outer_not_diagonal`/`outer_moves_modular_weight` 与 374 的 "
    "`layerStep_outer_ascent`/`directional_converse` 都依赖**全局**假设 "
    "`hdiag_inner : ∀τ, (∀a, L(τa)=L a) → InnerRealization τ`。本轮把该假设**局部化**：只对"
    "给定 σ 要求 `LayerDiagonal L σ → InnerRealization σ`（`LocalInnerOn`），配合 "
    "`hout : IsOuterAut σ`（`:= ¬InnerRealization`，368 定义）证出**同样的**严格升层"
    "（`local_layerStep_outer_ascent`）、模权改变（`local_layerStep_outer_weight_moves`）与"
    "非恒等（`local_directional_converse` 三支打包）。配套：①`LayerDiagonal` 与「不存在移动点」"
    "等价（`layerDiagonal_iff_no_move`）、与 374 `LayerStep L σ 0` 等价"
    "（`layerDiagonal_iff_layerStep_zero`）；②局部假设非空壳：恒等由单位 1 内实现"
    "（`localInnerOn_refl`）；③`global_implies_local`：全局是局部的特例（单向，不声称逆命题）；"
    "④`local_not_imply_global`：局部**严格弱于**全局——谓词层反例（D true=False、D false=True、"
    "I≡False）复现，说明局部化有真实内容。资产：新 Lean 模块 `G3P1b3LocalDiagonal.lean`"
    "（12 条：2 定义 + 10 定理，rc=0 零输出零告警；复用 368/374 构件不重复定义）；判据 "
    "`scripts/p7_5e376_local_diagonal_criteria.py` C01–C14 **14/14 ALL_PASS**（纯整数/布尔枚举，"
    "无浮点；含无 axiom/sorry/native_decide 机检）。**诚实边界**：局部化只削弱假设、不新增物理"
    "断言；`LocalInnerOn`/`IsOuterAut`/`LayerStep` 仍为显式前提，方向性未从 `Δ_mod`/KMS 导出；"
    "`local_not_imply_global` 是谓词层反例，不是代数层外自同构构造；载体/vN 完成性未定义 ⇒ "
    "**P2 未成立、G3 未闭合**；不关闭任何项（226 挂起、k(2) 开放）。"
)

A_P48 = ("诚实边界：`LayerStep`/`LayerAdvance` 为显式输入、未从 Δ_mod/KMS 导出；无有限阶只对"
         "给定 L 成立（模流仍周期）；载体/vN 完成性缺失 ⇒ P2 未成立、G3 未闭合；不关闭任何项"
         "（226 挂起、k(2) 开放）。")

SEG_P48 = (
    "286cd（2026-11-03，**G3-P1b-3 逆向链局部化**）：接 286cc。368/374 的逆向结论依赖全局 "
    "`hdiag_inner`（所有层对角自同构皆内实现）；本轮降到**单点假设** `LocalInnerOn L σ`"
    "（仅对给定 σ：层对角 ⟹ 内实现），配合外性 `IsOuterAut σ` 证出同样的严格升层、模权改变与"
    "非恒等（`local_directional_converse`）。配套：`LayerDiagonal` 等价形式"
    "（`layerDiagonal_iff_no_move` / `layerDiagonal_iff_layerStep_zero`）；局部假设非空壳"
    "（恒等内实现，`localInnerOn_refl`）；`global_implies_local`（单向）；"
    "`local_not_imply_global`（局部严格弱于全局，谓词层反例）。资产："
    "`G3P1b3LocalDiagonal.lean` 12 条（rc=0 零告警）；判据 C01–C14 14/14 ALL_PASS。"
    "诚实边界：局部化只削弱假设；`LayerStep` 方向性仍未从 Δ_mod/KMS 导出；谓词层反例≠代数层"
    "外自同构构造；载体/vN 完成性缺失 ⇒ P2 未成立、G3 未闭合；不关闭任何项（226 挂起、"
    "k(2) 开放）。"
)

A_ROAD = ("缺口：层步/强制前进为显式输入（未从 Δ_mod/KMS 导出）；无有限阶只对给定 L 成立"
          "（模流仍周期 σ_{t+1}=σ_t）；载体/vN 完成性未定义 ⇒ P2 未成立、G3 未闭合。"
          "不关闭任何项（226 挂起、k(2) 开放）。")

SEG_ROAD = (
    "P7-5e-376（G3-P1b-3：逆向链局部化——hdiag_inner 由全局降为单点，结论不变，2026-11-03）："
    "接 375。368/374 的逆向结论依赖全局 `hdiag_inner`；本轮只对给定 σ 假设 "
    "`LayerDiagonal L σ → InnerRealization σ`（`LocalInnerOn`），配合 `hout : IsOuterAut σ` "
    "证出同样的严格升层（`local_layerStep_outer_ascent`）、模权改变"
    "（`local_layerStep_outer_weight_moves`）与非恒等（`local_directional_converse`）。配套："
    "`LayerDiagonal` 等价形式；`localInnerOn_refl`（恒等内实现，非空壳）；"
    "`global_implies_local`（全局 ⟹ 局部，单向）；`local_not_imply_global`（局部严格弱于全局，"
    "谓词层反例）。资产：`G3P1b3LocalDiagonal.lean` 12 条（rc=0 零告警）；判据 "
    "`p7_5e376_local_diagonal_criteria.py` C01–C14 14/14。缺口：局部化只削弱假设；方向性仍未从 "
    "Δ_mod/KMS 导出；谓词层反例≠代数层构造；载体/vN 完成性未定义 ⇒ P2 未成立、G3 未闭合。"
    "不关闭任何项（226 挂起、k(2) 开放）。"
)

A_DIG = "## 九十、G3-P1b-3 层步输入强度校准：非空性 ∧ 外性不可去 ∧ 定向 ⟹ 无有限阶（2026-11-03）"

SEG_DIG = (
    "## 九十一、G3-P1b-3 逆向链局部化：hdiag_inner 由全局降为单点，结论不变（2026-11-03）\n\n"
    "**口径**：接 367（374 的逆向依赖全局 `hdiag_inner`）。本轮只削弱假设，不新增物理断言。\n\n"
    "1. **局部化**：只对给定 σ 假设「层对角 ⟹ 内实现」（`LocalInnerOn`），配合外性仍得严格升层。\n"
    "2. **模权**：k≠0、gap≠0 ⟹ 存在元素模权改变（`local_layerStep_outer_weight_moves`）。\n"
    "3. **打包**：`local_directional_converse` 三支（升层 ∧ 模权改变 ∧ 非恒等）。\n"
    "4. **非空壳**：恒等由单位 1 内实现（`localInnerOn_refl`）。\n"
    "5. **单向桥**：`global_implies_local`（不声称逆命题）。\n"
    "6. **严格弱化**：`local_not_imply_global` 谓词层反例。\n\n"
    "**资产**：`G3P1b3LocalDiagonal.lean`（12 条，rc=0 零告警）；"
    "`p7_5e376_local_diagonal_criteria.py` C01–C14 14/14 ALL_PASS。\n\n"
    "**诚实边界**：局部化只削弱假设；方向性未从 Δ_mod/KMS 导出；谓词层反例≠代数层构造；"
    "载体/vN 完成性未定义 ⇒ P2 未成立、G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）。"
)

ITEMS = [
    ("RS", P_RS, A_RS, SEG_RS, "367（本轮，G3-P1b-3", "after"),
    ("P48", P_P48, A_P48, SEG_P48, "286cd（2026-11-03", "after"),
    ("ROAD", P_ROAD, A_ROAD, SEG_ROAD, "P7-5e-376（G3-P1b-3", "after"),
    ("DIG", P_DIG, A_DIG, SEG_DIG, "## 九十一、", "before"),
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
