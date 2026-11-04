# -*- coding: utf-8 -*-
"""
P7-5e-378 / G3-P2-10 非对角忠实态的单位可实现性 —— 四处落盘（probe / apply / verify，幂等）
===========================================================================
用法：
  python scripts/p7_5e378_faithful_block_state_landing.py probe [apply|verify]

落盘四处：
  RESEARCH_STATE.md                                 新增 369
  paper/paper48_topological_forbidden_frequency.md  新增 286cf
  roadmap/phase102_baryon_lepton_parameter_free.md  新增 P7-5e-378
  E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md   新增 九十三
"""

import io
import os
import re
import sys

from p7_5e378_reorder_entries import digest_blocks, journal_runs, read_lines, write_lines

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P_RS = os.path.join(ROOT, "RESEARCH_STATE.md")
P_P48 = os.path.join(ROOT, "paper", "paper48_topological_forbidden_frequency.md")
P_ROAD = os.path.join(ROOT, "roadmap", "phase102_baryon_lepton_parameter_free.md")
P_DIG = r"E:\workspace\hyper-resolution\P7-5e_最新研究成果_2026-10-30.md"

SEG_RS = (
    "> **369（本轮，G3-P2-10：非对角忠实态的单位可实现性——类型判据拆除对角化限制，"
    "2026-11-04）**：接 368（论证上接 372/373）。368 的「非 III」半边只在**对角忠实态**"
    "（`DiagState`）内成立，非对角密度矩阵的谱分解未形式化。本轮把该限制拆掉：①一般忠实正定"
    "块态（`FaithfulBlockState`）把对称矩阵 `[[a,b],[b,c]]` 的正定性编码为 `0 < a` 与 "
    "`0 < a*c − b²`，由行列式非零直接得到代数单位（`FaithfulBlockState.unit`，经 `Matrix.nonsing_inv` "
    "双侧单位律）——**不需要对角化/谱分解**；②**单位共轭恒等 ⟺ 态为标量**"
    "（`conj_trivial_iff`）：`Ad ρ = id` 当且仅当 `ρ` 是标量矩阵，证明只用与 `E₁₂` 的交换子，"
    "不用特征值；③非标量 ⟹ 存在非平凡共轭（`conj_nontrivial`）；④任一忠实正定块态流单位可实现"
    "（`faithfulFlow_unitRealizable`，常数单位路径）；⑤两块的流恒等 ⟺ 两块都标量"
    "（`faithfulFlow_trivial_iff`/`faithfulFlow_nontrivial`）；⑥**非对角见证**"
    "（`nonDiagonalState` = `[[2,1],[1,1]]`）：忠实正定、`b≠0`、非标量，其流非平凡"
    "（`nonDiagonalFlow_nontrivial`）；⑦主定理 `faithfulBlockState_criterion` 三支合取。"
    "**结论**：载体类型判据的「非 III 半边」不再依赖对角化，可对一般（含非对角）忠实正定块态"
    "陈述；但这仍只是 2×2 块代数上的共轭恒等判据，不是谱分解、不是 KMS 导出。"
    "**资产**：新 Lean 模块 `G3P2FaithfulBlockState.lean`（20 条：1 结构 + 7 定义 + 12 定理；"
    "`lake build` rc=0、1716 jobs、零输出零告警；复用 372/373 构件不重复定义）；判据 "
    "`scripts/p7_5e378_faithful_block_state_criteria.py` C01–C14 **14/14 ALL_PASS**（纯整数/有理，"
    "无浮点；含无 axiom/sorry/native_decide 机检）。**诚实边界**：仅 `M₂(ℚ)×M₂(ℚ)` 乘积块模型；"
    "「忠实正定」只编码为 `0 < a` 与 `0 < a*c − b²`，正规性/σ-弱闭/因子性/一般维数未形式化；"
    "`Ad ρ` 只是模流 `Ad Δ_mod^{it}` 的**代数替身**，`ρ^{it}` 复相位、解析延拓与 KMS 本体未构造；"
    "谱比判据仍只对对角态成立（377），非对角态的模谱刚性未证；可操作性（operationality）判据"
    "未形式化，不声称载体类型可被实验操作判定；经典 I/II/III 分类与 Tomita `Δ_mod^{it} ∈ A^×` "
    "未形式化；载体（RecObj 忠实正规态空间/模算子/状态空间）仍未定义、vN 完成性未证 ⇒ "
    "**P2 未成立、G3 未闭合**；不关闭任何项（226 挂起、k(2) 开放）。"
)

