# -*- coding: utf-8 -*-
import io, sys

MAP = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\notes\generative_chain_map.md"
RS = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"

MAP_NEW = """### §11.85 V9 韦达判别式族唯一性（v1.3 修正：原全称陈述作废）

> **2026-11-09 勘误（第四轮外部评审 + 机检复核）**：本节原记载的 `vieta_discriminant_mersenne_unique`
> 是**假命题**，且其证明从未编译通过。原陈述为“σ⁻¹ ∈ [1,64] 唯一使‘韦达方程有 ℕ 根 ∧ 判别式
> 为完全平方’成立者即 15”——但 (a)(b) 两条件对 σ⁻¹ = 7（根 {1,7}，D=36=6²）、12（根 {2,6}，
> D=16=4²）、16（根 {4,4}，D=0）**同时成立**，故全称陈述被直接证伪；原文把这三例标为“✗ 非框架根”，
> 是悄悄追加了第三条（根必须恰为 {3,5}）而不写进定理陈述。另：原证明行 `interval_cases σ_inv with hσ`
> 在该 Lean 版本无 `with` 形式，末例目标 `⊢ ↑64 = SigmaInv` 无法闭合。
>
> **现行 Lean 内容（三真断言，2026-11-09 构建通过 3048 jobs / exit 0）**：
> - `vieta_discriminant_family_values`：D(N) = 4^N − 2^{N+3} + 4 在 N=1..12 的 12 项具体值（数值枚举，非全称）
> - `vieta_discriminant_mersenne_witness`：N=3 见证 D(3) = 4 = 2²、根 {3,5} 互异
> - `vieta_discriminant_out_of_family_counterexamples`：族外反例 7/12/16 显式登记
>
> **唯一性的正确表述**：只在 σ⁻¹ = 2^{N+1}−1 参数族**内**成立——族内 σ⁻¹=15（N=3）是唯一给出互异整数根
> 且判别式为完全平方者。“σ⁻¹ ∈ [1,64] 唯一”一句作废。方案 B（2^{N+1}+1，N=3 时 D=−4<0）与
> 方案 C（3^N−1，N=3 时 D=−40<0）无实根，此结论不受影响。
>
> **残余边界（不变）**：为何 σ⁻¹ 必须取“2 的幂减 1”这一参数化仍未独立推导；族内全枚举（除 N=3 外
> 各 N 的 D 非完全平方）目前是数值枚举，Lean 全枚举登记为待补。论文 §12.4 项 3 已同步。

登记：RESEARCH_STATE 任务 #637（v1.3 已追加勘误条目）
"""

RS_ANCHOR = "> [状态]：数学形式化层推进——登记任务 #637。\n"
RS_ADD = """>

> **⚠ 2026-11-09 勘误（第四轮外部评审 / v1.3 处置，追加不覆盖）**：
> 上文 V9 `vieta_discriminant_mersenne_unique` 为**假命题**且从未编译通过——
> (a)(b) 两条件对 σ⁻¹=7（根 {1,7}，D=6²）、σ⁻¹=12（根 {2,6}，D=4²）、σ⁻¹=16（根 {4,4}，D=0）同时成立；
> 原文以“非框架根”排除三例，等于把“根恰为 {3,5}”这条未写进陈述的附加条件偷偷用于排除。
> 连带上文“σ⁻¹=2^{N+1}−1 是唯一让韦达方程有整数根的参数选择”“枚举 [1,64] 内唯一”两处结论**同时作废**。
> 另：原证明行 `interval_cases σ_inv with hσ` 在本版 Lean 无 `with` 形式，末例 `⊢ ↑64 = SigmaInv` 闭合失败。
>
> **现行状态（2026-11-09 实测，`lake build MUFPFormalization.ActiveSilentVieta` 3048 jobs / exit 0）**：
> 假定理已撤销，改为三条真断言——`vieta_discriminant_family_values`（D(N)=4^N−2^{N+3}+4 的 N=1..12 取值）、
> `vieta_discriminant_mersenne_witness`（N=3：D=4=2²，根 {3,5} 互异）、
> `vieta_discriminant_out_of_family_counterexamples`（7/12/16 族外反例登记）。
> 唯一性仅在 σ⁻¹=2^{N+1}−1 族内成立；族外全称陈述作废。论文 §12.4 项 3 已同步，笔记 §11.85 已重写。
"""


def probe():
    t = io.open(MAP, encoding="utf-8").read()
    print("MAP old header count=", t.count("### §11.85 V9 韦达判别式 Mersenne 唯一性（2026-11-10）"))
    rs = io.open(RS, encoding="utf-8").read()
    print("RS anchor count=", rs.count(RS_ANCHOR), " eras have errata already=", "2026-11-09 勘误（第四轮外部评审 / v1.3 处置" in rs)


def apply():
    t = io.open(MAP, encoding="utf-8").read()
    head = "### §11.85 V9 韦达判别式 Mersenne 唯一性（2026-11-10）"
    nxt = "### §11.86 sin²θ_W 纯框架独立推导"
    if t.count(head) != 1 or t.count(nxt) != 1:
        print("ABORT MAP anchors", t.count(head), t.count(nxt))
        return
    i = t.index(head)
    j = t.index(nxt)
    t = t[:i] + MAP_NEW + "\n" + t[j:]
    io.open(MAP, "w", encoding="utf-8", newline="").write(t)
    print("MAP APPLIED lines=", t.count("\n") + 1)

    rs = io.open(RS, encoding="utf-8").read()
    if rs.count(RS_ANCHOR) != 1:
        print("ABORT RS anchor count", rs.count(RS_ANCHOR))
        return
    rs = rs.replace(RS_ANCHOR, RS_ANCHOR + RS_ADD, 1)
    io.open(RS, "w", encoding="utf-8", newline="").write(rs)
    print("RS APPLIED bytes=", len(rs))


mode = sys.argv[1] if len(sys.argv) > 1 else "probe"
if mode == "probe":
    probe()
else:
    apply()
