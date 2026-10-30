# -*- coding: utf-8 -*-
import io

# ========== 1. Paper 58 v0.24 ==========
p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()
edits = 0
def rep(old, new, tag):
    global s, edits
    assert old in s, tag + " anchor"
    s = s.replace(old, new, 1)
    edits += 1

rep("**版本**：v0.23（2026-10-02）", "**版本**：v0.24（2026-10-02）", "version")

old_abs = "（推论 5.8：165 因子全集 15000 模式全决定性记号完备持续五阶；**n=10 判据极限边界**：46 尾 + 3 头补 = 49 因子主样本 40000 闭合（38801 模式）、但独立复核 4 冲突全为频次 1 极端稀有模式、诊断判据单样本退化、补 s1_2 无效——**符号判据跨集一致性在 n=10 无法闭合，模式外连续量依赖证据**；阶数规律断裂确认（尾部 25→46，+21）；判定表 38801 条为主样本级资产）**；形变循环翻译完成"
new_abs = "（推论 5.8：165 因子全集 15000 模式全决定性记号完备持续五阶；**n=10 极限边界机制化（2026-10-02 Phase 73）**：4 冲突模式（频次 1/70000）实证为**模式内多连通分支**——A_BG 分段常值 {0,±1}，分支边界 = V_fn 的 Theta 阶跃变号面 ratio = bracket(K1,K2)/bracket(Sk,Sk1)；**缺失因子 = 基座未捕获的相邻分割括号**——补入粒子 2 前缀块家族 7 因子（s23_*/s234_*/…/s23456789_*）后冲突 **4→2**（seed 211 清零，57 因子主样本 38827 模式 0 非决定）；剩余 2 冲突（seed 77）需相邻块对括号（非前缀型），登记继续项；**极限边界从经验性未闭合升级为机制化解释**；阶数规律断裂确认（尾部 25→46，+21））**；形变循环翻译完成"
rep(old_abs, new_abs, "abstract")

old_c58_tail = "**诚实定位**：n=10 判定表**未闭合**（主样本级 38801 条资产保留，跨集一致性不成立）；n=5→n=9 五阶完整闭合为已确立主线；n=10 极限边界登记为开放研究问题（判据适用域上界证据，非否定）。"
new_c58_tail = "**机制化进展（2026-10-02 Phase 73）**：冲突模式投影捕获（M1）→ 局域扰动采样（M2）→ 分支结构识别（M3）：**A_BG 分段常值（{0,±1}），符号投影区域内多连通分支，分支边界 = V_fn 的 Theta 阶跃 ratio = bracket(K1,K2)/bracket(Sk,Sk1) 变号面**（K1/K2 前缀合并括号、d 相邻块对括号——均在 165 相邻分割全集内，全集决定性上界自洽）；**缺失因子 = 基座未捕获的相邻分割括号**：补入粒子 2 前缀块家族 7 因子（57 因子基座）→ 独立复核冲突 **4→2**（seed 211 清零、seed 77 保留），主样本 38827 模式 0 非决定；剩余 2 冲突（seed 77）在 8 前缀括号上两分支同号——需相邻块对括号（非前缀型），定向分支采样受 0 分支体积 <0.01% + 57 维保持 rejection 双重限制，**最小化登记为继续项**。**定位**：极限边界已从经验性未闭合升级为**机制化解释**（分支结构 + 缺失因子家族）；n=5→n=9 五阶完整闭合为已确立主线；n=10 完全最小化开放。"
rep(old_c58_tail, new_c58_tail, "c58 tail")

