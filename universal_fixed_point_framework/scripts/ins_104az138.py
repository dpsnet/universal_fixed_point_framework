# -*- coding: utf-8 -*-
"""104az-138 落盘：RESEARCH_STATE.md + roadmap 插入 'Mersenne 闭包家族完整判别'。"""
import io

RS = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
RM = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\roadmap\phase102b_full_endogenous_roadmap.md"

rs_anchor = "'为何框架素基恰为 Mersenne 指数集'为框架身份指认；k_max=8 物理必然性仍由 Clifford(3,1) 承载（264）。"
rm_anchor = "诚实边界：等价判别为数值验证非 Lean 证明，Mersenne 质数性为经典数论。"

rs_entry = (
    "- **★★★ Mersenne 闭包家族完整判别——闭包指数 p = 框架量集（2026-10-20，Phase 104az-138，脚本 `scripts/_phase104az138_mersenne_full.py`，out_138.txt）**：\n"
    "**① ★★★ 核心判别（137 升级）**：n=2^p−1 的平方差闭包性由 2^(p−1)−1 的 7-平滑性决定（(2^p−1)²−1=2^(p+1)·(2^(p−1)−1)）；**闭包 p = {2,3,4,5,7} = 框架量集 {幂基, N_gen, 不动点, 静默, 对合域}——5/5 全闭包**；\n"
    "**② ★★ 137 勘误/扩展**：137 只固化 p∈框架素基 {2,3,5,7}（4/4），**遗漏 p=4（不动点）——2⁴−1=15 也是闭包成员（15²−1=2⁵·7=224 全框架）**；完整 Mersenne 闭包成员 {3,7,15,31,127} = {2^p−1: p∈框架量集}（5/5）；\n"
    "**③ ★★ 断裂判别**：p=6、p=8 断裂（63²−1=2⁷·31、255²−1=2⁹·127）——因 2^(p−1)−1 = 31、127 是 Mersenne 质数但非框架素基（**31、127 自身是框架组合数 2⁵−1/2⁷−1 但不是框架素基成员——'Mersenne 嵌套断裂'**）；p≥9 全部断裂（2^(p−1)−1 含 ≥17 质因子）；\n"
    "**④ ★★ 二次 Mersenne 链**：2^(p−1)−1 ∈ {1,3,7,15,63} = {2^k−1: k∈{1,2,3,4,6}} 全为框架数（63=3²·7=N_gen²×对合域）——**Mersenne 闭包的内部结构是'二次 Mersenne 链'**；\n"
    "**⑤ ★★★ Lean 形式化（扩展 `MUFPFormalization.SqDiffClosure.lean`，lake build 3049 jobs 零 sorry 零 warning）**：mersenne_p4（2⁴−1=15）、mersenne_p4_sqdiff（15²−1=2⁵·7）、mersenne_p6_break（63²−1=2⁷·31）、mersenne_p8_break（255²−1=2⁹·127）、second_mersenne_chain（2^k−1 链 {1,3,7,15,63} 全框架）、mersenne_full_judgement（138 联合判别：闭包 p 5/5 + 断裂两例）；\n"
    "**⑥ 判别结论**：**平方差闭包的 Mersenne 子家族完整定案——指数 p 恰为框架量集（不含 k_max=8）**；k_max=8 的 Mersenne 255 断裂（含 127 非框架）与 134 迭代边界 63 断裂（含 31）一致——框架量集对 Mersenne 指数的选择是'幂基..对合域'的闭区间；\n"
    "**⑦ 诚实边界**：p≤30 全扫描为数值验证（非 Lean 证明）；31/127 质数性为经典数论；'为何框架量集恰为 Mersenne 闭包指数集'为框架身份指认；k_max=8 物理必然性仍由 Clifford(3,1) 承载（264）。\n"
)

rm_entry = (
    "- **★★★ Mersenne 闭包家族完整判别（2026-10-20，Phase 104az-138）**：n=2^p−1 闭包 ⟺ 2^(p−1)−1 为 7-平滑；**闭包 p = {2,3,4,5,7} = 框架量集（5/5）**（137 勘误：补 p=4 不动点→2⁴−1=15 闭包）；Mersenne 闭包成员 {3,7,15,31,127}={2^p−1: p∈框架量集}；p=6/8 断裂（63²−1=2⁷·31、255²−1=2⁹·127，'Mersenne 嵌套断裂'——2^(p−1)−1 为 31/127 非框架素基）；二次 Mersenne 链 2^(p−1)−1∈{1,3,7,15,63} 全框架；p≥9 全断裂；Lean `SqDiffClosure.lean` 扩展 3049 jobs 零 sorry 零 warning（p4 闭包、p6/p8 断裂、二次 Mersenne 链、138 联合判别）；诚实边界：p≤30 数值验证，31/127 质数性经典数论，指数集选择为身份指认。\n"
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

for name, path, key in (("RS", RS, "Phase 104az-138"), ("RM", RM, "Phase 104az-138")):
    with io.open(path, "r", encoding="utf-8") as f:
        t = f.read()
    print(f"[{name}] verify count = {t.count(key)}")
    assert t.count(key) == 1
print("OK")
