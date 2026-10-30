# -*- coding: utf-8 -*-
import io

p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()
edits = 0
def rep(old, new, tag):
    global s, edits
    assert old in s, tag + " anchor"
    s = s.replace(old, new, 1)
    edits += 1

rep("**版本**：v0.25（2026-10-03）", "**版本**：v0.26（2026-10-03）", "version")

old_abs = "；n=10 从“极限边界未闭合”升级为**完全闭合（跨集一致性）**；阶数规律断裂确认（尾部 25→46，+21））**；形变循环翻译完成"
new_abs = "；n=10 从“极限边界未闭合”升级为**完全闭合（跨集一致性）**；**阶数规律跨集回溯审计（Phase 74，2026-10-03）**：n=6/7 基座（12/16 因子）跨集稳健 PASS、**n=8/9 基座（23/27 因子）跨集暴露缺失 → 修正为 31/38 因子**（补前缀合并括号家族 s1_*大A/s12_*/s123_*/s1234_*/s12345_*/s123456_*/s1234567_* + 粒子 2 前缀块 + 中段合并）——**跨集一致性闭合基座序列 12/16/31/38/59**；补因子机制与 n=10 统一（基座未捕获的相邻分割括号）**；阶数规律断裂确认（尾部 25→46，+21））**；形变循环翻译完成"
rep(old_abs, new_abs, "abstract")

old_c58 = "**完全闭合达成（2026-10-03，Phase 73 终态）**："
new_c58 = "**跨集一致性回溯审计（2026-10-03，Phase 74）**：n=6/7/8/9 基座按 n=10 同标准（40000 主 + 5 seed × 15000）审计——**n=6（12 因子，环状 20 空间）PASS、n=7（16 因子）PASS、n=8（23 因子）FAIL（3 冲突）→ 补 8 因子 = 31 PASS、n=9（27 因子）FAIL（6 冲突）→ 补 11 因子 = 38 PASS**；n=8/9 补因子 = **前缀合并括号家族**（s1_23456/s1_2345678/s12_345678/s123_45678/s12345_678/s1234567_8/s23456_78/s1234_56；s1_23456/s123_456/s1234567_89/s23_45/s2_345678/s23456_789/s456_789 + 前 4 高频）——**与 n=10 补因子（粒子 2 前缀块 + 单粒子对）同机制：跨集暴露的缺失因子 = 基座未捕获的相邻分割括号（长前缀合并 + 中段合并）**；**跨集一致性闭合基座序列：12/16/31/38/59**（原主样本级序列 12/16/23/27/59 修正 n=8/9）。**n=10 判据完全闭合（2026-10-03，Phase 73 终态）**："
rep(old_c58, new_c58, "c58")

old_c13 = "**n=10 判据完全闭合（推论 5.8 终态，2026-10-03）**："
new_c13 = "**阶数规律跨集修正（推论 5.8 终态，2026-10-03，Phase 74）**：跨集一致性审计（5 seed × 15000）修正 n=8/9 基座——**闭合基座序列 12/16/31/38/59**（n=6/7 原基座稳健；n=8 23→31、n=9 27→38）；补因子统一机制（基座未捕获的相邻分割括号：长前缀合并 s1_*/s12_*/s123_*… + 粒子 2 前缀块 + 中段合并）；**原“主样本级贪心基座”在跨集下系统性暴露缺失（n=8/9/10 三阶）——主样本级闭合 ≠ 跨集闭合，跨集一致性审计为基座确定必要条件**。**n=10 判据完全闭合（推论 5.8 终态，2026-10-03）**："
rep(old_c13, new_c13, "conclusion 13")

old_hb = "⑩ **n=5→n=9 基座（主样本级贪心）在跨集一致性下的稳健性未系统验证**——n=10 教训（主样本级删除因子在跨集暴露缺失）提示应回溯检验（登记验证项）。"
new_hb = "⑩ **跨集一致性回溯审计完成（Phase 74）**：n=6/7 基座 PASS（跨集稳健）；**n=8/9 基座 FAIL → 修正为 31/38 因子**（补前缀合并括号家族，跨集一致性闭合，非最小基座证明）；n=10 的 59 因子同理为跨集一致性闭合；⑪ **主样本级闭合 ≠ 跨集闭合**——n=8/9/10 三阶主样本级贪心基座均在 5 seed 跨集下暴露缺失，跨集一致性审计为基座确定必要条件；⑫ n=8/9 补因子（8/11 个）与 n=10 补因子（9 个）均为跨集闭合而非最小基座（贪心最小性未证，登记）。"
rep(old_hb, new_hb, "hb")

old_app_tail = "| `scripts/paperX_n10_indep59.py` + `paperX_n10_indep59_summary.json` | **Phase 73 闭合**：59 因子扩展独立复核（seed 331/777/555）——3 seed 全部 0 冲突（总计 5 seed 115000 样本 0 违反） | 已运行（PASS） |"
new_app_tail = r"""| `scripts/paperX_n10_indep59.py` + `paperX_n10_indep59_summary.json` | **Phase 73 闭合**：59 因子扩展独立复核（seed 331/777/555）——3 seed 全部 0 冲突（总计 5 seed 115000 样本 0 违反） | 已运行（PASS） |
| `scripts/paperX_crossset_audit.py` + `paperX_crossset_audit_n7/8/9.json` | **Phase 74 审计**：n=7/8/9 基座跨集一致性（40000 主 + 5 seed ×15000）——n=7 PASS、n=8 3 冲突 FAIL、n=9 6 冲突 FAIL | 已运行 |
| `scripts/paperX_conflict_capture.py` + `paperX_n8/9_conflict_capture.json` | **Phase 74 诊断**：冲突模式投影捕获 + 主表回溯对比——n=8/9 变化因子 = 前缀合并括号家族（s1_*大A/s12_*/s123_*… + 粒子 2 前缀块） | 已运行 |
| `scripts/paperX_extend_verify.py` + `paperX_n8/9_extend_summary.json` | **Phase 74 补因子验证**：n=8 补 8 → 31 因子 PASS；n=9 补 11 → 38 因子 PASS（各 5 seed 全 0 冲突） | 已运行（PASS） |
| `scripts/paperX_n6_crossset_audit.py` + `paperX_n6_crossset_audit.json` | **Phase 74 审计**：n=6 环状 20 空间 12 因子基座——5 seed 全 0 冲突 PASS | 已运行（PASS） |"""
rep(old_app_tail, new_app_tail, "appendix A")

old_log = "| v0.25 | 2026-10-03 |"
new_log = r"""| v0.26 | 2026-10-03 | **跨集一致性回溯审计（Phase 74）**：n=6/7/8/9 基座按 n=10 同标准审计——n=6（12）PASS、n=7（16）PASS、n=8（23）FAIL→补 8=31 PASS、n=9（27）FAIL→补 11=38 PASS；补因子 = 前缀合并括号家族（s1_*/s12_*/s123_*/s1234_*/s12345_*/s123456_*/s1234567_* + 粒子 2 前缀块 + 中段合并），与 n=10 补因子（粒子 2 前缀块 + 单粒子对）同机制；**跨集一致性闭合基座序列 12/16/31/38/59**；主样本级闭合 ≠ 跨集闭合（n=8/9/10 三阶暴露）；摘要/推论 5.8/结论 13/诚实边界（⑩–⑫）/附录 A（+5 脚本）/变更记录同步。 |
| v0.25 | 2026-10-03 |"""
rep(old_log, new_log, "changelog")

with io.open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("Paper 58 v0.26 written, edits:", edits)
