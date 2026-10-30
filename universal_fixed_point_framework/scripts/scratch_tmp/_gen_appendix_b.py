# -*- coding: utf-8 -*-
import json

r = json.load(open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n5_explicit_results.json", encoding="utf-8"))
NONDET = [(-1, 1, -1, -1, -1, -1, 1, -1), (1, -1, 1, 1, 1, 1, -1, 1),
          (1, 1, -1, -1, -1, -1, 1, -1), (-1, -1, 1, 1, 1, 1, -1, 1),
          (-1, -1, 1, 1, -1, -1, -1, -1), (1, 1, -1, -1, 1, 1, 1, 1),
          (-1, -1, 1, 1, -1, 1, -1, -1), (1, 1, -1, -1, 1, -1, 1, 1),
          (1, 1, 1, 1, -1, -1, 1, -1), (-1, -1, -1, -1, 1, 1, -1, 1),
          (1, -1, -1, -1, 1, 1, -1, 1), (-1, -1, 1, 1, -1, -1, 1, -1),
          (-1, 1, 1, 1, -1, -1, 1, -1), (1, 1, -1, -1, 1, 1, -1, 1)]
pat2name = {"6": "E6", "7": "E7"}

def fmt_val(x):
    try:
        return str(int(float(x)))
    except (TypeError, ValueError):
        return str(x)

lines = ["## 附录B：n=5 符号判据显式判定表（14/16 非决定性模式的单因子闭合）", ""]
lines.append("扩展因子记号：E6 = sg([λ12, λ123]) = sg([λ1+λ2, λ1+λ2+λ3])（列 6）；E7 = sg([λ12, λ1234]) = sg([λ1+λ2, λ1+λ2+λ3+λ4])（列 7）。下表为 14 个单因子闭合模式的显式判定：模式（8 个 (31) sg：s12,s23,s34,s45,s51,s123,s234,s1234）+ 对应单因子取值 → A_BG 唯一确定（数值验证，见命题 5.2 证明）。")
lines.append("")
lines.append("| 模式 (s12,s23,s34,s45,s51,s123,s234,s1234) | 判定因子 | E=+1 | E=−1 |")
lines.append("|:---|:---|:---|:---|")
for pat in NONDET:
    entry = r["table"].get(str(pat))
    if not entry:
        continue
    col = next(iter(entry))
    m = entry[col]
    vp = m.get("1", ["-"])[0]
    vm = m.get("-1", ["-"])[0]
    pat_str = ",".join(str(x) for x in pat)
    lines.append("| (%s) | %s | %s | %s |" % (pat_str, pat2name[col], fmt_val(vp), fmt_val(vm)))
out = "\n".join(lines)
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\paperX_n5_appendix_b.md", "w", encoding="utf-8") as f:
    f.write(out)
print(out)
print("---")
print("saved paperX_n5_appendix_b.md")
