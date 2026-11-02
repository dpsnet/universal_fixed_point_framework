# -*- coding: utf-8 -*-
"""
P7-5e-368 / G3-P1b-3 真逆向 —— 四处落盘（probe / apply / verify，幂等）
=====================================================================
用法：
  python scripts/p7_5e368_m_modular_hamiltonian_landing.py probe
  python scripts/p7_5e368_m_modular_hamiltonian_landing.py apply
  python scripts/p7_5e368_m_modular_hamiltonian_landing.py verify

落盘四处：
  RESEARCH_STATE.md                          新增 359
  paper/paper48_topological_forbidden_frequency.md   新增 286bv
  roadmap/phase102_baryon_lepton_parameter_free.md  新增 P7-5e-368
  E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md  新增 八十三

另对纪要「八十二」的记号表做一处原位更正（M：模指数 → 模哈密顿量）。
"""

import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P_RS = os.path.join(ROOT, "RESEARCH_STATE.md")
P_P48 = os.path.join(ROOT, "paper", "paper48_topological_forbidden_frequency.md")
P_ROAD = os.path.join(ROOT, "roadmap", "phase102_baryon_lepton_parameter_free.md")
P_DIG = r"E:\workspace\hyper-resolution\P7-5e_最新研究成果_2026-10-30.md"

A_RS = ("**诚实边界**：归一化前提「模流参数周期取 1」仍是解释性输入（非范畴导出）；"
        "载体（RecObj 忠实正规态/模算子/状态空间）未定义，vN 完成性未证 ⇒ "
        "**P2 未成立、G3 未闭合**；不关闭任何项（226 仍挂起、k(2) 仍开放）。")

SEG_RS = (
    "> **359（本轮，G3-P1b-3 真逆向：M=模哈密顿量；外 ⟹ 模权不可内吸收，无周期需单向独立输入，"
    "2026-11-02）**：接 358。**记号更正（用户指出）**：M 是 **模哈密顿量**（自伴算子，"
    "Tomita–Takesaki），`Δ_mod=e^{−2πM}`、`σ_t=Ad Δ_mod^{it}=Ad e^{−2πitM}`；「M=1」的正确读法是"
    "**谱间隔归一为 1**（`spec M=ℤ`，相邻层间隔 1），不是把标量赋 1。358 的「模指数」称谓作废"
    "（数值结论不变：`Δ_mod=e^{−2π}`、层权比 e^{−2π}、K 每层 2π）。**P1b-3 真逆向结论"
    "（精确符号，无浮点）**：①层权 `w_n=e^{−2π·gap·n}`，gap≠0 ⟹ 层权单射（C01–C04）；"
    "gap=0 ⟹ 全层坍缩（C05）；gap=1 ⟹ e^{−2π}（C06）；②保全部层权的层置换必恒等（刚性，C09），"
    "故非恒等置换必移动模权；③若层对角自同构皆内实现，则**外 ⟹ 非层对角 ⟹ ∃a: "
    "w(L(σa))≠w(L(a))**（模权不可内吸收）；④叠加**单向层作用**（每步 +k 层，k≠0）⟹ "
    "m≠0 步回不到原层（C07–C08）。**反例锐化（诚实边界）**：非平凡置换可有限阶"
    "（`bnotEquiv` 二阶；三阶循环 C10）⇒ **外性/权重移动单独 ⇏ 无周期**，单向性是独立结构输入"
    "（与 P1a `StrictLayer` 同源）；且**模流本身周期**（单位谱 `σ_{t+1}=σ_t`），故「无周期」"
    "只能是**递归层深的单向性**，不是 t 上无周期（342 的深度/相位互补再次成立）。**资产**："
    "新 Lean 模块 `G3P1b3ConverseModular.lean`（14 条定理/定义，`lake env lean` rc=0 零输出零告警）；"
    "判据 `scripts/p7_5e368_m_modular_hamiltonian_criteria.py` C01–C16 **16/16 ALL_PASS**。"
    "**诚实边界**：载体（RecObj 忠实正规态/模算子/状态空间）未定义、vN 完成性未证 ⇒ "
    "**P2 未成立、G3 未闭合**；不关闭任何项（226 挂起、k(2) 开放）。"
)

A_P48 = ("诚实边界：参数周期归一为解释性输入；载体/vN 完成性缺失 ⇒ P2 未成立、G3 未闭合；"
         "不关闭任何项（226 挂起、k(2) 开放）。")