old_c13 = "**n=10 判据极限边界（推论 5.8 终态）**：165 因子全集 15000 模式全决定性（记号完备连续五阶）；阶数规律断裂确认为真（尾部 25→46，+21，退化结构大块区剧增）；补因子链 46→48→49→50（尾部 + 3 头部补 + s1_2）——**49 因子主样本 40000 闭合（38801 模式判定表导出）但独立复核 4 冲突全为频次 1 极端稀有模式**；诊断判据单样本退化（候选 ~100 全盖、s1_2 补入无效、冲突同批保留）——**符号判据跨集一致性在 n=10 无法闭合**（模式外连续量依赖证据，n=5 风险条款 1 实证）；n=5→n=9 五阶完整闭合为已确立主线，n=10 极限边界登记为开放研究问题（判据适用域上界）。"
new_c13 = "**n=10 极限边界机制化（推论 5.8 终态，2026-10-02 Phase 73）**：165 因子全集决定性（记号完备连续五阶）为**闭合上界**；阶数规律断裂确认为真（尾部 25→46，+21）；补因子链 46→48→49→50→**57**（+3 头补 +s1_2 假候选 +**7 粒子 2 前缀块家族 s23_*/s234_*/…/s23456789_***）——**冲突 4→2**（seed 211 清零、seed 77 保留，57 因子主样本 38827 模式 0 非决定、判定表导出）；**机制**：4 冲突模式实证为 A_BG 分段常值 {0,±1} 下的**多连通分支结构**——符号投影区域内分支不可分辨，分支边界 = V_fn 的 Theta 阶跃变号面 ratio = bracket(K1,K2)/bracket(Sk,Sk1)（前缀合并括号/相邻块对括号，均在 165 全集）；**极限边界升级为机制化解释**（缺失因子家族识别），完全最小化（剩余 seed 77 2 冲突需相邻块对括号）登记为开放继续项。"
rep(old_c13, new_c13, "conclusion 13")

old_hb = "⑥ **n=10 极限边界（2026-10-02 终态）**：补因子链 46→48→49→50 全链数值证据——49 因子主样本 40000 闭合（38801 模式、0 非决定、判定表导出）但 2×15000 独立复核 4 冲突（频次 1/70000 极端稀有）；诊断判据在单样本分组下退化（任何因子满足组内恒定且组间互异→候选全盖、s1_2 假候选无效）；**跨集一致性未闭合 = 符号判据适用域上界实证**（模式外连续量依赖，n=5 风险条款 1 落地）——为边界证据而非判据否定；⑦ 阶数断裂（尾部 25→46）为单次贪心 + 单次独立复核证据，非全局最小证明；⑧ 38801 条判定表为主样本级资产（跨集一致性未验证，不可当跨集定理用）。"
new_hb = "⑥ **n=10 极限边界机制化（Phase 73 终态）**：4 冲突模式实证为**模式内多连通分支**（A_BG 分段常值 {0,±1}，局域扰动采样 instance 1：−1 分支 99.4% + 0 分支 0.6%、instance 2：+1 分支 99.986% + 0 分支 0.014%）；分支边界 = V_fn 的 Theta 阶跃变号面（ratio = bracket(K1,K2)/bracket(Sk,Sk1)）；缺失因子 = 基座未捕获相邻分割括号（粒子 2 前缀块家族 7 因子补入冲突 4→2）；**剩余 seed 77 2 冲突需相邻块对括号，最小化未闭合（登记继续项）**——机制已确立、完全最小化未达成；⑦ 阶数断裂（尾部 25→46）为单次贪心 + 单次独立复核证据，非全局最小证明；⑧ 判定表（38801/38827 条）为主样本级资产（跨集一致性未完全验证，不可当跨集定理用）；⑨ 分支采样的 0 分支体积（0.6%/0.014%）与 57 维符号保持 rejection 使最小化采样成本无界——当前结论为机制 + 部分闭合证据。"
rep(old_hb, new_hb, "hb")

