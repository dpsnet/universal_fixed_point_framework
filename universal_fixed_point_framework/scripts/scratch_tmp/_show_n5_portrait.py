import json

r = json.load(open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n5_criterion_results.json", encoding="utf-8"))
print("型1[(31)公式缺陷]:", r["attribution_type1_formula_defect"])
print("型2[符号结构不足]:", r["attribution_type2_symbol_insufficient"])
print("--- 16 个 A_BG 非决定性模式的取值画像 ---")
for p, d in sorted(r["nondeterministic_portrait"].items(), key=lambda kv: -kv[1]["count"]):
    print(f"pat=({p}) cnt={d['count']} A_BG_vals={d['A_BG_vals']} A5_vals={d['A5_vals']} agree={d['agree']} disagree={d['disagree']}")