SEG_P48 = (
    "286bv（2026-11-02，**G3-P1b-3 真逆向 + 记号更正**）：M = 模哈密顿量（自伴算子，"
    "`Δ_mod=e^{−2πM}`，`σ_t=Ad e^{−2πitM}`）；「M=1」读作谱间隔归一 1（`spec M=ℤ`），"
    "不是标量赋值；358 的「模指数」称谓作废，数值结论不变。结论：层权 `w_n=e^{−2π·gap·n}`，"
    "gap≠0 ⟹ 单射；保权置换必恒等（刚性）；若层对角皆内实现，则外 ⟹ 存在元素模权改变"
    "（外性不可被内实现吸收）；叠加单向层作用（+k, k≠0）⟹ 无回退。反例：非平凡置换可有限阶"
    "（二阶/三阶循环）⇒ 外性单独 ⇏ 无周期，单向性须独立输入；模流本身周期（单位谱 "
    "`σ_{t+1}=σ_t`），「无周期」只读作递归层深单向性。资产：`G3P1b3ConverseModular.lean`"
    "（14 条，rc=0 零告警）；判据 C01–C16 16/16 ALL_PASS。诚实边界：载体/vN 完成性缺失 ⇒ "
    "P2 未成立、G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）。"
)

A_ROAD = ("缺口：参数周期归一为解释性输入；载体（RecObj 忠实正规态/模算子/状态空间）与 vN "
          "完成性仍未定义 ⇒ P2 未成立、G3 未闭合。不关闭任何项（226 挂起、k(2) 开放）。")

SEG_ROAD = (
    "P7-5e-368（G3-P1b-3 真逆向：M=模哈密顿量；外 ⟹ 模权不可内吸收；单向须独立输入，"
    "2026-11-02）：接 367。**记号更正**：M 是模哈密顿量（自伴算子），`Δ_mod=e^{−2πM}`、"
    "`σ_t=Ad e^{−2πitM}`；「M=1」= 谱间隔归一 1（spec M=ℤ），非标量赋值；367 的「模指数」"
    "称谓作废，数值结论（e^{−2π}、层权比 e^{−2π}、K 每层 2π）不变。**结论**：①层权 "
    "e^{−2π·gap·n}，gap≠0 ⟹ 单射（gap=0 坍缩）；②保权置换=恒等（刚性）；③层对角皆内实现 ⟹ "
    "外 ⟹ ∃a 模权改变（模权不可内吸收）；④单向步 +k(k≠0) ⟹ m≠0 无回退。**反例**：非平凡置换"
    "可有限阶（二阶/三阶循环）⇒ 外性单独 ⇏ 无周期；模流本身周期（单位谱 σ_{t+1}=σ_t），"
    "无周期只读作递归层深单向。资产：`G3P1b3ConverseModular.lean` 14 条（rc=0 零告警）；"
    "判据 `p7_5e368_m_modular_hamiltonian_criteria.py` C01–C16 16/16。缺口：载体"
    "（RecObj 忠实正规态/模算子/状态空间）与 vN 完成性未定义 ⇒ P2 未成立、G3 未闭合。"
    "不关闭任何项（226 挂起、k(2) 开放）。"
)

A_DIG = ("**诚实边界**：归一化前提「模流参数周期取 1」仍是解释性输入（非范畴导出）；"
         "载体（RecObj 忠实正规态/模算子/状态空间）未定义，vN 完成性未证 ⇒ "
         "**P2 未成立、G3 未闭合**；不关闭任何项（226 挂起、k(2) 开放）。")