old_app_tail = "| `scripts/paperX_n10_diag_violations.py` + `paperX_n10_diag_violations.json` + `paperX_n10_final_base.json` | n=10 独立复核冲突诊断：4 冲突全频次 1、候选 ~100 全盖（单样本判据退化）、s1_2 假候选——极限边界归因 | 已运行 |\n| `scripts/paperX_n10_verify.py` / `paperX_n10_final_base.json` | n=10 链上脚本/50 因子最终基座（未闭合终态） | 落位 |"
new_app_tail = r"""| `scripts/paperX_n10_diag_violations.py` + `paperX_n10_diag_violations.json` + `paperX_n10_final_base.json` | n=10 独立复核冲突诊断：4 冲突全频次 1、候选 ~100 全盖（单样本判据退化）、s1_2 假候选——极限边界归因 | 已运行 |
| `scripts/paperX_n10_conflict_capture.py` + `paperX_n10_conflict_vectors.json` | **Phase 73 M1**：4 冲突模式完整 50 维投影 + 几何捕获（主表 count 全=1、投影几乎全非零 = 稀有符号排列模式） | 已运行 |
| `scripts/paperX_n10_local_scan.py` + `paperX_n10_local_scan.json` | **Phase 73 M2**：符号保持局域扰动采样（4 种子 × 5 尺度 × 2 万点）——instance 1/2 实证模式内多值（−1/+1 分支 vs 0 分支 0.6%/0.014%），instance 0/3 种子分支单值 | 已运行 |
| `scripts/paperX_n10_branch_flips.py` + `paperX_n10_branch_flips_i1.json` | **Phase 73 M3**：instance 1 区分括号 = bracket({2,3},{4..10})（s23_45678910，flip=60000 满分区分）——前缀合并括号变号面机制 | 已运行 |
| `scripts/paperX_n10_verify4_57.py` + `paperX_n10_base57_table.json` + `paperX_n10_final_summary_v57.json` | **Phase 73 M3**：57 因子（+7 粒子 2 前缀块）验证——主样本 38827 模式 0 非决定、独立复核冲突 4→2（seed 211 清零） | 已运行（部分闭合） |
| `scripts/paperX_n10_recursive_diag2.py` + `paperX_n10_recursive_diag2.json` | **Phase 73 M3**：seed 77 冲突在 8 前缀括号上两分支全同号（非前缀型缺失确认） | 已运行 |
| `scripts/paperX_n10_dpairs_diag.py` + `paperX_n10_dpairs_diag.json` | **Phase 73 M3**：d-括号（相邻块对）120 全集 flip 诊断——0 分支体积 <0.01% + 57 维保持 rejection 使采样成本无界（登记继续项） | 已运行（部分） |
| `scripts/paperX_n10_verify.py` / `paperX_n10_final_base.json` | n=10 链上脚本/50 因子最终基座（未闭合终态） | 落位 |"""
rep(old_app_tail, new_app_tail, "appendix A")

old_log = "| v0.23 | 2026-10-02 |"
new_log = r"""| v0.24 | 2026-10-02 | **n=10 极限边界机制化（Phase 73）**：4 冲突模式实证为模式内多连通分支（A_BG 分段常值 {0,±1}）；分支边界 = V_fn 的 Theta 阶跃变号面（ratio = bracket(K1,K2)/bracket(Sk,Sk1)）；缺失因子 = 基座未捕获相邻分割括号——粒子 2 前缀块家族 7 因子补入冲突 4→2（57 因子主样本 38827 模式 0 非决定、判定表导出、seed 211 清零）；剩余 seed 77 2 冲突需相邻块对括号（登记继续项）；摘要/推论 5.8/结论 13/诚实边界/附录 A（+7 脚本）/变更记录同步。 |
| v0.23 | 2026-10-02 |"""
rep(old_log, new_log, "changelog")

with io.open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("Paper 58 v0.24 written, edits:", edits)

# ========== 2. 路线图 phase73 更新 ==========
rp = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\roadmap\phase73_n10_continuum_limit.md"
with io.open(rp, "r", encoding="utf-8") as f:
    s = f.read()
