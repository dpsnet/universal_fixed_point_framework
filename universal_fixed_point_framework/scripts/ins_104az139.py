# -*- coding: utf-8 -*-
"""104az-139 落盘：RESEARCH_STATE.md + roadmap 插入 '闭包质数子列判别'。"""
import io

RS = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
RM = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\roadmap\phase102b_full_endogenous_roadmap.md"

rs_anchor = "'为何框架量集恰为 Mersenne 闭包指数集'为框架身份指认；k_max=8 物理必然性仍由 Clifford(3,1) 承载（264）。"
rm_anchor = "诚实边界：p≤30 数值验证，31/127 质数性经典数论，指数集选择为身份指认。"

rs_entry = (
    "- **★★ 闭包质数子列判别——'闭包即质数筛选'（2026-10-20，Phase 104az-139，脚本 `scripts/_phase104az139_prime_subset.py`，out_139.txt）**：\n"
    "**① ★★★ 统计判别**：闭包成员 27 个中质数 16 个（**密度 59.3%**），随机对照 n≤512 质数密度仅 19.0%（27 个随机样本期望 5.1 个）——**实测 vs 期望比值 3.1x**；更精确的闭包率对照：质数 n 中闭包率 16/97=16.5% vs 合数 n 中闭包率 11/414=2.7%——**闭包对质数的偏好 ~6 倍**；\n"
    "**② ★★ 身份全谱**：全部 16 个质数闭包成员均满足 Mersenne 或 (n±1) 7-平滑（等价判别推论）；质数成员框架身份——Mersenne 型 {3,7,31,127}、框架积+1 型 {11=2·5+1, 13=2²·3+1, 17=4²+1, 19=2·3²+1, 29=7·4+1, 41=8·5+1, 71=2·5·7+1, 97=2⁵·3+1, 251=2·5³+1, 449=2⁶·7+1}（**10 个 +1 家族质数**）；2、5 为框架素基本身（平凡质数闭包）；\n"
    "**③ ★★ 合数对照**：合数闭包成员 {4,6,8,9,15,26,49,55,99,161,244} 的框架量身份——小框架幂 {4=2², 6=2·3, 8=2³, 9=3²}、Mersenne {15}、静默²+1 {26}、对合域² {49}、k_max×对合域−1 {55}、框架积+1 {99,161}、N_gen⁵+1 {244}——**质数/合数身份模式同源（均为框架积/幂±1 或 Mersenne），质数只是其中素数者**；\n"
    "**④ ★★★ Lean 形式化（扩展 `MUFPFormalization.SqDiffClosure.lean`，lake build 3049 jobs 零 sorry 零 warning）**：n13_sqdiff（13²−1=2³·3·7）、n19_identity/n19_sqdiff（19=2·3²+1、19²−1=2³·3²·5）、prime_subset_judgement（139 联合判别：13/19 + 11/17/29/41/97/251/449 的 +1 家族身份）；n13_identity 与 135 段既有（13=8+5）去重；\n"
    "**⑤ 判别结论**：**平方差闭包是'质数筛选器'（3.1x 富集，6 倍偏好）——闭包结构内在偏好质数 n**；质数闭包成员 100% 可指认为 Mersenne 或框架积/幂±1，与 137/138 统一模式闭合；'闭包即质数筛选'是 n²−1=(n−1)(n+1) 相邻平滑性的统计后果（质数只需相邻偶数平滑，合数还需自身因子参与）；\n"
    "**⑥ 诚实边界**：统计为 n≤512 数值验证（非 Lean 证明）；'质数偏好'的数论机制（相邻偶数 7-平滑对质数的条件概率）未形式化；k_max=8 物理必然性仍由 Clifford(3,1) 承载（264）。\n"
)

rm_entry = (
    "- **★★ 闭包质数子列判别（2026-10-20，Phase 104az-139）**：闭包质数密度 59.3%（16/27）vs 随机期望 19.0%（3.1x 富集）；质数闭包率 16.5% vs 合数闭包率 2.7%（6 倍偏好）——**闭包即质数筛选**；16 个质数闭包成员 100% 满足 Mersenne 或 (n±1) 7-平滑；身份谱：Mersenne {3,7,31,127} + 框架积+1 {11,13,17,19,29,41,71,97,251,449} + 框架素基 {2,5}；合数成员亦全为框架积/幂±1 或 Mersenne（模式同源）；Lean `SqDiffClosure.lean` 扩展 3049 jobs 零 sorry 零 warning（13/19 框架身份 + 139 联合判别，n13_identity 去重）；诚实边界：统计为数值验证，质数偏好机制未形式化。\n"
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

for name, path, key in (("RS", RS, "Phase 104az-139"), ("RM", RM, "Phase 104az-139")):
    with io.open(path, "r", encoding="utf-8") as f:
        t = f.read()
    print(f"[{name}] verify count = {t.count(key)}")
    assert t.count(key) == 1
print("OK")
