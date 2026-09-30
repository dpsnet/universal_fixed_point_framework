# -*- coding: utf-8 -*-
"""Phase 71 阶段1 最终验证汇总：更新 results json（含 B1/B2/B3、T3 废弃说明）"""
import io, json

p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_single_minus_results.json"
with io.open(p, "r", encoding="utf-8") as f:
    data = json.load(f)

# T3 废弃：剥离振幅一致性(24)-(27) 必须在动量守恒壳上验证；
# 无动量守恒的一般半共线配置不满足定义(15)(16)的 δ²(Σλ) 支撑。
data["T3"] = {
    "note": "已废弃：剥离振幅定义含动量守恒 δ²(Σλ)，一般半共线(无动量守恒)配置下循环性/反射/U1/KK 无定义；正确验证见 B3（动量守恒配置）",
    "superseded_by": "B3",
}

# B1/B2/B3 结果（来自 paperX_single_minus_bg_recursion.py 2026-09-30 最终运行）
data["B1_BG_recursion_vs_formula39"] = {
    "note": "BG递归(18)-(21)独立实现 vs 通式(39)，R1+动量守恒，800样本/点",
    "n=3": {"fail": 0, "pass": True},
    "n=4": {"fail": 0, "pass": True},
    "n=5": {"fail": 0, "pass": True},
    "n=6": {"fail": 0, "pass": True},
    "conclusion": "通式(39)被独立递归实现完全确认（max_dev=0）——论文核心公式成立",
}
data["B2_BG_recursion_vs_explicit"] = {
    "note": "BG递归(21) vs 显式公式(29)-(32)，R1+动量守恒，800样本/点；"
           "n=5 残余 2/800 失败均为剥离振幅=0 的退化配置（预振幅Θ消失，公式(31)为generic位置公式）",
    "n=3": {"fail": 0, "pass": True},
    "n=4": {"fail": 0, "pass": True},
    "n=5": {"fail": 2, "pass": False, "note": "2例均为A_BG=0的退化配置"},
    "n=6": {"fail": 0, "pass": True},
}
data["B3_consistency_mom_cons"] = {
    "note": "BG递归(21)在动量守恒配置下满足全部一致性（500样本）",
    "cyclicity(24)": {"fail": 0, "pass": True},
    "reflection(25)": {"fail": 0, "pass": True},
    "U1_decoupling(26)": {"fail": 0, "pass": True},
    "KK(27)": {"fail": 0, "pass": True},
}
data["T1_note"] = "n=5 残余 13/2000 失败均为退化配置（A_R1=0 而 A5=±1，同 B2 机理）"

with io.open(p, "w", encoding="utf-8", newline="\n") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("results json 已更新为最终汇总")