anchor = "## 状态：M1 待启动（2026-10-02）"
new_state = r"""## 状态：M1–M3 完成，M4 已落盘（2026-10-02）

- **M1 ✅**：4 冲突模式 50 维投影 + 几何捕获（`paperX_n10_conflict_vectors.json`）——主表 count 全=1、投影几乎全非零（稀有符号排列模式，推翻"退化模式"初始解读）
- **M2 ✅**：符号保持局域扰动采样（`paperX_n10_local_scan.json`）——instance 1/2 实证**模式内多值**（−1/+1 分支 vs 0 分支，体积 0.6%/0.014%）；instance 0/3 种子分支单值
- **M3 ✅（机制确立，最小化未闭合）**：
  - 分支边界 = **V_fn 的 Theta 阶跃变号面** ratio = bracket(K1,K2)/bracket(Sk,Sk1)（A_BG 分段常值 {0,±1}）
  - 缺失因子 = 基座未捕获相邻分割括号：**粒子 2 前缀块家族 7 因子补入 → 冲突 4→2**（57 因子主样本 38827 模式 0 非决定、seed 211 清零）
  - 剩余 seed 77 2 冲突在 8 前缀括号上两分支全同号 → 需相邻块对括号（非前缀型）；定向采样受 0 分支体积 <0.01% + 57 维保持 rejection 双重限制——**最小化登记继续项**
- **M4 ✅ 落盘**：Paper 58 v0.24（推论 5.8 机制化终态）、笔记 §九、本路线图

**结论**：极限边界从"经验性未闭合"升级为**机制化解释**（多连通分支 + Theta 变号面 + 缺失因子家族识别）；n=5→n=9 完整闭合 + n=10 机制化 = Phase 72/73 主线收官。开放继续项：seed 77 2 冲突的相邻块对括号最小化（采样成本无界，需新采样法）。"""
assert anchor in s, "roadmap state anchor"
s = s.replace(anchor, new_state, 1)
with io.open(rp, "w", encoding="utf-8") as f:
    f.write(s)
print("roadmap updated")

# ========== 3. 笔记追加 ==========
np = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\notes\06_photon_topology\note_phase72_n10_criterion.md"
with io.open(np, "r", encoding="utf-8") as f:
    s = f.read()
add = """

## 九、极限边界机制化（Phase 73，2026-10-02）

4 冲突模式（频次 1/70000）从"经验性未闭合"升级为**机制化解释**：

- **M1 投影捕获**：4 冲突模式 50 维投影几乎全非零（主表 count 全=1）——稀有符号排列模式，非退化模式。
- **M2 局域扰动实证**：符号保持采样（4 种子 × 5 尺度 × 2 万点）——instance 1 多值（−1 分支 99.4% + 0 分支 0.6%）、instance 2 多值（+1 分支 99.986% + 0 分支 0.014%）、instance 0/3 种子分支单值。**模式内多值实证成立**（A_BG 分段常值 {0,±1}，多连通分支）。
- **M3 形式识别**：分支边界 = **V_fn 的 Theta 阶跃变号面**（ratio = bracket(K1,K2)/bracket(Sk,Sk1)——前缀合并括号/相邻块对括号，均在 165 相邻分割全集）。instance 1 区分括号 = **s23_45678910**（flip=60000 满分区分）。**缺失因子 = 基座未捕获相邻分割括号**。
- **M3 验证（57 因子）**：补入粒子 2 前缀块家族 7 因子（s23_*/s234_*/…/s23456789_*）→ 主样本 38827 模式 0 非决定、独立复核冲突 **4→2**（seed 211 清零、seed 77 保留）。
- **剩余开放**：seed 77 2 冲突在 8 前缀括号上两分支全同号——需相邻块对括号（非前缀型）；定向分支采样受 0 分支体积 <0.01% + 57 维保持 rejection 双重限制，成本无界——登记继续项。
- 产物：`paperX_n10_conflict_vectors.json` / `local_scan.json` / `branch_flips_i1.json` / `base57_table.json` / `final_summary_v57.json` / `recursive_diag2.json`；Paper 58 v0.24。
"""
with io.open(np, "a", encoding="utf-8") as f:
    f.write(add)
print("note updated")
