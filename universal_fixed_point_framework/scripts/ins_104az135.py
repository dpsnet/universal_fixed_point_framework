# -*- coding: utf-8 -*-
"""104az-135 落盘：RESEARCH_STATE.md + roadmap 插入 '平方差 7-平滑闭包完整谱'（134 A1 勘误扩展）。"""
import io

RS = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
RM = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\roadmap\phase102b_full_endogenous_roadmap.md"

rs_anchor = "k_max=8 物理必然性仍由 Clifford(3,1) 承载（264）。"
rm_anchor = "f(63) 离开为边界观测。"

rs_entry = (
    "- **★ 平方差 7-平滑闭包完整谱——134 A1 勘误扩展 + 675 平方差身份发现（2026-10-20，Phase 104az-135，脚本 `scripts/_phase104az135_sqdiff_smooth.py`，out_135.txt）**：\n"
    "**① ★ 勘误登记**：134 A1 只测 n=2..8（7/7）——复核发现 **n=9 亦落框架素基（9²−1=80=2⁴·5=不动点²×静默）——134 的 [2,8] 结论不完整，补正为最长连续闭包段 [2,9]（长度 8，n=9=k_max+1=N_gen²）**；\n"
    "**② ★★★ 完整谱（n=2..64 全扫描，质因子 ⊆ {2,3,5,7}）**：闭包 n = {2,3,4,5,6,7,8,9} ∪ {11,13,15,17,19} ∪ {26,29,31,41,49,55}；**最长连续段 [2,9]（8 个）**、**首个断裂 n=10（99=9·11，11 质因子；10=k_max+2）**、21/23/25/27 断裂（22=2·11 等）、偶数闭包仅 2..8 ∪ {26}（n=26 是唯一 ≥10 的偶数闭包）；\n"
    "**③ ★★★ 新发现：675 平方差身份**——**n=26 的平方差 = 675（26²−1=675=3³·5²）且 26=静默²+1**——**δ=1/675 静默修正分母（P7-5t，F_np/m_s/T_c/m_τ 修正族）本身是平方差值**——修正分母家族（675 静默族）与平方差闭包直接连接（跨链）；\n"
    "**④ ★★ 闭包 n 家族指认（全落框架组合 ±1）**：9=k_max+1=N_gen²、11=k_max+3=N_active+k_max、13=k_max+静默、15=不动点²−1、17=不动点²+1（+1 家族）、19=不动点²+N_gen、26=静默²+1、29=对合域×不动点+1（+1 家族）、31=2⁵−1（Mersenne 静默指数）、41=k_max×静默+1（镜像分子对 P7-5e-274）、49=对合域²、55=k_max×对合域−1（56−1）——**闭包 n 集合 ≈ 框架组合 ±1 家族**（2..8 连续段本身是框架量区间）；\n"
    "**⑤ ★★ 31 双重角色**：n=31 是闭包值（31²−1=2⁶·3·5 全框架）、31 又是断裂质因子（n=63: 2⁷·31、n=32: 3·11·31）——闭包 n ∧ 断裂因子的自指角色（31=2⁵−1 Mersenne 与 f(63) 迭代边界一致）；\n"
    "**⑥ ★★★ Lean 形式化（扩展 `MUFPFormalization.SqDiffClosure.lean`，lake build 3049 jobs 零 sorry 零 warning）**：closure_n9（80）、closure_n9_frame（80=2⁴·5）、window_n9_end（9=3²∧9=8+1）、break_n10（99=9·11）、**closure_n26（26²−1=675）**、closure_n26_frame（675=3³·5²）、silence_sq_plus_one（26=静默²+1）、n11/n13/n17/n29/n41/n49/n55_identity（闭包 n 家族指认）、closure_n29/n31/n41/n49/n55（闭包分解）、break_n63/n32（31 断裂角色）、**sqdiff_smooth_full_judgement（135 联合判别）**；\n"
    "**⑦ 判别结论**：**平方差闭包谱呈框架结构**——最长连续段 [2,9] 恰为 [幂基, N_gen²]（k_max+1 端点）、闭包 n 全落框架组合 ±1 家族、675 修正分母获平方差身份——与 132 商闭包循环、133 双涌现路径、134 迭代边界构成同一代数结构的第四视角；\n"
    "**⑧ 诚实边界**：完整谱为数值全扫描（n≤64）+ Lean 固化（闭包/断裂/家族指认）；'为何最长连续段恰为 [2,9]'、'为何闭包 n 恰为框架组合 ±1'仍为框架身份指认（无独立机制推导）；675 平方差身份是新连接（非新机制）；n>64 的闭包成员（如 71?、89?）未穷举——亚序列规律（奇数 m 使 m±1 7-平滑）是数论结构，框架意义待判别；k_max=8 物理必然性仍由 Clifford(3,1) 承载（264）。\n"
)

rm_entry = (
    "- **★ 平方差 7-平滑闭包完整谱（2026-10-20，Phase 104az-135）**：134 A1 勘误——补入 n=9（9²−1=80=2⁴·5），最长连续闭包段更正为 **[2,9]（8 个，n=9=k_max+1=N_gen²）**；n=2..64 全扫描闭包 n = {2..9}∪{11,13,15,17,19}∪{26,29,31,41,49,55}，首个断裂 n=10（99=9·11）；**★ 新发现：n=26 → 675（δ=1/675 静默修正分母本身是平方差，26=静默²+1）——修正分母族与平方差闭包跨链**；闭包 n 家族全落框架组合 ±1（9=k_max+1、17=不动点²+1、29=对合域×不动点+1、31=2⁵−1、41=k_max×静默+1、49=对合域²、55=k_max×对合域−1）；31 双重角色（闭包 n ∧ 断裂质因子）；Lean `SqDiffClosure.lean` 扩展 3049 jobs 零 sorry 零 warning（closure_n9/n26、break_n10/n63/n32、家族指认、675 分解、联合判别）；诚实边界：谱为数值扫描+机器固化、'为何最长段 [2,9]'与'为何闭包 n = 框架±1'为身份指认、n>64 未穷举。\n"
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

for name, path, key in (("RS", RS, "Phase 104az-135"), ("RM", RM, "Phase 104az-135")):
    with io.open(path, "r", encoding="utf-8") as f:
        t = f.read()
    print(f"[{name}] verify count = {t.count(key)}")
    assert t.count(key) == 1
print("OK")
