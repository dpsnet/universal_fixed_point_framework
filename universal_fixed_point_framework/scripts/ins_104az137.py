# -*- coding: utf-8 -*-
"""104az-137 落盘：RESEARCH_STATE.md + roadmap 插入 '闭包结构定理 + Mersenne 闭包判别'。"""
import io

RS = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
RM = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\roadmap\phase102b_full_endogenous_roadmap.md"

rs_anchor = "亚序列规律（奇数 m 使 m±1 7-平滑）是数论结构，框架意义待判别；k_max=8 物理必然性仍由 Clifford(3,1) 承载（264）。"
rm_anchor = "n>64 未穷举。"

rs_entry = (
    "- **★★★ 平方差闭包结构定理判别 + Mersenne 闭包判别（2026-10-20，Phase 104az-137，脚本 `scripts/_phase104az137_smooth_pairs.py`，out_137.txt）**：\n"
    "**① ★★★ 等价判别**：闭包 ⟺ (n−1),(n+1) 均 7-平滑（n=2..512 全验证，**反例数 = 0**）——n²−1=(n−1)(n+1) 的结构定理形式；\n"
    "**② ★★★ Mersenne 闭包判别**：**闭包 n 序列中的 Mersenne 成员 {3,7,31,127} = {2^p−1 : p∈框架素基 {2,3,5,7}}——4/4 全闭包**（2²−1=3=N_gen、2³−1=7=对合域、2⁵−1=31、2⁷−1=127）；通用形式 (2^p−1)²−1=2^(p+1)·(2^(p−1)−1)，其中 2^(p−1)−1 ∈ {1,3,15,63} 全为框架数——**Mersenne 数的平方差自动落在框架素基闭包**；\n"
    "**③ ★★ 完整闭包序列（n≤512）**：{2..9, 11, 13, 15, 17, 19, 26, 29, 31, 41, 49, 55, 71, 97, 99, 127, 161, 244, 251, 449}，最长连续段 (2,9)；n>64 新成员 8 个：71, 97, 99, 127, 161, 244, 251, 449；\n"
    "**④ ★★ 新成员框架身份**：n=71 → **5040=7!=对合域阶乘**（71=幂基×静默×对合域+1=2·5·7+1）；n=127=2⁷−1（**对合域指数 Mersenne**，2⁶−1=63=3²·7 框架）；n=244=3⁵+1（N_gen⁵+1，n−1=243=3⁵ 纯 3 幂）；n=97=2⁵·3+1、n=99=2·7²+1、n=161=2⁵·5+1、n=251=2·5³+1、n=449=2⁶·7+1——**闭包 n = 框架积/幂 ±1 或 Mersenne 的统一模式**；\n"
    "**⑤ ★★ 断裂来源判别**：22=2·11 是第一个非 7-平滑偶数（11=第一个 >7 的质数）——**[2,9] 连续段与奇数 3..19 段由 '11 是第一个 >7 质数' 驱动**；n=22 断裂（22²−1=3·7·23）；\n"
    "**⑥ ★★★ Lean 形式化（扩展 `MUFPFormalization.SqDiffClosure.lean`，lake build 3049 jobs 零 sorry 零 warning）**：mersenne_p2/p3/p5/p7（2^p−1 四成员）、mersenne_p2_sqdiff..p7_sqdiff（Mersenne 平方差四分解）、n71_identity/n71_sqdiff（5040=2⁴·3²·5·7）、seven_factorial（7·6·5·4·3·2·1=5040）、n127_sqdiff（127²−1=2⁸·3²·7）、n244_identity/n244_sqdiff（244=3⁵+1、244²−1=3⁵·5·7²）、break_n22（22²−1=3·7·23）、mersenne_closure_judgement（137 联合判别）；\n"
    "**⑦ 判别结论**：**平方差闭包的等价判据（相邻对双 7-平滑）在 n≤512 全成立（结构定理级）**；Mersenne 成员与框架素基指数的 1:1 对应是新的判别级结构（框架素基 {2,3,5,7} 同时是 Mersenne 质数指数集——31、127 为 Mersenne 质数）；n=244=3⁵+1 将纯幂±1 家族扩展至 N_gen⁵+1；\n"
    "**⑧ 诚实边界**：等价判别为数值全验证（n≤512）而非 Lean 内证明（7-平滑定义/质因子分解超出当前实例级固化范围）；Mersenne 质数性（31、127 为质数）为经典数论；'为何框架素基恰为 Mersenne 指数集'为框架身份指认；k_max=8 物理必然性仍由 Clifford(3,1) 承载（264）。\n"
)

rm_entry = (
    "- **★★★ 平方差闭包结构定理 + Mersenne 闭包判别（2026-10-20，Phase 104az-137）**：等价判别——闭包 ⟺ (n−1),(n+1) 均 7-平滑（n≤512 零反例，结构定理级）；**Mersenne 闭包 4/4——{3,7,31,127}={2^p−1: p∈框架素基 {2,3,5,7}}**，通用 (2^p−1)²−1=2^(p+1)·(2^(p−1)−1) 全框架；闭包 n≤512 完整序列 {2..9,11,13,15,17,19,26,29,31,41,49,55,71,97,99,127,161,244,251,449}；新成员身份：71→5040=7!（对合域阶乘）、127=2⁷−1（对合域指数 Mersenne）、244=3⁵+1（N_gen⁵+1）、97/99/161/251/449 为框架积+1；断裂来源：22=2·11 第一个非 7-平滑偶数（11=第一个>7质数）驱动 [2,9] 与 3..19；Lean `SqDiffClosure.lean` 扩展 3049 jobs 零 sorry 零 warning（Mersenne 四成员+四分解、5040=7!、244=3⁵+1、n22 断裂、137 联合判别）；诚实边界：等价判别为数值验证非 Lean 证明，Mersenne 质数性为经典数论。\n"
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

for name, path, key in (("RS", RS, "Phase 104az-137"), ("RM", RM, "Phase 104az-137")):
    with io.open(path, "r", encoding="utf-8") as f:
        t = f.read()
    print(f"[{name}] verify count = {t.count(key)}")
    assert t.count(key) == 1
print("OK")