SEG_DIG = (
    "## 八十三、G3-P1b-3 真逆向 + 记号更正：M 是模哈密顿量（2026-11-02）\n\n"
    "**用户更正（本轮回填）**：标准 Tomita–Takesaki 记号中 `Δ_mod = e^{−2πM}`，"
    "**M 是自伴的模哈密顿量**，生成模流 `σ_t = Ad Δ_mod^{it} = Ad e^{−2πitM}`"
    "（`Δ_mod^{it} = e^{−2πitM}`，Stone）。因此 358 的「M = 模指数」称谓作废；"
    "「M=1」正确读作**模哈密顿量在层塔上的相邻谱间隔归一为 1**（`spec M = ℤ`，"
    "`m_{n+1}−m_n = 1`），不是把某个标量赋值为 1。数值结论（`Δ_mod=e^{−2π}`、"
    "层权比 `e^{−2π}`、K 每层 2π）不变。\n\n"
    "**记号（更正后）**\n\n"
    "| 记号 | 语义 | 可否赋值 |\n|---|---|---|\n"
    "| 框架 Δ | `spExchangeLaw` 交换律偏差 | 否 |\n"
    "| Δ_mod | 模算子 `e^{−2πM}` | 否（算子） |\n"
    "| M | **模哈密顿量**（自伴算子；谱间隔可归一） | 否（算子；只归一谱间隔） |\n\n"
    "**P1b-3 真逆向（精确符号，无浮点；C01–C16 16/16 ALL_PASS）**\n"
    "1. 层权 `w_n = e^{−2π·gap·n}`（gap = M 的相邻谱间隔）；gap≠0 ⇒ 层权单射；"
    "gap=0 ⇒ 坍缩为 1（必要条件）；\n"
    "2. 保持全部层权的层置换必为恒等（刚性）；故非恒等层作用必移动模权；\n"
    "3. 若层对角自同构皆为内实现，则外自同构必非层对角 ⇒ ∃a，`w(L(σa)) ≠ w(L(a))`"
    "——**外性不可被内实现吸收**；\n"
    "4. 叠加单向层作用（每步 +k，k≠0）⇒ 任意 m≠0 步不回原层（无回退）。\n\n"
    "**反例与边界（诚实）**：非平凡置换可有限阶（`bnotEquiv` 二阶；三阶循环）⇒ "
    "**外性/权重移动单独 ⇏ 无周期**；单向性是独立结构输入（与 P1a StrictLayer 同源）。"
    "且**模流本身是周期的**（单位谱下 `σ_{t+1}=σ_t`），所以本项的「无周期」只能是"
    "**递归层深的单向性**，不能读作模流在 t 上无周期（342 的深度/相位互补再次成立）。\n\n"
    "**资产**：`G3P1b3ConverseModular.lean`（14 条定理/定义，`lake env lean` rc=0 零输出零告警）；"
    "`scripts/p7_5e368_m_modular_hamiltonian_criteria.py` C01–C16 16/16 ALL_PASS。\n\n"
    "**诚实边界**：载体（RecObj 忠实正规态/模算子/状态空间）未定义、vN 完成性未证 ⇒ "
    "P2 未成立、G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）。"
)

OLD_ROW = ("| **M** | 模指数（`Δ_mod = e^{−2πM}`；模流参数周期 = 1/M） | S97 | 由归一固定 |")
NEW_ROW = ("| **M** | **模哈密顿量**（自伴算子；`Δ_mod = e^{−2πM}`；2026-11-02 用户更正，"
           "原称「模指数」作废） | S97 / 用户 | 否（算子；只归一谱间隔） |")

ITEMS = [
    ("RS", P_RS, A_RS, SEG_RS, "359（本轮，G3-P1b-3"),
    ("P48", P_P48, A_P48, SEG_P48, "286bv（2026-11-02"),
    ("ROAD", P_ROAD, A_ROAD, SEG_ROAD, "P7-5e-368（G3-P1b-3"),
    ("DIG", P_DIG, A_DIG, SEG_DIG, "## 八十三、"),
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
        print(f"[{name}] anchor_count={ca} marker_count={cm} newline={'CRLF' if nl_of(raw) == chr(13)+chr(10) else 'LF'}")
        if ca != 1 or cm > 1:
            ok = False
    raw = read_raw(P_DIG)
    print(f"[DIG-TABLE] old_row={raw.count(OLD_ROW)} new_row={raw.count(NEW_ROW)}")
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
    raw = read_raw(P_DIG)
    if OLD_ROW in raw:
        new = raw.replace(OLD_ROW, NEW_ROW, 1)
        with io.open(P_DIG, "w", encoding="utf-8", newline="") as fh:
            fh.write(new)
        print("[DIG-TABLE] corrected in place")
    elif NEW_ROW in raw:
        print("[DIG-TABLE] already corrected, skip")
    else:
        print("[DIG-TABLE] WARN: neither old nor new row found")
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
    raw = read_raw(P_DIG)
    print(f"[DIG-TABLE] old={raw.count(OLD_ROW)} new={raw.count(NEW_ROW)}")
    if raw.count(NEW_ROW) != 1:
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
