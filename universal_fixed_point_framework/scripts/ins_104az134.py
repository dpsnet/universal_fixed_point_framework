# -*- coding: utf-8 -*-
"""104az-134 落盘：RESEARCH_STATE.md + roadmap 插入 '平方差框架闭包' 条目。"""
import io

RS = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
RM = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\roadmap\phase102b_full_endogenous_roadmap.md"

rs_anchor = "**结论：k_max=8 由两条独立代数路径同时唯一锁定（幂基立方 + 平方差-2幂交点）——双涌现结构成立，全部机器验证**。"
rm_anchor = "诚实边界：纯数论唯一性的物理意义为框架身份指认、k_max 物理必然性由 Clifford(3,1) 承载。"

rs_entry = (
    "- **★★ 平方差框架闭包完整判别——f 迭代闭包 2→3→8→63 + '41,27,12,2' 试探对齐（2026-10-20，Phase 104az-134，脚本 `scripts/_phase104az134_sqdiff_closure.py`，out_134.txt）**：\n"
    "**① ★★★ 核心发现（A1）**：**n=2..8 的 7 个平方差全部落在框架素基 {2,3,5,7} 闭包内（7/7）**——2²−1=3（N_gen）、3²−1=8（k_max）、4²−1=15（静默×N_gen）、5²−1=24（N_gen×k_max）、6²−1=35（静默×对合域）、7²−1=48（差1链中段）、8²−1=63（对合域×N_gen²）——**从幂基到 k_max 的连续 7 个整数，平方差无一野值**；\n"
    "**② ★★ 2 幂唯一性在窗口内传承（A2）**：2≤n≤8 内 n²−1 为 2 幂的唯一 n=3（133 主定理窗口版）——**7 个平方差全落框架积，但只有 n=3 的恰为 2 幂——框架量集内 2 幂性是独特挑选**；\n"
    "**③ ★★ f 迭代纯框架链与边界（A3）**：f(x)=x²−1 迭代 **2→3→8→63 前 4 步全在纯框架闭包内**（幂基→N_gen→k_max→对合域×N_gen²）；**f(63)=3968=2⁷·31 离开纯框架层**（31=2⁵−1 Mersenne，静默指数 5）——纯框架闭包恰好覆盖 [2,8]（幂基→k_max 区间），63 是最后框架值；\n"
    "**④ B（未决线索'41,27,12,2'试探对齐，登记非定案）**：41=7²−8=对合域²−k_max（干净命中）、27=N_gen³、12=N_gen×不动点、2=幂基；链差分 {14,15,10}={2·7, 3·5, 2·5} 全落框架积；'44−3,30−3,15−3,5−3'中 44 非纯框架素基（44−3=41 无干净身份）、30=2·3·5 ✓、15=3·5 ✓、5=5 ✓——**41≈42（对合域×6）与 44−3 侧不干净，语义在压缩前上下文不可考——登记为框架对齐事实，不立结构判别**；\n"
    "**⑤ ★★★ Lean 形式化（新增 `MUFPFormalization.SqDiffClosure.lean`，lake build 3049 jobs 零 sorry 零 warning）**：closure_n2..n8（7 个平方差表，norm_num）、closure_n3_prime..n8_prime（框架素基分解 8=2³、15=3·5、24=2³·3、35=5·7、48=2⁴·3、63=3²·7）、sqdiff_closure_judgement（联合闭包定理）、**unique_two_power_in_window（2≤n≤8 ∧ n²−1=2^m → n=3——引用 133 主定理窗口传承）**、iter_chain（f 2=3 ∧ f 3=8 ∧ f 8=63）、iter_escape（f 63=2⁷·31 迭代边界）、thirty_one_mersenne（31=2⁵−1）、sqdiff_closure_full_judgement（联合判别）；\n"
    "**⑥ 判别结论**：**平方差闭包是框架结构性质（非巧合）**——[2,8] 区间平方差全落框架素基、2 幂唯一交点 n=3 恰为 N_gen、f 迭代纯框架链止于 63——与 132 商闭包循环（8→7→3→2）、133 双涌现路径构成同一代数结构的三视角；\n"
    "**⑦ 诚实边界**：闭包事实为代数观测（7/7 全验证 + Lean 固化），'为何闭包区间恰为 [2,8]=[幂基,k_max]'为框架身份指认（无独立机制推导）；f(63) 离开层（31 为 Mersenne 非框架素基成员）是边界观测非解释；'41,27,12,2' 仅登记对齐事实（语义待用户确认）；k_max=8 物理必然性仍由 Clifford(3,1) 承载（264）。\n"
)

rm_entry = (
    "- **★★ 平方差框架闭包完整判别（2026-10-20，Phase 104az-134）**：n=2..8 的 7 个平方差全落框架素基 {2,3,5,7} 闭包（2²−1=3、3²−1=8、4²−1=15、5²−1=24、6²−1=35、7²−1=48、8²−1=63——7/7 无一野值）；2 幂唯一交点 n=3（133 主定理窗口传承）；f(x)=x²−1 迭代纯框架链 2→3→8→63、f(63)=2⁷·31 离开纯框架层（31=2⁵−1 Mersenne）；Lean `SqDiffClosure.lean` 3049 jobs 零 sorry 零 warning（闭包表 + 素基分解 + 窗口唯一性引用 133 + 迭代链/边界 + Mersenne 身份）；'41,27,12,2' 试探：41=7²−8 干净命中、27=3³、12=3·4、2=2、链差分全落框架积——登记对齐事实（语义不可考，不立判别）；诚实边界：闭包为代数观测+机器固化、'为何闭包恰 [2,8]'为身份指认、f(63) 离开为边界观测。\n"
)

def insert(anchor, entry, path, name):
    with io.open(path, "r", encoding="utf-8") as f:
        text = f.read()
    cnt = text.count(anchor)
    print(f"[{name}] anchor count = {cnt}")
    assert cnt == 1, f"{name}: anchor count != 1 (={cnt})"
    pos = text.index(anchor) + len(anchor)
    new = text[:pos] + "\n" + entry + text[pos:]
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(new)
    print(f"[{name}] new len = {len(new)} (old {len(text)})")

insert(rs_anchor, rs_entry, RS, "RS")
insert(rm_anchor, rm_entry, RM, "RM")

for name, path, key in (("RS", RS, "Phase 104az-134"), ("RM", RM, "Phase 104az-134")):
    with io.open(path, "r", encoding="utf-8") as f:
        t = f.read()
    print(f"[{name}] verify count = {t.count(key)}")
    assert t.count(key) == 1
print("OK")