SEG_P48 = (
    "286cf（2026-11-04，**G3-P2-10 非对角忠实态的单位可实现性**）：接 286ce（论证上接 372/373）。"
    "286ce 的「非 III 半边」只在**对角忠实态**内成立。本轮拆除该限制：①`FaithfulBlockState` 把"
    "对称矩阵 `[[a,b],[b,c]]` 的正定性编码为 `0 < a` 与 `0 < a*c − b²`，由行列式非零经 "
    "`Matrix.nonsing_inv` 得到代数单位（`FaithfulBlockState.unit`），**不需谱分解**；②"
    "`conj_trivial_iff`：`Ad ρ = id` ⟺ `ρ` 为标量，只用与 `E₁₂` 的交换子；③`conj_nontrivial` "
    "逆否形式；④`faithfulFlow_unitRealizable`（常数单位路径）；⑤`faithfulFlow_trivial_iff`：两块流"
    "恒等 ⟺ 两块都标量；⑥非对角见证 `nonDiagonalState`=`[[2,1],[1,1]]`（`b≠0`、非标量、流非平凡）；"
    "⑦主定理 `faithfulBlockState_criterion` 三支合取。结论：非 III 半边不再依赖对角化，但仍只是 "
    "2×2 块代数上的共轭恒等判据。资产：`G3P2FaithfulBlockState.lean` 20 条（1 结构 + 7 定义 + 12 "
    "定理；`lake build` rc=0、零告警）；判据 C01–C14 14/14 ALL_PASS。诚实边界：仅乘积块模型；"
    "「忠实正定」只编码 Sylvester 判据；`Ad ρ` 是模流代数替身，KMS 本体未构造；谱比判据仍只对"
    "对角态成立；可操作性判据未形式化；经典因子分类与 Tomita `Δ_mod^{it} ∈ A^×` 未形式化；"
    "载体/vN 完成性缺失 ⇒ P2 未成立、G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）。"
)

SEG_ROAD = (
    "P7-5e-378（G3-P2-10：非对角忠实态的单位可实现性——拆除 P2-9 的对角化限制，2026-11-04）："
    "接 377（论证上接 372/373）。377 的「非 III」半边只在 `DiagState` 内成立。本轮：①一般忠实正定"
    "块态 `FaithfulBlockState`（`0 < a`、`0 < a*c − b²`）由 `Matrix.nonsing_inv` 构造代数单位 "
    "`FaithfulBlockState.unit`，不需谱分解；②`conj_trivial_iff`：`Ad ρ = id` ⟺ 标量（只用 `E₁₂` "
    "交换子）；③`conj_nontrivial`；④`faithfulFlow_unitRealizable`；⑤`faithfulFlow_trivial_iff`"
    "/`faithfulFlow_nontrivial`；⑥非对角见证 `nonDiagonalState`=`[[2,1],[1,1]]` 非标量且流非平凡；"
    "⑦主定理 `faithfulBlockState_criterion` 三支。资产：`G3P2FaithfulBlockState.lean` 20 条"
    "（1 结构 + 7 定义 + 12 定理；`lake build` rc=0 零告警）；判据 "
    "`p7_5e378_faithful_block_state_criteria.py` C01–C14 14/14。缺口：仅乘积块模型；忠实正定只编码 "
    "Sylvester 判据（正规性/σ-弱闭/因子性/一般维数未形式化）；`Ad ρ` 为模流代数替身，KMS 本体未"
    "构造；谱比判据仍只对对角态成立（377）；可操作性判据未形式化；经典因子分类与 Tomita "
    "`Δ_mod^{it} ∈ A^×` 未形式化；载体/vN 完成性未定义 ⇒ P2 未成立、G3 未闭合。"
    "不关闭任何项（226 挂起、k(2) 开放）。"
)

SEG_DIG = (
    "## 九十三、G3-P2-10 非对角忠实态的单位可实现性：拆除对角化限制（2026-11-04）\n\n"
    "**口径**：接 369（论证上接 368/372/373）。368 的「非 III 半边」只在 `DiagState` 内成立。\n\n"
    "1. **一般忠实正定块态**：`FaithfulBlockState` 把 `[[a,b],[b,c]]` 的正定性编码为 `0 < a` 与 "
    "`0 < a*c − b²`；由 `Matrix.nonsing_inv` 双侧单位律构造代数单位，不需要谱分解。\n"
    "2. **共轭恒等 ⟺ 标量**：`conj_trivial_iff` 用与 `E₁₂` 的交换子证明 `Ad ρ = id` 只能是标量。\n"
    "3. **非标量 ⟹ 非平凡共轭**：`conj_nontrivial`。\n"
    "4. **单位可实现**：任一忠实正定块态流单位可实现（`faithfulFlow_unitRealizable`）。\n"
    "5. **双块判据**：流恒等 ⟺ 两块都标量（`faithfulFlow_trivial_iff`/`faithfulFlow_nontrivial`）。\n"
    "6. **非对角见证**：`[[2,1],[1,1]]` 忠实正定、`b≠0`、非标量，其流非平凡"
    "（`nonDiagonalFlow_nontrivial`）。\n"
    "7. **主定理**：`faithfulBlockState_criterion` 三支合取。\n\n"
    "**资产**：`G3P2FaithfulBlockState.lean`（20 条：1 结构 + 7 定义 + 12 定理；`lake build` rc=0 "
    "零告警）；`p7_5e378_faithful_block_state_criteria.py` C01–C14 14/14 ALL_PASS。\n\n"
    "**诚实边界**：仅 `M₂(ℚ)×M₂(ℚ)` 乘积块模型；「忠实正定」只编码 Sylvester 判据（正规性/"
    "σ-弱闭/因子性/一般维数未形式化）；`Ad ρ` 仍为模流 `Ad Δ_mod^{it}` 的代数替身，`ρ^{it}` "
    "复相位、解析延拓与 KMS 本体未构造；谱比判据仍只对对角态成立（377）；可操作性判据未形式化；"
    "经典 I/II/III 与 Tomita `Δ_mod^{it} ∈ A^×` 未形式化；载体/vN 完成性未定义 ⇒ P2 未成立、"
    "G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）。"
)

# 按编号定位插入：新条目插到「前驱编号条目」之后，而不是插到某个句子之后。
# (name, path, entry_pattern, predecessor_key, segment, marker)
ITEMS = [
    ("RS", P_RS, r"^> \*\*(\d{3})（", "368", SEG_RS, "369（本轮，G3-P2-10"),
    ("P48", P_P48, r"^286([a-z]{2})（", "ce", SEG_P48, "286cf（2026-11-04"),
    ("ROAD", P_ROAD, r"^P7-5e-(\d{3})（", "377", SEG_ROAD, "P7-5e-378（G3-P2-10"),
]

DIG_PREV = 92
DIG_MARKER = "## 九十三、"


def _line_keys(lines, pat):
    rx = re.compile(pat)
    return [(i, rx.match(l).group(1)) for i, l in enumerate(lines) if rx.match(l)]


def probe():
    ok = True
    for name, path, pat, prev, _seg, marker in ITEMS:
        lines, nl = read_lines(path)
        keys = _line_keys(lines, pat)
        prevs = [i for i, k in keys if k == prev]
        marks = [i for i, l in enumerate(lines) if marker in l]
        print(f"[{name}] predecessor({prev})={len(prevs)} marker={len(marks)} nl={nl!r}")
        if len(prevs) != 1 or len(marks) > 1:
            ok = False
    lines, nl = read_lines(P_DIG)
    blocks = [b for b in digest_blocks(lines) if b[2] == DIG_PREV]
    marks = [l for l in lines if DIG_MARKER in l]
    print(f"[DIG] predecessor({DIG_PREV})={len(blocks)} marker={len(marks)} nl={nl!r}")
    if len(blocks) != 1 or len(marks) > 1:
        ok = False
    return ok


def apply():
    if not probe():
        print("PROBE FAIL — 前驱条目定位不唯一，停止 apply")
        return False
    for name, path, pat, prev, seg, marker in ITEMS:
        lines, nl = read_lines(path)
        if any(marker in l for l in lines):
            print(f"[{name}] already applied, skip")
            continue
        idx = [i for i, k in _line_keys(lines, pat) if k == prev][0]
        lines[idx + 1:idx + 1] = [seg]
        write_lines(path, lines, nl)
        print(f"[{name}] inserted after {prev} at L{idx + 1}")
    lines, nl = read_lines(P_DIG)
    if any(DIG_MARKER in l for l in lines):
        print("[DIG] already applied, skip")
        return True
    blocks = digest_blocks(lines)
    hit = [b for b in blocks if b[2] == DIG_PREV]
    if not hit:
        print(f"[DIG] FAIL: predecessor section {DIG_PREV} not found")
        return False
    start, end, _ = hit[0]
    body = SEG_DIG.split("\n")
    lines[end:end] = [""] + body
    write_lines(P_DIG, lines, nl)
    print(f"[DIG] inserted after section {DIG_PREV} (L{end})")
    return True


def verify():
    ok = True
    for name, path, pat, _prev, _seg, marker in ITEMS:
        lines, nl = read_lines(path)
        marks = [l for l in lines if marker in l]
        keys = [k for _, k in _line_keys(lines, pat)]
        runs = journal_runs(lines, pat)
        target = [ks for g, ks in runs if any(marker in lines[i] for i in g)]
        ascending = bool(target) and target[0] == sorted(target[0])
        print(f"[{name}] marker={len(marks)} run_ascending={ascending} nl={nl!r}")
        if len(marks) != 1 or not ascending or nl != "\r\n":
            ok = False
    lines, nl = read_lines(P_DIG)
    marks = [l for l in lines if DIG_MARKER in l]
    seq = [n for _, _, n in digest_blocks(lines) if 84 <= n <= 93]
    good = seq == list(range(84, 94))
    print(f"[DIG] marker={len(marks)} sections84..93={seq} nl={nl!r}")
    if len(marks) != 1 or not good or nl != "\r\n":
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
